#!/usr/bin/env python3
"""Patch PDFium source tree for the Windows static build.

Run from the pdfium source root (pdfium-src/pdfium/).
"""

import pathlib
import sys


def patch(path, old, new):
    p = pathlib.Path(path)
    src = p.read_text()
    if old not in src:
        print(f"ERROR: pattern not found in {path}")
        sys.exit(1)
    p.write_text(src.replace(old, new, 1))
    print(f"Patched: {path}")


# Since chromium/7934, cfx_renderdevice.h declares CreateForWindowsDC(HDC, ...)
# without including <windows.h>. Upstream gets HDC transitively through
# partition_alloc's headers, which we don't build (pdf_use_partition_alloc =
# false), so add the include explicitly.
patch(
    "core/fxge/cfx_renderdevice.h",
    '#include "build/build_config.h"\n',
    '#include "build/build_config.h"\n'
    "\n"
    "#if BUILDFLAG(IS_WIN)\n"
    "#include <windows.h>\n"
    "#endif\n"
    "\n",
)
