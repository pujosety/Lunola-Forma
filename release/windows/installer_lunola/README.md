# Lunola Forma installer bitmap derivatives

These files are **resized integrations of the approved artwork**, not regenerated
artwork and not real installer screenshots. No approved original is edited,
recolored, cropped, stretched, or replaced. No stock/LFS-pointer image is used.
The only additions are an opaque white background and the product byline.

## Layout

- `LunolaDialog.bmp`: 493 x 312, RGB (24-bit BMP). Artwork is limited to the
  164-pixel left sidebar. The complete logo is resized proportionally to
  144 x 48 at (10, 30); the complete splash is 144 x 144 at (10, 105).
  `by Pujo Setyo` is rendered at (10, 276), size 12 pixels, RGB (40, 40, 40).
  All pixels at x >= 164 remain pure white for native wizard text.
- `LunolaBanner.bmp`: 493 x 58, RGB (24-bit BMP). The complete approved square
  icon is resized to 54 x 54 at (434, 2). Everything outside that thumbnail
  remains white, including the native header-text region x < 420.
- `manifest.json`: original and derivative SHA256 values, source dimensions,
  placements, byline bounds, reserved native-text regions, and the explicit
  font source path/hash. The font file is **not distributed** here.

All thumbnails use Pillow LANCZOS resizing, followed by explicit RGBA alpha
compositing onto opaque white, then RGB conversion. The originals' proportions
and full image extents are preserved. The byline is ordinary product copy,
not a replacement for copyright, license, or upstream attribution notices.

## Generate

Run from the repository root. Python and Pillow are required; this artifact
was generated and tested with Python 3.14.7 and Pillow 12.3.0. Supply the actual
approved asset directory, actual font file, and separate output directory:

```sh
python tools/lunola/release/generate_installer_art.py --approved-assets D:/Lunola/Forma/inputs/approved --font C:/Windows/Fonts/segoeui.ttf --output release/windows/installer_lunola
```

There is no machine-specific font fallback in the generator. It refuses a
byline that does not fit. Identical approved bytes, font bytes/path and rendering
environment produce identical BMP and manifest bytes; the manifest has no
output-directory path or timestamps. Different fonts/Pillow/FreeType versions
are not claimed to produce identical text rasterization. The exact font hash
for this output is recorded in the manifest.

The generator validates all three approved hashes before writing. It rejects
output equal to, inside, or an ancestor of the approved source directory,
including resolved directory aliases. It also rejects output containing the
font source, and existing output targets that are symlinks, hardlinks, or
nonregular files. Valid independent outputs can be regenerated in place.
These are preflight safeguards, not protection against a concurrent hostile
process replacing paths between validation and writing. Run against immutable
inputs in a private output directory without concurrent writers.

## Verify

```sh
python -W error tools/lunola/qa/test_installer_art.py --approved-assets D:/Lunola/Forma/inputs/approved --font C:/Windows/Fonts/segoeui.ttf
```

The runner prints its exact module path and runs **6 tests**, with no mocked
artwork. Temporary files and adversarial copies stay under this worktree's
`release/windows/installer_lunola/.qa-*` directories and are removed on exit.
Tests check full-image and thumbnail pixel equality, dimensions/mode/format,
white native-text zones, byline fit, provenance hashes, byte-exact duplicate and
in-place generation, all three wrong-hash rejections, source-directory overlap,
hardlinked output rejection, font-source overlap, and preservation of all
three real approved originals after every test.

### Observed TDD evidence

| Slice | RED before implementation | GREEN after implementation |
| --- | --- | --- |
| Bitmap generation/layout | 1 test, 1 failure: generator missing | 1 test, OK |
| Approved-hash/source overlap guards | 2 tests, 6 failing subtests: unsafe inputs accepted | Full suite: 3 tests, OK |
| Manifest/determinism | 1 test, 1 failure: missing manifest | Full suite: 4 tests, OK |
| Linked targets/font overlap guards | 2 tests, 4 failing subtests: unsafe outputs accepted | Full suite: 6 tests, OK |

The linked-target test initially needed fixture cleanup correction; it was
rerun to obtain the clean 4-failure RED evidence before adding the guard.
Generation reports `Generated 2 installer bitmap derivatives.`

## Remaining release gates

Bitmap generation alone is not installer proof. A separate local revision-2 MSI
has since been built with these exact BMP bytes, and three real native inactive
authoring-preview dialogs have been inspected. See [package and native-preview
verification](../../../docs/lunola/INSTALLER_BRANDING_VERIFICATION.md).

A subsequently approved host upgrade to revision 2 returned MSI 0; its installed
runtime passed 12/12 smoke cases. No standalone uninstall or repair was run.
Functional wizard navigation,
Windows OS-level DPI/theme behavior, signing and clean-machine
install/upgrade/repair/uninstall/coexistence remain separate gates.
