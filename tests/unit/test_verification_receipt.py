from copy import deepcopy

import pytest

from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    CouncilPlan,
    IssueCluster,
    PreflightCheck,
    PreflightResult,
    ReviewRecordV2,
    ReviewTaskV2,
    RuntimeMetadata,
)
from council_of_translation.localization.compatibility import parse_review_record
from council_of_translation.localization.verification import (
    build_verification_receipt,
    render_verification_report,
)
from council_of_translation.localization.roles import build_council_plan


ROLE_IDS = [
    "technical_safety_reviewer",
    "fidelity_reviewer",
    "terminology_reviewer",
]


def _full_record() -> ReviewRecordV2:
    final = "- 最终处置：修改后可发布；需人工复核：否"
    return ReviewRecordV2(
        schema_version="2.5",
        review_id="20260824T010203000004Z_ab12cd34",
        parent_review_id="20260823T010203000004Z_cd34ef56",
        task=ReviewTaskV2(
            source_text="SECRET SOURCE {count}",
            candidate_translation="SECRET CANDIDATE",
            content_type="technical_documentation",
            history_mode="full",
        ),
        runtime_metadata=RuntimeMetadata(
            sampling_calls=3,
            elicitation_calls=2,
            sample_budget=13,
            reviewer_samples_successful=2,
            reviewer_samples_unavailable=1,
            reviewer_coverage="partial",
            briefing_elicitation_calls=1,
            context_gap_elicitation_calls=1,
            outcome_elicitation_calls=0,
            wall_clock_ms=876,
            sampling_wait_ms=650,
            independent_review_concurrency_limit=3,
            independent_review_peak_concurrency=3,
            independent_review_batch_count=1,
            independent_review_concurrency_disposition="configured",
        ),
        council_plan=CouncilPlan(
            mode="standard",
            content_type="technical_documentation",
            active_role_ids=ROLE_IDS,
            sample_budget=13,
            routing_profile="route_technical_documentation_standard_v1",
            routing_reason_codes=[
                "content_technical_documentation",
                "mode_standard",
                "legacy_portfolio_preserved",
            ],
        ),
        independent_reviews=[
            {"agent_name": ROLE_IDS[0], "sample_status": "structured_success", "role_feedback": "SECRET FEEDBACK"},
            {"agent_name": ROLE_IDS[1], "sample_status": "unavailable", "sample_error": "SECRET ERROR"},
            {"agent_name": ROLE_IDS[2], "sample_status": "structured_success", "findings": [{"problem": "SECRET PROBLEM"}]},
        ],
        preflight=PreflightResult(checks=[
            PreflightCheck(
                check_id="braced-placeholder-parity",
                kind="placeholder_parity",
                status="fail",
                severity="critical",
                blocking=True,
                message="SECRET CHECK MESSAGE",
            ),
            PreflightCheck(
                check_id="numeric-parity",
                kind="numeric_signal",
                status="warning",
                severity="major",
                message="SECRET WARNING MESSAGE",
            ),
        ]),
        issue_clusters=[
            IssueCluster(
                issue_id="issue_secret",
                topic="SECRET TOPIC",
                category="integrity",
                severity="critical",
                blocking=True,
            ),
            IssueCluster(
                issue_id="issue_secret_2",
                topic="SECRET TOPIC 2",
                category="new_private_family",
                severity="minor",
            ),
        ],
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="修改后可发布",
            review_needed="否",
            decision_rationale="SECRET RATIONALE",
            suggested_translation=None,
        ),
        status="COMPLETED_WITH_FALLBACK",
        fallback_reason="reviewer_coverage_partial",
        degraded=True,
        warnings=["SECRET WARNING"],
        display_report=f"# SECRET REPORT\n\n{final}",
        version_metadata={
            "package_version": "0.11.1",
            "diagnostic_build": "risk-coherent-council-v9.1",
            "record_schema": "2.5",
        },
    )


