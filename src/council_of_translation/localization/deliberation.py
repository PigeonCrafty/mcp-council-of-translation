"""Bounded issue selection, position matrices, and DecisionPoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pydantic import ValidationError

from council_of_translation.localization.models import (
    DecisionOption,
    DecisionPoint,
    DiscussionRound,
    DiscussionTurn,
    IssueCluster,
    ReviewMode,
    RolePosition,
    option_id_for_action,
)
from council_of_translation.localization.clustering import outcome_key


MODE_SAMPLE_BUDGETS: dict[ReviewMode, int] = {"lightweight": 6, "standard": 13, "strict": 18}
_DISCUSSION_LIMITS: dict[ReviewMode, tuple[int, int]] = {
    "lightweight": (1, 2),
    "standard": (1, 3),
    "strict": (2, 4),
}


@dataclass
class SampleBudget:
    mode: ReviewMode
    used: int = 0

    @property
    def limit(self) -> int:
        return MODE_SAMPLE_BUDGETS[self.mode]

    @property
    def remaining(self) -> int:
        return self.limit - self.used

    def consume(self, count: int = 1) -> None:
        if count < 0 or self.used + count > self.limit:
            raise RuntimeError(f"{self.mode} sampling budget exceeded: {self.used + count}>{self.limit}")
        self.used += count


def select_discussion_issues(clusters: Iterable[IssueCluster], mode: ReviewMode) -> list[IssueCluster]:
    issue_limit, participant_limit = _DISCUSSION_LIMITS[mode]
    eligible = [
        cluster
        for cluster in clusters
        if cluster.consensus_status == "disputed"
        and not cluster.blocking
        and len(cluster.participant_role_ids) >= 2
    ]
    severity_rank = {"critical": 3, "major": 2, "minor": 1, "preference": 0}
    eligible.sort(key=lambda cluster: (-severity_rank[cluster.severity], cluster.issue_id))
    selected: list[IssueCluster] = []
    for cluster in eligible[:issue_limit]:
        selected.append(cluster.model_copy(update={"participant_role_ids": cluster.participant_role_ids[:participant_limit]}))
    return selected


def position_matrix(cluster: IssueCluster) -> dict[str, list[dict[str, object]]]:
    return {
        cluster.issue_id: [
            {
                "role_id": position.role_id,
                "stance": position.stance,
                "option_id": position.option_id,
                "claim": position.claim,
                "evidence": position.evidence,
                "evidence_origin": position.evidence_origin,
                "constraint_tier": position.constraint_tier,
                "rule_refs": position.rule_refs,
                "confidence": position.confidence,
                "blocking": position.blocking,
                "conditions": position.conditions,
            }
            for position in cluster.positions
            if position.role_id in cluster.participant_role_ids
        ]
    }


class DiscussionEnvelopeUnavailable(ValueError):
    """Raised when one unsafe discussion envelope must be rejected atomically."""


def normalize_discussion_round(round_id: str, clusters: list[IssueCluster], raw_turns: object) -> DiscussionRound:
    packets = {cluster.issue_id: cluster for cluster in clusters}
    allowed = {issue_id: set(cluster.participant_role_ids) for issue_id, cluster in packets.items()}
    if not isinstance(raw_turns, list):
        raise DiscussionEnvelopeUnavailable("discussion turns must be a list")
    turns: list[DiscussionTurn] = []
    for raw in raw_turns:
        if not isinstance(raw, dict):
            raise DiscussionEnvelopeUnavailable("discussion turn must be an object")
        issue_id = raw.get("issue_id")
        speaker = raw.get("speaker")
        if not isinstance(issue_id, str) or not issue_id:
            raise DiscussionEnvelopeUnavailable("discussion turn has no issue reference")
        if not isinstance(speaker, str) or not speaker:
            raise DiscussionEnvelopeUnavailable("discussion turn has no speaker reference")
        if issue_id not in allowed or speaker not in allowed[issue_id]:
            raise DiscussionEnvelopeUnavailable("discussion turn has an unknown reference")
        try:
            turn = DiscussionTurn.model_validate({**raw, "round_id": round_id})
        except (ValidationError, TypeError, ValueError) as exc:
            raise DiscussionEnvelopeUnavailable("discussion turn failed schema validation") from exc
        cluster = packets[issue_id]
        if turn.proposed_action and turn.proposed_action not in cluster.candidate_actions:
            raise DiscussionEnvelopeUnavailable("discussion turn proposed an invalid action")
        if turn.position_changed:
            previous = next((item for item in cluster.positions if item.role_id == speaker), None)
            if (
                previous is None
                or previous.blocking
                or previous.constraint_tier == "hard"
                or not turn.proposed_action
                or turn.proposed_action not in cluster.candidate_actions
                or option_id_for_action(cluster.issue_id, turn.proposed_action) == previous.option_id
            ):
                raise DiscussionEnvelopeUnavailable("discussion turn declared an invalid position change")
        turns.append(turn)
    return DiscussionRound(round_id=round_id, issue_ids=list(allowed), turns=turns)


def apply_discussion_updates(clusters: Iterable[IssueCluster], round_: DiscussionRound) -> int:
    """Apply safe declared discussion changes to their existing matrix rows."""
    by_issue = {cluster.issue_id: cluster for cluster in clusters}
    applied = 0
    for turn in round_.turns:
        if not turn.position_changed:
            continue
        cluster = by_issue.get(turn.issue_id)
        if (
            cluster is None
            or turn.speaker not in cluster.participant_role_ids
            or turn.proposed_action not in cluster.candidate_actions
        ):
            continue
        previous = next((item for item in cluster.positions if item.role_id == turn.speaker), None)
        if previous is None or previous.blocking or previous.constraint_tier == "hard":
            continue
        revised = previous.model_copy(
            update={
                "stance": "accept",
                "option_id": option_id_for_action(cluster.issue_id, turn.proposed_action),
                "claim": turn.claim or previous.claim,
                "evidence": turn.evidence or previous.evidence,
                "evidence_origin": "model",
                "constraint_tier": "advisory",
                "rule_refs": [],
                "confidence": turn.confidence,
                "blocking": False,
            }
        )
        cluster.positions = [revised if item.role_id == turn.speaker else item for item in cluster.positions]
        applied += 1
    return applied


def build_decision_points(clusters: Iterable[IssueCluster], maximum: int = 3) -> list[DecisionPoint]:
    points: list[DecisionPoint] = []
    for cluster in clusters:
        actions = list(dict.fromkeys(outcome_key(action) for action in cluster.candidate_actions if action))
        if (
            cluster.blocking
            or cluster.category != "language_choice"
            or cluster.severity in {"critical", "major"}
            or not cluster.needs_user_input
            or len(actions) < 2
        ):
            continue
        outcome_options = [
            DecisionOption(
                option_id=option_id_for_action(cluster.issue_id, action),
                outcome_value=action,
                label=action,
                description=(
                    "保留当前候选译文"
                    if cluster.current_outcome and action == outcome_key(cluster.current_outcome)
                    else f"采用候选结果：{action}"
                ),
                support_role_ids=list(dict.fromkeys(
                    position.role_id
                    for position in cluster.positions
                    if position.option_id == option_id_for_action(cluster.issue_id, action)
                )),
                support_rationale="；".join(dict.fromkeys(
                    evidence
                    for position in cluster.positions
                    if position.option_id == option_id_for_action(cluster.issue_id, action)
                    for evidence in position.evidence
                )),
                policy_basis=["policy_gate_valid"],
                is_current_candidate=bool(
                    cluster.current_outcome
                    and action == outcome_key(cluster.current_outcome)
                ),
            )
            for index, action in enumerate(actions[:3])
        ]
        # Delegation is an interaction action, not a candidate outcome. PKG-013
        # appends it to the standard form without polluting the Position Matrix.
        options = [*outcome_options]
        anchor = next((value for value in [*cluster.source_spans, *cluster.candidate_spans] if value), "当前片段")
        category_label = {
            "language_choice": "措辞",
            "integrity": "完整性",
        }.get(cluster.category, "审校")
        points.append(
            DecisionPoint(
                decision_id=f"decision_{cluster.issue_id.removeprefix('issue_')}",
                issue_id=cluster.issue_id,
                question=f"“{anchor[:24]}”的{category_label}结果",
                options=options,
                recommended_option_id=outcome_options[0].option_id,
                fallback_option_id=outcome_options[0].option_id,
                reason_user_input_useful="多个方案均满足当前硬约束，选择取决于上下文或偏好。",
            )
        )
        if len(points) >= min(maximum, 3):
            break
    return points
