#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ] || { [ "$#" -eq 3 ] && [ "$3" != "--force" ]; }; then
  echo "usage: $0 <version> <dataset> [--force]" >&2
  exit 2
fi

VERSION=$1
DATASET=$2
FORCE=${3:-}
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
SCREENSHOTS="$ROOT/_tools/tutorial/screenshots"
WEBCLIENT=${WEBCLIENT:-"$ROOT/../webclient"}
ONLINE_IDE=${ONLINE_IDE:-"$ROOT/../online-ide"}
SHOTS="$SCREENSHOTS/$VERSION/shots.json"

[ -f "$SHOTS" ] || { echo "error: shot list missing: $SHOTS" >&2; exit 1; }
MODEL=$(jq -er --arg dataset "$DATASET" '.datasets[$dataset].model' "$SHOTS") || { echo "error: unknown dataset: $DATASET" >&2; exit 1; }
MIGRATION=$(jq -er --arg dataset "$DATASET" '.datasets[$dataset].migration' "$SHOTS") || { echo "error: dataset has no migration: $DATASET" >&2; exit 1; }
MODEL_FILE="$ROOT/pages/tutorials/model/$VERSION/models/$MODEL/application.alan"
if [[ "$MIGRATION" == online-ide:* ]]; then
  DATA_FILE="$ONLINE_IDE/docs/tutorials/restaurant1/$VERSION/${MIGRATION#online-ide:}/migration/migration.alan"
else
  DATA_FILE="$SCREENSHOTS/$VERSION/$MIGRATION"
fi
for FILE in "$MODEL_FILE" "$DATA_FILE"; do
  [ -f "$FILE" ] || { echo "error: required input missing: $FILE" >&2; exit 1; }
done

W=$WEBCLIENT
CP="$W/dependencies/dev/internals/alan/tools/compiler-project"
G="$W/build/generator/linux-x64/implementation"
for TOOL in "$CP" "$G/annotator" "$G/engine" "$W/dependencies/dev/runenv/system-types/datastore/tools/vm-tool"; do
  [ -x "$TOOL" ] || { echo "error: required tool missing: $TOOL" >&2; exit 1; }
done
for FILE in \
  "$W/dependencies/dev/devenv/interface-types/model/language" \
  "$W/build/src/auto-webclient/interface/configuration/language" \
  "$W/dependencies/dev/devenv/system-types/datastore/migration/language" \
  "$W/src/tests/migration_configuration.json" \
  "$W/build/src/webclient/interface/test/language" \
  "$W/build/src/auto-webclient/src/generators/." \
  "$W/src/webclient/src/collation_table.alan.json" \
  "$ONLINE_IDE/templates/default/project/systems/client/settings.alan" \
  "$W/build/src/auto-webclient/src/generator-contracts/default/contract.lib"; do
  [ -e "$FILE" ] || { echo "error: required path missing: $FILE" >&2; exit 1; }
done

OUT="$ROOT/.toolchains/screenshots/$VERSION/$DATASET"
if [ "$FORCE" != "--force" ] && [ -f "$OUT/build/test.pkg" ] && [ "$OUT/build/test.pkg" -nt "$MODEL_FILE" ] && [ "$OUT/build/test.pkg" -nt "$DATA_FILE" ]; then
  echo "reusing build: $OUT" >&2
  printf '%s\n' "$OUT"
  exit 0
fi

rm -rf "$OUT"
mkdir -p "$OUT/model" "$OUT/auto-client/contracts/default" "$OUT/migration/models/source" "$OUT/migration/models/target" "$OUT/tests" "$OUT/build"
cp "$MODEL_FILE" "$OUT/model/application.alan"
ln -s ../build/model "$OUT/auto-client/model.link"
cp "$ONLINE_IDE/templates/default/project/systems/client/settings.alan" "$OUT/auto-client/settings.alan"
printf '( )\n' > "$OUT/auto-client/annotations.alan"
: > "$OUT/auto-client/phrases.alan"
ln -s "$W/build/src/auto-webclient/src/generator-contracts/default/contract.lib" "$OUT/auto-client/contracts/default/contract.lib.link"
cp "$DATA_FILE" "$OUT/migration/migration.alan"
for FILE in configuration.json variables.json interface.alan; do cp "$ROOT/pages/tutorials/migrations/$VERSION/models/from-empty/$FILE" "$OUT/migration/$FILE"; done
cp "$ROOT/pages/tutorials/migrations/$VERSION/models/from-empty/models/source/application.alan" "$OUT/migration/models/source/application.alan"
ln -s ../../../model/application.alan "$OUT/migration/models/target/application.alan.link"
printf "default views: 'generated.alan' default window: 'main'\n" > "$OUT/tests/noop.alan"
ln -s ./build/gui.pkg "$OUT/gui_definition.lib.link"
ln -s ./build/instance.json "$OUT/instance.json.link"

run_generator() {
  local LOG
  if ! LOG=$("$G/engine" --ids short build/client.pkg "$W/build/src/auto-webclient/src/generators/." build/annotated.pkg "$W/src/webclient/src/collation_table.alan.json" build/gui.pkg 2>&1 > /dev/null); then
    if [[ "$LOG" == *"name collision"* ]]; then
      echo "name collision with short ids, retrying with full ids" >&2
      "$G/engine" --ids full build/client.pkg "$W/build/src/auto-webclient/src/generators/." build/annotated.pkg "$W/src/webclient/src/collation_table.alan.json" build/gui.pkg > /dev/null
    else
      printf '%s\n' "$LOG" >&2
      return 1
    fi
  fi
}

(
  cd "$OUT"
  "$CP" "$W/dependencies/dev/devenv/interface-types/model/language" --log error -C model build/model
  "$CP" "$W/build/src/auto-webclient/interface/configuration/language" --log error -C auto-client build/client.pkg
  "$G/annotator" build/client.pkg build/annotated.pkg > /dev/null
  run_generator
  "$CP" "$W/dependencies/dev/devenv/system-types/datastore/migration/language" --log error -C migration build/migration.pkg
  echo '{}' | "$W/dependencies/dev/runenv/system-types/datastore/tools/vm-tool" "$W/src/tests/migration_configuration.json" build/migration.pkg > build/instance.json
  "$CP" "$W/build/src/webclient/interface/test/language" --log warning --symbols -C . build/test.pkg
)
printf '%s\n' "$OUT"
