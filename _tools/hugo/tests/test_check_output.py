"""Tests of check-output.sh on a small synthetic repository and build.

Run from the repository root: python3 -m unittest discover -s _tools/hugo/tests
"""

import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(os.path.dirname(HERE), "check-output.sh")

REQUIRED = [
    "index.html", "404.html", "docs/index.html", "docs/archive.html", "learn/index.html", "about/index.html",
    "faq/index.html", "deps/index.html", "deps/status.json", "sitemap.xml", "robots.txt", "CNAME",
    "src/main.css", "src/main.js", "src/prism.min.js", "assets/fonts/ClearSans-Regular.woff",
]
GRAMMAR = "pages/docs/model/109/application/grammar"
PAGES = ["pages/docs/a", "pages/docs/b/c", GRAMMAR]
LIBSASS = "WARN  deprecated: css.Sass: libsass was deprecated in Hugo v0.153.0 and will be removed in a future release."


class CheckOutput(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.root, ignore_errors=True))
        os.makedirs(os.path.join(self.root, "_tools/hugo"))
        shutil.copy(SCRIPT, os.path.join(self.root, "_tools/hugo/check-output.sh"))
        for page in PAGES:
            self.write(page + ".md", "text\n")
            self.write("public/" + page + ".html", '<div id="grammar-rule--node">x</div>\n' if page == GRAMMAR else "x\n")
        for name in REQUIRED:
            self.write("public/" + name, "x\n")
        self.write("public/sitemap.xml", "<urlset>" + "<url><loc>https://x.test/p</loc></url>\n" * 3000 + "</urlset>")
        self.write("hugo.log", "Start building sites\n" + LIBSASS + "\n")

    def write(self, relative, text):
        path = os.path.join(self.root, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def run_check(self, log="hugo.log"):
        arguments = ["bash", os.path.join(self.root, "_tools/hugo/check-output.sh")]
        if log:
            arguments.append(os.path.join(self.root, log))
        return subprocess.run(arguments, capture_output=True, text=True)

    def assertFails(self, expected):
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(expected, result.stderr)
        return result

    def test_a_complete_build_passes(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("3 generated pages", result.stdout)

    def test_each_required_file(self):
        for name in REQUIRED:
            with self.subTest(name):
                path = os.path.join(self.root, "public", name)
                os.rename(path, path + ".off")
                self.assertFails("public/%s is missing" % name)
                os.rename(path + ".off", path)

    def test_page_count_comes_from_the_source(self):
        self.write("pages/docs/d.md", "text\n")
        self.assertFails("has 3 .html files, pages/docs has 4 .md files")

    def test_missing_rule_id(self):
        self.write("public/" + GRAMMAR + ".html", "<div>x</div>\n")
        self.assertFails('lacks id="grammar-rule--node"')

    def test_sitemap_floor(self):
        self.write("public/sitemap.xml", "<urlset>" + "<url><loc>https://x.test/p</loc></url>\n" * 2999 + "</urlset>")
        self.assertFails("2999 <loc> entries")

    def test_hugo_warnings(self):
        self.write("hugo.log", LIBSASS + "\nWARN  found no layout file for \"html\" for kind \"page\"\n")
        result = self.assertFails("Hugo reported:")
        self.assertIn("found no layout file", result.stderr)
        self.assertNotIn("libsass", result.stderr)
        self.write("hugo.log", "ERROR something\n")
        self.assertFails("ERROR something")

    def test_log_that_does_not_exist(self):
        result = self.run_check("nothing.log")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not exist", result.stderr)

    def test_without_a_log_the_warnings_are_not_checked(self):
        result = self.run_check(None)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("not checked", result.stderr)

    def test_kramdown_attribute_syntax_left_in_a_page(self):
        self.write("public/pages/docs/a.html", "<p>text</p>\n{: #id }\n")
        self.assertFails("the text {: is left")

    def test_kramdown_attribute_syntax_left_in_code_too(self):
        self.write("public/pages/docs/a.html", "<pre>{: #id }</pre>\n")
        self.assertFails("the text {: is left")

    def test_goldmark_attribute_line_outside_pre(self):
        self.write("public/pages/docs/a.html", "<p>text</p>\n{.class}\n")
        self.assertFails("{. or {#")
        self.write("public/pages/docs/a.html", "<p>text</p>\n  {#id}\n")
        self.assertFails("{. or {#")

    def test_goldmark_attribute_line_inside_pre_is_code(self):
        self.write("public/pages/docs/a.html", "<pre class=\"x\">\n{.class}\n{#id}\n</pre>\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_curly_brace_text_that_is_not_attribute_syntax(self):
        self.write("public/pages/docs/a.html", "<p>a { b } and {x} and { #y }</p>\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
