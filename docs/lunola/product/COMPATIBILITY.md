# Projects, scripts, and add-ons

**by Pujo Setyo**

Lunola Forma changes the application's presentation without renaming its technical interfaces.

## Project files

Keep `.blend` files, linked libraries, and append workflows in their existing formats. Branding does not change file signatures, DNA/RNA identifiers, or serialization.

File compatibility still follows the underlying engine version. An alpha build may contain changes that older versions do not understand. Keep an original copy and check your workflow before migrating a project.

## Python and add-ons

The Python module remains `bpy`. Existing operator IDs, Python namespaces, and add-on interfaces retain their names. The executable remains `blender.exe`, and the launcher remains `blender-launcher.exe`.

The current smoke suite checks a temporary add-on's registration and removal. It does not certify every third-party add-on. Test each add-on against the exact build you intend to use.

## Rendering

Cycles and Eevee keep their technical names and existing behavior. Both have passed small renders in the baseline and Phase C smoke suites, including a Cycles CPU render. GPU backend parity and every device configuration have not been verified.

## Preferences and associations

The current fork retains upstream configuration paths and application identifiers. It does not yet promise separate side-by-side preferences or taskbar grouping. No operating-system file associations have been changed by this project.
