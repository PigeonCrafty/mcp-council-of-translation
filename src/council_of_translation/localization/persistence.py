"""Durable, privacy-aware storage for localization review records."""

from __future__ import annotations

import json
import os
import re
import secrets
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from pydantic import ValidationError

from council_of_translation.localization.compatibility import (
    ReviewRecordV1,
    parse_review_record,
)
from council_of_translation.localization.models import HistoryMode, ReviewRecordV2


_NEW_REVIEW_ID = re.compile(r"^[0-9]{8}T[0-9]{12}Z_[0-9a-f]{8,32}$")
_LEGACY_REVIEW_ID = re.compile(r"^[0-9]{8}_[0-9]{6}$")
_SAFE_ROLE_IDS = {
    "technical_safety_reviewer",
    "fidelity_reviewer",
    "terminology_reviewer",
    "product_context_reviewer",
    "ux_copy_reviewer",
    "brand_voice_reviewer",
    "risk_ambiguity_reviewer",
    "fluency_reviewer",
}
_SAFE_BRIEF_FIELDS = {
    "domain", "content_type", "audience", "tone_goal", "primary_focus", "usage_context"
}
_SAFE_CONTENT_TYPES = {"unspecified", "ui", "marketing", "technical_documentation", "legal_risk"}
_SAFE_PHASE_DISPOSITIONS = {
    "completed", "skipped", "degraded", "blocked", "accept", "decline", "cancel",
    "unsupported", "malformed", "error", "pending", "可发布", "修改后可发布", "需人工复核",
}
_CURRENT_PACKAGE_VERSION = "0.8.0"
_CURRENT_DIAGNOSTIC_BUILD = "context-coherent-council-v6"


class ReviewPersistenceError(RuntimeError):
    """Base error for durable review history operations."""


class InvalidReviewIdError(ReviewPersistenceError):
    """Raised when an ID is neither a V2 nor a supported legacy ID."""


class ReviewRecordNotFoundError(ReviewPersistenceError):
    """Raised when no record exists in new or enabled legacy storage."""


class MalformedReviewRecordError(ReviewPersistenceError):
    """Raised when a stored file is not a valid V1 or V2 review record."""


def build_review_id(
    *,
    now: datetime | None = None,
    suffix_factory: Callable[[], str] | None = None,
) -> str:
    """Return a collision-resistant ID whose timestamp prefix sorts lexically."""
    instant = now or datetime.now(timezone.utc)
    if instant.tzinfo is None:
        instant = instant.replace(tzinfo=timezone.utc)
    instant = instant.astimezone(timezone.utc)
    suffix = (suffix_factory or (lambda: secrets.token_hex(6)))()
    if not re.fullmatch(r"[0-9a-f]{12}", suffix):
        raise ValueError("review ID suffix must contain exactly 12 lowercase hex characters")
    return f"{instant.strftime('%Y%m%dT%H%M%S%f')}Z_{suffix}"


def is_supported_review_id(review_id: str) -> bool:
    return bool(_NEW_REVIEW_ID.fullmatch(review_id) or _LEGACY_REVIEW_ID.fullmatch(review_id))


def default_reviews_dir() -> Path:
    """Resolve stable per-user storage, honoring COUNCIL_REVIEWS_DIR."""
    configured = os.environ.get("COUNCIL_REVIEWS_DIR")
    if configured:
        return Path(configured).expanduser()
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return root / "Council-of-Translation" / "reviews"
    if os.uname().sysname == "Darwin":  # pragma: no cover - platform specific
        return Path.home() / "Library" / "Application Support" / "Council-of-Translation" / "reviews"
    root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return root / "council-of-translation" / "reviews"


