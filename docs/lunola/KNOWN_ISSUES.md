# Known issues and release gates

**Latest identity build:** see [current executed verification](CURRENT_VERIFICATION.md) for source commit `d373d952`, rebuilt runtime, readable labels and actual GUI screenshots. Older sections below are historical milestones; they do not supersede the current report.

## Current limitations

- Baseline build and 12 background smoke tests completed successfully. GUI starts, with upstream Vulkan warning and automatic OpenGL fallback. No supported Vulkan device detected; do not change rendering architecture to hide this pre-branding hardware/driver limitation. Full splash/About interaction still needs authorized GUI input.
- Direct developer.blender.org fetch returned HTTP 403. Build scripts at pinned revision were inspected; indexed official documentation recovered by build/license audit; live page retrieval remains limited.
- RESOLVED for source build/runtime resources: official-upstream source LFS pull exited 0. Stock splash (1000 x 500), WiX bitmap (493 x 58) and dialog PNG (493 x 312) decoded successfully. Startup file materialized to 121384 bytes (not pointer text); runtime open remains untested. All 135 MSIX PNG files are no longer pointers. Windows dependency LFS download completed (exit 0). Full upstream HEAD LFS download subsequently completed with exit 0 and unchanged working-source diff. Evidence: `D:/Lunola/Forma/audit/source-resource-verification.json`.
- Source checkout is shallow (depth 1); local development is possible but complete historical source handoff is not yet prepared.
- Upstream main is the supplied repository default, not a selected long-term stable release; pin recorded and no update command will change it.
- Full baseline configuration does not produce official release GPU-kernel parity. CUDA/other release SDK requirements must be checked for final packaging.
- Icon/logo source alpha has minor visible exterior specks; do not auto-remove or change approved design without an evidence-based review.
- The approved splash composite is integrated and its embedded bytes verified in the final byline build. Detailed About theme/DPI visual checks remain open.

## Distribution gates

A local final byline portable build exists and passed 12 runtime tests; no signed installer or certified public binary release is claimed. Preserve upstream GPL/copyright and dependency notices, document modified files, provide corresponding source as required. Keep brand asset rights distinct from code licenses. Review actual licenses at pinned revision before distribution. No claim of Blender Foundation endorsement. Windows signing certificates and public release identity are not configured. Do not change operating-system file associations or push to any remote without explicit approval.
