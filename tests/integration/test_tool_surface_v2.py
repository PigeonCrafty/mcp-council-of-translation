import asyncio

import pytest


pytest.importorskip("fastmcp")

from council_of_translation.server import mcp
from council_of_translation.tools.review import DIAGNOSTIC_BUILD, _server_info, _task_and_diagnostics


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
