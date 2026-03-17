# pdfium-static

Static PDFium libraries for macOS, Linux and Windows.

Built from [pdfium.googlesource.com](https://pdfium.googlesource.com/pdfium/) via GitHub Actions.

## Download

Go to [Releases](../../releases) and download the `.a` / `.lib` for your platform.

Each release is tagged with the chromium branch number (e.g. `chromium/7543`).

## Build a new version

1. Go to **Actions** > **Build PDFium**
2. Click **Run workflow**
3. Enter the chromium branch number (e.g. `7543`)
4. Wait ~1-2h for the build to complete
5. A release is created automatically with the static libraries

## Usage with pdfium-render (Rust)

Match the `pdfium_XXXX` feature flag to the branch number:

```toml
# For chromium/7543
pdfium-render = { version = "0.8", features = ["static", "pdfium_7543"] }
```

## Build config

Libraries are built with:

- No V8 JavaScript engine
- No XFA support
- Complete static library (`pdf_is_complete_lib = true`)
- Release mode, no debug symbols
