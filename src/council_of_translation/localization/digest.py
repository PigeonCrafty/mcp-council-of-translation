"""Deterministic process-first digest and bounded display report."""

from __future__ import annotations

import re
from typing import Any

from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    ContextGapV2,
    CouncilPlan,
    IssueCluster,
    MinorityReport,
    PhaseReconsiderationProvenance,
    ProcessDigestV2,
    ReviewBriefV2,
    RoleLens,
    UserDecision,
)
from council_of_translation.localization.roles import ROLE_REGISTRY


def _semantic_key(value: str) -> str:
    return re.sub(r"[^\w\u3400-\u9fff]+", "", value.casefold())[:160]


def _dedupe(values: list[str], *, maximum: int = 8) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        bounded = str(value).strip()[:240]
        key = _semantic_key(bounded)
        if not bounded or not key or key in seen:
            continue
        if any(key in previous or previous in key for previous in seen if len(key) > 24):
            continue
        seen.add(key)
        result.append(bounded)
        if len(result) >= maximum:
            break
    return result


def _role_lenses(plan: CouncilPlan, reviews: list[dict[str, Any]]) -> list[RoleLens]:
    by_role = {
        str(review.get("agent_name", "")): review
        for review in reviews
        if isinstance(review, dict)
    }
    lenses: list[RoleLens] = []
    for role_id in plan.active_role_ids:
        review = by_role.get(role_id, {})
        findings = review.get("findings", []) if isinstance(review.get("findings", []), list) else []
        evidence = _dedupe([
            str(item.get("evidence") or item.get("problem") or "")
            for item in findings
            if isinstance(item, dict)
        ], maximum=4)
        feedback = str(review.get("role_feedback", "")).strip()
        if not feedback:
            feedback = "该角色的结构化评审不可用，未据此推断无问题。"
        status = str(review.get("sample_status", "unavailable"))
        lenses.append(RoleLens(
            role_id=role_id,
            perspective=feedback,
            evidence=evidence,
            disposition=(
                "完成职责内审校" if status == "structured_success" else "采样不可用，保留为盲区"
            ),
        ))
    return lenses


def build_process_digest(
    *,
    task: Any,
    brief: ReviewBriefV2,
    plan: CouncilPlan,
    independent_reviews: list[dict[str, Any]],
    clusters: list[IssueCluster],
    context_gaps: list[ContextGapV2],
    user_decisions: list[UserDecision],
    context_provenance: PhaseReconsiderationProvenance,
    outcome_provenance: PhaseReconsiderationProvenance,
    chief: ChiefEditorDecisionV2,
    reviewer_coverage: str,
) -> ProcessDigestV2:
    consensus = _dedupe([cluster.topic for cluster in clusters if cluster.consensus_status == "consensus"])
    disagreements = _dedupe([cluster.topic for cluster in clusters if cluster.consensus_status == "disputed"])
    minority_cluster = next(
        (cluster for cluster in clusters if cluster.consensus_status == "disputed"),
        None,
    )
    blind_spots: list[str] = []
    if reviewer_coverage != "full":
        blind_spots.append(f"独立评审覆盖为 {reviewer_coverage}；缺失角色不能解释为无问题。")
    blind_spots.extend(
        f"未回答背景：{gap.question}"
        for gap in context_gaps
        if gap.disposition == "unanswered"
    )
    blind_spots.extend(brief.assumptions)
    if not blind_spots:
        blind_spots.append("未识别额外盲区；结论仍限于调用方提供的文本与规则包。")

    gap_lines = []
    for gap in context_gaps:
        if gap.disposition == "answered":
            gap_lines.append(f"{gap.question} → 已回答：{gap.answer}")
        elif gap.disposition == "suppressed":
            gap_lines.append(f"{gap.question} → 已抑制（{gap.reason}）")
        else:
            gap_lines.append(f"{gap.question} → 未回答")

    decision_lines = []
    for decision in user_decisions:
        if decision.elicitation_action == "accept":
            decision_lines.append(f"用户选择：{decision.selected_outcome_value}")
        elif decision.elicitation_action == "delegate":
            decision_lines.append("用户明确委托 Council 按证据裁决。")
        else:
            decision_lines.append(f"用户决策交互：{decision.elicitation_action}")

    changes = [
        *(f"背景重审：{value}" for value in context_provenance.change_effects),
        *(f"结果重审：{value}" for value in outcome_provenance.change_effects),
    ]
    checklist = [
        *(f"必须修复：{item}" for item in chief.must_fix),
        *(f"建议修复：{item}" for item in chief.should_fix),
        *(f"可选改进：{item}" for item in chief.optional_improvements),
        *(f"执行顺序：{item}" for item in chief.execution_order),
        f"最终处置：{chief.publishability}；需人工复核：{chief.review_needed}",
    ]
    return ProcessDigestV2(
        case_brief=_dedupe([
            f"语言方向：{task.source_language} → {task.target_language}",
            f"领域/内容类型：{brief.domain} / {brief.content_type}",
            f"受众：{brief.audience or '未提供'}",
            f"审校重点：{brief.primary_focus or '按角色职责执行'}",
        ]),
        assumptions_context_confidence=_dedupe([
            f"上下文置信度：{brief.context_confidence}",
            *brief.assumptions,
        ]),
        blind_spots=_dedupe(blind_spots),
        role_lenses=_role_lenses(plan, independent_reviews),
        consensus=consensus or ["未形成需合并的实质共识项。"],
        minority_report=MinorityReport(
            dissent=minority_cluster.topic if minority_cluster else "未识别有效少数异议。",
            decisive_condition=(
                "若补充证据使该异议触及语义、技术完整性或显式规则，则其将成为决定性条件。"
                if minority_cluster else "若出现新的语义、技术或显式规则证据，应重新评审。"
            ),
            role_ids=minority_cluster.participant_role_ids if minority_cluster else [],
        ),
        material_disagreements=disagreements or ["无已记录的实质分歧。"],
        context_gaps_answers=_dedupe(gap_lines) or ["未提出需跟进的实质背景问题。"],
        user_decisions=_dedupe(decision_lines) or ["未请求用户结果选择。"],
        reconsideration_changes=_dedupe(changes) or ["未触发重审。"],
        editor_synthesis=_dedupe([
            chief.decision_rationale or "主编依据 Policy Gate 与角色证据完成综合。",
            chief.review_reason,
        ]),
        execution_checklist_final_disposition=_dedupe(checklist),
    )


