"""Deterministic process-first digest and bounded display report."""

from __future__ import annotations

import re
from typing import Any

from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    ContextGapV2,
    CouncilPlan,
    CouncilValueMetrics,
    IssueCluster,
    MinorityReport,
    PhaseReconsiderationProvenance,
    ProcessDigestV2,
    ReviewBriefV2,
    RoleLens,
    UserDecision,
)
from council_of_translation.localization.roles import ROLE_REGISTRY
from council_of_translation.localization.value_metrics import (
    _bounded_structured_evidence_keys,
    _logical_issue_groups,
    _normalize_anchor,
)


_ROLE_FOCUS = {
    "technical_safety_reviewer": "占位符、变量、标签与格式完整性",
    "fidelity_reviewer": "语义、逻辑关系与信息完整性",
    "terminology_reviewer": "术语表、历史译法与一致性",
    "product_context_reviewer": "组件、流程阶段与产品语境",
    "ux_copy_reviewer": "用户理解、行动指引与界面清晰度",
    "fluency_reviewer": "目标语言习惯、自然度与简洁性",
    "risk_ambiguity_reviewer": "法律含义、承诺边界与风险表达",
    "brand_voice_reviewer": "品牌语气、风格一致性与受众感受",
}
_INTERNAL_ENTITY_ID = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:issue|cluster|position|decision|option|gap)_"
    r"(?P<suffix>[A-Za-z0-9_-]+)"
    r"(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)
_INTERNAL_IMPLEMENTATION_LABEL = re.compile(
    r"(?<![A-Za-z0-9_])(?:actor_action_object|schema_version|diagnostic_build|"
    r"suggested_translation|routing_profile|routing_reason_codes)(?![A-Za-z0-9_])",
    re.IGNORECASE,
)
_INTERNAL_ROUTING_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    r"route_(?:unspecified|ui|marketing|technical_documentation|legal_risk)_"
    r"(?:lightweight|standard|strict)_v1|"
    r"content_(?:unspecified|ui|marketing|technical_documentation|legal_risk)|"
    r"mode_(?:lightweight|standard|strict)|"
    r"legacy_(?:unrecorded|routing_unrecorded|portfolio_preserved)|"
    r"risk_(?:focused|panorama|strict)|deterministic_preflight_coverage"
    r")(?![A-Za-z0-9_])",
    re.IGNORECASE,
)
_ROLE_ID_LABELS = {role_id.casefold(): role.display_name for role_id, role in ROLE_REGISTRY.items()}
_ROLE_ID = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    + "|".join(re.escape(role_id) for role_id in sorted(ROLE_REGISTRY, key=len, reverse=True))
    + r")(?![A-Za-z0-9_])",
    re.IGNORECASE,
)
_PRIMARY_VOCABULARY = (
    (re.compile(r"(?<![A-Za-z0-9_])effective\s+brief(?![A-Za-z0-9_])", re.IGNORECASE), "有效背景"),
    (re.compile(r"(?<![A-Za-z0-9_])preflight(?![A-Za-z0-9_])", re.IGNORECASE), "技术预检"),
    (re.compile(r"(?<![A-Za-z0-9_])placeholder_parity(?![A-Za-z0-9_])", re.IGNORECASE), "占位符一致性"),
    (re.compile(r"(?<![A-Za-z0-9_])tag_integrity(?![A-Za-z0-9_])", re.IGNORECASE), "标签完整性"),
    (re.compile(r"(?<![A-Za-z0-9_])context(?![A-Za-z0-9_])", re.IGNORECASE), "上下文"),
    (re.compile(r"(?<![A-Za-z0-9_])policy\s+gate(?![A-Za-z0-9_])", re.IGNORECASE), "约束审查"),
    (re.compile(r"(?<![A-Za-z0-9_])position\s+matrix(?![A-Za-z0-9_])", re.IGNORECASE), "证据矩阵"),
    (re.compile(r"(?<![A-Za-z0-9_])council\s+fallback(?![A-Za-z0-9_])", re.IGNORECASE), "委员会回退裁决"),
    (re.compile(r"(?<![A-Za-z0-9_])ux(?![A-Za-z0-9_])", re.IGNORECASE), "用户体验"),
)


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
        ranked = sorted(
            (item for item in findings if isinstance(item, dict)),
            key=lambda item: (
                0 if item.get("blocking") or item.get("severity") in {"critical", "major"} else 1,
                0 if item.get("finding_kind") == "choice" else 1,
                0 if item.get("finding_kind") == "affirmation" else 1,
            ),
        )
        strongest = ranked[0] if ranked else {}
        evidence = _dedupe([str(strongest.get("evidence") or "")], maximum=1)
        feedback = str(review.get("role_feedback", "")).strip()
        status = str(review.get("sample_status", "unavailable"))
        role = ROLE_REGISTRY.get(role_id)
        if status != "structured_success":
            perspective = "结构化评审不可用；该专业范围保留为盲区。"
        elif strongest.get("blocking") or strongest.get("severity") in {"critical", "major"}:
            perspective = f"发现高优先级{strongest.get('issue_type', '质量')}问题：{strongest.get('problem', '')}"
        elif strongest.get("finding_kind") == "choice":
            proposal = str(strongest.get("proposed_value") or "").strip()
            perspective = f"提出具体措辞选择{f'“{proposal}”' if proposal else ''}：{strongest.get('problem', '')}"
        elif strongest.get("finding_kind") == "affirmation":
            check = _ROLE_FOCUS.get(role_id, "该角色职责范围")
            perspective = f"围绕{check}确认当前译文可接受：{strongest.get('problem') or strongest.get('evidence') or '未发现实质问题'}"
        elif strongest:
            perspective = f"发现{strongest.get('issue_type', '质量')}问题：{strongest.get('problem') or feedback}"
        elif role:
            perspective = f"未发现职责范围内的实质问题；已检查{_ROLE_FOCUS.get(role_id, '该角色职责范围')}。"
        else:
            perspective = feedback or "未发现职责范围内的实质问题。"
        lenses.append(RoleLens(
            role_id=role_id,
            perspective=perspective,
            evidence=evidence,
            disposition=(
                "完成职责内审校" if status == "structured_success" else "采样不可用，保留为盲区"
            ),
        ))
    return lenses


