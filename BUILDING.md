# Build Lunola Forma

**by Pujo Setyo**

Lunola Forma uses the existing native build system. Windows x64 is the current verified development platform. This repository contains a complete application source snapshot. It retains the upstream build system, source provenance and pinned library submodules.

## Windows prerequisites

- Visual Studio 2022 with Desktop development with C++, MSVC and Windows SDK.
- MSVC compiler 19.44.35216 or newer for the currently pinned revision.
- CMake 3.21 or newer, available on PATH.
- Git and Git LFS.

The tested machine uses compiler 19.44.35229 and CMake 3.31.6. Its successful build is evidence for that environment, not every Windows configuration.

## Get the source

Clone `pujosety/Lunola-Forma` and record the exact commit you intend to build. The snapshot retains `.gitmodules`, `.gitattributes`, source and license files. Use Git LFS to materialize assets before configuring.

## Materialize resources and Windows dependencies

From the repository root in a Windows command prompt:

```bat
git lfs install
git lfs pull --include="assets/**,release/**" --exclude="tests/**"
git -c submodule.lib/windows_x64.update=checkout submodule update --init --depth 1 lib/windows_x64
git -C lib/windows_x64 lfs pull
```

The first pull requires the publication's LFS endpoint to contain all referenced objects. This is a publication gate, not a guarantee the initial target repository already provides them. Full upstream regression tests require additional test-data LFS objects.

Confirm `release/datafiles/startup.blend`, the splash PNG and the bundled Python executable contain their actual data, not Git LFS pointer text. File existence alone does not prove readiness. Keep the dependency gitlink pinned; do not run a source-updating convenience command against a revision intended to remain fixed.

## Compile and install

```bat
make.bat full 2022 x64 builddir ..uild_lunola_forma
```

The `full` preset uses Release optimization by default and keeps the interactive feature set. It does not guarantee the additional GPU SDK/binary settings of the upstream `release` preset. Do not call a CPU-capable full build an official-release-equivalent build.

The install phase is required. Distribute the complete installed folder, including Python, DLLs, datafiles, scripts and legal material, rather than only the executable. Native filenames remain `blender.exe` and `blender-launcher.exe` for compatibility.

## Verify the exact artifact

Run the installed executable with `--version`. Record the actual engine version, commit hash, build settings and branding revision. Run the runtime smoke suite against that exact path, then verify splash, About, native icons, header icon and Windows metadata separately.

The latest Pujo Setyo identity changes are a separate verification gate; earlier smoke passes do not automatically certify them. See [test results](docs/lunola/TEST_RESULTS.md) and [known issues](docs/lunola/KNOWN_ISSUES.md).

## Runtime QA from the repository

```text
python tools/lunola/qa/test_runner.py
python tools/lunola/qa/run_smoke.py --blender PATH_TO_INSTALLED_EXECUTABLE --output tools/lunola/qa/results/current --timeout 180 --render-timeout 300
```

Use a fresh output directory and the exact complete installed build. The portable launcher has passed its two host contract tests and all three scripts parse. That result is not a runtime pass for the final byline binary. See [QA tooling](tools/lunola/qa/README.md).

## Other platforms

Upstream source retains its Linux/macOS build paths, and Linux icon derivatives have been prepared. This project has not yet verified a branded Linux or macOS executable. Do not label those platforms supported by this release without a build and runtime report.
