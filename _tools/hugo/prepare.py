#!/usr/bin/env python3
"""Rewrite the CI-generated documentation pages for Hugo.

The GitLab CI job "Update the docs" commits the language documentation to
pages/docs/** in kramdown syntax (3300+ grammar, features and client-binding
pages) and a second script commits pages/docs/platform/<version>/release-notes.md
with the same front matter. Those files are written by a machine and are never
edited in this repository, so Hugo cannot be satisfied by changing them. This
script reads them and writes a rewritten mirror to .build/content/pages/docs,
which hugo.toml mounts over the content directory.

What changes, and why:

  1. The table of contents marker (`1. TOC` followed by `{:toc}`) is removed.
     kramdown expanded it to <ol id="markdown-toc">; the Hugo layout builds the
     list from the page's headings, so the marker must not render as a list.

  2. A `{: #ID }` line after a blank line and before a line that starts with
     `<div ` becomes an id attribute, written first, on that div. The generator
     emits this for every grammar rule (27921 times, always on the div that
     wraps the highlighted rule). kramdown attached the id to the div; Goldmark
     has no such line syntax, so the id moves into the tag itself.

  3. A `{: #ID }` line directly after a paragraph line and before a ``` fence
     is written as `{#ID}` on the same line. kramdown attached the id to the
     paragraph before it (<p id="ID">) and rendered the fence normally;
     Goldmark applies an attribute line placed right after a paragraph to that
     paragraph, so the result is the same. Occurs 24 times, always
     `{: #example--sibling-recursion }` in the model grammar pages.

  4. A fence opened on a blockquote line (`> ```js`) whose content and closing
     fence lines carry no `>` is completed: the lines up to and including the
     closing fence get the `> ` prefix. kramdown treats the unprefixed lines as
     lazy continuation of the blockquote, so the fence closes where its closing
     line is. CommonMark, and so Goldmark, ends the blockquote at the first line
     without `>`, which turns the closing fence into an opening one and makes
     the rest of the page code. Occurs in 41 pages, always one line of content:
     the "minimal implementation" example of the provided interface
     implementation grammar.

  5. A fence opener with a stray backtick after its info string (```js`) loses
     the backtick. kramdown reads the info string as `js``, renders a plain
     code block and closes at the next fence line. CommonMark does not accept a
     backtick in the info string of a backtick fence, so the line becomes text
     and the closing line (four backticks) opens a fence that swallows the rest
     of the page. Occurs once, in the model 89 grammar. The code block keeps its
     text; it gets the js class like the other examples.

  6. A blank line is added after a generated rule block (`</pre>`, `</div>`,
     `</div>`) when text follows it directly. kramdown ends a raw HTML block at
     its closing tag and parses the next line as markdown; CommonMark ends it at
     the next blank line, so a heading, paragraph or fence right after the block
     (3482 times in 620 pages) would be swallowed as raw HTML. A block followed
     by a blank line or by another tag is left alone.

  7. In a generated rule block, a `<` that a browser would read as markup but
     that is text is written as `&lt;`: `<!` (including `<!--`: a comment would
     hide the rest of the block), `<?`, and `</` that is not followed by one of
     the tag names the generator writes in a block (span, a, div, pre, code).
     The grammar operators `<!` and `</` of the datastore migration and
     relational database grammars are written that way. kramdown escaped them
     while it copied the block; Goldmark copies the block verbatim, and a
     browser reads `<!</span>` as a comment that swallows the closing tag, so
     the operator would disappear. Other `<` stay as they are: kramdown copied
     tags such as `<begin>` verbatim as well.

  8. An inline link destination that contains a space is wrapped in angle
     brackets: `[client bindings](../client bindings/client_bindings.html)`.
     kramdown accepts the space, CommonMark does not and shows the link as text.
     Occurs 334 times, always this destination, in the webclient widget pages.
     Text inside a code span that looks like a link is not a link and is left
     alone.

  9. In prose, a straight single quote that opens a quoted word or phrase
     becomes U+2018 and the one that closes it U+2019, the way kramdown's smart
     quotes wrote them. Goldmark's typographer decides by the word that follows
     and writes `'empty'` with two right quotes. An opening quote follows the
     start of a line, a space, `(`, `[`, `{`, or `*` or `_` (an emphasis that
     starts with the quote, `*'empty'*`) and precedes a non-space; a closing
     quote follows a non-space and precedes a space, punctuation or the end of
     the line. A quote before two digits and an s (`'90s`) is an apostrophe,
     U+2019, wherever it stands: kramdown has that case first, and not any quote
     before a digit, so `'5'` stays a quoted number. A quote after `/` is a
     closing quote in kramdown (a non-space before it), so it is written U+2019
     even before a word. Apostrophes inside words are left to Goldmark, which writes them
     as kramdown did. Code spans, inline <code>, <kbd>, <samp> and <pre>
     elements, HTML tags, fences, indented code, raw HTML blocks and link
     destinations are not prose and stay as they are.

 10. Any other line that starts with `{:` is an error, and so is a line that
     starts with `{.` or `{#`, outside fences and raw HTML (a rule block or an
     HTML block). The generator emits exactly the forms above; a new form must
     be noticed and handled here instead of leaking into the site as visible
     text. Goldmark would read a `{.` or `{#` line as a block attribute, apply
     it to the block before it and not show it.

 11. The front matter gets `toc: true` on every page whose table of contents
     marker was removed. Jekyll gave a page an index only when it had the marker
     (the 31 release notes have headings and no index), and the layouts build
     the index from this key.

 12. The front matter gets `url: "/pages/docs/<path without .md>.html"`. Jekyll
     wrote every page to that path (it keeps the spaces of directory names such
     as "client bindings"), and the toolchains deep-link to it, so Hugo must write
     the same file.

 13. Not a page: .build/data/key_order.json records the order of the keys that
     the version files list. Hugo's data loader gives a JSON object as a map,
     which Go templates range over in sorted key order, but the tables list
     components in the order of the file. The file has the shape
       {"platform": {"<platform version>": [keys of its "platform" object]},
        "system types": {"<dist directory>": [keys of "system types"]}}
     The first map comes from _data/versions.json, the second from every
     _data/dist/<version>/versions.json; a version without a dist file is not in
     the second map. The keys are in the order of the file (json keeps it). The
     data mount of hugo.toml takes .build/data.

Everything else is copied byte for byte. The content of fenced code blocks is
never touched (rules 4 and 5 only repair fence lines). The result depends only
on the input files: running the script twice gives the same tree.

The rewrites of a page are collected as byte ranges of the source and applied in
one pass over the sorted ranges. At one offset an insertion goes before a
replacement or deletion that starts there (a blank line inserted where a `1. TOC`
marker, which is removed, begins), and two ranges that overlap are an error, not
a guess.

Rules 4 to 9 exist because kramdown and Goldmark read the same generated text
differently. They were found by rendering the whole prepared tree with Hugo and
comparing it with the Jekyll output page by page; a new kind of difference
is not found here. check-output.sh catches leftover syntax in a built page, and
the output of the generator must be checked when it changes.

Usage:
    python3 _tools/hugo/prepare.py [--check] [--root REPOSITORY_ROOT]

With --check the rewrite runs in memory and only the counters are printed, so
CI logs show what the generator emitted without writing anything.
"""

