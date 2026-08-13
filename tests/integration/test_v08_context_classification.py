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


def _classify(task, item):
    brief, effective_task = build_effective_brief(task)
    selected, all_gaps = select_context_gaps(
        _parsed([item])[0], brief, active_role_ids=ACTIVE, task=effective_task
    )
    return len(selected), all_gaps[0].disposition, all_gaps[0].reason


def test_caller_reference_packets_answer_only_corresponding_existence_questions():
    glossary_question = _item(
        "是否存在官方批准且具有约束力的标语词表？",
        "官方词表会改变允许采用的品牌措辞",
        ["terminology_reviewer", "brand_voice_reviewer"],
    )
    reference_question = _item(
        "是否有批准的参考译法？",
        "批准译法会改变允许采用的选项",
        ["terminology_reviewer"],
    )
    truth_table = [
        (ReviewTaskV2(content_type="marketing", term_glossary="标语词表"), glossary_question, 0, "already_answered"),
        (ReviewTaskV2(content_type="marketing"), glossary_question, 1, ""),
        (ReviewTaskV2(content_type="marketing", reference_translations="批准译法"), reference_question, 0, "already_answered"),
        (ReviewTaskV2(content_type="marketing"), reference_question, 1, ""),
        (ReviewTaskV2(content_type="marketing", style_guide="品牌风格"), glossary_question, 1, ""),
        (ReviewTaskV2(content_type="marketing", project_rules="遵循规则"), reference_question, 1, ""),
        (ReviewTaskV2(content_type="marketing", term_glossary="标语词表"), _item(
            "目标受众是谁？", "受众会改变品牌建议", ["brand_voice_reviewer"]
        ), 1, ""),
        (ReviewTaskV2(content_type="marketing", term_glossary="标语词表"), _item(
            "官方术语在这里是否语义正确？", "语义会改变建议", ["terminology_reviewer"]
        ), 1, ""),
    ]
    for task, item, expected_selected, expected_reason in truth_table:
        selected, disposition, reason = _classify(task, item)
        assert selected == expected_selected
        assert disposition == ("suppressed" if expected_reason else "unanswered")
        assert reason == expected_reason


def test_brand_or_functional_usage_requires_matching_explicit_single_side_context():
    compound = _item(
        "该文案是品牌标语还是功能按钮？",
        "用途会改变角色路由与建议选项",
        ["brand_voice_reviewer", "product_context_reviewer"],
    )
    truth_table = [
        (ReviewTaskV2(content_type="marketing", context="官网首页品牌宣传标语"), 0, "already_answered"),
        (ReviewTaskV2(content_type="ui", context="多步骤设置向导底部主操作按钮"), 0, "already_answered"),
        (ReviewTaskV2(content_type="marketing"), 1, ""),
        (ReviewTaskV2(context="官网首页品牌宣传标语"), 1, ""),
        (ReviewTaskV2(content_type="marketing", context="官网首页"), 1, ""),
        (ReviewTaskV2(content_type="marketing", context="多步骤设置向导底部主操作按钮"), 1, ""),
        (ReviewTaskV2(content_type="marketing", context="品牌标语用于设置向导主操作按钮"), 1, ""),
        (ReviewTaskV2(content_type="ui", context="官网首页品牌宣传标语"), 1, ""),
    ]
    for task, expected_selected, expected_reason in truth_table:
        selected, disposition, reason = _classify(task, compound)
        assert selected == expected_selected
        assert disposition == ("suppressed" if expected_reason else "unanswered")
        assert reason == expected_reason
