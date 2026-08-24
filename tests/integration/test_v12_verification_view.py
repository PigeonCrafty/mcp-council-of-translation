import asyncio
from copy import deepcopy

from fastmcp import Client

from council_of_translation.localization.models import (
    ChiefEditorDecisionV2,
    ReviewRecordV2,
    ReviewTaskV2,
    RuntimeMetadata,
)
from council_of_translation.localization.compatibility import parse_review_record
from council_of_translation.localization.orchestration import compact_review_response
from council_of_translation.localization.persistence import ReviewStore
from council_of_translation.localization.roles import build_council_plan
from council_of_translation.presentation import structured_payload
from council_of_translation.server import mcp
from council_of_translation.tools import review as review_module


def _record() -> ReviewRecordV2:
    record = ReviewRecordV2(
        schema_version="2.5",
        review_id="20260824T020304000005Z_ab12cd34",
        task=ReviewTaskV2(
            source_text="Save",
            candidate_translation="保存",
            content_type="ui",
            history_mode="full",
        ),
        chief_editor_decision=ChiefEditorDecisionV2(
            publishability="可发布",
            review_needed="否",
        ),
        status="COMPLETED",
        display_report=(
            "# 审校背景\n\n- 当前译文通过审校。\n\n"
            "## 主编结论\n\n- 最终处置：可发布；需人工复核：否"
        ),
    )
    # A persisted full record physically contains every modeled field, including
    # empty lists and zero counters. Revalidation reproduces that loaded shape.
    return ReviewRecordV2.model_validate(record.model_dump(mode="json"))


def test_actual_registered_verification_view_has_exact_dual_channel_wrapper(monkeypatch):
    record = _record()
    before = deepcopy(record.model_dump(mode="json"))
    calls = {"load": 0, "save": 0}

    class FakeStore:
        def load(self, review_id):
            calls["load"] += 1
            assert review_id == record.review_id
            return record

        def save(self, *args, **kwargs):
            calls["save"] += 1
            raise AssertionError("verification retrieval must not save")

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    async def call():
        async with Client(mcp) as client:
            return await client.call_tool(
                "view_review_record",
                {"review_id": record.review_id, "detail_level": "verification"},
            )

    result = asyncio.run(call())
    payload = result.structured_content

    assert list(payload) == ["review_id", "display_report", "verification_receipt"]
    assert payload["review_id"] == record.review_id
    assert payload["verification_receipt"]["review_id"] == record.review_id
    assert payload["verification_receipt"]["availability"]["verification_complete"] is True
    assert result.content[0].text.startswith("# Council 验证回执")
    assert [line for line in payload["display_report"].splitlines() if line.startswith("#")] == [
        "# Council 验证回执",
        "## 记录与路由",
        "## 覆盖与调用",
        "## 风险与裁决",
        "## 一致性与可用性",
    ]
    serving = payload["verification_receipt"]["serving"]
    assert (
        f"当前服务：包 `{serving['package_version']}`；"
        f"模块 `{serving['module_version']}`；"
        f"构建 `{serving['diagnostic_build']}`；"
        f"Schema `{serving['schema_version']}`。"
    ) in payload["display_report"]
    assert result.content[0].text.endswith(
        f"审校记录：{record.review_id}；可用 view_review_record 获取结构化证据。"
    )
    assert "source_text" not in str(payload)
    assert "candidate_translation" not in str(payload)
    assert calls == {"load": 1, "save": 0}
    assert record.model_dump(mode="json") == before


def test_existing_full_and_summary_payloads_remain_exact(monkeypatch):
    record = _record()

    class FakeStore:
        def load(self, review_id):
            assert review_id == record.review_id
            return record

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    full = structured_payload(review_module.view_review_record.fn(record.review_id, "full"))
    summary = structured_payload(review_module.view_review_record.fn(record.review_id, "summary"))

    assert full == record.model_dump(mode="json")
    assert summary == compact_review_response(record)


def test_direct_invalid_detail_level_keeps_bounded_truthful_error(monkeypatch):
    record = _record()

    class FakeStore:
        def load(self, review_id):
            return record

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    payload = structured_payload(
        review_module.view_review_record.fn(record.review_id, "PRIVATE invalid detail")
    )

    assert payload == {"error": "detail_level must be full, summary, or verification"}
    assert "PRIVATE" not in str(payload)


