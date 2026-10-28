#!/usr/bin/env bash
# Build the site into public/, or serve it with live reload:
#
#   _tools/hugo/build.sh                 rewrite the generated pages, build, check the output
#   _tools/hugo/build.sh serve [FLAGS]   rewrite, then hugo server with the given flags
#
# HUGO names the binary when it is not on the PATH. The script changes to the repository
# root first, from its own location: hugo.toml, its mount sources and the output of
# prepare.py are relative to it, so Hugo must run there whatever directory the caller is in.
set -euo pipefail

mode=${1:-build}
if [ "$mode" != build ] && [ "$mode" != serve ]; then
  echo "usage: $0 [build | serve [hugo server flags]]" >&2
  exit 2
fi

cd "$(dirname "$0")/../.."

HUGO=${HUGO:-hugo}

python3 _tools/hugo/prepare.py

if [ "$mode" = serve ]; then
  shift
  # in memory: hugo server would otherwise write a development build into public/
  "$HUGO" server --renderToMemory "$@"
else
  # public/ is emptied first, so it holds exactly this build. The output is kept in a log:
  # Hugo exits 0 when it warns that it wrote less than it should, and check-output.sh reads the log.
  mkdir -p .build
  "$HUGO" --cleanDestinationDir 2>&1 | tee .build/hugo.log
  _tools/hugo/check-output.sh .build/hugo.log
fi
