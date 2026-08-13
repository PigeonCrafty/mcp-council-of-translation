"""Runtime ports and transport adapters for Council Core.

This module deliberately does not import FastMCP.  The production adapters use
the small, duck-typed surface exposed by a context (``sample`` and ``elicit``),
while the scripted implementations make orchestration tests deterministic.
"""

from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass, field
import os
from time import perf_counter
from typing import Any, Callable, Literal, Protocol, cast, runtime_checkable

from council_of_translation.localization.models import RuntimeMetadata


SampleStatus = Literal["success", "malformed", "error"]
ElicitationAction = Literal[
    "accept", "decline", "cancel", "unsupported", "malformed", "error"
]

MAX_RUNTIME_TEXT = 16_000
MAX_EVENT_DETAIL = 240
MAX_TELEMETRY_EVENTS = 64
MAX_REVIEW_CONCURRENCY = 3
REVIEW_CONCURRENCY_ENV = "COUNCIL_REVIEW_CONCURRENCY"


@dataclass(frozen=True)
class ModelExecutionResult:
    status: SampleStatus
    text: str = ""
    error: str = ""


@dataclass(frozen=True)
class ReviewConcurrencyConfig:
    effective_limit: int
    disposition: Literal["default", "configured", "invalid_fallback"]


@dataclass(frozen=True)
class CorrelatedSampleWork:
    role_id: str
    prompt: str
    max_tokens: int = 1_400


@dataclass(frozen=True)
class CorrelatedSampleResult:
    role_id: str
    result: ModelExecutionResult


@dataclass(frozen=True)
class SamplingBatchStats:
    effective_limit: int
    peak_concurrency: int
    batch_count: int
    wall_clock_ms: int


@dataclass(frozen=True)
class InteractionCapabilities:
    form_elicitation: bool = False


@dataclass(frozen=True)
class ElicitationResult:
    action: ElicitationAction
    data: dict[str, Any] = field(default_factory=dict)
    error: str = ""


@runtime_checkable
class ModelExecutor(Protocol):
    async def sample(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 1_400,
    ) -> ModelExecutionResult: ...


@runtime_checkable
class UserInteractionGateway(Protocol):
    def capabilities(self) -> InteractionCapabilities: ...

    async def elicit(
        self,
        message: str,
        *,
        response_type: Any,
    ) -> ElicitationResult: ...


@dataclass(frozen=True)
class RuntimeEvent:
    kind: Literal["sampling", "elicitation", "parse_failure", "fallback"]
    outcome: str
    elapsed_ms: int = 0
    detail: str = ""


TelemetryHook = Callable[[RuntimeEvent], None]


def resolve_review_concurrency(raw: str | None = None) -> ReviewConcurrencyConfig:
    """Resolve one review's bounded operator concurrency configuration."""
    value = os.environ.get(REVIEW_CONCURRENCY_ENV) if raw is None else raw
    if value is None:
        return ReviewConcurrencyConfig(MAX_REVIEW_CONCURRENCY, "default")
    if value in {"1", "2", "3"}:
        return ReviewConcurrencyConfig(int(value), "configured")
    return ReviewConcurrencyConfig(1, "invalid_fallback")


