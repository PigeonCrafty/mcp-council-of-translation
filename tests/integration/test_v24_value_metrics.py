import asyncio
import json

import pytest

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def _envelope(*findings):
    return json.dumps({
        "role_feedback": "checked the assigned scope",
        "findings": list(findings),
    })


def _technical_finding(source_span, candidate_span, *, evidence):
    return {
        "issue_type": "technical",
        "severity": "critical",
        "source_span": source_span,
        "candidate_span": candidate_span,
        "problem": "Required source structure is missing",
        "evidence": evidence,
        "action": "Restore the required source structure",
        "confidence": 0.99,
    }


def test_metrics_add_no_sampling_or_elicitation_to_clean_review(tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=6)
    clean = json.dumps({"role_feedback": "checked", "findings": []})
    executor = ScriptedModelExecutor([clean] * 6, telemetry)
    gateway = ScriptedUserInteractionGateway([], telemetry=telemetry)

    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Save",
            candidate_translation="保存",
            content_type="ui",
            mode="lightweight",
            briefing_mode="off",
            interactive_mode="off",
        ),
        executor,
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))

    assert record.runtime_metadata.sampling_calls == len(record.council_plan.active_role_ids) == 4
    assert record.runtime_metadata.elicitation_calls == 0
    assert record.council_value_metrics.confirmation_only_role_count == len(
        record.council_plan.active_role_ids
    )
    assert {item.contribution_kind for item in record.council_value_metrics.role_contributions} == {
        "confirmation_only"
    }


@pytest.mark.parametrize(("source", "candidate", "span", "evidence"), [
    ("Delete {count} files", "删除文件", "{count}", "{count}"),
    ("Click <b>Save</b>", "点击保存", "<b>", "required tag <b>"),
])
def test_preflight_and_model_support_are_one_visible_issue_without_clean_contradiction(
    tmp_path, source, candidate, span, evidence
):
    telemetry = RuntimeTelemetry(sample_budget=6)
    finding = _technical_finding(span, "", evidence=evidence)
    scripts = [_envelope(finding, finding), *[_envelope() for _ in range(3)]]
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text=source,
            candidate_translation=candidate,
            content_type="ui",
            mode="lightweight",
            briefing_mode="off",
            interactive_mode="off",
        ),
        ScriptedModelExecutor(scripts, telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))

    technical = next(
        item for item in record.council_value_metrics.role_contributions
        if item.role_id == "technical_safety_reviewer"
    )
    assert record.preflight.blocking is True
    assert technical.contribution_kind == "unique_material"
    assert technical.unique_issue_count == technical.material_finding_count == 1
    assert record.council_value_metrics.unique_material_issue_count == 1
    assert "新增 1 个独立问题" in record.display_report
    assert "未发现新增实质问题" not in record.display_report
    assert record.chief_editor_decision.publishability != "可发布"


def test_preflight_issue_remains_visible_when_technical_review_is_unavailable(tmp_path):
    telemetry = RuntimeTelemetry(sample_budget=6)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Delete {count} files",
            candidate_translation="删除文件",
            content_type="ui",
            mode="lightweight",
            briefing_mode="off",
            interactive_mode="off",
        ),
        ScriptedModelExecutor([RuntimeError("technical sample failed"), *[_envelope() for _ in range(3)]], telemetry),
        ScriptedUserInteractionGateway([], telemetry=telemetry),
        store=ReviewStore(tmp_path, include_legacy=False),
    ))

    technical = next(
        item for item in record.council_value_metrics.role_contributions
        if item.role_id == "technical_safety_reviewer"
    )
    assert technical.contribution_kind == "unavailable"
    assert technical.unique_issue_count == technical.material_finding_count == 1
    assert record.council_value_metrics.unique_material_issue_count == 1
    assert record.council_value_metrics.unavailable_role_count == 1
    assert "覆盖风险" in record.display_report
    assert "未发现新增实质问题" not in record.display_report
    assert record.chief_editor_decision.publishability != "可发布"
