# Windows MSI candidate — Lunola Forma

## Actual artifact

**Public product name: Lunola Forma. Publisher: Pujo Setyo.**

- File: `Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64.msi`.
- Size: 293,054,011 bytes (293.1 decimal MB).
- SHA256: `d56143a5d3fe1f74ff7d227dee025b5d2856d2dbe3a62ddf2fd1871c2095fbb3`.
- Binary source: `d373d95263ee1824ac864ab9f0478274754c0b4a`; engine **5.4.0 Alpha**.
- Numeric MSI ProductVersion: `5.4.0`; Alpha status is retained in filename, package description/comments and embedded package information.
- Local output folder: `D:/Lunola/Forma/packages/Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-installer`.
- **Status: built and database/payload verified local candidate. Installation, uninstallation and clean-machine tests have NOT RUN. Not a signed or approved public release.**

## Separate installer lineage

A separate per-user MSI candidate was authored rather than reusing the upstream MSI registry and upgrade lineage. Original compatibility-sensitive source templates remain unchanged.

Actual MSI database values:

| Field | Read-back value / authored behavior |
|---|---|
| ProductName | `Lunola Forma` |
| Manufacturer | `Pujo Setyo` |
| ProductCode | `{0466F77C-EC4B-5302-9320-EC54D4A8DD8A}` |
| UpgradeCode | `{F04B9EC1-A1D0-5121-8294-45B4931E981B}`; checked distinct from the original Blender lineage |
| Default target | `%LocalAppData%\Programs\Lunola Forma 5.4` |
| Scope | Current-user only; limited-privilege package; explicit `NOT ALLUSERS` launch condition |
| Start Menu shortcut | `Lunola Forma 5.4`; target `blender-launcher.exe`; approved Lunola icon |
| Registry authored by candidate | HKCU under `Software\Lunola\Forma\Installer\5.4`; no HKLM component writes |
| Upstream file association/custom actions | No `Extension` rows and no `CustomAction` rows; no `.blend` or thumbnail registration authored |
| Same-numeric-version alpha candidates | Authored launch condition requires uninstalling a different existing 5.4.0 alpha before replacement; real upgrade/repair behavior is untested |

This is a minimal MSI candidate, not a custom branded multi-page setup wizard. Installed ARP/uninstaller display, actual shortcut creation/removal and coexistence are **authored intentions pending execution**, not observed installation results.

Separate install directory/UpgradeCode prevents this candidate from intentionally upgrading the Blender installer lineage. It does **not** certify full coexistence: application preference/API/executable identities remain upstream-compatible. Never claim isolated user preferences from the MSI identity changes alone.

## Actual executed evidence

1. WiX 3.14.1 portable compiler/linker acquired from the official WiX release repository and used locally; no compiler MSI installation. Tool archive local SHA256 recorded in `audit/release-installer/wix-tool-download.json`; the upstream asset did not provide a digest. This pinned tooling build is not a recommendation or claim of current security-support status.
2. Actual Candle compilation and Light linking with ICE validation enabled. Initial ICE64 error traced to a missing profile-directory RemoveFolder row and fixed; validation was **not suppressed**.
3. Final linker completed with **6,887 ICE91 warnings** and no validation errors. These warn that per-user directories are not distributed to every profile in a per-machine install. The candidate explicitly rejects `ALLUSERS` and is per-user only. Warnings are retained, counted and explained, not presented as a warning-free build.
4. Actual MSI read-only Windows Installer API inspection: product/vendor/version, GUIDs, directory, registry, shortcut, upgrade and launch-condition tables checked. Two end-to-end candidate acceptance tests PASS, including the per-machine rejection condition.
5. Four embedded CAB streams read from the actual MSI and extracted with Windows `expand.exe`, without calling MSI installation or administrative install. Exact file-table inventory and every payload byte hash verified. MSI contains **6,887 files**, including **6,883 original runtime files** and four legal/package documents. The original runtime SHA256 inventory matches exactly.
6. Actual engine/launcher metadata from restored payload reports `Lunola Forma` / `Pujo Setyo`.
7. Final restored MSI payload executed with isolated QA profiles and fresh results: **12/12 runtime PASS**, including `.blend` save/reopen, Eevee and Cycles CPU.
8. SHA256 sidecar and full machine-readable `installer-verification.json` generated next to the candidate.

Mutable runtime caution: a rejected intermediate candidate copied Python bytecode already changed by a prior relocated smoke execution. Strict payload hash checking caught it. Final packaging uses the unexecuted stage, verified against the original ZIP inventory before building; rejected intermediate candidates and logs remain in local audit directories, not the final output.

## Clean-machine blocker and prepared harness

`C:/Windows/System32/WindowsSandbox.exe` is absent on the host. No feature enablement, reboot, host MSI installation or host association changes were attempted. Actual install/uninstall/repair/upgrade, ARP and shortcut lifecycle, roaming cleanup and clean-machine dependency checks remain **NOT RUN**.

Prepared local test bundle:

- `audit/release-installer/Lunola-Forma-Install-Uninstall-Test.wsb`.
- Input mapping is read-only; only the isolated `sandbox-reports` folder is writable from the guest.
- `sandbox-test.ps1` refuses the current host account and requires the Sandbox test account/mappings. Its syntax and refusal guard were actually checked on the host; **the install/uninstall test was not executed**.
- When deliberately launched on a Sandbox-capable host, the harness checks MSI checksum, installs per-user, verifies executable/ARP/shortcut, performs a limited installed API/`.blend` save probe, uninstalls, and records cleanup and HKCU `.blend` preservation. That prospective probe is not GPU/render certification.

Do not execute the MSI on the current development host to bypass this isolation gate. The Sandbox harness must produce real result/log files before these gates are marked PASS.

## Public distribution gates

No push or remote release. Matching modified-source publication, signing, artwork and binary-specific redistribution review remain required, alongside actual install/uninstall and clean-machine testing. See [application verification](CURRENT_VERIFICATION.md) and [portable ZIP verification](PORTABLE_PACKAGE_VERIFICATION.md).

Primary schema references reviewed during verification: Microsoft Windows Installer documentation for ICE64 (profile-directory cleanup), ICE91 (per-user warning scope) and Filename (short-name/long-name encoding). Native MSI short names such as `short.8|Lunola Forma 5.4` were preserved; checks inspect the defined long-display-name portion, not a rewritten identifier.
