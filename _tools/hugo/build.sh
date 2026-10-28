#!/usr/bin/env bash
# Build the site into public/, or serve it with live reload:
#
#   _tools/hugo/build.sh                 build, then check the output
#   _tools/hugo/build.sh serve [FLAGS]   hugo server with the given flags
#
# HUGO names the binary when it is not on the PATH. The script changes to the repository
# root first, from its own location: hugo.toml and its mount sources are relative to it,
# so Hugo must run there whatever directory the caller is in.
set -euo pipefail

mode=${1:-build}
if [ "$mode" != build ] && [ "$mode" != serve ]; then
  echo "usage: $0 [build | serve [hugo server flags]]" >&2
  exit 2
fi

cd "$(dirname "$0")/../.."

HUGO=${HUGO:-hugo}

if [ "$mode" = serve ]; then
  shift
  # in memory: hugo server would otherwise write a development build into public/
  "$HUGO" server --renderToMemory "$@"
else
  # public/ is emptied first, so it holds exactly this build. The output is kept in a log:
  # Hugo exits 0 when it warns that it wrote less than it should, and check-output.sh reads the log.
  log=$(mktemp)
  trap 'rm -f "$log"' EXIT
  "$HUGO" --cleanDestinationDir 2>&1 | tee "$log"
  _tools/hugo/check-output.sh "$log"
fi