def _metadata_projection(record: ReviewRecordV2) -> dict[str, Any]:
    """Create a valid V2.2 allowlist projection without user or model prose."""
    task = record.task
    return {
        "schema_version": "2.2",
        "review_id": record.review_id,
        "parent_review_id": record.parent_review_id,
        "created_at": record.created_at.isoformat(),
        "completed_at": record.completed_at.isoformat() if record.completed_at else None,
        "task": {
            "mode": task.mode,
            "output_mode": task.output_mode,
            "interactive_mode": task.interactive_mode,
            "briefing_mode": task.briefing_mode,
            "decision_fallback": task.decision_fallback,
            "trace_level": task.trace_level,
            "history_mode": "metadata",
        },
        "input_diagnostics": record.input_diagnostics.model_dump(mode="json"),
        "runtime_metadata": {
            "sampling_calls": record.runtime_metadata.sampling_calls,
            "elicitation_calls": record.runtime_metadata.elicitation_calls,
            "parse_failures": record.runtime_metadata.parse_failures,
            "elapsed_ms": record.runtime_metadata.elapsed_ms,
            "sample_budget": record.runtime_metadata.sample_budget,
            "reviewer_samples_successful": record.runtime_metadata.reviewer_samples_successful,
            "reviewer_samples_unavailable": record.runtime_metadata.reviewer_samples_unavailable,
            "reviewer_coverage": record.runtime_metadata.reviewer_coverage,
            "briefing_elicitation_calls": record.runtime_metadata.briefing_elicitation_calls,
            "context_gap_elicitation_calls": record.runtime_metadata.context_gap_elicitation_calls,
            "outcome_elicitation_calls": record.runtime_metadata.outcome_elicitation_calls,
            "package_version": _CURRENT_PACKAGE_VERSION,
            "diagnostic_build": _CURRENT_DIAGNOSTIC_BUILD,
        },
        "council_plan": {
            "mode": record.council_plan.mode,
            "discussion_enabled": record.council_plan.discussion_enabled,
            "interactive_enabled": record.council_plan.interactive_enabled,
            "sample_budget": record.council_plan.sample_budget,
            "max_discussion_rounds": record.council_plan.max_discussion_rounds,
            "max_decision_points": record.council_plan.max_decision_points,
        },
        "chief_editor_decision": {
            "publishability": record.chief_editor_decision.publishability,
            "review_needed": record.chief_editor_decision.review_needed,
        },
        "status": record.status,
        "degraded": record.degraded,
        "effective_brief": {
            "content_type": (
                record.effective_brief.content_type
                if record.effective_brief.content_type in _SAFE_CONTENT_TYPES
                else "unspecified"
            ),
            "context_confidence": record.effective_brief.context_confidence,
        },
        "briefing_interaction": {
            "requested": record.briefing_interaction.requested,
            "action": record.briefing_interaction.action,
            "asked_fields": [
                field for field in record.briefing_interaction.asked_fields
                if field in _SAFE_BRIEF_FIELDS
            ],
        },
        "context_gap_interaction": {
            "requested": record.context_gap_interaction.requested,
            "action": record.context_gap_interaction.action,
            "asked_count": record.context_gap_interaction.asked_count,
            "answered_count": record.context_gap_interaction.answered_count,
        },
        "reconsideration_provenance": {
            "requested_role_ids": [
                role_id for role_id in record.reconsideration_provenance.requested_role_ids
                if role_id in _SAFE_ROLE_IDS
            ],
            "completed_role_ids": [
                role_id for role_id in record.reconsideration_provenance.completed_role_ids
                if role_id in _SAFE_ROLE_IDS
            ],
            "skipped_role_ids": [
                role_id for role_id in record.reconsideration_provenance.skipped_role_ids
                if role_id in _SAFE_ROLE_IDS
            ],
            "failed_role_ids": [
                role_id for role_id in record.reconsideration_provenance.failed_role_ids
                if role_id in _SAFE_ROLE_IDS
            ],
        },
        "context_reconsideration_provenance": {
            name: [role_id for role_id in getattr(record.context_reconsideration_provenance, name) if role_id in _SAFE_ROLE_IDS]
            for name in ("requested_role_ids", "completed_role_ids", "skipped_role_ids", "failed_role_ids")
        },
        "outcome_reconsideration_provenance": {
            name: [role_id for role_id in getattr(record.outcome_reconsideration_provenance, name) if role_id in _SAFE_ROLE_IDS]
            for name in ("requested_role_ids", "completed_role_ids", "skipped_role_ids", "failed_role_ids")
        },
        "phase_trace": {
            "phases": [
                {
                    "phase": phase.phase,
                    "disposition": (
                        phase.disposition if phase.disposition in _SAFE_PHASE_DISPOSITIONS else "degraded"
                    ),
                    "counts": phase.counts,
                }
                for phase in record.phase_trace.phases
            ]
        },
        "version_metadata": {
            "package_version": _CURRENT_PACKAGE_VERSION,
            "diagnostic_build": _CURRENT_DIAGNOSTIC_BUILD,
            "record_schema": "2.2",
        },
    }


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.stem}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    except (OSError, TypeError, ValueError) as exc:
        raise ReviewPersistenceError("review record write failed") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


