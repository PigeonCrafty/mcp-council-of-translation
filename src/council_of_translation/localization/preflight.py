"""Conservative deterministic integrity checks for source/candidate pairs."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import re
from typing import Iterable

from council_of_translation.localization.models import PreflightCheck, PreflightResult


_BRACED = re.compile(r"(?<!\{)\{[A-Za-z_][\w.-]*(?:![rsa])?(?::[^{}]+)?\}(?!\})")
_PRINTF = re.compile(r"%(?!%)(?:\d+\$)?[-+#0 ']*(?:\d+|\*)?(?:\.(?:\d+|\*))?[hlLzjt]*[diuoxXfFeEgGaAcspn]")
_VARIABLE = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}|\$[A-Za-z_][A-Za-z0-9_]*")
_COMMAND = re.compile(r"(?<![\w-])--[a-zA-Z][\w-]*|(?<!\w)/[a-zA-Z][\w-]*(?!\w)")
_URL = re.compile(r"https?://[^\s<>\]\[\"']+")
_NUMBER = re.compile(r"(?<!\w)[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?!\w)")
_VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def _counter(pattern: re.Pattern[str], text: str) -> Counter[str]:
    return Counter(pattern.findall(text))


def _parity_check(
    check_id: str,
    kind: str,
    source_tokens: Counter[str],
    candidate_tokens: Counter[str],
    *,
    blocking: bool = True,
    warning_only: bool = False,
) -> PreflightCheck:
    missing = list((source_tokens - candidate_tokens).elements())
    extra = list((candidate_tokens - source_tokens).elements())
    mismatch = bool(missing or extra)
    status = "warning" if mismatch and warning_only else "fail" if mismatch else "pass"
    return PreflightCheck(
        check_id=check_id,
        kind=kind,
        status=status,
        severity="major" if warning_only else "critical" if mismatch else "minor",
        source_evidence=missing,
        candidate_evidence=extra,
        blocking=bool(mismatch and blocking and not warning_only),
        message=(f"missing={missing}; extra={extra}" if mismatch else "token parity preserved"),
    )


class _TagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.stack: list[str] = []
        self.tags: Counter[str] = Counter()
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        self.tags[normalized] += 1
        if normalized not in _VOID_TAGS:
            self.stack.append(normalized)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags[tag.lower()] += 1

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        if not self.stack or self.stack[-1] != normalized:
            self.errors.append(f"unexpected closing tag </{normalized}>")
            return
        self.stack.pop()

    def finish(self) -> None:
        self.errors.extend(f"unclosed tag <{tag}>" for tag in reversed(self.stack))


def _parse_tags(text: str) -> _TagParser:
    parser = _TagParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # HTMLParser may reject malformed declarations.
        parser.errors.append(f"tag parse error: {type(exc).__name__}")
    parser.finish()
    return parser


def _tag_check(source: str, candidate: str) -> PreflightCheck:
    source_tags = _parse_tags(source)
    candidate_tags = _parse_tags(candidate)
    missing = list((source_tags.tags - candidate_tags.tags).elements())
    extra = list((candidate_tags.tags - source_tags.tags).elements())
    mismatch = bool(missing or extra or candidate_tags.errors)
    return PreflightCheck(
        check_id="tag-integrity",
        kind="tag_integrity",
        status="fail" if mismatch else "pass",
        severity="critical" if mismatch else "minor",
        source_evidence=[*(f"required tag <{tag}>" for tag in missing), *source_tags.errors],
        candidate_evidence=[*(f"extra tag <{tag}>" for tag in extra), *candidate_tags.errors],
        blocking=mismatch,
        message="required-tag parity and candidate tag balance" if not mismatch else "tag structure is not preserved",
    )


def _markdown_signature(text: str) -> Counter[str]:
    signature: Counter[str] = Counter()
    signature["fence"] = len(re.findall(r"(?m)^\s*```", text))
    signature["heading"] = len(re.findall(r"(?m)^\s{0,3}#{1,6}\s", text))
    signature["link"] = len(re.findall(r"\[[^\]]+\]\([^)]+\)", text))
    signature["list"] = len(re.findall(r"(?m)^\s*(?:[-*+] |\d+[.)] )", text))
    return signature


def run_preflight(
    source_text: str,
    candidate_translation: str,
    *,
    do_not_translate: Iterable[str] = (),
    hard_constraints: Iterable[str] = (),
) -> PreflightResult:
    """Run only deterministic checks over caller-supplied inputs.

    `hard_constraints` may promote numeric or Markdown parity, require an exact
    candidate literal with ``required_literal:<text>``, or prohibit one with
    ``forbidden_literal:<text>``. Other free-form entries remain reviewer
    context and cannot become deterministic blockers.
    """
    constraint_values = [str(item) for item in hard_constraints]
    hard = set(constraint_values)
    checks = [
        _parity_check("braced-placeholder-parity", "placeholder_parity", _counter(_BRACED, source_text), _counter(_BRACED, candidate_translation)),
        _parity_check("printf-placeholder-parity", "printf_placeholder_parity", _counter(_PRINTF, source_text), _counter(_PRINTF, candidate_translation)),
        _parity_check("variable-parity", "variable_token_parity", _counter(_VARIABLE, source_text), _counter(_VARIABLE, candidate_translation)),
        _parity_check("command-parity", "command_token_parity", _counter(_COMMAND, source_text), _counter(_COMMAND, candidate_translation)),
        _tag_check(source_text, candidate_translation),
        _parity_check("url-parity", "url_preservation", _counter(_URL, source_text), _counter(_URL, candidate_translation)),
    ]

    dnt_values = [literal for literal in dict.fromkeys(str(item) for item in do_not_translate) if literal]
    missing_dnt = [literal for literal in dnt_values if literal in source_text and literal not in candidate_translation]
    checks.append(
        PreflightCheck(
            check_id="explicit-dnt-preservation",
            kind="do_not_translate_preservation",
            status="fail" if missing_dnt else "pass",
            severity="critical" if missing_dnt else "minor",
            source_evidence=missing_dnt,
            candidate_evidence=[],
            blocking=bool(missing_dnt),
            message="explicit caller-provided literals preserved" if not missing_dnt else "explicit do-not-translate literal missing",
        )
    )

    for index, constraint in enumerate(constraint_values, start=1):
        prefix, separator, literal = str(constraint).partition(":")
        if not separator or not literal or prefix not in {"required_literal", "forbidden_literal"}:
            continue
        present = literal in candidate_translation
        violation = not present if prefix == "required_literal" else present
        checks.append(
            PreflightCheck(
                check_id=f"explicit-{prefix.replace('_', '-')}-{index}",
                kind="explicit_hard_constraint",
                status="fail" if violation else "pass",
                severity="critical" if violation else "minor",
                source_evidence=[str(constraint)],
                candidate_evidence=[literal] if present else [],
                blocking=violation,
                message="explicit caller hard constraint violated" if violation else "explicit caller hard constraint satisfied",
            )
        )

    numeric_hard = "numeric_parity" in hard
    checks.append(
        _parity_check(
            "numeric-parity",
            "numeric_signal",
            _counter(_NUMBER, source_text),
            _counter(_NUMBER, candidate_translation),
            blocking=numeric_hard,
            warning_only=not numeric_hard,
        )
    )
    markdown_hard = "markdown_parity" in hard
    checks.append(
        _parity_check(
            "markdown-structure",
            "markdown_signal",
            _markdown_signature(source_text),
            _markdown_signature(candidate_translation),
            blocking=markdown_hard,
            warning_only=not markdown_hard,
        )
    )
    return PreflightResult(checks=checks)