def _consensus_lines(
    plan: CouncilPlan,
    reviews: list[dict[str, Any]],
    clusters: list[IssueCluster],
    reviewer_coverage: str,
) -> list[str]:
    clustered = _dedupe([
        cluster.topic for cluster in clusters if cluster.consensus_status == "consensus"
    ])
    if reviewer_coverage != "full":
        return clustered or ["评审覆盖不足，不能据此形成正向共识。"]

    by_role = {
        str(review.get("agent_name", "")): review
        for review in reviews
        if isinstance(review, dict) and review.get("sample_status") == "structured_success"
    }
    if any(role_id not in by_role for role_id in plan.active_role_ids):
        return clustered or ["评审覆盖不足，不能据此形成正向共识。"]

    outcomes: list[str] = []
    every_role_affirmed = True
    has_material_issue = False
    for role_id in plan.active_role_ids:
        findings = by_role[role_id].get("findings", [])
        findings = findings if isinstance(findings, list) else []
        affirmations = [
            item for item in findings
            if isinstance(item, dict) and item.get("finding_kind") == "affirmation"
        ]
        every_role_affirmed = every_role_affirmed and bool(affirmations)
        has_material_issue = has_material_issue or any(
            isinstance(item, dict)
            and item.get("finding_kind") != "affirmation"
            and item.get("severity") in {"critical", "major"}
            for item in findings
        )
        if affirmations:
            outcome = str(
                affirmations[0].get("proposed_value")
                or affirmations[0].get("candidate_span")
                or ""
            ).strip()
            outcomes.append(outcome)

    if every_role_affirmed and not has_material_issue:
        normalized = {_semantic_key(value) for value in outcomes if _semantic_key(value)}
        if len(normalized) == 1 and len(outcomes) == len(plan.active_role_ids):
            outcome = _human_line(outcomes[0], 80)
            return [
                f"所有专业视角均未发现阻碍发布的问题；共同支持保留“{outcome}”。"
            ]
        return ["所有专业视角均未发现阻碍发布的问题；未据此推断共同措辞建议。"]

    return clustered or ["各角色未发现发布阻断项，但缺少共同的结构化语义主张。"]


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
    consensus = _consensus_lines(plan, independent_reviews, clusters, reviewer_coverage)
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
            _routing_display_line(plan),
            f"受众：{brief.audience or '未提供'}",
            f"审校重点：{brief.primary_focus or '按角色职责执行'}",
        ]),
        assumptions_context_confidence=_dedupe([
            f"上下文置信度：{brief.context_confidence}",
            *brief.assumptions,
        ]),
        blind_spots=_dedupe(blind_spots),
        role_lenses=_role_lenses(plan, independent_reviews),
        consensus=consensus,
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
            chief.decision_rationale or "主编依据有效约束与角色证据完成综合。",
            chief.review_reason,
        ]),
        execution_checklist_final_disposition=_dedupe(checklist),
    )


_NO_OP_PREFIXES = (
    "未提出需跟进", "未请求用户", "未触发重审", "未识别有效少数异议",
)


