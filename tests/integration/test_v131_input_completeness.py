from __future__ import annotations

import asyncio
import json

import pytest

from council_of_translation.localization.orchestration import (
    compact_review_response,
    continue_structured_review,
    run_structured_review,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)
from council_of_translation.localization.verification import build_verification_receipt
from council_of_translation.tools.review import MAX_REVIEW_FIELD_LENGTH, _task_and_diagnostics


_CLEAN = json.dumps({"role_feedback": "checked", "findings": []})


class _CountingStore(ReviewStore):
    def __init__(self, root):
        super().__init__(root, include_legacy=False)
        self.save_count = 0

    def save(self, record, *, history_mode=None):
        self.save_count += 1
        return super().save(record, history_mode=history_mode)


def _task(source: str, candidate: str, **updates):
    values = {
        "source_text": source,
        "candidate_translation": candidate,
        "source_language": "en",
        "target_language": "zh-CN",
        "content_type": "ui",
        "context": "settings primary action",
        "audience": "general users",
        "mode": "standard",
        "output_mode": "review_only",
        "interactive_mode": "off",
        "briefing_mode": "off",
        "decision_fallback": "council_adjudication",
        "trace_level": "summary",
        "history_mode": "full",
        "term_glossary": "Save=保存",
        "style_guide": "concise",
        "project_rules": "",
        "brand_guidelines": "",
        "technical_constraints": "",
        "do_not_translate_literals": None,
        "hard_constraints": None,
        "reference_translations": "",
        "known_exceptions": "",
        "notes": "",
    }
    values.update(updates)
    return _task_and_diagnostics(**values)


def _run(task, diagnostics, store, *, script=None, gateway=None):
    telemetry = RuntimeTelemetry(sample_budget=13)
    record = asyncio.run(run_structured_review(
        task,
        ScriptedModelExecutor(script or [_CLEAN] * 6, telemetry),
        gateway or ScriptedUserInteractionGateway(telemetry=telemetry),
        store=store,
        input_diagnostics=diagnostics,
    ))
    return record, telemetry


@pytest.mark.parametrize(
    ("source_extra", "candidate_extra", "expected_warnings"),
    [
        (1, 0, {"input_truncated", "source_input_truncated"}),
        (0, 1, {"input_truncated", "candidate_input_truncated"}),
        (1, 1, {"input_truncated", "source_input_truncated", "candidate_input_truncated"}),
    ],
)
def test_truncation_is_fail_closed_in_full_compact_and_receipt(
    tmp_path, source_extra, candidate_extra, expected_warnings
):
    task, diagnostics = _task(
        "S" * (MAX_REVIEW_FIELD_LENGTH + source_extra),
        "译" * (MAX_REVIEW_FIELD_LENGTH + candidate_extra),
    )
    store = _CountingStore(tmp_path / "records")
    record, telemetry = _run(task, diagnostics, store)

    assert diagnostics.source_reviewed_length <= MAX_REVIEW_FIELD_LENGTH
    assert diagnostics.candidate_reviewed_length <= MAX_REVIEW_FIELD_LENGTH
    assert set(record.warnings) == expected_warnings
    assert record.degraded is True
    assert "input_truncated" in record.fallback_reason.split(";")
    assert record.decision_support.level == "insufficient"
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert record.chief_editor_decision.review_needed == "是"
    assert "仅审校了有界前缀" in record.display_report
    assert "不构成全文发布许可" in record.display_report
    compact = compact_review_response(record)
    assert compact["degraded"] is True
    assert set(compact["warnings"]) == expected_warnings
    assert compact["decision_support"]["level"] == "insufficient"
    receipt = build_verification_receipt(record)
    assert receipt["outcome"]["degraded"] is True
    assert receipt["outcome"]["fallback_reason_code"] == "input_truncated"
    assert receipt["outcome"]["publishability"] == "需人工复核"
    assert receipt["decision_support"]["level"] == "insufficient"
    assert telemetry.sampling_calls == 6
    assert telemetry.elicitation_calls == 0
    assert store.save_count == 1


