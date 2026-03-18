#!/usr/bin/env python3
"""Patch PDFium source tree to support WASM/Emscripten as a build target.

PDFium doesn't officially support emscripten as a target_os. These patches
(derived from paulocoutinhox/pdfium-lib) wire up everything needed.

Run from the pdfium source root (pdfium-src/pdfium/).
Requires EMSDK environment variable to be set.
"""

import os
import pathlib
import re
import sys


def patch(path, old, new):
    p = pathlib.Path(path)
    src = p.read_text()
    if old not in src:
        print(f"ERROR: pattern not found in {path}")
        sys.exit(1)
    p.write_text(src.replace(old, new, 1))
    print(f"Patched: {path}")


def patch_re(path, pattern, new):
    p = pathlib.Path(path)
    src = p.read_text()
    result, n = re.subn(pattern, new, src, count=1, flags=re.DOTALL)
    if not n:
        print(f"ERROR: regex not found in {path}")
        sys.exit(1)
    p.write_text(result)
    print(f"Patched: {path}")


# 1. Replace emscripten assert(false) with toolchain assignment
patch_re(
    "build/config/BUILDCONFIG.gn",
    r'\} else if \(target_os == "emscripten"\) \{[^}]*assert\([^)]*\)[^}]*\} else \{',
    '} else if (target_os == "emscripten") {\n  _default_toolchain = "//build/toolchain/wasm:$target_cpu"\n} else {',
)

# 2. Add wasm compiler config after mac
patch(
    "build/config/compiler/BUILD.gn",
    'configs += [ "//build/config/mac:compiler" ]\n    }',
    'configs += [ "//build/config/mac:compiler" ]\n    } else if (current_os == "emscripten") {\n      configs += [ "//build/config/wasm:compiler" ]\n    }',
)

# 3. Disable stack protector for emscripten
patch(
    "build/config/compiler/BUILD.gn",
    'if (current_os != "aix") {',
    'if (current_os != "aix" && current_os != "emscripten") {',
)

# 4-5. Treat WASM as POSIX in fxcrt and fxge
patch("core/fxcrt/BUILD.gn", "if (is_posix) {", "if (is_posix || is_wasm) {")
patch(
    "core/fxge/BUILD.gn",
    "if (is_linux || is_chromeos) {",
    "if (is_linux || is_chromeos || is_wasm) {",
)

# 6. Create wasm compiler config (POSIX defines for libopenjpeg)
pathlib.Path("build/config/wasm").mkdir(parents=True, exist_ok=True)
pathlib.Path("build/config/wasm/BUILD.gn").write_text(
    'config("compiler") {\n  defines = [ "_POSIX_C_SOURCE=200112" ]\n}\n'
)
print("Created: build/config/wasm/BUILD.gn")

# 7. Fix emscripten SDK path + suppress warnings in wasm toolchain
emsdk = os.environ.get("EMSDK")
if not emsdk:
    print("ERROR: EMSDK environment variable not set")
    sys.exit(1)
patch(
    "build/toolchain/wasm/BUILD.gn",
    'emscripten_path = "//third_party/emsdk/upstream/emscripten/"',
    f'emscripten_path = "{emsdk}/upstream/emscripten"',
)
patch(
    "build/toolchain/wasm/BUILD.gn",
    "toolchain_args = {",
    'extra_cflags = "-Wno-unknown-warning-option"\n  extra_cxxflags = "-Wno-unknown-warning-option"\n\n  toolchain_args = {',
)

# 8. Disable skia dependency
patch("BUILD.gn", 'deps += [ "//skia" ]', '#deps += [ "//skia" ]')
