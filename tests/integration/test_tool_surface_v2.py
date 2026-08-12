import asyncio

import pytest


pytest.importorskip("fastmcp")

from council_of_translation.server import mcp
from council_of_translation.localization.models import DecisionOption, DecisionPoint
from council_of_translation.localization.orchestration import (
    _decisions_from_elicitation,
    _interaction_form,
    _interaction_message,
)
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import ElicitationResult
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


def test_server_info_and_versioned_defaults():
    info = _server_info()
    assert info["package_version"] == "0.4.0"
    assert info["module_version"] == "0.4.0"
    assert info["diagnostic_build"] == DIAGNOSTIC_BUILD == "structured-deliberation-v2"
    assert info["default_interactive_mode"] == "auto"
    assert info["default_history_mode"] == "full"
    assert info["sample_budgets"] == {"lightweight": 6, "standard": 10, "strict": 14}


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

    for point in points:
        expected = [option.option_id for option in point.options]
        field = pydantic_schema["properties"][point.decision_id]
        assert field["enum"] == expected
        assert point.question in field["description"]
        assert all(option.label in field["description"] for option in point.options)
        assert fastmcp_schema["properties"][point.decision_id]["enum"] == expected
    message = _interaction_message(points)
    assert all(point.question in message for point in points)
    assert all(
        option.option_id in message and option.label in message and option.description in message
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
        [point], ElicitationResult(action="accept", data={point.decision_id: "not-valid"})
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
    assert result["error_type"] == "ReviewPersistenceError"
    assert result["error"] == "review record write failed"
    assert private_path not in str(result)
