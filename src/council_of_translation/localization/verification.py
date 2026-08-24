"""Privacy-safe deterministic projections for review verification receipts."""

from __future__ import annotations

from collections import Counter
import json
import re
from typing import Any

from council_of_translation import __diagnostic_build__, __schema_version__, __version__
from council_of_translation.localization.compatibility import ReviewRecordV1
from council_of_translation.localization.models import ReviewRecordV2
from council_of_translation.localization.roles import ROLE_REGISTRY


RECEIPT_SCHEMA_VERSION = "1.0"
MAX_VERIFICATION_REPORT = 3_200
MAX_VERIFICATION_TEXT = 12_000
CANONICAL_RECEIPT_LABEL = "Canonical verification_receipt JSON:"
_CANONICAL_RECEIPT_KEYS = (
    "receipt_schema_version",
    "review_id",
    "record",
    "serving",
    "routing",
    "reviewer_execution",
    "runtime",
    "preflight",
    "issues",
    "outcome",
    "coherence",
    "availability",
)
_MAX_SAFE_RECEIPT_INTEGER = 9_007_199_254_740_991

_SAFE_ROLE_IDS = {
    role_id for role_id, role in ROLE_REGISTRY.items() if role.role_type == "reviewer"
}
_SAFE_MODES = {"lightweight", "standard", "strict"}
_SAFE_CONTENT_TYPES = {
    "unspecified", "ui", "marketing", "technical_documentation", "legal_risk"
}
_SAFE_ROUTING_PROFILES = {
    "legacy_unrecorded",
    *(f"route_{content}_{mode}_v1" for content in (
        "unspecified", "ui", "marketing", "technical_documentation", "legal_risk"
    ) for mode in ("lightweight", "standard", "strict")),
}
_SAFE_ROUTING_REASON_CODES = {
    "legacy_routing_unrecorded", "content_unspecified", "content_ui",
    "content_marketing", "content_technical_documentation", "content_legal_risk",
    "mode_lightweight", "mode_standard", "mode_strict", "legacy_portfolio_preserved",
    "risk_focused", "risk_panorama", "risk_strict", "deterministic_preflight_coverage",
}
_SAFE_SAMPLE_STATUSES = {"structured_success", "unavailable"}
_SAFE_COVERAGE = {"full", "partial", "none", "not_applicable"}
_SAFE_CONCURRENCY_DISPOSITIONS = {"legacy", "default", "configured", "invalid_fallback"}
_SAFE_RECORD_STATUSES = {
    "COMPLETED", "COMPLETED_WITH_FALLBACK", "NEEDS_HUMAN_REVIEW", "RETURNED_PENDING"
}
_SAFE_LEGACY_STATUSES = {"completed", "pending", "failed", "error"}
_SAFE_PREFLIGHT_KINDS = {
    "placeholder_parity", "printf_placeholder_parity", "variable_token_parity",
    "command_token_parity", "tag_integrity", "url_preservation",
    "do_not_translate_preservation", "explicit_hard_constraint", "numeric_signal",
    "markdown_signal",
}
_SAFE_SEVERITIES = ("critical", "major", "minor", "preference")
_SAFE_CATEGORIES = {"integrity", "correctness", "language_choice", "signal"}
_SAFE_PUBLISHABILITY = {"可发布", "修改后可发布", "需人工复核"}
_SAFE_REVIEW_NEEDED = {"是", "否"}
_SAFE_FALLBACK = re.compile(r"^[a-z0-9][a-z0-9_:-]{0,79}$")
_SAFE_PACKAGE_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[a-z0-9.+-]{0,40})?$")
_SAFE_BUILD = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,79}$")
_SAFE_CURRENT_REVIEW_ID = re.compile(r"^[0-9]{8}T[0-9]{12}Z_[0-9a-f]{8,32}$")
_SAFE_LEGACY_REVIEW_ID = re.compile(r"^[0-9]{8}_[0-9]{6}$")


