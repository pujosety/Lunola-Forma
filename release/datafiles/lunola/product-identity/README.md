# Product identity splash variant

This is a separately owned **1000 × 500 RGB PNG** derivative for Lunola Forma by Pujo Setyo. It does not rewrite the original Phase B generator, manifest, outputs, previews, or approved originals.

## Recipe

- Require `Pillow==12.3.0`.
- Verify the pinned Phase B composite and all three approved original hashes before writing.
- Start from the existing Phase B composite; preserve the logo, cat artwork and tagline pixel-for-pixel.
- Replace only the old byline area `[40, 407, 240, 435)` with the existing panel color and draw `by Pujo Setyo` at `(40, 407)` using the same packaged font, size 18 and text color.
- No new artwork, recoloring, resampling, cropping, distortion or baked version string.
- `manifest.json` records provenance, recipe, input/output hashes, dimensions and the separate embedding target.

```text
python release/datafiles/lunola/product-identity/generate_splash.py
python release/datafiles/lunola/product-identity/test_product_identity.py
```

The generator writes only this variant folder. After verification, `lunola-forma-splash.png` was copied byte-for-byte to `release/datafiles/splash.png`. Regeneration does **not** automatically update the embedding target or installed binaries.

## Copywriting and licensing

About adds `by Pujo Setyo` and keeps the actual engine version, date, hash, branch, backend and GNU GPL statement. Optional donation, store, website, community/recruitment and release-promotion links are removed from these two menus. Technical documentation remains available from the splash's Manual link.

The compact About **License & Source** section explicitly identifies **Upstream: Blender**, retains the existing upstream GNU GPL/license-source information destination, and labels the existing contributor-credits destination **Upstream Authors**. No new URLs were invented. This upstream license/source page is not represented as a download for the modified Lunola Forma source; distribution still requires the actual corresponding modified source. Upstream copyrights, GPL texts, third-party notices and legal authorship are not replaced by the product byline.

## Evidence and limits

Host tests execute isolated real draw methods using a layout recorder; they do not import the full application or certify GUI layout. Independent pixel reconstruction verifies the entire PNG, and difference bounds verify that only the byline changed. Regression tests preserve all existing Phase B assets and approved input bytes.

Local scope-preservation checks use the pre-edit snapshot in `D:/Lunola/Forma/audit/product-identity/`. The independent original Phase B suite is run through `audit/product-identity/verify.py` so its preexisting saved reports remain untouched.

**Implemented in source, not rebuilt or installed.** No application build, runtime replacement, GUI input, commit or push was performed for this change.
