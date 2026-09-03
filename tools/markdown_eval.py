#!/usr/bin/env python3
"""Shared bounded GFM block parsing for deterministic evaluation controls."""
from __future__ import annotations

import re

EVAL_HEADING_RE = re.compile(r"^ {0,3}###[ \t]+([A-Z]+)\.[ \t]+[^ \t\r\n]", re.MULTILINE)
FENCE_OPEN_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
HTML_TYPE1_RE = re.compile(r"^(?:script|pre|style)(?=[\t >]|$)", re.IGNORECASE)
HTML_TYPE1_END_RE = re.compile(r"</(?:script|pre|style)>", re.IGNORECASE)
HTML_BLOCK_TAGS = (
    "address", "article", "aside", "base", "basefont", "blockquote", "body", "caption",
    "center", "col", "colgroup", "dd", "details", "dialog", "dir", "div", "dl", "dt",
    "fieldset", "figcaption", "figure", "footer", "form", "frame", "frameset", "h1", "h2",
    "h3", "h4", "h5", "h6", "head", "header", "hr", "html", "iframe", "legend", "li",
    "link", "main", "menu", "menuitem", "nav", "noframes", "ol", "optgroup", "option", "p",
    "param", "section", "source", "summary", "table", "tbody", "td", "tfoot", "th", "thead",
    "title", "tr", "track", "ul",
)
HTML_TYPE6_RE = re.compile(
    rf"^/?(?:{'|'.join(HTML_BLOCK_TAGS)})(?=[\t />]|$)",
    re.IGNORECASE,
)
HTML_TAG_LIKE_RE = re.compile(r"^/?[A-Za-z][A-Za-z0-9-]*(?=[\t />])")


def _line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def _content_after_indent(body: str) -> str | None:
    """Return content after 0-3 spaces; four-space indentation is code, not a block start."""
    indent = len(body) - len(body.lstrip(" "))
    if indent > 3:
        return None
    return body[indent:]


def _raw_html_start(content: str) -> tuple[str, re.Pattern[str] | None] | None:
    """Classify supported GFM raw-HTML block starts; unknown tag-like starts fail closed."""
    if HTML_TYPE1_RE.match(content[1:]) if content.startswith("<") else False:
        return "until_match", HTML_TYPE1_END_RE
    if content.startswith("<?"):
        return "until_match", re.compile(r"\?>")
    if re.match(r"<![A-Z]", content):
        return "until_match", re.compile(r">")
    if content.startswith("<![CDATA["):
        return "until_match", re.compile(r"\]\]>")
    if content.startswith("<") and HTML_TYPE6_RE.match(content[1:]):
        return "until_blank", None
    if content.startswith("<") and HTML_TAG_LIKE_RE.match(content[1:]):
        raise ValueError(
            "Raw HTML-like tag syntax is unsupported in references/eval-scenarios.md; "
            "use Markdown/plain text so eval-control parsing remains deterministic"
        )
    return None


def effective_markdown(text: str) -> str:
    """Blank non-Markdown GFM blocks while preserving visible line structure.

    This is intentionally bounded to the eval-control surface. It handles HTML comments,
    fenced code, GFM raw-HTML block types 1/3/4/5/6, and fails closed on other tag-like
    starts rather than pretending to implement a general-purpose Markdown renderer.
    """
    output: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    html_mode: str | None = None
    html_end_re: re.Pattern[str] | None = None

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        ending = _line_ending(line)

        if fence_char is not None:
            closing = re.fullmatch(
                rf" {{0,3}}{re.escape(fence_char)}{{{fence_len},}}[ \t]*",
                body,
            )
            output.append(ending)
            if closing:
                fence_char = None
                fence_len = 0
            continue

        if html_mode == "comment":
            output.append(ending)
            if "-->" in body:
                html_mode = None
            continue

        if html_mode == "until_match":
            output.append(ending)
            if html_end_re is not None and html_end_re.search(body):
                html_mode = None
                html_end_re = None
            continue

        if html_mode == "until_blank":
            if not body.strip():
                html_mode = None
                output.append(line)
            else:
                output.append(ending)
            continue

        content = _content_after_indent(body)
        if content is not None and content.startswith("<!--"):
            output.append(ending)
            if "-->" not in content[4:]:
                html_mode = "comment"
            continue

        match = FENCE_OPEN_RE.match(body)
        if match:
            fence = match.group("fence")
            info = match.group("info")
            # GFM/CommonMark backtick info strings cannot themselves contain backticks.
            if not (fence.startswith("`") and "`" in info):
                fence_char = fence[0]
                fence_len = len(fence)
                output.append(ending)
                continue

        if content is not None:
            raw_html = _raw_html_start(content)
            if raw_html is not None:
                html_mode, html_end_re = raw_html
                output.append(ending)
                if html_mode == "until_match" and html_end_re is not None and html_end_re.search(content):
                    html_mode = None
                    html_end_re = None
                continue

        output.append(line)

    return "".join(output)


def parse_eval_ids(text: str) -> list[str]:
    """Return eval IDs from effective top-level ATX headings."""
    return EVAL_HEADING_RE.findall(effective_markdown(text))
