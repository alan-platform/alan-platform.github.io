#!/usr/bin/env bash
set -uo pipefail
if [ "$#" -lt 3 ] || [ "$#" -gt 4 ] || { [ "$#" -eq 4 ] && [ "$4" != --pp ]; }; then echo "usage: $0 <devenv> <from-model-version> <model-dir> [--pp]" >&2; exit 2; fi
DEVENV=$1; FROM=$2; DIR=$(cd "$3" && pwd); APP="$DIR/application.alan"
COMP="$DEVENV/platform/project-compiler/tools/compiler-project"; MODEL_LANG="$DEVENV/platform/if-types/model/language"; PP="$DEVENV/platform/project-compiler/tools/pretty-printer"
# a model with '//@ expect error <text>' is meant to fail: it is up to date when the new compiler reports that text
EXPECT=$(sed -nE 's#^[[:space:]]*//@[[:space:]]+expect[[:space:]]+error[[:space:]]+(.*)$#\1#p' "$APP" | head -n1)
if [ -n "$EXPECT" ]; then
  OUT=$("$COMP" "$MODEL_LANG" --format vscode -C "$DIR" /dev/null 2>&1)
  if printf '%s' "$OUT" | grep -qF -- "$EXPECT"; then exit 0; fi
  echo "$APP:1:1: error: model has '//@ expect error' and does not yet fail with that text under the new language; the transform cannot process a failing model, upgrade it by hand" >&2
  printf '%s\n' "$OUT" | sed -E '/^[[:space:]]*$/d; s/ to [0-9]+:[0-9]+//' | head -n 5 >&2
  exit 1
fi
if ! "$COMP" "$MODEL_LANG" -C "$DIR" /dev/null >/dev/null 2>&1; then
  # since 2026.3 a bundle ships upgrade/<old version>/package, run with upgrade/template-engine (as ./alan upgrade
  # does); before that the model shipped scripts/transform/configs/<old version>, run with scripts/transform/transform.sh
  BUNDLE="$DEVENV/platform/if-types/model"
  if [ -e "$BUNDLE/upgrade/$FROM/package" ] && [ -x "$BUNDLE/upgrade/template-engine" ]; then
    "$BUNDLE/upgrade/template-engine" "$BUNDLE/upgrade/$FROM/package" "$DIR" "$DIR" -- || { echo "$APP:1:1: error: TRANSFORM-FAILED (input does not parse under model $FROM?)" >&2; exit 1; }
  elif [ -e "$BUNDLE/scripts/transform/configs/$FROM/package" ]; then
    "$BUNDLE/scripts/transform/transform.sh" "$FROM" "$DIR" || { echo "$APP:1:1: error: TRANSFORM-FAILED (input does not parse under model $FROM?)" >&2; exit 1; }
  else
    AVAIL=$(ls "$BUNDLE/upgrade" "$BUNDLE/scripts/transform/configs" 2>/dev/null | grep -v -e '^$' -e ':$' -e template-engine | tr '\n' ' ')
    echo "$APP:1:1: error: no transform from model $FROM; available: $AVAIL" >&2; exit 2
  fi
fi
[ "${4:-}" != --pp ] || "$PP" "$MODEL_LANG" -C "$DIR"
OUT=$("$COMP" "$MODEL_LANG" --format vscode -C "$DIR" /dev/null 2>&1); CODE=$?
if [ "$CODE" -ne 0 ]; then printf '%s\n' "$OUT" | sed -E '/^[[:space:]]*$/d; s/ to [0-9]+:[0-9]+//' >&2; exit "$CODE"; fi
