#!/usr/bin/env bash
# Produce a new platform version of the tutorials in this repo and in online-ide:
#   pages/tutorials/model/<new>       copied from <prev>, models upgraded with the platform's model transform
#   pages/tutorials/migrations/<new>  copied from <prev>, migration projects upgraded (models + migration language)
#   pages/tutorials/mission/<new>     copied from <prev>, models upgraded with the model transform
#   online-ide docs/tutorials/{restaurant1,mission-control}/<new>   step models transformed, step migrations converted
# then snippets are regenerated, everything is verified, and a report lists what still needs a human.
set -euo pipefail
if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then echo "usage: $0 <new> [<prev>] [--force]" >&2; exit 2; fi
NEW=$1; FORCE=false; PREV=
[[ "$NEW" =~ ^[0-9]{4}\.[0-9]+$ ]] || { echo "error: <new> must look like 2026.2, got '$NEW'" >&2; exit 2; }
for x in "${@:2}"; do if [ "$x" = --force ]; then FORCE=true; elif [ -z "$PREV" ]; then PREV=$x; else echo "usage: $0 <new> [<prev>] [--force]" >&2; exit 2; fi; done
ROOT=$(cd "$(dirname "$0")/../.." && pwd); TOOLS="$ROOT/_tools/tutorial"; IDE="${ONLINE_IDE:-$ROOT/../online-ide}"; T="$IDE/docs/tutorials/restaurant1"; TM="$IDE/docs/tutorials/mission-control"
PREV=${PREV:-$(jq -r .current "$ROOT/_data/versions.json")}
[[ "$PREV" =~ ^[0-9]{4}\.[0-9]+$ ]] || { echo "error: <prev> must look like 2024.2, got '$PREV'" >&2; exit 2; }
[ "$PREV" != "$NEW" ] || { echo "error: <new> and <prev> are the same version" >&2; exit 2; }
WEB="$ROOT/pages/tutorials/model"; MIG="$ROOT/pages/tutorials/migrations"; MSN="$ROOT/pages/tutorials/mission"; FAIL=(); CENSUS=ok; MIGRATION=ok; VERIFY=0
say() { echo "== step $1: $2" >&2; }
dist_field() { # <version> <jq path> : read from _data/dist/<version>/versions.json, else from the fetched toolchain, else empty
  local v=$1 q=$2 f
  for f in "$ROOT/_data/dist/$v/versions.json" "$ROOT/.toolchains/$v/versions.json" "$ROOT/.toolchains/$v/.alan/.versions-fetched.json"; do
    if [ -f "$f" ]; then jq -r "$q // empty" "$f"; return 0; fi
  done
  return 0
}

say A "prepare toolchain"
for d in "$WEB/$NEW" "$MIG/$NEW" "$MSN/$NEW" "$T/$NEW" "$TM/$NEW"; do
  if [ -e "$d" ]; then $FORCE || { echo "error: $d exists (use --force to replace)" >&2; exit 1; }; rm -rf "$d"; fi
done
DEVENV=$("$TOOLS/fetch-toolchain.sh" "$NEW"); NEW_MODEL=$(jq -r .model "$DEVENV/platform/platform.json")
FROM_MODEL=$(awk '/^model_version:/{print $2; exit}' "$WEB/$PREV/application-tutorial.md")
PREV_DS=$(dist_field "$PREV" '."system types".datastore.version'); [ -n "$PREV_DS" ] || PREV_DS=$(jq -r '."system types".datastore.version' "$T/$PREV/.alanversions")
NEW_DS=$(dist_field "$NEW" '."system types".datastore.version'); [ -n "$NEW_DS" ] || NEW_DS=$(jq -r '."system types".datastore.version' "$DEVENV/../.versions-fetched.json")
echo "model $FROM_MODEL -> $NEW_MODEL, datastore $PREV_DS -> $NEW_DS" >&2