import argparse
import json
import os
import re
import shutil
import sys
import time

SOURCE = "pages/docs"
DEST = ".build/content/pages/docs"
DATA_DEST = ".build/data"
URL_PREFIX = "/pages/docs/"

# The two lines kramdown turns into a table of contents. The blank lines between
# them are removed with them; the blank lines around the pair stay.
TOC = re.compile(rb"^1\. TOC[ \t]*\n(?:[ \t]*\n)*\{:toc\}[ \t]*(?:\n|\Z)", re.M)

# Every line that starts a kramdown attribute list ({:) or reads as a Goldmark block attribute
# ({. and {#). Lines inside fences are excluded by position, see fenced_ranges().
IAL_LINE = re.compile(rb"^[ \t]*\{[:.#][^\n]*$", re.M)

# The one attribute form the generator emits. The id alphabet is what the
# generator can produce and what is safe inside an HTML attribute and inside a
# Goldmark attribute block without quoting.
IAL_ID = re.compile(rb"^\{:[ \t]*#([A-Za-z0-9_.-]+)[ \t]*\}[ \t]*$")

FRONT_MATTER_END = re.compile(rb"\n---[ \t]*\n")

FENCE_LINE = re.compile(rb"^ {0,3}(`{3,}|~{3,})([^\n]*)$", re.M)

