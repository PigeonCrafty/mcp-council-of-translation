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


def test_equal_duplicate_placeholders_pass():
    result = run_preflight("{name}: {count} / {count}", "{name}：{count} / {count}")
    check = next(item for item in result.checks if item.kind == "placeholder_parity")
    assert check.status == "pass"
    assert check.blocking is False