say B "copy website tutorials"
cp -r "$WEB/$PREV" "$WEB/$NEW"; sed -i -E "s/^model_version: .*/model_version: $NEW_MODEL/; s/^platform_version: .*/platform_version: $NEW/" "$WEB/$NEW"/*.md
HAVE_MIG=false
if [ -d "$MIG/$PREV" ]; then
  cp -r "$MIG/$PREV" "$MIG/$NEW"; sed -i -E "s/^platform_version: .*/platform_version: $NEW/" "$MIG/$NEW"/*.md
  if [ -d "$MIG/$NEW/models" ]; then HAVE_MIG=true; else echo "warning: $MIG/$PREV has no models/, copied the page without verification" >&2; fi
else
  echo "warning: no migrations tutorial for $PREV; nothing copied" >&2
fi
HAVE_MSN=false
if [ -d "$MSN/$PREV" ]; then
  cp -r "$MSN/$PREV" "$MSN/$NEW"; sed -i -E "s/^model_version: .*/model_version: $NEW_MODEL/; s/^platform_version: .*/platform_version: $NEW/" "$MSN/$NEW"/*.md
  if [ -d "$MSN/$NEW/models" ]; then HAVE_MSN=true; fi
fi
SHOTS="$TOOLS/screenshots"; HAVE_SHOTS=false
if [ -d "$SHOTS/$PREV" ]; then
  # shot lists reference the tutorial version only in their output paths; datasets name model dirs and steps
  cp -r "$SHOTS/$PREV" "$SHOTS/$NEW"; sed -i "s#pages/tutorials/\([a-z]*\)/$PREV/#pages/tutorials/\1/$NEW/#g" "$SHOTS/$NEW"/*.json; HAVE_SHOTS=true
fi

say C "copy online-ide tutorials"
IDE_DIRS=("$T"); if $HAVE_MSN && [ -d "$TM/$PREV" ]; then IDE_DIRS+=("$TM"); fi
for base in "${IDE_DIRS[@]}"; do
  rsync -a --exclude .alan --exclude CLAUDE.md --exclude AGENTS.md "$base/$PREV/" "$base/$NEW/"
  if [ -f "$ROOT/.toolchains/$NEW/versions.json" ]; then cp "$ROOT/.toolchains/$NEW/versions.json" "$base/$NEW/.alanversions"
  elif [ -f "$DEVENV/../.versions-fetched.json" ]; then jq --arg v "$NEW" '{"platform version": $v, "system types": {datastore: ."system types".datastore}}' "$DEVENV/../.versions-fetched.json" > "$base/$NEW/.alanversions"
  else curl -sSf "https://dist.alan-platform.com/share/versions/$NEW/versions.json" | jq '{"platform version": ."platform version", "system types": {datastore: ."system types".datastore}}' > "$base/$NEW/.alanversions"; fi
  sed -i "s/^VERSION=.*/VERSION=\"$NEW\"/" "$base/$NEW/.alanscript"
done

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
census() { { "$TOOLS/snippets.py" census "$NEW"; $HAVE_MIG && "$TOOLS/snippets.py" census "$NEW" --tutorial migrations; $HAVE_MSN && "$TOOLS/snippets.py" census "$NEW" --tutorial mission; } | jq -s 'add | map_values(.markers |= map(.[0:2]))'; }

say D "upgrade models"
census > "$TMP/census-before.json"
for d in "$WEB/$NEW"/models/*/; do "$TOOLS/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$d" || FAIL+=("website model: $d"); done
if $HAVE_MIG; then
  for d in "$MIG/$NEW"/models/*/; do
    if [ -f "$d/migration.alan" ]; then "$TOOLS/upgrade-migration-project.sh" "$DEVENV" "$FROM_MODEL" "$PREV_DS" "$d" || FAIL+=("website migration project: $d")
    elif [ -f "$d/application.alan" ]; then "$TOOLS/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$d" || FAIL+=("website model: $d"); fi
  done
