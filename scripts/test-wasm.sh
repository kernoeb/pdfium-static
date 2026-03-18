#!/usr/bin/env bash
# Test a WASM PDFium library by compiling and running a minimal program.
# Usage: test-wasm.sh <lib_path>
# Run from the pdfium source root (pdfium-src/pdfium/).
set -euo pipefail

LIB_PATH="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

emcc -o /tmp/test_pdfium.js "$SCRIPT_DIR/test_pdfium.c" \
  "$LIB_PATH" \
  -I. \
  -s USE_ZLIB=1 -s USE_LIBJPEG=1 \
  -s WASM=1 -s ALLOW_MEMORY_GROWTH=1
echo "emcc link test passed"

node /tmp/test_pdfium.js
echo "WASM runtime test passed"
