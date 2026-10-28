"""Tests of prepare.py, the one-time converter, on small synthetic pages: every rewrite, every form it
refuses, and the pages that are already in the Hugo form.

Run from the repository root: python3 -m unittest discover -s _tools/hugo/tests
"""

import hashlib
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)

import prepare  # noqa: E402

PREPARE = os.path.join(TOOLS, "prepare.py")
FRONT = '---\nlayout: "doc"\norigin: "a"\n---\n'
RELATIVE = "a/1/b/grammar.md"


def block(text="'<span class=\"token string\">x</span>' { }"):
    """A generated rule block as the CI job writes it."""
    return (
        '<div class="language-js highlighter-rouge">\n<div class="highlight">\n'
        '<pre class="highlight language-js code-custom">\n%s\n</pre>\n</div>\n</div>\n' % text
    )


def rewrite(body, relative=RELATIVE, front=FRONT):
    """Return (output text, counters, errors) of one page."""
    counters = {key: 0 for key, _ in prepare.COUNTER_LABELS}
    errors = []
    result = prepare.rewrite_page((front + body).encode("utf-8"), relative, counters, errors)
    return (result.decode("utf-8") if result is not None else None), counters, errors


def body_of(output):
    return output.split("---\n", 2)[2]


class Rewrites(unittest.TestCase):
    def test_toc_marker_after_a_rule_block(self):
        # a blank line is inserted where the removed marker starts; the two edits meet at one offset
        output, counters, errors = rewrite(block() + "1. TOC\n{:toc}\n\n## Heading\n")
        self.assertEqual(errors, [])
        self.assertEqual(body_of(output), block() + "\n\n## Heading\n")
        self.assertEqual((counters["toc"], counters["toc_pages"], counters["block_breaks"]), (1, 1, 1))
        self.assertIn('url: "/pages/docs/a/1/b/grammar.html"\ntoc: true\n---\n', output)

    def test_toc_marker_with_blank_line_between(self):
        output, _, errors = rewrite("\n1. TOC\n\n{:toc}\n\n## H\n")
        self.assertEqual(errors, [])
        self.assertEqual(body_of(output), "\n\n## H\n")

    def test_page_without_marker_has_no_toc_key(self):
        output, counters, _ = rewrite("Text.\n")
        self.assertNotIn("toc:", output)
        self.assertEqual(counters["toc_pages"], 0)

    def test_overlapping_rewrites_are_an_error(self):
        clash = lambda body, fences, blocks, counters: [(body.index(b"{:toc}") + 2, body.index(b"{:toc}") + 3, b"X")]
        with mock.patch.object(prepare, "curl_single_quotes", clash):
            _, _, errors = rewrite("text 'x'\n\n1. TOC\n{:toc}\n\n## H\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("two rewrites overlap", errors[0])

    def test_id_moves_onto_the_div_as_its_first_attribute(self):
        output, counters, errors = rewrite("\n{: #grammar-rule--node }\n" + block())
        self.assertEqual(errors, [])
        self.assertIn('<div id="grammar-rule--node" class="language-js highlighter-rouge">', output)
        self.assertNotIn("{:", output)
        self.assertEqual(counters["div_ids"], 1)

    def test_id_after_a_paragraph_before_a_fence(self):
        output, counters, errors = rewrite("The model:\n{: #example--y }\n```js\nx\n```\n")
        self.assertEqual(errors, [])
        self.assertEqual(body_of(output), "The model:\n{#example--y}\n```js\nx\n```\n")
        self.assertEqual(counters["paragraph_ids"], 1)

    def test_url_keeps_spaces_of_directory_names(self):
        output, _, _ = rewrite("Text.\n", relative="webclient/zora.1rc8.0/client bindings/client_bindings.md")
        self.assertIn('url: "/pages/docs/webclient/zora.1rc8.0/client bindings/client_bindings.html"', output)

    def test_a_page_in_the_hugo_form_passes_unchanged(self):
        # url and toc in the front matter, attribute lines of the Hugo form, quotes, a rule block with names in it:
        # nothing of it is touched, and nothing is an error
        front = '---\nlayout: "doc"\nurl: "/pages/docs/a/1/b/grammar.html"\ntoc: true\n---\n'
        body = (
            "The 'empty' text and don't. See [a](b c).\n{#example--y}\n```js\nx\n```\n\n"
            "{.class}\n\n" + block("a <begin> <!-- c -->") + "## Heading\n"
        )
        output, counters, errors = rewrite(body, front=front)
        self.assertEqual(errors, [])
        self.assertEqual(output, front + body)
        self.assertEqual(counters["hugo_form"], 1)
        self.assertEqual(sum(counters[key] for key in counters if key not in ("hugo_form", "files")), 0)

    def test_a_page_with_a_url_key_and_no_toc_key_passes_unchanged_too(self):
        front = '---\nlayout: "doc"\nurl: "/pages/docs/a/1/b/grammar.html"\n---\n'
        output, _, errors = rewrite("Text.\n", front=front)
        self.assertEqual((errors, output), ([], front + "Text.\n"))

    def test_a_kramdown_line_in_a_page_that_has_a_url_key_is_an_error(self):
        front = '---\nurl: "/x"\n---\n'
        _, _, errors = rewrite("Text.\n\n1. TOC\n{:toc}\n\n```js\n{: #in-a-fence }\n```\n", front=front)
        self.assertEqual(len(errors), 1)
        self.assertIn("{:toc}", errors[0])
        self.assertIn("pages/docs/a/1/b/grammar.md:7:", errors[0])

    def test_blockquote_fence_is_completed(self):
        output, counters, _ = rewrite("Text\n> ```js\ncode\n```\n\nAfter.\n")
        self.assertEqual(body_of(output), "Text\n> ```js\n> code\n> ```\n\nAfter.\n")
        self.assertEqual(counters["blockquote_fences"], 1)

    def test_blockquote_fence_that_is_closed_in_the_quote_is_left(self):
        text = "> ```js\n> code\n> ```\n"
        output, counters, _ = rewrite(text)
        self.assertEqual(body_of(output), text)
        self.assertEqual(counters["blockquote_fences"], 0)

    def test_blockquote_fence_without_a_closing_line_is_an_error(self):
        _, _, errors = rewrite("> ```js\ncode\n\nmore\n")
        self.assertIn("not closed", errors[0])

    def test_stray_backtick_after_the_fence_language(self):
        output, counters, _ = rewrite("```js`\ncode\n````\n\nAfter.\n")
        self.assertEqual(body_of(output), "```js\ncode\n````\n\nAfter.\n")
        self.assertEqual(counters["stray_backtick"], 1)

    def test_fence_that_is_never_closed_is_an_error(self):
        _, _, errors = rewrite("```js\ncode\n")
        self.assertIn("never closed", errors[0])

    def test_blank_line_after_a_rule_block_that_text_follows(self):
        output, counters, _ = rewrite(block() + "## Heading\n")
        self.assertEqual(body_of(output), block() + "\n## Heading\n")
        self.assertEqual(counters["block_breaks"], 1)

    def test_no_blank_line_when_a_blank_line_or_a_tag_follows(self):
        text = block() + "\n" + block() + block()
        output, counters, _ = rewrite(text)
        self.assertEqual(body_of(output), text)
        self.assertEqual(counters["block_breaks"], 0)

    def test_everything_but_the_tags_of_the_generator_is_escaped_in_a_rule_block(self):
        inner = (
            "a <span class=\"x\">b</span> <a href=\"#x\">c</a> <pre> </pre> <div> </div> <code>d</code> "
            "<begin> <end>. <step> <!</span> <?x </</span> <!-- c --> </foo> <= << <-"
        )
        output, counters, _ = rewrite(block(inner))
        self.assertIn(
            "a <span class=\"x\">b</span> <a href=\"#x\">c</a> <pre> </pre> <div> </div> <code>d</code> "
            "&lt;begin> &lt;end>. &lt;step> &lt;!</span> &lt;?x &lt;/</span> &lt;!-- c --> &lt;/foo> &lt;= &lt;&lt; &lt;-",
            output,
        )
        self.assertEqual(counters["escaped_lt"], 12)

    def test_a_tag_name_that_only_starts_like_a_tag_of_the_generator_is_escaped(self):
        output, _, _ = rewrite(block("<spanx> <abbr> <divider> <preview> <codex>"))
        self.assertIn("&lt;spanx> &lt;abbr> &lt;divider> &lt;preview> &lt;codex>", output)

    def test_markup_text_outside_a_rule_block_is_not_escaped(self):
        output, counters, _ = rewrite("`<!` and <!-- a comment --> and </foo>\n")
        self.assertIn("`<!` and <!-- a comment --> and </foo>", output)
        self.assertEqual(counters["escaped_lt"], 0)

    def test_link_destination_with_a_space(self):
        output, counters, _ = rewrite("See [client bindings](../client bindings/c.html) and `[a](b c)` and [t](u 'v').\n")
        self.assertIn("[client bindings](<../client bindings/c.html>)", output)
        self.assertIn("`[a](b c)`", output)
        self.assertEqual(counters["link_spaces"], 1)

    def test_link_destination_in_a_fence_or_a_code_span_of_two_backticks(self):
        output, counters, _ = rewrite("```md\n[a](b c)\n```\n\n``x [a](b c) y``\n")
        self.assertIn("[a](b c)\n```", output)
        self.assertIn("``x [a](b c) y``", output)
        self.assertEqual(counters["link_spaces"], 0)


class Quotes(unittest.TestCase):
    def quotes(self, text):
        output, counters, errors = rewrite(text)
        self.assertEqual(errors, [])
        return body_of(output), counters

    def test_quoted_words_and_apostrophes(self):
        text, counters = self.quotes("called 'empty' and renders, (the 'not') and [a 'b'] and don't, it's.\n")
        self.assertEqual(text, "called ‘empty’ and renders, (the ‘not’) and [a ‘b’] and don't, it's.\n")
        self.assertEqual((counters["quote_open"], counters["quote_close"]), (3, 3))

    def test_emphasis_that_starts_with_a_quote(self):
        text, _ = self.quotes("and *'empty'* and _'under'_ here\n")
        self.assertEqual(text, "and *‘empty’* and _‘under’_ here\n")

    def test_decades_and_numbers(self):
        text, _ = self.quotes("the '90s and the '5' number\n")
        self.assertEqual(text, "the ’90s and the ‘5’ number\n")

    def test_after_a_slash_the_quote_closes(self):
        text, _ = self.quotes("a /'x'/ path and 'x'/'y'\n")
        self.assertEqual(text, "a /’x’/ path and ‘x’/’y’\n")

    def test_span_across_two_lines(self):
        text, _ = self.quotes("two lines: 'first\nsecond' done.\n")
        self.assertEqual(text, "two lines: ‘first\nsecond’ done.\n")

    def test_escaped_quote_is_left(self):
        text, _ = self.quotes("Escaped \\'plain\\' and 'it' ends.\n")
        self.assertEqual(text, "Escaped \\'plain\\' and ‘it’ ends.\n")

    def test_not_prose_is_left(self):
        source = (
            "A `code 'span'` and ``double 'span'`` and <code>'c'</code> and <kbd>'k'</kbd> and "
            "<a href='x'>link</a> and [t](u 'title').\n\n"
            "```js\n'fenced' stays\n```\n\n"
            "<div class='html'>\n'html block' stays\n</div>\n\n"
            "    indented 'code' stays\n\n" + block("'rule' stays")
        )
        text, counters = self.quotes(source)
        self.assertEqual(text, source)
        self.assertEqual(counters["quote_open"] + counters["quote_close"], 0)

    def test_list_continuation_is_prose(self):
        text, _ = self.quotes("- item with 'quoted' text\n    continuation 'again' here\n")
        self.assertEqual(text, "- item with ‘quoted’ text\n    continuation ‘again’ here\n")


class Attributes(unittest.TestCase):
    def error_lines(self, body):
        _, _, errors = rewrite(body)
        return errors

    def test_unknown_kramdown_forms_are_errors_with_file_and_line(self):
        errors = self.error_lines("Some text.\n{: .more }\n\n{: #grammar-rule--x }\nNot a div.\n")
        self.assertEqual(len(errors), 2)
        self.assertIn("pages/docs/a/1/b/grammar.md:6:", errors[0])
        self.assertIn("{: .more }", errors[0])
        self.assertIn("pages/docs/a/1/b/grammar.md:8:", errors[1])

    def test_orphan_toc_attribute_line_is_an_error(self):
        self.assertEqual(len(self.error_lines("{:toc}\n")), 1)

    def test_goldmark_attribute_lines_are_errors(self):
        errors = self.error_lines("Text\n{.class}\n\nMore text\n{#id}\n")
        self.assertEqual(len(errors), 2)
        self.assertIn("block attribute", errors[0])

    def test_attribute_lines_in_fences_and_raw_html_are_not_errors(self):
        body = (
            "```js\n{.class}\n{#id}\n{: #x }\n```\n\n"
            "<div class=\"x\">\n{.class}\n{#id}\n</div>\n\n" + block("{#in a rule block}")
        )
        self.assertEqual(self.error_lines(body), [])


class Whole(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.root, ignore_errors=True))
        self.old = FRONT + "1. TOC\n{:toc}\n\n## H 'x'\n"
        self.write("pages/docs/a/1/b/grammar.md", self.old)
        self.write("pages/docs/webclient/v/client bindings/c.md", FRONT + "Text.\n")
        self.write("pages/docs/notes.txt", "not a page\n")
        self.write("pages/other.md", "'untouched' page outside pages/docs\n")
        self.write("_data/versions.json", "{}")

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def read(self, relative):
        with open(os.path.join(self.root, relative), encoding="utf-8") as handle:
            return handle.read()

    def run_prepare(self, *args):
        return subprocess.run([sys.executable, PREPARE, "--root", self.root, *args], capture_output=True, text=True)

    def tree_hash(self):
        digest = hashlib.sha1()
        for dirpath, dirnames, filenames in sorted(os.walk(self.root)):
            dirnames.sort()
            for name in sorted(filenames):
                path = os.path.join(dirpath, name)
                digest.update(path.encode())
                with open(path, "rb") as handle:
                    digest.update(handle.read())
        return digest.hexdigest()

    def test_a_mode_is_required(self):
        result = self.run_prepare()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.read("pages/docs/a/1/b/grammar.md"), self.old)

    def test_in_place_rewrites_the_pages_and_nothing_else(self):
        os.chmod(os.path.join(self.root, "pages/docs/a/1/b/grammar.md"), 0o644)
        before = self.tree_hash()
        result = self.run_prepare("--in-place")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("rewrote 2 pages", result.stdout)
        self.assertIn('url: "/pages/docs/a/1/b/grammar.html"\ntoc: true\n', self.read("pages/docs/a/1/b/grammar.md"))
        self.assertIn("## H \u2018x\u2019\n", self.read("pages/docs/a/1/b/grammar.md"))
        self.assertIn('url: "/pages/docs/webclient/v/client bindings/c.html"', self.read("pages/docs/webclient/v/client bindings/c.md"))
        self.assertEqual(self.read("pages/docs/notes.txt"), "not a page\n")
        self.assertEqual(self.read("pages/other.md"), "'untouched' page outside pages/docs\n")
        self.assertNotEqual(self.tree_hash(), before)
        self.assertEqual(
            sorted(os.listdir(self.root)), ["_data", "pages"], "nothing but the pages is written: no .build, no data"
        )
        self.assertEqual(sorted(os.listdir(os.path.join(self.root, "pages/docs"))), ["a", "notes.txt", "webclient"])
        mode = stat.S_IMODE(os.stat(os.path.join(self.root, "pages/docs/a/1/b/grammar.md")).st_mode)
        self.assertEqual(mode, 0o644)

    def test_a_second_run_changes_nothing(self):
        self.run_prepare("--in-place")
        first = self.tree_hash()
        result = self.run_prepare("--in-place")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("rewrote 0 pages", result.stdout)
        self.assertEqual(self.tree_hash(), first)

    def test_converted_and_newer_pages_are_counted_as_the_hugo_form(self):
        self.write("pages/docs/new/1/x/grammar.md", '---\nurl: "/pages/docs/new/1/x/grammar.html"\ntoc: true\n---\n\nText.\n')
        result = self.run_prepare("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"already in the Hugo form, left as they are\s+1\n")

    def test_check_writes_nothing(self):
        before = self.tree_hash()
        result = self.run_prepare("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("check only", result.stdout)
        self.assertEqual(self.tree_hash(), before)

    def test_output_writes_a_copy_and_leaves_the_pages(self):
        before = self.tree_hash()
        out = os.path.join(self.root, "..", "prepare-out-%d" % os.getpid())
        self.addCleanup(lambda: __import__("shutil").rmtree(out, ignore_errors=True))
        result = self.run_prepare("--output", out)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.tree_hash(), before)
        with open(os.path.join(out, "a/1/b/grammar.md"), encoding="utf-8") as handle:
            self.assertIn("toc: true", handle.read())
        self.assertFalse(os.path.exists(os.path.join(out, "notes.txt")))
        self.assertEqual(self.run_prepare("--output", out).returncode, 2, "a directory that is not empty is refused")

    def test_an_unknown_form_stops_the_run_and_writes_nothing(self):
        self.write("pages/docs/z/1/y/grammar.md", FRONT + "Text\n{: .more }\n")
        before = self.tree_hash()
        for mode in ("--in-place", "--check"):
            result = self.run_prepare(mode)
            self.assertEqual(result.returncode, 1)
            self.assertIn("z/1/y/grammar.md:6:", result.stderr)
            self.assertIn("nothing written", result.stderr)
            self.assertEqual(self.tree_hash(), before)


if __name__ == "__main__":
    unittest.main()
