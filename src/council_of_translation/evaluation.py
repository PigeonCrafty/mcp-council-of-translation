"""Offline golden-corpus comparison for Council regression evidence."""

from __future__ import annotations

from typing import Any, Iterable


_PROPERTIES = (
    "critical_issue_recalled",
    "false_positive_free",
    "contribution_kinds",
    "conflict_detected",
    "user_authority",
    "chief_consistent",
    "sampling_calls",
    "sample_budget",
    "discussion_marginal_value",
)


def _safe_case(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("golden case must be an object")
    case_id = value.get("case_id")
    expected = value.get("expected")
    observed = value.get("observed")
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("golden case requires case_id")
    if not isinstance(expected, dict) or not isinstance(observed, dict):
        raise ValueError(f"golden case {case_id} requires expected and observed objects")
    missing = [key for key in _PROPERTIES if key not in expected or key not in observed]
    if missing:
        raise ValueError(f"golden case {case_id} lacks properties: {', '.join(missing)}")
    return value


def evaluate_golden_cases(cases: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Return deterministic JSON-safe aggregate comparisons without any I/O."""
    values = [_safe_case(case) for case in cases]
    if not values:
        raise ValueError("golden corpus must not be empty")

    failures: list[dict[str, Any]] = []
    property_matches = {key: 0 for key in _PROPERTIES}
    critical_expected = 0
    critical_recalled = 0
    for case in values:
        case_id = case["case_id"]
        expected = case["expected"]
        observed = case["observed"]
        for key in _PROPERTIES:
            matches = observed[key] == expected[key]
            property_matches[key] += int(matches)
            if not matches:
                failures.append({
                    "case_id": case_id,
                    "property": key,
                    "expected": expected[key],
                    "observed": observed[key],
                })
        if expected["critical_issue_recalled"]:
            critical_expected += 1
            critical_recalled += int(bool(observed["critical_issue_recalled"]))
        if not isinstance(observed["sampling_calls"], int) or not isinstance(observed["sample_budget"], int):
            failures.append({"case_id": case_id, "property": "call_budget", "expected": "integers", "observed": "invalid"})
        elif observed["sampling_calls"] > observed["sample_budget"]:
            failures.append({
                "case_id": case_id,
                "property": "call_budget",
                "expected": f"<= {observed['sample_budget']}",
                "observed": observed["sampling_calls"],
            })

    total = len(values)
    failed_case_ids = sorted({item["case_id"] for item in failures})
    return {
        "schema_version": "1.0",
        "total_cases": total,
        "passed_cases": total - len(failed_case_ids),
        "failed_case_ids": failed_case_ids,
        "critical_issue_recall": critical_recalled / critical_expected if critical_expected else 1.0,
        "false_positive_free_rate": property_matches["false_positive_free"] / total,
        "contribution_kind_accuracy": property_matches["contribution_kinds"] / total,
        "conflict_detection_accuracy": property_matches["conflict_detected"] / total,
        "user_authority_accuracy": property_matches["user_authority"] / total,
        "chief_consistency_rate": property_matches["chief_consistent"] / total,
        "call_budget_accuracy": (
            property_matches["sampling_calls"] + property_matches["sample_budget"]
        ) / (2 * total),
        "discussion_marginal_value_accuracy": property_matches["discussion_marginal_value"] / total,
        "failures": failures,
    }
