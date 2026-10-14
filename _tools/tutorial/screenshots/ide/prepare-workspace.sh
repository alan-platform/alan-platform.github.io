#!/usr/bin/env bash
set -euo pipefail

usage() { echo "usage: $0 <version> [<step>] [--from-release] [--dir <name>]" >&2; exit 2; }
[ "$#" -ge 1 ] || usage
VERSION=$1; shift
STEP=step_01; FROM_RELEASE=false; DIR=workspace
while [ "$#" -gt 0 ]; do
  case "$1" in
    --from-release) FROM_RELEASE=true; shift ;;
    --dir) [ "$#" -ge 2 ] || usage; DIR=$2; shift 2 ;;
    -*) usage ;;
    *) STEP=$1; shift ;;
  esac
done
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
ONLINE_IDE=${ONLINE_IDE:-"$ROOT/../online-ide"}
WORKSPACE="$ROOT/.toolchains/vscode/$DIR/project"
TEMPLATE="$ONLINE_IDE/templates/default/project"
TUTORIAL=${TUTORIAL:-model}   # the tutorial under pages/tutorials whose model <step> names
MODEL="$ROOT/pages/tutorials/$TUTORIAL/$VERSION/models/$STEP/application.alan"
SERVER_DATA="$ROOT/.toolchains/vscode/server-data"

[ -d "$TEMPLATE" ] || { echo "error: template missing: $TEMPLATE" >&2; exit 1; }
[ -f "$MODEL" ] || { echo "error: model missing: $MODEL" >&2; exit 1; }
rm -rf "$WORKSPACE"
mkdir -p "$(dirname "$WORKSPACE")"
cp -r "$TEMPLATE" "$WORKSPACE"
cd "$WORKSPACE"
rm -rf AGENTS.md CLAUDE.md dist .alan/deploy-lock
ln -sfn "$ONLINE_IDE/docs" _docs
sed '/^[[:space:]]*\/\/@/d' "$MODEL" > models/model/application.alan
# The template is one platform version; a workspace for another takes that version's system types from
# _data/dist/<version>/versions.json (only those the template lists) and its alan script, when fetch-toolchain.sh has it.
DIST="$ROOT/_data/dist/$VERSION/versions.json"
SWITCHED=false
if [ -f "$DIST" ] && [ "$(jq -r '."platform version"' versions.json)" != "$VERSION" ]; then
  SWITCHED=true
  jq --slurpfile d "$DIST" '."platform version" = $d[0]."platform version" | ."system types" |= with_entries(.value = $d[0]."system types"[.key])' versions.json > versions.json.tmp
  mv versions.json.tmp versions.json
  rm -rf .alan
  [ ! -x "$ROOT/.toolchains/$VERSION/alan" ] || cp "$ROOT/.toolchains/$VERSION/alan" ./alan
fi

# VS Code for the Web keeps user settings in the browser, so the colour theme for the shots is set as
# a workspace setting (the template already has .vscode/settings.json with files.exclude).
THEME=$(jq -er '.theme // empty' "$ROOT/_tools/tutorial/screenshots/$VERSION/ide-shots.json" || true)
if [ -n "$THEME" ]; then
  jq --arg theme "$THEME" '. + {"workbench.colorTheme": $theme}' .vscode/settings.json > .vscode/settings.json.tmp
  mv .vscode/settings.json.tmp .vscode/settings.json
fi
# the linked online-ide docs may carry local toolchain caches from test runs; the published docs do not have them
jq '.["files.exclude"] += {"_docs/**/.alan": true}' .vscode/settings.json > .vscode/settings.json.tmp
mv .vscode/settings.json.tmp .vscode/settings.json

if ! ./alan fetch; then echo "warning: alan fetch failed; using offline devenv if needed" >&2; fi
if [ ! -d .alan/devenv ]; then
  # the template's own devenv is of the template's platform version, so it only stands in when that is the one asked for
  $SWITCHED && { echo "error: alan fetch failed, and the template's devenv is not platform $VERSION" >&2; exit 1; }
  rm -rf .alan
  cp -r "$TEMPLATE/.alan" .alan
fi
rm -rf AGENTS.md CLAUDE.md
# a model meant not to compile (a language server screenshot of its error) is not built, and gets no migration
if grep -q '^[[:space:]]*//@[[:space:]]*expect[[:space:]]*error' "$MODEL"; then
  # the template's migrations need a build, and the tutorial folders are not what such a screenshot is about
  rm -rf AGENTS.md CLAUDE.md migrations _docs
  echo "model has '//@ expect error': workspace prepared without build and migrations" >&2
  exit 0
fi
./alan build
# Only from_empty exists before the first deployment; from_release appears after deploying with "migrate",
# with the deployed model as source (deploy.sh copies .alan/deployed.alan there).
.alan/devenv/system-types/datastore/scripts/generate_migration.sh migrations/from_empty models/model --strategy bootstrap
if $FROM_RELEASE; then
  .alan/devenv/system-types/datastore/scripts/generate_migration.sh migrations/from_release models/model
  cp models/model/application.alan migrations/from_release/models/source/application.alan
fi
# the platform tarball drops these files into the project root on every fetch; the online IDE users see them too, the tutorial does not
rm -f AGENTS.md CLAUDE.md
[ -f migrations/from_empty/migration.alan ] || { echo "error: migration generation failed: migrations/from_empty/migration.alan" >&2; exit 1; }
cat migrations/from_empty/migration.alan >&2


VSCODE_ROOT="$ROOT/.toolchains/vscode"
SERVER=$(find "$VSCODE_ROOT/cli-data/serve-web" -mindepth 1 -maxdepth 1 -type d -print -quit)
[ -n "$SERVER" ] && [ -x "$SERVER/bin/code-server" ] || { echo "error: code-server missing under $VSCODE_ROOT/cli-data/serve-web" >&2; exit 1; }
"$SERVER/bin/code-server" --accept-server-license-terms --server-data-dir "$SERVER_DATA" --extensions-dir "$SERVER_DATA/extensions" --list-extensions >&2
