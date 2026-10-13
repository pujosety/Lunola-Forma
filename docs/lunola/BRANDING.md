# Lunola Forma — Branding

Status: approved identity and prepared asset derivatives VERIFIED; application branding integration NOT yet built/tested.

Phase B assets: `release/datafiles/lunola/`. Parent independently ran 16 tests, including external-original byte comparison; all PASS. Windows ICO frames: 16/24/32/48/64/96/128/256. Linux PNGs: same sizes plus 512. About full-color transparent logo: 1086x362. Splash composite: 1000x500, light left panel and uncropped square cat artwork on right; actual version intentionally not baked. Manifest and generator are reproducible. This verifies asset files, not application integration. The approved navy LUNOLA lettering requires light backing in dark About UI.

Product: **Lunola Forma**. Parent: **Lunola**. Description: Professional 3D Creation Suite.

Upstream commit: `de6e3c4fb9183490ccd5235c4fe2e29372d22f97`. Branch: `brand/lunola-forma`.

## Approved originals

Originals preserved without changes outside source checkout in `D:/Lunola/Forma/inputs/approved/`.

| Asset | Dimensions | Format | SHA-256 |
|---|---|---|---|
| lunola-forma-logo.png | 2172 x 724 | RGBA | 9e2c53a548d398c536b929ab4dac0fa38702cf75294a2f1c14c847111e5ccdda |
| lunola-forma-icon.png | 1254 x 1254 | RGBA | e89ba124051b61175a05dfefb0d24f44c0fa6e7dd6eec23dd8dcb005a95bf111 |
| lunola-forma-splash-art.png | 1254 x 1254 | RGB | 18decbf5337fe62c178f32f04769fdd0adea4480cb0dcfc2a3c7ac9e29089bdc |

Do not regenerate or distort assets. Resizing only for integration. Preserve originals and transparency. Asset distribution licensing/ownership must be confirmed before public release; supplied approval is not a third-party-rights assessment.

## Compatibility boundaries

Keep `bpy`, DNA/RNA, `.blend` format/signatures, Python modules, operator IDs, add-on interfaces, serialization and keymaps unchanged. No global Blender text replacement. No engine changes. No file association changes without approval.

## Integration gate

Audit and baseline build must pass before replacing source resources. Final splash follows the existing popup mechanism; exact two-panel layout is conditional on low-impact feasibility. Attribution and license notices remain. No official Blender endorsement implied.
