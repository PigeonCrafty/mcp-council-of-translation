"""Deterministic guided-session briefing helpers.

The helpers are sampling-free and deliberately separate user-provided answers
from bounded Council assumptions.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Literal

from pydantic import Field, create_model

from council_of_translation.localization.models import (
    BriefingInteraction,
    ContextGapV2,
    ReviewBriefV2,
    ReviewTaskV2,
)
from council_of_translation.localization.roles import normalize_content_type


INFER_VALUE = "不确定，由 Council 推断"
CONTENT_VALUES = ("界面文案", "营销文案", "技术文档", "法律或风险文案", INFER_VALUE)
CONTENT_VALUE_MAP = {
    "界面文案": "ui",
    "营销文案": "marketing",
    "技术文档": "technical_documentation",
    "法律或风险文案": "legal_risk",
    INFER_VALUE: "unspecified",
}
BRIEF_FIELDS = ("domain", "content_type", "audience", "tone_goal", "primary_focus", "usage_context")
CONTEXT_ASSUMPTION_VALUE = "由 Council 按现有证据继续，不提供额外背景"


def _provided_context_count(task: ReviewTaskV2) -> int:
    values = (
        normalize_content_type(task.content_type) != "unspecified",
        bool(task.context.strip()),
        bool(task.audience.strip()),
        bool(task.term_glossary.strip() or task.style_guide.strip()),
        bool(task.project_rules.strip() or task.brand_guidelines.strip()),
        bool(task.technical_constraints.strip() or task.reference_translations.strip()),
    )
    return sum(values)


def _provided_context_category_count(task: ReviewTaskV2) -> int:
    categories = (
        bool(task.context.strip() or task.reference_translations.strip()),
        bool(task.audience.strip()),
        bool(task.style_guide.strip() or task.brand_guidelines.strip()),
        bool(
            task.term_glossary.strip()
            or task.project_rules.strip()
            or task.technical_constraints.strip()
        ),
    )
    return sum(categories)


def context_is_sufficient(task: ReviewTaskV2) -> bool:
    """Return a transparent, sampling-free sufficiency decision."""
    content_type_is_recognized = normalize_content_type(task.content_type) != "unspecified"
    return content_type_is_recognized and _provided_context_category_count(task) >= 2


def briefing_fields(task: ReviewTaskV2) -> list[str]:
    missing: list[str] = []
    if not task.context.strip():
        missing.extend(["domain", "usage_context"])
    if normalize_content_type(task.content_type) == "unspecified":
        missing.append("content_type")
    if not task.audience.strip():
        missing.append("audience")
    if not (task.style_guide.strip() or task.brand_guidelines.strip()):
        missing.append("tone_goal")
    if not (task.project_rules.strip() or task.notes.strip()):
        missing.append("primary_focus")
    ordered = [name for name in BRIEF_FIELDS if name in missing]
    return ordered[:6] or list(BRIEF_FIELDS)


def should_request_briefing(task: ReviewTaskV2, *, supported: bool) -> bool:
    del supported  # capability affects the recorded action, not whether a brief is needed
    if task.briefing_mode == "off":
        return False
    if task.briefing_mode == "always":
        return True
    return not context_is_sufficient(task)


def build_briefing_form(fields: list[str]) -> type:
    definitions: dict[str, tuple[Any, Any]] = {}
    for name in fields[:6]:
        if name == "content_type":
            value_type = Literal.__getitem__(CONTENT_VALUES)
            definitions[name] = (
                value_type,
                Field(
                    title="内容类型",
                    description="选择译文实际出现的位置或用途；不确定时可交由 Council 推断。",
                ),
            )
        else:
            title, description = {
                "domain": ("业务领域", "例如支付、协作或开发者工具；可留空。"),
                "audience": ("目标读者", "说明主要读者及其熟悉程度；可留空。"),
                "tone_goal": ("语气与沟通目标", "说明希望读者感受到什么或完成什么；可留空。"),
                "primary_focus": ("本次审校重点", "说明最值得优先判断的一项质量目标；可留空。"),
                "usage_context": ("使用场景", "说明组件、页面、流程阶段或相邻操作；可留空。"),
            }[name]
            definitions[name] = (
                str,
                Field(default="", title=title, description=description, max_length=240),
            )
    return create_model("CouncilBriefingForm", **definitions)


def briefing_message(fields: list[str]) -> str:
    labels = {
        "domain": "业务领域", "content_type": "内容类型", "audience": "目标读者",
        "tone_goal": "语气与沟通目标", "primary_focus": "本次审校重点", "usage_context": "使用场景",
    }
    return "为了让各角色按真实场景审校，请补充以下简短背景（不确定项可交由 Council 推断）：" + "、".join(
        labels[name] for name in fields[:6]
    )


def build_effective_brief(
    task: ReviewTaskV2,
    *,
    accepted_answers: dict[str, str] | None = None,
) -> tuple[ReviewBriefV2, ReviewTaskV2]:
    answers = {
        key: value.strip()[:240]
        for key, value in (accepted_answers or {}).items()
        if key in BRIEF_FIELDS and isinstance(value, str) and value.strip()
    }
    normalized = normalize_content_type(task.content_type)
    content_value = normalized
    content_provenance = "normalized_alias" if normalized != "unspecified" else "inferred_default"
    if "content_type" in answers:
        content_value = CONTENT_VALUE_MAP.get(answers["content_type"], "unspecified")
        content_provenance = "user_briefing"

    updated = task.model_copy(deep=True)
    if "content_type" in answers:
        updated.content_type = content_value
    if "audience" in answers:
        updated.audience = answers["audience"]
    if "usage_context" in answers:
        updated.context = answers["usage_context"]

    provenance: dict[str, Any] = {
        "domain": "inferred_default",
        "content_type": content_provenance,
        "location": "normalized_alias" if content_value != "unspecified" else "inferred_default",
        "audience": "caller" if task.audience else "inferred_default",
        "tone_goal": "caller" if (task.style_guide or task.brand_guidelines) else "inferred_default",
        "primary_focus": "caller" if (task.project_rules or task.notes) else "inferred_default",
        "usage_context": "caller" if task.context else "inferred_default",
    }
    for key in answers:
        provenance[key] = "user_briefing"

    supplied = _provided_context_count(updated)
    confidence = (
        "full" if supplied >= 4 or len(answers) >= 4
        else "partial" if supplied >= 1 or answers
        else "minimal"
    )
    assumptions: list[str] = []
    if content_value == "unspecified":
        assumptions.append("内容类型未知；Council 采用通用本地化审校视角。")
    if not updated.audience:
        assumptions.append("目标读者未知；不假定专业知识水平。")
    if not updated.context:
        assumptions.append("使用场景未知；产品语境判断按有限证据处理。")
    return ReviewBriefV2(
        domain=answers.get("domain", "unspecified"),
        content_type=content_value,
        location=content_value,
        audience=updated.audience,
        tone_goal=answers.get("tone_goal", task.brand_guidelines or task.style_guide),
        primary_focus=answers.get("primary_focus", task.project_rules or task.notes),
        usage_context=updated.context,
        assumptions=assumptions,
        context_confidence=confidence,
        field_provenance=provenance,
    ), updated


def normalize_briefing_answers(fields: list[str], data: Any) -> dict[str, str] | None:
    if not isinstance(data, dict) or set(data) != set(fields):
        return None
    answers: dict[str, str] = {}
    for name in fields:
        value = data.get(name)
        if not isinstance(value, str) or len(value) > 240:
            return None
        if name == "content_type" and value not in CONTENT_VALUES:
            return None
        if value.strip():
            answers[name] = value.strip()
    return answers


def briefing_interaction(
    *, fields: list[str], action: str, answers: dict[str, str] | None = None, requested: bool = True,
) -> BriefingInteraction:
    normalized_action = action if action in {"accept", "decline", "cancel", "unsupported", "malformed", "error", "skipped"} else "malformed"
    accepted = answers if normalized_action == "accept" and answers is not None else {}
    return BriefingInteraction(
        requested=requested,
        action=normalized_action,
        asked_fields=fields if requested else [],
        accepted_answers=accepted,
        answer_provenance={key: "user_briefing" for key in accepted},
        retry_hint=(
            "请以 briefing_mode=auto 或 always 重试并接受背景表单，或明确使用 briefing_mode=off。"
            if requested and normalized_action != "accept" else ""
        ),
    )


def parse_context_gaps(raw: Any, role_id: str) -> tuple[list[ContextGapV2], int]:
    """Parse gaps independently so malformed gap prose cannot erase findings."""
    if raw is None:
        return [], 0
    if not isinstance(raw, list):
        return [], 1
    parsed: list[ContextGapV2] = []
    invalid = max(0, len(raw) - 5)
    for item in raw[:5]:
        if not isinstance(item, dict):
            invalid += 1
            continue
        question = item.get("question", "")
        materiality = item.get("materiality", "")
        affected = item.get("affected_role_ids", [role_id])
        if (
            not isinstance(question, str)
            or not question.strip()
            or len(question) > 1_000
            or not isinstance(materiality, str)
            or not materiality.strip()
            or len(materiality) > 1_000
            or not isinstance(affected, list)
            or any(not isinstance(value, str) for value in affected)
        ):
            invalid += 1
            continue
        digest = hashlib.sha256(
            f"{question.strip().casefold()}\x1f{materiality.strip().casefold()}".encode("utf-8")
        ).hexdigest()[:12]
        parsed.append(ContextGapV2(
            gap_id=f"gap_{digest}",
            question=question,
            materiality=materiality,
            affected_role_ids=list(dict.fromkeys(affected or [role_id])),
            source_role_id=role_id,
            provenance="model",
        ))
    return parsed, invalid


def _gap_is_answered(gap: ContextGapV2, brief: ReviewBriefV2) -> bool:
    question = gap.question.casefold()
    checks = (
        (("audience", "读者", "用户"), bool(brief.audience)),
        (("context", "场景", "页面", "组件", "位置"), bool(brief.usage_context)),
        (("tone", "语气", "风格"), bool(brief.tone_goal)),
        (("domain", "领域", "业务"), brief.domain != "unspecified"),
        (("content type", "内容类型"), brief.content_type != "unspecified"),
    )
    return any(value and any(token in question for token in tokens) for tokens, value in checks)


def select_context_gaps(
    gaps: list[ContextGapV2], brief: ReviewBriefV2,
) -> tuple[list[ContextGapV2], list[ContextGapV2]]:
    """Select at most two material unanswered gaps with stable semantic dedupe."""
    selected: list[ContextGapV2] = []
    all_gaps: list[ContextGapV2] = []
    seen: set[str] = set()
    material_terms = ("改变", "影响", "判断", "结论", "选项", "建议", "change", "affect", "outcome", "decision")
    generic = ("more context", "更多背景", "还有什么", "anything else")
    for gap in gaps:
        normalized = re.sub(r"\W+", "", gap.question.casefold())
        update: dict[str, str] = {}
        if normalized in seen:
            update = {"disposition": "suppressed", "reason": "duplicate_gap"}
        elif _gap_is_answered(gap, brief):
            update = {"disposition": "suppressed", "reason": "already_answered"}
        elif any(term in gap.question.casefold() for term in generic):
            update = {"disposition": "suppressed", "reason": "generic_curiosity"}
        elif not any(term in gap.materiality.casefold() for term in material_terms):
            update = {"disposition": "suppressed", "reason": "immaterial_gap"}
        elif len(selected) >= 2:
            update = {"disposition": "suppressed", "reason": "question_limit"}
        if update:
            bounded = gap.model_copy(update=update)
        else:
            bounded = gap
            selected.append(bounded)
            seen.add(normalized)
        all_gaps.append(bounded)
    return selected, all_gaps


def build_context_gap_form(gaps: list[ContextGapV2]) -> tuple[type, dict[str, ContextGapV2]]:
    fields: dict[str, tuple[Any, Any]] = {}
    mapping: dict[str, ContextGapV2] = {}
    for index, gap in enumerate(gaps[:2], start=1):
        field_name = f"context_{index}"
        mapping[field_name] = gap
        fields[field_name] = (
            str,
            Field(
                title=f"补充背景 {index}",
                description=(
                    f"{gap.question[:120]} 回答会影响：{gap.materiality[:120]}。"
                    f"若不提供，请填写“{CONTEXT_ASSUMPTION_VALUE}”。"
                )[:160],
                min_length=1,
                max_length=240,
            ),
        )
    return create_model("CouncilContextGapForm", **fields), mapping


def context_gap_message(gaps: list[ContextGapV2]) -> str:
    lines = ["以下背景可能改变专业判断；请在一个表单中回答（最多两项）："]
    for index, gap in enumerate(gaps[:2], start=1):
        lines.append(f"{index}. {gap.question[:160]}")
    return "\n".join(lines)


def normalize_context_answers(
    mapping: dict[str, ContextGapV2], data: Any,
) -> dict[str, str] | None:
    if not isinstance(data, dict) or set(data) != set(mapping):
        return None
    answers: dict[str, str] = {}
    for field_name, gap in mapping.items():
        value = data.get(field_name)
        if not isinstance(value, str) or not value.strip() or len(value) > 240:
            return None
        answers[gap.gap_id] = value.strip()
    return answers