def _sanitize_primary_text(value: str) -> str:
    """Remove implementation identifiers without erasing ordinary translation tokens."""
    text = value
    for pattern, replacement in _PRIMARY_VOCABULARY:
        text = pattern.sub(replacement, text)
    text = _ROLE_ID.sub(lambda match: _ROLE_ID_LABELS[match.group(0).casefold()], text)
    text = _INTERNAL_ENTITY_ID.sub("内部引用", text)
    text = _INTERNAL_ROUTING_TOKEN.sub("内部路由信息", text)
    return _INTERNAL_IMPLEMENTATION_LABEL.sub("内部信息", text)


def _routing_display_line(plan: CouncilPlan) -> str:
    """Describe only fixed legal-risk routes without interpolating provenance values."""
    return {
        "route_legal_risk_lightweight_v1": (
            "风险审校路线：聚焦语义、术语、风险歧义与语言自然度；确定性技术预检照常执行。"
        ),
        "route_legal_risk_standard_v1": (
            "风险审校路线：覆盖语义、术语、产品语境、用户理解、风险歧义与语言自然度；"
            "确定性技术预检照常执行。"
        ),
        "route_legal_risk_strict_v1": (
            "风险审校路线：在全景覆盖上增加技术完整性复核；确定性技术预检照常执行。"
        ),
    }.get(plan.routing_profile, "")


def _human_line(value: str, maximum: int = 120) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    text = _sanitize_primary_text(text)
    text = re.sub(r"。+\s*；", "；", text)
    text = re.sub(r"；{2,}", "；", text)
    return text if len(text) <= maximum else text[: maximum - 1].rstrip() + "…"


def _material(values: list[str], *, maximum: int = 3) -> list[str]:
    return [
        _human_line(value)
        for value in values
        if value and not value.startswith(_NO_OP_PREFIXES)
    ][:maximum]


def _section(title: str, values: list[str]) -> list[str]:
    return [f"## {title}", *(f"- {value}" for value in values)] if values else []


def _is_canonical_procedural_synthesis(value: str) -> bool:
    """Identify only the chief's generated adjudication-counter boilerplate."""
    text = re.sub(r"\s+", " ", str(value)).strip()
    return bool(
        re.search(r"(?:policy\s+gate|约束审查)", text, re.IGNORECASE)
        and re.search(r"用户有效选择\s*\d+\s*项", text)
        and re.search(r"(?:council\s+fallback|委员会回退裁决)\s*\d+\s*项", text, re.IGNORECASE)
        and re.search(r"人工复核\s*\d+\s*项", text)
        and re.search(r"未使用(?:票数)?多数", text)
    )


def _whole_optional_evidence(values: list[str], maximum: int = 80) -> str:
    """Return one complete evidence item or omit it; never create a fragment."""
    for value in values:
        text = re.sub(r"\s+", " ", str(value)).strip()
        text = _sanitize_primary_text(text)
        if text and len(text) <= maximum:
            return text
    return ""


def _compatibility_evidence_is_redundant(lens: RoleLens) -> bool:
    """Suppress repetitive clean evidence without assigning a contribution kind."""
    perspective = re.sub(r"\s+", " ", lens.perspective).strip()
    return (
        (perspective.startswith("围绕") and "确认当前译文可接受" in perspective)
        or perspective.startswith("未发现职责范围内的实质问题")
    )


def _fallback_value_metrics(digest: ProcessDigestV2) -> CouncilValueMetrics:
    """Account for legacy lenses without inferring structured facts from prose."""
    from council_of_translation.localization.models import RoleContribution

    contributions = []
    for lens in digest.role_lenses:
        contributions.append(RoleContribution(
            role_id=lens.role_id,
            contribution_kind="confirmation_only",
        ))
    return CouncilValueMetrics(
        role_contributions=contributions,
        confirmation_only_role_count=len(contributions),
    )