_NO_OP_PREFIXES = (
    "未提出需跟进", "未请求用户", "未触发重审", "未识别有效少数异议",
)


def _human_line(value: str, maximum: int = 120) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text if len(text) <= maximum else text[: maximum - 1].rstrip() + "…"


def _material(values: list[str], *, maximum: int = 3) -> list[str]:
    return [
        _human_line(value)
        for value in values
        if value and not value.startswith(_NO_OP_PREFIXES)
    ][:maximum]


def _section(title: str, values: list[str]) -> list[str]:
    return [f"## {title}", *(f"- {value}" for value in values)] if values else []


def _role_lines(digest: ProcessDigestV2) -> list[str]:
    lines: list[str] = []
    for lens in digest.role_lenses[:8]:
        role = ROLE_REGISTRY.get(lens.role_id)
        label = role.display_name if role else "未识别专业角色"
        perspective = _human_line(lens.perspective or lens.disposition, 120)
        evidence = _material(lens.evidence, maximum=1)
        suffix = f"；依据：{_human_line(evidence[0], 80)}" if evidence else ""
        lines.append(_human_line(f"{label}：{perspective}{suffix}", 150))
    return lines


def render_display_report(
    digest: ProcessDigestV2,
    *,
    status: str = "",
    degraded: bool = False,
    warnings: list[str] | None = None,
    fallback_reason: str = "",
) -> str:
    """Render an adaptive Chinese report while preserving the 12-field digest."""
    background = _material(digest.case_brief, maximum=4)
    background.extend(_material(digest.assumptions_context_confidence, maximum=2))

    deliberation = [
        *(f"共识：{value}" for value in _material(digest.consensus, maximum=2)),
        *(f"分歧：{value}" for value in _material(digest.material_disagreements, maximum=2)),
        *(f"盲区：{value}" for value in _material(digest.blind_spots, maximum=2)),
    ]
    minority = digest.minority_report
    if minority.dissent and not minority.dissent.startswith("未识别有效少数异议"):
        deliberation.append(f"少数意见：{_human_line(minority.dissent)}")
        if minority.decisive_condition:
            deliberation.append(f"决定条件：{_human_line(minority.decisive_condition)}")

    interaction = [
        *_material(digest.context_gaps_answers, maximum=2),
        *_material(digest.user_decisions, maximum=2),
        *_material(digest.reconsideration_changes, maximum=2),
    ]

    conclusion = _material(digest.editor_synthesis, maximum=2)
    checklist = _material(digest.execution_checklist_final_disposition, maximum=6)
    final = next((item for item in reversed(checklist) if item.startswith("最终处置：")), "")
    conclusion.extend(item for item in checklist if item != final)
    if degraded or warnings or fallback_reason:
        conclusion.append("本次执行存在降级或回退；相关风险需在发布前人工确认。")
    if status == "RETURNED_PENDING":
        conclusion.append("审校尚待补充信息或决定，当前结论不是发布许可。")
    if not final:
        final = "最终处置：需人工复核；需人工复核：是"

    sections = [
        _section("审校背景", background),
        _section("专业视角", _role_lines(digest)),
        _section("共识、分歧与盲区", [_human_line(value) for value in deliberation]),
    ]
    if interaction:
        sections.append(_section("你的决定与复议", interaction))
    sections.append(_section("主编结论", [*conclusion[:5], _human_line(final)]))
    report = "\n\n".join("\n".join(section) for section in sections if section)
    if len(report) <= 3_200:
        return report

    final_line = f"- {_human_line(final)}"
    available = 3_200 - len(final_line) - 1
    return report[:available].rstrip() + "\n" + final_line
