# Development release notes

**by Pujo Setyo**

## Lunola Forma rebranding

This development line introduces the Lunola Forma identity while retaining the existing 3D workflow.

### Built and tested in Phase C

- Lunola Forma window title and Windows product metadata.
- Full-color About logo resource and product labels.
- The actual engine version and build details remain intact.
- Both Windows executables built successfully; 12 background smoke tests passed.

The native window title has been inspected. The About resource is embedded, but its full visual layout is not yet certified.

### Built and runtime-tested in the final byline revision

- A splash composition with the Lunola Forma wordmark and approved cat artwork.
- Native Windows application and document icons.
- A raster Lunola product icon in the application header.

The asset suite, splash-resource contracts, and icon-source tests have passed. The final byline build passed embedded-asset, PE-icon, installed-header-data and 12 runtime checks. Full About theme/DPI visual certification remains incomplete.

### Not part of this update

No new modeling or rendering features, rewritten engine, changed keymap, new project format, or renamed Python API. Global file associations are unchanged. Source publication is separate from a public binary release.

This is an alpha development build, not a finished installer or a stable release. See the [engineering test report](../TEST_RESULTS.md) for executed checks and unresolved gates.