# The end of a generated rule block, followed directly by something that is not a
# blank line and not a tag. The blocks contain no blank lines (checked on the whole
# tree), so the block ends at this match.
BLOCK_END_BEFORE_TEXT = re.compile(rb"^</pre>\n</div>\n</div>\n(?=[^\n<])", re.M)

# A whole generated rule block, from its first line to the last of the three closing lines.
RULE_BLOCK = re.compile(rb'^<div class="language-js highlighter-rouge">\n.*?^</pre>\n</div>\n</div>$', re.M | re.S)

# A `<` that is text in a rule block but that a browser reads as markup: a declaration, comment or
# processing instruction opener, or an end tag that is not one the generator writes.
BLOCK_MARKUP_TEXT = re.compile(rb"<(?=!|\?|/(?!(?:span|a|div|pre|code)\s*>))")

# An inline link destination with a space and no title: `](a b/c.html)`.
LINK_WITH_SPACE = re.compile(rb"\]\(([^()<>\"'\s][^()<>\"'\n]* [^()<>\"'\n]*)\)")

# A code span: a backtick run closed by a run of the same length.
CODE_SPAN = re.compile(rb"(?<!`)(?P<run>`+)(?!`).+?(?<!`)(?P=run)(?!`)", re.S)

# Inline constructs where a straight quote is not prose: a code span (a backtick run closed by a
# run of the same length), an HTML tag or autolink, a link destination. Everything else is text.
INLINE_NOT_PROSE = re.compile(
    CODE_SPAN.pattern
    + rb"|<(?P<element>code|kbd|samp|pre)(?:[ \t][^<>]*)?>.*?</(?P=element)>"
    rb"|<[A-Za-z/!][^<>]*>"
    rb"|\]\([^)\n]*\)",
    re.S | re.I,
)
SINGLE_QUOTE = re.compile(rb"'")
HTML_BLOCK_START = re.compile(
    rb"^ {0,3}(?:<!--|</?(?:address|article|aside|blockquote|body|caption|center|dd|details|dialog|dir|div|dl|dt"
    rb"|fieldset|figcaption|figure|footer|form|h[1-6]|header|hr|html|li|main|menu|nav|ol|p|pre|script|section"
    rb"|style|summary|table|tbody|td|tfoot|th|thead|tr|ul)(?:[ \t]|/?>|$))"
)
LIST_ITEM = re.compile(rb"^ {0,3}(?:[-*+]|[0-9]+[.)])(?:[ \t]|$)")
OPENING_AFTER = b" \t\n([{*_"
DECADE = re.compile(rb"'(?=[0-9]{2}s)")
CLOSING_BEFORE = b" \t\n.,;:!?)]}/-*_\"'"

# A backtick fence opener whose info string ends in backticks, which CommonMark rejects.
STRAY_BACKTICK_OPENER = re.compile(rb"^( {0,3}`{3,}[^\s`]+)`+([ \t]*)$", re.M)

# A fence opened on a blockquote line. The prefix group is reused for the lines
# that lack it.
BLOCKQUOTE_PREFIX = re.compile(rb" {0,3}>[ ]?")
BLOCKQUOTE_FENCE = re.compile(rb"^( {0,3}>[ ]?)(`{3,}|~{3,})([^\n]*)$", re.M)

# A line that cannot be the text of a paragraph: it is indented as code or
# starts another block (heading, quote, HTML, table, fence, list item, rule,
# attribute list).
NOT_PARAGRAPH = re.compile(
    rb"^(?: {4}|\t| {0,3}(?:#{1,6}(?:[ \t]|$)|>|<|\||`{3}|~{3}|\{|[-*+](?:[ \t]|$)"
    rb"|[0-9]+[.)](?:[ \t]|$)|-{3,}|={3,}|\*{3,}|_{3,}))"
)

