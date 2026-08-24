from __future__ import annotations

import asyncio
import json

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


_CLEAN = json.dumps({"role_feedback": "checked", "findings": []})


def _run(task: ReviewTaskV2, script: list[object], tmp_path, *, gateway=None):
    telemetry = RuntimeTelemetry(sample_budget=18)
    return asyncio.run(run_structured_review(
        task,
        ScriptedModelExecutor(script, telemetry),
        gateway or ScriptedUserInteractionGateway(telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))


def _rich_task(**updates: object) -> ReviewTaskV2:
    task = ReviewTaskV2(
        source_text="Save 12",
        candidate_translation="保存 12",
        content_type="ui",
        context="settings primary action",
        audience="general users",
        style_guide="concise",
        term_glossary="Save=保存",
    )
    return task.model_copy(update=updates)


def test_clean_parent_persists_one_coherent_schema_26_assessment(tmp_path):
    record = _run(_rich_task(), [_CLEAN] * 6, tmp_path)
    loaded = ReviewStore(tmp_path, include_legacy=False).load(record.review_id)

    assert record.schema_version == loaded.schema_version == "2.6"
    assert record.decision_support == loaded.decision_support
    assert record.decision_support.level == "well_supported"
    assert record.decision_support.basis_codes == [
        "full_reviewer_coverage", "clean_confirmation"
    ]
    assert record.decision_support.outcome_coherent is True


def test_partial_coverage_is_insufficient_and_never_publishable(tmp_path):
    record = _run(
        _rich_task(),
        [_CLEAN, _CLEAN, RuntimeError("unavailable"), _CLEAN, _CLEAN, _CLEAN],
        tmp_path,
    )
    assert record.decision_support.level == "insufficient"
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert record.decision_support.outcome_coherent is True


def test_full_coverage_deterministic_blocker_is_well_supported_negative_disposition(tmp_path):
    task = _rich_task(
        candidate_translation="保存",
        hard_constraints=["numeric_parity"],
    )
    record = _run(task, [_CLEAN] * 6, tmp_path)
    assert record.preflight.blocking is True
    assert record.decision_support.level == "well_supported"
    assert "deterministic_blocker" in record.decision_support.basis_codes
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.status == "NEEDS_HUMAN_REVIEW"


def test_required_briefing_pending_is_assessed_before_any_sampling(tmp_path):
    task = ReviewTaskV2(
        source_text="Save", candidate_translation="保存", briefing_mode="always"
    )
    telemetry = RuntimeTelemetry(sample_budget=18)
    gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(action="decline")], telemetry=telemetry
    )
    record = asyncio.run(run_structured_review(
        task,
        ScriptedModelExecutor([_CLEAN] * 6, telemetry),
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    assert record.schema_version == "2.6"
    assert record.runtime_metadata.sampling_calls == 0
    assert record.decision_support.level == "insufficient"
    assert "pending_user_input" in record.decision_support.limitation_codes
    assert record.decision_support.outcome_coherent is True
