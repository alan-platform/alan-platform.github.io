"""Tests of prepare.py on small synthetic pages: every rewrite, and every form it refuses.

Run from the repository root: python3 -m unittest discover -s _tools/hugo/tests
"""

import hashlib
import json
import os
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

    def test_front_matter_with_a_url_key_is_an_error(self):
        output, _, errors = rewrite("Text.\n", front='---\nurl: "/x"\n---\n')
        self.assertIsNone(output)
        self.assertIn("already has a url key", errors[0])

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

    def test_markup_text_in_a_rule_block_is_escaped(self):
        inner = (
            "a <span>b</span> <a href=\"#x\">c</a> <begin> "
            "<!</span> <?x </</span> <!-- c --> </foo> </code>"
        )
        output, counters, _ = rewrite(block(inner))
        self.assertIn(
            "a <span>b</span> <a href=\"#x\">c</a> <begin> "
            "&lt;!</span> &lt;?x &lt;/</span> &lt;!-- c --> &lt;/foo> </code>",
            output,
        )
        self.assertEqual(counters["escaped_lt"], 5)

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
        self.write("pages/docs/a/1/b/grammar.md", FRONT + "1. TOC\n{:toc}\n\n## H 'x'\n")
        self.write("pages/docs/webclient/v/client bindings/c.md", FRONT + "Text.\n")
        self.write(
            "_data/versions.json",
            '{"current": "2026.3", "versions": [\n'
            ' {"name": "2026.3", "platform": {"zeta": "1", "alpha": "2", "model": "3"}},\n'
            ' {"name": "2026.2", "platform": {"model": "4", "interface": "5"}},\n'
            ' {"name": "2026.1"}]}',
        )
        self.write(
            "_data/dist/2026.3/versions.json",
            '{"platform version": "2026.3", "system types": {"webclient": {}, "connector": {}, "auto-webclient": {}}}',
        )

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def run_prepare(self, *args):
        return subprocess.run([sys.executable, PREPARE, "--root", self.root, *args], capture_output=True, text=True)

    def tree_hash(self):
        digest = hashlib.sha1()
        for dirpath, dirnames, filenames in sorted(os.walk(os.path.join(self.root, ".build"))):
            dirnames.sort()
            for name in sorted(filenames):
                path = os.path.join(dirpath, name)
                digest.update(path.encode())
                with open(path, "rb") as handle:
                    digest.update(handle.read())
        return digest.hexdigest()

    def test_writes_pages_and_key_order(self):
        result = self.run_prepare()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = os.path.join(self.root, ".build/content/pages/docs")
        self.assertTrue(os.path.isfile(os.path.join(out, "webclient/v/client bindings/c.md")))
        with open(os.path.join(out, "a/1/b/grammar.md"), encoding="utf-8") as handle:
            self.assertIn("## H ‘x’\n", handle.read())
        with open(os.path.join(self.root, ".build/data/key_order.json"), encoding="utf-8") as handle:
            order = json.load(handle)
        self.assertEqual(
            order,
            {
                "platform": {"2026.3": ["zeta", "alpha", "model"], "2026.2": ["model", "interface"]},
                "system types": {"2026.3": ["webclient", "connector", "auto-webclient"]},
            },
        )
        self.assertEqual(list(order["platform"]["2026.3"]), ["zeta", "alpha", "model"])

    def test_check_writes_nothing_and_prints_the_counters(self):
        result = self.run_prepare("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("key_order.json: platform versions", result.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.root, ".build")))

    def test_two_runs_give_the_same_tree(self):
        self.run_prepare()
        first = self.tree_hash()
        self.run_prepare()
        self.assertEqual(self.tree_hash(), first)

    def test_an_unknown_form_stops_the_run_and_leaves_no_output(self):
        self.run_prepare()
        self.write("pages/docs/a/1/b/grammar.md", FRONT + "Text\n{: .more }\n")
        result = self.run_prepare()
        self.assertEqual(result.returncode, 1)
        self.assertIn("grammar.md:6:", result.stderr)
        self.assertIn("nothing written", result.stderr)
        self.assertFalse(os.path.exists(os.path.join(self.root, ".build/content/pages/docs")))
        self.assertFalse(os.path.exists(os.path.join(self.root, ".build/data")))

    def test_an_invalid_version_file_is_an_error_that_names_it(self):
        self.write("_data/versions.json", '{"versions": [')
        result = self.run_prepare()
        self.assertEqual(result.returncode, 1)
        self.assertIn("_data/versions.json", result.stderr)

    def test_a_version_without_a_dist_file_is_absent_from_the_second_map(self):
        self.run_prepare()
        with open(os.path.join(self.root, ".build/data/key_order.json"), encoding="utf-8") as handle:
            order = json.load(handle)
        self.assertNotIn("2026.2", order["system types"])


if __name__ == "__main__":
    unittest.main()
