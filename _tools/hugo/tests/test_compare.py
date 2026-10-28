"""Tests of compare.py on small synthetic sites: what the gate accepts, and what it reports in which category.

Run from the repository root: python3 -m unittest discover -s _tools/hugo/tests
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
COMPARE = os.path.join(os.path.dirname(HERE), "compare.py")

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://x.test/{name}">
<link rel="stylesheet" href="{css}">
<script>var tag = {inline};</script>
</head>
<body><main>
<h1 id="top">Title</h1>
<h2 id="{h2id}">{h2}</h2>
<p>{text}</p>
<p>{links}</p>
<pre class="highlight"><code>{pre}</code></pre>
<script src="{script}"></script>
</main></body></html>
"""

DEFAULT_PAGE = dict(
    title="Alan",
    description="About Alan",
    css="/src/main.css?100",
    inline="1",
    h2id="intro",
    h2="Intro",
    text="Hello world",
    links='<a href="/other.html">Other</a> <a href="/b.html#sec">B</a> <a href="/a%20b.html">Spaced</a>',
    pre="line one\n\tline two\n",
    script="/src/main.js?100",
)

CSS = "a{color:red;margin:0.5em}li:nth-child(4n+1){top:0}.x{font:12px/1.5 a}\n"
SITEMAP = '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>'


def page(name="index.html", **changes):
    fields = dict(DEFAULT_PAGE, name=name, **changes)
    return TEMPLATE.format(**fields)


def default_files():
    return {
        "index.html": page(),
        "other.html": page("other.html", title="Other", h2id="o", h2="O", links=""),
        "b.html": page("b.html", title="B", h2id="sec", h2="Sec", links=""),
        "a b.html": page("a b.html", title="Spaced", h2id="s", h2="S", links=""),
        "src/main.css": CSS,
        "src/main.js": "var x = 1;\n",
        "sitemap.xml": SITEMAP % "<url><loc>https://x.test/</loc></url><url><loc>https://x.test/other.html</loc></url>",
        "robots.txt": "User-agent: *\nAllow: /\n",
        "CNAME": "x.test\n",
        "assets/x.bin": b"\x00\x01\x02",
    }


