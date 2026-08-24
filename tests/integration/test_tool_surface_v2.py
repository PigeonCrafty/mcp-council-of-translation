import asyncio

import pytest


pytest.importorskip("fastmcp")

from council_of_translation.server import mcp
from council_of_translation.localization.models import DecisionOption, DecisionPoint
from council_of_translation.localization.orchestration import (
    _decisions_from_elicitation,
    _form_mapping,
    _interaction_form,
    _interaction_message,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import ElicitationResult
from council_of_translation.presentation import structured_payload
from council_of_translation.tools.review import (
    DIAGNOSTIC_BUILD,
    _server_info,
    _task_and_diagnostics,
    review_translation,
)


def test_exact_frozen_public_tool_surface():
    tools = asyncio.run(mcp.get_tools())
    assert set(tools) == {
        "review_translation",
        "continue_review",
        "view_review_record",
        "list_review_records",
        "get_server_info",
    }
    briefing = tools["review_translation"].parameters["properties"]["briefing_mode"]
    assert briefing == {
        "default": "auto",
        "enum": ["auto", "always", "off"],
        "type": "string",
    }
    detail = tools["view_review_record"].parameters["properties"]["detail_level"]
    assert detail == {
        "default": "full",
        "enum": ["full", "summary", "verification"],
        "type": "string",
    }


def test_server_info_and_versioned_defaults(monkeypatch):
    monkeypatch.delenv("COUNCIL_REVIEW_CONCURRENCY", raising=False)
    info = _server_info()
    assert info["package_version"] == "0.13.0"
    assert info["module_version"] == "0.13.0"
    assert info["diagnostic_build"] == DIAGNOSTIC_BUILD == "calibrated-evidence-council-v11"
    assert info["schema_version"] == "2.6"
    assert info["default_interactive_mode"] == "auto"
    assert info["default_briefing_mode"] == "auto"
    assert info["default_history_mode"] == "full"
    assert info["sample_budgets"] == {"lightweight": 6, "standard": 13, "strict": 18}
    assert info["independent_review_concurrency_limit"] == 3
    assert info["max_independent_review_concurrency"] == 3
    assert info["independent_review_concurrency_disposition"] == "default"
    assert info["verification_receipt_schema_version"] == "1.1"
    assert info["review_record_detail_levels"] == ["full", "summary", "verification"]


@pytest.mark.parametrize("configured", ["1", "2", "3"])
def test_server_info_reports_valid_concurrency_configuration(monkeypatch, configured):
    monkeypatch.setenv("COUNCIL_REVIEW_CONCURRENCY", configured)
    info = _server_info()
    assert info["independent_review_concurrency_limit"] == int(configured)
    assert info["max_independent_review_concurrency"] == 3
    assert info["independent_review_concurrency_disposition"] == "configured"


@pytest.mark.parametrize("configured", ["", "0", "4", "many"])
def test_server_info_reports_invalid_concurrency_fallback(monkeypatch, configured):
    monkeypatch.setenv("COUNCIL_REVIEW_CONCURRENCY", configured)
    info = _server_info()
    assert info["independent_review_concurrency_limit"] == 1
    assert info["max_independent_review_concurrency"] == 3
    assert info["independent_review_concurrency_disposition"] == "invalid_fallback"


def test_public_input_modes_normalize_conservatively():
    task, diagnostics = _task_and_diagnostics(
        source_text="Save",
        candidate_translation="保存",
        source_language="en",
        target_language="zh-CN",
        content_type="ui",
        context="",
        audience="",
        mode="unknown",
        output_mode="rewrite-anyway",
        interactive_mode="unknown",
        decision_fallback="unknown",
        trace_level="unknown",
        history_mode="unknown",
        term_glossary="",
        style_guide="",
        project_rules="",
        brand_guidelines="",
        technical_constraints="",
        do_not_translate_literals=None,
        hard_constraints=None,
        reference_translations="",
        known_exceptions="",
        notes="",
    )
    assert task.mode == "standard"
    assert task.output_mode == "review_only"
    assert task.interactive_mode == "auto"
    assert task.briefing_mode == "auto"
    assert task.decision_fallback == "council_adjudication"
    assert task.trace_level == "summary"
    assert task.history_mode == "full"
    assert diagnostics.source_truncated is False


def test_return_pending_requires_full_history():
    import pytest

    values = {
        "source_text": "Save",
        "candidate_translation": "保存",
        "source_language": "auto",
        "target_language": "zh-CN",
        "content_type": "ui",
        "context": "",
        "audience": "",
        "mode": "standard",
        "output_mode": "review_only",
        "interactive_mode": "auto",
        "decision_fallback": "return_pending",
        "trace_level": "summary",
        "history_mode": "metadata",
        "term_glossary": "",
        "style_guide": "",
        "project_rules": "",
        "brand_guidelines": "",
        "technical_constraints": "",
        "do_not_translate_literals": [],
        "hard_constraints": [],
        "reference_translations": "",
        "known_exceptions": "",
        "notes": "",
    }
    with pytest.raises(ValueError, match="requires history_mode=full"):
        _task_and_diagnostics(**values)


def test_batched_form_schema_and_fastmcp_conversion_expose_described_enums():
    from fastmcp.server.context import get_elicitation_schema

    points = [
        DecisionPoint(
            decision_id="decision_wording",
            issue_id="issue_wording",
            question="按钮应采用哪种措辞？",
            options=[
                DecisionOption(option_id="option_continue", label="继续", description="保持当前流程"),
                DecisionOption(option_id="option_next", label="下一步", description="强调导航动作"),
            ],
        ),
        DecisionPoint(
            decision_id="decision_tone",
            issue_id="issue_tone",
            question="语气应如何处理？",
            options=[
                DecisionOption(option_id="option_formal", label="正式", description="面向企业用户"),
                DecisionOption(option_id="option_casual", label="轻松", description="面向消费者"),
            ],
        ),
    ]
    form = _interaction_form(points)
    pydantic_schema = form.model_json_schema()
    fastmcp_schema = get_elicitation_schema(form)

    for index, point in enumerate(points, start=1):
        expected = list(_form_mapping(point))
        field_name = f"review_choice_{index}"
        field = pydantic_schema["properties"][field_name]
        assert field["enum"] == expected
        assert field["title"] == point.question
        assert all(option.description in field["description"] for option in point.options)
        assert fastmcp_schema["properties"][field_name]["enum"] == expected
        assert all(option.option_id not in field["description"] for option in point.options)
    message = _interaction_message(points)
    assert all(point.question in message for point in points)
    assert all(
        option.option_id not in message and option.label in message and option.description in message
        for point in points
    for option in point.options
    )


def test_missing_or_invalid_accepted_form_data_degrades_to_malformed():
    point = DecisionPoint(
        decision_id="decision_wording",
        issue_id="issue_wording",
        question="选择措辞",
        options=[DecisionOption(option_id="valid", label="有效")],
    )
    missing = _decisions_from_elicitation([point], ElicitationResult(action="accept", data={}))
    invalid = _decisions_from_elicitation(
        [point], ElicitationResult(action="accept", data={"review_choice_1": "not-valid"})
    )
    assert missing[0].elicitation_action == "malformed"
    assert invalid[0].elicitation_action == "malformed"


def test_public_review_normalizes_atomic_write_failure_without_path(monkeypatch, tmp_path):
    from council_of_translation.localization import orchestration, persistence

    store = ReviewStore(tmp_path / "records", legacy_dir=tmp_path / "legacy")
    monkeypatch.setattr(orchestration, "ReviewStore", lambda: store)
    private_path = str(tmp_path / "PRIVATE" / "record.json")

    def fail_replace(source, destination):
        raise OSError(f"cannot replace {private_path}")

    monkeypatch.setattr(persistence.os, "replace", fail_replace)

    class RawJsonContext:
        async def sample(self, *args, **kwargs):
            return '{"role_feedback":"ok","findings":[]}'

    result = asyncio.run(
        review_translation.fn(
            source_text="Save",
            candidate_translation="保存",
            ctx=RawJsonContext(),
        )
    )
    payload = structured_payload(result)
    assert payload["error_type"] == "ReviewPersistenceError"
    assert payload["error"] == "review record write failed"
    assert private_path not in str(payload)