def _coverage_lines(
    digest: ProcessDigestV2,
    metrics: CouncilValueMetrics,
    *,
    compatibility_fallback: bool = False,
    clusters: list[IssueCluster] | None = None,
) -> list[str]:
    by_role = {lens.role_id: lens for lens in digest.role_lenses}
    order = {"unique_material": 0, "corroborating": 1, "confirmation_only": 2, "unavailable": 3}
    contributions = sorted(metrics.role_contributions, key=lambda item: (
        order[item.contribution_kind],
        list(by_role).index(item.role_id) if item.role_id in by_role else 99,
    ))
    if clusters is None:
        lines: list[str] = []
        for contribution in contributions:
            lens = by_role.get(contribution.role_id)
            if lens is None:
                continue
            role = ROLE_REGISTRY.get(lens.role_id)
            label = role.display_name if role else "未识别专业角色"
            evidence = (
                _whole_optional_evidence(lens.evidence)
                if (
                    compatibility_fallback
                    and not _compatibility_evidence_is_redundant(lens)
                ) or contribution.contribution_kind in {"unique_material", "corroborating"}
                else ""
            )
            suffix = f"；依据：{evidence}" if evidence else ""
            if contribution.contribution_kind == "unique_material":
                summary = f"新增 {contribution.unique_issue_count} 个独立问题；{lens.perspective}"
            elif contribution.contribution_kind == "corroborating":
                summary = f"交叉印证 {contribution.corroborated_issue_count} 个问题；{lens.perspective}"
            elif contribution.contribution_kind == "confirmation_only":
                summary = (
                    f"兼容记录未提供结构化贡献分类；{lens.perspective}"
                    if compatibility_fallback
                    else "完成确认性覆盖，未提交实质问题。"
                )
            else:
                summary = "结构化评审不可用；该专业范围保留为盲区。"
            perspective_limit = max(40, 150 - len(label) - 1 - len(suffix))
            perspective = _human_line(summary, perspective_limit)
            if suffix:
                perspective = perspective.rstrip("。；; ")
            lines.append(_human_line(f"{label}：{perspective}{suffix}", 150))
        return lines

    lines: list[str] = []
    accounted: set[str] = set()

    for contribution in contributions:
        if contribution.contribution_kind != "unique_material":
            continue
        lens = by_role.get(contribution.role_id)
        if lens is None:
            continue
        role = ROLE_REGISTRY.get(lens.role_id)
        label = role.display_name if role else "未识别专业角色"
        evidence = _whole_optional_evidence(lens.evidence) if clusters is None else ""
        suffix = f"；依据：{evidence}" if evidence else ""
        summary = f"新增 {contribution.unique_issue_count} 个独立问题"
        if clusters is None:
            summary += f"；{lens.perspective}"
        perspective_limit = max(40, 150 - len(label) - 1 - len(suffix))
        perspective = _human_line(summary, perspective_limit)
        if suffix:
            perspective = perspective.rstrip("。；; ")
        lines.append(_human_line(f"{label}：{perspective}{suffix}", 150))
        accounted.add(contribution.role_id)

    corroborating_ids = {
        item.role_id
        for item in contributions
        if item.contribution_kind == "corroborating" and item.role_id in by_role
    }
    if clusters:
        for group in _logical_issue_groups(clusters):
            group_roles = [
                role_id
                for role_id in by_role
                if role_id in corroborating_ids
                and role_id not in accounted
                and any(role_id in cluster.participant_role_ids for cluster in group)
            ]
            if not group_roles:
                continue
            labels = "、".join(
                ROLE_REGISTRY[role_id].display_name
                if role_id in ROLE_REGISTRY else "未识别专业角色"
                for role_id in group_roles
            )
            deterministic = [cluster for cluster in group if not cluster.finding_ids]
            anchors = (
                _deterministic_literals(deterministic)
                if deterministic
                else _dedupe([
                    *[span for cluster in group for span in cluster.source_spans],
                    *[span for cluster in group for span in cluster.candidate_spans],
                ], maximum=2)
            )
            anchor = " → ".join(_human_line(item, 36) for item in anchors if item)
            topics = _dedupe([
                cluster.topic for cluster in group if cluster.finding_ids
            ], maximum=1)
            topic = _human_line(topics[0]) if topics else (
                "确定性检查发现受保护内容或结构缺失。"
                if deterministic else "同一结构化问题。"
            )
            location = f"“{anchor}”相关问题" if anchor else "同一结构化问题"
            lines.append(
                _human_line(f"{labels}：共同交叉印证{location}：{topic}", 240)
            )
            accounted.update(group_roles)

    remaining_corroborating = [
        role_id for role_id in by_role
        if role_id in corroborating_ids and role_id not in accounted
    ]
    if remaining_corroborating:
        labels = "、".join(
            ROLE_REGISTRY[role_id].display_name
            if role_id in ROLE_REGISTRY else "未识别专业角色"
            for role_id in remaining_corroborating
        )
        lines.append(_human_line(f"{labels}：共同完成结构化交叉印证。", 180))
        accounted.update(remaining_corroborating)

    confirmation_ids = [
        item.role_id
        for item in contributions
        if item.contribution_kind == "confirmation_only"
        and item.role_id in by_role
        and item.role_id not in accounted
    ]
    if confirmation_ids:
        labels = "、".join(
            ROLE_REGISTRY[role_id].display_name
            if role_id in ROLE_REGISTRY else "未识别专业角色"
            for role_id in confirmation_ids
        )
        summary = (
            "兼容记录未提供结构化贡献分类。"
            if compatibility_fallback
            else "完成确认性覆盖，未提交实质问题。"
        )
        lines.append(_human_line(f"{labels}：{summary}", 240))
        accounted.update(confirmation_ids)

    for contribution in contributions:
        if contribution.contribution_kind != "unavailable" or contribution.role_id in accounted:
            continue
        lens = by_role.get(contribution.role_id)
        if lens is None:
            continue
        role = ROLE_REGISTRY.get(lens.role_id)
        label = role.display_name if role else "未识别专业角色"
        lines.append(f"{label}：结构化评审不可用；该专业范围保留为盲区。")
        accounted.add(contribution.role_id)
    return lines


