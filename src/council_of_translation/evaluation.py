"""Executable offline golden-corpus evaluation for Council regression evidence."""

from __future__ import annotations

import asyncio
import json
import re
from typing import Any, Iterable, get_args

from council_of_translation.localization.models import ReviewRecordV2, ReviewTaskV2
from council_of_translation.localization.orchestration import (
    continue_structured_review,
    run_structured_review,
)
from council_of_translation.localization.runtime import (
    ElicitationResult,
    InteractionCapabilities,
    ModelExecutionResult,
    RuntimeEvent,
    RuntimeTelemetry,
)


_PROPERTIES = (
    "critical_issue_recalled",
    "false_positive_free",
    "contribution_kinds",
    "conflict_detected",
    "user_authority",
    "chief_consistent",
    "sampling_calls",
    "sample_budget",
    "discussion_marginal_value",
)
_PACKET = re.compile(r"=== (?P<name>[A-Z_]+) START ===\n(?P<body>.*?)\n=== (?P=name) END ===", re.DOTALL)


def _safe_case(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("golden case must be an object")
    case_id = value.get("case_id")
    expected = value.get("expected")
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("golden case requires case_id")
    if "observed" in value:
        raise ValueError(f"golden case {case_id} must not contain fixture-authored observed data")
    if not isinstance(value.get("task"), dict) or not isinstance(value.get("reviewers"), dict):
        raise ValueError(f"golden case {case_id} requires task and reviewer envelope inputs")
    if not isinstance(expected, dict):
        raise ValueError(f"golden case {case_id} requires expected outcomes")
    missing = [key for key in _PROPERTIES if key not in expected]
    if missing:
        raise ValueError(f"golden case {case_id} lacks properties: {', '.join(missing)}")
    return value


def _packets(prompt: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for match in _PACKET.finditer(prompt):
        try:
            result[match.group("name")] = json.loads(match.group("body"))
        except (TypeError, ValueError):
            continue
    return result


class _GoldenExecutor:
    """Prompt-aware deterministic executor that still traverses production parsing."""

    def __init__(self, case: dict[str, Any]) -> None:
        self.case = case
        self.telemetry = RuntimeTelemetry()
        self.prompts: list[str] = []

    def _independent(self, packet: dict[str, Any]) -> dict[str, Any] | BaseException:
        role_id = str(packet.get("id", ""))
        envelope = self.case["reviewers"].get(role_id)
        if envelope == "error":
            return RuntimeError(f"scripted unavailable reviewer: {role_id}")
        if envelope is None:
            return {"role_feedback": "assigned scope checked", "findings": []}
        return envelope

    def _discussion(self, issues: list[dict[str, Any]]) -> dict[str, Any]:
        mode = str(self.case.get("discussion", "none"))
        if mode == "none" or not issues:
            return {"turns": []}
        issue = issues[0]
        roles = list(issue.get("participant_role_ids", []))
        turn: dict[str, Any] = {
            "issue_id": issue.get("issue_id", ""),
            "speaker": roles[0] if roles else "",
            "target": roles[1] if len(roles) > 1 else "",
            "stance": "qualify",
            "claim": "bounded golden discussion claim",
            "evidence": ["independent supplemental evidence"],
            "confidence": 0.8,
            "position_changed": False,
        }
        if mode == "material":
            actions = list(issue.get("candidate_actions", []))
            positions = list(issue.get("positions", []))
            if actions and positions:
                target_action = actions[0]
                target_option = next(
                    (position.get("option_id") for position in positions if position.get("role_id") == roles[0]),
                    "",
                )
                for position in positions:
                    if position.get("option_id") != target_option:
                        turn["speaker"] = position.get("role_id", turn["speaker"])
                        break
                turn["proposed_action"] = target_action
                turn["position_changed"] = True
        return {"turns": [turn]}

    def _reconsider(self, packet: dict[str, Any]) -> dict[str, Any]:
        decisions = {item.get("decision_id"): item for item in packet.get("user_decisions", [])}
        positions = []
        for issue in packet.get("issues", []):
            decision = decisions.get(f"decision_{str(issue.get('issue_id', '')).removeprefix('issue_')}")
            if not decision:
                continue
            positions.append({
                "issue_id": issue.get("issue_id", ""),
                "stance": "accept",
                "option_id": decision.get("selected_option_id", ""),
                "claim": "accepted the valid user-selected outcome",
                "evidence": ["explicit user selection"],
                "confidence": 0.9,
                "blocking": False,
                "conditions": [],
            })
        return {"positions": positions}

    async def sample(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 1_400,
    ) -> ModelExecutionResult:
        del temperature, max_tokens
        self.prompts.append(prompt)
        packets = _packets(prompt)
        if "CONTEXT_RECONSIDERATION" in packets:
            scripted = self.case.get("context_reconsideration", {})
            value: dict[str, Any] | BaseException = {
                "change_effect": scripted.get("change_effect", "unchanged"),
                "findings": scripted.get("findings", []),
            }
        elif "ISSUE_PACKETS" in packets:
            value = self._discussion(packets["ISSUE_PACKETS"])
        elif "RECONSIDERATION_PACKET" in packets:
            value = self._reconsider(packets["RECONSIDERATION_PACKET"])
        else:
            value = self._independent(packets.get("ROLE_DEFINITION", {}))
        if isinstance(value, BaseException):
            result = ModelExecutionResult(status="error", error=str(value)[:240])
        else:
            result = ModelExecutionResult(
                status="success",
                text=json.dumps(value, ensure_ascii=False, separators=(",", ":")),
            )
        self.telemetry.record(RuntimeEvent("sampling", result.status, detail=result.error))
        return result


class _GoldenGateway:
    """Schema-driven deterministic interaction adapter for corpus authority cases."""

    def __init__(self, case: dict[str, Any], telemetry: RuntimeTelemetry) -> None:
        self.case = case
        self.telemetry = telemetry
        self.requests: list[str] = []

    def capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(form_elicitation=bool(self.case.get("interaction")))

    async def elicit(self, message: str, *, response_type: Any) -> ElicitationResult:
        self.requests.append(message)
        interaction = self.case.get("interaction", {})
        if interaction.get("initial_action") == "decline":
            result = ElicitationResult(action="decline")
            self.telemetry.record(RuntimeEvent("elicitation", result.action))
            return result
        fields = response_type.model_fields
        if fields and all(name.startswith("context_") for name in fields):
            answer = str(interaction.get("context_answer", "confirmed product context"))
            result = ElicitationResult(
                action="accept",
                data={name: answer for name in fields},
            )
        else:
            choice_index = int(interaction.get("choice_index", 1))
            data: dict[str, str] = {}
            for name, field in fields.items():
                choices = [value for value in get_args(field.annotation) if isinstance(value, str)]
                non_delegation = [value for value in choices if not value.startswith("暂不决定")]
                selected = non_delegation[min(choice_index, len(non_delegation) - 1)]
                data[name] = selected
            result = ElicitationResult(action="accept", data=data)
        self.telemetry.record(RuntimeEvent("elicitation", result.action))
        return result


def _observed(
    case: dict[str, Any],
    record: ReviewRecordV2,
    *,
    deterministic_preference_rejected: bool = False,
) -> dict[str, Any]:
    expected_roles = set(case["expected"]["contribution_kinds"])
    contributions = {
        item.role_id: item.contribution_kind
        for item in record.council_value_metrics.role_contributions
        if item.role_id in expected_roles
    }
    has_critical = any(
        cluster.blocking or cluster.severity == "critical"
        for cluster in record.issue_clusters
    )
    is_clean_case = case.get("category") == "clean"
    accepted = any(decision.elicitation_action == "accept" for decision in record.user_decisions)
    answered_context = bool(record.context_gap_interaction.answered_gap_ids)
    deterministic_blocker = any(cluster.blocking for cluster in record.issue_clusters)
    critical_issue = any(cluster.severity == "critical" for cluster in record.issue_clusters)
    if deterministic_preference_rejected:
        authority = "blocked_by_policy"
    elif answered_context:
        authority = "context_update_applied"
    elif accepted and (deterministic_blocker or critical_issue):
        authority = "blocked_by_policy"
    elif accepted:
        authority = "valid_choice_respected"
    elif record.context_gap_interaction.requested:
        authority = "context_requested"
    else:
        authority = "not_applicable"
    chief_consistent = (
        bool(record.chief_editor_decision.decision_rationale)
        and (
            not deterministic_blocker
            or (
                record.chief_editor_decision.review_needed == "是"
                and record.chief_editor_decision.publishability != "可发布"
            )
        )
        and (
            not critical_issue
            or record.chief_editor_decision.publishability != "可发布"
        )
    )
    return {
        "critical_issue_recalled": has_critical,
        "false_positive_free": not record.issue_clusters if is_clean_case else True,
        "contribution_kinds": contributions,
        "conflict_detected": bool(record.discussion_rounds),
        "user_authority": authority,
        "chief_consistent": chief_consistent,
        "sampling_calls": record.runtime_metadata.sampling_calls,
        "sample_budget": record.runtime_metadata.sample_budget,
        "discussion_marginal_value": record.council_value_metrics.discussion_marginal_value,
    }


async def run_golden_cases(cases: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Execute the actual production review path and compare runtime observations."""
    values = [_safe_case(case) for case in cases]
    if not values:
        raise ValueError("golden corpus must not be empty")

    failures: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    property_matches = {key: 0 for key in _PROPERTIES}
    critical_expected = 0
    critical_recalled = 0
    total_sampling_calls = 0
    total_elicitation_calls = 0
    for case in values:
        task = ReviewTaskV2.model_validate({
            "source_language": "en",
            "target_language": "zh-CN",
            "content_type": "ui",
            "mode": "standard",
            "briefing_mode": "off",
            "interactive_mode": "off",
            "history_mode": "off",
            **case["task"],
        })
        executor = _GoldenExecutor(case)
        gateway = _GoldenGateway(case, executor.telemetry)
        record = await run_structured_review(task, executor, gateway)
        deterministic_preference_rejected = False
        if case.get("continuation_probe") == "reject_invalid_then_accept_valid":
            point = record.decision_points[0]
            invalid = next(option for option in point.options if not option.valid)
            valid = next(
                option for option in point.options
                if option.valid and not option.is_current_candidate and not option.is_delegation
            )
            try:
                await continue_structured_review(
                    record,
                    [{"decision_id": point.decision_id, "selected_option_id": invalid.option_id}],
                    executor,
                )
            except ValueError as exc:
                deterministic_preference_rejected = (
                    "invalid option" in str(exc)
                    and invalid.option_id in str(exc)
                )
            record = await continue_structured_review(
                record,
                [{"decision_id": point.decision_id, "selected_option_id": valid.option_id}],
                executor,
            )
        observed = _observed(
            case,
            record,
            deterministic_preference_rejected=deterministic_preference_rejected,
        )
        observations.append({
            "case_id": case["case_id"],
            "observed": observed,
            "status": record.status,
            "publishability": record.chief_editor_decision.publishability,
            "continuation_preference_rejected": deterministic_preference_rejected,
            "sampling_calls": record.runtime_metadata.sampling_calls,
            "elicitation_calls": record.runtime_metadata.elicitation_calls,
        })
        total_sampling_calls += record.runtime_metadata.sampling_calls
        total_elicitation_calls += record.runtime_metadata.elicitation_calls
        for key in _PROPERTIES:
            matches = observed[key] == case["expected"][key]
            property_matches[key] += int(matches)
            if not matches:
                failures.append({
                    "case_id": case["case_id"],
                    "property": key,
                    "expected": case["expected"][key],
                    "observed": observed[key],
                })
        if case["expected"]["critical_issue_recalled"]:
            critical_expected += 1
            critical_recalled += int(bool(observed["critical_issue_recalled"]))
        if observed["sampling_calls"] > observed["sample_budget"]:
            failures.append({
                "case_id": case["case_id"],
                "property": "call_budget",
                "expected": f"<= {observed['sample_budget']}",
                "observed": observed["sampling_calls"],
            })

    total = len(values)
    failed_case_ids = sorted({item["case_id"] for item in failures})
    return {
        "schema_version": "2.0",
        "total_cases": total,
        "passed_cases": total - len(failed_case_ids),
        "failed_case_ids": failed_case_ids,
        "critical_issue_recall": critical_recalled / critical_expected if critical_expected else 1.0,
        "false_positive_free_rate": property_matches["false_positive_free"] / total,
        "contribution_kind_accuracy": property_matches["contribution_kinds"] / total,
        "conflict_detection_accuracy": property_matches["conflict_detected"] / total,
        "user_authority_accuracy": property_matches["user_authority"] / total,
        "chief_consistency_rate": property_matches["chief_consistent"] / total,
        "call_budget_accuracy": (
            property_matches["sampling_calls"] + property_matches["sample_budget"]
        ) / (2 * total),
        "discussion_marginal_value_accuracy": property_matches["discussion_marginal_value"] / total,
        "runtime_observations": {
            "sampling_calls": total_sampling_calls,
            "elicitation_calls": total_elicitation_calls,
            "case_results": observations,
        },
        "failures": failures,
    }


def evaluate_golden_cases(cases: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Synchronous entry point for the deterministic, offline production runner."""
    return asyncio.run(run_golden_cases(cases))
