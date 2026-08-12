"""Executable reviewer roles and deterministic Council planning."""

from __future__ import annotations

from types import MappingProxyType
from typing import Literal, Mapping

from council_of_translation.localization.models import CouncilPlan, ReviewMode, RoleDefinition


ContentType = Literal["unspecified", "ui", "marketing", "technical_documentation", "legal_risk"]


class ReviewerRole(RoleDefinition):
    """V2 role definition with the read-only V0.3 prompt attributes."""

    @property
    def agent_name(self) -> str:
        return self.id

    @property
    def role(self) -> str:
        return self.display_name

    @property
    def role_mission(self) -> str:
        return self.mission

    @property
    def review_focus(self) -> str:
        return "、".join(self.scope) + "。"

    @property
    def modes(self) -> tuple[ReviewMode, ...]:
        return tuple(self.applicable_modes)  # type: ignore[return-value]


def _reviewer(
    *,
    id: str,
    display_name: str,
    mission: str,
    scope: tuple[str, ...],
    must_check: tuple[str, ...],
    must_not_decide: tuple[str, ...],
    evidence_policy: tuple[str, ...],
    blocking_conditions: tuple[str, ...],
    applicable_modes: tuple[ReviewMode, ...],
    applicable_content_types: tuple[str, ...],
    priority: int,
) -> ReviewerRole:
    return ReviewerRole(
        id=id,
        display_name=display_name,
        role_type="reviewer",
        mission=mission,
        scope=list(scope),
        must_check=list(must_check),
        must_not_decide=list(must_not_decide),
        evidence_policy=list(evidence_policy),
        blocking_conditions=list(blocking_conditions),
        applicable_modes=list(applicable_modes),
        applicable_content_types=list(applicable_content_types),
        discussion_policy="when_relevant",
        priority=priority,
        output_contract_version="2.0",
        prompt_version="2.0",
    )


