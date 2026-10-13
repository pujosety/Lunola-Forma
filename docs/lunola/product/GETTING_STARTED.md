# Get started with Lunola Forma

**by Pujo Setyo**

## Open the application

Use the complete Windows portable folder supplied with your build. Run `blender.exe` inside it; the technical filename is retained for compatibility. Do not move only the executable out of its folder, because it needs the bundled runtime and resources.

The new branded output is being prepared at `D:/Lunola/Forma/Lunola-Forma`. Wait for its verification report before treating it as a tested release. The earlier Phase C application is at `D:/Lunola/Forma/build-phase-c/bin/Release/blender.exe` and still has the old splash and icons.

## Create your first scene

Choose **General** from the startup screen. The scene contains a cube, a camera, and a light.

Select the cube. Use **G** to move it, **R** to rotate it, and **S** to scale it. Press **Tab** to enter Edit Mode when you want to work on its mesh. Lunola Forma keeps the existing keymap and workspace behavior.

Switch to **Shading** to experiment with materials, or use **Animation** to work with keyframes. Choose Eevee or Cycles in the render settings for your scene. Availability of individual GPU devices depends on the build and hardware.

## Save your project

Use **File > Save As** and keep the `.blend` extension. Save a separate copy before opening an important project with this alpha build. Test a saved file by closing and reopening it before you replace an established working copy.

## Keep creating

[Compatibility notes](COMPATIBILITY.md) explain retained formats and APIs. If startup or rendering fails, use [troubleshooting](TROUBLESHOOTING.md) before changing system settings.