def test_full_v25_receipt_has_exact_canonical_shape_and_values():
    receipt = build_verification_receipt(_full_record())

    assert list(receipt) == [
        "receipt_schema_version", "review_id", "record", "serving", "routing",
        "reviewer_execution", "runtime", "preflight", "issues", "outcome", "coherence",
        "availability",
    ]
    assert list(receipt["record"]) == [
        "schema_version", "history_mode", "parent_review_id", "recorded_package_version",
        "recorded_diagnostic_build",
    ]
    assert list(receipt["serving"]) == [
        "package_version", "module_version", "diagnostic_build", "schema_version"
    ]
    assert list(receipt["routing"]) == [
        "mode", "content_type", "profile", "reason_codes", "active_role_ids"
    ]
    assert list(receipt["reviewer_execution"]) == [
        "samples", "coverage", "successful_count", "unavailable_count"
    ]
    assert list(receipt["runtime"]) == [
        "sampling_calls_total", "sample_budget_total", "elicitation_calls_total",
        "briefing_elicitation_calls", "context_gap_elicitation_calls",
        "outcome_elicitation_calls", "wall_clock_ms", "sampling_wait_ms",
        "independent_review_concurrency_limit", "independent_review_peak_concurrency",
        "independent_review_batch_count", "independent_review_concurrency_disposition",
    ]
    assert list(receipt["preflight"]) == [
        "blocking", "failed_check_count", "failed_blocking_check_count",
        "failed_blocking_check_kinds",
    ]
    assert list(receipt["issues"]) == [
        "cluster_count", "blocking_cluster_count", "severity_counts", "category_counts"
    ]
    assert list(receipt["outcome"]) == [
        "status", "degraded", "warning_count", "fallback_reason_code",
        "fallback_reason_redacted", "publishability", "review_needed",
        "suggested_translation_present",
    ]
    assert list(receipt["coherence"]) == [
        "expected_terminal_disposition", "terminal_disposition_occurrences",
        "terminal_disposition_is_last_report_line", "terminal_disposition_matches_structured",
    ]
    assert receipt["receipt_schema_version"] == "1.0"
    assert receipt["record"]["recorded_package_version"] == "0.11.1"
    assert receipt["routing"]["active_role_ids"] == ROLE_IDS
    assert receipt["reviewer_execution"]["samples"] == [
        {"role_id": ROLE_IDS[0], "sample_status": "structured_success"},
        {"role_id": ROLE_IDS[1], "sample_status": "unavailable"},
        {"role_id": ROLE_IDS[2], "sample_status": "structured_success"},
    ]
    assert receipt["preflight"] == {
        "blocking": True,
        "failed_check_count": 1,
        "failed_blocking_check_count": 1,
        "failed_blocking_check_kinds": ["placeholder_parity"],
    }
    assert receipt["issues"]["category_counts"] == {"integrity": 1, "other": 1}
    assert receipt["issues"]["severity_counts"] == {
        "critical": 1, "major": 0, "minor": 1, "preference": 0
    }
    assert receipt["coherence"] == {
        "expected_terminal_disposition": "- 最终处置：修改后可发布；需人工复核：否",
        "terminal_disposition_occurrences": 1,
        "terminal_disposition_is_last_report_line": True,
        "terminal_disposition_matches_structured": True,
    }
    assert receipt["availability"] == {
        "verification_complete": True,
        "not_recorded_fields": [],
        "redacted_fields": [],
    }


def test_receipt_and_report_are_deterministic_pure_and_privacy_safe():
    record = _full_record()
    before = deepcopy(record.model_dump(mode="json"))

    first = build_verification_receipt(record)
    second = build_verification_receipt(record)
    report = render_verification_report(first)

    assert first == second
    assert record.model_dump(mode="json") == before
    assert [line for line in report.splitlines() if line.startswith("#")] == [
        "# Council 验证回执",
        "## 记录与路由",
        "## 覆盖与调用",
        "## 风险与裁决",
        "## 一致性与可用性",
    ]
    assert len(report) <= 2_400
    assert "`technical_safety_reviewer`" in report
    assert "SECRET" not in str(first)
    assert "SECRET" not in report
    for prohibited in ("source_text", "candidate_translation", "role_feedback", "issue_secret"):
        assert prohibited not in str(first)


def test_unknown_codes_are_null_redacted_and_never_echoed():
    record = _full_record()
    record.fallback_reason = "PRIVATE prose with a path C:/SECRET"

    receipt = build_verification_receipt(record)

    assert receipt["outcome"]["fallback_reason_code"] is None
    assert receipt["outcome"]["fallback_reason_redacted"] is True
    assert receipt["availability"] == {
        "verification_complete": False,
        "not_recorded_fields": [],
        "redacted_fields": ["outcome.fallback_reason_code"],
    }
    assert "PRIVATE" not in str(receipt)
    assert "SECRET" not in str(receipt)


