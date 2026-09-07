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
MODEL="$ROOT/pages/tutorials/model/$VERSION/models/$STEP/application.alan"
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
  rm -rf .alan
  cp -r "$TEMPLATE/.alan" .alan
fi
rm -rf AGENTS.md CLAUDE.md
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
