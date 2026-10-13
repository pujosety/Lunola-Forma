# Source publication snapshot

**Lunola Forma by Pujo Setyo**

This commit imports the complete application source snapshot onto the destination repository's initialization history. It is not a complete mirror of upstream Git history.

## Provenance

Upstream base: `de6e3c4fb9183490ccd5235c4fe2e29372d22f97`. Destination initialization parent: `5fc95426dfeb0255acc685060fdab80d90844353`. Source filenames, copyright/SPDX notices, AUTHORS, COPYING, license files and five dependency submodule pins are retained.

The importer selects the complete upstream tracked file inventory plus reviewed Lunola source/resources/docs and portable runtime QA. Build folders, platform-library contents, caches, generated QA results, temporary fixtures and credentials are excluded.

## Executed verification before this snapshot

- Product-identity source/resource checks: 13 PASS.
- Prior approved-asset checks: 20 PASS.
- Icon source contracts: 9 PASS.
- Final installed Windows byline build: successful compile/install; actual embedded splash, installed script/readme, native PE icon payloads and header data checked.
- Runtime smoke suite: 12 PASS; independently repeated with the in-repository harness, also 12 PASS.
- Real GUI header preview ID checked; detailed About sizing, every theme/DPI and a clean-machine release test remain incomplete.

The executed executable reports the upstream base hash because it was built from the reviewed development worktree before publication. This source snapshot has its own Git commit; a build from this repository will report that snapshot's actual hash. Do not describe the earlier binary as compiled from a later publication commit.

## Publication checks

Read back the destination ref after push, compare the exact commit, confirm the full tree and all referenced LFS objects, and perform a fresh-clone resource check. A committed source snapshot is not a signed installer or a complete public binary release.

Brand artwork rights and binary-specific dependency/corresponding-source review remain release gates. Mandatory upstream attribution and notices are preserved rather than replaced by the product byline.
