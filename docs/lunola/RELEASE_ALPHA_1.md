# Lunola Forma 5.4.0 Alpha 1

**by Pujo Setyo · Windows x64 · unsigned prerelease**

Release tag: `v5.4.0-alpha.1`. Engine and runtime source commit: `d373d95263ee1824ac864ab9f0478274754c0b4a`. The release tag includes later installer artwork, packaging recipes, documentation and release metadata; the executable was not rebuilt from that later documentation commit.

## Downloads and installation

Use [the Alpha 1 release](https://github.com/pujosety/Lunola-Forma/releases/tag/v5.4.0-alpha.1):

- **Setup-r2.msi**: tested current-user installation/upgrade, branded Welcome/header/GPL wizard, Lunola-only upgrade lineage and Start Menu shortcut. No `.blend` file associations or thumbnail registration are authored. Back up projects before installing an alpha.
- **Windows-x64.zip**: extract the complete directory, then run `blender-launcher.exe` or `blender.exe`. Preserve Python, DLLs, scripts, assets and legal notices. Existing upstream-compatible preference paths are retained; this is not certification of independently isolated Blender profiles.
- **Source.zip**: full tracked application/source snapshot with actual hydrated and hash-verified LFS data, not GitHub's pointer-only automatic archive. Platform-library gitlinks remain pinned; their binary contents are not misrepresented as source.
- **Copyleft-Dependency-Sources.zip**: 15 upstream source archives verified against the exact recipe hashes, including GPL-enabled FFmpeg, x264/x265 and applicable LGPL/MPL dependencies. The complete application source also includes dependency build recipes and patches; [resolved source URLs/hashes](DEPENDENCY_SOURCES.json) identify other recipe dependencies, including build-time/other-platform entries.
- **SHA256SUMS.txt** and **RELEASE_MANIFEST.json**: asset integrity, actual binary/source provenance and test scope.

PowerShell checksum example:

```powershell
Get-FileHash .\Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-Setup-r2.msi -Algorithm SHA256
```

These exact tested binary bytes retain their packaging-time `local verification only` text in LUNOLA_README/package-info files. That historical text is not silently rewritten after tests; these release notes record the subsequent approved publication and host upgrade. PackageInfo does not claim this is a signed/stable/clean-machine-certified product.

## Verified behavior

- Native build/install and exact version/hash read-back.
- Approved app branding, splash/About, engine/launcher ProductName and publisher.
- 12/12 real background smoke cases on the tested portable and actual revision-2 host-installed runtime: API, transform, material, modifier, Geometry Nodes, animation, temporary add-on, OBJ export, `.blend` save/reopen, Eevee and Cycles CPU.
- User-approved revision-2 host upgrade returned MSI 0 without reboot; product, launcher shortcut and installed-cache artwork read-back succeeded.
- 64 pre-upgrade scoped source/resource/native-preview tests and independently checked issue forms/documents. Historical local audit-path/EOL limitations are explicitly explained in [installer evidence](INSTALLER_BRANDING_VERIFICATION.md).
- Runtime cabinets/immutable payload retained; post-runtime differences are restricted to regenerated Python caches, not source, binaries, DLLs or artwork.

## Source, licenses and artwork

[Exact executable source](https://github.com/pujosety/Lunola-Forma/tree/d373d95263ee1824ac864ab9f0478274754c0b4a), [release source tag](https://github.com/pujosety/Lunola-Forma/tree/v5.4.0-alpha.1), [source/build instructions](../../BUILDING.md), [executed packaging recipes](../../tools/lunola/release/recipes/README.md), and [source provenance](../../SOURCE.md) are adjacent to the binary downloads. Git users must use Git LFS and retain the pinned Windows library commit `aa0c5db72fa9488bb685bdddbede780d19f483f5`.

Retain COPYING, AUTHORS, complete GPL and third-party notices. Lunola Forma is independently branded and based on Blender, not endorsed by Blender Foundation. Combined binary notices are GPL-3.0-or-later; individual files/dependencies retain their original terms. The actual shipped FFmpeg DLL reports GPL version 2 or later and `--enable-gpl`, x264/x265, and `--disable-nonfree`; do not describe it solely using the recipe's LGPL label. Its source and applicable build patches are supplied. This inventory/source handoff is not a claim of universal legal or trademark clearance.

On October 13, 2026, the maintainer explicitly confirmed that the supplied Lunola logo, icon and splash may be distributed publicly. This records permission, not an invented ownership claim or an independent rights investigation. Originals remain byte-identical; font files used to rasterize the installer byline are not distributed as fonts.

## Known limits

Unsigned Windows development prerelease; not stable. No signing certificate, clean-machine certification, controlled standalone repair/uninstall/rollback, comprehensive interactive revision-2 navigation or native OS DPI/localization coverage. GPU release-kernel parity, every add-on/hardware combination and branded Linux/macOS binaries are not certified. Same-numeric-version alpha upgrade ordering and retained ICE61/ICE91 warnings are documented, not suppressed. Use backups and report reproducible failures without private logs or credentials.
