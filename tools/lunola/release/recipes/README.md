# Executed alpha packaging recipes

These are the exact procedural recipes used for the tested portable, initial MSI, native wizard revision 1, and artwork revision 2, with an SPDX header added for publication. They are **historical fixed-workspace recipes**, not a newly tested portable packaging CLI.

They expect `D:/Lunola/Forma`, the documented native toolchain, existing build/QA state, a pristine verified runtime stage, and preceding audit artifacts. Review paths before adapting to another machine. Their guards refuse overwriting earlier packages. They never install or publish a package. Old `local verification only` metadata describes the packaging-time state; the release notes record the subsequent user-approved publication and host upgrade without altering the tested binary bytes.

Order:

1. Build and install the exact application source commit `d373d95263ee1824ac864ab9f0478274754c0b4a` with the source's native build system; run the real 12-case smoke suite.
2. `build_portable.py`: create and verify the complete CPack ZIP.
3. `build_installer.py`: create per-user WiX authoring, deterministic Lunola identifiers, runtime file-ID/hash map and original MSI.
4. `build_wizard.py`: retain GPL text and add native WixUI_InstallDir, reviewing same-version alpha upgrade policy.
5. Generate approved BMPs using `../generate_installer_art.py` and the supplied approved assets/font.
6. `build_branded.py`: bind both exact BMPs and the explicitly distinct revision-2 ProductCode.

The generated `.wxs`, `.rtf`, runtime manifest and compiler logs were retained locally. File/component IDs and GUIDs are deterministically derived from runtime paths and the unchanged Lunola lineage; PackageCode and file timestamps need not reproduce the original MSI checksum. See [installer verification](../../../../docs/lunola/INSTALLER_BRANDING_VERIFICATION.md) and [source handoff](../../../../docs/lunola/RELEASE_ALPHA_1.md).

Do not run a package/install target against a previously exercised stage: Python caches can change. Do not suppress ICE warnings or treat a successful MSI build as signing, clean-machine, repair or uninstall proof.
