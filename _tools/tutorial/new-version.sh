#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then echo "usage: $0 <new> [<prev>] [--force]" >&2; exit 2; fi
NEW=$1; FORCE=false; PREV=
[[ "$NEW" =~ ^[0-9]{4}\.[0-9]+$ ]] || { echo "error: <new> must look like 2026.2, got '$NEW'" >&2; exit 2; }
for x in "${@:2}"; do if [ "$x" = --force ]; then FORCE=true; elif [ -z "$PREV" ]; then PREV=$x; else echo "usage: $0 <new> [<prev>] [--force]" >&2; exit 2; fi; done
ROOT=$(cd "$(dirname "$0")/../.." && pwd); IDE="${ONLINE_IDE:-$ROOT/../online-ide}"; T="$IDE/docs/tutorials/restaurant1"
PREV=${PREV:-$(jq -r .current "$ROOT/_data/versions.json")}
[[ "$PREV" =~ ^[0-9]{4}\.[0-9]+$ ]] || { echo "error: <prev> must look like 2024.2, got '$PREV'" >&2; exit 2; }
[ "$PREV" != "$NEW" ] || { echo "error: <new> and <prev> are the same version" >&2; exit 2; }
WEB="$ROOT/pages/tutorials/model"; FAIL=(); CENSUS=ok; MIGRATION=ok; VERIFY=0
say() { echo "== step $1: $2" >&2; }
say A "prepare toolchain"
if [ -e "$WEB/$NEW" ] || [ -e "$T/$NEW" ]; then $FORCE || { echo "error: version exists" >&2; exit 1; }; rm -rf "$WEB/$NEW" "$T/$NEW"; fi
DEVENV=$("$ROOT/_tools/tutorial/fetch-toolchain.sh" "$NEW"); NEW_MODEL=$(jq -r .model "$DEVENV/platform/platform.json"); FROM_MODEL=$(awk '/^model_version:/{print $2; exit}' "$WEB/$PREV/application-tutorial.md")
say B "copy website tutorial"; cp -r "$WEB/$PREV" "$WEB/$NEW"; sed -i -E "s/^model_version: .*/model_version: $NEW_MODEL/; s/^platform_version: .*/platform_version: $NEW/" "$WEB/$NEW"/*.md
say C "copy online-ide tutorial"; rsync -a --exclude .alan --exclude CLAUDE.md --exclude AGENTS.md "$T/$PREV/" "$T/$NEW/"
if [ -f "$ROOT/.toolchains/$NEW/versions.json" ]; then cp "$ROOT/.toolchains/$NEW/versions.json" "$T/$NEW/.alanversions"; else curl -sSf "https://dist.alan-platform.com/share/versions/$NEW/versions.json" | jq '{"platform version": ."platform version", "system types": {datastore: ."system types".datastore}}' > "$T/$NEW/.alanversions"; fi
sed -i "s/^VERSION=.*/VERSION=\"$NEW\"/" "$T/$NEW/.alanscript"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
say D "upgrade models"; "$ROOT/_tools/tutorial/snippets.py" census "$NEW" > "$TMP/census-before.json"
for d in "$WEB/$NEW"/models/*; do "$ROOT/_tools/tutorial/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$d" || FAIL+=("website model: $d"); done
for d in "$T/$NEW"/step_*/to_model; do "$ROOT/_tools/tutorial/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$d" --pp || FAIL+=("online-ide model: $d"); done
"$ROOT/_tools/tutorial/snippets.py" census "$NEW" > "$TMP/census-after.json" || FAIL+=("census after transform")
# compare marker sequences, not line numbers: the transform may re-flow lines
jq 'map_values(.markers |= map(.[0:2]))' "$TMP/census-before.json" > "$TMP/census-before.seq.json"
jq 'map_values(.markers |= map(.[0:2]))' "$TMP/census-after.json" > "$TMP/census-after.seq.json"
if ! diff -u "$TMP/census-before.seq.json" "$TMP/census-after.seq.json" > "$TMP/census.diff"; then echo "error: marker census changed by transform:" >&2; cat "$TMP/census.diff" >&2; CENSUS=diff; FAIL+=("marker census"); fi
say E "upgrade migrations"; prev_step=
for step in "$T/$NEW"/step_*/; do [ -n "$prev_step" ] || prev_step=$step; "$ROOT/_tools/tutorial/upgrade-migration.sh" "$DEVENV" "$prev_step" "$step" || { FAIL+=("migration: $step"); MIGRATION=fail; }; prev_step=$step; done
say F "extract and verify"; "$ROOT/_tools/tutorial/snippets.py" extract "$NEW" --write || FAIL+=("extract"); "$ROOT/_tools/tutorial/snippets.py" verify "$NEW" --platform "$DEVENV" --reference "$IDE" || { VERIFY=1; FAIL+=("verify"); }
say F2 "online-ide test.sh (models and migrations for restaurant1/$NEW)"; (cd "$IDE" && ./test.sh "restaurant1/$NEW") || FAIL+=("online-ide test.sh restaurant1/$NEW")
say G "prose review"
echo "== prose review (file:line: text)"
{
  # 1. transform-driven: substrings that the model transform changed, looked up in the pages
  for d in "$WEB/$NEW"/models/*/; do
    name=$(basename "$d")
    [ -f "$WEB/$PREV/models/$name/application.alan" ] || continue
    python3 - "$WEB/$PREV/models/$name/application.alan" "$d/application.alan" <<'PY'
import difflib, re, sys
old = open(sys.argv[1], encoding="utf-8").read().splitlines()
new = open(sys.argv[2], encoding="utf-8").read().splitlines()
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag not in ("replace", "delete"):
        continue
    for k, o in enumerate(old[i1:i2]):
        n = new[j1 + k] if j1 + k < j2 else ""
        best = ""
        for t2, a1, a2, b1, b2 in difflib.SequenceMatcher(a=o, b=n, autojunk=False).get_opcodes():
            if t2 in ("replace", "delete") and a2 - a1 > len(best):
                best = o[a1:a2]
        best = re.sub(r"\s+", " ", best).strip()
        if len(best) >= 3:
            print(best)
PY
  done | sort -u | while IFS= read -r needle; do grep -nF -- "$needle" "$WEB/$NEW"/*.md || true; done
  # 2. inline fence lines that no model contains, new since the previous version
  # compare without page line numbers, which shift between versions
  { "$ROOT/_tools/tutorial/snippets.py" extract "$NEW" --check-inline 2>/dev/null || true; } | sed -E "s#^$WEB/$NEW/##; s/^([^:]*):[0-9]+:/\\1:/" | sort -u > "$TMP/inline-new.txt"
  { "$ROOT/_tools/tutorial/snippets.py" extract "$PREV" --check-inline 2>/dev/null || true; } | sed -E "s#^$WEB/$PREV/##; s/^([^:]*):[0-9]+:/\\1:/" | sort -u > "$TMP/inline-prev.txt"
  comm -23 "$TMP/inline-new.txt" "$TMP/inline-prev.txt"
  # 3. grammar tokens removed between the two model language versions
  OLD_G=$(git -C "$ROOT" show "HEAD:pages/docs/model/$FROM_MODEL/application/grammar.md" 2>/dev/null || true)
  NEW_G=$(cat "$ROOT/pages/docs/model/$NEW_MODEL/application/grammar.md" 2>/dev/null || git -C "$ROOT" show "HEAD:pages/docs/model/$NEW_MODEL/application/grammar.md" 2>/dev/null || true)
  if [ -z "$OLD_G" ] || [ -z "$NEW_G" ]; then
    echo "warning: grammar docs for model $FROM_MODEL or $NEW_MODEL unavailable; token diff skipped" >&2
  else
    comm -23 <(printf '%s\n' "$OLD_G" | grep -oE '`[^`]+`' | sort -u) <(printf '%s\n' "$NEW_G" | grep -oE '`[^`]+`' | sort -u) \
      | sed 's/^`//; s/`$//' | while IFS= read -r tok; do [ -n "$tok" ] && grep -nF -- "$tok" "$WEB/$NEW"/*.md || true; done
  fi
  # 4. migration workflow prose when the datastore major version changed
  OLD_DS=$(jq -r '."system types".datastore.version' "$T/$PREV/.alanversions" | cut -d. -f1); NEW_DS=$(jq -r '."system types".datastore.version' "$T/$NEW/.alanversions" | cut -d. -f1)
  if [ "$OLD_DS" != "$NEW_DS" ]; then grep -nE 'regexp\.alan|from_release|from-release|migration\.alan|[Mm]igrat' "$WEB/$NEW"/*.md || true; fi
} | sed "s#^$WEB/$NEW/##" | sort -u
echo "== compile/transform failures"; [ "${#FAIL[@]}" -eq 0 ] && echo ok || printf '%s\n' "${FAIL[@]}"
echo "== census"; echo "$CENSUS"; echo "== migrations"; echo "$MIGRATION"; echo "== verify"; echo "$VERIFY"
echo "_data/versions.json \"current\" is still $PREV; promote in a separate commit when ready"
[ -d "$ROOT/pages/tutorials/migrations/$NEW" ] || echo "pages/tutorials/migrations/$NEW missing (docs.md links it via current); needs its own rewrite"
echo "commit with explicit paths (pages/tutorials/model/$NEW, and in online-ide docs/tutorials/restaurant1/$NEW)"
[ "${#FAIL[@]}" -eq 0 ]
