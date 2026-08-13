import asyncio
import json

from council_of_translation.localization.guided import (
    CONTEXT_ASSUMPTION_VALUE,
    build_effective_brief,
    parse_context_gaps,
    select_context_gaps,
)
from council_of_translation.localization.models import ReviewTaskV2
from council_of_translation.localization.orchestration import _review_findings, run_structured_review
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.runtime import (
    ElicitationResult,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
)


def _envelope(*, gaps=None, findings=None):
    return json.dumps({
        "role_feedback": "完成职责内检查。",
        "findings": findings or [],
        **({"context_gaps": gaps} if gaps is not None else {}),
    }, ensure_ascii=False)


def _gap(question="该按钮出现在哪个流程阶段？", materiality="答案会改变交互语义判断和建议选项", roles=None):
    return {
        "question": question,
        "materiality": materiality,
        "affected_role_ids": roles or ["fidelity_reviewer"],
    }


def _run(tmp_path, reviews, interactions, *, mode="standard", extra_samples=None, supported=True):
    telemetry = RuntimeTelemetry(sample_budget=18)
    executor = ScriptedModelExecutor([*reviews, *(extra_samples or [])], telemetry)
    gateway = ScriptedUserInteractionGateway(interactions, supported=supported, telemetry=telemetry)
    record = asyncio.run(run_structured_review(
        ReviewTaskV2(
            source_text="Continue", candidate_translation="继续", content_type="ui",
            mode=mode, briefing_mode="off",
        ),
        executor,
        gateway,
        store=ReviewStore(tmp_path, include_legacy=False),
    ))
    return record, executor, gateway


def test_invalid_context_gap_isolated_from_valid_finding():
    raw = {
        "role_feedback": "发现一个语言选择。",
        "findings": [{
            "source_span": "Continue", "candidate_span": "继续", "issue_type": "ux",
            "finding_kind": "choice", "proposed_value": "下一步", "problem": "选择",
            "evidence": "按钮", "action": "考虑替换",
        }],
        "context_gaps": [{"question": 123}, "bad"],
    }
    feedback, findings, gaps, invalid, error = _review_findings(raw, "fidelity_reviewer")
    assert feedback and len(findings) == 1 and not error
    assert gaps == [] and invalid == 2


def test_valid_duplicate_answered_and_immaterial_gap_selection_is_bounded():
    task = ReviewTaskV2(
        source_text="Continue", candidate_translation="继续", content_type="ui",
        audience="管理员", context="设置页",
    )
    brief, _ = build_effective_brief(task)
    raw = [
        _gap(),
        _gap(),
        _gap(question="目标用户是谁？"),
        _gap(question="是否还有更多背景？"),
        _gap(question="产品版本是什么？", materiality="只是好奇"),
        _gap(question="这是主操作还是次操作？", roles=["ux_copy_reviewer"]),
    ]
    parsed, invalid = parse_context_gaps(raw, "fidelity_reviewer")
    selected, all_gaps = select_context_gaps(parsed, brief)
    assert invalid == 1  # reviewer envelope is capped at five gaps
    assert len(selected) <= 2
    reasons = {gap.reason for gap in all_gaps if gap.disposition == "suppressed"}
    assert {"duplicate_gap", "already_answered", "generic_curiosity"} <= reasons


def test_one_two_question_form_and_affected_role_reconsideration(tmp_path):
    reviews = [
        _envelope(gaps=[
            _gap(roles=["fidelity_reviewer"]),
            _gap(
                question="该文案是否面向高风险确认操作？",
                materiality="答案会改变风险判断和最终建议",
                roles=["risk_ambiguity_reviewer"],
            ),
        ]),
        *[_envelope() for _ in range(5)],
    ]
    reconsider = json.dumps({"change_effect": "unchanged", "findings": []})
    record, executor, gateway = _run(
        tmp_path,
        reviews,
        [ElicitationResult(action="accept", data={"context_1": "设置流程的下一步按钮", "context_2": CONTEXT_ASSUMPTION_VALUE})],
        extra_samples=[reconsider],
    )
    assert len(gateway.requests) == 1
    schema = gateway.requests[0][1].model_json_schema()
    assert list(schema["properties"]) == ["context_1", "context_2"]
    assert record.context_gap_interaction.action == "accept"
    assert len(record.context_gap_interaction.asked_gap_ids) == 2
    assert record.context_gap_interaction.asked_count == 2
    assert record.context_gap_interaction.answered_count == 2
    assert record.context_reconsideration_provenance.requested_role_ids == ["fidelity_reviewer"]
    assert record.context_reconsideration_provenance.completed_role_ids == ["fidelity_reviewer"]
    assert record.outcome_reconsideration_provenance.requested_role_ids == []
    assert record.runtime_metadata.sampling_calls == 7
    assert "CONTEXT_RECONSIDERATION" in executor.prompts[-1]


