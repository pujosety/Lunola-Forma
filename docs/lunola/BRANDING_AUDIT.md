# Complete identity branding audit

## Scope and evidence boundary

Project: **Lunola Forma by Pujo Setyo**. Branch: `brand/complete-lunola-identity`, based on `f55fdf13a57992398b3b1535e5da5b879774d0cf`. This phase is local and not authorized for push. Source changes and host/runtime-import tests are not proof of a rebuilt or visually tested application.

Taxonomy: **A** user-facing branding, **B** product navigation, **C** application/package metadata, **D** compatibility-sensitive identifiers, **E** upstream attribution/legal/history, **F** external services/dependencies.

## Applied native display changes

The exact original string, path, audited line, category and replacement for every native display change are recorded in [the native manifest](../../tools/lunola/qa/native_identity_manifest.json). The manifest also records separate Windows crash-routing edits and CLI/resource-symbol preservation exceptions. The native preservation test compares the complete modified file with the base blob after only those explicit transformations.

Current validation: source/preservation, native build/install and 12 runtime smoke cases PASS for `d373d952`. Actual startup, Help, dark About at UI scale 1.0 and light About at 1.25 were captured and inspected. Native crash recovery was not deliberately induced; installer/signing, clean-machine and OS-level DPI gates remain. See [current verification](CURRENT_VERIFICATION.md).

## Product navigation and About

| Original / surface | File | Category | Replacement / preservation | Validation |
|---|---|---|---|---|
| Upstream Support, Community, Get Involved, generic Manual/Report a Bug | `scripts/startup/bl_ui/space_topbar.py` | A/B | Lunola documentation, issues, feature requests, repository, development release notes, legal/source and About | Source contracts and real application-Python imports PASS; installed GUI pending |
| Runtime bug report with OS/GPU/build query prefill | `scripts/startup/bl_operators/wm.py` | B | Empty official issue form, manually entered diagnostics; enum/operator IDs retained | Real-Python preset resolver PASS; no report submitted |
| Product links scattered through UI | `scripts/modules/_lunola_urls.py` | B | Small pure-script URL module; no startup network requests | Host contracts PASS |
| Windows native crash issue redirect with system query fields | `source/blender/blenlib/intern/system_win32.cc` | B | Native early-startup constant in `BLI_lunola_identity.hh`, no diagnostic query; review/redaction warning | Source contract PASS; crash deliberately not induced |
| About lacks official fork source | `scripts/startup/bl_operators/wm.py` | A/B/E | Product description, official repository, actual version/hash/date/branch, GPL and separated Blender attribution | Source/import checks PASS; visual sizing pending |
| Canonical default theme/keyconfig names shown as product branding | `scripts/startup/bl_operators/wm.py` | A/D | Display aliases only; saved keyconfig/preset/profile names unchanged | Source contract; preferences round-trip pending |
| Factory settings display name | `scripts/startup/bl_ui/space_topbar.py` | A | Load Factory Lunola Forma Settings; operator ID unchanged | Source contract |

## Verified GitHub availability

Repository and Issues are reachable; Issues are enabled. Creating an issue requires GitHub login. No report was posted. Releases is reachable but empty, so release notes use the existing repository changelog, explicitly marked development/pending. The newly prepared tutorial/reporting guides and issue templates are local and unavailable on remote `main` until an authorized publication. The tutorial entry remains hidden rather than linking to unpublished content.

## Repository documents and reporting

README includes overview, actual capabilities, screenshot status, installation, requirements, builds, documentation, issues, contributing, release status, attribution and license. Four YAML issue forms cover bugs, features, performance and compatibility. Every diagnostic field is manual; logs are optional and a privacy-review checkbox is required. Hidden-file ignore rules admit only the reviewed issue-form directory while keeping credentials ignored. Parent independently parsed/validated the YAML and documentation: **388 checks PASS**.

## Explicit preservation exceptions

- **D:** `bpy`, module names, DNA/RNA/operator identifiers, `.blend` serialization, executable names, version/hash, real build fields, canonical keymaps, presets and existing preferences locations.
- **D:** Alembic/USD and other format metadata used by importers, thumbnail/JPEG/EXR sentinels, registry/application IDs, installer upgrade lineage, MSIX signed identity, MIME/UTI, Vulkan/OpenXR profile identities. Changes require separate interoperability/coexistence review.
- **E:** AUTHORS, COPYING, SPDX/copyright headers, third-party notices, Blender ancestry, actual exporter/component authorship and legal upstream links.
- **F:** Upstream API/manual deep links, Blender extensions service, add-on publisher trackers, third-party repositories, network permission and offline controls. These are not redirected to an unrelated Lunola homepage.
- **D/E:** CLI `Blender` banners remain for existing parsers and honest engine identity; they are not a claim of upstream endorsement.

## Remaining integration and regression gates

Packaging metadata and remaining Python UI are independently owned implementation tracks. After their results are reviewed, rerun all source contracts and asset checks, compile/install the new artifact, inspect PE and generated packaging metadata, run complete real-runtime regression and preferences round-trip, then capture actual Help/About/startup before/after screenshots. File-association descriptions can be checked in source/binary resources without registering associations on this user's system. Unsupported-platform installer/runtime checks remain explicit rather than fabricated.