async def sample_correlated_batch(
    executor: ModelExecutor,
    work: list[CorrelatedSampleWork],
    *,
    limit: int,
    telemetry: RuntimeTelemetry | None = None,
) -> tuple[list[CorrelatedSampleResult], SamplingBatchStats]:
    """Attempt role-correlated samples once, bounded and returned in input order."""
    if not work:
        return [], SamplingBatchStats(0, 0, 0, 0)
    effective_limit = max(1, min(int(limit), MAX_REVIEW_CONCURRENCY, len(work)))
    semaphore = asyncio.Semaphore(effective_limit)
    active = 0
    peak = 0
    started = perf_counter()

    async def run_one(item: CorrelatedSampleWork) -> CorrelatedSampleResult:
        nonlocal active, peak
        async with semaphore:
            active += 1
            peak = max(peak, active)
            try:
                try:
                    result = await executor.sample(
                        item.prompt,
                        temperature=0.2,
                        max_tokens=item.max_tokens,
                    )
                except Exception as exc:
                    result = ModelExecutionResult(status="error", error=_bounded_error(exc))
                    if telemetry is not None:
                        telemetry.record(RuntimeEvent("sampling", "error", detail=result.error))
                return CorrelatedSampleResult(item.role_id, result)
            finally:
                active -= 1

    results = await asyncio.gather(*(run_one(item) for item in work))
    wall_clock_ms = _elapsed_ms(started)
    batch_count = (len(work) + effective_limit - 1) // effective_limit
    return results, SamplingBatchStats(
        effective_limit=effective_limit,
        peak_concurrency=peak,
        batch_count=batch_count,
        wall_clock_ms=wall_clock_ms,
    )


class RuntimeTelemetry:
    """Bounded, content-free counters suitable for persisted runtime metadata."""

    def __init__(
        self,
        *,
        sample_budget: int = 10,
        hook: TelemetryHook | None = None,
        max_events: int = MAX_TELEMETRY_EVENTS,
    ) -> None:
        self.sample_budget = max(0, min(int(sample_budget), 18))
        self.hook = hook
        self.max_events = max(0, min(int(max_events), MAX_TELEMETRY_EVENTS))
        self.sampling_calls = 0
        self.elicitation_calls = 0
        self.elicitation_actions: list[str] = []
        self.parse_failures = 0
        self.fallbacks: list[str] = []
        self.elapsed_ms = 0
        self.wall_clock_ms = 0
        self.sampling_wait_ms = 0
        self.independent_review_concurrency_limit = 1
        self.independent_review_peak_concurrency = 0
        self.independent_review_batch_count = 0
        self.independent_review_concurrency_disposition = "legacy"
        self.events: list[RuntimeEvent] = []
        self.phase_elicitation_actions: dict[str, list[str]] = {
            "briefing": [],
            "context_gap": [],
            "outcome": [],
        }

    def record_phase_elicitation(self, phase: str, action: str) -> None:
        """Attribute an already-counted elicitation to one workflow phase."""
        if phase not in self.phase_elicitation_actions:
            return
        actions = self.phase_elicitation_actions[phase]
        if len(actions) < MAX_TELEMETRY_EVENTS:
            actions.append(str(action)[:64])

    def record(self, event: RuntimeEvent) -> None:
        safe_event = RuntimeEvent(
            kind=event.kind,
            outcome=str(event.outcome)[:64],
            elapsed_ms=max(0, int(event.elapsed_ms)),
            detail=str(event.detail)[:MAX_EVENT_DETAIL],
        )
        self.elapsed_ms += safe_event.elapsed_ms
        if safe_event.kind == "sampling":
            self.sampling_calls += 1
            self.sampling_wait_ms += safe_event.elapsed_ms
        elif safe_event.kind == "elicitation":
            self.elicitation_calls += 1
            if len(self.elicitation_actions) < MAX_TELEMETRY_EVENTS:
                self.elicitation_actions.append(safe_event.outcome)
        elif safe_event.kind == "parse_failure":
            self.parse_failures += 1
        elif safe_event.kind == "fallback":
            if len(self.fallbacks) < MAX_TELEMETRY_EVENTS:
                self.fallbacks.append(safe_event.outcome)
        if len(self.events) < self.max_events:
            self.events.append(safe_event)
        if self.hook is not None:
            try:
                self.hook(safe_event)
            except Exception:
                # Telemetry must never make the review workflow fail.
                pass

    def snapshot(self) -> RuntimeMetadata:
        return RuntimeMetadata(
            sampling_calls=self.sampling_calls,
            elicitation_calls=self.elicitation_calls,
            elicitation_actions=self.elicitation_actions,
            parse_failures=self.parse_failures,
            fallbacks=self.fallbacks,
            elapsed_ms=self.elapsed_ms,
            wall_clock_ms=self.wall_clock_ms,
            sampling_wait_ms=self.sampling_wait_ms,
            independent_review_concurrency_limit=self.independent_review_concurrency_limit,
            independent_review_peak_concurrency=self.independent_review_peak_concurrency,
            independent_review_batch_count=self.independent_review_batch_count,
            independent_review_concurrency_disposition=(
                self.independent_review_concurrency_disposition
            ),
            sample_budget=self.sample_budget,
            briefing_elicitation_calls=len(self.phase_elicitation_actions["briefing"]),
            briefing_elicitation_actions=self.phase_elicitation_actions["briefing"],
            context_gap_elicitation_calls=len(self.phase_elicitation_actions["context_gap"]),
            context_gap_elicitation_actions=self.phase_elicitation_actions["context_gap"],
            outcome_elicitation_calls=len(self.phase_elicitation_actions["outcome"]),
            outcome_elicitation_actions=self.phase_elicitation_actions["outcome"],
        )