COUNTER_LABELS = [
    ("files", "markdown files read"),
    ("written", "markdown files written"),
    ("skipped", "non-markdown files skipped"),
    ("quote_open", "single quotes written as U+2018 (opening, in prose)"),
    ("quote_close", "single quotes written as U+2019 (closing, in prose)"),
    ("escaped_lt", "< escaped in rule blocks (<!, <?, </ that closes no tag of the block)"),
    ("link_spaces", "link destinations with a space wrapped in <>"),
    ("stray_backtick", "fence openers cleaned of a stray backtick after the info string"),
    ("blockquote_fences", "blockquote fences completed with the > prefix"),
    ("block_breaks", "blank lines added after a rule block followed by text"),
    ("toc", "table of contents markers removed (1. TOC + {:toc})"),
    ("div_ids", "ids moved onto <div class=\"language-js highlighter-rouge\">"),
    ("paragraph_ids", "ids moved onto a paragraph before a fence ({#ID})"),
    ("fenced_ial", "attribute lines inside fences left as they are"),
    ("urls", "url added to front matter"),
    ("toc_pages", "toc: true added to front matter (pages that had the marker)"),
    ("key_order_platform", "key_order.json: platform versions"),
    ("key_order_types", "key_order.json: system type lists"),
]


class Failure(Exception):
    pass


def fenced_ranges(body):
    """Return (start, end) byte ranges of fenced code blocks, fence lines included.

    CommonMark rules: an opening fence is at least three backticks or tildes with
    at most three spaces of indentation; a backtick fence's info string cannot
    contain a backtick; the closing fence uses the same character, is at least as
    long and carries nothing after it. An unclosed fence runs to the end of the
    file in CommonMark; it is returned as the second value so the caller can
    report it: it swallows the rest of the page, which kramdown may not do.
    """
    ranges = []
    open_start = None
    open_char = None
    open_len = 0
    for m in FENCE_LINE.finditer(body):
        marker = m.group(1)
        rest = m.group(2)
        if open_start is None:
            if marker[:1] == b"`" and b"`" in rest:
                continue
            open_start = m.start()
            open_char = marker[:1]
            open_len = len(marker)
        elif marker[:1] == open_char and len(marker) >= open_len and not rest.strip():
            ranges.append((open_start, m.end()))
            open_start = None
    if open_start is not None:
        ranges.append((open_start, len(body)))
    return ranges, open_start


def in_ranges(ranges, position):
    # Few ranges per file; a linear scan is fine, and the candidates come in order.
    for start, end in ranges:
        if start <= position < end:
            return True
        if start > position:
            return False
    return False


def complete_blockquote_fences(body, name, line_base, counters, errors):
    """Prefix the unprefixed lines of a fence that opens on a blockquote line.

    Only the shape seen in the generated pages is accepted: no blank line between
    the opening and the closing fence. Anything else is reported, not guessed.
    """
    edits = []  # (offset of a line to prefix, prefix)
    position = 0
    for m in BLOCKQUOTE_FENCE.finditer(body):
        if m.start() < position:
            continue
        prefix, marker, info = m.group(1), m.group(2), m.group(3)
        if marker[:1] == b"`" and b"`" in info:
            continue  # not a fence, the info string of a backtick fence has no backtick
        unprefixed = []
        closed_at = None
        cursor = m.end() + 1
        while cursor < len(body):
            line_end = body.find(b"\n", cursor)
            if line_end < 0:
                line_end = len(body)
            line = body[cursor:line_end]
            if not line.strip():
                break
            quote = BLOCKQUOTE_PREFIX.match(line)
            if not quote:
                unprefixed.append(cursor)
            content = (line[quote.end() :] if quote else line).strip()
            if content and not content.strip(marker[:1]) and len(content) >= len(marker):
                closed_at = line_end
                break
            cursor = line_end + 1
        if closed_at is None:
            errors.append(
                "%s:%d: fence opened on a blockquote line is not closed before a blank line: %s"
                % (name, line_base + body.count(b"\n", 0, m.start()) + 1, m.group(0).decode("utf-8", "replace"))
            )
            continue
        position = closed_at
        if unprefixed:
            edits.extend((offset, prefix) for offset in unprefixed)
            counters["blockquote_fences"] += 1
    if not edits:
        return body
    pieces = []
    last = 0
    for offset, prefix in edits:
        pieces.append(body[last:offset])
        pieces.append(prefix)
        last = offset
    pieces.append(body[last:])
    return b"".join(pieces)


def in_html_block(body, position):
    """Whether a position of the body lies in a raw HTML block: one that starts at a line that
    opens a block level element and runs to the next blank line."""
    found = body.rfind(b"\n\n", 0, position)
    start = found + 2 if found >= 0 else 0
    end = body.find(b"\n", start)
    return bool(HTML_BLOCK_START.match(body[start : end if end >= 0 else len(body)]))


