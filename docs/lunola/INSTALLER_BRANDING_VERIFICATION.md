# Installer artwork revision 2 — local verification

## Artifact and scope

Product: **Lunola Forma**, publisher **Pujo Setyo**, byline **by Pujo Setyo**.

`Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-Setup-r2.msi`

- Size: 293,850,364 bytes.
- SHA256: `6169a894051850b23beedba519fb8c54740ce0603ccd47fdfcb8faad76a365be`.
- Embedded engine/source: `d373d95263ee1824ac864ab9f0478274754c0b4a`, unchanged 5.4.0 Alpha.
- UI revision ProductCode: `{D087D68B-5D38-5349-902D-2CBFEE158BCD}`.
- Previous installed wizard revision: `{425A1781-FC04-5D6F-BA22-C56AFD2B6FE4}`.
- Lunola UpgradeCode remains `{F04B9EC1-A1D0-5121-8294-45B4931E981B}`.
- Unsigned development package included in the user-authorized Alpha 1 prerelease; signing and comprehensive clean-machine certification remain unfulfilled.

**Revision 2 was subsequently installed through a user-approved host upgrade on October 13, 2026.** MSI returned 0 without reboot; revision 1 is now state -1 and revision 2 state 5. The installed executable hash is unchanged, metadata reads Lunola Forma / Pujo Setyo, and its actual installed runtime passed **12/12** isolated smoke cases. The Start Menu shortcut targets the installed blender-launcher.exe. This was a silent upgrade, not certification of interactive Next/Back/license/destination behavior. The earlier preservation checks below describe the pre-upgrade preview phase.

## Artwork and executed checks

The complete approved logo and splash are proportionally resized into a white Welcome sidebar. The approved icon is resized into the header banner; `by Pujo Setyo` is ordinary product copy. Approved originals are not regenerated, cropped, recolored, stretched, or overwritten. The GPL dialog and attribution remain intact. See [derivative recipe and manifest](../../release/windows/installer_lunola/README.md).

- **36 scoped unit tests PASS:** 25 existing source/native/navigation/packaging/runner contracts, 6 derivative/provenance/safety cases, 1 real-MSI bitmap binding check, 3 real-MSI wizard regressions, and 1 real native read-only preview/cleanup/capture case.
- **28 current immutable artwork tests PASS:** 8 product-variant cases and 20 prior approved-resource cases. Total executed unit tests across these scopes: **64**.
- **388 independent issue-form/document checks PASS**, distinct from unit-test count.
- Four runtime CAB streams and non-UI payload tables match the previously verified payload. No engine or runtime replacement is claimed.
- MSI binary bitmap entries match the generated BMP bytes. Read-only tables confirm Lunola product identity, GPL text, retained upgrade lineage, and the explicit new UI revision.
- Actual Authenticode read-back: **NotSigned**. ICE validation warnings and same-numeric-version alpha migration risks remain open; they were not suppressed.

### Historical audit-path limitation

The older private Phase-B hash map points at a different checkout and includes deleted ephemeral QA reports. Its legacy rerun failed on text-file CRLF transport and missing QA reports; that evidence was retained, not rewritten or described as PASS. Current immutable checks instead use a separately owned baseline derived from Git commit `24fb0ff3`: 21 tracked resource/source files, strict Git blob/LFS hashes for artwork, and explicitly verified LF-to-CRLF transport for two text files only. Original artwork hashes and the historical private map are unchanged. This is a canonical-checkout resource check, not retroactive certification of the obsolete private audit fixture.

## Real native inactive previews

These images are actual Windows Installer authoring-preview windows, **not synthesized interfaces and not executed installation screens**. `MsiOpenDatabaseW` opens read-only; `MsiEnableUIPreview`/`MsiPreviewDialog` render native dialogs without a costing/install session. Each preview pumps its own native messages, captures only its positively identified HWND with `PrintWindow`, closes all owned preview/database handles, and preserves the installed product and executable.

The desktop UIA capture provider timed out on these authoring-preview windows. Native owner-process GDI capture was used instead; there was no foreground input, installer launch, checkbox acceptance, install/repair/remove action, or synthesized UI fallback.

### Welcome

![Native inactive Welcome: complete logo, splash and byline](images/installer-r2-preview-WelcomeDlg.png)

Logo, complete splash and byline are visible in the sidebar, without overlap into native heading/body/buttons.

### License agreement

![Native inactive GPL license preview](images/installer-r2-preview-LicenseAgreementDlg.png)

Header icon does not overlap the title; native GPL text renders. Checkbox and navigation appearance are preview state, not evidence of consent or functional interactive navigation.

### Installation directory

![Native inactive directory preview](images/installer-r2-preview-InstallDirDlg.png)

Header icon remains proportional and separate from the title/instructions. The directory property is blank without installer costing. Destination resolution, Next/Back behavior, upgrade/install/repair/remove, Windows DPI/theme coverage and clean-machine behavior are **not certified** by these previews.

## Approved host upgrade follow-up

Installed read-back checked all 6,887 packaged paths after runtime execution: 6,593 files are byte-identical; 294 differences are exclusively regenerated Python __pycache__ .pyc files. No source, binary, DLL, asset or other non-cache payload mismatch was found. This is not a claim that every post-execution cache remains byte-identical. The installed Windows Installer cache also contains both exact revision-2 BMP resources. Local upgrade log, before/after product state, cache differences and shortcut read-back are in audit/installer-host-r2/. Installed-runtime report: tools/lunola/qa/results/installed-host-r2/summary.json.

## Remaining release gates

Signing, matching-source publication and redistribution review; controlled rollback/repair/uninstall and interactive revision-2 wizard navigation; clean-machine validation; Windows OS-level DPI/theme/resolution checks. Preserve existing host applications until a separately authorized, isolated installation test is available.

Local evidence and recipe: `D:/Lunola/Forma/audit/installer-branding/`. Artifact and verification JSON: `D:/Lunola/Forma/packages/Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-Setup-r2/`.