def _legal_record(
    mode: str,
    sampling_calls: int,
    publishability: str,
    review_needed: str,
    status: str,
) -> ReviewRecordV2:
    record = _record()
    suffix = {"lightweight": "aaaaaaaaaaaa", "standard": "bbbbbbbbbbbb", "strict": "cccccccccccc"}[mode]
    record.review_id = f"20260824T020304000005Z_{suffix}"
    plan = build_council_plan(mode, "legal_risk")
    record.council_plan = plan
    record.independent_reviews = [
        {"agent_name": role_id, "sample_status": "structured_success"}
        for role_id in plan.active_role_ids
    ]
    record.runtime_metadata = RuntimeMetadata(
        sampling_calls=sampling_calls,
        elicitation_calls=0,
        sample_budget=plan.sample_budget,
        reviewer_samples_successful=len(plan.active_role_ids),
        reviewer_samples_unavailable=0,
        reviewer_coverage="full",
        independent_review_concurrency_limit=3,
        independent_review_peak_concurrency=3,
        independent_review_batch_count=(len(plan.active_role_ids) + 2) // 3,
        independent_review_concurrency_disposition="default",
    )
    record.chief_editor_decision = ChiefEditorDecisionV2(
        publishability=publishability,
        review_needed=review_needed,
    )
    record.status = status
    record.display_report = (
        "# 审校背景\n\n- 合成法律风险记录。\n\n"
        f"## 主编结论\n\n- 最终处置：{publishability}；需人工复核：{review_needed}"
    )
    return ReviewRecordV2.model_validate(record.model_dump(mode="json"))


def test_live_shaped_a_b_c_verification_views_preserve_canonical_values(monkeypatch):
    records = [
        _legal_record("standard", 7, "修改后可发布", "否", "COMPLETED"),
        _legal_record("lightweight", 4, "可发布", "否", "COMPLETED"),
        _legal_record("strict", 8, "需人工复核", "是", "NEEDS_HUMAN_REVIEW"),
    ]

    class FakeStore:
        def load(self, review_id):
            return next(record for record in records if record.review_id == review_id)

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    for record, expected in zip(
        records,
        [
            ("standard", 7, 13, "修改后可发布", "否"),
            ("lightweight", 4, 6, "可发布", "否"),
            ("strict", 8, 18, "需人工复核", "是"),
        ],
    ):
        payload = structured_payload(
            review_module.view_review_record.fn(record.review_id, "verification")
        )
        receipt = payload["verification_receipt"]
        mode, calls, budget, publishability, review_needed = expected
        assert receipt["routing"]["mode"] == mode
        assert receipt["routing"]["active_role_ids"] == record.council_plan.active_role_ids
        assert receipt["runtime"]["sampling_calls_total"] == calls
        assert receipt["runtime"]["sample_budget_total"] == budget
        assert receipt["runtime"]["elicitation_calls_total"] == 0
        assert receipt["reviewer_execution"]["coverage"] == "full"
        assert receipt["outcome"]["publishability"] == publishability
        assert receipt["outcome"]["review_needed"] == review_needed
        assert receipt["coherence"]["terminal_disposition_occurrences"] == 1
        assert receipt["coherence"]["terminal_disposition_is_last_report_line"] is True
        assert receipt["coherence"]["terminal_disposition_matches_structured"] is True
        assert len(payload["display_report"]) <= 2_400


def test_terminal_mismatch_is_reported_without_repair(monkeypatch):
    record = _legal_record("standard", 7, "修改后可发布", "否", "COMPLETED")
    mismatched = "- 最终处置：需人工复核；需人工复核：是"
    record.display_report = f"# 审校背景\n\n{mismatched}"
    before = record.model_dump(mode="json")

    class FakeStore:
        def load(self, review_id):
            return record

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)
    payload = structured_payload(
        review_module.view_review_record.fn(record.review_id, "verification")
    )
    coherence = payload["verification_receipt"]["coherence"]

    assert coherence == {
        "expected_terminal_disposition": "- 最终处置：修改后可发布；需人工复核：否",
        "terminal_disposition_occurrences": 0,
        "terminal_disposition_is_last_report_line": False,
        "terminal_disposition_matches_structured": False,
    }
    assert record.display_report.endswith(mismatched)
    assert record.model_dump(mode="json") == before


def test_unavailable_reviewer_and_continuation_parent_are_visible_without_prose(monkeypatch):
    record = _legal_record("standard", 7, "需人工复核", "是", "NEEDS_HUMAN_REVIEW")
    record.parent_review_id = "20260823T020304000005Z_cd34ef56"
    failed_role = record.council_plan.active_role_ids[2]
    record.independent_reviews[2] = {
        "agent_name": failed_role,
        "sample_status": "unavailable",
        "sample_error": "PRIVATE PROVIDER FAILURE",
    }
    record.runtime_metadata.reviewer_samples_successful -= 1
    record.runtime_metadata.reviewer_samples_unavailable = 1
    record.runtime_metadata.reviewer_coverage = "partial"

    class FakeStore:
        def load(self, review_id):
            return record

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)
    payload = structured_payload(
        review_module.view_review_record.fn(record.review_id, "verification")
    )
    receipt = payload["verification_receipt"]

    assert receipt["record"]["parent_review_id"] == record.parent_review_id
    assert receipt["reviewer_execution"]["coverage"] == "partial"
    assert receipt["reviewer_execution"]["unavailable_count"] == 1
    assert {item["role_id"]: item["sample_status"] for item in receipt["reviewer_execution"]["samples"]}[failed_role] == "unavailable"
    assert "PRIVATE" not in str(payload)


