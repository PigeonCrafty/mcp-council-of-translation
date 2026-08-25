from copy import deepcopy
import hashlib
import json
from pathlib import Path

from council_of_translation.evaluation import evaluate_golden_cases


CORPUS = Path(__file__).parents[1] / "fixtures" / "v24_golden_corpus.json"
ORIGINAL_CASE_IDS = [
    "placeholder_loss", "broken_markup", "meaning_reversal", "negation_error",
    "modality_shift", "critical_omission", "hard_tb_violation",
    "natural_but_inaccurate", "accurate_but_unnatural", "ui_context_mismatch",
    "terminology_vs_fluency", "consent_authorization_ambiguity",
    "brand_only_preference", "clean_translation", "multiple_valid_candidates",
    "user_context_changes_decision", "user_preference_conflicts_blocker",
    "no_real_conflict",
]
RISK_CASE_IDS = [
    "legal_risk_lightweight_modality_shift",
    "legal_risk_product_state_blind_spot",
    "legal_risk_user_understanding_blind_spot",
    "legal_risk_missing_jurisdiction_context",
    "legal_risk_strict_required_literal",
    "legal_risk_clean_panorama",
]
CALIBRATION_CASE_IDS = [
    "calibration_clean_full_coverage",
    "calibration_deterministic_blocker",
    "calibration_material_model_edits",
    "calibration_unresolved_material_context",
    "calibration_partial_coverage",
    "calibration_valid_user_decision_reconsidered",
]
EXPECTED_CASE_IDS = [*ORIGINAL_CASE_IDS, *RISK_CASE_IDS, *CALIBRATION_CASE_IDS]
NON_RENAMED_CANONICAL_SHA256 = "e9d45c0c09efdc475bdf6502178a642f364183c87302c0723c56a3b7291aa992"


def _cases():
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def test_golden_corpus_has_exact_thirty_input_cases_and_preserves_prior_twenty_four():
    cases = _cases()
    assert [case["case_id"] for case in cases] == EXPECTED_CASE_IDS
    non_renamed = deepcopy(cases)
    for case in non_renamed:
        case["expected"].pop("critical_or_blocking_cluster_present")
        case["expected"].pop("clean_case_has_no_clusters")
    canonical = json.dumps(
        non_renamed, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    assert hashlib.sha256(canonical).hexdigest() == NON_RENAMED_CANONICAL_SHA256
    assert [case["case_id"] for case in cases[24:]] == CALIBRATION_CASE_IDS
    assert all(case.get("calibration_case") is True for case in cases[24:])
    assert len({case["category"] for case in cases}) >= 10
    assert all("observed" not in case for case in cases)
    assert all(isinstance(case["task"], dict) for case in cases)
    assert all(isinstance(case["reviewers"], dict) for case in cases)
    assert all(case["expected"]["chief_consistent"] for case in cases)
    assert any(case["expected"]["critical_or_blocking_cluster_present"] for case in cases)
    assert all(
        case["expected"]["clean_case_has_no_clusters"] is None
        for case in cases if case["category"] != "clean"
    )
    assert all(
        case["expected"]["clean_case_has_no_clusters"] is True
        for case in cases if case["category"] == "clean"
    )
    assert any(not case["expected"]["conflict_detected"] for case in cases)
    assert {case["expected"]["discussion_marginal_value"] for case in cases} == {
        "not_applicable", "none", "material"
    }


def test_offline_runner_executes_actual_orchestration_and_matches_frozen_corpus():
    aggregate = evaluate_golden_cases(_cases())
    json.dumps(aggregate, ensure_ascii=False)

    assert aggregate["schema_version"] == "2.1"
    assert aggregate["total_cases"] == aggregate["passed_cases"] == 30
    assert aggregate["failed_case_ids"] == []
    for metric in (
        "critical_presence_contract_accuracy", "clean_case_no_cluster_accuracy",
        "contribution_kind_accuracy", "conflict_detection_accuracy",
        "user_authority_accuracy", "chief_consistency_rate",
        "call_budget_accuracy", "discussion_marginal_value_accuracy",
    ):
        assert aggregate[metric] == 1.0
    assert "critical_issue_recall" not in aggregate
    assert "false_positive_free_rate" not in aggregate
    assert aggregate["decision_support_accuracy"] == 1.0
    assert aggregate["support_disposition_coherence"] == 1.0
    assert aggregate["insufficient_false_reassurance_rate"] == 0.0

    runtime = aggregate["runtime_observations"]
    assert runtime["sampling_calls"] == 186
    assert runtime["elicitation_calls"] == 5
    assert runtime["sample_budget"] == 374
    assert runtime["routing_calls"] == runtime["display_calls"] == 0
    assert len(runtime["case_results"]) == 30
    assert all(item["sampling_calls"] <= 18 for item in runtime["case_results"])

    by_id = {item["case_id"]: item for item in runtime["case_results"]}
    expected_routes = {
        "legal_risk_lightweight_modality_shift": ("route_legal_risk_lightweight_v1", 4),
        "legal_risk_product_state_blind_spot": ("route_legal_risk_standard_v1", 6),
        "legal_risk_user_understanding_blind_spot": ("route_legal_risk_standard_v1", 6),
        "legal_risk_missing_jurisdiction_context": ("route_legal_risk_standard_v1", 6),
        "legal_risk_strict_required_literal": ("route_legal_risk_strict_v1", 7),
        "legal_risk_clean_panorama": ("route_legal_risk_standard_v1", 6),
    }
    for case_id, (profile, role_count) in expected_routes.items():
        assert by_id[case_id]["routing_profile"] == profile
        assert len(by_id[case_id]["active_role_ids"]) == role_count
        assert by_id[case_id]["routing_reason_codes"][0] == "content_legal_risk"


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
        item["case_id"] == "placeholder_loss" and item["property"] == "critical_or_blocking_cluster_present"
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
        item["case_id"] == "clean_translation" and item["property"] == "clean_case_has_no_clusters"
        for item in result["failures"]
    )

    support_mutation = deepcopy(cases)
    support_mutation[26]["expected"]["decision_support_level"] = "well_supported"
    result = evaluate_golden_cases(support_mutation)
    assert result["failed_case_ids"] == ["calibration_material_model_edits"]
    assert any(
        item["case_id"] == "calibration_material_model_edits"
        and item["property"] == "decision_support_level"
        for item in result["failures"]
    )

    permissive_insufficient_mutation = deepcopy(cases)
    permissive_insufficient_mutation[28]["expected"]["publishability"] = "可发布"
    result = evaluate_golden_cases(permissive_insufficient_mutation)
    assert result["failed_case_ids"] == ["calibration_partial_coverage"]
    assert any(
        item["case_id"] == "calibration_partial_coverage"
        and item["property"] == "publishability"
        and item["observed"] == "需人工复核"
        for item in result["failures"]
    )