@pytest.mark.parametrize(
    ("mode", "sampling_calls", "budget", "publishability", "review_needed", "status"),
    [
        ("standard", 7, 13, "修改后可发布", "否", "COMPLETED"),
        ("lightweight", 4, 6, "可发布", "否", "COMPLETED"),
        ("strict", 8, 18, "需人工复核", "是", "NEEDS_HUMAN_REVIEW"),
    ],
)
def test_q013_shaped_full_records_preserve_exact_route_roles_calls_and_outcomes(
    mode, sampling_calls, budget, publishability, review_needed, status
):
    record = _full_record()
    plan = build_council_plan(mode, "legal_risk")
    record.council_plan = plan
    record.independent_reviews = [
        {"agent_name": role_id, "sample_status": "structured_success"}
        for role_id in plan.active_role_ids
    ]
    record.runtime_metadata = RuntimeMetadata(
        sampling_calls=sampling_calls,
        elicitation_calls=0,
        sample_budget=budget,
        reviewer_samples_successful=len(plan.active_role_ids),
        reviewer_samples_unavailable=0,
        reviewer_coverage="full",
        independent_review_concurrency_limit=3,
        independent_review_peak_concurrency=min(3, len(plan.active_role_ids)),
        independent_review_batch_count=(len(plan.active_role_ids) + 2) // 3,
        independent_review_concurrency_disposition="default",
    )
    record.chief_editor_decision = ChiefEditorDecisionV2(
        publishability=publishability, review_needed=review_needed
    )
    record.status = status
    record.fallback_reason = ""
    record.degraded = False
    record.warnings = []
    terminal = f"- 最终处置：{publishability}；需人工复核：{review_needed}"
    record.display_report = f"# 审校背景\n\n{terminal}"

    receipt = build_verification_receipt(record)

    assert receipt["routing"] == {
        "mode": mode,
        "content_type": "legal_risk",
        "profile": plan.routing_profile,
        "reason_codes": plan.routing_reason_codes,
        "active_role_ids": plan.active_role_ids,
    }
    assert receipt["reviewer_execution"]["samples"] == [
        {"role_id": role_id, "sample_status": "structured_success"}
        for role_id in plan.active_role_ids
    ]
    assert receipt["reviewer_execution"]["coverage"] == "full"
    assert receipt["runtime"]["sampling_calls_total"] == sampling_calls
    assert receipt["runtime"]["sample_budget_total"] == budget
    assert receipt["runtime"]["elicitation_calls_total"] == 0
    assert receipt["outcome"]["publishability"] == publishability
    assert receipt["outcome"]["review_needed"] == review_needed
    assert receipt["coherence"]["terminal_disposition_matches_structured"] is True


def test_projection_has_zero_executor_gateway_orchestration_and_store_save_activity(monkeypatch):
    from council_of_translation.localization import orchestration, persistence, runtime

    calls = {"executor": 0, "gateway": 0, "orchestration": 0, "save": 0}

    async def forbidden_executor(*args, **kwargs):
        calls["executor"] += 1
        raise AssertionError("executor activity is forbidden")

    async def forbidden_gateway(*args, **kwargs):
        calls["gateway"] += 1
        raise AssertionError("gateway activity is forbidden")

    async def forbidden_orchestration(*args, **kwargs):
        calls["orchestration"] += 1
        raise AssertionError("orchestration activity is forbidden")

    def forbidden_save(*args, **kwargs):
        calls["save"] += 1
        raise AssertionError("save activity is forbidden")

    monkeypatch.setattr(runtime.ScriptedModelExecutor, "sample", forbidden_executor)
    monkeypatch.setattr(runtime.ScriptedUserInteractionGateway, "elicit", forbidden_gateway)
    monkeypatch.setattr(orchestration, "run_structured_review", forbidden_orchestration)
    monkeypatch.setattr(persistence.ReviewStore, "save", forbidden_save)

    receipt = build_verification_receipt(_full_record())
    render_verification_report(receipt)

    assert calls == {"executor": 0, "gateway": 0, "orchestration": 0, "save": 0}


