#!/usr/bin/env python3
"""Shared effective-Markdown parsing for deterministic evaluation controls."""
from __future__ import annotations

import re

EVAL_HEADING_RE = re.compile(r"^###\s+([A-Z]+)\.\s+", re.MULTILINE)
FENCE_OPEN_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
HTML_COMMENT_RE = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)


def _line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def strip_fenced_code_blocks(text: str) -> str:
    """Blank fenced code while preserving line structure for later Markdown parsing."""
    output: list[str] = []
    fence_char: str | None = None
    fence_len = 0

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if fence_char is None:
            match = FENCE_OPEN_RE.match(body)
            if match:
                fence = match.group("fence")
                info = match.group("info")
                # CommonMark backtick info strings cannot themselves contain backticks.
                if fence.startswith("`") and "`" in info:
                    output.append(line)
                    continue
                fence_char = fence[0]
                fence_len = len(fence)
                output.append(_line_ending(line))
                continue
            output.append(line)
            continue

        closing = re.fullmatch(
            rf" {{0,3}}{re.escape(fence_char)}{{{fence_len},}}[ \t]*",
            body,
        )
        output.append(_line_ending(line))
        if closing:
            fence_char = None
            fence_len = 0

    return "".join(output)


def effective_markdown(text: str) -> str:
    """Return Markdown text that can contribute visible headings/tables to these controls."""
    without_fences = strip_fenced_code_blocks(text)

    def blank_comment(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    return HTML_COMMENT_RE.sub(blank_comment, without_fences)


def parse_eval_ids(text: str) -> list[str]:
    """Return eval IDs from effective Markdown headings, excluding hidden/example content."""
    return EVAL_HEADING_RE.findall(effective_markdown(text))
