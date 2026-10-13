# Changelog

**Lunola Forma by Pujo Setyo**

## Unreleased — 5.4.0 Alpha engine base

There is no published binary release. This changelog distinguishes previously executed local verification from current source/documentation work; it is not evidence of a rebuild of this branch.

### Previously built and locally verified

The [build report](docs/lunola/BUILD_REPORT.md) and [test report](docs/lunola/TEST_RESULTS.md) record the final installed Windows x64 byline build before publication:

- Lunola Forma window titles, About logo, Windows display metadata and approved splash artwork.
- Approved native executable/launcher icons and installed raster product-menu icon.
- Pujo Setyo splash/About byline and promotional-link cleanup.
- Compilation/install, version execution, embedded assets, native PE icons and header resource checks.
- All 12 background runtime smoke cases, independently repeated with the repository harness: API, transform, material, modifier, Geometry Nodes, animation, temporary add-on, OBJ export, save/reopen, Eevee and Cycles CPU.
- Recorded GUI startup/title observations; these do not certify detailed About sizing, themes or DPI.

These results describe that exact local artifact, not a newly compiled public Git revision.

### Source and documentation

- Complete source snapshot published with upstream provenance, pinned dependencies and retained notices; upstream Git history is not mirrored in full.
- Product guides, build/contribution/security guidance and reproducible QA handoff.
- Expanded README: overview, features, screenshot status, installation, requirements, source build, documentation, issues, contributions, releases, attribution and license.
- First-scene tutorial adapted from the existing product getting-started guide.
- Four privacy-safe GitHub issue forms: Bug Report, Feature Request, Performance Issue and Compatibility Issue. Logs and attachments are optional and manually reviewed; no automatic collection or upload, default labels or assignees.
- Issue-reporting guide covering minimal reproductions, actual version information and redaction.

Issue forms require publication to the repository's default branch before they can be selected there. This uncommitted documentation update has not built or runtime-tested a new application binary.

### Pending release gates and known limits

- Public binary packaging/downloads, installer/signing and clean-machine installation.
- Detailed About layout, theme and DPI verification; public application screenshots.
- GPU release parity, broader hardware coverage and third-party add-on compatibility.
- Verified branded Linux/macOS builds.

The real engine base remains **5.4.0 Alpha**. No stable-release claim, certified hardware requirements or universal add-on compatibility is made. `.blend`, `bpy`, upstream identifiers, keymaps, copyrights, [AUTHORS](AUTHORS) and [COPYING](COPYING) remain intact.

Check the [official repository](https://github.com/pujosety/Lunola-Forma) and [release page](https://github.com/pujosety/Lunola-Forma/releases) for future publication; this changelog remains the source-level fallback while releases are pending.
