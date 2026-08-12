import json

from council_of_translation.localization.models import (
    DecisionOption,
    DecisionPoint,
    IssueCluster,
    ReconsiderationProvenance,
    ReviewRecordV2,
    ReviewTaskV2,
    UserDecision,
)
from council_of_translation.localization.orchestration import (
    _deliberation_summary,
    _effective_task,
    compact_review_response,
)
from council_of_translation.localization.policy import build_chief_decision


def _cluster(issue_id: str, topic: str, severity: str = "minor") -> IssueCluster:
    return IssueCluster(
        issue_id=issue_id,
        topic=topic,
        category="language_choice",
        severity=severity,
        consensus_status="consensus",
    )


def test_chief_checklists_are_semantically_deduplicated_and_resolutions_not_optional():
    clusters = [
        _cluster("i1", "Fix spacing"),
        _cluster("i2", "Ｆｉｘ　ｓｐａｃｉｎｇ"),
    ]
    chief, _ = build_chief_decision(clusters, [], [])
    assert chief.optional_improvements == ["Fix spacing"]
    assert chief.execution_order == ["Fix spacing"]

    choice_cluster = _cluster("i3", "button wording")
    point = DecisionPoint(
        decision_id="d3",
        issue_id="i3",
        question="choose",
        options=[DecisionOption(option_id="o3", outcome_value="下一步", label="下一步")],
    )
    decision = UserDecision(
        decision_id="d3",
        selected_option_id="o3",
        selected_outcome_value="下一步",
        elicitation_action="accept",
    )
    chief, _ = build_chief_decision([choice_cluster], [point], [decision])
    assert chief.optional_improvements == []
    assert chief.terminology_decisions == ["对“button wording”采用“下一步”"]
    assert chief.execution_order == ["对“button wording”采用“下一步”"]


def test_effective_task_reports_presence_without_copying_rule_packets():
    task = ReviewTaskV2(
        content_type="ui",
        audience="new users",
        term_glossary="PRIVATE TB CONTENT",
        project_rules="PRIVATE RULE CONTENT",
        hard_constraints=["required_literal:PRIVATE_LITERAL", "numeric_parity"],
        do_not_translate_literals=["PRIVATE_DNT"],
    )
    effective = _effective_task(task)
    serialized = json.dumps(effective.model_dump(mode="json"))
    assert effective.content_type == "ui"
    assert effective.audience == "new users"
    assert "term_glossary:provided" in effective.material_rule_context
    assert "hard_constraint:required_literal" in effective.material_rule_context
    assert "PRIVATE" not in serialized

    aliased = _effective_task(ReviewTaskV2(content_type="product-ui"))
    assert aliased.content_type == "ui"


def test_compact_response_surfaces_decision_digest_degradation_and_retrieval_hint():
    cluster = _cluster("i1", "button wording")
    point = DecisionPoint(
        decision_id="d1",
        issue_id="i1",
        question="choose",
        options=[DecisionOption(option_id="o1", outcome_value="下一步", label="下一步")],
    )
    decision = UserDecision(
        decision_id="d1",
        selected_option_id="o1",
        selected_outcome_value="下一步",
        elicitation_action="accept",
    )
    chief, trace = build_chief_decision([cluster], [point], [decision])
    provenance = ReconsiderationProvenance(completed_role_ids=["ux_copy_reviewer"])
    record = ReviewRecordV2(
        review_id="20260812T010203000004Z_ab12cd34",
        task=ReviewTaskV2(content_type="ui", audience="new users"),
        issue_clusters=[cluster],
        decision_points=[point],
        user_decisions=[decision],
        chief_editor_decision=chief,
        decision_trace=trace,
        reconsideration_provenance=provenance,
        effective_task=_effective_task(ReviewTaskV2(content_type="ui", audience="new users")),
        deliberation_summary=_deliberation_summary([cluster], [decision], trace, provenance),
        status="COMPLETED_WITH_FALLBACK",
        degraded=True,
        warnings=["reconsideration_failed:ux_copy_reviewer"],
    )
    compact = compact_review_response(record)
    assert compact["effective_task"] == record.effective_task.model_dump(mode="json")
    assert compact["deliberation_summary"] == record.deliberation_summary.model_dump(mode="json")
    assert compact["degraded"] is True
    assert compact["warnings"] == record.warnings
    assert compact["review_id"] in compact["retrieval_hint"] or "review_id" in compact["retrieval_hint"]
    assert "suggested_translation" not in compact["chief_editor"]
    assert "reasoning" not in json.dumps(compact)


def test_hostile_model_topic_and_chief_lists_are_bounded_in_compact_output():
    clusters = [
        _cluster(f"i{index}", "恶" * 10_000)
        for index in range(20)
    ]
    chief, trace = build_chief_decision(clusters, [], [])
    record = ReviewRecordV2(
        review_id="20260812T010203000004Z_ab12cd34",
        task=ReviewTaskV2(),
        issue_clusters=clusters,
        chief_editor_decision=chief,
        decision_trace=trace,
    )
    compact = compact_review_response(record)
    assert len(compact["blind_spots"]) == 8
    assert all(len(item) <= 240 for item in compact["blind_spots"])
    for name in ("must_fix", "should_fix", "optional_improvements", "execution_order"):
        assert len(compact["chief_editor"][name]) <= 12
        assert all(len(item) <= 240 for item in compact["chief_editor"][name])
