#!/usr/bin/env bash
#
# Re-vendor every template onto a new Bootstrap 6 build, then verify them all.
#
#   _kit/upgrade.sh <sha|tag>          # dry run: fetch, diff, report risk
#   _kit/upgrade.sh <sha|tag> --apply  # actually re-vendor + verify
#
# Why this exists
# ---------------
# Each template carries its own copy of dist/ so the download is self-contained.
# That is right for buyers and wrong for us: an upstream release means N copies
# to replace. This makes it one command, and — more importantly — it diffs the
# new dist against the pinned one FIRST and tells you which of the known-breaking
# surfaces moved, so you know whether to expect a markup pass or just a swap.
#
# The verification gate in verify.mjs is what actually catches breakage:
# zero console errors, no trailing gap, links resolve, no v5 leftovers.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NEW_SHA="${1:?usage: upgrade.sh <sha|tag> [--apply]}"
APPLY="${2:-}"
OLD_SHA="$(cat "$ROOT/_kit/PINNED_SHA" 2>/dev/null || echo none)"
RAW="https://raw.githubusercontent.com/twbs/bootstrap/$NEW_SHA/dist"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

echo "current pin : $OLD_SHA"
echo "target      : $NEW_SHA"
echo

# ---------------------------------------------------------------- fetch
for f in css/bootstrap.min.css css/bootstrap.css js/bootstrap.bundle.min.js \
         js/bootstrap.bundle.js css/bootstrap-utilities.metadata.json; do
  mkdir -p "$STAGE/$(dirname "$f")"
  code=$(curl -sL -o "$STAGE/$f" -w '%{http_code}' "$RAW/$f")
  [ "$code" = "200" ] || { echo "✗ $f → HTTP $code (bad sha/tag?)"; exit 1; }
done
echo "✓ fetched dist for $NEW_SHA"

NEW_CSS="$STAGE/css/bootstrap.css"
OLD_CSS="$ROOT/_kit/vendor/bootstrap6/css/bootstrap.min.css"

if [ "$(md5 -q "$STAGE/css/bootstrap.min.css")" = "$(md5 -q "$OLD_CSS")" ]; then
  echo "✓ identical to the current pin — nothing to do"; exit 0
fi

# ------------------------------------------------- breaking-surface probe
# These are the things our 15 templates actually depend on. If one disappears
# or is renamed upstream, every template needs a markup pass, not just a swap.
echo
echo "checking the surfaces our templates rely on:"
MISSING=0
for c in btn-solid btn-outline btn-subtle btn-text btn-icon theme-primary \
         dialog-header drawer-start menu-item form-field form-ghost form-adorn \
         check switch radio otp strength chip-input combobox-toggle form-range-input \
         stepper-item avatar accordion-icon breadcrumb-link nav-overflow \
         carousel-icon-prev fg-1 bg-2 fs-4xl; do
  if ! grep -q "\.$c" "$NEW_CSS"; then echo "  ✗ GONE: .$c"; MISSING=$((MISSING+1)); fi
done

for v in --bs-primary-base --bs-bg-body --bs-fg-body --bs-radius-4 --bs-border-color; do
  if ! grep -q -- "$v:" "$NEW_CSS"; then echo "  ✗ GONE: $v"; MISSING=$((MISSING+1)); fi
done

# The closed-dialog workaround in base.css is only needed while upstream ships
# no :not([open]) guard. If they fix it, our override becomes dead weight.
if grep -q "not(\[open\])" "$NEW_CSS"; then
  echo "  ℹ upstream now guards dialog:not([open]) — the base.css override can go"
fi

if [ "$MISSING" -eq 0 ]; then
  echo "  ✓ all $(echo 33) checked surfaces still present"
else
  echo
  echo "  ⚠ $MISSING surface(s) changed — expect a markup pass, not a clean swap."
fi

echo
echo "size delta: $(wc -c < "$OLD_CSS" | tr -d ' ') → $(wc -c < "$STAGE/css/bootstrap.min.css" | tr -d ' ') bytes"

if [ "$APPLY" != "--apply" ]; then
  echo
  echo "dry run. re-run with --apply to vendor and verify."
  exit 0
fi

# ---------------------------------------------------------------- apply
echo
cp "$STAGE/css/bootstrap.min.css" "$ROOT/_kit/vendor/bootstrap6/css/"
cp "$STAGE/js/bootstrap.bundle.min.js" "$ROOT/_kit/vendor/bootstrap6/js/"
cp "$STAGE/css/bootstrap-utilities.metadata.json" "$ROOT/_kit/vendor/bootstrap6/css/"
echo "$NEW_SHA" > "$ROOT/_kit/PINNED_SHA"

n=0
for d in "$ROOT"/*/; do
  name="$(basename "$d")"
  [ "$name" = "_kit" ] && continue
  [ "$name" = "node_modules" ] && continue
  [ -d "$d/assets/vendor/bootstrap6" ] || continue
  cp "$STAGE/css/bootstrap.min.css" "$d/assets/vendor/bootstrap6/css/"
  cp "$STAGE/js/bootstrap.bundle.min.js" "$d/assets/vendor/bootstrap6/js/"
  cp "$STAGE/css/bootstrap-utilities.metadata.json" "$d/assets/vendor/bootstrap6/css/" 2>/dev/null || true
  echo "$NEW_SHA" > "$d/.bs6-sha"          # so a deployed template says what it was built on
  n=$((n+1))
done
echo "✓ re-vendored $n templates onto $NEW_SHA"

# ---------------------------------------------------------------- verify
echo
echo "verifying …"
PASS=0; FAIL=0; FAILED=""
for d in "$ROOT"/*/; do
  name="$(basename "$d")"
  [ -f "$d/template.json" ] || continue
  if node "$ROOT/_kit/verify.mjs" "$d" >/dev/null 2>&1; then
    echo "  ✓ $name"; PASS=$((PASS+1))
  else
    echo "  ✗ $name"; FAIL=$((FAIL+1)); FAILED="$FAILED $name"
  fi
done

echo
echo "$PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
  echo "failing:$FAILED"
  echo "run: node _kit/verify.mjs <dir>   for detail"
  echo "NOTHING has been republished — fix, then publish per template."
  exit 1
fi
echo
echo "all clean."
