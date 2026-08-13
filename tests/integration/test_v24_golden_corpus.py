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


def test_golden_corpus_has_exact_eighteen_audit_cases_and_machine_expectations():
    cases = _cases()
    assert [case["case_id"] for case in cases] == EXPECTED_CASE_IDS
    assert len({case["category"] for case in cases}) >= 10
    assert all(case["expected"]["chief_consistent"] for case in cases)
    assert any(case["expected"]["critical_issue_recalled"] for case in cases)
    assert any(not case["expected"]["conflict_detected"] for case in cases)
    assert {case["expected"]["discussion_marginal_value"] for case in cases} == {
        "not_applicable", "none", "low", "material"
    }


def test_offline_aggregate_is_json_safe_complete_and_perfect_for_frozen_corpus():
    aggregate = evaluate_golden_cases(_cases())
    json.dumps(aggregate, ensure_ascii=False)

    assert aggregate["total_cases"] == aggregate["passed_cases"] == 18
    assert aggregate["failed_case_ids"] == []
    for metric in (
        "critical_issue_recall", "false_positive_free_rate",
        "contribution_kind_accuracy", "conflict_detection_accuracy",
        "user_authority_accuracy", "chief_consistency_rate",
        "call_budget_accuracy", "discussion_marginal_value_accuracy",
    ):
        assert aggregate[metric] == 1.0


def test_offline_comparison_reports_regression_without_model_tool_or_network():
    cases = _cases()
    cases[10]["observed"]["discussion_marginal_value"] = "none"
    cases[16]["observed"]["sampling_calls"] = 14

    aggregate = evaluate_golden_cases(cases)

    assert aggregate["passed_cases"] == 16
    assert aggregate["failed_case_ids"] == [
        "terminology_vs_fluency", "user_preference_conflicts_blocker"
    ]
    assert any(item["property"] == "discussion_marginal_value" for item in aggregate["failures"])
    assert any(item["property"] == "call_budget" for item in aggregate["failures"])
