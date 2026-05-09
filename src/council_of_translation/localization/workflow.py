import json
import logging
import re
import ast
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastmcp import Context

from council_of_translation.localization.prompt_builders import (
    build_chief_editor_prompt,
    build_conflict_review_prompt,
    build_reviewer_prompt,
)
from council_of_translation.localization.roles import get_reviewers_for_mode, normalize_mode
from council_of_translation.localization.schemas import (
    ChiefEditorDecision,
    ExampleRevision,
    Finding,
    ConflictReview,
    ReviewMode,
    ReviewRecord,
    ReviewResult,
    TranslationReviewTask,
)
from council_of_translation.security import safe_extract_text, sanitize_text


def build_unstructured_review_result(
    response_text: str,
    agent_name: str,
    role: str,
) -> ReviewResult:
    raw = sanitize_text(response_text, max_length=3000)
    if not raw:
        raw = "该评审员未返回可用文本。"

    return {
        "agent_name": agent_name,
        "role": role,
        "verdict": "有保留通过",
        "role_feedback": raw,
        "findings": [
            {
                "span": "",
                "issue_type": "other",
                "severity": "minor",
                "role_perspective": role,
                "problem": "该评审员未按 JSON schema 输出。",
                "evidence": raw,
                "action": "请主审结合原始评审文本保守裁决。",
            }
        ],
        "issues": ["该评审员未按 JSON schema 输出；以下依据原始评审文本供主审参考。"],
        "suggestions": [raw],
        "example_revisions": [],
        "confidence": "低",
        "rationale": raw,
    }


def extract_text_from_response(response: Any) -> str:
    try:
        if hasattr(response, "text"):
            return str(response.text)

        if hasattr(response, "content") and response.content:
            content_item = response.content[0]

            if hasattr(content_item, "text"):
                return str(content_item.text)

            if isinstance(content_item, dict) and "text" in content_item:
                return str(content_item["text"])

            content_str = safe_extract_text(str(content_item))
            match = re.search(r"text='(.+?)'(?:\s+annotations=|\s+meta=|$)", content_str, re.DOTALL)
            if not match:
                match = re.search(r'text="(.+?)"(?:\s+annotations=|\s+meta=|$)', content_str, re.DOTALL)
            if match:
                text = match.group(1)
                return text.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')

        return extract_text_from_sampling_repr(str(response))
    except (AttributeError, KeyError, IndexError, TypeError) as e:
        logging.warning(f"Failed to extract text from response: {e}")
        return ""


def extract_text_from_sampling_repr(response_text: str) -> str:
    content_str = safe_extract_text(response_text)

    # Goose may expose MCP sampling as a repr like:
    # SamplingResult(text='{"agent_name": ...}', result='{...}')
    match = re.search(
        r"text=(?P<quoted>'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")\s*,\s*result=",
        content_str,
        re.DOTALL,
    )
    if match:
        try:
            return str(ast.literal_eval(match.group("quoted")))
        except (SyntaxError, ValueError):
            quoted = match.group("quoted")
            return quoted[1:-1].replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')

    return content_str


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_json_object(text: str) -> dict[str, Any]:
    text = _strip_code_fence(text)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    json_fragment = extract_first_json_object(text)
    if json_fragment:
        try:
            parsed = json.loads(json_fragment)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    raise ValueError("Unable to parse JSON object from sampling response")