fi
if $HAVE_MSN; then for d in "$MSN/$NEW"/models/*/; do "$TOOLS/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$d" || FAIL+=("website mission model: $d"); done; fi
for base in "${IDE_DIRS[@]}"; do
  for d in "$base/$NEW"/step_*/to_model; do "$TOOLS/upgrade-model.sh" "$DEVENV" "$FROM_MODEL" "$d" --pp || FAIL+=("online-ide model: $d"); done
done
census > "$TMP/census-after.json" || FAIL+=("census after transform")
# marker sequences must survive the transforms (line numbers may shift, they are not compared)
if ! diff -u "$TMP/census-before.json" "$TMP/census-after.json" > "$TMP/census.diff"; then echo "error: marker census changed by transform:" >&2; cat "$TMP/census.diff" >&2; CENSUS=diff; FAIL+=("marker census"); fi

say E "upgrade online-ide step migrations"
for base in "${IDE_DIRS[@]}"; do
  prev_step=
  for step in "$base/$NEW"/step_*/; do [ -n "$prev_step" ] || prev_step=$step; "$TOOLS/upgrade-migration.sh" "$DEVENV" "$prev_step" "$step" || { FAIL+=("migration: $step"); MIGRATION=fail; }; prev_step=$step; done
done

say F "extract and verify"
"$TOOLS/snippets.py" extract "$NEW" --write || FAIL+=("extract model")
"$TOOLS/snippets.py" verify "$NEW" --platform "$DEVENV" --reference "$IDE" || { VERIFY=1; FAIL+=("verify model"); }
if $HAVE_MIG; then
  "$TOOLS/snippets.py" extract "$NEW" --tutorial migrations --write || FAIL+=("extract migrations")
  "$TOOLS/snippets.py" verify "$NEW" --tutorial migrations --platform "$DEVENV" || { VERIFY=1; FAIL+=("verify migrations"); }
fi
if $HAVE_MSN; then
  "$TOOLS/snippets.py" extract "$NEW" --tutorial mission --write || FAIL+=("extract mission")
  "$TOOLS/snippets.py" verify "$NEW" --tutorial mission --platform "$DEVENV" --reference "$IDE" || { VERIFY=1; FAIL+=("verify mission"); }
fi
say F2 "online-ide test.sh (models and migrations)"
for base in "${IDE_DIRS[@]}"; do name=$(basename "$base"); (cd "$IDE" && ./test.sh "$name/$NEW") || FAIL+=("online-ide test.sh $name/$NEW"); done

