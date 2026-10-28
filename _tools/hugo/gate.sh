#!/usr/bin/env bash
# The parity gate of the Hugo port: compares a full Jekyll build of the last Jekyll commit (tag jekyll-last)
# with the Hugo build in public/, and fails on any difference that is not listed here.
#
#   _tools/hugo/gate.sh JEKYLL_SITE_DIR [compare.py options]
#
# Every allowed difference below is a deliberate one, with its reason. Add a line only with a reason.
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 JEKYLL_SITE_DIR [compare.py options]" >&2
  exit 2
fi
baseline=$1
shift

cd "$(dirname "$0")/../.."

allowed=(
  # Six connector processor grammars that kramdown rendered broken: a <begin> and <end> inside a rule block made
  # it print a closing tag and the attribute line of the next rule as text, and lose the ids of two rules.
  # Hugo renders them correctly, so their text and ids differ from the baseline.
  --allow-diff "2:pages/docs/connector/39/processor/grammar.html"
  --allow-diff "4b:pages/docs/connector/39/processor/grammar.html"
  --allow-diff "2:pages/docs/connector/40/processor/grammar.html"
  --allow-diff "4b:pages/docs/connector/40/processor/grammar.html"
  --allow-diff "2:pages/docs/connector/partitions-108.4/processor/grammar.html"
  --allow-diff "4b:pages/docs/connector/partitions-108.4/processor/grammar.html"
  --allow-diff "2:pages/docs/connector/partitions-108.4.2/processor/grammar.html"
  --allow-diff "4b:pages/docs/connector/partitions-108.4.2/processor/grammar.html"
  --allow-diff "2:pages/docs/connector/partitions-108.5/processor/grammar.html"
  --allow-diff "4b:pages/docs/connector/partitions-108.5/processor/grammar.html"
  --allow-diff "2:pages/docs/connector/partitions-108.6/processor/grammar.html"
  --allow-diff "4b:pages/docs/connector/partitions-108.6/processor/grammar.html"
  # Two release notes with a code span that ends in a space: kramdown dropped the space, Goldmark keeps it.
  --allow-diff "2:pages/docs/model/109/release-notes.html"
  --allow-diff "2:pages/docs/model/partitions-108.6/release-notes.html"
  # The 404 page is titled "404" as on the live site, where GitHub's Jekyll took the title from its heading
  # (jekyll-titles-from-headings); the local Jekyll build the baseline comes from did not run that plugin.
  --allow-diff "3:404.html"
  # The home page refers to its images as /assets/...; the Jekyll template used a filter that does not exist
  # and left the paths relative, which only worked because the page sits at the root.
  --allow-diff "5:index.html"
)

exec python3 _tools/hugo/compare.py "${allowed[@]}" "$@" "$baseline" public
