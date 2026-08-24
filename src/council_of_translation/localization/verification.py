"""Privacy-safe deterministic projections for review verification receipts."""

from __future__ import annotations

from collections import Counter
import re
from typing import Any

from council_of_translation import __diagnostic_build__, __schema_version__, __version__
from council_of_translation.localization.models import ReviewRecordV2
from council_of_translation.localization.roles import ROLE_REGISTRY


RECEIPT_SCHEMA_VERSION = "1.0"
MAX_VERIFICATION_REPORT = 3_200

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


class _Availability:
    def __init__(self) -> None:
        self.not_recorded: set[str] = set()
        self.redacted: set[str] = set()

    def redact(self, path: str) -> None:
        self.redacted.add(path)

    def payload(self) -> dict[str, Any]:
        return {
            "verification_complete": not self.not_recorded and not self.redacted,
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


def _safe_count(value: Any, path: str, state: _Availability) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    state.redact(path)
    return None


def _sample_projection(record: ReviewRecordV2, state: _Availability) -> list[dict[str, Any]] | None:
    active_role_ids = record.council_plan.active_role_ids
    if any(role_id not in _SAFE_ROLE_IDS for role_id in active_role_ids):
        state.redact("reviewer_execution.samples")
        return None
    by_role: dict[str, Any] = {}
    for sample in record.independent_reviews:
        if not isinstance(sample, dict):
            state.redact("reviewer_execution.samples")
            return None
        role_id = sample.get("agent_name")
        if role_id in by_role or role_id not in _SAFE_ROLE_IDS:
            state.redact("reviewer_execution.samples")
            return None
        by_role[role_id] = sample.get("sample_status")
    result: list[dict[str, Any]] = []
    for role_id in active_role_ids:
        status = by_role.get(role_id)
        if status not in _SAFE_SAMPLE_STATUSES:
            state.redact("reviewer_execution.samples")
            return None
        result.append({"role_id": role_id, "sample_status": status})
    if set(by_role) != set(active_role_ids):
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


def _coherence_projection(record: ReviewRecordV2) -> dict[str, Any]:
    expected = (
        f"- 最终处置：{record.chief_editor_decision.publishability}；"
        f"需人工复核：{record.chief_editor_decision.review_needed}"
    )
    lines = [line.strip() for line in record.display_report.splitlines() if line.strip()]
    occurrences = sum(line == expected for line in lines)
    return {
        "expected_terminal_disposition": expected,
        "terminal_disposition_occurrences": occurrences,
        "terminal_disposition_is_last_report_line": bool(lines) and lines[-1] == expected,
        "terminal_disposition_matches_structured": occurrences > 0,
    }


def _fallback_code(value: Any, state: _Availability) -> str | None:
    if value == "":
        return ""
    if isinstance(value, str) and _SAFE_FALLBACK.fullmatch(value):
        return value
    state.redact("outcome.fallback_reason_code")
    return None


def build_verification_receipt(record: ReviewRecordV2) -> dict[str, Any]:
    """Project a current full V2.5 record into the canonical receipt schema."""
    if record.schema_version != "2.5" or record.task.history_mode != "full":
        raise ValueError("current full V2.5 record required")

    state = _Availability()
    plan = record.council_plan
    runtime = record.runtime_metadata
    chief = record.chief_editor_decision
    active_roles = _safe_string_list(
        plan.active_role_ids, _SAFE_ROLE_IDS, "routing.active_role_ids", state
    )
    receipt = {
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "review_id": record.review_id,
        "record": {
            "schema_version": record.schema_version,
            "history_mode": "full",
            "parent_review_id": record.parent_review_id,
            "recorded_package_version": str(record.version_metadata.get("package_version", "")),
            "recorded_diagnostic_build": str(record.version_metadata.get("diagnostic_build", "")),
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
            "samples": _sample_projection(record, state),
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
        "coherence": _coherence_projection(record),
        "availability": {},
    }
    receipt["availability"] = state.payload()
    return receipt


def render_verification_report(receipt: dict[str, Any]) -> str:
    """Render the canonical receipt as deterministic five-section Markdown."""
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
    reason_text = "、".join(f"`{item}`" for item in reason_codes) if reason_codes else "无"
    failed_kinds = preflight["failed_blocking_check_kinds"]
    failed_text = "、".join(f"`{item}`" for item in failed_kinds) if failed_kinds else "无"
    category_counts = issues["category_counts"]
    category_text = "、".join(f"`{key}`={value}" for key, value in category_counts.items()) if category_counts else "无"

    lines = [
        "# Council 验证回执",
        "",
        "## 记录与路由",
        "",
        f"- 回执 `{receipt['receipt_schema_version']}`；记录 `{receipt['review_id']}`；记录 Schema `{record['schema_version']}`；历史 `{record['history_mode']}`。",
        f"- 记录版本 `{record['recorded_package_version']}` / `{record['recorded_diagnostic_build']}`；当前服务 `{serving['package_version']}` / `{serving['diagnostic_build']}`。",
        f"- 路由：模式 `{routing['mode']}`；内容 `{routing['content_type']}`；配置 `{routing['profile']}`；原因 {reason_text}。",
        f"- 活跃角色：{role_text}。",
        "",
        "## 覆盖与调用",
        "",
        f"- 样本：{sample_text}；覆盖 `{execution['coverage']}`，成功 {execution['successful_count']}，不可用 {execution['unavailable_count']}。",
        f"- 调用：采样 {runtime['sampling_calls_total']}/{runtime['sample_budget_total']}；引导 {runtime['elicitation_calls_total']}（简报 {runtime['briefing_elicitation_calls']}、背景缺口 {runtime['context_gap_elicitation_calls']}、结果选择 {runtime['outcome_elicitation_calls']}）。",
        f"- 时间：总计 {runtime['wall_clock_ms']} ms，采样等待 {runtime['sampling_wait_ms']} ms；并发上限/峰值/批次 {runtime['independent_review_concurrency_limit']}/{runtime['independent_review_peak_concurrency']}/{runtime['independent_review_batch_count']}，处置 `{runtime['independent_review_concurrency_disposition']}`。",
        "",
        "## 风险与裁决",
        "",
        f"- 预检：阻断 {preflight['blocking']}；失败 {preflight['failed_check_count']}，其中阻断 {preflight['failed_blocking_check_count']}；类型 {failed_text}。",
        f"- 议题：{issues['cluster_count']} 个，阻断 {issues['blocking_cluster_count']}；类别 {category_text}；严重度 {issues['severity_counts']}。",
        f"- 状态 `{outcome['status']}`；降级 {outcome['degraded']}；警告 {outcome['warning_count']}；回退 `{outcome['fallback_reason_code']}`；回退已脱敏 {outcome['fallback_reason_redacted']}。",
        f"- 主编：{outcome['publishability']}；需人工复核：{outcome['review_needed']}；含建议译文：{outcome['suggested_translation_present']}。",
        "",
        "## 一致性与可用性",
        "",
        f"- 期望终态：{coherence['expected_terminal_disposition']}；出现 {coherence['terminal_disposition_occurrences']} 次；位于末行 {coherence['terminal_disposition_is_last_report_line']}；与结构化裁决一致 {coherence['terminal_disposition_matches_structured']}。",
        f"- 验证完整：{availability['verification_complete']}；未记录字段 {len(availability['not_recorded_fields'])}；脱敏字段 {len(availability['redacted_fields'])}。",
    ]
    report = "\n".join(lines)
    if len(report) > MAX_VERIFICATION_REPORT:
        raise ValueError("verification report exceeds hard cap")
    return report