def in_code_span(body, position):
    """Whether a position of the body lies in a code span of its paragraph."""
    start = body.rfind(b"\n\n", 0, position) + 1
    end = body.find(b"\n\n", position)
    paragraph = body[start : end if end >= 0 else len(body)]
    return any(m.start() <= position - start < m.end() for m in CODE_SPAN.finditer(paragraph))


def curl_single_quotes(body, fences, blocks, counters):
    """Return edits that write the quotes of quoted words in prose as U+2018 and U+2019."""
    edits = []
    chunk_start = 0
    chunk_lines = []

    def flush():
        if not chunk_lines:
            return
        text = b"\n".join(chunk_lines)
        spans = []
        if b"`" in text or b"<" in text or b"](" in text:
            spans = [(m.start(), m.end()) for m in INLINE_NOT_PROSE.finditer(text)]
        for m in SINGLE_QUOTE.finditer(text):
            i = m.start()
            if in_ranges(spans, i):
                continue
            before = text[i - 1 : i] if i else b"\n"
            after = text[i + 1 : i + 2] or b"\n"
            if before == b"\\":
                continue
            curly_open = text[max(0, i - 3) : i] in ("\u201c".encode(), "\u2018".encode())
            if DECADE.match(text, i):
                edits.append((chunk_start + i, chunk_start + i + 1, "\u2019".encode()))
                counters["quote_close"] += 1
            elif (before in OPENING_AFTER or curly_open) and after not in b" \t\n":
                edits.append((chunk_start + i, chunk_start + i + 1, "\u2018".encode()))
                counters["quote_open"] += 1
            elif before not in b" \t\n" and (after in CLOSING_BEFORE or before == b"/"):
                edits.append((chunk_start + i, chunk_start + i + 1, "\u2019".encode()))
                counters["quote_close"] += 1
        chunk_lines.clear()

    masked = sorted(fences + blocks)
    next_masked = 0
    position = 0
    in_html = False
    in_list = False
    previous_blank = True
    for line in body.split(b"\n"):
        start = position
        position += len(line) + 1
        while next_masked < len(masked) and masked[next_masked][1] <= start:
            next_masked += 1
        in_code = next_masked < len(masked) and masked[next_masked][0] <= start
        blank = not line.strip()
        prose = True
        if blank:
            in_html = False
            prose = False
        elif in_code:
            prose = False
        elif in_html:
            prose = False
        elif HTML_BLOCK_START.match(line):
            in_html = True
            prose = False
        elif line[:1] == b"\t" or line[:4] == b"    ":
            # a list continuation or the lazy line of a paragraph is prose, other indented text is code
            prose = in_list or not previous_blank
        else:
            in_list = bool(LIST_ITEM.match(line))
        previous_blank = blank
        if prose:
            if not chunk_lines:
                chunk_start = start
            chunk_lines.append(line)
        else:
            flush()
    flush()
    return edits


def split_front_matter(data, name):
    """Return the front matter lines, its closing line and the body."""
    if not data.startswith(b"---\n"):
        raise Failure("%s:1: no front matter" % name)
    m = FRONT_MATTER_END.search(data, 3)
    if not m:
        raise Failure("%s: front matter is not closed" % name)
    front = data[: m.start() + 1]
    if re.search(rb"^url:", front, re.M):
        raise Failure("%s: front matter already has a url key" % name)
    return front, data[m.start() + 1 : m.end()], data[m.end() :]