def is_canonical_verification_receipt(value: Any) -> bool:
    """Recognize the frozen receipt envelope without coercing or deriving it."""
    return (
        isinstance(value, dict)
        and value.get("receipt_schema_version") == RECEIPT_SCHEMA_VERSION
        and tuple(value) == _CANONICAL_RECEIPT_KEYS
    )


def append_canonical_receipt_json(primary_text: str, receipt: dict[str, Any]) -> str:
    """Append one compact serialization of the exact canonical receipt object."""
    try:
        canonical_json = json.dumps(
            receipt,
            ensure_ascii=False,
            separators=(",", ":"),
        )
    except (TypeError, ValueError):
        raise ValueError("verification receipt JSON serialization failed") from None
    combined = (
        f"{primary_text}\n\n{CANONICAL_RECEIPT_LABEL}\n"
        f"```json\n{canonical_json}\n```"
    )
    if len(combined) > MAX_VERIFICATION_TEXT:
        raise ValueError("verification text exceeds hard cap")
    return combined


class _Availability:
    def __init__(self) -> None:
        self.not_recorded: set[str] = set()
        self.redacted: set[str] = set()
        self.required_missing = False

    def missing(self, path: str, *, required: bool = True) -> None:
        self.not_recorded.add(path)
        self.required_missing = self.required_missing or required

    def redact(self, path: str) -> None:
        self.redacted.add(path)

    def payload(self) -> dict[str, Any]:
        return {
            "verification_complete": not self.required_missing and not self.redacted,
            "not_recorded_fields": sorted(self.not_recorded),
            "redacted_fields": sorted(self.redacted),
        }


def _safe_scalar(value: Any, allowed: set[str], path: str, state: _Availability) -> str | None:
    if isinstance(value, str) and value in allowed:
        return value
    state.redact(path)
    return None


def _safe_string_list(
    values: Any,
    allowed: set[str],
    path: str,
    state: _Availability,
) -> list[str] | None:
    if not isinstance(values, list) or any(not isinstance(item, str) or item not in allowed for item in values):
        state.redact(path)
        return None
    return list(dict.fromkeys(values))


def _safe_parent_review_id(value: Any, state: _Availability) -> str | None:
    if value is None:
        return None
    if isinstance(value, str) and (
        _SAFE_CURRENT_REVIEW_ID.fullmatch(value)
        or _SAFE_LEGACY_REVIEW_ID.fullmatch(value)
    ):
        return value
    state.redact("record.parent_review_id")
    return None


def _safe_active_role_ids(values: Any, state: _Availability) -> list[str] | None:
    if (
        not isinstance(values, list)
        or len(values) > len(_SAFE_ROLE_IDS)
        or any(not isinstance(item, str) or item not in _SAFE_ROLE_IDS for item in values)
        or len(values) != len(set(values))
    ):
        state.redact("routing.active_role_ids")
        return None
    return list(values)


def _safe_count(value: Any, path: str, state: _Availability) -> int | None:
    if (
        isinstance(value, int)
        and not isinstance(value, bool)
        and 0 <= value <= _MAX_SAFE_RECEIPT_INTEGER
    ):
        return value
    state.redact(path)
    return None


def _sample_projection(
    record: ReviewRecordV2,
    active_role_ids: list[str] | None,
    state: _Availability,
) -> list[dict[str, Any]] | None:
    samples = record.independent_reviews
    if (
        active_role_ids is None
        or not isinstance(samples, list)
        or len(samples) != len(active_role_ids)
    ):
        state.redact("reviewer_execution.samples")
        return None
    result: list[dict[str, Any]] = []
    for sample in samples:
        if not isinstance(sample, dict):
            state.redact("reviewer_execution.samples")
            return None
        role_id = sample.get("agent_name")
        status = sample.get("sample_status")
        if role_id not in _SAFE_ROLE_IDS or status not in _SAFE_SAMPLE_STATUSES:
            state.redact("reviewer_execution.samples")
            return None
        result.append({"role_id": role_id, "sample_status": status})
    if [item["role_id"] for item in result] != active_role_ids:
        state.redact("reviewer_execution.samples")
        return None
    return result