say G "prose review"
PAGES=("$WEB/$NEW"/*.md); $HAVE_MIG && PAGES+=("$MIG/$NEW"/*.md)
echo "== prose review (file:line: text)"
{
  # 1. transform-driven: substrings that the transforms changed in any .alan file, looked up in the pages
  for tut in "$WEB" "$MIG"; do
    [ -d "$tut/$NEW/models" ] && [ -d "$tut/$PREV/models" ] || continue
    (cd "$tut/$NEW/models" && find . -name '*.alan') | while IFS= read -r rel; do
      [ -f "$tut/$PREV/models/$rel" ] || continue
      python3 - "$tut/$PREV/models/$rel" "$tut/$NEW/models/$rel" <<'PY'
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
    done
  done | sort -u | while IFS= read -r needle; do grep -nF -- "$needle" "${PAGES[@]}" || true; done
  # 2. inline fence lines that no model contains, new since the previous version (page line numbers stripped)
  for tut in model migrations; do
    [ "$tut" = model ] || $HAVE_MIG || continue
    { "$TOOLS/snippets.py" extract "$NEW" --tutorial "$tut" --check-inline 2>/dev/null || true; } | sed -E "s#^$ROOT/pages/tutorials/$tut/$NEW/##; s/^([^:]*):[0-9]+:/\\1:/" | sort -u > "$TMP/inline-new.txt"
    { "$TOOLS/snippets.py" extract "$PREV" --tutorial "$tut" --check-inline 2>/dev/null || true; } | sed -E "s#^$ROOT/pages/tutorials/$tut/$PREV/##; s/^([^:]*):[0-9]+:/\\1:/" | sort -u > "$TMP/inline-prev.txt"
    comm -23 "$TMP/inline-new.txt" "$TMP/inline-prev.txt" | sed "s#^#$ROOT/pages/tutorials/$tut/$NEW/#"
  done
  # 3. grammar tokens removed between language versions: the model language (all pages) and the connector
  #    processor language, which is the migration language (migrations pages)
  token_diff() { # <old doc path> <new doc path> <pages...>
    local old_doc=$1 new_doc=$2; shift 2
    local OLD_G NEW_G
    OLD_G=$(git -C "$ROOT" show "HEAD:$old_doc" 2>/dev/null || cat "$ROOT/$old_doc" 2>/dev/null || true)
    NEW_G=$(cat "$ROOT/$new_doc" 2>/dev/null || git -C "$ROOT" show "HEAD:$new_doc" 2>/dev/null || true)
    if [ -z "$OLD_G" ] || [ -z "$NEW_G" ]; then echo "warning: $old_doc or $new_doc unavailable; token diff skipped" >&2; return; fi
    comm -23 <(printf '%s\n' "$OLD_G" | grep -oE '`[^`]+`' | sort -u) <(printf '%s\n' "$NEW_G" | grep -oE '`[^`]+`' | sort -u) \
      | sed 's/^`//; s/`$//' | while IFS= read -r tok; do [ -n "$tok" ] && grep -nF -- "$tok" "$@" || true; done
  }
  token_diff "pages/docs/model/$FROM_MODEL/application/grammar.md" "pages/docs/model/$NEW_MODEL/application/grammar.md" "${PAGES[@]}"
  if $HAVE_MIG; then
    PREV_CONN=$(dist_field "$PREV" '."system types".connector.version'); NEW_CONN=$(dist_field "$NEW" '."system types".connector.version')
    if [ -n "$PREV_CONN" ] && [ -n "$NEW_CONN" ] && [ "$PREV_CONN" != "$NEW_CONN" ]; then
      token_diff "pages/docs/connector/$PREV_CONN/processor/grammar.md" "pages/docs/connector/$NEW_CONN/processor/grammar.md" "$MIG/$NEW"/*.md
    fi
  fi
  # 4. migration workflow prose when the datastore major version changed
  if [ "${PREV_DS%%.*}" != "${NEW_DS%%.*}" ]; then grep -nE 'regexp\.alan|from_release|from-release|from_empty|migration\.alan|[Mm]igrat' "${PAGES[@]}" || true; fi
} | sed "s#^$ROOT/pages/tutorials/##" | sort -u

echo "== compile/transform failures"; [ "${#FAIL[@]}" -eq 0 ] && echo ok || printf '%s\n' "${FAIL[@]}"
echo "== census"; echo "$CENSUS"; echo "== online-ide migrations"; echo "$MIGRATION"; echo "== verify"; echo "$VERIFY"
echo "_data/versions.json \"current\" is still $PREV; promote in a separate commit when ready"
$HAVE_MIG || echo "pages/tutorials/migrations/$NEW was not produced; docs.md links it via current"
if $HAVE_SHOTS; then
  echo "screenshots: review $SHOTS/$NEW/shots.json against GUI changes, then run $SHOTS/shoot.mjs $NEW and $SHOTS/ide/prepare-workspace.sh $NEW && $SHOTS/ide/ide-shoot.mjs $NEW (needs the webclient checkout built, see README)"
else
  echo "screenshots: no shot list for $PREV; the images of $NEW are still copies of $PREV"
fi
echo "commit with explicit paths (pages/tutorials/{model,migrations,mission}/$NEW, _tools/tutorial/screenshots/$NEW, and in online-ide docs/tutorials/{restaurant1,mission-control}/$NEW)"
[ "${#FAIL[@]}" -eq 0 ]
