from copy import deepcopy
import json
from pathlib import Path

from council_of_translation.evaluation import evaluate_golden_cases


CORPUS = Path(__file__).parents[1] / "fixtures" / "v24_golden_corpus.json"
EXPECTED_CASE_IDS = [
    "placeholder_loss", "broken_markup", "meaning_reversal", "negation_error",
    "modality_shift", "critical_omission", "hard_tb_violation",
    "natural_but_inaccurate", "accurate_but_unnatural", "ui_context_mismatch",
    "terminology_vs_fluency", "consent_authorization_ambiguity",
    "brand_only_preference", "clean_translation", "multiple_valid_candidates",
    "user_context_changes_decision", "user_preference_conflicts_blocker",
    "no_real_conflict",
]


def _cases():
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def test_golden_corpus_has_exact_eighteen_input_cases_and_expected_only():
    cases = _cases()
    assert [case["case_id"] for case in cases] == EXPECTED_CASE_IDS
    assert len({case["category"] for case in cases}) >= 10
    assert all("observed" not in case for case in cases)
    assert all(isinstance(case["task"], dict) for case in cases)
    assert all(isinstance(case["reviewers"], dict) for case in cases)
    assert all(case["expected"]["chief_consistent"] for case in cases)
    assert any(case["expected"]["critical_issue_recalled"] for case in cases)
    assert any(not case["expected"]["conflict_detected"] for case in cases)
    assert {case["expected"]["discussion_marginal_value"] for case in cases} == {
        "not_applicable", "none", "material"
    }


def test_offline_runner_executes_actual_orchestration_and_matches_frozen_corpus():
    aggregate = evaluate_golden_cases(_cases())
    json.dumps(aggregate, ensure_ascii=False)

    assert aggregate["schema_version"] == "2.0"
    assert aggregate["total_cases"] == aggregate["passed_cases"] == 18
    assert aggregate["failed_case_ids"] == []
    for metric in (
        "critical_issue_recall", "false_positive_free_rate",
        "contribution_kind_accuracy", "conflict_detection_accuracy",
        "user_authority_accuracy", "chief_consistency_rate",
        "call_budget_accuracy", "discussion_marginal_value_accuracy",
    ):
        assert aggregate[metric] == 1.0

    runtime = aggregate["runtime_observations"]
    assert runtime["sampling_calls"] > 18
    assert len(runtime["case_results"]) == 18
    assert all(item["sampling_calls"] <= 18 for item in runtime["case_results"])


def test_context_and_preference_authority_are_observed_through_real_forms():
    aggregate = evaluate_golden_cases(_cases())
    by_id = {item["case_id"]: item for item in aggregate["runtime_observations"]["case_results"]}

    context = by_id["user_context_changes_decision"]
    boundary = by_id["user_preference_conflicts_blocker"]
    assert context["elicitation_calls"] >= 1
    assert context["observed"]["user_authority"] == "context_update_applied"
    assert boundary["elicitation_calls"] >= 1
    assert boundary["observed"]["user_authority"] == "blocked_by_policy"
    assert boundary["continuation_preference_rejected"] is True
    assert boundary["status"] != "RETURNED_PENDING"


def test_negative_mutations_rerun_production_instead_of_editing_observed_values():
    cases = _cases()

    expected_mutation = deepcopy(cases)
    expected_mutation[10]["expected"]["discussion_marginal_value"] = "none"
    result = evaluate_golden_cases(expected_mutation)
    assert result["failed_case_ids"] == ["terminology_vs_fluency"]

    input_mutation = deepcopy(cases)
    input_mutation[0]["task"]["candidate_translation"] = "删除 {count} 个文件"
    result = evaluate_golden_cases(input_mutation)
    assert "placeholder_loss" in result["failed_case_ids"]
    assert any(
        item["case_id"] == "placeholder_loss" and item["property"] == "critical_issue_recalled"
        for item in result["failures"]
    )

    envelope_mutation = deepcopy(cases)
    envelope_mutation[13]["reviewers"]["fidelity_reviewer"] = {
        "role_feedback": "invented issue",
        "findings": [{
            "issue_type": "accuracy", "severity": "major",
            "source_span": "Save", "candidate_span": "保存",
            "problem": "Invented semantic issue", "evidence": "scripted mutation",
            "action": "Change the candidate", "confidence": 0.8,
        }],
    }
    result = evaluate_golden_cases(envelope_mutation)
    assert "clean_translation" in result["failed_case_ids"]
    assert any(
        item["case_id"] == "clean_translation" and item["property"] == "false_positive_free"
        for item in result["failures"]
    )
