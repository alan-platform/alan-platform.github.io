#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then echo "usage: $0 <build-dir> [--port N] [--app-name NAME] [--data-dir DIR]" >&2; exit 2; fi
BUILD_DIR=$1
shift
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
WEBCLIENT=${WEBCLIENT:-"$ROOT/../webclient"}
while [ "$#" -gt 0 ]; do
  case "$1" in
    --port) [ "$#" -ge 2 ] || { echo "error: --port needs a value" >&2; exit 2; }; PORT=$2; shift 2 ;;
    --app-name) [ "$#" -ge 2 ] || { echo "error: --app-name needs a value" >&2; exit 2; }; APP_NAME=$2; shift 2 ;;
    --data-dir) [ "$#" -ge 2 ] || { echo "error: --data-dir needs a value" >&2; exit 2; }; DATA_DIR=$2; shift 2 ;;
    *) echo "error: unknown argument: $1" >&2; exit 2 ;;
  esac
done
SERVER="$WEBCLIENT/build/javascript/test-server/index.js"
[ -f "$SERVER" ] || { echo "error: test server missing: $SERVER; run make build/javascript/test-server/index.js in $WEBCLIENT" >&2; exit 1; }
exec node "$SERVER" --serve --port "${PORT:-0}" --app-name "${APP_NAME:-Sandbox}" ${DATA_DIR:+--data-dir "$DATA_DIR"} --packages "$BUILD_DIR/build/test.pkg"