def _represented_cluster_topics(
    clusters: list[IssueCluster] | None,
    rendered_lines: list[str],
) -> set[str]:
    """Return only bounded cluster topics literally emitted in earlier lines."""
    return {
        _semantic_key(cluster.topic)
        for cluster in (clusters or [])
        if _semantic_key(cluster.topic)
        and any(_human_line(cluster.topic) in line for line in rendered_lines)
    }


def _bounded_cluster_topics(group: list[IssueCluster]) -> list[str]:
    return _dedupe([cluster.topic for cluster in group if cluster.topic], maximum=3)


def _deterministic_literals(group: list[IssueCluster]) -> list[str]:
    """Recover bounded protected literals from deterministic check evidence only."""
    literals: list[str] = []
    for cluster in group:
        if cluster.finding_ids:
            continue
        refs = " ".join(cluster.immutable_hard_constraints)
        for value in cluster.source_spans:
            bounded = str(value).strip()[:240]
            prefix, separator, literal = bounded.partition(":")
            if separator and literal and prefix in {"required_literal", "forbidden_literal"}:
                literals.append(literal)
                continue
            tokens = sorted(
                key.removeprefix("token:")
                for key in _bounded_structured_evidence_keys(bounded)
                if key.startswith("token:")
            )
            if tokens:
                literals.extend(tokens)
            elif (
                "explicit-dnt-preservation" in refs
                or "explicit-required-literal" in refs
                or "explicit-forbidden-literal" in refs
            ) and bounded:
                literals.append(bounded)
    return _dedupe(literals, maximum=3)


def _deterministic_work_item(group: list[IssueCluster]) -> str:
    """Translate deterministic telemetry into one natural primary repair."""
    refs = {
        ref
        for cluster in group
        if not cluster.finding_ids
        for ref in cluster.immutable_hard_constraints
    }
    if not refs:
        return ""
    literals = _deterministic_literals(group)
    quoted = "、".join(f"{value}" for value in literals)
    if any("forbidden-literal" in ref for ref in refs):
        return f"必须修复：移除禁用内容 {quoted}。" if quoted else "必须修复：移除调用方明确禁用的内容。"
    if any("placeholder-parity" in ref or ref in {"variable-parity", "command-parity"} for ref in refs):
        return f"必须修复：恢复并原样保留占位符 {quoted}。" if quoted else "必须修复：恢复缺失的占位符或变量。"
    if "url-parity" in refs:
        return f"必须修复：恢复并原样保留链接 {quoted}。" if quoted else "必须修复：恢复缺失的链接。"
    if "tag-integrity" in refs:
        return f"必须修复：恢复并校正标签结构 {quoted}。" if quoted else "必须修复：恢复并校正标签结构。"
    if any("explicit-dnt-preservation" in ref or "explicit-required-literal" in ref for ref in refs):
        return f"必须修复：恢复并原样保留受保护内容 {quoted}。" if quoted else "必须修复：恢复调用方要求保留的内容。"
    if "numeric-parity" in refs:
        return "必须修复：恢复原文中的数字信息。"
    if "markdown-structure" in refs:
        return "必须修复：恢复原文的 Markdown 结构。"
    return "必须修复：恢复确定性检查指出的受保护内容或结构。"


def _normalized_span_set(values: list[str]) -> tuple[str, ...]:
    return tuple(sorted({anchor for value in values if (anchor := _normalize_anchor(value))}))


def _replacement_actions(cluster: IssueCluster) -> tuple[str, ...]:
    current = _normalize_anchor(cluster.current_outcome)
    return tuple(sorted({
        action
        for value in cluster.candidate_actions
        if (action := _normalize_anchor(value)) and action != current
    }))


def _bounded_anchor_sets_related(
    left: tuple[str, ...],
    right: tuple[str, ...],
) -> bool:
    """Admit only exact singleton anchors or direct bounded containment."""
    if not left or not right:
        return False
    if left == right:
        return True
    if len(left) != 1 or len(right) != 1:
        return False
    left_anchor, right_anchor = left[0], right[0]
    return left_anchor in right_anchor or right_anchor in left_anchor


