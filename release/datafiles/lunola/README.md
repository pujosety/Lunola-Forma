# Lunola Forma — Phase B prepared assets

**Prepared and tested, not integrated into Blender.** All files owned by this
phase are contained in `release/datafiles/lunola/`. Existing stock resources,
production source, build configuration, executable metadata, launcher/installer
associations, and runtime UI are unchanged. There are no commits or pushes.

## Contents

- `originals/`: byte-identical copies of the three approved PNG inputs.
- `derived/windows/lunola-forma.ico`: eight explicitly encoded PNG/RGBA frames,
  16, 24, 32, 48, 64, **96**, 128, and 256 pixels; 32-bit icon directory entries.
- `derived/linux/<size>x<size>/lunola-forma.png`: straight-alpha RGBA icons at
  16, 24, 32, 48, 64, 96, 128, 256, and 512 pixels.
- `derived/about/lunola-forma-logo.png`: full-color, full-canvas, transparent
  1086x362 derivative of the complete approved 2172x724 logo.
- `derived/splash/lunola-forma-splash.png`: opaque RGB 1000x500 composite.
- `previews/light-dark.png`: native-size icons on both themes, full-color logo,
  and nearest-neighbor 8x previews of the 16px icon for edge inspection.
- `generate_assets.py`: reproducible generator, strict input validation, manual
  ICO directory writer; no Blender API dependency.
- `asset_tests.py`: 16 real automated asset checks.
- `manifest.json`: approved hashes, output hashes/dimensions/modes, provenance,
  pinned tool version, and splash geometry/text.
- `test-results.json` / `test-output.txt`: results and raw output of the actual
  acceptance test run, not simulated results or application-runtime evidence.

## Reproduce

Python >=3.10 and **Pillow==12.3.0** are required. The acceptance run used Python
3.14 and Pillow 12.3.0. Pillow's packaged scalable default font is used for the
two splash labels and preview captions; no host font lookup or additional font
asset is required. Tool version is deliberately pinned because encoder,
resampler and packaged font changes can affect pixel/byte reproducibility.
No timestamps or machine-specific input paths are embedded in the manifest.

From the repository root:

```bash
# Regenerate solely from the checked-in byte-identical approved copies:
PYTHONDONTWRITEBYTECODE=1 python release/datafiles/lunola/generate_assets.py

# Check hashes, decoded pixels, ICO entries and clean-generation byte identity:
PYTHONDONTWRITEBYTECODE=1 python release/datafiles/lunola/asset_tests.py

# On the original asset host, additionally compare external input bytes directly:
PYTHONDONTWRITEBYTECODE=1 python release/datafiles/lunola/asset_tests.py \
  --approved-source D:/Lunola/Forma/inputs/approved
```

For initial materialization only, the generator also accepts
`--source D:/Lunola/Forma/inputs/approved`. It checks all approved hashes and image
formats before writing anything. Existing originals are verified, never
rewritten. Output is restricted to this asset directory or its descendants.
Tests create temporary regeneration directories here and remove them afterward.

## Original identities (preserved)

| Approved PNG | Dimensions / mode | SHA256 |
| --- | --- | --- |
| `lunola-forma-logo.png` | 2172x724 RGBA | `9e2c53a548d398c536b929ab4dac0fa38702cf75294a2f1c14c847111e5ccdda` |
| `lunola-forma-icon.png` | 1254x1254 RGBA | `e89ba124051b61175a05dfefb0d24f44c0fa6e7dd6eec23dd8dcb005a95bf111` |
| `lunola-forma-splash-art.png` | 1254x1254 RGB | `18decbf5337fe62c178f32f04769fdd0adea4480cb0dcfc2a3c7ac9e29089bdc` |

## Filtering and composition

All resizes use Lanczos. Transparent RGBA inputs are converted to premultiplied
`RGBa`, filtered, and converted back to straight `RGBA`; no black/white matte is
introduced. RGB artwork is filtered directly. No original is cropped,
recolored, regenerated, sharpened, reconstructed, or stretched. The original
transparent canvas/margins are preserved. Any source edge specks remain source
content, not a license to redesign it. Tests verify that black versus white
hidden RGB in fully transparent synthetic pixels cannot contaminate resized
visible edges. Every real icon and About output is also pixel-compared against
a direct premultiplied resize of its approved source.

Splash coordinates are top-left based, with rectangles using exclusive
right/bottom endpoints:

- Light left panel: `(0,0)-(500,500)`, RGB `(247,245,241)`.
- Right artwork: complete approved square resized 1254x1254 -> 500x500,
  positioned `(500,0)-(1000,500)`; no cropping or distortion.
- Complete logo canvas: 420x140 at `(40,125)-(460,265)`; exact 3:1 aspect ratio.
- Tagline: `Professional 3D Creation Suite` at `(40,294)`, font size 23.
- Attribution: `Based on Blender` at `(40,407)`, font size 18.
- No application version is baked into the PNG. The existing runtime overlay
  supplies actual build version during a later integration phase; its placement
  and any overlay interaction have not been exercised by this asset-only work.

The attribution describes derivation and does not assert Blender Foundation
endorsement, ownership, or a license grant.

## Verified / limitations

The actual acceptance run passed **16/16 tests**, with no failures or errors.
Checks cover original byte identity against the supplied input folder, PNG
formats/sizes/transparency, every ICO entry and decoded frame, full-color logo,
uncropped splash pixels, exact text composition/no baked version, label bounds,
hidden-RGB halo prevention, output hashes/inventory, and byte-identical clean
regeneration. Invalid original bytes are rejected before output writes.

The generated splash and theme contact sheet were visually inspected. Icons
remain recognizable at small sizes with normal detail loss from downsampling;
no new black/white matte halo was apparent. The approved dark navy `LUNOLA`
wordmark has low contrast on a dark background; it was intentionally not
recolored. Later About integration should select a suitable light backing or
otherwise explicitly review this limitation without altering approved artwork.

Windows Explorer/taskbar resource loading, actual About/splash UI, runtime
version overlays, stock-resource replacement, and installer/platform integration
are **not implemented or tested in this phase**. No C/C++ or production Python
source was edited and no build/runtime behavior claim follows from these tests.

Brand artwork rights were not supplied; these copies and derivatives do not
invent a copyright owner or license grant. Distribution requires the separate
rights review and preservation of upstream code/third-party notices.
