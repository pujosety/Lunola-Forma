# Lunola Forma

**by Pujo Setyo · Professional 3D Creation Suite**

![Lunola Forma approved wordmark](release/datafiles/lunola/derived/about/lunola_forma_about_light.png)

Build a world of your own.

## Overview

Lunola Forma is an independently branded, Blender-based 3D creation application from Lunola. This repository contains the complete application source snapshot and reviewed product-identity changes, not the complete upstream Git history. The Pujo Setyo byline identifies product presentation; it does not replace upstream authorship.

**Development status:** **Lunola Forma 5.4.0 Alpha 1** is an unsigned Windows x64 prerelease, not stable. [Download installer or portable ZIP](https://github.com/pujosety/Lunola-Forma/releases/tag/v5.4.0-alpha.1). The exact tested engine source is `d373d952`; [release/source information](docs/lunola/RELEASE_ALPHA_1.md) and [current verification](docs/lunola/CURRENT_VERIFICATION.md) distinguish executed tests from remaining clean-machine/signing gates.

Official repository: [pujosety/Lunola-Forma](https://github.com/pujosety/Lunola-Forma).

## Features

The inherited engine provides modeling, sculpting, materials, animation, Geometry Nodes, rendering and compositing workflows. Lunola Forma changes presentation rather than rewriting the engine:

- Approved Lunola wordmark, splash artwork, native icons and product display text.
- Retained `.blend`, `bpy`, operator IDs, DNA/RNA, keymaps and add-on interfaces.
- Retained Eevee and Cycles names; small Eevee and Cycles CPU renders passed the recorded local Windows smoke suite.
- Native executable names remain `blender.exe` and `blender-launcher.exe` for compatibility.

The smoke suite does not certify every feature, third-party add-on or GPU backend. See [compatibility](docs/lunola/product/COMPATIBILITY.md), [known issues](docs/lunola/KNOWN_ISSUES.md) and [test results](docs/lunola/TEST_RESULTS.md).

## Screenshots

Actual [before/after application screenshots and current verification](docs/lunola/CURRENT_VERIFICATION.md) are available on this local identity branch. The wordmark above is an approved asset, not a screenshot. The verified Windows artifact is built from `d373d952`; dark 100% and light 125% application-UI samples are recorded separately from untested native OS DPI and release gates. These application screenshots and identity changes accompany the Alpha 1 source publication.

## Installation

Download **Setup-r2.msi** for current-user installation, or the **Windows-x64.zip** for portable use from [Alpha 1](https://github.com/pujosety/Lunola-Forma/releases/tag/v5.4.0-alpha.1). Both are unsigned development artifacts; back up important projects. Verify SHA256SUMS, retain all runtime/legal files, and read [installation, source and known limits](docs/lunola/RELEASE_ALPHA_1.md). The Source ZIP is source code, not an installable application.

If you already have a verified local Windows portable build, keep its **complete installed folder** together and run `blender.exe` inside it. Python, DLLs, scripts, resources and legal notices are needed; copying only the executable is insufficient. Check `blender.exe --version` and back up important projects before using an alpha build.

## System requirements

Windows x64 is the locally verified development target. No certified minimum/recommended CPU, RAM, GPU, VRAM or disk-space requirements have been established for a public Lunola Forma release. GPU availability depends on the exact build, driver and backend; GPU release parity and clean-machine installation remain unverified. Upstream Linux/macOS build paths exist, but branded binaries for those platforms have not been verified.

For **building**, the current pin requires Visual Studio 2022 with Desktop development with C++, MSVC 19.44.35216 or newer, a Windows SDK, CMake 3.21 or newer, Git and Git LFS. These are compiler prerequisites, not end-user hardware requirements. See [BUILDING.md](BUILDING.md).

## Build from source

```bat
git clone https://github.com/pujosety/Lunola-Forma.git
cd Lunola-Forma
git lfs pull --include="assets/**,release/**" --exclude="tests/**"
git -c submodule.lib/windows_x64.update=checkout submodule update --init --depth 1 lib/windows_x64
git -C lib/windows_x64 lfs pull
make.bat full 2022 x64 builddir ..\build_lunola_forma
```

Use a Windows command prompt with required tools available. Record your source commit, retain pinned dependencies and verify LFS resources contain real data. Read [BUILDING.md](BUILDING.md) before compiling and [QA tooling](tools/lunola/qa/README.md) before testing the exact installed artifact. The `full` preset does not establish official-release GPU parity. No new build was run for this documentation update.

## Documentation

- [Product guide](docs/lunola/product/README.md)
- [First-scene tutorial](docs/lunola/product/TUTORIALS.md) — adapted from the existing product guide, not a promised tutorial collection
- [Projects and add-ons](docs/lunola/product/COMPATIBILITY.md)
- [Troubleshooting](docs/lunola/product/TROUBLESHOOTING.md)
- [Implementation](docs/lunola/IMPLEMENTATION.md), [build evidence](docs/lunola/BUILD_REPORT.md) and [test evidence](docs/lunola/TEST_RESULTS.md)
- [Source provenance](SOURCE.md) and [publication evidence](PUBLICATION.md)

Historical build paths and milestone notes in guides are evidence, not download locations. Follow the release status above for availability.

## Issues

Use [GitHub Issues](https://github.com/pujosety/Lunola-Forma/issues) and choose Bug Report, Feature Request, Performance Issue or Compatibility Issue. Read the [reporting and privacy guide](docs/lunola/ISSUE_REPORTING.md) first. Include the actual build/commit, engine version, OS, relevant GPU/driver information, reproduction steps, expected behavior and actual behavior. Logs and attachments are optional: manually review and redact them before posting. Templates do not collect or upload data automatically.

For security concerns follow [SECURITY.md](SECURITY.md); do not post exploit details, credentials or private data in public issues.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, preserve technical compatibility and approved artwork, and report executed tests separately from pending checks. Include real application evidence for visual changes. No maintainer response time or contribution acceptance is guaranteed.

## Releases

[Lunola Forma 5.4.0 Alpha 1](https://github.com/pujosety/Lunola-Forma/releases/tag/v5.4.0-alpha.1) provides the tested Windows installer, portable package, hydrated application source, copyleft dependency sources, checksums and provenance. See [release notes](docs/lunola/RELEASE_ALPHA_1.md) and [CHANGELOG.md](CHANGELOG.md). Prerelease status does not imply signing, complete GPU coverage or clean-machine certification.

## Attribution

Lunola Forma is based on Blender and is independently branded; it does not claim Blender endorsement. Preserve [AUTHORS](AUTHORS), source-file copyright notices and third-party notices. Pujo Setyo's product byline does not assert ownership of all inherited code. See [SOURCE.md](SOURCE.md) and the [legal guide](docs/lunola/product/LEGAL.md) for provenance and artwork considerations.

## License

The application's GPL terms are documented in [COPYING](COPYING); per-file notices and bundled dependency licenses remain authoritative. Preserve them and provide corresponding modified source when distributing binaries under applicable terms. Product branding does not replace those licenses or grant unspecified artwork rights.
