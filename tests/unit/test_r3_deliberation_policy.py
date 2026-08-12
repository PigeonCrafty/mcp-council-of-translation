from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import (
    apply_discussion_updates,
    build_decision_points,
    normalize_discussion_round,
)
from council_of_translation.localization.models import (
    DecisionOption,
    DecisionPoint,
    FindingV2,
    RolePosition,
)
from council_of_translation.localization.policy import adjudicate_decision_point


def _finding(role: str, action: str) -> FindingV2:
    return FindingV2(
        agent_name=role,
        role_perspective=role,
        source_span="Continue button",
        candidate_span="继续按钮",
        issue_type="terminology" if role == "terminology_reviewer" else "fluency",
        problem="wording choice",
        evidence="observable wording evidence",
        action=action,
        confidence=0.8,
    )


def _production_cluster():
    return cluster_findings(
        [_finding("terminology_reviewer", "继续"), _finding("fluency_reviewer", "下一步")]
    )[0]


def test_production_positions_and_decision_points_share_authoritative_option_ids():
    cluster = _production_cluster()
    point = build_decision_points([cluster])[0]
    position_ids = {position.option_id for position in cluster.positions}
    point_ids = {option.option_id for option in point.options}

    assert position_ids == point_ids
    assert len(position_ids) == 2


def test_discussion_applies_only_safe_existing_option_changes():
    cluster = _production_cluster()
    before = {position.role_id: position.option_id for position in cluster.positions}
    round_ = normalize_discussion_round(
        "round_1",
        [cluster],
        [
            {
                "issue_id": cluster.issue_id,
                "speaker": "terminology_reviewer",
                "stance": "reconsider",
                "claim": "context favors navigation wording",
                "evidence": ["button advances a step"],
                "proposed_action": "下一步",
                "confidence": 0.9,
                "position_changed": True,
                "blocking": True,
                "constraint_tier": "hard",
            },
            {
                "issue_id": cluster.issue_id,
                "speaker": "unrelated_role",
                "proposed_action": "下一步",
                "position_changed": True,
            },
            {
                "issue_id": cluster.issue_id,
                "speaker": "fluency_reviewer",
                "proposed_action": "不存在的选项",
                "position_changed": True,
            },
        ],
    )

    assert len(round_.turns) == 1
    assert apply_discussion_updates([cluster], round_) == 1
    after = {position.role_id: position for position in cluster.positions}
    assert after["terminology_reviewer"].option_id == after["fluency_reviewer"].option_id
    assert after["terminology_reviewer"].option_id != before["terminology_reviewer"]
    assert after["terminology_reviewer"].blocking is False
    assert after["terminology_reviewer"].constraint_tier == "advisory"
    assert after["terminology_reviewer"].evidence_origin == "model"


def test_position_matrix_uses_provenance_tier_blocking_and_confidence_without_majority():
    point = DecisionPoint(
        decision_id="d",
        issue_id="i",
        question="q",
        options=[DecisionOption(option_id="trusted", label="Trusted"), DecisionOption(option_id="popular", label="Popular")],
    )
    positions = [
        RolePosition(
            role_id="technical_safety_reviewer",
            stance="accept",
            option_id="trusted",
            evidence=["explicit rule"],
            evidence_origin="caller",
            constraint_tier="contextual",
            rule_refs=["TB-1"],
            confidence=0.7,
        ),
        RolePosition(role_id="technical_safety_reviewer", stance="accept", option_id="popular", evidence=["taste"], confidence=0.7),
        RolePosition(role_id="technical_safety_reviewer", stance="accept", option_id="popular", evidence=["taste"], confidence=0.7),
    ]

    selected, basis, human = adjudicate_decision_point(point, positions, None)
    assert selected == "trusted"
    assert human is False
    assert basis == [
        "position_matrix",
        "role_relevance",
        "evidence_provenance",
        "constraint_tier",
        "blocking_state",
        "confidence",
    ]

    model_escalation = RolePosition(
        role_id="technical_safety_reviewer",
        stance="accept",
        option_id="trusted",
        evidence_origin="model",
        constraint_tier="hard",
        blocking=True,
    )
    assert model_escalation.constraint_tier == "advisory"
    assert model_escalation.blocking is False


def test_genuine_equal_evidence_tie_requires_human_review():
    point = DecisionPoint(
        decision_id="d",
        issue_id="i",
        question="q",
        options=[DecisionOption(option_id="a", label="A"), DecisionOption(option_id="b", label="B")],
    )
    positions = [
        RolePosition(role_id="fluency_reviewer", stance="accept", option_id="a", evidence=["usage"], confidence=0.8),
        RolePosition(role_id="fluency_reviewer", stance="accept", option_id="b", evidence=["usage"], confidence=0.8),
    ]
    assert adjudicate_decision_point(point, positions, None) == (
        "",
        ["indistinguishable_or_insufficient_valid_evidence"],
        True,
    )