REVIEWER_ROLES: tuple[ReviewerRole, ...] = (
    _reviewer(
        id="technical_safety_reviewer",
        display_name="技术与占位符审校员",
        mission="你只负责检查候选译文是否安全保留占位符、变量、命令、标签、格式和不可翻译项，并考虑长度或格式约束。",
        scope=("占位符安全", "结构保留", "格式完整性", "技术约束兼容性"),
        must_check=(
            "placeholder_parity",
            "variable_and_command_token_preservation",
            "markup_integrity",
            "url_preservation",
            "do_not_translate_preservation",
            "explicit_format_constraints",
        ),
        must_not_decide=(
            "semantic_or_stylistic_preference_without_technical_impact",
            "create_technical_constraints_not_supplied_by_caller_or_preflight",
        ),
        evidence_policy=(
            "Prefer deterministic preflight and explicit caller technical constraints.",
            "Treat model observations as review evidence, never as deterministic blockers.",
        ),
        blocking_conditions=(
            "caller_or_preflight_confirms_missing_placeholder_or_required_token",
            "caller_or_preflight_confirms_broken_or_missing_required_markup",
            "caller_or_preflight_confirms_missing_url_or_do_not_translate_literal",
        ),
        applicable_modes=("lightweight", "standard", "strict"),
        applicable_content_types=("unspecified", "ui", "technical_documentation", "legal_risk"),
        priority=10,
    ),
    _reviewer(
        id="fidelity_reviewer",
        display_name="忠实度审校员",
        mission="你只负责检查候选译文是否准确表达原文含义，是否存在漏译、误译、过度发挥、逻辑关系错误、否定或条件处理错误。",
        scope=("语义准确性", "信息完整性", "逻辑关系", "义务等级", "限制条件"),
        must_check=("proposition_alignment", "omission", "addition", "negation", "modality", "condition", "scope", "actor_action_object"),
        must_not_decide=("override_explicit_project_rules", "prefer_fluency_over_semantic_correctness", "invent_missing_source_context"),
        evidence_policy=("Anchor claims in source/candidate spans.", "Use caller context only when explicitly supplied."),
        blocking_conditions=("evidence_confirms_meaning_reversal", "evidence_confirms_critical_omission", "evidence_confirms_negation_or_modality_failure"),
        applicable_modes=("lightweight", "standard", "strict"),
        applicable_content_types=("*",),
        priority=20,
    ),
    _reviewer(
        id="terminology_reviewer",
        display_name="术语与一致性管理员",
        mission="你只负责检查候选译文与术语表、历史译法和同类文案是否一致，避免同一概念多种译法或专有名词错误翻译。",
        scope=("术语一致性", "命名稳定性", "风格规则一致性"),
        must_check=("explicit_tb_terms", "approved_names", "reference_consistency", "intra_text_consistency"),
        must_not_decide=("claim_hard_tb_violation_without_explicit_tb_evidence", "override_semantic_or_technical_integrity"),
        evidence_policy=("Explicit TB and project rules are hard evidence.", "References and conventions are soft evidence unless caller marks them binding."),
        blocking_conditions=("explicit_hard_tb_or_project_rule_violation" ,),
        applicable_modes=("lightweight", "standard", "strict"),
        applicable_content_types=("*",),
        priority=30,
    ),
    _reviewer(
        id="product_context_reviewer",
        display_name="产品语境审校员",
        mission="你只负责检查候选译文是否适合真实产品场景，包括组件类型、交互阶段、界面长度和上下文语义。",
        scope=("场景适配", "组件匹配", "交互语义", "长度与界面可用性"),
        must_check=("component_semantics", "interaction_stage", "audience_and_context", "explicit_length_constraints"),
        must_not_decide=("invent_product_context", "override_technical_or_semantic_integrity"),
        evidence_policy=("Prefer caller-supplied product context and UI metadata.", "Label assumptions when context is absent."),
        blocking_conditions=("explicit_context_confirms_action_or_state_is_materially_misrepresented",),
        applicable_modes=("standard", "strict"),
        applicable_content_types=("unspecified", "ui", "technical_documentation"),
        priority=40,
    ),
    _reviewer(
        id="ux_copy_reviewer",
        display_name="用户体验文案审校员",
        mission="你只负责检查候选译文是否便于用户理解和行动，是否清楚表达发生了什么、为什么以及用户下一步该做什么。",
        scope=("易懂性", "可操作性", "认知负担", "错误提示可执行性"),
        must_check=("action_clarity", "state_clarity", "recovery_guidance", "cognitive_load"),
        must_not_decide=("override_semantic_fidelity", "override_hard_terminology", "invent_product_behavior"),
        evidence_policy=("Ground advice in supplied UI context, audience, and observable wording." ,),
        blocking_conditions=("explicit_context_confirms_copy_directs_a_materially_wrong_or_unsafe_action",),
        applicable_modes=("standard", "strict"),
        applicable_content_types=("unspecified", "ui"),
        priority=50,
    ),
    _reviewer(
        id="brand_voice_reviewer",
        display_name="品牌语气守门员",
        mission="你只负责检查候选译文是否符合品牌语气和沟通风格，不负责判断技术正确性或术语规范性，除非它们直接影响语气一致性。",
        scope=("品牌语气", "正式程度", "情感温度", "统一表达风格"),
        must_check=("explicit_brand_guidelines", "tone_consistency", "register", "emotional_temperature"),
        must_not_decide=("invent_brand_rule_without_evidence", "override_technical_semantic_or_hard_tb_constraints"),
        evidence_policy=("Treat explicit brand guidelines as authoritative.", "Treat generic taste as a preference, not a rule."),
        blocking_conditions=("explicit_brand_or_project_rule_marks_the_violation_as_release_blocking",),
        applicable_modes=("strict",),
        applicable_content_types=("unspecified", "marketing"),
        priority=60,
    ),
    _reviewer(
        id="risk_ambiguity_reviewer",
        display_name="风险与歧义审校员",
        mission="你只负责检查候选译文是否存在歧义、误导、过度承诺、文化敏感或潜在风险表达。",
        scope=("歧义", "误解风险", "合规敏感性", "文化风险", "措辞稳妥性"),
        must_check=("material_ambiguity", "misleading_claim", "overpromise", "cultural_and_compliance_risk"),
        must_not_decide=("invent_legal_requirements", "expand_source_meaning_to_remove_hypothetical_risk"),
        evidence_policy=("Prefer explicit jurisdiction, risk, and project rules.", "State uncertainty when legal or cultural context is absent."),
        blocking_conditions=("explicit_rule_or_source_evidence_confirms_material_safety_legal_or_authorization_risk",),
        applicable_modes=("strict",),
        applicable_content_types=("unspecified", "marketing", "legal_risk"),
        priority=70,
    ),
    _reviewer(
        id="fluency_reviewer",
        display_name="自然度润色员",
        mission="你只负责检查候选译文是否符合目标语言习惯，是否流畅自然、简洁清楚，避免翻译腔和生硬表达。",
        scope=("自然度", "可读性", "语序", "搭配", "简洁度"),
        must_check=("target_language_idiom", "readability", "word_order", "collocation", "concision"),
        must_not_decide=("override_hard_tb", "override_placeholder_rule", "override_semantic_fidelity", "promote_style_preference_to_blocker"),
        evidence_policy=("Use target-language convention as advisory evidence.", "Defer to explicit project style and higher-tier constraints."),
        blocking_conditions=(),
        applicable_modes=("lightweight", "standard", "strict"),
        applicable_content_types=("*",),
        priority=80,
    ),
)