def test_context_gap_decline_and_unsupported_continue_without_fabricated_answer(tmp_path):
    reviews = [_envelope(gaps=[_gap()]), *[_envelope() for _ in range(5)]]
    declined, _, _ = _run(
        tmp_path / "decline", reviews, [ElicitationResult(action="decline")]
    )
    assert declined.context_gap_interaction.action == "decline"
    assert declined.context_reconsideration_provenance.requested_role_ids == []
    assert all(gap.answer == "" for gap in declined.context_gaps)

    unsupported, _, gateway = _run(
        tmp_path / "unsupported", reviews, [], supported=False
    )
    assert unsupported.context_gap_interaction.action == "unsupported"
    assert gateway.requests == []
    assert unsupported.context_reconsideration_provenance.requested_role_ids == []


def test_lightweight_context_reconsideration_budget_insufficiency_is_truthful(tmp_path):
    roles = ["technical_safety_reviewer", "fidelity_reviewer", "terminology_reviewer"]
    reviews = [
        _envelope(gaps=[_gap(roles=roles)]),
        *[_envelope() for _ in range(3)],
    ]
    reconsider = json.dumps({"change_effect": "unchanged", "findings": []})
    record, _, _ = _run(
        tmp_path,
        reviews,
        [ElicitationResult(action="accept", data={"context_1": "设置流程主按钮"})],
        mode="lightweight",
        extra_samples=[reconsider, reconsider],
    )
    assert record.runtime_metadata.sampling_calls == 6
    assert len(record.context_reconsideration_provenance.completed_role_ids) == 2
    assert len(record.context_reconsideration_provenance.skipped_role_ids) == 1
    assert record.degraded is True
    assert "context_reconsideration_degraded" in record.fallback_reason


def test_caller_glossary_suppresses_only_the_answered_existence_gap_in_core(tmp_path):
    gap = _gap(
        question="是否存在官方批准且具有约束力的标语词表？",
        materiality="官方词表会改变允许采用的品牌措辞",
        roles=["terminology_reviewer", "brand_voice_reviewer"],
    )
    reviews = [_envelope(gaps=[gap]), *[_envelope() for _ in range(5)]]

    def run_case(root, term_glossary):
        telemetry = RuntimeTelemetry(sample_budget=13)
        executor = ScriptedModelExecutor(reviews, telemetry)
        gateway = ScriptedUserInteractionGateway([], supported=False, telemetry=telemetry)
        record = asyncio.run(run_structured_review(
            ReviewTaskV2(
                source_text="Bigger", candidate_translation="更大", content_type="marketing",
                term_glossary=term_glossary, briefing_mode="off", mode="standard",
            ),
            executor,
            gateway,
            store=ReviewStore(root, include_legacy=False),
        ))
        return record, gateway

    supplied, supplied_gateway = run_case(tmp_path / "supplied", "官方标语词表")
    assert supplied_gateway.requests == []
    assert supplied.context_gap_interaction.action == "skipped"
    assert supplied.context_gaps[0].disposition == "suppressed"
    assert supplied.context_gaps[0].reason == "already_answered"

    missing, missing_gateway = run_case(tmp_path / "missing", "")
    assert missing_gateway.requests == []
    assert missing.context_gap_interaction.action == "unsupported"
    assert missing.context_gaps[0].disposition == "unanswered"
    assert missing.runtime_metadata.outcome_elicitation_calls == 0
    assert missing.status == "NEEDS_HUMAN_REVIEW"