def _preflight_projection(record: ReviewRecordV2, state: _Availability) -> dict[str, Any]:
    failed = [check for check in record.preflight.checks if check.status == "fail"]
    blocking = [check for check in failed if check.blocking]
    kinds = sorted({check.kind for check in blocking})
    if any(kind not in _SAFE_PREFLIGHT_KINDS for kind in kinds):
        state.redact("preflight.failed_blocking_check_kinds")
        safe_kinds: list[str] | None = None
    else:
        safe_kinds = kinds
    return {
        "blocking": bool(record.preflight.blocking),
        "failed_check_count": len(failed),
        "failed_blocking_check_count": len(blocking),
        "failed_blocking_check_kinds": safe_kinds,
    }


def _issue_projection(record: ReviewRecordV2) -> dict[str, Any]:
    severity_counts = Counter(cluster.severity for cluster in record.issue_clusters)
    category_counts = Counter(
        cluster.category if cluster.category in _SAFE_CATEGORIES else "other"
        for cluster in record.issue_clusters
    )
    return {
        "cluster_count": len(record.issue_clusters),
        "blocking_cluster_count": sum(bool(cluster.blocking) for cluster in record.issue_clusters),
        "severity_counts": {name: severity_counts.get(name, 0) for name in _SAFE_SEVERITIES},
        "category_counts": dict(sorted(category_counts.items())),
    }


def _coherence_projection(record: ReviewRecordV2, state: _Availability) -> dict[str, Any]:
    if (
        record.chief_editor_decision.publishability not in _SAFE_PUBLISHABILITY
        or record.chief_editor_decision.review_needed not in _SAFE_REVIEW_NEEDED
    ):
        for path in (
            "coherence.expected_terminal_disposition",
            "coherence.terminal_disposition_occurrences",
            "coherence.terminal_disposition_is_last_report_line",
            "coherence.terminal_disposition_matches_structured",
        ):
            state.redact(path)
        return {
            "expected_terminal_disposition": None,
            "terminal_disposition_occurrences": None,
            "terminal_disposition_is_last_report_line": None,
            "terminal_disposition_matches_structured": None,
        }
    expected = (
        f"- 最终处置：{record.chief_editor_decision.publishability}；"
        f"需人工复核：{record.chief_editor_decision.review_needed}"
    )
    lines = [line.strip() for line in record.display_report.splitlines() if line.strip()]
    occurrences = sum(line == expected for line in lines)
    is_last = bool(lines) and lines[-1] == expected
    return {
        "expected_terminal_disposition": expected,
        "terminal_disposition_occurrences": occurrences,
        "terminal_disposition_is_last_report_line": is_last,
        "terminal_disposition_matches_structured": occurrences == 1 and is_last,
    }


def _fallback_code(value: Any, state: _Availability) -> str | None:
    if value == "":
        return ""
    if isinstance(value, str) and _SAFE_FALLBACK.fullmatch(value):
        return value
    state.redact("outcome.fallback_reason_code")
    return None


def _recorded_identifier(
    value: Any,
    pattern: re.Pattern[str],
    path: str,
    state: _Availability,
) -> str | None:
    if isinstance(value, str) and pattern.fullmatch(value):
        return value
    state.redact(path)
    return None


