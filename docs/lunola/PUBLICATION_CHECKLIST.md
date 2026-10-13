# Publication checklist

**Target:** `https://github.com/pujosety/Lunola-Forma`
**Product:** Lunola Forma by Pujo Setyo
**Status:** User-authorized source commit/publication. Preserve the destination initialization history; no force-push. Remote read-back and fresh-clone checks must complete before publication is reported successful.

## Remote safety

- [x] Read remote refs and confirm a nonempty `main` branch.
- [x] Inspect target tree: it currently contains only `README.md`.
- [ ] Re-read target refs immediately before publication; stop if they changed.
- [x] Preserve the destination initialization history; no force-overwrite of `main`.
- [x] Authenticate as the repository owner without exposing credentials; successful push still requires remote verification.
- [x] Separate publication repository with `origin` bound to `pujosety/Lunola-Forma`; the development checkout still points upstream.

Observed target `main`/HEAD: `5fc95426dfeb0255acc685060fdab80d90844353`.

## Full source, not a documentation-only upload

- [x] Finish and independently verify byline/presentation source and asset tests.
- [ ] Complete the exact final byline build/runtime and visual verification.
- [ ] Review the exact final source diff and modified assets.
- [ ] Include all application source, scripts and build configuration at the recorded revision.
- [ ] Preserve `.gitmodules`, `.gitattributes`, dependency pins, AUTHORS, COPYING and third-party notices.
- [x] Document complete-source snapshot strategy without claiming complete upstream history.
- [x] Publish complete source snapshot with provenance and preserved per-file authorship/license material.
- [ ] Resolve every required LFS object and make fresh-clone access work. Existing pointers alone are insufficient.
- [ ] Review LFS object count/size and destination quota before transferring data; do not blindly upload the full test corpus.
- [ ] Ensure the branding PNGs and other new LFS assets are uploaded to the destination endpoint.
- [x] Keep platform libraries as pinned submodules, not copied dependency/cache contents.

## Clean repository content

- [x] Prepare repository-facing README/build/contribution/security/changelog/source documents.
- [x] Copy the runtime smoke harness into `tools/lunola/qa`; 2 launcher tests PASS, 3 scripts parse, no hardcoded workstation paths.
- [ ] Finish portable handoff/review of remaining asset/UI verification fixtures and rerun source-controlled QA against the final build.
- [ ] Remove generated reports, caches, `__pycache__`, temporary fixtures and machine-only artifacts from the publication selection.
- [ ] Do not stage installed executables, build folders, local dependency contents, personal logs, credentials or signing material.
- [ ] Check every tracked/untracked candidate; do not use an unreviewed blanket `git add .`.
- [ ] Review public docs for workstation-only paths, stale PASS claims and broken links.

## Build and release evidence

- [x] Compile/install the final byline revision; its exact executable passed all 12 smoke cases.
- [ ] Verify installed scripts, About and splash artwork, native and header icons, actual version/hash and PE metadata.
- [ ] Capture real before/after screenshots and list visual checks not yet exercised.
- [ ] Test the complete portable folder on a clean appropriate Windows environment.
- [ ] Review corresponding-source availability, dependency notices and brand asset rights before binary distribution.
- [ ] Record exact source commit, artifacts/checksums, dependency pins and known limitations.

## After an explicitly authorized push

- [ ] Read back the destination branch SHA and compare it with the intended commit.
- [ ] Confirm the full source tree is present, not just the initialized README.
- [ ] Fresh-clone the published branch and verify LFS hydration and pinned Windows dependency checkout.
- [ ] Verify any enabled CI against the exact published head; do not describe unconfigured or unexecuted CI as passing.
- [ ] Only then report source publication as complete. Binary release is a separate gate.
