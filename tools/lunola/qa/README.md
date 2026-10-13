# Lunola Forma runtime QA

This is the in-repository copy of the exercised 12-case smoke harness. It uses real bundled `bpy`, not a mock Python module.

## Run from a source checkout

```text
python tools/lunola/qa/test_runner.py
python tools/lunola/qa/run_smoke.py --blender PATH_TO_INSTALLED_EXECUTABLE --output tools/lunola/qa/results/current --timeout 180 --render-timeout 300
```

Use an explicit complete installed application and a fresh/empty output directory under this QA folder. The runner never searches PATH for an executable and never installs dependencies or changes associations. Host launcher tests use only the standard library. The actual application script runs inside the executable's bundled Python.

## Coverage

Twelve cases: API/factory scene, cube transforms, materials, subdivision, Geometry Nodes, animation, temporary add-on, OBJ export, `.blend` save, separate-process reopen, Eevee render, and Cycles CPU render.

The runner uses factory startup, disabled script auto-execution, isolated user/temp directories, explicit Python failure codes and per-process timeouts. Missing executables produce a nonzero exit and NOT RUN cases. A successful process without a valid matching case report never passes.

`summary.json`, logs and artifacts are written under `results/`, which is ignored by Git. Results record the actual executable and build metadata. Do not commit local paths, generated projects, renders or reports from this folder.

## Verification domains

This suite proves only the listed basic workflows. It does not certify every add-on, feature, GPU backend, performance characteristic, file format, installer or visual surface. Verify native metadata, splash/About and icons separately. Upstream deliberately does not allocate UI preview icon IDs in background mode; test image decoding headlessly and UI handles/rendering in a GUI process.

The original harness passed on prior installed builds. The current source copy's host tests are rerun independently. A final product-identity build must be tested explicitly; copied test code or an earlier report is not a new runtime pass.