def extract_first_json_object(text: str) -> str:
    start = text.find("{")
    if start == -1:
        return ""

    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]

    return ""


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [sanitize_text(str(item), max_length=1000) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [sanitize_text(value, max_length=1000)]
    return []


def _normalize_issue_type(value: Any) -> str:
    if value in {"accuracy", "fluency", "style", "terminology", "context", "risk", "technical", "ux", "other"}:
        return str(value)
    return "other"


def _normalize_severity(value: Any) -> str:
    if value in {"critical", "major", "minor", "preference"}:
        return str(value)
    return "minor"


def _normalize_findings(value: Any, role: str) -> list[Finding]:
    if not isinstance(value, list):
        return []

    findings: list[Finding] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        problem = sanitize_text(str(item.get("problem") or ""), max_length=1000)
        action = sanitize_text(str(item.get("action") or ""), max_length=1000)
        if not problem and not action:
            continue
        findings.append(
            {
                "span": sanitize_text(str(item.get("span") or ""), max_length=500),
                "issue_type": _normalize_issue_type(item.get("issue_type")),  # type: ignore[typeddict-item]
                "severity": _normalize_severity(item.get("severity")),  # type: ignore[typeddict-item]
                "role_perspective": sanitize_text(str(item.get("role_perspective") or role), max_length=200),
                "problem": problem,
                "evidence": sanitize_text(str(item.get("evidence") or ""), max_length=1000),
                "action": action,
            }
        )
    return findings


def _normalize_example_revisions(value: Any, max_examples: int) -> list[ExampleRevision]:
    if not isinstance(value, list) or max_examples <= 0:
        return []

    examples: list[ExampleRevision] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        suggested = sanitize_text(str(item.get("suggested") or ""), max_length=500)
        if not suggested:
            continue
        examples.append(
            {
                "span": sanitize_text(str(item.get("span") or ""), max_length=300),
                "current": sanitize_text(str(item.get("current") or ""), max_length=500),
                "suggested": suggested,
                "reason": sanitize_text(str(item.get("reason") or ""), max_length=500),
            }
        )
        if len(examples) >= max_examples:
            break
    return examples


def normalize_output_mode(output_mode: str | None) -> str:
    if output_mode in {"review_only", "with_snippets", "full_rewrite"}:
        return output_mode
    return "review_only"


def normalize_conflict_review_mode(value: str | None) -> str:
    if value in {"off", "auto", "always"}:
        return value
    return "auto"


def _int_at_least(value: Any, default: int, minimum: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(parsed, minimum)


def effective_output_mode(task: TranslationReviewTask) -> str:
    requested = normalize_output_mode(task.get("output_mode"))
    text_size = len(task.get("source_text", "")) + len(task.get("candidate_translation", ""))
    if requested == "full_rewrite" and text_size > 4000:
        return "review_only"
    return requested


def enforce_output_mode_on_review(review: ReviewResult, task: TranslationReviewTask) -> ReviewResult:
    if effective_output_mode(task) == "review_only":
        review["example_revisions"] = []
    else:
        max_examples = _int_at_least(task.get("max_examples"), default=5, minimum=0)
        review["example_revisions"] = review.get("example_revisions", [])[:max_examples]
    if effective_output_mode(task) != "full_rewrite" and "recommended_translation" in review:
        del review["recommended_translation"]  # type: ignore[typeddict-item]
    return review


def normalize_review_result(raw: dict[str, Any], agent_name: str, role: str) -> ReviewResult:
    verdict = raw.get("verdict", "有保留通过")
    if verdict not in {"通过", "有保留通过", "不通过"}:
        verdict = "有保留通过"

    confidence = raw.get("confidence", "低")
    if confidence not in {"高", "中", "低"}:
        confidence = "低"

    role_feedback = sanitize_text(str(raw.get("role_feedback") or raw.get("rationale") or ""), max_length=2000)
    findings = _normalize_findings(raw.get("findings"), role)
    return {
        "agent_name": sanitize_text(str(raw.get("agent_name") or agent_name), max_length=100),
        "role": sanitize_text(str(raw.get("role") or role), max_length=100),
        "verdict": verdict,
        "role_feedback": role_feedback,
        "findings": findings,
        "issues": _string_list(raw.get("issues")),
        "suggestions": _string_list(raw.get("suggestions")),
        "example_revisions": _normalize_example_revisions(raw.get("example_revisions"), 5),
        "confidence": confidence,
        "rationale": sanitize_text(str(raw.get("rationale") or ""), max_length=2000),
    }


def normalize_conflict_review(raw: dict[str, Any], conflict: ConflictReview) -> ConflictReview:
    return {
        "conflict_id": sanitize_text(str(raw.get("conflict_id") or conflict["conflict_id"]), max_length=100),
        "topic": sanitize_text(str(raw.get("topic") or conflict["topic"]), max_length=500),
        "involved_agents": _string_list(raw.get("involved_agents")) or conflict["involved_agents"],
        "positions": _string_list(raw.get("positions")) or conflict["positions"],
        "resolution": sanitize_text(str(raw.get("resolution") or ""), max_length=1500),
        "rationale": sanitize_text(str(raw.get("rationale") or ""), max_length=1500),
    }


def normalize_chief_editor_decision(raw: dict[str, Any], task: TranslationReviewTask) -> ChiefEditorDecision:
    publishability = raw.get("publishability", "需人工复核")
    if publishability not in {"可发布", "修改后可发布", "需人工复核"}:
        publishability = "需人工复核"

    review_needed = raw.get("review_needed", "是")
    if review_needed not in {"是", "否"}:
        review_needed = "是"

    decision: ChiefEditorDecision = {
        "publishability": publishability,
        "must_fix": _string_list(raw.get("must_fix")),
        "should_fix": _string_list(raw.get("should_fix")),
        "optional_improvements": _string_list(raw.get("optional_improvements")),
        "example_revisions": _normalize_example_revisions(
            raw.get("example_revisions"),
            0 if effective_output_mode(task) == "review_only" else _int_at_least(task.get("max_examples"), default=5, minimum=0),
        ),
        "terminology_decisions": _string_list(raw.get("terminology_decisions")),
        "conflict_resolutions": _string_list(raw.get("conflict_resolutions")),
        "execution_order": _string_list(raw.get("execution_order")),
        "decision_rationale": sanitize_text(str(raw.get("decision_rationale") or ""), max_length=3000),
        "review_needed": review_needed,
        "review_reason": sanitize_text(str(raw.get("review_reason") or ""), max_length=2000),
    }
    if effective_output_mode(task) == "full_rewrite":
        suggested = raw.get("suggested_translation") or raw.get("recommended_translation") or task.get("candidate_translation", "")
        decision["suggested_translation"] = sanitize_text(str(suggested), max_length=12000)  # type: ignore[typeddict-unknown-key]
    return decision


def build_fallback_chief_editor_decision(
    task: TranslationReviewTask,
    reviews: list[ReviewResult],
    reason: str,
) -> ChiefEditorDecision:
    must_fix: list[str] = []
    should_fix: list[str] = []
    optional_improvements: list[str] = []

    for review in reviews:
        critical_or_major = [
            f"{finding['span']}: {finding['problem']} -> {finding['action']}".strip(": ")
            for finding in review.get("findings", [])
            if finding["severity"] in {"critical", "major"}
        ]
        minor_or_pref = [
            f"{finding['span']}: {finding['problem']} -> {finding['action']}".strip(": ")
            for finding in review.get("findings", [])
            if finding["severity"] in {"minor", "preference"}
        ]
        if review["verdict"] == "不通过":
            must_fix.extend(critical_or_major or review["issues"])
            should_fix.extend(review["suggestions"])
        elif review["verdict"] == "有保留通过":
            should_fix.extend(critical_or_major)
            optional_improvements.extend(minor_or_pref or review["issues"])
            optional_improvements.extend(review["suggestions"])

    if any(review["verdict"] == "不通过" for review in reviews):
        publishability = "修改后可发布"
    elif should_fix or optional_improvements:
        publishability = "修改后可发布"
    else:
        publishability = "可发布"

    # Keep fallback output compact; raw reviewer text can be long.
    must_fix = must_fix[:5]
    should_fix = should_fix[:8]
    optional_improvements = optional_improvements[:8]

    decision: ChiefEditorDecision = {
        "publishability": publishability,
        "must_fix": must_fix,
        "should_fix": should_fix,
        "optional_improvements": optional_improvements,
        "example_revisions": [],
        "terminology_decisions": [],
        "conflict_resolutions": [],
        "execution_order": (must_fix + should_fix + optional_improvements)[:8],
        "decision_rationale": sanitize_text(
            f"chief_editor 未返回可解析 JSON，已根据 reviewer 结构化结果和原始评审文本生成保守裁决。原因：{reason}",
            max_length=3000,
        ),
        "review_needed": "是",
        "review_reason": "主审输出格式异常；建议外层 Agent 参考 reviewer 意见后人工确认。",
    }
    if effective_output_mode(task) == "full_rewrite":
        decision["suggested_translation"] = task.get("candidate_translation", "")  # type: ignore[typeddict-unknown-key]
    return decision


def detect_conflicts(task: TranslationReviewTask, reviews: list[ReviewResult]) -> list[ConflictReview]:
    mode = normalize_conflict_review_mode(task.get("enable_conflict_review"))
    if mode == "off":
        return []

    max_conflicts = _int_at_least(task.get("max_conflicts"), default=2, minimum=0)
    if max_conflicts == 0:
        return []

    conflicts: list[ConflictReview] = []
    combined = "\n".join(
        [
            f"{review['agent_name']}\n"
            + "\n".join(
                review["issues"]
                + review["suggestions"]
                + [review.get("role_feedback", ""), review["rationale"]]
                + [
                    f"{finding['span']} {finding['issue_type']} {finding['severity']} {finding['problem']} {finding['action']}"
                    for finding in review.get("findings", [])
                ]
            )
            for review in reviews
        ]
    )

    def add_conflict(topic: str, agents: list[str], positions: list[str]):
        if len(conflicts) >= max_conflicts:
            return
        conflicts.append(
            {
                "conflict_id": f"conflict_{len(conflicts) + 1}",
                "topic": topic,
                "involved_agents": agents,
                "positions": positions,
                "resolution": "",
                "rationale": "",
            }
        )

    findings_by_span: dict[str, list[tuple[str, Finding]]] = {}
    for review in reviews:
        for finding in review.get("findings", []):
            span = finding.get("span", "").strip()
            if not span:
                continue
            findings_by_span.setdefault(span.lower(), []).append((review["agent_name"], finding))

    for span, span_findings in findings_by_span.items():
        if len(span_findings) < 2:
            continue
        severities = {finding["severity"] for _, finding in span_findings}
        issue_types = {finding["issue_type"] for _, finding in span_findings}
        actions = {finding["action"] for _, finding in span_findings if finding["action"]}
        has_meaningful_difference = len(severities) > 1 or len(issue_types) > 1 or len(actions) > 1
        if not has_meaningful_difference:
            continue
        add_conflict(
            f"同一片段的评审意见需要裁决：{span}",
            [agent for agent, _ in span_findings],
            [
                f"{agent}: {finding['severity']}/{finding['issue_type']} - {finding['problem']} -> {finding['action']}"
                for agent, finding in span_findings
            ],
        )

    if ("同意" in combined and ("permission" in combined.lower() or "授权" in combined or "许可" in combined)):
        add_conflict(
            "permissions/consent 的译法是否应加入“同意”",
            ["fidelity_reviewer", "risk_ambiguity_reviewer"],
            [
                "忠实度视角通常倾向避免超出原文 permissions 的义务等级。",
                "风险视角可能倾向更稳妥的合规措辞。",
            ],
        )

    if ("保留英文" in combined or "英文括注" in combined or "中文化" in combined) and (
        "human-in-the-loop" in combined or "round-trip" in combined or "source-cited" in combined
    ):
        add_conflict(
            "半固定英文技术术语应保留英文括注还是中文化",
            ["terminology_reviewer", "fluency_reviewer", "technical_safety_reviewer"],
            [
                "术语/技术安全视角倾向保留英文锚点以稳定映射。",
                "自然度/UX 视角倾向中文可读性和扫读效率。",
            ],
        )

    if ("speaker preservation" in combined and ("声音风格" in combined or "说话人特征" in combined)):
        add_conflict(
            "speaker preservation 应译为说话人特征保留还是声音风格相关表达",
            ["fidelity_reviewer", "terminology_reviewer", "risk_ambiguity_reviewer"],
            [
                "术语一致性视角倾向固定为“说话人特征保留”。",
                "风险/产品语境视角关注是否扩大为 voice style preservation。",
            ],
        )

    if mode == "always" and not conflicts and reviews:
        add_conflict(
            "是否存在需要主审特别裁决的评审分歧",
            [review["agent_name"] for review in reviews[:3]],
            ["未检测到明确关键词冲突；请确认是否仅需按优先级汇总。"],
        )

    return conflicts[:max_conflicts]


async def run_conflict_reviews(
    task: TranslationReviewTask,
    reviews: list[ReviewResult],
    ctx: "Context",
) -> list[ConflictReview]:
    conflicts = detect_conflicts(task, reviews)
    resolved: list[ConflictReview] = []

    for conflict in conflicts:
        ctx.info(f"Sampling targeted conflict review: {conflict['conflict_id']}")
        try:
            prompt = build_conflict_review_prompt(task, conflict)
            response = await ctx.sample(prompt, temperature=0.2, max_tokens=900)
            response_text = extract_text_from_response(response)
            raw = parse_json_object(response_text)
            resolved.append(normalize_conflict_review(raw, conflict))
        except Exception as e:
            logging.warning(f"Conflict review failed for {conflict['conflict_id']}: {e}")
            conflict["resolution"] = "冲突复议未返回可解析结果；请主审按角色优先级裁决。"
            conflict["rationale"] = str(e)
            resolved.append(conflict)

    return resolved


def build_review_id() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_review_record(record: ReviewRecord, reviews_dir: str = "reviews") -> str:
    reviews_path = Path(reviews_dir)
    reviews_path.mkdir(exist_ok=True)
    file_path = reviews_path / f"{record['review_id']}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return str(file_path)


async def run_translation_review(task: TranslationReviewTask, ctx: "Context") -> ReviewRecord:
    mode: ReviewMode = normalize_mode(task.get("mode"))
    review_id = task.get("task_id") or build_review_id()
    task["task_id"] = review_id
    task["mode"] = mode
    task["output_mode"] = effective_output_mode(task)  # type: ignore[typeddict-item]
    task["enable_conflict_review"] = normalize_conflict_review_mode(task.get("enable_conflict_review"))  # type: ignore[typeddict-item]
    task["max_examples"] = _int_at_least(task.get("max_examples"), default=5, minimum=0)  # type: ignore[typeddict-item]
    task["max_conflicts"] = _int_at_least(task.get("max_conflicts"), default=2, minimum=0)  # type: ignore[typeddict-item]

    reviewers = get_reviewers_for_mode(mode)
    reviews: list[ReviewResult] = []

    ctx.info(f"Starting localization review {review_id} in {mode} mode")
    for index, role in enumerate(reviewers, 1):
        ctx.info(f"Sampling {role.agent_name} ({index}/{len(reviewers)})")
        prompt = build_reviewer_prompt(role, task)
        response_text = ""
        try:
            response = await ctx.sample(prompt, temperature=0.2, max_tokens=1400)
            response_text = extract_text_from_response(response)
            raw_result = parse_json_object(response_text)
            reviews.append(enforce_output_mode_on_review(normalize_review_result(raw_result, role.agent_name, role.role), task))
        except Exception as e:
            logging.warning(f"Reviewer {role.agent_name} returned unstructured output: {e}")
            reviews.append(enforce_output_mode_on_review(build_unstructured_review_result(response_text, role.agent_name, role.role), task))

    conflict_reviews = await run_conflict_reviews(task, reviews, ctx)
    ctx.info("Sampling chief_editor")
    try:
        editor_prompt = build_chief_editor_prompt(task, reviews, conflict_reviews)
        response = await ctx.sample(editor_prompt, temperature=0.2, max_tokens=2400)
        response_text = extract_text_from_response(response)
        raw_decision = parse_json_object(response_text)
        decision = normalize_chief_editor_decision(raw_decision, task)
    except Exception as e:
        logging.warning(f"Chief editor returned unstructured output: {e}")
        decision = build_fallback_chief_editor_decision(task, reviews, str(e))

    record: ReviewRecord = {
        "review_id": review_id,
        "task": task,
        "mode": mode,
        "status": "completed",
        "reviews": reviews,
        "conflict_reviews": conflict_reviews,
        "chief_editor_decision": decision,
    }

    file_path = save_review_record(record)
    ctx.info(f"Localization review saved to: {file_path}")
    return record