def test_exact_boundary_is_complete_but_boundary_plus_one_is_not(tmp_path):
    exact_task, exact_diagnostics = _task(
        "S" * MAX_REVIEW_FIELD_LENGTH, "译" * MAX_REVIEW_FIELD_LENGTH
    )
    exact, _ = _run(exact_task, exact_diagnostics, _CountingStore(tmp_path / "exact"))
    assert exact.input_diagnostics.source_reviewed_length == MAX_REVIEW_FIELD_LENGTH
    assert exact.input_diagnostics.candidate_reviewed_length == MAX_REVIEW_FIELD_LENGTH
    assert exact.input_diagnostics.source_truncated is False
    assert exact.input_diagnostics.candidate_truncated is False
    assert exact.degraded is False
    assert exact.status == "COMPLETED"

    long_task, long_diagnostics = _task(
        "S" * (MAX_REVIEW_FIELD_LENGTH + 1), "译" * MAX_REVIEW_FIELD_LENGTH
    )
    long, _ = _run(long_task, long_diagnostics, _CountingStore(tmp_path / "long"))
    assert long.input_diagnostics.source_reviewed_length == MAX_REVIEW_FIELD_LENGTH
    assert long.status == "NEEDS_HUMAN_REVIEW"


def test_clean_prefix_with_critical_omitted_suffix_never_claims_complete_publication(tmp_path):
    task, diagnostics = _task(
        "S" * MAX_REVIEW_FIELD_LENGTH + "CRITICAL_OMITTED_SUFFIX",
        "译" * MAX_REVIEW_FIELD_LENGTH,
    )
    record, _ = _run(task, diagnostics, _CountingStore(tmp_path / "records"))
    assert "CRITICAL_OMITTED_SUFFIX" not in record.task.source_text
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert record.chief_editor_decision.publishability == "需人工复核"
    assert "不构成全文发布许可" in record.display_report


def test_truncation_survives_briefing_return_and_deterministic_blocker(tmp_path):
    task, diagnostics = _task(
        "Save 12 " + "S" * MAX_REVIEW_FIELD_LENGTH,
        "保存 " + "译" * MAX_REVIEW_FIELD_LENGTH,
        briefing_mode="always",
        interactive_mode="auto",
        hard_constraints=["numeric_parity"],
    )
    telemetry = RuntimeTelemetry(sample_budget=13)
    gateway = ScriptedUserInteractionGateway(
        [ElicitationResult(action="decline")], telemetry=telemetry
    )
    record = asyncio.run(run_structured_review(
        task,
        ScriptedModelExecutor([_CLEAN] * 6, telemetry),
        gateway,
        store=_CountingStore(tmp_path / "records"),
        input_diagnostics=diagnostics,
    ))
    assert record.preflight.blocking is True
    assert record.decision_support.level == "insufficient"
    assert record.status == "NEEDS_HUMAN_REVIEW"
    assert "input_truncated" in record.warnings
    assert telemetry.sampling_calls == 0
    assert telemetry.elicitation_calls == 1


def test_metadata_history_and_continuation_cannot_relax_truncation(tmp_path):
    task, diagnostics = _task(
        "S" * (MAX_REVIEW_FIELD_LENGTH + 1),
        "译" * MAX_REVIEW_FIELD_LENGTH,
        history_mode="metadata",
    )
    store = _CountingStore(tmp_path / "records")
    parent, _ = _run(task, diagnostics, store)
    loaded = store.load(parent.review_id)
    assert loaded.input_diagnostics.source_truncated is True
    assert loaded.degraded is True
    assert loaded.status == "NEEDS_HUMAN_REVIEW"
    assert loaded.decision_support.level == "insufficient"

    telemetry = RuntimeTelemetry(sample_budget=13)
    child = asyncio.run(continue_structured_review(
        parent, [], ScriptedModelExecutor([], telemetry), store=store
    ))
    assert child.input_diagnostics == parent.input_diagnostics
    assert child.degraded is True
    assert child.status == "NEEDS_HUMAN_REVIEW"
    assert child.chief_editor_decision.publishability == "需人工复核"
    assert child.decision_support.level == "insufficient"
    assert "input_truncated" in child.warnings
    assert telemetry.sampling_calls == 0
    assert telemetry.elicitation_calls == 0
    assert store.save_count == 2