def rewrite_body(body, name, line_base, counters, errors):
    body, cleaned = STRAY_BACKTICK_OPENER.subn(rb"\1\2", body)
    counters["stray_backtick"] += cleaned
    body = complete_blockquote_fences(body, name, line_base, counters, errors)

    def escape_block(match):
        block, count = BLOCK_MARKUP_TEXT.subn(b"&lt;", match.group(0))
        counters["escaped_lt"] += count
        return block

    if b"<!" in body or b"<?" in body or b"</" in body:
        body = RULE_BLOCK.sub(escape_block, body)
    blocks = [(m.start(), m.end()) for m in RULE_BLOCK.finditer(body)]

    def fail(offset, reason, text):
        errors.append(
            "%s:%d: %s: %s"
            % (name, line_base + body.count(b"\n", 0, offset) + 1, reason, text.decode("utf-8", "replace"))
        )

    fences, unclosed = fenced_ranges(body)
    if unclosed is not None:
        fail(unclosed, "fence is never closed", body[unclosed : body.find(b"\n", unclosed)])
    edits = []  # (start, end, replacement)
    toc_ranges = []

    # 1. table of contents marker
    for m in TOC.finditer(body):
        if in_ranges(fences, m.start()):
            continue
        edits.append((m.start(), m.end(), b""))
        toc_ranges.append((m.start(), m.end()))
        counters["toc"] += 1

    # blank line after a rule block that text follows directly
    for m in BLOCK_END_BEFORE_TEXT.finditer(body):
        if not in_ranges(fences, m.start()):
            edits.append((m.end(), m.end(), b"\n"))
            counters["block_breaks"] += 1

    # quotes of quoted words
    if b"'" in body:
        edits.extend(curl_single_quotes(body, fences, blocks, counters))

    # link destinations with a space, outside code
    if b"](" in body:
        for m in LINK_WITH_SPACE.finditer(body):
            if in_ranges(fences, m.start()) or in_ranges(blocks, m.start()) or in_code_span(body, m.start()):
                continue
            edits.append((m.start(1), m.start(1), b"<"))
            edits.append((m.end(1), m.end(1), b">"))
            counters["link_spaces"] += 1

    # attribute lines
    for m in IAL_LINE.finditer(body):
        start, end = m.start(), m.end()
        text = m.group(0)
        if in_ranges(fences, start):
            counters["fenced_ial"] += 1
            continue
        if in_ranges(toc_ranges, start):
            continue  # the {:toc} line of a marker removed above
        if text.lstrip()[:2] in (b"{.", b"{#"):
            if not in_ranges(blocks, start) and not in_html_block(body, start):
                fail(start, "line that Goldmark would read as a block attribute and not show", text)
            continue

        ial = IAL_ID.match(text)
        if not ial:
            fail(start, "kramdown attribute line in a form this script does not know", text)
            continue
        ident = ial.group(1)

        if start == 0:
            prev_line = b""
        else:
            prev_start = body.rfind(b"\n", 0, start - 1) + 1
            prev_line = body[prev_start : start - 1]
        next_start = end + 1
        next_end = body.find(b"\n", next_start)
        next_line = body[next_start : next_end if next_end >= 0 else len(body)]

        if not prev_line.strip():
            # kramdown: a blank line before the attribute line, so it belongs to the block after it
            if next_line.startswith(b"<div "):
                edits.append((start, next_start, b""))
                edits.append((next_start, next_start + len(b"<div "), b'<div id="' + ident + b'" '))
                counters["div_ids"] += 1
            else:
                fail(start, "attribute line before a block that is not a <div", text)
        elif not NOT_PARAGRAPH.match(prev_line) and FENCE_LINE.match(next_line):
            # kramdown: no blank line before the attribute line, so it belongs to the
            # paragraph before it; Goldmark reads {#ID} on the line after a paragraph the same way
            edits.append((start, end, b"{#" + ident + b"}"))
            counters["paragraph_ids"] += 1
        else:
            fail(start, "attribute line that does not follow paragraph text and precede a fence", text)

    if not edits:
        return body
    # insertions before replacements at the same offset; a range that starts inside the one
    # before it is a clash between two rewrites
    edits.sort(key=lambda e: (e[0], e[0] != e[1]))
    pieces = []
    position = 0
    for start, end, replacement in edits:
        if start < position:
            fail(start, "two rewrites overlap", body[start : start + 40])
            return body
        pieces.append(body[position:start])
        pieces.append(replacement)
        position = end
    pieces.append(body[position:])
    return b"".join(pieces)


def rewrite_page(data, relative, counters, errors):
    name = SOURCE + "/" + relative
    try:
        front, closing, body = split_front_matter(data, name)
    except Failure as failure:
        errors.append(str(failure))
        return None
    url = URL_PREFIX + relative[: -len(".md")] + ".html"
    if not re.fullmatch(r"[A-Za-z0-9_./ -]+", url):
        errors.append("%s: path has characters that need quoting in a front matter string" % name)
        return None
    line_base = front.count(b"\n") + closing.count(b"\n")
    markers_before = counters["toc"]
    body = rewrite_body(body, name, line_base, counters, errors)
    counters["urls"] += 1
    added = b'url: "' + url.encode("ascii") + b'"\n'
    if counters["toc"] > markers_before:
        if re.search(rb"^toc:", front, re.M):
            errors.append("%s: front matter already has a toc key" % name)
            return None
        added += b"toc: true\n"
        counters["toc_pages"] += 1
    return front + added + closing + body


