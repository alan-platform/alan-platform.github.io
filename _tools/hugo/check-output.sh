#!/usr/bin/env bash
# Checks that the build in public/ is complete: _tools/hugo/check-output.sh [HUGO_LOG]
#
# Hugo exits 0 and writes a smaller site when a mount source is missing (no pages/docs, so the
# generated pages are absent), when a data glob matches nothing, and when a layout is missing (a
# warning, and the page is not written). Deploying that would publish an incomplete site, so
# build.sh runs this after Hugo, and the workflow with it before it uploads the artifact.
#
# HUGO_LOG is the output of the Hugo run (build.sh keeps it in a temporary file). Without it the
# check of the warnings is skipped.
#
# The page count comes from the source. The only number kept here is the floor of the sitemap.
set -uo pipefail

cd "$(dirname "$0")/../.." || exit 1

SITEMAP_FLOOR=3000
LOG=${1:-}
failures=0

fail() {
  echo "check-output: $*" >&2
  failures=$((failures + 1))
}

# 1. every generated page was written: one .html for each .md of pages/docs
sources=$(find pages/docs -name '*.md' | wc -l)
pages=$(find public/pages/docs -name '*.html' 2>/dev/null | wc -l)
if [ "$sources" -eq 0 ]; then
  fail "pages/docs has no .md files"
elif [ "$pages" -ne "$sources" ]; then
  fail "public/pages/docs has $pages .html files, pages/docs has $sources .md files"
fi

# 2. the pages and files that every deployment needs
for file in \
  index.html 404.html docs/index.html docs/archive.html learn/index.html about/index.html faq/index.html \
  deps/index.html deps/status.json sitemap.xml robots.txt CNAME \
  src/main.css src/main.js src/prism.min.js assets/fonts/ClearSans-Regular.woff; do
  if [ ! -f "public/$file" ]; then
    fail "public/$file is missing"
  fi
done

# 3. a rule block of a generated page carries its id (the generator writes it on the div)
grammar=public/pages/docs/model/109/application/grammar.html
if ! grep -q 'id="grammar-rule--node"' "$grammar" 2>/dev/null; then
  fail "$grammar lacks id=\"grammar-rule--node\""
fi

# 4. the sitemap lists the pages
locations=$(grep -o '<loc>' public/sitemap.xml 2>/dev/null | wc -l)
if [ "$locations" -lt "$SITEMAP_FLOOR" ]; then
  fail "public/sitemap.xml has $locations <loc> entries, fewer than $SITEMAP_FLOOR"
fi

# 5. Hugo warned about nothing but the deprecation of LibSass, which the stylesheet pipeline uses
if [ -n "$LOG" ]; then
  if [ ! -f "$LOG" ]; then
    fail "the Hugo log $LOG does not exist"
  else
    warnings=$(grep -E '^(WARN|ERROR)' "$LOG" | grep -vi 'libsass')
    if [ -n "$warnings" ]; then
      fail "Hugo reported:"
      while IFS= read -r line; do
        echo "  $line" >&2
      done <<< "$warnings"
    fi
  fi
else
  echo "check-output: no Hugo log given, the warnings are not checked" >&2
fi

# 6. no attribute syntax is left in the text of a page: {: anywhere, and a line that starts with {. or {#
# outside <pre>, where Goldmark would have taken it for a block attribute or shown it. This fails the
# build of a generator that writes a form Hugo does not read.
literal=$(grep -rlF --include='*.html' '{:' public/pages/docs 2>/dev/null | head -5)
if [ -n "$literal" ]; then
  fail "the text {: is left in built pages; the generator writes a form Hugo does not read:"
  while IFS= read -r page; do
    echo "  $page" >&2
  done <<< "$literal"
fi
leading=$(grep -rlE --include='*.html' '^[[:space:]]*\{[.#]' public/pages/docs 2>/dev/null | python3 -c '
import re
import sys

for line in sys.stdin:
    path = line.rstrip("\n")
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = re.sub(r"<pre\b.*?</pre>", "", handle.read(), flags=re.S)
    if re.search(r"^[ \t]*\{[.#]", text, re.M):
        print(path)
' | head -5)
if [ -n "$leading" ]; then
  fail "a line that starts with {. or {# is left in built pages, outside <pre>:"
  while IFS= read -r page; do
    echo "  $page" >&2
  done <<< "$leading"
fi

if [ "$failures" -ne 0 ]; then
  echo "check-output: $failures checks failed, the site is not complete" >&2
  exit 1
fi
echo "check-output: $pages generated pages, $locations sitemap entries, all required files present"
