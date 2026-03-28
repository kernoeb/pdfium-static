#!/usr/bin/env bash
# Fetch the latest PDFium chromium branch number from the upstream repository.
# Outputs the branch number (e.g. 7734) to stdout.

set -euo pipefail

PDFIUM_REPO="https://pdfium.googlesource.com/pdfium.git"

latest=$(git ls-remote --heads "$PDFIUM_REPO" 'refs/heads/chromium/*' \
  | sed 's|.*refs/heads/chromium/||' \
  | sort -n \
  | tail -1)

if [ -z "$latest" ]; then
  echo "ERROR: Could not determine latest PDFium branch" >&2
  exit 1
fi

echo "$latest"
