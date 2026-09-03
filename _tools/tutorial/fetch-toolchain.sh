#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo "usage: $0 <platform-version>" >&2; exit 2; fi
V=$1
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
if [ -n "${ALAN_DEVENV:-}" ]; then
  if [ ! -f "$ALAN_DEVENV/platform/platform.json" ]; then echo "error: ALAN_DEVENV has no platform/platform.json" >&2; exit 1; fi
  [ -d "$ALAN_DEVENV/system-types/datastore/migration/language" ] || echo "warning: datastore migration language missing" >&2
  printf '%s\n' "$ALAN_DEVENV"; exit 0
fi
CACHE="$ROOT/.toolchains/$V"
DEVENV="$CACHE/.alan/devenv"
if [ -x "$DEVENV/platform/project-compiler/tools/compiler-project" ] && [ -d "$DEVENV/system-types/datastore/migration/language" ]; then printf '%s\n' "$DEVENV"; exit 0; fi
mkdir -p "$CACHE"; cd "$CACHE"
curl -sSf "https://dist.alan-platform.com/share/versions/$V/versions.json" | jq '{"platform version": ."platform version", "system types": {datastore: ."system types".datastore}}' > versions.json
curl -sSf "https://dist.alan-platform.com/share/alan/alan-$V-linux-x64.tar.gz" | tar xzf -
rm -f CLAUDE.md AGENTS.md
./alan fetch
rm -f CLAUDE.md AGENTS.md
[ -x "$DEVENV/platform/project-compiler/tools/compiler-project" ] || { echo "error: compiler missing after fetch" >&2; exit 1; }
printf '%s\n' "$DEVENV"