class Gate(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.root, ignore_errors=True))
        self.baseline = self.build("baseline", {"feed.xml": "<feed/>", "README.md": "# r", "LICENSE": "l"})

    def build(self, name, changes=None):
        """Write a site; a change maps a path to new content, or to None to leave the file out."""
        files = default_files()
        for path, content in (changes or {}).items():
            if content is None:
                files.pop(path, None)
            else:
                files[path] = content
        directory = os.path.join(self.root, name)
        for path, content in files.items():
            target = os.path.join(directory, path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(content if isinstance(content, bytes) else content.encode("utf-8"))
        return directory

    def compare(self, changes=None, *args):
        """Compare the baseline with a Hugo site that has the changes; return (exit code, counts, output)."""
        self.hugo_count = getattr(self, "hugo_count", 0) + 1
        hugo = self.build("hugo%d" % self.hugo_count, changes)
        result = subprocess.run(
            [sys.executable, COMPARE, self.baseline, hugo, "--jobs", "1", *args], capture_output=True, text=True
        )
        counts = {}
        for line in result.stdout.splitlines():
            match = re.match(r"^(\d[ab]?)\s{2,}[a-z ]+?\s{2,}(\d+)$", line)
            if match:
                counts[match.group(1)] = int(match.group(2))
        return result.returncode, counts, result.stdout

    def assertPasses(self, changes=None, *args):
        code, counts, output = self.compare(changes, *args)
        self.assertEqual(code, 0, output)
        return output

    def assertOnly(self, category, changes=None, *args):
        """The gate fails, and only the given category has differences."""
        code, counts, output = self.compare(changes, *args)
        self.assertEqual(code, 1, output)
        self.assertEqual({key for key, count in counts.items() if count}, {category}, output)
        return output

    # allowed differences

    def test_identical_sites_pass(self):
        self.assertPasses()

    def test_feed_readme_and_license_may_be_missing(self):
        self.assertPasses()

    def test_cache_buster_value_and_encoded_space(self):
        self.assertPasses(
            {
                "index.html": page(css="/src/main.css?9999", script="/src/main.js?5").replace("/a%20b.html", "/a b.html"),
            }
        )

    def test_whitespace_between_blocks_and_token_spans(self):
        self.assertPasses({"index.html": page(text="Hello world", pre="<span>line</span> one\n\tline two\n").replace("</p>", "</p>\n\n\n  ")})

    def test_css_spellings_of_the_two_sass_compilers(self):
        self.assertPasses({"src/main.css": "a{color:red;margin:.5em}li:nth-child(4n + 1){top:0}.x{font:12px / 1.5 a}\n"})

    # a <pre> block

    def pre(self, text):
        return {"index.html": page(pre=text)}

    def test_pre_indented_by_the_item_of_a_list_passes(self):
        base = "a\n\tb\n"
        self.baseline = self.build("baseline2", {"index.html": page(pre="  a\n  \tb\n")})
        self.assertPasses(self.pre(base))
        self.baseline = self.build("baseline3", {"index.html": page(pre="  a\n  \tb\n")})
        self.assertPasses(self.pre("\ta\n\t\tb\n"))

    def test_pre_with_one_line_indented_differently_fails(self):
        self.assertOnly("2", self.pre("line one\n\t line two\n"))
        self.assertOnly("2", self.pre(" line one\n\tline two\n"))

    def test_pre_with_a_changed_or_missing_line_fails(self):
        self.assertOnly("2", self.pre("line 1\n\tline two\n"))
        self.assertOnly("2", self.pre("line one\n"))

    # the categories

    def test_missing_file(self):
        output = self.assertOnly("1", {"CNAME": None})
        self.assertIn("CNAME", output)

    def test_file_only_in_hugo_fails_with_strict(self):
        self.assertPasses({"extra.txt": "x"})
        self.assertOnly("1", {"extra.txt": "x"}, "--strict")

    def test_text(self):
        self.assertOnly("2", {"index.html": page(text="Hello there")})

    def test_head(self):
        self.assertOnly("3", {"index.html": page(description="Other words")})
        self.assertOnly("3", {"index.html": page(title="Alan 2")})

    def test_scripts_and_stylesheets_in_order(self):
        self.assertOnly("3", {"index.html": page(inline="2")})
        self.assertOnly("3", {"index.html": page(css="/src/other.css?1"), "src/other.css": "x"})

    def test_headings_and_ids(self):
        # the heading text is body text as well
        code, counts, output = self.compare({"index.html": page(h2="Other heading")})
        self.assertEqual((code, counts["2"], counts["4a"], counts["4b"]), (1, 1, 1, 0), output)
        self.assertIn("Other heading", output)
        code, counts, output = self.compare({"index.html": page(h2id="changed")})
        self.assertEqual((code, counts["2"], counts["4a"], counts["4b"]), (1, 0, 1, 1), output)

    def test_swapped_links_pass_the_set_but_not_the_order(self):
        swapped = page(links='<a href="/b.html#sec">Other</a> <a href="/other.html">B</a> <a href="/a%20b.html">Spaced</a>')
        output = self.assertOnly("5", {"index.html": swapped})
        self.assertIn("other links or order", output)

    def test_a_new_link_is_a_difference_of_the_set(self):
        self.assertOnly("5", {"index.html": page(links=DEFAULT_PAGE["links"] + ' <a href="https://x.test/new"></a>')})

    def test_link_broken_only_in_hugo(self):
        gone = page(links=DEFAULT_PAGE["links"] + ' <a href="/gone.html"></a>')
        output = self.assertOnly("6", {"index.html": gone}, "--allow-diff", "5:index.html")
        self.assertIn("/gone.html", output)
        self.assertOnly("6", {"index.html": page(links=DEFAULT_PAGE["links"] + ' <a href="/b.html#nothere"></a>')}, "--allow-diff", "5:index.html")

    def test_link_broken_in_both_builds_is_not_counted(self):
        both = {"index.html": page(links=DEFAULT_PAGE["links"] + ' <a href="/gone.html">Gone</a>')}
        self.baseline = self.build("baseline2", both)
        output = self.assertPasses(both)
        self.assertIn("broken in both builds", output)

    def test_css(self):
        self.assertOnly("7", {"src/main.css": CSS.replace("red", "blue")})

    def test_sitemap_and_robots(self):
        self.assertOnly("8", {"sitemap.xml": SITEMAP % "<url><loc>https://x.test/</loc></url>"})
        self.assertOnly("8", {"robots.txt": "User-agent: *\nDisallow: /\n"})

    def test_static_file_bytes(self):
        self.assertOnly("9", {"assets/x.bin": b"\x00\x01\x03"})

    # the allowlist

    def test_allow_diff_accepts_one_category_on_matching_paths(self):
        change = {"index.html": page(text="Hello there")}
        output = self.assertPasses(change, "--allow-diff", "2:index.*")
        self.assertIn("allowed by --allow-diff", output)
        self.assertOnly("2", change, "--allow-diff", "3:index.html")

    def test_allow_diff_matches_the_whole_reference_of_a_link(self):
        long_reference = "/gone-" + "long-" * 60 + ".html"
        change = {"index.html": page(links=DEFAULT_PAGE["links"] + ' <a href="%s"></a>' % long_reference)}
        self.assertOnly("6", change, "--allow-diff", "5:index.html")
        code, _, output = self.compare(change, "--allow-diff", "5:index.html", "--allow-diff", "6:/gone-long-*")
        self.assertEqual(code, 0, output)

    def test_allow_leaves_a_file_out_of_every_category(self):
        self.assertPasses({"index.html": page(text="Hello there", title="x")}, "--allow", "index.html")

    def test_fold_quotes(self):
        self.baseline = self.build("baseline2", {"index.html": page(text="it ‘x’ is")})
        change = {"index.html": page(text="it ’x’ is")}
        self.assertOnly("2", change)
        self.assertPasses(change, "--fold-quotes")


if __name__ == "__main__":
    unittest.main()