class ReviewStore:
    """Read and write review history with optional V1 working-directory fallback."""

    def __init__(
        self,
        storage_dir: str | Path | None = None,
        *,
        legacy_dir: str | Path | None = None,
        include_legacy: bool = True,
    ) -> None:
        self.storage_dir = Path(storage_dir) if storage_dir is not None else default_reviews_dir()
        self.include_legacy = include_legacy
        self.legacy_dir = Path(legacy_dir) if legacy_dir is not None else Path.cwd() / "reviews"

    def save(
        self,
        record: ReviewRecordV2 | dict[str, Any],
        *,
        history_mode: HistoryMode | None = None,
    ) -> Path | None:
        validated = record if isinstance(record, ReviewRecordV2) else ReviewRecordV2.model_validate(record)
        mode = history_mode or validated.task.history_mode
        if mode == "off":
            return None
        if not is_supported_review_id(validated.review_id) or _LEGACY_REVIEW_ID.fullmatch(validated.review_id):
            raise InvalidReviewIdError("new V2 records require a sortable V2 review ID")
        write_record = validated.model_copy(
            update={
                "schema_version": "2.2",
                "version_metadata": {
                    **validated.version_metadata,
                    "record_schema": "2.2",
                },
            }
        )
        payload = (
            write_record.model_dump(mode="json")
            if mode == "full"
            else _metadata_projection(write_record)
        )
        destination = self.storage_dir / f"{validated.review_id}.json"
        _atomic_write_json(destination, payload)
        return destination

    def load(self, review_id: str) -> ReviewRecordV1 | ReviewRecordV2:
        path = self.path_for(review_id)
        try:
            with path.open("r", encoding="utf-8") as stream:
                value = json.load(stream)
            record = parse_review_record(value)
        except (json.JSONDecodeError, UnicodeError, ValidationError, ValueError, OSError) as exc:
            raise MalformedReviewRecordError(
                f"review record {review_id!r} is malformed: {exc}"
            ) from exc
        if record.review_id != review_id:
            raise MalformedReviewRecordError(
                f"review record {review_id!r} contains mismatched review_id {record.review_id!r}"
            )
        return record

    def path_for(self, review_id: str) -> Path:
        if not is_supported_review_id(review_id):
            raise InvalidReviewIdError(f"unsupported review ID: {review_id!r}")
        current = self.storage_dir / f"{review_id}.json"
        try:
            if current.is_file():
                return current
            if self.include_legacy:
                legacy = self.legacy_dir / f"{review_id}.json"
                if legacy.is_file():
                    return legacy
        except OSError as exc:
            raise ReviewPersistenceError("review history lookup failed") from exc
        raise ReviewRecordNotFoundError(f"review record not found: {review_id}")

    def iter_records(self) -> Iterable[ReviewRecordV1 | ReviewRecordV2]:
        seen: set[str] = set()
        directories = [self.storage_dir]
        if self.include_legacy and self.legacy_dir != self.storage_dir:
            directories.append(self.legacy_dir)
        for directory in directories:
            try:
                paths = sorted(directory.glob("*.json"), reverse=True) if directory.is_dir() else []
            except OSError as exc:
                raise ReviewPersistenceError("review history listing failed") from exc
            for path in paths:
                review_id = path.stem
                if review_id in seen or not is_supported_review_id(review_id):
                    continue
                seen.add(review_id)
                yield self.load(review_id)


def save_review_record(
    record: ReviewRecordV2 | dict[str, Any],
    *,
    history_mode: HistoryMode | None = None,
    reviews_dir: str | Path | None = None,
) -> Path | None:
    return ReviewStore(storage_dir=reviews_dir).save(record, history_mode=history_mode)


def load_review_record(
    review_id: str,
    *,
    reviews_dir: str | Path | None = None,
    legacy_reviews_dir: str | Path | None = None,
    include_legacy: bool = True,
) -> ReviewRecordV1 | ReviewRecordV2:
    return ReviewStore(
        storage_dir=reviews_dir,
        legacy_dir=legacy_reviews_dir,
        include_legacy=include_legacy,
    ).load(review_id)
