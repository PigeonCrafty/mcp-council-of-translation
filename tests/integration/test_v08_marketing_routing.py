import asyncio
import json

from council_of_translation.localization.clustering import cluster_findings
from council_of_translation.localization.deliberation import build_decision_points
from council_of_translation.localization.models import FindingV2, ReviewTaskV2, option_id_for_action
from council_of_translation.localization.orchestration import _form_mapping, run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def test_standard_marketing_deep_path_fits_exact_thirteen_calls(tmp_path):
    roles = build_council_plan("standard", "marketing").active_role_ids
    assert len(roles) == 6
    findings = [
        FindingV2(
            agent_name=role_id,
            source_span="bigger than bigger",
            candidate_span="比大更大",
            issue_type="style",
            severity="minor",
            finding_kind="choice",
            proposed_value="比大更大" if index < 3 else "胜过伟大",
            problem="品牌措辞选择",
            evidence="品牌与产品语境",
            action="按已确认用途选择",
            confidence=0.8,
        )
        for index, role_id in enumerate(roles)
    ]
    cluster = cluster_findings(findings)[0]
    point = build_decision_points([cluster])[0]
    selected_value = next(
        value for value, option in _form_mapping(point).items()
        if option is not None and option.outcome_value == "胜过伟大"
    )
    reviews = []
    for index, finding in enumerate(findings):
        payload = {
            "role_feedback": f"role-{index}",
            "findings": [finding.model_dump(mode="json")],
        }
        if index == 0:
            payload["context_gaps"] = [{
                "question": "该文案是品牌标语还是功能按钮？",
                "materiality": "用途会改变角色路由与建议选项",
                "affected_role_ids": roles[:3],
            }]
        reviews.append(json.dumps(payload, ensure_ascii=False))
    context_reconsiderations = [
        json.dumps({"change_effect": "unchanged", "findings": []}) for _ in range(3)
    ]
    discussion = json.dumps({"turns": []})
    outcome_reconsiderations = [
        json.dumps({"positions": [{
            "issue_id": cluster.issue_id,
            "stance": "accept",
            "option_id": option_id_for_action(cluster.issue_id, "胜过伟大"),
            "claim": "接受有效用户选择",
            "evidence": ["已确认品牌用途"],
            "confidence": 0.8,
        }]}, ensure_ascii=False)
        for _ in range(3)
    ]
    telemetry = RuntimeTelemetry(sample_budget=13)
    executor = ScriptedModelExecutor(
        [*reviews, *context_reconsiderations, discussion, *outcome_reconsiderations],
        telemetry,
    )
    gateway = ScriptedUserInteractionGateway([
        ElicitationResult(action="accept", data={"context_1": "这是官网品牌标语。"}),
        ElicitationResult(action="accept", data={"review_choice_1": selected_value}),
    ], telemetry=telemetry)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="bigger than bigger",
            candidate_translation="比大更大",
            content_type="marketing",
            briefing_mode="off",
            mode="standard",
        ),
        executor,
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    assert record.council_plan.active_role_ids == roles
    assert len(record.process_digest.role_lenses) == 6
    assert record.runtime_metadata.sampling_calls == record.runtime_metadata.sample_budget == 13
    assert record.runtime_metadata.reviewer_samples_successful == 6
    assert record.runtime_metadata.reviewer_coverage == "full"
    assert len(record.context_reconsideration_provenance.completed_role_ids) == 3
    assert len(record.outcome_reconsideration_provenance.completed_role_ids) == 3
    markers = [
        "CONTEXT" if "CONTEXT_RECONSIDERATION" in prompt
        else "DISCUSSION" if "ISSUE_PACKETS" in prompt
        else "OUTCOME" if "RECONSIDERATION_PACKET" in prompt
        else "INDEPENDENT"
        for prompt in executor.prompts
    ]
    assert markers == ["INDEPENDENT"] * 6 + ["CONTEXT"] * 3 + ["DISCUSSION"] + ["OUTCOME"] * 3
