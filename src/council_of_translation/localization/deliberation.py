"""Bounded issue selection, position matrices, and DecisionPoints."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Iterable

from council_of_translation.localization.models import (
    DecisionOption,
    DecisionPoint,
    DiscussionRound,
    DiscussionTurn,
    IssueCluster,
    ReviewMode,
    RolePosition,
)


MODE_SAMPLE_BUDGETS: dict[ReviewMode, int] = {"lightweight": 6, "standard": 10, "strict": 14}
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
                "confidence": position.confidence,
                "blocking": position.blocking,
                "conditions": position.conditions,
            }
            for position in cluster.positions
            if position.role_id in cluster.participant_role_ids
        ]
    }


def normalize_discussion_round(round_id: str, clusters: list[IssueCluster], raw_turns: Iterable[dict]) -> DiscussionRound:
    allowed = {
        cluster.issue_id: set(cluster.participant_role_ids)
        for cluster in clusters
    }
    turns: list[DiscussionTurn] = []
    for raw in raw_turns:
        issue_id = str(raw.get("issue_id", ""))
        speaker = str(raw.get("speaker", ""))
        if issue_id not in allowed or speaker not in allowed[issue_id]:
            continue
        turns.append(DiscussionTurn.model_validate({**raw, "round_id": round_id}))
    return DiscussionRound(round_id=round_id, issue_ids=list(allowed), turns=turns)


def _option_id(issue_id: str, action: str) -> str:
    digest = hashlib.sha256(f"{issue_id}\x1f{action}".encode()).hexdigest()[:10]
    return f"option_{digest}"


def build_decision_points(clusters: Iterable[IssueCluster], maximum: int = 3) -> list[DecisionPoint]:
    points: list[DecisionPoint] = []
    for cluster in clusters:
        actions = list(dict.fromkeys(action for action in cluster.candidate_actions if action))
        if cluster.blocking or not cluster.needs_user_input or len(actions) < 2:
            continue
        options = [
            DecisionOption(option_id=_option_id(cluster.issue_id, action), label=action, description=action)
            for action in actions
        ]
        points.append(
            DecisionPoint(
                decision_id=f"decision_{cluster.issue_id.removeprefix('issue_')}",
                issue_id=cluster.issue_id,
                question=f"请选择“{cluster.topic}”的有效处理方式",
                options=options,
                recommended_option_id=options[0].option_id,
                fallback_option_id=options[0].option_id,
                reason_user_input_useful="多个方案均满足当前硬约束，选择取决于上下文或偏好。",
            )
        )
        if len(points) >= min(maximum, 3):
            break
    return points

