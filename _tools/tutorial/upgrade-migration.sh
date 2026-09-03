#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 3 ]; then echo "usage: $0 <devenv> <prev-step-dir> <step-dir>" >&2; exit 2; fi
DEVENV=$1; PREV=$(cd "$2" && pwd); STEP=$(cd "$3" && pwd); MIG="$STEP/migration/migration.alan"
if head -n1 "$MIG" | grep -q '^root = root as \$ {'; then echo "skip (already new syntax): $MIG" >&2; exit 0; fi
# The upgrade tool rejects extra files inside the migration project, so the target model lives in a sibling dir.
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
PROJ="$TMP/migration"; mkdir -p "$PROJ/from" "$PROJ/to" "$TMP/target"
cp "$PREV/to_model/application.alan" "$PROJ/from/application.alan"
cp "$STEP/to_model/application.alan" "$TMP/target/application.alan"
printf '%s' '../../target/application.alan' > "$PROJ/to/application.alan.link"
: > "$PROJ/regexp.alan"; cp "$MIG" "$PROJ/migration.alan"
"$DEVENV/system-types/datastore/scripts/upgrade/upgrade_migration.sh" legacy "$PROJ"
PP="$DEVENV/platform/project-compiler/tools/pretty-printer"; MIG_LANG="$DEVENV/system-types/datastore/migration/language"; COMP="$DEVENV/platform/project-compiler/tools/compiler-project"
"$PP" "$MIG_LANG" -C "$PROJ"
OUT=$("$COMP" "$MIG_LANG" --format vscode -C "$PROJ" /dev/null 2>&1) || { printf '%s\n' "$OUT" | sed -E '/^[[:space:]]*$/d; s/ to [0-9]+:[0-9]+//' >&2; exit 1; }
cp "$PROJ/migration.alan" "$MIG"
