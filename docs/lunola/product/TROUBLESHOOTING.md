# Troubleshooting

**by Pujo Setyo**

## Startup reports that Vulkan failed

The tested machine reports that no Vulkan device meets the current build's requirements. The application falls back to OpenGL. This warning also appears in the unmodified baseline; it is not evidence of a branding regression.

Keep the warning and log when reporting the issue. Do not change the rendering architecture or install a random driver package to make the warning disappear. Driver changes are a separate system-maintenance decision.

## The splash or icon still shows Blender

Check which executable you opened. The baseline and Phase C outputs intentionally retain the old splash and native icons. The later branding output uses a separate portable destination.

Do not assume a running window updates when its source resources change. Use the executable named in the latest verified build report. Native icon caches and pinned shortcuts may also need separate inspection after the correct binary is confirmed.

## An add-on does not work

Record the application's actual version, the add-on version, and the error message. Try the add-on in a disposable project. Do not overwrite your only working file while investigating an alpha-build issue.

## A render fails

Save the scene and capture the log. Record the selected engine and whether the device is CPU or GPU. Compare against the same scene in the unmodified baseline before labeling the failure a fork regression.

## Report a problem

Provide the build version and hash, operating system, GPU details, steps to reproduce, and a small sample project when possible. Do not include passwords, private assets, or confidential scene data. A Lunola support URL has not been configured; do not send fork-specific branding issues to upstream as if they were official Blender defects.
