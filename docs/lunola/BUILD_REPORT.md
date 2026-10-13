# Windows build report

**Latest identity build:** see [current executed verification](CURRENT_VERIFICATION.md) for source commit `d373d952`, rebuilt runtime, readable labels and actual GUI screenshots. Older sections below are historical milestones; they do not supersede the current report.

## Final byline revision — BUILT AND RUNTIME VERIFIED

Pipeline: `audit/product-identity/build_and_verify.py`; target `D:/Lunola/Forma/Lunola-Forma-by-Pujo-Setyo`. Reuses the existing native build cache and preserves the prior portable. Checks exact embedded byline PNG, installed About/splash script, rendered readme template, native PE icon payloads, real header image data and 12 runtime cases. No result is marked PASS until executed. Visual About sizing remains a separate pending gate.


## D/E branding rebuild — superseded by the verified final byline build

The user explicitly requested the remaining visible splash and logos be replaced. Stock splash source now equals the approved 1000x500 composite; 3 source/resource tests PASS. Both Windows ICO source resources now equal the approved eight-frame ICO; 9 host icon/menu/install contracts PASS. Header uses a cached approved raster preview and preserves menu/API IDs.

Runner: `D:/Lunola/Forma/audit/phase-e/build_and_verify_de.py`. It reuses the Phase C build cache but requests a separate runtime output (`build-phase-c/bin-de`) and portable install (`D:/Lunola/Forma/Lunola-Forma`). Before linking it checks generated project output paths to avoid overwriting open Phase C executables. It verifies actual embedded PNG bytes, PE icon groups, installed header preview with real bpy, and the complete 12-case runtime smoke suite. State: `audit/phase-e/de-build-state.json`. Initial header lookup/background-ID checks needed correction; recovered resource checks and all 12 runtime cases then passed. The final byline pipeline independently passed build/install, embedded assets, PE icons, header data and 12 runtime cases.

Prior Phase C binaries still have the stock splash/icons and must not be presented as the final rebranded output. Historical Phase C freeze-stock tests describe that earlier milestone; D/E-specific tests govern the deliberate stock-resource replacements. No changes to file associations, core formats, renderers or APIs.

## Phase C result

Separate build completed, exit 0: `D:/Lunola/Forma/build-phase-c/bin/Release/blender.exe`. Actual version remains `Blender 5.4.0 Alpha`, expected upstream hash `de6e3c4fb918`. Both executable and launcher PE ProductName/FileDescription independently read as `Lunola Forma`; upstream CompanyName/copyright/OriginalFilename retained. Actual branded runtime QA: 12/12 PASS; report `D:/Lunola/Forma/audit/qa/results/phase-c-20261013-043736/summary.json`.

Native GUI capture confirms title `(Unsaved) — Lunola Forma 5.4.0 Alpha`. Existing stock splash/icons intentionally remain for later phases. GPU warning still falls back from Vulkan to OpenGL as in baseline. About layout is NOT visually verified: explicit GUI input consent timed out. No denied input was retried or bypassed. This historical visual gate remains incomplete for detailed About sizing; later D/E integration was separately built and runtime-tested.

## Original baseline result

Status: baseline BUILT; --version executed successfully; 12/12 background compatibility smoke tests PASS. This is the upstream full preset with Release configuration, not official-release GPU parity.

## Reproducibility

- Source: https://github.com/blender/blender
- Source version verified in `BKE_blender_version.h`: **5.4.0 alpha** (not a stable release). Version macros remain unchanged.
- Windows source compiler minimum checked: `19.44.35216` (VS 2022 17.14.14).
- Source commit: `de6e3c4fb9183490ccd5235c4fe2e29372d22f97`
- Windows x64 library gitlink: `aa0c5db72fa9488bb685bdddbede780d19f483f5`
- Visual Studio 2022 Community path: `D:/DevTools/VisualStudio/2022/Community`
- Installed MSVC toolset folder: `14.44.35207`
- CMake executed: `3.31.6-msvc6`
- Baseline directory: `D:/Lunola/Forma/build-baseline`
- Runner: `D:/Lunola/Forma/audit/prepare_baseline.py`
- Machine-readable live state: `D:/Lunola/Forma/audit/baseline-state.json`

Runner verifies source pin and no tracked production diff, downloads only Windows library submodule at its pinned commit, hydrates build/runtime source LFS assets (not the full test data corpus), then runs:

```bat
make.bat full 2022 x64 builddir D:\Lunola\Forma\build-baseline
```

`full` is an upstream configuration, not a claim of official release parity. Optional precompiled CUDA GPU kernels are not enabled by that preset. Final release configuration remains a separate acceptance gate. No render backends are edited.

## Results

Libraries checkout: completed at pinned gitlink.
Libraries LFS: completed, exit 0.
Source LFS: official endpoint pull exited 0. Stock splash and both WiX artworks decode; 135 MSIX PNGs have 0 unresolved pointers. `startup.blend` materialized to 121384 bytes, but runtime opening not yet tested. Evidence: `source-lfs-prehydrate.log` and `source-resource-verification.json` under audit.
CMake configure and compilation/install: completed, baseline-build exited 0.
Executable: `D:/Lunola/Forma/build-baseline/bin/Release/blender.exe`.
Version command: executed, `Blender 5.4.0 Alpha`, hash `de6e3c4fb918`.
Background smoke tests: 12 PASS, exit 0; `D:/Lunola/Forma/audit/qa/results/baseline-auto-20261013-015309/summary.json`.
GUI startup: visible default scene and first-run splash, screenshot retained. Vulkan device unsupported; upstream falls back to OpenGL. Screenshot shows warning obscuring part of splash. GUI interaction approval timed out; no input workaround attempted.

Each executed stage has a log in `D:/Lunola/Forma/audit/`. An exit-zero build alone is insufficient; executable presence and version execution are checked by runner. Update this report from actual logs on completion.
