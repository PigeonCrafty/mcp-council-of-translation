import asyncio
from time import perf_counter

import pytest

from council_of_translation.localization.runtime import (
    CorrelatedSampleWork,
    ModelExecutionResult,
    resolve_review_concurrency,
    sample_correlated_batch,
)


class DelayedExecutor:
    def __init__(self, delays, *, failing_role=""):
        self.delays = delays
        self.failing_role = failing_role
        self.active = 0
        self.peak = 0
        self.started = []
        self.completed = []
        self.calls = {}

    async def sample(self, prompt, *, temperature=0.2, max_tokens=1_400):
        del temperature, max_tokens
        role_id = prompt
        self.calls[role_id] = self.calls.get(role_id, 0) + 1
        self.started.append(role_id)
        self.active += 1
        self.peak = max(self.peak, self.active)
        try:
            await asyncio.sleep(self.delays[role_id])
            if role_id == self.failing_role:
                raise RuntimeError("bounded provider failure")
            self.completed.append(role_id)
            return ModelExecutionResult(status="success", text=role_id)
        finally:
            self.active -= 1


def run(coro):
    return asyncio.run(coro)


@pytest.mark.parametrize(
    ("raw", "limit", "disposition"),
    [
        (None, 3, "default"),
        ("1", 1, "configured"),
        ("2", 2, "configured"),
        ("3", 3, "configured"),
        ("", 1, "invalid_fallback"),
        ("fast", 1, "invalid_fallback"),
        ("0", 1, "invalid_fallback"),
        ("4", 1, "invalid_fallback"),
    ],
)
def test_review_concurrency_configuration_truth_table(monkeypatch, raw, limit, disposition):
    monkeypatch.delenv("COUNCIL_REVIEW_CONCURRENCY", raising=False)
    if raw is not None:
        monkeypatch.setenv("COUNCIL_REVIEW_CONCURRENCY", raw)
    config = resolve_review_concurrency()
    assert config.effective_limit == limit
    assert config.disposition == disposition


def test_batch_is_bounded_overlapping_and_returns_input_order():
    roles = [f"role-{index}" for index in range(6)]
    executor = DelayedExecutor({role: 0.01 * (6 - index) for index, role in enumerate(roles)})
    results, stats = run(sample_correlated_batch(
        executor,
        [CorrelatedSampleWork(role, role) for role in roles],
        limit=3,
    ))
    assert executor.peak == stats.peak_concurrency == 3
    assert stats.effective_limit == 3
    assert stats.batch_count == 2
    assert executor.completed != roles
    assert [item.role_id for item in results] == roles
    assert [item.result.text for item in results] == roles
    assert executor.calls == {role: 1 for role in roles}


def test_sequential_override_has_no_overlap_and_is_materially_slower():
    roles = [f"role-{index}" for index in range(6)]
    delays = {role: 0.025 for role in roles}
    sequential = DelayedExecutor(delays)
    started = perf_counter()
    _, sequential_stats = run(sample_correlated_batch(
        sequential, [CorrelatedSampleWork(role, role) for role in roles], limit=1
    ))
    sequential_wall = perf_counter() - started
    parallel = DelayedExecutor(delays)
    started = perf_counter()
    _, parallel_stats = run(sample_correlated_batch(
        parallel, [CorrelatedSampleWork(role, role) for role in roles], limit=3
    ))
    parallel_wall = perf_counter() - started
    assert sequential_stats.peak_concurrency == 1
    assert sequential_stats.batch_count == 6
    assert parallel_stats.peak_concurrency == 3
    assert parallel_stats.batch_count == 2
    assert parallel_wall < sequential_wall * 0.7


def test_one_exception_isolated_without_replay_or_sibling_cancellation():
    roles = [f"role-{index}" for index in range(6)]
    executor = DelayedExecutor({role: 0.005 for role in roles}, failing_role="role-2")
    results, stats = run(sample_correlated_batch(
        executor, [CorrelatedSampleWork(role, role) for role in roles], limit=3
    ))
    assert stats.peak_concurrency == 3
    assert [item.role_id for item in results] == roles
    assert results[2].result.status == "error"
    assert "bounded provider failure" in results[2].result.error
    assert all(item.result.status == "success" for index, item in enumerate(results) if index != 2)
    assert executor.calls == {role: 1 for role in roles}
