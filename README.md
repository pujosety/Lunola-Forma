# Lunola Forma

**by Pujo Setyo · Professional 3D Creation Suite**

![Lunola Forma approved wordmark](release/datafiles/lunola/derived/about/lunola_forma_about_light.png)

Build a world of your own.

## Overview

Lunola Forma is an independently branded, Blender-based 3D creation application from Lunola. This repository contains the complete application source snapshot and reviewed product-identity changes, not the complete upstream Git history. The Pujo Setyo byline identifies product presentation; it does not replace upstream authorship.

**Development status:** the engine base is **5.4.0 Alpha**, not a stable release. The current identity branch has a locally built and runtime/GUI-verified Windows x64 artifact from `d373d952`. There is currently **no downloadable public release**. See [current verification and remaining gates](docs/lunola/CURRENT_VERIFICATION.md); a tested portable is not a signed installer or clean-machine certification.

Official repository: [pujosety/Lunola-Forma](https://github.com/pujosety/Lunola-Forma).

## Features

The inherited engine provides modeling, sculpting, materials, animation, Geometry Nodes, rendering and compositing workflows. Lunola Forma changes presentation rather than rewriting the engine:

- Approved Lunola wordmark, splash artwork, native icons and product display text.
- Retained `.blend`, `bpy`, operator IDs, DNA/RNA, keymaps and add-on interfaces.
- Retained Eevee and Cycles names; small Eevee and Cycles CPU renders passed the recorded local Windows smoke suite.
- Native executable names remain `blender.exe` and `blender-launcher.exe` for compatibility.

The smoke suite does not certify every feature, third-party add-on or GPU backend. See [compatibility](docs/lunola/product/COMPATIBILITY.md), [known issues](docs/lunola/KNOWN_ISSUES.md) and [test results](docs/lunola/TEST_RESULTS.md).

## Screenshots

Actual [before/after application screenshots and current verification](docs/lunola/CURRENT_VERIFICATION.md) are available on this local identity branch. The wordmark above is an approved asset, not a screenshot. The verified Windows artifact is built from `d373d952`; dark 100% and light 125% application-UI samples are recorded separately from untested native OS DPI and release gates. These screenshots and the identity branch are not published to remote `main` yet.

## Installation

No public binary package or installer is available yet. A source archive is not an installable application. Check [releases](https://github.com/pujosety/Lunola-Forma/releases) for future packages; until then use the [source repository](https://github.com/pujosety/Lunola-Forma), [changelog](CHANGELOG.md) and source-build instructions below.

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

Public binary releases are **pending**. The [release page](https://github.com/pujosety/Lunola-Forma/releases) is the future distribution location, not evidence that a download exists. Working fallbacks are this [source repository](https://github.com/pujosety/Lunola-Forma) and [CHANGELOG.md](CHANGELOG.md). Local alpha results do not imply signing, an installer, complete GPU coverage or a stable release.

## Attribution

Lunola Forma is based on Blender and is independently branded; it does not claim Blender endorsement. Preserve [AUTHORS](AUTHORS), source-file copyright notices and third-party notices. Pujo Setyo's product byline does not assert ownership of all inherited code. See [SOURCE.md](SOURCE.md) and the [legal guide](docs/lunola/product/LEGAL.md) for provenance and artwork considerations.

## License

The application's GPL terms are documented in [COPYING](COPYING); per-file notices and bundled dependency licenses remain authoritative. Preserve them and provide corresponding modified source when distributing binaries under applicable terms. Product branding does not replace those licenses or grant unspecified artwork rights.
