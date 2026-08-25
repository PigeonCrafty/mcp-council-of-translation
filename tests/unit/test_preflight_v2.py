import pytest

from council_of_translation.localization.preflight import run_preflight


@pytest.mark.parametrize(
    ("source", "candidate", "kind"),
    [
        ("Delete {count} files", "删除文件", "placeholder_parity"),
        ("Saved %2$s: %d", "已保存 %2$s", "printf_placeholder_parity"),
        ("Run $APP --force", "运行应用", "variable_token_parity"),
        ("Run /help", "运行帮助", "command_token_parity"),
        ("See https://example.com/a", "请查看网站", "url_preservation"),
    ],
)
def test_high_confidence_integrity_mismatches_block(source, candidate, kind):
    result = run_preflight(source, candidate)
    check = next(item for item in result.checks if item.kind == kind)
    assert check.status == "fail"
    assert check.blocking is True
    assert result.blocking is True


def test_tag_balance_and_required_tag_parity_block():
    result = run_preflight("Click <strong>Save</strong>", "点击 <strong>保存")
    check = next(item for item in result.checks if item.kind == "tag_integrity")
    assert check.status == "fail"
    assert check.blocking is True


def test_void_tag_and_translated_text_do_not_false_positive():
    result = run_preflight("Line<br>Next", "第一行<br>下一行")
    check = next(item for item in result.checks if item.kind == "tag_integrity")
    assert check.status == "pass"
    assert check.blocking is False


def test_only_explicit_dnt_literals_are_enforced():
    result = run_preflight("Open Pigeon mode", "打开模式", do_not_translate=["Pigeon"])
    check = next(item for item in result.checks if item.kind == "do_not_translate_preservation")
    assert check.blocking is True

    generic = run_preflight("Open Pigeon mode", "打开模式")
    generic_check = next(item for item in generic.checks if item.kind == "do_not_translate_preservation")
    assert generic_check.status == "pass"


def test_numbers_and_markdown_are_warnings_by_default():
    result = run_preflight("# Delete 3 files", "删除文件")
    relevant = [item for item in result.checks if item.kind in {"numeric_signal", "markdown_signal"}]
    assert {item.status for item in relevant} == {"warning"}
    assert all(item.blocking is False for item in relevant)
    assert result.blocking is False


def test_explicit_project_constraint_can_promote_numeric_parity():
    result = run_preflight("Delete 3 files", "删除文件", hard_constraints=["numeric_parity"])
    check = next(item for item in result.checks if item.kind == "numeric_signal")
    assert check.status == "fail"
    assert check.blocking is True


def test_explicit_literal_hard_constraints_are_deterministic():
    result = run_preflight(
        "Click Acme",
        "点击示例公司 beta",
        hard_constraints=["required_literal:Acme", "forbidden_literal:beta", "free-form advice"],
    )
    hard_checks = [item for item in result.checks if item.kind == "explicit_hard_constraint"]
    assert len(hard_checks) == 2
    assert all(item.blocking for item in hard_checks)
    assert "free-form advice" not in {evidence for item in hard_checks for evidence in item.source_evidence}


def test_equal_duplicate_placeholders_pass():
    result = run_preflight("{name}: {count} / {count}", "{name}：{count} / {count}")
    check = next(item for item in result.checks if item.kind == "placeholder_parity")
    assert check.status == "pass"
    assert check.blocking is False


@pytest.mark.parametrize(
    ("source", "candidate"),
    [
        ("100% safe", "100% 安全"),
        ("50% discount", "五折优惠"),
        ("25% off", "七五折"),
        ("100% satisfied", "完全满意"),
        ("Value: % s", "值"),
        ("Value: % d", "值"),
        ("Value: % o", "值"),
    ],
)
def test_percentage_prose_is_not_a_printf_placeholder(source, candidate):
    result = run_preflight(source, candidate)
    check = next(item for item in result.checks if item.kind == "printf_placeholder_parity")
    assert check.status == "pass"
    assert check.blocking is False
    assert result.blocking is False


@pytest.mark.parametrize("punctuation", list(".,;:!?。，；：！？"))
def test_sentence_final_url_punctuation_is_not_part_of_identity(punctuation):
    result = run_preflight(
        f"See https://example.com/a{punctuation}",
        "请查看 https://example.com/a",
    )
    check = next(item for item in result.checks if item.kind == "url_preservation")
    assert check.status == "pass"
    assert check.blocking is False
    assert result.blocking is False


@pytest.mark.parametrize(
    ("source", "candidate"),
    [
        ("See (https://example.com/a).", "请查看 https://example.com/a"),
        ("See [https://example.com/a],", "请查看 https://example.com/a"),
        ("请查看（https://example.com/a）。", "请查看 https://example.com/a"),
        ("请查看【https://example.com/a】，", "请查看 https://example.com/a"),
        ("请查看《https://example.com/a》！", "请查看 https://example.com/a"),
        ("请查看「https://example.com/a」？", "请查看 https://example.com/a"),
    ],
)
def test_closing_punctuation_around_url_is_not_part_of_identity(source, candidate):
    result = run_preflight(source, candidate)
    check = next(item for item in result.checks if item.kind == "url_preservation")
    assert check.status == "pass"
    assert check.blocking is False
    assert result.blocking is False


def test_balanced_url_internal_syntax_is_preserved():
    result = run_preflight(
        "See https://example.com/search?q=(term)",
        "请查看 https://example.com/search?q=(term",
    )
    check = next(item for item in result.checks if item.kind == "url_preservation")
    assert check.status == "fail"
    assert check.blocking is True
    assert check.source_evidence == ["https://example.com/search?q=(term)"]


@pytest.mark.parametrize("token", ["%s", "%d", "%2$s", "%02d", "%.2f", "%%", "% 5d"])
def test_unambiguous_printf_tokens_remain_protected(token):
    result = run_preflight(f"Value: {token}", "值")
    check = next(item for item in result.checks if item.kind == "printf_placeholder_parity")
    assert check.status == "fail"
    assert check.blocking is True
    assert check.source_evidence == [token]


@pytest.mark.parametrize(
    ("source", "candidate", "kind", "kwargs"),
    [
        ("Hello {name}", "你好", "placeholder_parity", {}),
        ("Run ${APP}", "运行应用", "variable_token_parity", {}),
        ("Run /help", "运行帮助", "command_token_parity", {}),
        ("Run --force", "运行", "command_token_parity", {}),
        ("Click <strong>Save</strong>", "点击保存", "tag_integrity", {}),
        ("Open Acme", "打开", "do_not_translate_preservation", {"do_not_translate": ["Acme"]}),
        ("Open Acme", "打开", "explicit_hard_constraint", {"hard_constraints": ["required_literal:Acme"]}),
        ("Open", "打开 beta", "explicit_hard_constraint", {"hard_constraints": ["forbidden_literal:beta"]}),
    ],
)
def test_existing_deterministic_protected_token_corpus_still_blocks(
    source, candidate, kind, kwargs
):
    result = run_preflight(source, candidate, **kwargs)
    checks = [item for item in result.checks if item.kind == kind]
    assert any(item.status == "fail" and item.blocking for item in checks)
    assert result.blocking is True
