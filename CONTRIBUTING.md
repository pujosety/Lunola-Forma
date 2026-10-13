# Contribute to Lunola Forma

**by Pujo Setyo**

Keep changes focused, reproducible and compatible with existing projects.

## Scope

The current development milestone is product identity. It is not an engine rewrite. Do not add unrelated features or change default keymaps as part of a branding patch.

Keep `.blend`, `bpy`, DNA/RNA, serialized engine identifiers, Python modules and operator IDs intact. Display text is not the same as an API or file-format name. Never globally replace product-name tokens across the source tree.

## Before changing code

1. Record your checkout and inspect the relevant source/build instructions.
2. Reproduce the issue or write a focused test before making a behavior change.
3. Establish the unmodified baseline when investigating a fork-specific regression.
4. Work on a dedicated branch and keep the change small enough to review.

## Verification

Run prior-phase asset/resource checks as well as new tests. Build C/C++ changes, execute the installed application, and distinguish source contracts from runtime results. Report skipped or blocked checks explicitly.

For visual changes, include real application screenshots. An asset preview is not proof of GUI integration. Inspect small icons, transparency, themes and DPI where relevant.

## Assets and notices

Do not regenerate, recolor, distort or overwrite approved originals. Keep byte-identity records and reproducible derivative recipes. New art needs rights provenance before public distribution.

Preserve copyright, license and third-party notices. The Pujo Setyo byline describes this product's identity and presentation, not ownership of all upstream source.

## Pull requests

Describe the problem, the modified paths, executed tests, artifact revision, and remaining limitations. Do not include credentials, personal logs, user preferences, build caches or binary dependency folders.

No contribution acceptance, maintainer response time, automated CI coverage or upstream affiliation is promised by this document. Upstream contributions follow upstream's own review process.