def test_metadata_and_legacy_actual_verification_views_are_bounded(monkeypatch, tmp_path):
    store = ReviewStore(tmp_path / "records", include_legacy=False)
    metadata_record = _record()
    metadata_record.task.history_mode = "metadata"
    store.save(metadata_record, history_mode="metadata")
    loaded_metadata = store.load(metadata_record.review_id)
    legacy = parse_review_record({
        "review_id": "20260824_020304",
        "mode": "standard",
        "status": "completed",
        "chief_editor_decision": {"publishability": "可发布", "review_needed": "否"},
        "task": {"source": "PRIVATE LEGACY SOURCE"},
    })

    class FakeStore:
        def load(self, review_id):
            return loaded_metadata if review_id == loaded_metadata.review_id else legacy

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)
    metadata_payload = structured_payload(
        review_module.view_review_record.fn(loaded_metadata.review_id, "verification")
    )
    legacy_payload = structured_payload(
        review_module.view_review_record.fn(legacy.review_id, "verification")
    )

    assert metadata_payload["verification_receipt"]["record"]["history_mode"] == "metadata"
    assert metadata_payload["verification_receipt"]["availability"]["verification_complete"] is False
    assert legacy_payload["verification_receipt"]["record"]["history_mode"] == "legacy"
    assert "PRIVATE" not in str(legacy_payload)
    assert len(metadata_payload["display_report"]) <= 2_400
    assert len(legacy_payload["display_report"]) <= 2_400


def test_verification_retrieval_preserves_bytes_counters_timestamps_and_normal_report(monkeypatch, tmp_path):
    store = ReviewStore(tmp_path / "records", include_legacy=False)
    record = _legal_record("standard", 7, "修改后可发布", "否", "COMPLETED")
    record.runtime_metadata.elicitation_calls = 2
    record.runtime_metadata.briefing_elicitation_calls = 1
    record.runtime_metadata.context_gap_elicitation_calls = 1
    record.completed_at = record.created_at
    path = store.save(record)
    before_bytes = path.read_bytes()
    before = store.load(record.review_id)
    calls = {"load": 0, "save": 0}

    class ReadOnlyStore:
        def load(self, review_id):
            calls["load"] += 1
            return store.load(review_id)

        def save(self, *args, **kwargs):
            calls["save"] += 1
            raise AssertionError("verification retrieval must not save")

    monkeypatch.setattr(review_module, "ReviewStore", ReadOnlyStore)
    payload = structured_payload(
        review_module.view_review_record.fn(record.review_id, "verification")
    )
    after = store.load(record.review_id)

    assert calls == {"load": 1, "save": 0}
    assert path.read_bytes() == before_bytes
    assert after.created_at == before.created_at
    assert after.completed_at == before.completed_at
    assert after.runtime_metadata.sampling_calls == before.runtime_metadata.sampling_calls == 7
    assert after.runtime_metadata.elicitation_calls == before.runtime_metadata.elicitation_calls == 2
    assert after.display_report == before.display_report
    assert payload["verification_receipt"]["runtime"]["sampling_calls_total"] == 7
    assert payload["verification_receipt"]["runtime"]["elicitation_calls_total"] == 2


def test_actual_verification_tool_bounds_hostile_parent_and_duplicate_roles(monkeypatch):
    path_record = _record()
    path_record.parent_review_id = "C:/PRIVATE_PARENT_SENTINEL"
    duplicate_record = _record()
    duplicate_record.review_id = "20260824T020304000006Z_de34fa56"
    duplicate_record.council_plan.active_role_ids = ["fidelity_reviewer"] * 100
    duplicate_record.independent_reviews = [
        {"agent_name": "fidelity_reviewer", "sample_status": "structured_success"}
    ]
    records = {
        path_record.review_id: path_record,
        duplicate_record.review_id: duplicate_record,
    }

    class FakeStore:
        def load(self, review_id):
            return records[review_id]

    monkeypatch.setattr(review_module, "ReviewStore", FakeStore)

    async def call_both():
        async with Client(mcp) as client:
            return [
                await client.call_tool(
                    "view_review_record",
                    {"review_id": review_id, "detail_level": "verification"},
                )
                for review_id in records
            ]

    results = asyncio.run(call_both())
    path_payload = results[0].structured_content
    duplicate_payload = results[1].structured_content

    assert path_payload["verification_receipt"]["record"]["parent_review_id"] is None
    assert path_payload["verification_receipt"]["availability"]["redacted_fields"] == [
        "record.parent_review_id"
    ]
    assert "PRIVATE_PARENT_SENTINEL" not in str(path_payload)
    assert duplicate_payload["verification_receipt"]["routing"]["active_role_ids"] is None
    assert duplicate_payload["verification_receipt"]["reviewer_execution"]["samples"] is None
    assert {
        "routing.active_role_ids",
        "reviewer_execution.samples",
    } <= set(duplicate_payload["verification_receipt"]["availability"]["redacted_fields"])
    for payload in (path_payload, duplicate_payload):
        assert len(payload["display_report"]) <= 3_200
