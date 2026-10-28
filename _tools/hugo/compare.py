#!/usr/bin/env python3
"""Parity gate: compare a Jekyll build with a Hugo build of the same site.

    compare.py BASELINE_DIR HUGO_DIR [--allow PATTERN ...] [--allow-diff CATEGORY:PATTERN ...]
               [--fold-quotes] [--strict] [--limit N] [--jobs N]

BASELINE_DIR is the reference (the full Jekyll build of the tag jekyll-last),
HUGO_DIR the Hugo output (public/). The exit code is 1 when anything differs
beyond the allowlist, 0 otherwise. The report prints a count per category, then
the first N differences of each category with the file path and a short diff.

Categories:

  1   inventory   every file of BASELINE_DIR exists in HUGO_DIR at the same
                  relative path; files only in HUGO_DIR are listed, and fail
                  only with --strict
  2   text        per HTML page, the visible text of <body> (script, style and
                  noscript skipped, whitespace runs collapsed) is equal, and the
                  ordered list of <pre> texts is equal line by line (one trailing
                  newline of each is ignored, a leading tab counts as two spaces
                  and the indentation all lines of a block share is removed,
                  because kramdown rewrote the leading whitespace of a fence near
                  a list item), so a changed line, a line whose indentation moved
                  relative to the other lines, or a line break in code shows
  3   head        <title>, meta description, canonical link, og:type, og:site_name,
                  og:title, og:description, og:url, og:image and twitter:card;
                  the ordered list of <script src> values and inline script texts
                  and the ordered list of stylesheet links
  4a  headings    the ordered list of headings (tag, id, text) of <body>
  4b  ids         the set of id attributes of <body>
  5   refs        the set of href and src values of <body>, and the ordered list
                  of (link text, href) of its <a> elements and of its src
                  values, so two links that swap destinations show
  6   links       every href and src that points into the site resolves to a
                  file, and every fragment to an id of its target page; only
                  links broken in HUGO_DIR and not in BASELINE_DIR count
  7   css         src/main.css after whitespace and trailing semicolon normalisation,
                  and three more rules for what the two Sass compilers write
                  differently: "(4n + 1)" in an nth-* selector is "(4n+1)", a
                  number that starts with "0." starts with ".", and spaces around
                  "/" are removed
  8   sitemap     the set of <loc> values of sitemap.xml, and robots.txt
  9   static      every other file of both builds has the same bytes (files copied
                  from the repository: images, .alan sources, deps, scripts)

Allowlist (always on): the files feed.xml, README.md and LICENSE may be absent
from HUGO_DIR, a "?digits" cache-buster on /src/*.css and /src/*.js is removed
from href and src values before they are compared, and an encoded space (%20)
in an href or src equals a space (Jekyll keeps the space of a directory name,
Hugo encodes it, both name the same file).

Allowlist (asked for): --allow adds file name patterns (fnmatch on the path
relative to the site root); a matching file is left out of every category.
--allow-diff CATEGORY:PATTERN accepts the differences of one category on the
paths that match, for example 4b:pages/docs/connector/*/processor/grammar.html;
the number of accepted differences is printed. --fold-quotes compares text and
headings with the left single quote folded into the right one.

The text comparison puts a space at the boundary of block level elements and
none at the boundary of inline elements, so a newline between two paragraphs
does not count but a missing space between two inline elements does. Markup is
ignored: Rouge token spans in Jekyll's code blocks and plain code in Hugo's give
the same text.

Link resolution follows what GitHub Pages serves: a path is a file, or a
directory with an index.html, or a file with .html appended.

Standard library only. The pages are parsed in parallel, one process per core.
"""

import argparse
import difflib
import fnmatch
import hashlib
import multiprocessing
import os
import posixpath
import re
import sys
import time
import xml.etree.ElementTree as ElementTree
from html.parser import HTMLParser
from urllib.parse import unquote

DEFAULT_ALLOW = ["feed.xml", "README.md", "LICENSE"]
SPECIAL_FILES = {"src/main.css", "sitemap.xml", "robots.txt"}

