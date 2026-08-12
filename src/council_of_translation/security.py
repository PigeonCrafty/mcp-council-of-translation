"""Input normalization shared by the V0.5 public tool boundary."""

from __future__ import annotations


def sanitize_text(text: str, max_length: int = 5_000) -> str:
    """Remove control bytes and cap untrusted text without interpreting it."""
    if not isinstance(text, str):
        return ""
    cleaned = "".join(character for character in text if character.isprintable() or character in "\n\r\t")
    cleaned = cleaned.replace("\x00", "")
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "... [truncated]"
    return cleaned.strip()
