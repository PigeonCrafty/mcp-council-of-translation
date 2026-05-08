import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fastmcp import Context

from council_of_translation.localization.prompt_builders import (
    build_chief_editor_prompt,
    build_reviewer_prompt,
)
from council_of_translation.localization.roles import get_reviewers_for_mode, normalize_mode
from council_of_translation.localization.schemas import (
    ChiefEditorDecision,
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
        "issues": ["该评审员未按 JSON schema 输出；以下依据原始评审文本供主审参考。"],
        "suggestions": [raw],
        "recommended_translation": "",
        "confidence": "低",
        "rationale": raw,
    }


def extract_text_from_response(response: Any) -> str:
    try:
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

        return str(response)
    except (AttributeError, KeyError, IndexError, TypeError) as e:
        logging.warning(f"Failed to extract text from response: {e}")
        return ""


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

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    raise ValueError("Unable to parse JSON object from sampling response")


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [sanitize_text(str(item), max_length=1000) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [sanitize_text(value, max_length=1000)]
    return []


def normalize_review_result(raw: dict[str, Any], agent_name: str, role: str) -> ReviewResult:
    verdict = raw.get("verdict", "有保留通过")
    if verdict not in {"通过", "有保留通过", "不通过"}:
        verdict = "有保留通过"

    confidence = raw.get("confidence", "低")
    if confidence not in {"高", "中", "低"}:
        confidence = "低"

    return {
        "agent_name": sanitize_text(str(raw.get("agent_name") or agent_name), max_length=100),
        "role": sanitize_text(str(raw.get("role") or role), max_length=100),
        "verdict": verdict,
        "issues": _string_list(raw.get("issues")),
        "suggestions": _string_list(raw.get("suggestions")),
        "recommended_translation": sanitize_text(str(raw.get("recommended_translation") or ""), max_length=3000),
        "confidence": confidence,
        "rationale": sanitize_text(str(raw.get("rationale") or ""), max_length=2000),
    }


def normalize_chief_editor_decision(raw: dict[str, Any], task: TranslationReviewTask) -> ChiefEditorDecision:
    publishability = raw.get("publishability", "需人工复核")
    if publishability not in {"可发布", "修改后可发布", "需人工复核"}:
        publishability = "需人工复核"

    review_needed = raw.get("review_needed", "是")
    if review_needed not in {"是", "否"}:
        review_needed = "是"

    candidate = task.get("candidate_translation", "")
    return {
        "publishability": publishability,
        "must_fix": _string_list(raw.get("must_fix")),
        "optional_improvements": _string_list(raw.get("optional_improvements")),
        "recommended_translation": sanitize_text(
            str(raw.get("recommended_translation") or candidate),
            max_length=3000,
        ),
        "alternatives": _string_list(raw.get("alternatives")),
        "decision_rationale": sanitize_text(str(raw.get("decision_rationale") or ""), max_length=3000),
        "review_needed": review_needed,
        "review_reason": sanitize_text(str(raw.get("review_reason") or ""), max_length=2000),
    }


def build_fallback_chief_editor_decision(
    task: TranslationReviewTask,
    reviews: list[ReviewResult],
    reason: str,
) -> ChiefEditorDecision:
    must_fix: list[str] = []
    optional_improvements: list[str] = []
    recommended_translation = task.get("candidate_translation", "")

    for review in reviews:
        if review["verdict"] == "不通过":
            must_fix.extend(review["issues"])
            must_fix.extend(review["suggestions"])
        elif review["verdict"] == "有保留通过":
            optional_improvements.extend(review["issues"])
            optional_improvements.extend(review["suggestions"])

        if not recommended_translation and review["recommended_translation"]:
            recommended_translation = review["recommended_translation"]

    if any(review["verdict"] == "不通过" for review in reviews):
        publishability = "修改后可发布"
    elif optional_improvements:
        publishability = "修改后可发布"
    else:
        publishability = "可发布"

    # Keep fallback output compact; raw reviewer text can be long.
    must_fix = must_fix[:5]
    optional_improvements = optional_improvements[:8]

    return {
        "publishability": publishability,
        "must_fix": must_fix,
        "optional_improvements": optional_improvements,
        "recommended_translation": recommended_translation,
        "alternatives": [],
        "decision_rationale": sanitize_text(
            f"chief_editor 未返回可解析 JSON，已根据 reviewer 结构化结果和原始评审文本生成保守裁决。原因：{reason}",
            max_length=3000,
        ),
        "review_needed": "是",
        "review_reason": "主审输出格式异常；建议外层 Agent 参考 reviewer 意见后人工确认。",
    }


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

    reviewers = get_reviewers_for_mode(mode)
    reviews: list[ReviewResult] = []

    ctx.info(f"Starting localization review {review_id} in {mode} mode")
    for index, role in enumerate(reviewers, 1):
        ctx.info(f"Sampling {role.agent_name} ({index}/{len(reviewers)})")
        prompt = build_reviewer_prompt(role, task)
        response_text = ""
        try:
            response = await ctx.sample(prompt, temperature=0.2, max_tokens=900)
            response_text = extract_text_from_response(response)
            raw_result = parse_json_object(response_text)
            reviews.append(normalize_review_result(raw_result, role.agent_name, role.role))
        except Exception as e:
            logging.warning(f"Reviewer {role.agent_name} returned unstructured output: {e}")
            reviews.append(build_unstructured_review_result(response_text, role.agent_name, role.role))

    ctx.info("Sampling chief_editor")
    try:
        editor_prompt = build_chief_editor_prompt(task, reviews)
        response = await ctx.sample(editor_prompt, temperature=0.2, max_tokens=1200)
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
        "chief_editor_decision": decision,
    }

    file_path = save_review_record(record)
    ctx.info(f"Localization review saved to: {file_path}")
    return record