CATEGORIES = [
    ("1", "inventory"),
    ("2", "text"),
    ("3", "head"),
    ("4a", "headings"),
    ("4b", "ids"),
    ("5", "refs"),
    ("6", "links"),
    ("7", "css"),
    ("8", "sitemap and robots"),
    ("9", "static files"),
]

META_KEYS = (
    "description",
    "og:type",
    "og:site_name",
    "og:title",
    "og:description",
    "og:url",
    "og:image",
    "twitter:card",
)

BLOCK_TAGS = frozenset(
    "address article aside blockquote body br dd details dialog div dl dt fieldset figcaption figure footer "
    "form h1 h2 h3 h4 h5 h6 header hgroup hr li main nav ol option p pre section select summary table tbody "
    "td textarea tfoot th thead title tr ul".split()
)
HEADING_TAGS = frozenset(["h1", "h2", "h3", "h4", "h5", "h6"])
SKIPPED_TEXT = frozenset(["script", "style", "noscript"])
CACHE_BUSTER = re.compile(r"^(/src/[^/?#]+\.(?:css|js))\?[0-9]+$")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")


def collapse(text):
    return " ".join(text.split())


class PageParser(HTMLParser):
    """One pass over a page: head metadata, body text, headings, ids, references, scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_body = False
        self.in_title = False
        self.skip = 0
        self.title_parts = []
        self.meta = {}
        self.canonical = None
        self.text = []
        self.headings = []
        self.heading = None
        self.body_ids = set()
        self.all_ids = set()
        self.body_refs = set()
        self.all_refs = set()
        self.pre_depth = 0
        self.pre_parts = []
        self.pre_texts = []
        self.anchor = None
        self.anchors = []  # (link text, href) in document order
        self.srcs = []  # src values of the body in document order
        self.script = None  # text of the inline script being read
        self.scripts = []  # ("src", value) or ("inline", text) in document order
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        attributes = {}
        for name, value in attrs:
            if name not in attributes:
                attributes[name] = value if value is not None else ""
        if tag == "body":
            self.in_body = True
        element_id = attributes.get("id")
        if element_id is not None:
            self.all_ids.add(element_id)
            if self.in_body:
                self.body_ids.add(element_id)
        if tag == "a" and attributes.get("name"):
            self.all_ids.add(attributes["name"])
        for name in ("href", "src"):
            value = attributes.get(name)
            if value is not None:
                value = value.strip()
                self.all_refs.add(value)
                if self.in_body:
                    self.body_refs.add(value)
                    if name == "src":
                        self.srcs.append(value)
        if tag == "script":
            if attributes.get("src") is not None:
                self.scripts.append(("src", attributes["src"].strip()))
            else:
                self.script = []
        elif tag == "link" and "stylesheet" in attributes.get("rel", "").lower().split():
            self.stylesheets.append(attributes.get("href", "").strip())
        if self.in_body and tag == "a" and attributes.get("href") is not None:
            self.anchor = (attributes["href"].strip(), [])
        if tag == "pre" and self.in_body:
            self.pre_depth += 1
        if not self.in_body:
            if tag == "title":
                self.in_title = True
            elif tag == "meta":
                key = (attributes.get("name") or attributes.get("property") or "").lower()
                if key in META_KEYS and key not in self.meta:
                    self.meta[key] = collapse(attributes.get("content", ""))
            elif tag == "link" and "canonical" in attributes.get("rel", "").lower().split():
                if self.canonical is None:
                    self.canonical = attributes.get("href", "").strip()
            return
        if tag in SKIPPED_TEXT:
            self.skip += 1
        if tag in BLOCK_TAGS:
            self.text.append(" ")
        if tag in HEADING_TAGS:
            self.heading = (tag, element_id or "", [])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.script is not None:
            self.scripts.append(("inline", collapse("".join(self.script))))
            self.script = None
        if not self.in_body:
            return
        if tag in SKIPPED_TEXT and self.skip:
            self.skip -= 1
        if tag in BLOCK_TAGS:
            self.text.append(" ")
        if self.heading is not None and tag == self.heading[0]:
            name, element_id, parts = self.heading
            self.headings.append((name, element_id, collapse("".join(parts))))
            self.heading = None
        if tag == "a" and self.anchor is not None:
            self.anchors.append((collapse("".join(self.anchor[1])), self.anchor[0]))
            self.anchor = None
        if tag == "pre" and self.pre_depth:
            self.pre_depth -= 1
            if not self.pre_depth:
                self.pre_texts.append("".join(self.pre_parts))
                self.pre_parts = []
        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.script is not None:
            self.script.append(data)
        if not self.in_body:
            return
        if self.pre_depth:
            self.pre_parts.append(data)
        if self.skip:
            return
        self.text.append(data)
        if self.heading is not None:
            self.heading[2].append(data)
        if self.anchor is not None:
            self.anchor[1].append(data)

    @property
    def title(self):
        return collapse("".join(self.title_parts))

    @property
    def body_text(self):
        return collapse("".join(self.text))


def parse_page(path):
    with open(path, "rb") as handle:
        document = handle.read().decode("utf-8", "replace")
    parser = PageParser()
    parser.feed(document)
    parser.close()
    return parser


class Inventory:
    def __init__(self, root):
        self.root = root
        self.files = set()
        self.dirs = set()
        for dirpath, _, filenames in os.walk(root):
            relative_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
            if relative_dir == ".":
                relative_dir = ""
            for filename in filenames:
                self.files.add((relative_dir + "/" + filename) if relative_dir else filename)
            part = relative_dir
            while part and part not in self.dirs:
                self.dirs.add(part)
                part = posixpath.dirname(part)

    def locate(self, normal, directory_hint):
        """Find what a server would answer for a path: file, directory index, or .html appended."""
        if not directory_hint and normal in self.files:
            return normal
        if directory_hint or normal == "" or normal in self.dirs:
            index = (normal + "/" if normal else "") + "index.html"
            if index in self.files:
                return index
        if not directory_hint and normal and normal + ".html" in self.files:
            return normal + ".html"
        return None


def short(text, width=160):
    text = text.replace("\n", " ")
    return text if len(text) <= width else text[: width - 3] + "..."


def trimmed(words, limit=40):
    return " ".join(words if len(words) <= limit else words[:limit] + ["..."])


def word_diff(baseline, hugo, context=6, regions=3):
    """Describe the first differing regions of two texts, word by word."""
    a = baseline.split(" ")
    b = hugo.split(" ")
    limit = min(len(a), len(b))
    start = 0
    while start < limit and a[start] == b[start]:
        start += 1
    end = 0
    while end < limit - start and a[-1 - end] == b[-1 - end]:
        end += 1
    middle_a = a[start : len(a) - end][:1500]
    middle_b = b[start : len(b) - end][:1500]
    matcher = difflib.SequenceMatcher(None, middle_a, middle_b, autojunk=False)
    pieces = [" ".join(a[max(0, start - context) : start])]
    shown = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            words = middle_a[i1:i2]
            if shown == 0:
                continue
            if shown >= regions:
                pieces.append(" ".join(words[:context]))
                break
            if len(words) <= 2 * context:
                pieces.append(" ".join(words))
            else:
                pieces.append(" ".join(words[:context]) + " ... " + " ".join(words[-context:]))
            continue
        shown += 1
        if shown > regions:
            pieces.append("...")
            break
        removed = trimmed(middle_a[i1:i2])
        added = trimmed(middle_b[j1:j2])
        pieces.append("[-%s-]" % removed if removed else "")
        pieces.append("{+%s+}" % added if added else "")
    return "at word %d (baseline %d words, hugo %d words)\n%s" % (
        start + 1,
        len(a),
        len(b),
        short(" ".join(piece for piece in pieces if piece), 600),
    )


def list_diff(label_a, label_b, a, b, limit=8):
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    lines = []
    if only_a:
        lines.append("only in %s (%d): %s" % (label_a, len(only_a), "; ".join(short(x, 100) for x in only_a[:limit])))
    if only_b:
        lines.append("only in %s (%d): %s" % (label_b, len(only_b), "; ".join(short(x, 100) for x in only_b[:limit])))
    return "\n".join(lines)


def unified(a_lines, b_lines, limit=14):
    lines = list(difflib.unified_diff(a_lines, b_lines, "baseline", "hugo", n=1, lineterm=""))
    shown = [short(line, 200) for line in lines[:limit]]
    if len(lines) > limit:
        shown.append("... (%d more diff lines)" % (len(lines) - limit))
    return "\n".join(shown)


def scripts_diff(a, b):
    """Describe the first script that differs; an inline script is shown around the first character that differs."""
    head = "scripts, in order: %d in baseline, %d in hugo" % (len(a), len(b))
    for index in range(min(len(a), len(b))):
        if a[index] == b[index]:
            continue
        (kind_a, value_a), (kind_b, value_b) = a[index], b[index]
        if kind_a == kind_b == "inline":
            at = next((i for i in range(min(len(value_a), len(value_b))) if value_a[i] != value_b[i]), min(len(value_a), len(value_b)))
            return "%s; number %d, an inline script, differs at character %d: baseline %r, hugo %r" % (
                head, index + 1, at + 1, value_a[max(0, at - 20) : at + 30], value_b[max(0, at - 20) : at + 30])
        return "%s; number %d: baseline %s %s, hugo %s %s" % (
            head, index + 1, kind_a, short(value_a, 80), kind_b, short(value_b, 80))
    longer, side = (a, "baseline") if len(a) > len(b) else (b, "hugo")
    kind, value = longer[min(len(a), len(b))]
    return "%s; the common ones are equal, %s has one more: %s %s" % (head, side, kind, short(value, 80))


def strip_newline(text):
    return text[:-1] if text.endswith("\n") else text


def normalise_indent(text):
    """Write a leading tab as two spaces and remove the indentation that all lines of a block share.

    kramdown rewrote the leading whitespace of the lines of a fence that follows a list item: a tab was
    expanded to four columns and the two columns of the item's indentation taken off, so a leading tab
    came out as two spaces; a fence indented inside a list item kept the item's indentation, which
    CommonMark removes. Both are whole-block differences in width, not in structure, and this
    normalisation makes them equal: a changed line, a line whose indentation moved relative to the
    other lines (by as little as one space) and a missing line still show."""
    lines = []
    for line in text.split("\n"):
        indent = line[: len(line) - len(line.lstrip(" \t"))]
        lines.append(indent.replace("\t", "  ") + line[len(indent) :])
    shared = os.path.commonprefix([line[: len(line) - len(line.lstrip(" "))] for line in lines if line.strip()])
    return "\n".join(line[len(shared) :] if line.startswith(shared) else line for line in lines)


def pre_diff(a, b):
    """Describe the first <pre> that differs, line by line."""
    head = "pre texts: %d in baseline, %d in hugo" % (len(a), len(b))
    for index in range(min(len(a), len(b))):
        if a[index] != b[index]:
            lines = list(difflib.unified_diff(a[index].split("\n"), b[index].split("\n"), "baseline", "hugo", n=1, lineterm=""))
            shown = [short(line[:1] + line[1:].replace(" ", "\u00b7"), 160) for line in lines[:12]]
            if len(lines) > 12:
                shown.append("... (%d more diff lines)" % (len(lines) - 12))
            return "%s; the first that differs is number %d (spaces shown as middle dots):\n%s" % (head, index + 1, "\n".join(shown))
    extra = a[len(b) :] if len(a) > len(b) else b[len(a) :]
    return "%s; the common ones are equal, the next one starts: %s" % (head, short(extra[0], 100))


def normalise_ref(value):
    """Remove the cache-buster, and write an encoded space as a space: Jekyll keeps the
    space of a directory name in an href, Hugo encodes it, and both name the same file."""
    return CACHE_BUSTER.sub(r"\1", value).replace("%20", " ")


def analyse_reference(page, ref):
    """Return None for a reference that does not point into the site, else
    (normalised path, directory hint, fragment, same page). The path is relative to the
    site root without a leading slash, and '' for the root itself."""
    ref = ref.strip()
    if not ref or ref.startswith("//") or SCHEME.match(ref):
        return None
    path_part, _, fragment = ref.partition("#")
    path_part = path_part.partition("?")[0]
    if path_part == "":
        return (page, False, fragment, True)
    path = unquote(path_part)
    if not path.startswith("/"):
        path = posixpath.join(posixpath.dirname(page), path)
    hint = path.endswith("/") or path.endswith("/.") or path.endswith("/..")
    normal = posixpath.normpath("/" + path.lstrip("/")).lstrip("/")
    if normal == ".":
        normal = ""
    return (normal, hint, fragment, False)


def check_links(page, refs, ids, inventory):
    """Return (broken, cross) for one page: broken references, and fragments of other pages to check."""
    broken = []
    cross = []
    for ref in sorted(refs):
        parsed = analyse_reference(page, ref)
        if parsed is None:
            continue
        normal, hint, fragment, same_page = parsed
        if same_page:
            target = page
        else:
            target = inventory.locate(normal, hint)
            if target is None:
                broken.append((ref, "no such file"))
                continue
        if fragment in ("", "top"):
            continue
        decoded = unquote(fragment)
        if target == page:
            if fragment not in ids and decoded not in ids:
                broken.append((ref, "no such id on this page"))
        elif target.endswith(".html"):
            cross.append((ref, target, fragment))
    return broken, cross


WORKER = {}


def init_worker(baseline_inventory, hugo_inventory, fold_quotes):
    WORKER["baseline"] = baseline_inventory
    WORKER["hugo"] = hugo_inventory
    WORKER["fold"] = fold_quotes


def fold(text):
    """Treat a left single quote like a right one: Goldmark's typographer and kramdown's
    smart quotes disagree on which side some quotes of the form 'word' belong to."""
    return text.replace("\u2018", "\u2019")


def compare_page(task):
    """Parse a page of HUGO_DIR and its counterpart in BASELINE_DIR, return the differences."""
    relative, in_baseline = task
    baseline_inventory = WORKER["baseline"]
    hugo_inventory = WORKER["hugo"]
    hugo = parse_page(os.path.join(hugo_inventory.root, relative))
    diffs = []
    baseline_links = None
    if in_baseline:
        baseline = parse_page(os.path.join(baseline_inventory.root, relative))
        baseline_links = check_links(relative, baseline.all_refs, baseline.all_ids, baseline_inventory)

        text_a, text_b = baseline.body_text, hugo.body_text
        headings_a, headings_b = baseline.headings, hugo.headings
        anchors_a, anchors_b = baseline.anchors, hugo.anchors
        if WORKER["fold"]:
            text_a, text_b = fold(text_a), fold(text_b)
            headings_a = [(t, i, fold(x)) for t, i, x in headings_a]
            headings_b = [(t, i, fold(x)) for t, i, x in headings_b]
            anchors_a = [(fold(x), h) for x, h in anchors_a]
            anchors_b = [(fold(x), h) for x, h in anchors_b]
        lines = []
        if text_a != text_b:
            lines.append(word_diff(text_a, text_b))
        pre_a = [normalise_indent(strip_newline(x)) for x in baseline.pre_texts]
        pre_b = [normalise_indent(strip_newline(x)) for x in hugo.pre_texts]
        if pre_a != pre_b:
            lines.append(pre_diff(pre_a, pre_b))
        if lines:
            diffs.append(("2", relative, "\n".join(lines)))

        head_lines = []
        pairs = [("title", baseline.title, hugo.title), ("canonical", baseline.canonical, hugo.canonical)]
        pairs += [(key, baseline.meta.get(key), hugo.meta.get(key)) for key in META_KEYS]
        for key, a, b in pairs:
            if a != b:
                head_lines.append("%s: baseline=%r hugo=%r" % (key, short(str(a), 100), short(str(b), 100)))
        scripts_a = [(kind, normalise_ref(value) if kind == "src" else value) for kind, value in baseline.scripts]
        scripts_b = [(kind, normalise_ref(value) if kind == "src" else value) for kind, value in hugo.scripts]
        if scripts_a != scripts_b:
            head_lines.append(scripts_diff(scripts_a, scripts_b))
        sheets_a = [normalise_ref(value) for value in baseline.stylesheets]
        sheets_b = [normalise_ref(value) for value in hugo.stylesheets]
        if sheets_a != sheets_b:
            head_lines.append("stylesheets, in order:")
            head_lines.append(unified(sheets_a, sheets_b))
        if head_lines:
            diffs.append(("3", relative, "\n".join(head_lines)))

        if headings_a != headings_b:
            render = lambda items: ["%s #%s %s" % (tag, ident, short(text, 100)) for tag, ident, text in items]
            diffs.append(("4a", relative, unified(render(headings_a), render(headings_b))))
        if baseline.body_ids != hugo.body_ids:
            diffs.append(("4b", relative, list_diff("baseline", "hugo", baseline.body_ids, hugo.body_ids)))

        refs_a = {normalise_ref(value) for value in baseline.body_refs}
        refs_b = {normalise_ref(value) for value in hugo.body_refs}
        if refs_a != refs_b:
            diffs.append(("5", relative, list_diff("baseline", "hugo", refs_a, refs_b)))
        else:
            # same values, but perhaps on other links or in another order
            links_a = ["%s -> %s" % (short(text, 60), normalise_ref(href)) for text, href in anchors_a]
            links_b = ["%s -> %s" % (short(text, 60), normalise_ref(href)) for text, href in anchors_b]
            srcs_a = ["src " + normalise_ref(value) for value in baseline.srcs]
            srcs_b = ["src " + normalise_ref(value) for value in hugo.srcs]
            if links_a + srcs_a != links_b + srcs_b:
                diffs.append(("5", relative, "same values, other links or order:\n" + unified(links_a + srcs_a, links_b + srcs_b)))

    hugo_links = check_links(relative, hugo.all_refs, hugo.all_ids, hugo_inventory)
    return relative, diffs, baseline_links, hugo_links


def scan_ids(task):
    root, relative = task
    return relative, frozenset(parse_page(os.path.join(root, relative)).all_ids)


def normalise_css(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" ?([{};,:]) ?", r"\1", text)
    text = text.replace(";}", "}")
    # what the two Sass compilers write differently
    text = re.sub(r"(:nth-[a-z-]+\()([^)]*)\)", lambda m: m.group(1) + re.sub(r"\s*([+-])\s*", r"\1", m.group(2)) + ")", text)
    text = re.sub(r"(?<![\w.])0\.(?=[0-9])", ".", text)
    text = re.sub(r" ?/ ?", "/", text)
    return text.strip()


def read_text(root, relative):
    with open(os.path.join(root, relative), "rb") as handle:
        return handle.read().decode("utf-8", "replace")


def file_digest(path):
    digest = hashlib.sha1()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def locations(path_text):
    root = ElementTree.fromstring(path_text.encode("utf-8"))
    return {element.text.strip() for element in root.iter() if element.tag.endswith("}loc") or element.tag == "loc"}


def main():
    parser = argparse.ArgumentParser(description="Parity gate between a Jekyll build and a Hugo build.")
    parser.add_argument("baseline")
    parser.add_argument("hugo")
    parser.add_argument("--allow", action="append", default=[], metavar="PATTERN",
                        help="file that may differ or be absent, fnmatch on the relative path (repeatable)")
    parser.add_argument("--allow-diff", action="append", default=[], metavar="CATEGORY:PATTERN",
                        help="differences of one category (1, 2, 3, 4a, 4b, 5, 6, 7, 8, 9) whose path matches the "
                             "pattern are counted as allowed; for category 6 the path is the reference (repeatable)")
    parser.add_argument("--fold-quotes", action="store_true",
                        help="compare text and headings with left single quotes folded into right ones")
    parser.add_argument("--strict", action="store_true", help="files only in HUGO_DIR fail the gate")
    parser.add_argument("--limit", type=int, default=20, help="differences shown per category (default 20)")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 1, help="parser processes")
    args = parser.parse_args()

    started = time.monotonic()
    allow = DEFAULT_ALLOW + args.allow
    allowed = lambda relative: any(fnmatch.fnmatchcase(relative, pattern) for pattern in allow)

    for directory in (args.baseline, args.hugo):
        if not os.path.isdir(directory):
            print("compare: %s is not a directory" % directory, file=sys.stderr)
            return 2

    baseline_inventory = Inventory(args.baseline)
    hugo_inventory = Inventory(args.hugo)
    findings = {key: [] for key, _ in CATEGORIES}  # (path, detail, weight)
    notes = []

    def add(key, path, detail, weight=1):
        findings[key].append((path, detail, weight))

    # 1. inventory
    missing_allowed = 0
    for relative in sorted(baseline_inventory.files - hugo_inventory.files):
        if allowed(relative):
            missing_allowed += 1
        else:
            add("1", relative, "missing from hugo")
    extra = sorted(f for f in hugo_inventory.files - baseline_inventory.files if not allowed(f))
    if extra:
        notes.append("%d files only in hugo (listed, not a failure without --strict): %s" % (
            len(extra), "; ".join(extra[:10]) + (" ..." if len(extra) > 10 else "")))
    if args.strict:
        for relative in extra:
            add("1", relative, "only in hugo")

    # 2 to 6. pages
    hugo_pages = sorted(f for f in hugo_inventory.files if f.endswith(".html") and not allowed(f))
    tasks = [(f, f in baseline_inventory.files) for f in hugo_pages]
    broken = {"baseline": {}, "hugo": {}}
    cross = {"baseline": [], "hugo": []}
    with multiprocessing.Pool(args.jobs, init_worker, (baseline_inventory, hugo_inventory, args.fold_quotes)) as pool:
        for relative, diffs, baseline_links, hugo_links in pool.imap_unordered(compare_page, tasks, chunksize=8):
            for key, path, detail in diffs:
                add(key, path, detail)
            if baseline_links is not None:
                broken["baseline"][relative] = {ref for ref, _ in baseline_links[0]}
                cross["baseline"].extend((relative,) + item for item in baseline_links[1])
            broken["hugo"][relative] = hugo_links[0]
            cross["hugo"].extend((relative,) + item for item in hugo_links[1])

        # fragments of other pages: parse each cited target once per side
        for side, root in (("baseline", args.baseline), ("hugo", args.hugo)):
            targets = sorted({item[2] for item in cross[side]})
            id_sets = dict(pool.imap_unordered(scan_ids, [(root, t) for t in targets], chunksize=8))
            for page, ref, target, fragment in cross[side]:
                ids = id_sets[target]
                if fragment in ids or unquote(fragment) in ids:
                    continue
                reason = "no id %r in /%s" % (fragment, target)
                if side == "baseline":
                    broken["baseline"].setdefault(page, set()).add(ref)
                else:
                    broken["hugo"][page].append((ref, reason))

    already_broken = 0
    by_reference = {}  # (reference, reason) -> pages
    for page in sorted(broken["hugo"]):
        known = broken["baseline"].get(page, set())
        for ref, reason in broken["hugo"][page]:
            if ref in known:
                already_broken += 1
            else:
                by_reference.setdefault((ref, reason), []).append(page)
    for (ref, reason), pages in by_reference.items():
        listed = "; ".join(pages[:3]) + (" ..." if len(pages) > 3 else "")
        add("6", ref, "%s, on %d pages: %s" % (reason, len(pages), listed), len(pages))
    if already_broken:
        notes.append("%d links broken in both builds, not counted" % already_broken)

    # 7. css
    if "src/main.css" in baseline_inventory.files and "src/main.css" in hugo_inventory.files and not allowed("src/main.css"):
        a = normalise_css(read_text(args.baseline, "src/main.css"))
        b = normalise_css(read_text(args.hugo, "src/main.css"))
        if a != b:
            split = lambda text: text.replace("}", "}\n").split("\n")
            add("7", "src/main.css", unified(split(a), split(b)))

    # 8. sitemap and robots
    if "sitemap.xml" in baseline_inventory.files and "sitemap.xml" in hugo_inventory.files and not allowed("sitemap.xml"):
        try:
            a = locations(read_text(args.baseline, "sitemap.xml"))
            b = locations(read_text(args.hugo, "sitemap.xml"))
            if a != b:
                add("8", "sitemap.xml", "%d <loc> in baseline, %d in hugo\n%s" % (
                    len(a), len(b), list_diff("baseline", "hugo", a, b, 10)))
        except ElementTree.ParseError as error:
            add("8", "sitemap.xml", "not well-formed XML: %s" % error)
    if "robots.txt" in baseline_inventory.files and "robots.txt" in hugo_inventory.files and not allowed("robots.txt"):
        a = [line.rstrip() for line in read_text(args.baseline, "robots.txt").strip().split("\n")]
        b = [line.rstrip() for line in read_text(args.hugo, "robots.txt").strip().split("\n")]
        if a != b:
            add("8", "robots.txt", unified(a, b))

    # 9. static files
    static_checked = 0
    for relative in sorted(baseline_inventory.files & hugo_inventory.files):
        if relative.endswith(".html") or relative in SPECIAL_FILES or allowed(relative):
            continue
        static_checked += 1
        a = os.path.join(args.baseline, relative)
        b = os.path.join(args.hugo, relative)
        if os.path.getsize(a) != os.path.getsize(b):
            add("9", relative, "size %d in baseline, %d in hugo" % (os.path.getsize(a), os.path.getsize(b)))
        elif file_digest(a) != file_digest(b):
            add("9", relative, "same size, different bytes")

    # differences allowed by --allow-diff
    allowed_diffs = 0
    for entry in args.allow_diff:
        key, _, pattern = entry.partition(":")
        if key not in findings or not pattern:
            print("compare: --allow-diff wants CATEGORY:PATTERN, got %r" % entry, file=sys.stderr)
            return 2
        kept = [e for e in findings[key] if not fnmatch.fnmatchcase(e[0], pattern)]
        allowed_diffs += sum(e[2] for e in findings[key]) - sum(e[2] for e in kept)
        findings[key] = kept
    if allowed_diffs:
        notes.append("%d differences allowed by --allow-diff, not counted" % allowed_diffs)

    # report
    elapsed = time.monotonic() - started
    print("parity gate: %s (baseline) vs %s (hugo)" % (args.baseline, args.hugo))
    print("%d pages parsed in hugo, %d of them in baseline too; %d static files compared; allowed absent: %d" % (
        len(hugo_pages), sum(1 for _, in_baseline in tasks if in_baseline), static_checked, missing_allowed))
    print()
    total = 0
    failing = 0
    print("category                 differences")
    for key, name in CATEGORIES:
        count = sum(weight for _, _, weight in findings[key])
        total += count
        failing += 1 if count else 0
        print("%-3s %-20s %7d" % (key, name, count))
    for note in notes:
        print("note: " + note)
    for key, name in CATEGORIES:
        entries = sorted(findings[key], key=lambda entry: (-entry[2], entry[0]))
        if not entries:
            continue
        print()
        grouped = "" if len(entries) == sum(w for _, _, w in entries) else ", in %d groups" % len(entries)
        print("== %s %s: %d%s, first %d ==" % (key, name, sum(w for _, _, w in entries), grouped, min(len(entries), args.limit)))
        for path, detail, _ in entries[: args.limit]:
            print(short(path, 200))
            for line in detail.split("\n"):
                print("    " + line)
    print()
    if total:
        print("compare: FAIL, %d differences in %d categories (%.1f s)" % (total, failing, elapsed))
        return 1
    print("compare: PASS, 0 differences (%.1f s)" % elapsed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
