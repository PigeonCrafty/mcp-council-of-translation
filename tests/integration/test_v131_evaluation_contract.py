from copy import deepcopy
import json
from pathlib import Path

import jsonschema
import pytest

from council_of_translation.evaluation import evaluate_golden_cases


ROOT = Path(__file__).parents[2]
CORPUS = ROOT / "tests" / "fixtures" / "v24_golden_corpus.json"
SCHEMA = ROOT / "docs" / "blind-evaluation-set.schema.json"


def _cases():
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def _blind_set():
    return {
        "set_id": "external-eval-1",
        "independent_curation": {
            "relationship_to_implementation": "independent_external",
            "curator": "External localization evaluator",
            "curated_at": "2026-08-25",
            "methodology": "Cases were selected without access to implementation outputs.",
        },
        "cases": [{
            "case_id": "case-1",
            "source": "Save changes",
            "candidate": "保存更改",
            "expected_issue_family": "clean",
            "source_anchor": "Save changes",
            "candidate_anchor": "保存更改",
            "accepted_severity_range": ["minor", "preference"],
            "allowed_alternative_interpretations": ["保存修改"],
            "forbidden_findings": ["placeholder loss"],
        }],
    }


def test_blind_set_schema_is_2020_12_and_accepts_complete_independent_provenance():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(_blind_set(), schema, format_checker=jsonschema.FormatChecker())


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value.pop("independent_curation"),
        lambda value: value["independent_curation"].update(
            {"relationship_to_implementation": "worker_authored"}
        ),
        lambda value: value["cases"][0].pop("source_anchor"),
        lambda value: value["cases"][0].update({"candidate_anchor": "x" * 241}),
        lambda value: value["cases"][0].update({"accepted_severity_range": ["unknown"]}),
        lambda value: value["cases"][0].pop("forbidden_findings"),
    ],
)
def test_blind_set_schema_rejects_missing_or_nonindependent_contract_fields(mutation):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    value = deepcopy(_blind_set())
    mutation(value)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(value, schema, format_checker=jsonschema.FormatChecker())


def test_evaluator_21_uses_truthful_property_names_and_clean_null_semantics():
    cases = _cases()
    aggregate = evaluate_golden_cases(cases)

    assert aggregate["schema_version"] == "2.1"
    assert aggregate["total_cases"] == aggregate["passed_cases"] == 30
    assert aggregate["critical_presence_contract_accuracy"] == 1.0
    assert aggregate["clean_case_no_cluster_accuracy"] == 1.0
    assert "critical_issue_recall" not in aggregate
    assert "false_positive_free_rate" not in aggregate
    by_id = {
        item["case_id"]: item["observed"]
        for item in aggregate["runtime_observations"]["case_results"]
    }
    for case in cases:
        observed = by_id[case["case_id"]]
        assert "critical_issue_recalled" not in observed
        assert "false_positive_free" not in observed
        if case["category"] == "clean":
            assert observed["clean_case_has_no_clusters"] is True
        else:
            assert observed["clean_case_has_no_clusters"] is None


def test_evaluator_rejects_nonclean_boolean_clean_case_expectation():
    cases = _cases()
    cases[0]["expected"]["clean_case_has_no_clusters"] = True
    with pytest.raises(ValueError, match="requires null"):
        evaluate_golden_cases(cases)
