# Windows portable package verification

## Product identity

The public app and release name is **Lunola Forma**. **by Pujo Setyo** is its byline. The internal executable filenames remain compatibility-sensitive and are not public product names.

Actual locally generated artifact:

`Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64.zip`

- Binary source commit: `d373d95263ee1824ac864ab9f0478274754c0b4a`.
- Package size: 296,978,654 bytes (297.0 decimal MB).
- SHA256: `a897ff7ca81db124dfa616bb295e0bf180dfde8d199debed2f928fc34421549b`.
- Local folder: `D:/Lunola/Forma/packages/Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64`.
- Status: **verified local portable development package, not a published public release**.

## Executed packaging and read-back

CPack ZIP was run against a separate stage populated from the exact already-verified installed runtime. The existing generated CPack config reports product `Lunola Forma`, vendor `Pujo Setyo`, version `5.4.0`. Packaging explicitly overrides the archive name to retain the real Alpha status and Windows x64 identity. `CPACK_INSTALL_CMAKE_PROJECTS` is explicitly empty; packaging does not rebuild/reinstall the native source, modify Windows registry or register file associations.

The package contains 6,883 runtime files, each byte-hash checked against the installed artifact after ZIP creation, plus `COPYING`, `AUTHORS`, `LUNOLA_README.txt` and `LUNOLA_PACKAGE_INFO.json`. Existing dependency license notices are preserved. Developer `.pdb`/`.lib` files are excluded; DLLs, scripts and assets remain intact.

Checks actually executed:

- ZIP CRC validation, unique safe entries, exact single branded root folder, exact expected inventory and SHA256: PASS.
- End-to-end acceptance first failed for the missing package, then passed after packaging; final rerun passed without resource warnings.
- Extracted executable and launcher VERSIONINFO: ProductName/FileDescription `Lunola Forma`, CompanyName `Pujo Setyo`: PASS.
- Extracted executable, new isolated smoke output: **12/12 runtime PASS**, including `.blend` save/reopen, Eevee and Cycles CPU rendering.
- Exact original binary hash/build identity and unchanged engine version preserved.

Local reproducible operation/evidence is under `audit/release-portable/`: `build_portable.py`, `test_portable.py`, `effective-package-settings.json`, `cpack.log`, `extracted-metadata.json`, and `latest-package.json`. The output directory includes `SHA256SUMS.txt` and the full `package-verification.json`; runtime evidence is ignored under `tools/lunola/qa/results/portable-d373d952-identity/summary.json`.

## Use and remaining gates

Extract the complete archive and run `blender-launcher.exe` or `blender.exe`. Do not move the executable out of its runtime folder.

This test runs on the development Windows host; **it is not a clean-machine test**. The package is not an MSI/MSIX installer and provides no installer/uninstaller or registered shortcuts. WiX tools are not currently available on this host. Existing legacy installer registry/upgrade identities remain preserved pending a deliberate coexistence/migration decision; they must not be presented as already migrated or safe to install beside Blender.

No push, remote release, signing or OS association changes were performed. Before public redistribution, publish matching modified source, review artwork and binary-specific dependency redistribution rights, and complete release/clean-machine validation. Native OS DPI and broader hardware coverage remain open. See [current application verification](CURRENT_VERIFICATION.md).