def source_files(source_root):
    """Yield (relative path with forward slashes, absolute path), in a fixed order."""
    for dirpath, dirnames, filenames in os.walk(source_root):
        dirnames.sort()
        for filename in sorted(filenames):
            absolute = os.path.join(dirpath, filename)
            yield os.path.relpath(absolute, source_root).replace(os.sep, "/"), absolute


def key_order(root, errors):
    """Return the key_order.json structure, or None when a version file is unusable."""
    def read(path):
        with open(path, "rb") as handle:
            # a JSON object is read as a dict, which keeps the order of the file
            return json.loads(handle.read().decode("utf-8"), object_pairs_hook=lambda pairs: dict(pairs))

    result = {"platform": {}, "system types": {}}
    versions_path = os.path.join(root, "_data", "versions.json")
    try:
        versions = read(versions_path)
        for entry in versions["versions"]:
            keys = entry.get("platform")
            if not isinstance(keys, dict):
                continue
            name = entry["name"]
            if name in result["platform"]:
                raise ValueError("version %s is listed twice" % name)
            result["platform"][name] = list(keys)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        errors.append("_data/versions.json: %s" % error)
        return None
    dist = os.path.join(root, "_data", "dist")
    for name in sorted(os.listdir(dist)) if os.path.isdir(dist) else []:
        path = os.path.join(dist, name, "versions.json")
        if not os.path.isfile(path):
            continue
        try:
            types = read(path).get("system types")
        except (OSError, ValueError, AttributeError) as error:
            errors.append("_data/dist/%s/versions.json: %s" % (name, error))
            return None
        if isinstance(types, dict):
            result["system types"][name] = list(types)
    return result


def write_file(target, data):
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)


def main():
    parser = argparse.ArgumentParser(description="Rewrite the CI-generated pages/docs for Hugo.")
    parser.add_argument("--check", action="store_true", help="rewrite in memory, print the counters, write nothing")
    parser.add_argument(
        "--root",
        default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        help="repository root (default: two levels above this script)",
    )
    args = parser.parse_args()

    source_root = os.path.join(args.root, SOURCE)
    dest_root = os.path.join(args.root, DEST)
    if not os.path.isdir(source_root):
        print("prepare: %s does not exist" % source_root, file=sys.stderr)
        return 2

    started = time.monotonic()
    counters = {key: 0 for key, _ in COUNTER_LABELS}
    errors = []
    if not args.check:
        shutil.rmtree(dest_root, ignore_errors=True)
        shutil.rmtree(os.path.join(args.root, DATA_DEST), ignore_errors=True)

    for relative, absolute in source_files(source_root):
        if not relative.endswith(".md"):
            counters["skipped"] += 1
            continue
        counters["files"] += 1
        with open(absolute, "rb") as handle:
            data = handle.read()
        result = rewrite_page(data, relative, counters, errors)
        if result is None or args.check or errors:
            continue
        write_file(os.path.join(dest_root, relative), result)
        counters["written"] += 1

    order = key_order(args.root, errors)
    if order is not None:
        counters["key_order_platform"] = len(order["platform"])
        counters["key_order_types"] = len(order["system types"])
        if not args.check and not errors:
            write_file(
                os.path.join(args.root, DATA_DEST, "key_order.json"),
                (json.dumps(order, indent=1, ensure_ascii=False) + "\n").encode("utf-8"),
            )

    if errors:
        if not args.check:
            shutil.rmtree(dest_root, ignore_errors=True)
            shutil.rmtree(os.path.join(args.root, DATA_DEST), ignore_errors=True)
        for error in errors[:50]:
            print("prepare: " + error, file=sys.stderr)
        if len(errors) > 50:
            print("prepare: ... and %d more" % (len(errors) - 50), file=sys.stderr)
        print("prepare: %d errors, nothing written" % len(errors), file=sys.stderr)
        return 1

    width = max(len(label) for _, label in COUNTER_LABELS)
    for key, label in COUNTER_LABELS:
        print("%s  %7d" % (label.ljust(width), counters[key]))
    elapsed = time.monotonic() - started
    if args.check:
        print("check only, nothing written (%.1f s)" % elapsed)
    else:
        print("wrote %s (%.1f s)" % (os.path.relpath(dest_root, args.root), elapsed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
