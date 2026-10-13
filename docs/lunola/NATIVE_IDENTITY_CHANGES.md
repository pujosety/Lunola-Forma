# Native identity changes

## Executed source checks

This phase applies the explicit display-literal manifest in `tools/lunola/qa/native_identity_manifest.json`, not a global product-name replacement. Native quit/factory dialogs, temporary window titles, graphics/CPU warnings and selected RNA/tooltips use Lunola Forma. Format labels use `.blend` and unit labels use scene units where appropriate.

The native test first failed for every intended display replacement, then passed after integration. Its preservation gate reconstructs the exact allowlisted edits from the base Git blobs and compares the entire changed file, including preserved copyright headers. The crash-navigation contract separately verifies a user-triggered, empty GitHub issue form and a privacy warning. This is source evidence, not a forced crash or GUI test.

## Navigation and privacy

Windows crash support now uses `BLI_lunola_identity.hh`, a small native constant available before Python startup. Product navigation in Python is centralized in `_lunola_urls.py`. Both point to the official Lunola repository. No OS, GPU, build metadata, local path or crash log is transmitted in the issue URL. Restart and View Crash Log still work through their original callbacks. The user must manually review/redact any attachment.

## Preserved exceptions

- CLI `Blender` version/startup banners remain because launchers and external consumers parse them. The exact engine version, date, hash and branch are retained.
- `.blend`, operators, RNA/DNA identifiers, actual keyconfig/preset names, module namespaces and executable names are unchanged.
- Alembic application metadata, USD version/generated prefixes, EXR sentinels, JPEG/thumbnail metadata and other import/export provenance are preserved where readers depend on them.
- Vulkan/OpenXR engine/application identities remain pending driver-profile compatibility review; no renderer changes were made.
- Required upstream attribution, AUTHORS, COPYING, SPDX headers and third-party notices remain.
- Upstream graphics/API/manual service links are not repurposed as Lunola product links.
- macOS native menu display changes are source-only until a macOS build is tested; Windows is the current executable verification target.

## Pending acceptance

Build/install, real runtime regression, native metadata, Help/About visual sizing, theme/DPI, preferences round-trip and screenshots must be verified after all independently owned implementation tracks are integrated. No new binary or remote publication is claimed by this report.