def _model_work_item(group: list[IssueCluster]) -> str:
    """Render one exact-anchor replacement while retaining distinct consequences."""
    first = group[0]
    current = next((value.strip() for value in first.candidate_spans if value.strip()), "")
    current_key = _normalize_anchor(current)
    proposals = [
        value.strip()
        for value in first.candidate_actions
        if value.strip() and _normalize_anchor(value) != current_key
    ]
    proposal = proposals[0] if proposals else ""
    if current and proposal:
        repair = f"建议修复：将“{_human_line(current, 72)}”调整为“{_human_line(proposal, 96)}”"
    elif proposal:
        repair = f"建议修复：采用“{_human_line(proposal, 120)}”"
    else:
        repair = f"建议修复：{_human_line(first.topic, 160).rstrip('。')}"
    consequences = _bounded_cluster_topics(group[1:])
    if consequences:
        repair += "；相关影响：" + "；".join(_human_line(value, 100).rstrip("。") for value in consequences)
    return _human_line(repair + "。", 240)


def _primary_work_item_groups(clusters: list[IssueCluster]) -> list[dict[str, Any]]:
    """Build bounded, non-mutating human work-item identities for primary text."""
    groups: list[dict[str, Any]] = []
    assigned_model_ids: set[str] = set()
    for index, logical_group in enumerate(_logical_issue_groups(clusters)):
        deterministic = [cluster for cluster in logical_group if not cluster.finding_ids]
        if not deterministic:
            continue
        literals = _deterministic_literals(deterministic)
        literal_keys = {_normalize_anchor(value) for value in literals if _normalize_anchor(value)}
        corroborating: list[IssueCluster] = []
        for cluster in logical_group:
            if not cluster.finding_ids:
                continue
            spans = [*cluster.source_spans, *cluster.candidate_spans]
            exact = {_normalize_anchor(value) for value in spans if _normalize_anchor(value)}
            structured = {
                key.removeprefix("token:")
                for value in cluster.evidence
                for key in _bounded_structured_evidence_keys(value)
                if key.startswith("token:")
            }
            # Exact spans are direct corroboration.  Containment is admitted only
            # when independent structured evidence carries the same repair anchor;
            # a whole sentence that merely contains a token cannot absorb a
            # separate semantic reversal.
            if literal_keys & exact or literal_keys & structured:
                corroborating.append(cluster)
                assigned_model_ids.add(cluster.issue_id)
        members = [*deterministic, *corroborating]
        groups.append({
            "key": f"deterministic:{index}",
            "members": members,
            "anchors": literal_keys,
            "topics": _bounded_cluster_topics(members),
            "line": _deterministic_work_item(deterministic),
        })

    model_clusters = [
        cluster for cluster in clusters
        if cluster.finding_ids and cluster.issue_id not in assigned_model_ids
    ]
    model_buckets: dict[tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]], list[IssueCluster]] = {}
    for cluster in model_clusters:
        actions = _replacement_actions(cluster)
        if not actions:
            continue
        identity = (
            _normalized_span_set(cluster.source_spans),
            _normalized_span_set(cluster.candidate_spans),
            actions,
        )
        if not identity[0] or not identity[1]:
            continue
        model_buckets.setdefault(identity, []).append(cluster)
    for index, members in enumerate(model_buckets.values()):
        if len({cluster.category for cluster in members}) < 2:
            continue
        groups.append({
            "key": f"model:{index}",
            "members": members,
            "anchors": set(),
            "topics": _bounded_cluster_topics(members),
            "line": _model_work_item(members),
        })

    # Live ordinary-issue findings often have no proposal at all.  Preserve the
    # exact-action identity above, then conservatively group only actionless,
    # cross-family clusters whose source and candidate anchors independently
    # match or directly contain one another.  Requiring pairwise compatibility
    # prevents transitive bridging through a broad sentence span.
    actionless_groups: list[list[IssueCluster]] = []
    for cluster in model_clusters:
        if _replacement_actions(cluster):
            continue
        source_anchors = _normalized_span_set(cluster.source_spans)
        candidate_anchors = _normalized_span_set(cluster.candidate_spans)
        if not source_anchors or not candidate_anchors:
            continue
        for members in actionless_groups:
            if all(
                cluster.category != member.category
                and _bounded_anchor_sets_related(
                    source_anchors,
                    _normalized_span_set(member.source_spans),
                )
                and _bounded_anchor_sets_related(
                    candidate_anchors,
                    _normalized_span_set(member.candidate_spans),
                )
                for member in members
            ):
                members.append(cluster)
                break
        else:
            actionless_groups.append([cluster])
    model_offset = len(model_buckets)
    for index, members in enumerate(actionless_groups, start=model_offset):
        if len(members) < 2:
            continue
        groups.append({
            "key": f"model:{index}",
            "members": members,
            "anchors": set(),
            "topics": _bounded_cluster_topics(members),
            "line": _model_work_item(members),
        })
    return groups


