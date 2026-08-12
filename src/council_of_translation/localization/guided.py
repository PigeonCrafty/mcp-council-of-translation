"""Deterministic guided-session briefing helpers.

The helpers are sampling-free and deliberately separate user-provided answers
from bounded Council assumptions.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, create_model

from council_of_translation.localization.models import (
    BriefingInteraction,
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


def context_is_sufficient(task: ReviewTaskV2) -> bool:
    """Return a transparent, sampling-free sufficiency decision."""
    return _provided_context_count(task) >= 3


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
    confidence = "full" if supplied >= 4 else "partial" if supplied >= 1 else "minimal"
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
        if value.strip() and not (name == "content_type" and value == INFER_VALUE):
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