def _v2_projection(record: ReviewRecordV2) -> tuple[dict[str, Any], _Availability]:
    state = _Availability()
    plan = record.council_plan
    runtime = record.runtime_metadata
    chief = record.chief_editor_decision
    active_roles = _safe_active_role_ids(plan.active_role_ids, state)
    receipt = {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "review_id": record.review_id,
        "record": {
            "schema_version": record.schema_version,
            "history_mode": "metadata" if record.task.history_mode == "metadata" else "full",
            "parent_review_id": _safe_parent_review_id(record.parent_review_id, state),
            "recorded_package_version": _recorded_identifier(
                record.version_metadata.get("package_version"),
                _SAFE_PACKAGE_VERSION,
                "record.recorded_package_version",
                state,
            ),
            "recorded_diagnostic_build": _recorded_identifier(
                record.version_metadata.get("diagnostic_build"),
                _SAFE_BUILD,
                "record.recorded_diagnostic_build",
                state,
            ),
        },
        "serving": {
            "package_version": __version__,
            "module_version": __version__,
            "diagnostic_build": __diagnostic_build__,
            "schema_version": __schema_version__,
        },
        "routing": {
            "mode": _safe_scalar(plan.mode, _SAFE_MODES, "routing.mode", state),
            "content_type": _safe_scalar(
                plan.content_type, _SAFE_CONTENT_TYPES, "routing.content_type", state
            ),
            "profile": _safe_scalar(
                plan.routing_profile, _SAFE_ROUTING_PROFILES, "routing.profile", state
            ),
            "reason_codes": _safe_string_list(
                plan.routing_reason_codes,
                _SAFE_ROUTING_REASON_CODES,
                "routing.reason_codes",
                state,
            ),
            "active_role_ids": active_roles,
        },
        "reviewer_execution": {
            "samples": _sample_projection(record, active_roles, state),
            "coverage": _safe_scalar(
                runtime.reviewer_coverage, _SAFE_COVERAGE, "reviewer_execution.coverage", state
            ),
            "successful_count": _safe_count(
                runtime.reviewer_samples_successful,
                "reviewer_execution.successful_count",
                state,
            ),
            "unavailable_count": _safe_count(
                runtime.reviewer_samples_unavailable,
                "reviewer_execution.unavailable_count",
                state,
            ),
        },
        "runtime": {
            "sampling_calls_total": _safe_count(runtime.sampling_calls, "runtime.sampling_calls_total", state),
            "sample_budget_total": _safe_count(runtime.sample_budget, "runtime.sample_budget_total", state),
            "elicitation_calls_total": _safe_count(runtime.elicitation_calls, "runtime.elicitation_calls_total", state),
            "briefing_elicitation_calls": _safe_count(runtime.briefing_elicitation_calls, "runtime.briefing_elicitation_calls", state),
            "context_gap_elicitation_calls": _safe_count(runtime.context_gap_elicitation_calls, "runtime.context_gap_elicitation_calls", state),
            "outcome_elicitation_calls": _safe_count(runtime.outcome_elicitation_calls, "runtime.outcome_elicitation_calls", state),
            "wall_clock_ms": _safe_count(runtime.wall_clock_ms, "runtime.wall_clock_ms", state),
            "sampling_wait_ms": _safe_count(runtime.sampling_wait_ms, "runtime.sampling_wait_ms", state),
            "independent_review_concurrency_limit": _safe_count(runtime.independent_review_concurrency_limit, "runtime.independent_review_concurrency_limit", state),
            "independent_review_peak_concurrency": _safe_count(runtime.independent_review_peak_concurrency, "runtime.independent_review_peak_concurrency", state),
            "independent_review_batch_count": _safe_count(runtime.independent_review_batch_count, "runtime.independent_review_batch_count", state),
            "independent_review_concurrency_disposition": _safe_scalar(
                runtime.independent_review_concurrency_disposition,
                _SAFE_CONCURRENCY_DISPOSITIONS,
                "runtime.independent_review_concurrency_disposition",
                state,
            ),
        },
        "preflight": _preflight_projection(record, state),
        "issues": _issue_projection(record),
        "outcome": {
            "status": _safe_scalar(record.status, _SAFE_RECORD_STATUSES, "outcome.status", state),
            "degraded": bool(record.degraded),
            "warning_count": len(record.warnings),
            "fallback_reason_code": _fallback_code(record.fallback_reason, state),
            "fallback_reason_redacted": "outcome.fallback_reason_code" in state.redacted,
            "publishability": _safe_scalar(chief.publishability, _SAFE_PUBLISHABILITY, "outcome.publishability", state),
            "review_needed": _safe_scalar(chief.review_needed, _SAFE_REVIEW_NEEDED, "outcome.review_needed", state),
            "suggested_translation_present": chief.suggested_translation is not None,
        },
        "coherence": _coherence_projection(record, state),
        "availability": {},
    }
    return receipt, state