def _entry_work_items(
    text: str,
    groups: list[dict[str, Any]],
    seen_groups: set[str],
) -> list[dict[str, Any]]:
    normalized = _normalize_anchor(text)
    topic_matches = [
        group
        for group in groups
        if any(
            (topic_key := _normalize_anchor(topic)) and topic_key in normalized
            for topic in group["topics"]
        )
    ]
    if topic_matches:
        unseen = [group for group in topic_matches if group["key"] not in seen_groups]
        return unseen or [topic_matches[0]]
    anchor_matches = [
        group for group in groups
        if group["anchors"] and any(anchor in normalized for anchor in group["anchors"])
    ]
    if anchor_matches:
        unseen = [group for group in anchor_matches if group["key"] not in seen_groups]
        return unseen or [anchor_matches[0]]
    return []


def _primary_checklist(
    values: list[str],
    clusters: list[IssueCluster] | None,
) -> list[str]:
    """Project structured clusters into bounded primary-only human work items."""
    groups = _primary_work_item_groups(clusters or [])
    result: list[str] = []
    seen_groups: set[str] = set()
    seen_text: set[str] = set()
    for value in values:
        text = str(value).strip()[:240]
        if not text:
            continue
        matched = _entry_work_items(text, groups, seen_groups)
        if matched and all(group["key"] in seen_groups for group in matched):
            continue
        candidates = matched or [None]
        for group in candidates:
            group_key = group["key"] if group else ""
            if group_key and group_key in seen_groups:
                continue
            rendered = str(group["line"] or text) if group else text
            key = _semantic_key(rendered)
            if not key or key in seen_text:
                continue
            result.append(_human_line(rendered, 240))
            if group_key:
                seen_groups.add(group_key)
            seen_text.add(key)
            if len(result) >= 6:
                break
        if len(result) >= 6:
            break
    return result


def _value_lines(
    digest: ProcessDigestV2,
    metrics: CouncilValueMetrics,
    *,
    compatibility_fallback: bool = False,
) -> list[str]:
    by_role = {lens.role_id: lens for lens in digest.role_lenses}
    values = _dedupe([
        by_role[item.role_id].perspective
        for item in metrics.role_contributions
        if item.contribution_kind == "unique_material" and item.role_id in by_role
    ], maximum=3)
    lines = [f"新增问题：{_human_line(value)}" for value in values]
    if metrics.corroborated_issue_count:
        lines.append(f"交叉印证：{metrics.corroborated_issue_count} 个问题得到多个专业视角支持。")
    if not lines and metrics.unique_material_issue_count:
        lines.append(
            f"结构化检查识别 {metrics.unique_material_issue_count} 个独立问题；"
            "相关角色不可用时仍保留该问题与证据。"
        )
    if compatibility_fallback:
        lines = ["兼容记录未包含结构化贡献指标；不据角色自然语言推断新增价值。"]
    elif not lines:
        lines.append("未发现新增实质问题；结构化评审覆盖完整。")
    if metrics.discussion_marginal_value != "not_applicable":
        discussion = {
            "none": "讨论未增加新的结构化证据，也未改变立场。",
            "low": f"讨论补充 {metrics.discussion_new_evidence_count} 条新证据，未改变立场。",
            "material": (
                f"讨论新增证据 {metrics.discussion_new_evidence_count} 条、"
                f"改变立场 {metrics.discussion_position_change_count} 次、"
                f"解决问题 {metrics.discussion_resolved_issue_count} 个。"
            ),
        }[metrics.discussion_marginal_value]
        lines.append(discussion)
    return lines[:5]


def _join_sections(sections: list[list[str]]) -> str:
    return "\n\n".join("\n".join(section) for section in sections if section)


def _bound_five_sections(sections: list[list[str]], maximum: int = 3_200) -> str:
    """Keep every section and whole high-value lines under the primary hard cap."""
    report = _join_sections(sections)
    if len(report) <= maximum:
        return report

    selected: set[tuple[int, int]] = set()
    for section_index, section in enumerate(sections):
        selected.add((section_index, 0))
        if len(section) > 1:
            selected.add((section_index, 1))
    final_index = len(sections[-1]) - 1
    selected.add((len(sections) - 1, final_index))
    for line_index, line in enumerate(sections[-1][1:final_index], start=1):
        if "降级" in line or "回退" in line or "尚待补充" in line:
            selected.add((len(sections) - 1, line_index))

    safety_markers = (
        "必须修复", "分歧", "盲区", "少数意见", "决定条件",
        "覆盖风险", "不可用", "降级", "回退", "人工复核",
    )
    material_markers = (
        "建议修复", "新增", "交叉印证",
    )
    candidates: list[tuple[int, int, int]] = []
    for section_index, section in enumerate(sections):
        for line_index, line in enumerate(section[1:], start=1):
            if (section_index, line_index) in selected:
                continue
            priority = (
                0 if any(marker in line for marker in safety_markers)
                else 1 if section_index == 2
                else 2 if any(marker in line for marker in material_markers)
                else 3
            )
            candidates.append((priority, section_index, line_index))

    def render_current() -> str:
        chosen = [
            [line for line_index, line in enumerate(section) if (section_index, line_index) in selected]
            for section_index, section in enumerate(sections)
        ]
        return _join_sections(chosen)

    for _, section_index, line_index in sorted(candidates):
        selected.add((section_index, line_index))
        if len(render_current()) > maximum:
            selected.remove((section_index, line_index))
    return render_current()


