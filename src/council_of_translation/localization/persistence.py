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
    """Create a valid V2 allowlist projection without user or model prose."""
    task = record.task
    return {
        "schema_version": "2.0",
        "review_id": record.review_id,
        "parent_review_id": record.parent_review_id,
        "created_at": record.created_at.isoformat(),
        "completed_at": record.completed_at.isoformat() if record.completed_at else None,
        "task": {
            "mode": task.mode,
            "output_mode": task.output_mode,
            "interactive_mode": task.interactive_mode,
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
            "package_version": "0.4.0",
            "diagnostic_build": "structured-deliberation-v2",
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
        "version_metadata": {
            "package_version": "0.4.0",
            "diagnostic_build": "structured-deliberation-v2",
            "record_schema": "2.0",
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
        payload = (
            validated.model_dump(mode="json")
            if mode == "full"
            else _metadata_projection(validated)
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