def _set_path(receipt: dict[str, Any], path: str, value: Any) -> None:
    section, field = path.split(".", 1)
    receipt[section][field] = value


def _mark_missing(
    receipt: dict[str, Any],
    state: _Availability,
    path: str,
    *,
    required: bool = True,
) -> None:
    _set_path(receipt, path, None)
    state.redacted.discard(path)
    state.missing(path, required=required)


def _physically_set(model: Any, field: str) -> bool:
    return field in getattr(model, "model_fields_set", set())


def _apply_v2_availability(
    record: ReviewRecordV2,
    receipt: dict[str, Any],
    state: _Availability,
) -> None:
    schema = record.schema_version
    metadata = record.task.history_mode == "metadata"
    receipt["record"]["history_mode"] = "metadata" if metadata else "full"

    if not _physically_set(record, "parent_review_id"):
        _mark_missing(receipt, state, "record.parent_review_id")
    version_recorded = _physically_set(record, "version_metadata")
    for field, key in (
        ("recorded_package_version", "package_version"),
        ("recorded_diagnostic_build", "diagnostic_build"),
    ):
        if not version_recorded or key not in record.version_metadata:
            _mark_missing(receipt, state, f"record.{field}")

    plan_recorded = _physically_set(record, "council_plan")
    plan = record.council_plan
    for field, model_field in (("mode", "mode"), ("content_type", "content_type")):
        if not plan_recorded or not _physically_set(plan, model_field):
            _mark_missing(receipt, state, f"routing.{field}")
    if schema != "2.5":
        _mark_missing(receipt, state, "routing.profile", required=False)
        _mark_missing(receipt, state, "routing.reason_codes", required=False)
    else:
        for field, model_field in (("profile", "routing_profile"), ("reason_codes", "routing_reason_codes")):
            if not plan_recorded or not _physically_set(plan, model_field):
                _mark_missing(receipt, state, f"routing.{field}")
    if metadata or not plan_recorded or not _physically_set(plan, "active_role_ids"):
        _mark_missing(receipt, state, "routing.active_role_ids", required=metadata or schema == "2.5")

    if metadata or not _physically_set(record, "independent_reviews"):
        _mark_missing(receipt, state, "reviewer_execution.samples", required=metadata)
    runtime_recorded = _physically_set(record, "runtime_metadata")
    runtime = record.runtime_metadata
    runtime_fields = (
        ("reviewer_execution.coverage", "reviewer_coverage", "2.0"),
        ("reviewer_execution.successful_count", "reviewer_samples_successful", "2.0"),
        ("reviewer_execution.unavailable_count", "reviewer_samples_unavailable", "2.0"),
        ("runtime.sampling_calls_total", "sampling_calls", "2.0"),
        ("runtime.sample_budget_total", "sample_budget", "2.0"),
        ("runtime.elicitation_calls_total", "elicitation_calls", "2.0"),
        ("runtime.briefing_elicitation_calls", "briefing_elicitation_calls", "2.2"),
        ("runtime.context_gap_elicitation_calls", "context_gap_elicitation_calls", "2.2"),
        ("runtime.outcome_elicitation_calls", "outcome_elicitation_calls", "2.2"),
        ("runtime.wall_clock_ms", "wall_clock_ms", "2.3"),
        ("runtime.sampling_wait_ms", "sampling_wait_ms", "2.3"),
        ("runtime.independent_review_concurrency_limit", "independent_review_concurrency_limit", "2.3"),
        ("runtime.independent_review_peak_concurrency", "independent_review_peak_concurrency", "2.3"),
        ("runtime.independent_review_batch_count", "independent_review_batch_count", "2.3"),
        ("runtime.independent_review_concurrency_disposition", "independent_review_concurrency_disposition", "2.3"),
    )
    for path, model_field, introduced in runtime_fields:
        schema_supports = tuple(map(int, schema.split("."))) >= tuple(map(int, introduced.split(".")))
        if not schema_supports:
            _mark_missing(receipt, state, path, required=False)
        elif not runtime_recorded or not _physically_set(runtime, model_field):
            _mark_missing(receipt, state, path)

    preflight_paths = (
        "preflight.blocking", "preflight.failed_check_count",
        "preflight.failed_blocking_check_count", "preflight.failed_blocking_check_kinds",
    )
    issue_paths = (
        "issues.cluster_count", "issues.blocking_cluster_count",
        "issues.severity_counts", "issues.category_counts",
    )
    if metadata or not _physically_set(record, "preflight"):
        for path in preflight_paths:
            _mark_missing(receipt, state, path, required=metadata)
    if metadata or not _physically_set(record, "issue_clusters"):
        for path in issue_paths:
            _mark_missing(receipt, state, path, required=metadata)

    if not _physically_set(record, "status"):
        _mark_missing(receipt, state, "outcome.status")
    if schema == "2.0":
        _mark_missing(receipt, state, "outcome.degraded", required=False)
        _mark_missing(receipt, state, "outcome.warning_count", required=False)
    else:
        if not _physically_set(record, "degraded"):
            _mark_missing(receipt, state, "outcome.degraded")
        if metadata or not _physically_set(record, "warnings"):
            _mark_missing(receipt, state, "outcome.warning_count", required=metadata)
    if metadata or not _physically_set(record, "fallback_reason"):
        _mark_missing(receipt, state, "outcome.fallback_reason_code", required=metadata)
        _mark_missing(receipt, state, "outcome.fallback_reason_redacted", required=metadata)
    chief_recorded = _physically_set(record, "chief_editor_decision")
    chief = record.chief_editor_decision
    for field in ("publishability", "review_needed"):
        if not chief_recorded or not _physically_set(chief, field):
            _mark_missing(receipt, state, f"outcome.{field}")
    if metadata or not chief_recorded or not _physically_set(chief, "suggested_translation"):
        _mark_missing(receipt, state, "outcome.suggested_translation_present", required=metadata)

    coherence_paths = (
        "coherence.expected_terminal_disposition",
        "coherence.terminal_disposition_occurrences",
        "coherence.terminal_disposition_is_last_report_line",
        "coherence.terminal_disposition_matches_structured",
    )
    display_supported = tuple(map(int, schema.split("."))) >= (2, 2)
    if metadata or not display_supported or not _physically_set(record, "display_report"):
        for path in coherence_paths:
            _mark_missing(receipt, state, path, required=metadata or display_supported)