def render_display_report(
    digest: ProcessDigestV2,
    *,
    metrics: CouncilValueMetrics | None = None,
    status: str = "",
    degraded: bool = False,
    warnings: list[str] | None = None,
    fallback_reason: str = "",
    clusters: list[IssueCluster] | None = None,
) -> str:
    """Render the frozen value-first five-section primary Council report."""
    compatibility_fallback = metrics is None
    value_metrics = metrics or _fallback_value_metrics(digest)
    background = _material(digest.case_brief, maximum=4)
    background.extend(_material(digest.assumptions_context_confidence, maximum=2))

    value_lines = _value_lines(
        digest,
        value_metrics,
        compatibility_fallback=compatibility_fallback,
    )
    coverage_lines = _coverage_lines(
        digest,
        value_metrics,
        compatibility_fallback=compatibility_fallback,
        clusters=clusters,
    )
    represented_topics = _represented_cluster_topics(
        clusters,
        [*value_lines, *coverage_lines],
    )
    deterministic_topics = {
        _semantic_key(cluster.topic)
        for group in _primary_work_item_groups(clusters or [])
        if str(group["key"]).startswith("deterministic:")
        for cluster in group["members"]
        if not cluster.finding_ids and _semantic_key(cluster.topic)
    }
    deliberation = [
        *(f"共识：{value}" for value in _material(digest.consensus, maximum=2)
          if _semantic_key(value) not in represented_topics
          and _semantic_key(value) not in deterministic_topics),
        *(f"分歧：{value}" for value in _material(digest.material_disagreements, maximum=2)
          if _semantic_key(value) not in represented_topics
          and _semantic_key(value) not in deterministic_topics),
        *(f"盲区：{value}" for value in _material(digest.blind_spots, maximum=2)),
    ]
    minority = digest.minority_report
    if minority.dissent and not minority.dissent.startswith("未识别有效少数异议"):
        if _semantic_key(minority.dissent) not in represented_topics:
            deliberation.append(f"少数意见：{_human_line(minority.dissent)}")
        elif minority.decisive_condition:
            deliberation.append("少数意见：已保留该问题的少数立场及其决定条件。")
        if minority.decisive_condition:
            deliberation.append(f"决定条件：{_human_line(minority.decisive_condition)}")

    interaction = [
        *_material(digest.context_gaps_answers, maximum=2),
        *_material(digest.user_decisions, maximum=2),
        *_material(digest.reconsideration_changes, maximum=2),
    ]

    conclusion = _material([
        value for value in digest.editor_synthesis
        if not _is_canonical_procedural_synthesis(value)
    ], maximum=2)
    checklist = _primary_checklist(digest.execution_checklist_final_disposition, clusters)
    final = next((item for item in reversed(checklist) if item.startswith("最终处置：")), "")
    conclusion.extend(item for item in checklist if item != final)
    status_lines: list[str] = []
    if degraded or warnings or fallback_reason:
        status_lines.append("本次执行存在降级或回退；相关风险需在发布前人工确认。")
    if status == "RETURNED_PENDING":
        status_lines.append("审校尚待补充信息或决定，当前结论不是发布许可。")
    if not final:
        final = "最终处置：需人工复核；需人工复核：是"

    deliberation.extend(f"交互与复议：{value}" for value in interaction)
    if value_metrics.unavailable_role_count:
        deliberation.insert(
            0,
            f"覆盖风险：{value_metrics.unavailable_role_count} 个角色的结构化评审不可用。",
        )
    sections = [
        _section("审校背景", background or ["审校背景未完整提供；结论限于当前输入。"]),
        _section(
            "Council 新增视角",
            value_lines,
        ),
        _section(
            "角色覆盖与分工",
            coverage_lines or ["尚无可展示的角色覆盖。"],
        ),
        _section("共识、分歧与盲区", [_human_line(value) for value in deliberation] or ["无可展示结论。"]),
        _section(
            "主编结论",
            [*conclusion[: max(0, 5 - len(status_lines))], *status_lines, _human_line(final)],
        ),
    ]
    return _bound_five_sections(sections)