CHIEF_EDITOR = RoleDefinition(
    id="chief_editor",
    display_name="主审 / 汇总裁决员",
    role_type="adjudicator",
    mission="根据约束、证据、角色立场、用户决定和政策门结果作出可追溯裁决。",
    scope=["政策门后裁决", "冲突解决", "发布性判断", "执行清单"],
    must_check=["policy_gate_result", "immutable_hard_constraints", "position_matrix", "user_decisions", "evidence_provenance"],
    must_not_decide=["act_as_independent_reviewer", "count_raw_votes", "override_invalid_option", "edit_translation_files"],
    evidence_policy=["Apply the frozen evidence hierarchy and cite decision bases.", "Return human review when valid alternatives remain indistinguishable."],
    blocking_conditions=["unresolved_technical_or_semantic_blocker", "conflicting_hard_rules", "insufficient_evidence_for_safe_adjudication"],
    applicable_modes=["lightweight", "standard", "strict"],
    applicable_content_types=["*"],
    discussion_policy="adjudicate",
    priority=1000,
    output_contract_version="2.0",
    prompt_version="2.0",
)


ROLE_DEFINITIONS: tuple[RoleDefinition, ...] = (*REVIEWER_ROLES, CHIEF_EDITOR)
ROLE_REGISTRY: Mapping[str, RoleDefinition] = MappingProxyType({role.id: role for role in ROLE_DEFINITIONS})

SAMPLE_BUDGETS: Mapping[ReviewMode, int] = MappingProxyType({
    "lightweight": 6,
    "standard": 13,
    "strict": 18,
})

_CONTENT_ALIASES: Mapping[str, ContentType] = MappingProxyType({
    "": "unspecified",
    "unspecified": "unspecified",
    "general": "unspecified",
    "ui": "ui",
    "ux": "ui",
    "product_ui": "ui",
    "ui_button": "ui",
    "marketing": "marketing",
    "marketing_copy": "marketing",
    "technical": "technical_documentation",
    "technical_documentation": "technical_documentation",
    "documentation": "technical_documentation",
    "docs": "technical_documentation",
    "legal": "legal_risk",
    "compliance": "legal_risk",
    "legal_risk": "legal_risk",
})


ROLE_PRIORITY_RULES = """裁决优先级：
1. 显式项目规则、TB、SG、known_exceptions
2. 技术约束
3. 语义忠实
4. 风险控制
5. 产品语境
6. 术语一致
7. 用户理解效率
8. 品牌语气
9. 自然度润色
10. reviewer 风格偏好

若项目规则与通用本地化经验冲突，优先遵循项目规则；若传入规则互相冲突，应标记人工复核。"""


def normalize_mode(mode: str | None) -> ReviewMode:
    if mode in {"lightweight", "standard", "strict"}:
        return mode  # type: ignore[return-value]
    return "standard"


def normalize_content_type(content_type: str | None) -> ContentType:
    normalized = (content_type or "").strip().lower().replace("-", "_").replace(" ", "_")
    return _CONTENT_ALIASES.get(normalized, "unspecified")


def get_role_definition(role_id: str) -> RoleDefinition:
    """Return a registered role or raise ``KeyError`` for an unknown identifier."""

    return ROLE_REGISTRY[role_id]


def get_reviewers_for_mode(mode: ReviewMode) -> list[ReviewerRole]:
    """Compatibility selector retaining the V0.3 mode-only behavior."""

    normalized_mode = normalize_mode(mode)
    return sorted(
        [role for role in REVIEWER_ROLES if normalized_mode in role.applicable_modes],
        key=lambda role: role.priority,
    )


def get_reviewers_for_plan(mode: str | None, content_type: str | None = None) -> list[ReviewerRole]:
    """Select reviewers by mode and normalized localization content type."""

    normalized_content = normalize_content_type(content_type)
    reviewers = get_reviewers_for_mode(normalize_mode(mode))
    if normalized_content == "unspecified":
        return reviewers
    return [
        role
        for role in reviewers
        if "*" in role.applicable_content_types or normalized_content in role.applicable_content_types
    ]


def build_council_plan(
    mode: str | None,
    content_type: str | None = None,
    *,
    interactive_mode: Literal["auto", "off", "required"] = "auto",
) -> CouncilPlan:
    """Build a deterministic plan without sampling or mutating the registry."""

    normalized_mode = normalize_mode(mode)
    normalized_content = normalize_content_type(content_type)
    reviewers = get_reviewers_for_plan(normalized_mode, normalized_content)
    return CouncilPlan(
        mode=normalized_mode,
        content_type=normalized_content,
        active_role_ids=[role.id for role in reviewers],
        discussion_enabled=normalized_mode != "lightweight",
        interactive_enabled=interactive_mode != "off",
        sample_budget=SAMPLE_BUDGETS[normalized_mode],
        max_discussion_rounds=0 if normalized_mode == "lightweight" else 1,
        max_decision_points=3,
    )