def _legacy_receipt(record: ReviewRecordV1) -> dict[str, Any]:
    state = _Availability()
    receipt: dict[str, Any] = {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "review_id": record.review_id,
        "record": {
            "schema_version": "1.0", "history_mode": "legacy", "parent_review_id": None,
            "recorded_package_version": None, "recorded_diagnostic_build": None,
        },
        "serving": {
            "package_version": __version__, "module_version": __version__,
            "diagnostic_build": __diagnostic_build__, "schema_version": __schema_version__,
        },
        "routing": {"mode": None, "content_type": None, "profile": None, "reason_codes": None, "active_role_ids": None},
        "reviewer_execution": {"samples": None, "coverage": None, "successful_count": None, "unavailable_count": None},
        "runtime": {
            "sampling_calls_total": None, "sample_budget_total": None,
            "elicitation_calls_total": None, "briefing_elicitation_calls": None,
            "context_gap_elicitation_calls": None, "outcome_elicitation_calls": None,
            "wall_clock_ms": None, "sampling_wait_ms": None,
            "independent_review_concurrency_limit": None,
            "independent_review_peak_concurrency": None,
            "independent_review_batch_count": None,
            "independent_review_concurrency_disposition": None,
        },
        "preflight": {"blocking": None, "failed_check_count": None, "failed_blocking_check_count": None, "failed_blocking_check_kinds": None},
        "issues": {"cluster_count": None, "blocking_cluster_count": None, "severity_counts": None, "category_counts": None},
        "outcome": {
            "status": None, "degraded": None, "warning_count": None,
            "fallback_reason_code": None, "fallback_reason_redacted": None,
            "publishability": None, "review_needed": None,
            "suggested_translation_present": None,
        },
        "coherence": {
            "expected_terminal_disposition": None,
            "terminal_disposition_occurrences": None,
            "terminal_disposition_is_last_report_line": None,
            "terminal_disposition_matches_structured": None,
        },
        "availability": {},
    }
    for section in ("record", "routing", "reviewer_execution", "runtime", "preflight", "issues", "outcome", "coherence"):
        for field in receipt[section]:
            path = f"{section}.{field}"
            if path not in {"record.schema_version", "record.history_mode"}:
                state.missing(path, required=False)
    if _physically_set(record, "mode"):
        receipt["routing"]["mode"] = _safe_scalar(
            record.mode, _SAFE_MODES, "routing.mode", state
        )
        state.not_recorded.discard("routing.mode")
    if _physically_set(record, "status"):
        receipt["outcome"]["status"] = _safe_scalar(
            record.status, _SAFE_RECORD_STATUSES | _SAFE_LEGACY_STATUSES, "outcome.status", state
        )
        state.not_recorded.discard("outcome.status")
    if _physically_set(record, "chief_editor_decision") and isinstance(record.chief_editor_decision, dict):
        for field, allowed in (("publishability", _SAFE_PUBLISHABILITY), ("review_needed", _SAFE_REVIEW_NEEDED)):
            if field in record.chief_editor_decision:
                receipt["outcome"][field] = _safe_scalar(
                    record.chief_editor_decision[field], allowed, f"outcome.{field}", state
                )
                state.not_recorded.discard(f"outcome.{field}")
    for required_path in ("routing.mode", "outcome.status", "outcome.publishability", "outcome.review_needed"):
        if required_path in state.not_recorded:
            state.required_missing = True
    receipt["availability"] = state.payload()
    return receipt


