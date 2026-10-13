# Current Windows identity verification

## Artifact and source

**Lunola Forma by Pujo Setyo — Professional 3D Creation Suite**

- Exact built source commit: `d373d95263ee1824ac864ab9f0478274754c0b4a`.
- Branch: `brand/complete-lunola-identity`.
- Engine version: **5.4.0 Alpha**, unchanged.
- Local complete installed folder: `D:/Lunola/Forma/Lunola-Forma-complete-identity-final`.
- Executable: `blender.exe`; launcher: `blender-launcher.exe`.
- This is the verified engine used in the unsigned Alpha 1 Windows development prerelease, not a signed or stable build. The identity source and subsequent packaging/documentation changes are included in the Alpha 1 publication. A later documentation-only commit does not change the source hash embedded in this executable.

## Executed checks

| Domain | Actual result |
|---|---|
| Configure, native build and install | PASS; executed version reports `d373d95263ee` |
| Python/native/packaging/preservation and launcher contracts | 25 tests PASS |
| Immutable product artwork and prior approved assets | 28 tests PASS during identity integration; artwork is unchanged by label polish |
| Issue YAML / product-document validation | 388 independent checks PASS during integration |
| Real background application smoke suite | 12/12 PASS: API, transform, material, modifier, Geometry Nodes, animation, add-on, OBJ export, save/reopen, Eevee and Cycles CPU |
| Installed scripts, embedded splash, native PE icon frames and header image data | PASS against actual installed files/binaries |
| Native VERSIONINFO, engine and launcher | ProductName/FileDescription `Lunola Forma`; CompanyName `Pujo Setyo`; original copyright and executable metadata preserved |
| Older-build preferences | Two saved settings from `de6e3c4fb918` loaded successfully by the new executable in an isolated profile |
| Registered product-link dispatch | Six actual application operators dispatched exact GitHub URLs to an intercepted browser sink; no reports submitted |
| Actual GUI startup | Correct approved splash and title; default theme/keyconfig display labels fit; underlying keyconfig remains `Blender` |
| Actual Help menu | Product navigation, release-pending fallback, legal/source, About and clearly labeled upstream manual visible |
| Actual About | Logo, description, byline, version/date/hash/branch, official repository, GPL/source/authors and complete Blender attribution visible |
| Theme / scaling samples | Dark at application UI scale 1.0; light at application UI scale 1.25 |
| Launch/shutdown | Isolated application launches succeeded; three positively identified prior GUI test processes closed gracefully without force-killing user application instances |

Browser interception is operator-dispatch evidence, **not** an actual browser click/login test. Repository/Issues/changelog/legal destinations and the retained upstream API/manual/extension sites were separately reachable during identity integration; issue creation requires login. Releases is empty, so development notes use a real existing changelog. Local issue forms and tutorial/reporting guides are not remotely available until an authorized publication; the tutorial menu entry remains hidden.

## Actual screenshots

These are unedited application captures, not mockups or artwork previews. Before images show earlier local builds; after images show the exact build above. The before About image is the pre-polish identity build `182bc846`, while the earlier startup/Help examples precede complete identity migration.

### Startup before / after

![Earlier startup: legacy default theme/keyconfig labels](images/before-startup.png)

![Verified startup: readable Lunola theme/keyconfig display](images/after-startup.png)

### Help before / after

![Earlier Help: upstream product navigation](images/before-help.png)

![Verified Help: Lunola navigation and labeled upstream manual](images/after-help.png)

The native hover tooltip partly overlaps menu rows in these captures; exact routes and labels are separately checked by the installed-runtime probe.

### About before / after

![Pre-polish About: longer GPL link clipped](images/before-about.png)

![Verified About: dark, 100 percent application UI scale](images/after-about-dark.png)

![Verified About: light, 125 percent application UI scale](images/after-about-light-125.png)

## Locally packaged portable

The exact verified binary has also been packaged as `Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64.zip`, extracted and tested again: **12/12 runtime PASS**. See [portable package identity, checksum and limits](PORTABLE_PACKAGE_VERIFICATION.md). This remains a local development package, not a public release or installer certification.

## Local Windows installer candidate

Revision 1 has a real **Lunola Forma Setup** wizard: its interactive host upgrade completed with MSI result **0**, and that installed application passed **12/12 runtime checks**. The newer **artwork revision 2** adds approved logo/splash/header-icon derivatives and `by Pujo Setyo`; its package, resource bytes and three real native inactive previews are verified. A subsequent **user-approved host upgrade to revision 2 returned MSI 0**, and the actual installed application passed **12/12 runtime tests**. Product/shortcut/cached-bitmap read-back succeeded; interactive revision-2 wizard navigation is still untested. See [revision-2 artwork verification and screenshots](INSTALLER_BRANDING_VERIFICATION.md) and [revision-1 observed installed result](WINDOWS_INSTALLER_WIZARD_FIX.md). Controlled uninstall/repair, clean-machine validation and signing remain open; the [initial candidate report](WINDOWS_INSTALLER_CANDIDATE.md) is historical.

## Remaining release gates and scope limits

- Application UI scaling is **not** certification of Windows OS-level DPI, all resolutions, all themes or every localized interface.
- No deliberate crash was induced. Native crash routing and its privacy boundary have source contracts; this does not certify every crash-recovery path.
- File associations, registry identities, installer upgrade lineage and signed MSIX identity are not migrated or registered on this machine. Display metadata is checked; MSI/MSIX signing, install/uninstall/coexistence and native schema validation remain separate gates.
- No clean-machine or exhaustive GPU/add-on compatibility certification. The `full` preset does not establish official-release GPU-kernel parity.
- macOS/Linux display metadata was checked at source/template level; branded binaries, icons and runtime integration for those platforms are not certified.
- Artwork distribution rights, signing and binary-specific dependency/corresponding-source review remain distribution gates.
- Remaining Blender references include real engine/API/file-format identifiers, CLI interoperability, necessary upstream services and required attribution. Rule-classified source inventory is not a claim of manual review of every remaining line.

See [branding audit](BRANDING_AUDIT.md), [native changes](NATIVE_IDENTITY_CHANGES.md), [Python changes](PYTHON_IDENTITY_CHANGES.md), and [packaging changes](PACKAGING_IDENTITY_CHANGES.md).
