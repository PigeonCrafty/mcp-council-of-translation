import asyncio
import json

from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


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