def build_verification_receipt(record: ReviewRecordV1 | ReviewRecordV2) -> dict[str, Any]:
    """Project a parsed record without treating compatibility defaults as facts."""
    if isinstance(record, ReviewRecordV1):
        return _legacy_receipt(record)
    receipt, state = _v2_projection(record)
    _apply_v2_availability(record, receipt, state)
    receipt["availability"] = state.payload()
    return receipt


def render_verification_report(receipt: dict[str, Any]) -> str:
    """Render the canonical receipt as deterministic five-section Markdown."""
    def shown(value: Any) -> str:
        return "未记录" if value is None else str(value)

    def code(value: Any) -> str:
        return "未记录" if value is None else f"`{value}`"

    record = receipt["record"]
    serving = receipt["serving"]
    routing = receipt["routing"]
    execution = receipt["reviewer_execution"]
    runtime = receipt["runtime"]
    preflight = receipt["preflight"]
    issues = receipt["issues"]
    outcome = receipt["outcome"]
    coherence = receipt["coherence"]
    availability = receipt["availability"]

    roles = routing["active_role_ids"]
    samples = execution["samples"]
    role_text = "、".join(f"`{item}`" for item in roles) if roles is not None else "未记录"
    if samples is None:
        sample_text = "未记录"
    else:
        sample_text = "、".join(
            f"`{item['role_id']}`=`{item['sample_status']}`" for item in samples
        ) or "不适用"
    reason_codes = routing["reason_codes"]
    reason_text = (
        "未记录" if reason_codes is None
        else "、".join(f"`{item}`" for item in reason_codes) or "无"
    )
    failed_kinds = preflight["failed_blocking_check_kinds"]
    failed_text = (
        "未记录" if failed_kinds is None
        else "、".join(f"`{item}`" for item in failed_kinds) or "无"
    )
    category_counts = issues["category_counts"]
    category_text = (
        "未记录" if category_counts is None
        else "、".join(f"`{key}`={value}" for key, value in category_counts.items()) or "无"
    )
    severity_counts = issues["severity_counts"]
    severity_text = (
        "未记录" if severity_counts is None
        else "、".join(f"`{key}`={value}" for key, value in severity_counts.items())
    )

    lines = [
        "# Council 验证回执",
        "",
        "## 记录与路由",
        "",
        f"- 回执 `{receipt['receipt_schema_version']}`；记录 `{receipt['review_id']}`；记录 Schema `{record['schema_version']}`；历史 `{record['history_mode']}`。",
        f"- 记录版本 {code(record['recorded_package_version'])} / {code(record['recorded_diagnostic_build'])}；当前服务：包 {code(serving['package_version'])}；模块 {code(serving['module_version'])}；构建 {code(serving['diagnostic_build'])}；Schema {code(serving['schema_version'])}。",
        f"- 路由：模式 {code(routing['mode'])}；内容 {code(routing['content_type'])}；配置 {code(routing['profile'])}；原因 {reason_text}。",
        f"- 活跃角色：{role_text}。",
        "",
        "## 覆盖与调用",
        "",
        f"- 样本：{sample_text}；覆盖 {code(execution['coverage'])}，成功 {shown(execution['successful_count'])}，不可用 {shown(execution['unavailable_count'])}。",
        f"- 调用：采样 {shown(runtime['sampling_calls_total'])}/{shown(runtime['sample_budget_total'])}；引导 {shown(runtime['elicitation_calls_total'])}（简报 {shown(runtime['briefing_elicitation_calls'])}、背景缺口 {shown(runtime['context_gap_elicitation_calls'])}、结果选择 {shown(runtime['outcome_elicitation_calls'])}）。",
        f"- 时间：总计 {shown(runtime['wall_clock_ms'])} ms，采样等待 {shown(runtime['sampling_wait_ms'])} ms；并发上限/峰值/批次 {shown(runtime['independent_review_concurrency_limit'])}/{shown(runtime['independent_review_peak_concurrency'])}/{shown(runtime['independent_review_batch_count'])}，处置 {code(runtime['independent_review_concurrency_disposition'])}。",
        "",
        "## 风险与裁决",
        "",
        f"- 预检：阻断 {shown(preflight['blocking'])}；失败 {shown(preflight['failed_check_count'])}，其中阻断 {shown(preflight['failed_blocking_check_count'])}；类型 {failed_text}。",
        f"- 议题：{shown(issues['cluster_count'])} 个，阻断 {shown(issues['blocking_cluster_count'])}；类别 {category_text}；严重度 {severity_text}。",
        f"- 状态 {code(outcome['status'])}；降级 {shown(outcome['degraded'])}；警告 {shown(outcome['warning_count'])}；回退 {code(outcome['fallback_reason_code'])}；回退已脱敏 {shown(outcome['fallback_reason_redacted'])}。",
        f"- 主编：{shown(outcome['publishability'])}；需人工复核：{shown(outcome['review_needed'])}；含建议译文：{shown(outcome['suggested_translation_present'])}。",
        "",
        "## 一致性与可用性",
        "",
        f"- 期望终态：{shown(coherence['expected_terminal_disposition'])}；出现 {shown(coherence['terminal_disposition_occurrences'])} 次；位于末行 {shown(coherence['terminal_disposition_is_last_report_line'])}；与结构化裁决一致 {shown(coherence['terminal_disposition_matches_structured'])}。",
        f"- 验证完整：{availability['verification_complete']}；未记录字段 {len(availability['not_recorded_fields'])}；脱敏字段 {len(availability['redacted_fields'])}。",
    ]
    report = "\n".join(lines)
    if len(report) > MAX_VERIFICATION_REPORT:
        raise ValueError("verification report exceeds hard cap")
    return report
