"""Security regressions retained after removal of the legacy debate workflow."""

import tempfile
from pathlib import Path

from council_of_translation.localization.persistence import InvalidReviewIdError, ReviewStore
from council_of_translation.security import sanitize_text


def test_text_sanitization():
    assert "\x00" not in sanitize_text("Test\x00with\x00nulls")
    assert "\x01" not in sanitize_text("Test\x01with control")
    truncated = sanitize_text("A" * 10_000, max_length=1_000)
    assert len(truncated) <= 1_020
    assert "truncated" in truncated.lower()
    assert "\n" in sanitize_text("newlines\nand tabs\tare preserved")


def test_review_store_validation():
    """V2 storage rejects traversal before filesystem access."""
    temp_parent = Path(__file__).parents[2] / ".tmp"
    temp_parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temp_parent) as temp_dir:
        root = Path(temp_dir)
        store = ReviewStore(root / "records", legacy_dir=root / "legacy")
        for malicious in ("../../../etc/passwd", "invalid_format", "..%2Freviews%2Fsecret"):
            try:
                store.load(malicious)
                assert False, "Should have raised InvalidReviewIdError"
            except InvalidReviewIdError:
                pass