def _elapsed_ms(start: float) -> int:
    return max(0, int((perf_counter() - start) * 1_000))


def _bounded_error(error: BaseException | str) -> str:
    return str(error)[:MAX_EVENT_DETAIL]


def _extract_sample_text(response: Any) -> str:
    if isinstance(response, str):
        return response[:MAX_RUNTIME_TEXT]
    text = getattr(response, "text", None)
    if text is not None:
        return str(text)[:MAX_RUNTIME_TEXT]
    content = getattr(response, "content", None)
    if isinstance(content, (list, tuple)) and content:
        item = content[0]
        if isinstance(item, dict) and "text" in item:
            return str(item["text"])[:MAX_RUNTIME_TEXT]
        item_text = getattr(item, "text", None)
        if item_text is not None:
            return str(item_text)[:MAX_RUNTIME_TEXT]
    return ""


class FastMCPModelExecutor:
    """Duck-typed adapter for a FastMCP-compatible context's sampling API."""

    def __init__(self, context: Any, telemetry: RuntimeTelemetry | None = None) -> None:
        self._context = context
        self.telemetry = telemetry or RuntimeTelemetry()

    async def sample(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 1_400,
    ) -> ModelExecutionResult:
        start = perf_counter()
        sampler = getattr(self._context, "sample", None)
        if not callable(sampler):
            result = ModelExecutionResult(status="error", error="sampling unsupported")
        else:
            try:
                response = await sampler(
                    prompt[:MAX_RUNTIME_TEXT],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                text = _extract_sample_text(response)
                result = (
                    ModelExecutionResult(status="success", text=text)
                    if text.strip()
                    else ModelExecutionResult(status="malformed", error="empty sampling response")
                )
            except Exception as exc:  # transport failures are normalized for Core
                result = ModelExecutionResult(status="error", error=_bounded_error(exc))
        self.telemetry.record(
            RuntimeEvent("sampling", result.status, _elapsed_ms(start), result.error)
        )
        return result


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    dumper = getattr(value, "model_dump", None)
    if callable(dumper):
        dumped = dumper()
        return dict(dumped) if isinstance(dumped, dict) else {}
    return {}


def _normalize_elicitation(response: Any) -> ElicitationResult:
    envelope = _as_mapping(response)
    action_value = envelope.get("action", getattr(response, "action", ""))
    action = str(getattr(action_value, "value", action_value)).lower()
    if action not in {"accept", "decline", "cancel"}:
        return ElicitationResult(action="malformed", error="unknown elicitation action")
    if action != "accept":
        return ElicitationResult(action=cast(ElicitationAction, action))
    raw_data = envelope.get("data", getattr(response, "data", None))
    data = _as_mapping(raw_data)
    if not data:
        return ElicitationResult(action="malformed", error="accepted elicitation has no form data")
    return ElicitationResult(action="accept", data=data)


class FastMCPUserInteractionGateway:
    """Duck-typed one-form elicitation adapter with explicit safe outcomes."""

    def __init__(self, context: Any, telemetry: RuntimeTelemetry | None = None) -> None:
        self._context = context
        self.telemetry = telemetry or RuntimeTelemetry()

    def capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(
            form_elicitation=callable(getattr(self._context, "elicit", None))
        )

    async def elicit(
        self,
        message: str,
        *,
        response_type: Any,
    ) -> ElicitationResult:
        start = perf_counter()
        elicitor = getattr(self._context, "elicit", None)
        if not callable(elicitor):
            result = ElicitationResult(action="unsupported")
        else:
            try:
                response = await elicitor(
                    message=message[:MAX_RUNTIME_TEXT], response_type=response_type
                )
                result = _normalize_elicitation(response)
            except (NotImplementedError, AttributeError) as exc:
                result = ElicitationResult(action="unsupported", error=_bounded_error(exc))
            except Exception as exc:  # client cancellation/errors must not escape into Core
                result = ElicitationResult(action="error", error=_bounded_error(exc))
        self.telemetry.record(
            RuntimeEvent("elicitation", result.action, _elapsed_ms(start), result.error)
        )
        return result


ScriptedSample = ModelExecutionResult | str | BaseException
ScriptedElicitation = ElicitationResult | dict[str, Any] | BaseException


class ScriptedModelExecutor:
    """Deterministic model double; exhausting the script is a normalized error."""

    def __init__(
        self,
        script: list[ScriptedSample],
        telemetry: RuntimeTelemetry | None = None,
    ) -> None:
        self._script = deque(script)
        self.telemetry = telemetry or RuntimeTelemetry()
        self.prompts: list[str] = []

    async def sample(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 1_400,
    ) -> ModelExecutionResult:
        del temperature, max_tokens
        start = perf_counter()
        self.prompts.append(prompt[:MAX_RUNTIME_TEXT])
        if not self._script:
            result = ModelExecutionResult(status="error", error="sample script exhausted")
        else:
            scripted = self._script.popleft()
            if isinstance(scripted, BaseException):
                result = ModelExecutionResult(status="error", error=_bounded_error(scripted))
            elif isinstance(scripted, ModelExecutionResult):
                result = scripted
            elif isinstance(scripted, str) and scripted.strip():
                result = ModelExecutionResult(status="success", text=scripted[:MAX_RUNTIME_TEXT])
            else:
                result = ModelExecutionResult(status="malformed", error="empty scripted response")
        self.telemetry.record(
            RuntimeEvent("sampling", result.status, _elapsed_ms(start), result.error)
        )
        return result


class ScriptedUserInteractionGateway:
    """Deterministic interaction double for accept/decline/cancel/error paths."""

    def __init__(
        self,
        script: list[ScriptedElicitation] | None = None,
        *,
        supported: bool = True,
        telemetry: RuntimeTelemetry | None = None,
    ) -> None:
        self._script = deque(script or [])
        self._supported = supported
        self.telemetry = telemetry or RuntimeTelemetry()
        self.requests: list[tuple[str, Any]] = []

    def capabilities(self) -> InteractionCapabilities:
        return InteractionCapabilities(form_elicitation=self._supported)

    async def elicit(
        self,
        message: str,
        *,
        response_type: Any,
    ) -> ElicitationResult:
        start = perf_counter()
        self.requests.append((message[:MAX_RUNTIME_TEXT], response_type))
        if not self._supported:
            result = ElicitationResult(action="unsupported")
        elif not self._script:
            result = ElicitationResult(action="error", error="elicitation script exhausted")
        else:
            scripted = self._script.popleft()
            if isinstance(scripted, BaseException):
                result = ElicitationResult(action="error", error=_bounded_error(scripted))
            elif isinstance(scripted, ElicitationResult):
                result = scripted
            else:
                result = _normalize_elicitation(scripted)
        self.telemetry.record(
            RuntimeEvent("elicitation", result.action, _elapsed_ms(start), result.error)
        )
        return result
