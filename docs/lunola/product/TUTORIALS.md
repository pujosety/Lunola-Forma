# First scene in Lunola Forma

**by Pujo Setyo**

This short guide adapts the actual scene, transform and save steps from [Getting started](GETTING_STARTED.md). It is not a collection of unavailable videos or promised courses. It assumes you have a complete, verified local build; public binary releases are pending. The engine base is **5.4.0 Alpha**.

## 1. Open a scene

Run `blender.exe` inside the complete installed Windows folder. Keep its runtime and resources together. Choose **General** from the startup screen to begin with a cube, camera and light. Technical filenames and the existing keymap are retained.

## 2. Transform the cube

Select the cube. Press **G** to move it, **R** to rotate it or **S** to scale it. Confirm with the left mouse button or Enter; cancel with Escape. Press **Tab** to switch between Object Mode and Edit Mode when working on the mesh. These steps assume the existing default keymap; customized keymaps may differ.

## 3. Explore materials and animation

Switch to **Shading** to explore materials or **Animation** for keyframes. Eevee and Cycles retain their technical names. The recorded local smoke suite includes small Eevee and Cycles CPU renders; it does not certify every GPU or render setup. See [compatibility](COMPATIBILITY.md).

## 4. Save and reopen safely

Choose **File > Save As** and keep the `.blend` extension. Save to a new file rather than overwriting an important established project. Close and reopen the saved copy to check your workflow before using it as a working copy. Alpha-version compatibility is not guaranteed with older engine versions.

## If something fails

Read [Troubleshooting](TROUBLESHOOTING.md) and the [issue-reporting guide](../ISSUE_REPORTING.md). Share a minimal reproduction only after removing private content. Existing guide references to local build paths are historical notes, not downloadable release packages.