@pytest.mark.parametrize("schema_version", ["2.0", "2.1", "2.2", "2.3", "2.4"])
def test_historical_v2_availability_is_schema_aware_without_compatibility_defaults(schema_version):
    payload = _full_record().model_dump(mode="json")
    payload["schema_version"] = schema_version
    payload["version_metadata"]["record_schema"] = schema_version
    payload["council_plan"].pop("routing_profile", None)
    payload["council_plan"].pop("routing_reason_codes", None)
    if schema_version in {"2.0", "2.1", "2.2"}:
        for field in (
            "wall_clock_ms", "sampling_wait_ms", "independent_review_concurrency_limit",
            "independent_review_peak_concurrency", "independent_review_batch_count",
            "independent_review_concurrency_disposition",
        ):
            payload["runtime_metadata"].pop(field, None)
    if schema_version in {"2.0", "2.1"}:
        for field in (
            "briefing_elicitation_calls", "context_gap_elicitation_calls",
            "outcome_elicitation_calls",
        ):
            payload["runtime_metadata"].pop(field, None)
        payload.pop("display_report", None)
    if schema_version == "2.0":
        payload.pop("degraded", None)
        payload.pop("warnings", None)

    receipt = build_verification_receipt(parse_review_record(payload))
    unavailable = set(receipt["availability"]["not_recorded_fields"])

    assert receipt["record"]["schema_version"] == schema_version
    assert receipt["record"]["history_mode"] == "full"
    assert receipt["routing"]["profile"] is None
    assert receipt["routing"]["reason_codes"] is None
    assert {"routing.profile", "routing.reason_codes"} <= unavailable
    if schema_version in {"2.0", "2.1", "2.2"}:
        assert receipt["runtime"]["wall_clock_ms"] is None
        assert "runtime.independent_review_concurrency_disposition" in unavailable
    else:
        assert receipt["runtime"]["wall_clock_ms"] == 876
    if schema_version in {"2.0", "2.1"}:
        assert receipt["runtime"]["briefing_elicitation_calls"] is None
        assert receipt["coherence"]["expected_terminal_disposition"] is None
    else:
        assert receipt["runtime"]["briefing_elicitation_calls"] == 1
        assert receipt["coherence"]["terminal_disposition_matches_structured"] is True
    assert receipt["availability"]["redacted_fields"] == []
    assert receipt["availability"]["verification_complete"] is True


def test_v1_projects_only_physically_recorded_bounded_fields():
    legacy = parse_review_record({
        "review_id": "20260824_010203",
        "mode": "standard",
        "status": "completed",
        "chief_editor_decision": {"publishability": "可发布", "review_needed": "否"},
        "task": {"source": "PRIVATE SOURCE"},
        "reviews": [{"feedback": "PRIVATE REVIEW"}],
    })

    receipt = build_verification_receipt(legacy)
    report = render_verification_report(receipt)

    assert receipt["record"]["history_mode"] == "legacy"
    assert receipt["routing"]["mode"] == "standard"
    assert receipt["outcome"]["status"] == "completed"
    assert receipt["outcome"]["publishability"] == "可发布"
    assert receipt["outcome"]["review_needed"] == "否"
    assert receipt["runtime"]["sampling_calls_total"] is None
    assert receipt["availability"]["not_recorded_fields"] == sorted(
        receipt["availability"]["not_recorded_fields"]
    )
    assert receipt["availability"]["verification_complete"] is True
    assert "PRIVATE" not in str(receipt)
    assert "PRIVATE" not in report


def test_hostile_roles_codes_statuses_paths_and_prose_are_redacted_without_echo():
    record = _full_record()
    record.version_metadata = {
        "package_version": "C:/PRIVATE/version",
        "diagnostic_build": "PRIVATE build prose",
        "record_schema": "2.5",
    }
    record.council_plan = CouncilPlan.model_construct(
        mode="PRIVATE MODE",
        content_type="PRIVATE CONTENT",
        active_role_ids=["PRIVATE ROLE"],
        routing_profile="PRIVATE PROFILE",
        routing_reason_codes=["PRIVATE REASON"],
    )
    record.independent_reviews = [
        {"agent_name": "PRIVATE ROLE", "sample_status": "PRIVATE STATUS"}
    ]
    record.runtime_metadata.independent_review_concurrency_disposition = "PRIVATE CONCURRENCY"
    record.preflight = PreflightResult.model_construct(
        checks=[PreflightCheck.model_construct(status="fail", blocking=True, kind="PRIVATE CHECK")],
        blocking=True,
    )
    record.status = "PRIVATE OUTCOME"
    record.fallback_reason = "C:/PRIVATE/fallback prose"
    record.chief_editor_decision.publishability = "PRIVATE VERDICT"
    record.chief_editor_decision.review_needed = "PRIVATE REVIEW"
    record.display_report = "PRIVATE REPORT"

    receipt = build_verification_receipt(record)
    report = render_verification_report(receipt)

    assert receipt["availability"]["verification_complete"] is False
    assert receipt["availability"]["redacted_fields"] == sorted(
        receipt["availability"]["redacted_fields"]
    )
    for path in (
        "record.recorded_package_version",
        "record.recorded_diagnostic_build",
        "routing.mode",
        "routing.content_type",
        "routing.profile",
        "routing.reason_codes",
        "routing.active_role_ids",
        "reviewer_execution.samples",
        "runtime.independent_review_concurrency_disposition",
        "preflight.failed_blocking_check_kinds",
        "outcome.status",
        "outcome.fallback_reason_code",
        "outcome.publishability",
        "outcome.review_needed",
        "coherence.expected_terminal_disposition",
    ):
        assert path in receipt["availability"]["redacted_fields"]
    assert "PRIVATE" not in str(receipt)
    assert "PRIVATE" not in report
