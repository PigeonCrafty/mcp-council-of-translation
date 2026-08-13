"""Small V1/V2 record adapters with conservative additive-schema defaults."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from council_of_translation.localization.models import ReviewRecordV2


class ReviewRecordV1(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: Literal["1.0"] = "1.0"
    review_id: str
    task: dict[str, Any] = Field(default_factory=dict)
    mode: str = "standard"
    status: str = "completed"
    reviews: list[dict[str, Any]] = Field(default_factory=list)
    conflict_reviews: list[dict[str, Any]] = Field(default_factory=list)
    chief_editor_decision: dict[str, Any] = Field(default_factory=dict)


def parse_review_record(value: Any) -> ReviewRecordV1 | ReviewRecordV2:
    """Parse a stored record without treating malformed data as a success."""
    if not isinstance(value, dict):
        raise ValueError("review record must be a JSON object")
    schema_version = value.get("schema_version")
    if schema_version in (None, "1", "1.0"):
        data = dict(value)
        data["schema_version"] = "1.0"
        return ReviewRecordV1.model_validate(data)
    if schema_version in ("2", "2.0"):
        data = dict(value)
        data["schema_version"] = "2.0"
        return ReviewRecordV2.model_validate(data)
    if schema_version == "2.1":
        return ReviewRecordV2.model_validate(value)
    if schema_version in ("2.2", "2.3", "2.4"):
        return ReviewRecordV2.model_validate(value)
    raise ValueError(f"unsupported review record schema_version: {schema_version}")


def record_schema_version(value: Any) -> str:
    return parse_review_record(value).schema_version
