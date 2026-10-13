# Test results

Status: unmodified baseline 12/12 background smoke tests PASS, independently read and counted from actual summary; Phase C branded application background smoke tests also 12/12 PASS. Report: `D:/Lunola/Forma/audit/qa/results/phase-c-20261013-043736/summary.json`. Actual PE metadata and native window title verified; About visual layout NOT VERIFIED. Final splash/icon build tests remain NOT RUN. Evidence: `D:/Lunola/Forma/audit/qa/results/baseline-auto-20261013-015309/summary.json`. GUI screenshot: `D:/Lunola/Forma/audit/screenshots/baseline-startup-vulkan-fallback.png`. UI started, but warning overlaps splash and manual interaction was not authorized.

## Preparation verified

- Visual Studio installation is complete and launchable; no restart required per vswhere.
- MSVC compiler file exists.
- Real x64 C++ probe compiled, linked against Windows SDK and executed successfully using vcvars64.bat. Output: `Windows x64 SDK/linker OK; MSVC=1944; native architecture=9`. Evidence: `D:/Lunola/Forma/audit/toolchain-probe.log`. This is NOT a Blender build or application test.
- CMake --version executed successfully.
- Originals inspected with Pillow; full logo/icon are RGBA, splash is RGB.
- Source revision and branding branch recorded.

## Harness checks — not application results

Parent independently ran `python D:/Lunola/Forma/audit/qa/test_runner.py`: 2 tests PASS. All three QA Python scripts compile. Fresh parent missing-executable check exited 2 and recorded exactly 12/12 cases NOT RUN at `D:/Lunola/Forma/audit/qa/results/parent-negative-20261012-233437/summary.json`. These prove launcher error handling only, not Blender compatibility.

Runtime command (use actual verified executable and a fresh output directory):

```text
python D:/Lunola/Forma/audit/qa/run_smoke.py --blender ACTUAL_BASELINE_EXE --output D:/Lunola/Forma/audit/qa/results/baseline
```

## Asset/source integration checks

After the Phase C About derivative was added, the original Phase B inventory check correctly caught an undocumented extension (15/16 PASS). QA contracts were repaired explicitly: only that known derivative is allowed, with pinned hash, dimensions and pixel-exact white composition; unknown or modified extras still fail. Generated reports/cache are no longer snapshotted as immutable inputs. Parent independently re-ran the complete updated asset suite: **20/20 PASS**, and Phase C source/resource suite: **12/12 PASS**. Tracked build-input diff hash remains identical. Evidence: `D:/Lunola/Forma/audit/phase-c/QA_BOUNDARY_FIX.md`. These source/asset checks are distinct from runtime results. The separate Phase C build subsequently completed with actual PE verification and 12/12 runtime smoke PASS; visual About gate remains open.

## Required runtime matrix

Run against unmodified baseline and branded build, distinguishing upstream failures from regressions. Use temporary project/output paths, factory startup and no user preferences writes.

| Test | Baseline | Lunola Forma | Evidence required |
|---|---|---|---|
| Executable --version | PASS | PASS (Phase C) | actual version/hash |
| UI startup/default scene | STARTUP VERIFIED; Vulkan warning present | NOT RUN | screenshot/log |
| Splash/logo | NOT RUN | NOT RUN | screenshot |
| Window/taskbar/Alt+Tab icon | NOT RUN | NOT RUN | light/dark screenshots |
| About attribution/version | NOT RUN | NOT RUN | screenshot |
| Transform default cube | PASS | PASS (Phase C) | scene assertions |
| Assign material | PASS | PASS (Phase C) | scene assertions |
| Eevee render | PASS | PASS (Phase C) | render output/log |
| Cycles CPU render | PASS | PASS (Phase C) | render output/log |
| Cycles GPU where supported | NOT RUN | NOT RUN | hardware/backend evidence or limitation |
| Save/close/reopen .blend | PASS | PASS (Phase C) | separate process reopen/assertions |
| Supported format export | PASS | PASS (Phase C) | nonempty export and geometry check |
| bpy API | PASS | PASS (Phase C) | Python assertions |
| Add-on register/unregister | PASS | PASS (Phase C) | executed compatibility smoke |

Additional preserved-feature samples: modifiers, Geometry Nodes, UV, sculpting, animation/rigging, simulations, linked/append assets as applicable. Basic smoke tests do not prove all add-ons or all feature compatibility. Do not mark unexecuted cases PASS.
