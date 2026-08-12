import asyncio

from pydantic import BaseModel

from council_of_translation.localization.runtime import (
    ElicitationResult,
    FastMCPModelExecutor,
    FastMCPUserInteractionGateway,
    ModelExecutionResult,
    ModelExecutor,
    RuntimeEvent,
    RuntimeTelemetry,
    ScriptedModelExecutor,
    ScriptedUserInteractionGateway,
    UserInteractionGateway,
)


def run(coro):
    return asyncio.run(coro)


class FormData(BaseModel):
    decision_1: str


class SamplingResponse:
    text = '{"ok": true}'


class AcceptedResponse:
    action = "accept"
    data = FormData(decision_1="option-a")


class DuckContext:
    async def sample(self, prompt, *, temperature, max_tokens):
        assert prompt == "review"
        assert temperature == 0.1
        assert max_tokens == 99
        return SamplingResponse()

    async def elicit(self, *, message, response_type):
        assert message == "Choose"
        assert response_type is FormData
        return AcceptedResponse()


def test_core_protocols_and_fastmcp_duck_adapters_have_no_fastmcp_dependency():
    telemetry = RuntimeTelemetry(sample_budget=6)
    executor = FastMCPModelExecutor(DuckContext(), telemetry)
    gateway = FastMCPUserInteractionGateway(DuckContext(), telemetry)

    assert isinstance(executor, ModelExecutor)
    assert isinstance(gateway, UserInteractionGateway)
    sampled = run(executor.sample("review", temperature=0.1, max_tokens=99))
    elicited = run(gateway.elicit("Choose", response_type=FormData))

    assert sampled == ModelExecutionResult(status="success", text='{"ok": true}')
    assert elicited == ElicitationResult(action="accept", data={"decision_1": "option-a"})
    assert gateway.capabilities().form_elicitation is True
    assert telemetry.snapshot().sampling_calls == 1
    assert telemetry.snapshot().elicitation_actions == ["accept"]


def test_fastmcp_adapters_normalize_malformed_error_and_unsupported():
    class EmptySample:
        async def sample(self, *args, **kwargs):
            return object()

    class FailedSample:
        async def sample(self, *args, **kwargs):
            raise RuntimeError("provider failed")

    malformed = run(FastMCPModelExecutor(EmptySample()).sample("x"))
    failed = run(FastMCPModelExecutor(FailedSample()).sample("x"))
    gateway = FastMCPUserInteractionGateway(object())

    assert malformed.status == "malformed"
    assert failed == ModelExecutionResult(status="error", error="provider failed")
    assert gateway.capabilities().form_elicitation is False
    assert run(gateway.elicit("x", response_type=FormData)).action == "unsupported"


def test_sampling_accepts_raw_json_and_rejects_reasoning_only_or_empty_content():
    class RawJson:
        async def sample(self, *args, **kwargs):
            return '{"role_feedback":"ok","findings":[]}'

    class ReasoningOnly:
        async def sample(self, *args, **kwargs):
            return type("Response", (), {"reasoning": "private analysis"})()

    class EmptyText:
        async def sample(self, *args, **kwargs):
            return type("Response", (), {"text": "   "})()

    assert run(FastMCPModelExecutor(RawJson()).sample("x")).status == "success"
    assert run(FastMCPModelExecutor(ReasoningOnly()).sample("x")).status == "malformed"
    assert run(FastMCPModelExecutor(EmptyText()).sample("x")).status == "malformed"


def test_scripted_model_covers_success_malformed_error_and_exhaustion():
    executor = ScriptedModelExecutor(
        ["valid", "", RuntimeError("boom"), ModelExecutionResult(status="malformed")]
    )

    assert run(executor.sample("one")).status == "success"
    assert run(executor.sample("two")).status == "malformed"
    assert run(executor.sample("three")).status == "error"
    assert run(executor.sample("four")).status == "malformed"
    assert run(executor.sample("five")).error == "sample script exhausted"
    assert executor.telemetry.snapshot().sampling_calls == 5


def test_scripted_gateway_covers_accept_decline_cancel_malformed_error_and_unsupported():
    gateway = ScriptedUserInteractionGateway(
        [
            {"action": "accept", "data": {"decision_1": "a"}},
            {"action": "decline"},
            ElicitationResult(action="cancel"),
            {"action": "mystery"},
            RuntimeError("client failed"),
        ]
    )

    outcomes = [run(gateway.elicit("form", response_type=FormData)) for _ in range(5)]
    assert [outcome.action for outcome in outcomes] == [
        "accept",
        "decline",
        "cancel",
        "malformed",
        "error",
    ]
    assert outcomes[0].data == {"decision_1": "a"}
    assert gateway.telemetry.snapshot().elicitation_calls == 5

    unsupported = ScriptedUserInteractionGateway(supported=False)
    assert unsupported.capabilities().form_elicitation is False
    assert run(unsupported.elicit("form", response_type=FormData)).action == "unsupported"


def test_telemetry_hooks_and_storage_are_bounded_and_content_free():
    observed = []
    telemetry = RuntimeTelemetry(sample_budget=999, hook=observed.append, max_events=999)
    for index in range(80):
        telemetry.record(RuntimeEvent("fallback", f"fallback-{index}", detail="x" * 1_000))
    telemetry.record(RuntimeEvent("parse_failure", "invalid_json"))

    snapshot = telemetry.snapshot()
    assert snapshot.sample_budget == 14
    assert snapshot.parse_failures == 1
    assert len(telemetry.events) == 64
    assert len(observed) == 81
    assert len(snapshot.fallbacks) == 64
    assert all(len(event.detail) <= 240 for event in observed)
    assert not hasattr(snapshot, "prompts")

    RuntimeTelemetry(hook=lambda event: (_ for _ in ()).throw(RuntimeError("ignored"))).record(
        RuntimeEvent("fallback", "safe")
    )
