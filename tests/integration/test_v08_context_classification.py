from council_of_translation.localization.guided import (
    build_effective_brief,
    parse_context_gaps,
    select_context_gaps,
)
from council_of_translation.localization.models import ReviewTaskV2


ACTIVE = [
    "fidelity_reviewer",
    "terminology_reviewer",
    "product_context_reviewer",
    "brand_voice_reviewer",
    "risk_ambiguity_reviewer",
    "fluency_reviewer",
]


def _parsed(items):
    gaps = []
    invalid = 0
    for item in items:
        parsed, count = parse_context_gaps([item], "fidelity_reviewer")
        gaps.extend(parsed)
        invalid += count
    return gaps, invalid


def _item(question, materiality, roles=None):
    return {
        "question": question,
        "materiality": materiality,
        "affected_role_ids": roles or ["fidelity_reviewer"],
    }


def test_live_brand_ui_and_binding_glossary_variants_are_material():
    task = ReviewTaskV2(
        content_type="marketing",
        context="多步骤软件设置向导底部的主操作按钮",
    )
    brief, _ = build_effective_brief(task)
    gaps, invalid = _parsed([
        _item(
            "该文案是品牌标语还是功能按钮？",
            "两种用途适用不同专业角色与发布标准",
            ["brand_voice_reviewer", "product_context_reviewer"],
        ),
        _item(
            "是否存在官方批准且具有约束力的标语词表或参考译法？",
            "官方规范将约束允许采用的品牌措辞",
            ["terminology_reviewer", "brand_voice_reviewer"],
        ),
    ])

    selected, all_gaps = select_context_gaps(gaps, brief, active_role_ids=ACTIVE)

    assert invalid == 0
    assert [gap.question for gap in selected] == [gap.question for gap in gaps]
    assert all(gap.disposition == "unanswered" for gap in all_gaps)


def test_impact_grammar_accepts_semantic_variants_but_not_generic_assertions():
    brief, _ = build_effective_brief(ReviewTaskV2(content_type="marketing"))
    gaps, _ = _parsed([
        _item("目标受众是否为现有客户？", "受众答案决定 meaning 和 recommended_outcome"),
        _item("此产品场景是否允许夸张表达？", "会影响 role_routing 与 release_decision"),
        _item("产品经理最喜欢哪种颜色？", "这个问题很重要，最好询问"),
        _item("是否还有更多背景？", "会影响结论"),
    ])
    selected, all_gaps = select_context_gaps(gaps, brief, active_role_ids=ACTIVE)
    assert [gap.question for gap in selected] == [gaps[0].question, gaps[1].question]
    reasons = {gap.question: gap.reason for gap in all_gaps if gap.disposition == "suppressed"}
    assert reasons[gaps[2].question] == "immaterial_gap"
    assert reasons[gaps[3].question] == "generic_curiosity"


def test_answered_duplicate_limit_and_invalid_roles_remain_bounded():
    brief, _ = build_effective_brief(ReviewTaskV2(
        content_type="marketing", audience="现有客户", context="首页横幅"
    ))
    gaps, _ = _parsed([
        _item("目标受众是谁？", "受众会改变建议", ["unknown_role"]),
        _item("该文案是品牌标语还是功能按钮？", "用途决定角色路由", ["brand_voice_reviewer", "unknown_role"]),
        _item("该文案是品牌标语还是功能按钮？", "用途决定角色路由", ["brand_voice_reviewer"]),
        _item("是否存在官方约束词表？", "词表影响选项有效性", ["terminology_reviewer"]),
        _item("产品上下文是否改变发布决定？", "产品上下文改变发布决定", ["product_context_reviewer"]),
    ])
    selected, all_gaps = select_context_gaps(gaps, brief, active_role_ids=ACTIVE)
    assert len(selected) == 2
    assert selected[0].affected_role_ids == ["brand_voice_reviewer"]
    reasons = [gap.reason for gap in all_gaps if gap.disposition == "suppressed"]
    assert "already_answered" in reasons
    assert "duplicate_gap" in reasons
    assert "question_limit" in reasons
