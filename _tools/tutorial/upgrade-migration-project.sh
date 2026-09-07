#!/usr/bin/env bash
# Upgrade one migration project of the migrations tutorial (pages/tutorials/migrations/<v>/models/<dir>):
# the source and target models go through the platform's model transform, migration.alan is compiled with the
# new migration language and, when that fails and the platform ships a matching upgrade config, upgraded in place.
set -uo pipefail
if [ "$#" -ne 4 ]; then echo "usage: $0 <devenv> <from-model-version> <from-datastore-version> <migration-project-dir>" >&2; exit 2; fi
DEVENV=$1; FROM_MODEL=$2; FROM_DS=$3; DIR=$(cd "$4" && pwd); MIG="$DIR/migration.alan"
HERE=$(cd "$(dirname "$0")" && pwd)
COMP="$DEVENV/platform/project-compiler/tools/compiler-project"; MIG_LANG="$DEVENV/system-types/datastore/migration/language"; PP="$DEVENV/platform/project-compiler/tools/pretty-printer"
UPG="$DEVENV/system-types/datastore/scripts/upgrade"
[ -f "$MIG" ] || { echo "$MIG:1:1: error: not a migration project (no migration.alan)" >&2; exit 2; }
rc=0
for sub in source target; do
  [ -f "$DIR/models/$sub/application.alan" ] || continue
  "$HERE/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$DIR/models/$sub" || rc=1
done
[ $rc -eq 0 ] || exit $rc
compile() { "$COMP" "$MIG_LANG" --format vscode -C "$DIR" /dev/null 2>&1; }
report() { printf '%s\n' "$1" | sed -E '/^[[:space:]]*$/d; s/ to [0-9]+:[0-9]+//' | grep -v 'annotation package' >&2; }
# a migration with '//@ expect error <text>' is up to date when the new compiler reports that text
EXPECT=$(sed -nE 's#^[[:space:]]*//@[[:space:]]+expect[[:space:]]+error[[:space:]]+(.*)$#\1#p' "$MIG" | head -n1)
OUT=$(compile); CODE=$?
if [ -n "$EXPECT" ]; then
  if printf '%s' "$OUT" | grep -qF -- "$EXPECT"; then exit 0; fi
  echo "$MIG:1:1: error: migration has '//@ expect error' and does not yet fail with that text under the new language; upgrade it by hand" >&2
  report "$OUT" | head -n 5; exit 1
fi
[ "$CODE" -ne 0 ] || exit 0
CFG=""
for cand in "from-migration-$FROM_DS" "from-migration-${FROM_DS%%.*}"; do
  if [ -e "$UPG/configs/$cand/package" ]; then CFG=${cand#from-migration-}; break; fi
done
if [ -z "$CFG" ]; then
  AVAIL=$(ls "$UPG/configs" 2>/dev/null | tr '\n' ' ')
  echo "$MIG:1:1: error: does not compile under the new migration language and no upgrade config from datastore $FROM_DS exists (available: $AVAIL); upgrade by hand" >&2
  report "$OUT" | head -n 5; exit 1
fi
"$UPG/upgrade_migration.sh" "$CFG" "$DIR" || { echo "$MIG:1:1: error: MIGRATION-UPGRADE-FAILED (config from-migration-$CFG)" >&2; exit 1; }
"$PP" "$MIG_LANG" -C "$DIR"
OUT=$(compile); CODE=$?
[ "$CODE" -eq 0 ] || report "$OUT"
exit "$CODE"
