#!/usr/bin/env bash
set -uo pipefail
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ] || { [ "$#" -eq 4 ] && [ "$4" != --pp ]; }; then echo "usage: $0 <devenv> <from-model-version> <model-dir> [--pp]" >&2; exit 2; fi
DEVENV=$1; FROM=$2; DIR=$(cd "$3" && pwd); APP="$DIR/application.alan"
COMP="$DEVENV/platform/project-compiler/tools/compiler-project"; MODEL_LANG="$DEVENV/platform/if-types/model/language"; PP="$DEVENV/platform/project-compiler/tools/pretty-printer"
if ! "$COMP" "$MODEL_LANG" -C "$DIR" /dev/null >/dev/null 2>&1; then
  CFG="$DEVENV/platform/if-types/model/scripts/transform/configs/$FROM/package"
  if [ ! -e "$CFG" ]; then
    AVAIL=$(ls "$DEVENV/platform/if-types/model/scripts/transform/configs" 2>/dev/null | tr '\n' ' ')
    echo "$APP:1:1: error: no transform config $FROM; available: $AVAIL" >&2; exit 2
  fi
  "$DEVENV/platform/if-types/model/scripts/transform/transform.sh" "$FROM" "$DIR" || { echo "$APP:1:1: error: TRANSFORM-FAILED (input does not parse under model $FROM?)" >&2; exit 1; }
fi
[ "${4:-}" != --pp ] || "$PP" "$MODEL_LANG" -C "$DIR"
OUT=$("$COMP" "$MODEL_LANG" --format vscode -C "$DIR" /dev/null 2>&1); CODE=$?
if [ "$CODE" -ne 0 ]; then printf '%s\n' "$OUT" | sed -E '/^[[:space:]]*$/d; s/ to [0-9]+:[0-9]+//' >&2; exit "$CODE"; fi
