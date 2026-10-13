# Source and provenance

## Product identity

**Lunola Forma by Pujo Setyo** is a separately branded 3D creation application. The byline credits the product identity/presentation. It does not replace original authorship of upstream code or dependencies, and no official upstream endorsement is claimed.

## Source baseline

- Upstream source repository: `blender/blender` (GitHub mirror).
- Exact audited source commit: `de6e3c4fb9183490ccd5235c4fe2e29372d22f97`.
- Reported engine version at that revision: `5.4.0 Alpha`.
- Local branding branch: `brand/lunola-forma`.
- Pinned Windows x64 library gitlink: `aa0c5db72fa9488bb685bdddbede780d19f483f5`.

History strategy: complete application source snapshot imported onto this repository's existing initialization history. The upstream development checkout was shallow; this publication does not claim to mirror complete upstream Git history. Per-file notices, AUTHORS, source provenance and dependency gitlinks are retained. LFS data and dependency source must still be materialized/reviewed as appropriate for a release.

## Publication target

`https://github.com/pujosety/Lunola-Forma`

This snapshot adds the complete application source tree to the destination initialization history without a force-overwrite. Its publication/ref and fresh-clone checks are recorded separately; binary release remains a separate gate.

Alpha 1 supplies the complete tracked application source with hydrated LFS resources, retained notices, modified assets, dependency build/patch recipes and the actually executed packaging scripts. See [release source access](docs/lunola/RELEASE_ALPHA_1.md) and [resolved dependency URLs/hashes](docs/lunola/DEPENDENCY_SOURCES.json). The executable reports exact source commit d373d95263ee1824ac864ab9f0478274754c0b4a; later release-tag changes are packaging resources and documentation, not a claimed rebuild.

## Preserve original information

Keep [COPYING](COPYING), [AUTHORS](AUTHORS), per-file SPDX/copyright statements, [license texts](doc/license/) and [dependency notices](release/license/). Review the actual redistributed files and relevant dependency source/patches before claiming a complete corresponding-source package.

The approved logo/icon/splash originals retain their recorded hashes. Artwork-rights provenance is separate from source licensing. The maintainer explicitly confirmed public redistribution permission for the supplied assets on October 13, 2026; this is not an ownership claim or independent trademark clearance.

## Release manifest

Before publishing binaries, record the exact modified-source commit, build configuration, dependency pins, branding asset hashes, artifact checksums and verified tests. Provide the exact corresponding-source location rather than only an upstream link. Alpha 1 is published as an unsigned development prerelease, with the unresolved certification limits stated rather than presented as a stable release.
