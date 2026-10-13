# Windows installer wizard fix and observed host result

## Root cause

The first MSI candidate had **no Dialog or Control tables**. Its native installation finished successfully without a normal setup wizard. Windows Application events recorded status `0`, the executable existed, and `MsiQueryProductStateW` reported the original product installed. This was an installer presentation omission, not a failed application build.

A read-only regression first failed because the original package lacked the interactive wizard. `WixUI_InstallDir` was then bound, with the complete GPL-3.0-or-later text already shipped in the runtime converted to a license-dialog RTF. Engine code and approved artwork were not changed.

A second actual-host case was caught: reusing the already-installed ProductCode with a different PackageCode caused **Windows Installer error 1638 before the wizard**. The final candidate has a separate explicit installer UI revision ProductCode, preserves the same Lunola-only UpgradeCode, and authors detection/update of the previous same-numeric-version candidate. The engine version is still **5.4.0 Alpha**; it was not falsely bumped to fix packaging identity.

## Final local artifact

`Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-Setup.msi`

- Size: 293,371,132 bytes (293.4 decimal MB).
- SHA256: `5e20ee34fef8bec3e82bdb1aa7c5712b2860b093a5e36f6b3845f38ba5bea318`.
- Engine/source commit: `d373d95263ee1824ac864ab9f0478274754c0b4a`.
- ProductName: **Lunola Forma**; Manufacturer: **Pujo Setyo**.
- UI revision ProductCode: `{425A1781-FC04-5D6F-BA22-C56AFD2B6FE4}`.
- Previous candidate ProductCode: `{0466F77C-EC4B-5302-9320-EC54D4A8DD8A}`.
- Lunola UpgradeCode preserved: `{F04B9EC1-A1D0-5121-8294-45B4931E981B}`.
- No remote push/release. Unsigned development candidate, not a stable/public distribution approval.

## Executed verification

- **3 read-only real-MSI regressions PASS:** wizard dialogs/control routes; complete GPL license text; distinct UI revision ProductCode and same-version previous-candidate detection.
- File/component/registry/directory/shortcut/removal/association tables remained exactly equal to the original candidate. Product identity/update policy changes were explicitly reviewed rather than hidden as UI-only edits.
- Four embedded runtime cabinets are byte-identical to the original MSI whose restored runtime passed 12/12 checks; no engine, asset, DLL or API replacement was performed.
- Actual **Lunola Forma Setup** Welcome displayed and captured. Prepare/Welcome transitions replace native window IDs; rediscovery was used instead of input against a stale handle.
- The full interactive flow was subsequently observed in the actual MSI log: license acceptance, destination page, confirmation page, removal of the prior Lunola candidate, file copy, and **installation completion / engine return code 0**. The agent did not issue a license-checkbox or Install/Repair/Remove input; it stopped UI input once installation was observed and monitored the result.
- Read-back after completion: old product state `-1`, new product state `5`; installed engine hash unchanged and equal to the verified payload hash.
- Installed executable metadata: `Lunola Forma` / `Pujo Setyo`; actual uninstall display name `Lunola Forma`, version `5.4.0` observed.
- Native `MsiEnumProductsExW` returned context flag `2`; the observed ARP entry was under HKLM. Registry hive location alone was not used to infer installer context.
- Actual per-user Start Menu shortcut exists: `Lunola Forma 5.4`.
- **Actual installed executable**, new isolated test output: **12/12 runtime PASS**, including API, transforms, materials, modifiers, Geometry Nodes, animation, add-on, OBJ export, `.blend` save/reopen, Eevee and Cycles CPU.

![Actual rendered Lunola Forma Setup Welcome](images/installer-wizard-welcome.png)

Installed application:

`C:/Users/pujoh/AppData/Local/Programs/Lunola Forma 5.4/blender.exe`

Use the Start Menu entry **Lunola Forma 5.4**. The executable filename remains technical compatibility identity, not the public product name.

## Remaining gates and limits

This is an observed successful host upgrade and a runtime-checked installed artifact, **not a clean-machine or exhaustive installer certification**. Windows Sandbox remains unavailable. Controlled uninstall/repair/rollback, all user contexts, roaming profiles, clean dependency environments, signing, artwork/binary redistribution review and matching source publication remain open.

ICE validation was not suppressed. Final output retains **1 ICE61 warning** for intentional same-numeric-version upgrade inclusion and **6,887 ICE91 per-user-directory warnings**. Same-version alpha revisions need deliberate release ordering: numeric MSI version comparison does not distinguish their source hashes. These warnings and the untested rollback/downgrade cases are not concealed by the successful observed path.

Local evidence: `audit/installer-wizard/` contains source recipe, rejected prototypes, the regression, actual MSI tables, cabinet equality verification, GUI log/process/discovery captures and observed product/registry/context read-back. Installed runtime results are under ignored `tools/lunola/qa/results/installed-wizard-d373d952/summary.json`.

The earlier [MSI candidate report](WINDOWS_INSTALLER_CANDIDATE.md) is a historical pre-wizard/pre-observation milestone. See [current application verification](CURRENT_VERIFICATION.md) for the latest artifact boundaries.
