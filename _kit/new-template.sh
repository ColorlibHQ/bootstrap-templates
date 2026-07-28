#!/usr/bin/env bash
# Usage: _kit/new-template.sh <slug>
set -euo pipefail
SLUG="$1"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/$SLUG"
mkdir -p "$DEST/assets/css" "$DEST/assets/js"
cp -R "$ROOT/_kit/vendor" "$DEST/assets/"
cp "$ROOT/_kit/base.css" "$DEST/assets/css/base.css"
cp "$ROOT/_kit/base.js"  "$DEST/assets/js/base.js"
echo "scaffolded $DEST"
