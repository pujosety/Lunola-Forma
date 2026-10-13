# SPDX-License-Identifier: GPL-2.0-or-later
"""Host-only display/template checks; never install or register associations.

Reverse the explicit allowed edits and compare the full original byte digest.
This protects IDs, paths, actions, legal text and every other non-display byte.
"""
import hashlib
from pathlib import Path
import plistlib
import os
import shutil
import subprocess
import tempfile
import uuid
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
PRODUCT_URL = "https://github.com/pujosety/Lunola-Forma"
CASES = {'cpack': ('build_files/cmake/packaging.cmake',
           'a787ace892ccf1d2110faec77d881e3e1f748908b8d0baebf18a953ab30e6221',
           [('set(PROJECT_DESCRIPTION  "Blender is the free and open source 3D creation suite '
             'software.")',
             'set(PROJECT_DESCRIPTION  "Lunola Forma - Professional 3D Creation Suite, based on '
             'Blender.")'),
            ('set(PROJECT_CONTACT      "foundation@blender.org")',
             '# No verified distributor email is available.\nset(PROJECT_CONTACT      "")'),
            ('set(PROJECT_VENDOR       "Blender Foundation")',
             'set(PROJECT_VENDOR       "Pujo Setyo")\n'
             '\n'
             '# Display/archive identity only; project targets and install identities stay '
             'unchanged.\n'
             'set(CPACK_PACKAGE_NAME "Lunola Forma")\n'
             'set(LUNOLA_PACKAGE_ARCHIVE_NAME "lunola-forma")'),
            ('${PROJECT_NAME_LOWER}-${MAJOR_VERSION}',
             '${LUNOLA_PACKAGE_ARCHIVE_NAME}-${MAJOR_VERSION}'),
            ('set(CPACK_PACKAGE_EXECUTABLES "blender-launcher" "Blender '
             '${MAJOR_VERSION}.${MINOR_VERSION}")',
             'set(CPACK_PACKAGE_EXECUTABLES "blender-launcher" "Lunola Forma '
             '${MAJOR_VERSION}.${MINOR_VERSION}")'),
            ('set(CPACK_CREATE_DESKTOP_LINKS "blender-launcher" "Blender '
             '${MAJOR_VERSION}.${MINOR_VERSION}")',
             '# Desktop-link entries are executable tokens, not display-name pairs.\n'
             'set(CPACK_CREATE_DESKTOP_LINKS "blender-launcher")'),
            ('${PROJECT_NAME}-${BLENDER_VERSION}-${BUILD_REV}-OSX-',
             '${LUNOLA_PACKAGE_ARCHIVE_NAME}-${BLENDER_VERSION}-${BUILD_REV}-OSX-'),
            ('${PROJECT_NAME}-${BLENDER_VERSION}-${BUILD_REV}-${PACKAGE_SYSTEM_NAME}-',
             '${LUNOLA_PACKAGE_ARCHIVE_NAME}-${BLENDER_VERSION}-${BUILD_REV}-${PACKAGE_SYSTEM_NAME}-'),
            ('string(TOLOWER ${PROJECT_NAME} PROJECT_NAME_LOWER)',
             'string(TOLOWER ${PROJECT_NAME} PROJECT_NAME_LOWER)\n'
             '# Preserve the technical RPM name instead of deriving it from the display label.\n'
             'set(CPACK_RPM_PACKAGE_NAME ${PROJECT_NAME_LOWER})')]),
 'wix': ('release/windows/installer_wix/WIX.template',
         '57c58919e0ed8d798ac585ada722922186678530860c913ee2f00c6312a55a7b',
         [('<ProgressText Action="RegisterBlender">Registering Blender</ProgressText>',
           '<ProgressText Action="RegisterBlender">Registering Lunola Forma</ProgressText>'),
          ('<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT" Value="Learn how to support '
           'Blender" />',
           '<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT" Value="Visit the Lunola Forma '
           'project and support" />'),
          ('<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOX" Value="1" />',
           '<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOX" Value="0" />'),
          ('https://fund.blender.org/?utm_source=blender-$(var.CPACK_PACKAGE_VERSION)-installer-msi',
           'https://github.com/pujosety/Lunola-Forma')]),
 'msix': ('release/windows/msix/AppxManifest.xml.template',
          '51f5c246babed1b043c132cddacecb4e691678d996acf9aa78a5d3545d5653e1',
          [('<DisplayName>Blender[LTSORNOT]</DisplayName>',
            '<DisplayName>Lunola Forma [VERSION]</DisplayName>'),
           ('<PublisherDisplayName>Blender Foundation</PublisherDisplayName>',
            '<PublisherDisplayName>Pujo Setyo</PublisherDisplayName>'),
           ('<Description>Blender [VERSION] is the Free and Open Source 3D creation '
            'suite</Description>',
            '<Description>Lunola Forma [VERSION] - Professional 3D Creation Suite, based on '
            'Blender</Description>'),
           ('DisplayName="Blender [VERSION]"', 'DisplayName="Lunola Forma [VERSION]"'),
           ('Description="Blender is the Free and Open Source 3D creation suite"',
            'Description="Lunola Forma - Professional 3D Creation Suite, based on Blender"'),
           ('ShortName="Blender [VERSION]"', 'ShortName="Lunola Forma [VERSION]"')]),
 'macos': ('release/darwin/Blender.app/Contents/Info.plist',
           '775639870740cc48c46cf8c45095d984d6c1dda0005ba73c21da279253c68267',
           [('<string>${MACOSX_BUNDLE_LONG_VERSION_STRING}, Blender Foundation</string>',
             '<string>${MACOSX_BUNDLE_LONG_VERSION_STRING}, Pujo Setyo</string>'),
            ('<key>CFBundleName</key>\n\t<string>Blender</string>',
             '<key>CFBundleName</key>\n\t<string>Lunola Forma</string>'),
            ('A Blender extension wants to access your microphone.',
             'A Lunola Forma extension wants to access your microphone.'),
            ('A Blender extension wants to access your camera.',
             'A Lunola Forma extension wants to access your camera.'),
            ('A Blender extension wants to capture your system audio.',
             'A Lunola Forma extension wants to capture your system audio.')]),
 'desktop': ('release/freedesktop/blender.desktop',
             'c4217dca99b95ba897824e7888a7583f7fa92581585e7aaf1d5161c6ce24f776',
             [('Name=Blender\n', 'Name=Lunola Forma\n')]),
 'resource': ('release/windows/icons/winblender.rc',
              'b1dbdc961f3862a1cabba20bba3c197bf658b7aac2d4a7fc0e16fb1107940ef1',
              [('VALUE "CompanyName", "Blender Foundation"', 'VALUE "CompanyName", "Pujo Setyo"')]),
 'appstream': ('release/freedesktop/org.blender.Blender.metainfo.xml',
               '751cab69351acb0c32b0310ac4052af87f8c4f5fa2ae427c63736a69b8fff056',
               [('    <name>Blender</name>\n'
                 '    <summary>Free and open source 3D creation suite</summary>\n'
                 '    <metadata_license>CC0-1.0</metadata_license>\n'
                 '    <project_license>GPL-3.0</project_license>\n'
                 '    <description>\n'
                 '        <p>\n'
                 '            Blender is the free and open source 3D creation suite. It supports\n'
                 '            the entirety of the 3D pipeline — modeling, rigging, animation,\n'
                 '            simulation, rendering, compositing, motion tracking, and video\n'
                 '            editing.\n'
                 '        </p>\n'
                 '\n'
                 '        <p>\n'
                 '            Blender is a public project, made by hundreds of people from around '
                 'the\n'
                 '            world; by studios and individual artists, professionals and '
                 'hobbyists,\n'
                 '            scientists, students, VFX experts, animators, game artists, modders, '
                 'and\n'
                 '            the list goes on.\n'
                 '        </p>\n'
                 '    </description>\n'
                 '    <url type="homepage">https://www.blender.org</url>\n'
                 '    <url '
                 'type="bugtracker">https://projects.blender.org/blender/blender/issues?q=&amp;labels=296</url>\n'
                 '    <url type="faq">https://www.blender.org/support/faq/</url>\n'
                 '    <url type="help">https://www.blender.org/support/</url>\n'
                 '    <url type="donation">https://fund.blender.org/</url>\n'
                 '    <url '
                 'type="translate">https://developer.blender.org/docs/handbook/translating/translator_guide/</url>\n'
                 '    <url type="vcs-browser">https://projects.blender.org/blender/blender</url>\n'
                 '    <url type="contribute">https://www.blender.org/get-involved/</url>\n'
                 '    <screenshots>\n'
                 '        <screenshot type="default">\n'
                 '            <caption>Sculpt</caption>\n'
                 '            '
                 '<image>https://download.blender.org/demo/screenshots/blender_screenshot_1.jpg</image>\n'
                 '        </screenshot>\n'
                 '        <screenshot>\n'
                 '            <caption>Model</caption>\n'
                 '            '
                 '<image>https://download.blender.org/demo/screenshots/blender_screenshot_2.jpg</image>\n'
                 '        </screenshot>\n'
                 '        <screenshot>\n'
                 '            <caption>Animate</caption>\n'
                 '            '
                 '<image>https://download.blender.org/demo/screenshots/blender_screenshot_3.jpg</image>\n'
                 '        </screenshot>\n'
                 '        <screenshot>\n'
                 '            <caption>Edit &amp; Grade</caption>\n'
                 '            '
                 '<image>https://download.blender.org/demo/screenshots/blender_screenshot_4.jpg</image>\n'
                 '        </screenshot>\n'
                 '    </screenshots>\n',
                 '    <name>Lunola Forma</name>\n'
                 '    <summary>Professional 3D Creation Suite, based on Blender</summary>\n'
                 '    <metadata_license>CC0-1.0</metadata_license>\n'
                 '    <project_license>GPL-3.0</project_license>\n'
                 '    <description>\n'
                 '        <p>\n'
                 '            Lunola Forma is a free and open source 3D creation suite based on\n'
                 '            Blender, distributed by Pujo Setyo. It provides tools for modeling,\n'
                 '            rigging, animation, simulation, rendering, compositing, motion\n'
                 '            tracking, and video editing.\n'
                 '        </p>\n'
                 '        <p>\n'
                 '            Blender is the upstream project, created by its authors and\n'
                 '            contributors. Lunola Forma is a separate distribution and is not\n'
                 '            endorsed by the Blender Foundation.\n'
                 '        </p>\n'
                 '        <p>\n'
                 '            The release history below describes upstream Blender releases,\n'
                 '            not Lunola Forma releases.\n'
                 '        </p>\n'
                 '    </description>\n'
                 '    <url type="homepage">https://github.com/pujosety/Lunola-Forma</url>\n'
                 '    <url '
                 'type="bugtracker">https://github.com/pujosety/Lunola-Forma/issues</url>\n'
                 '    <url type="help">https://github.com/pujosety/Lunola-Forma/issues</url>\n'
                 '    <url type="vcs-browser">https://github.com/pujosety/Lunola-Forma</url>\n'
                 '    <url type="contribute">https://github.com/pujosety/Lunola-Forma</url>\n')])}


class PackagingIdentityTests(unittest.TestCase):
    def check_case(self, name):
        path, original_sha256, edits = CASES[name]
        data = (ROOT / path).read_bytes()
        newline = "\r\n" if b"\r\n" in data else "\n"
        text = data.decode("utf-8").replace("\r\n", "\n")
        for old, new in edits:
            with self.subTest(path=path, display=new):
                self.assertTrue(new in text, f"Missing display edit: {new}")
        # Revert in reverse order so adjacent scoped replacements remain exact.
        for old, new in reversed(edits):
            self.assertEqual(text.count(new), 1, (path, new))
            text = text.replace(new, old, 1)
        self.assertEqual(hashlib.sha256(text.replace("\n", newline).encode("utf-8")).hexdigest(), original_sha256,
                         f"Non-display/identity/legal bytes changed: {path}")
        if path.endswith((".xml", ".template")):
            rendered = re.sub(r"\$\(var\.[^)]+\)", "TEST_VALUE", data.decode("utf-8"))
            rendered = re.sub(r"\[(?:VERSION|PUBLISHER|ARCHITECTURE|PACKAGETYPE|LTSORNOT)\]", "TEST_VALUE", rendered)
            ET.fromstring(rendered)
        if path.endswith(".plist"):
            plistlib.loads(data)

    def test_cpack_display_and_preservation(self):
        self.check_case("cpack")

    def test_wix_display_and_preservation(self):
        self.check_case('wix')

    def test_msix_display_and_preservation(self):
        self.check_case('msix')

    def test_macos_display_and_preservation(self):
        self.check_case('macos')

    def test_desktop_display_and_preservation(self):
        self.check_case('desktop')

    def test_resource_display_and_preservation(self):
        self.check_case('resource')

    def test_appstream_display_and_preservation(self):
        self.check_case('appstream')


    def test_generated_cpack_config_without_build_or_install(self):
        cmake = os.environ.get("LUNOLA_TEST_CMAKE") or shutil.which("cmake")
        if not cmake:
            self.skipTest("Set LUNOLA_TEST_CMAKE to run the configure-only fixture")
        # Isolated synthetic version/platform fixture; not a supported-platform build.
        # Source directory has no .git, so packaging.cmake cannot execute Git.
        with tempfile.TemporaryDirectory(prefix="lunola-packaging-", dir=os.environ.get("TMPDIR")) as temp:
            src = Path(temp) / "fixture"
            out = Path(temp) / "config"
            src.mkdir()
            license_path = Path("release/license/spdx/GPL-3.0-or-later.txt")
            (src / license_path).parent.mkdir(parents=True)
            shutil.copyfile(ROOT / license_path, src / license_path)
            fixture = '\n'.join([
                'cmake_minimum_required(VERSION 3.21)',
                'project(Blender LANGUAGES NONE)',
                'set(BLENDER_VERSION_MAJOR 5)',
                'set(BLENDER_VERSION_MINOR 4)',
                'set(BLENDER_VERSION_PATCH 0)',
                'set(MSVC TRUE)',
                'set(CMAKE_SIZEOF_VOID_P 8)',
                'set(CPACK_GENERATOR ZIP)',
                f'include("{(ROOT / CASES["cpack"][0]).as_posix()}")',
            ])
            (src / "CMakeLists.txt").write_text(fixture, encoding="utf-8")
            command = [cmake, "-S", str(src), "-B", str(out)]
            ninja = Path(cmake).parents[2] / "Ninja/ninja.exe"
            if ninja.exists():
                command += ["-G", "Ninja", f"-DCMAKE_MAKE_PROGRAM={ninja.as_posix()}"]
            result = subprocess.run(command, capture_output=True, text=True, timeout=90)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            config = (out / "CPackConfig.cmake").read_text(encoding="utf-8")
            def value(key):
                match = re.search(r'set\(' + key + r' "([^"]*)"\)', config)
                self.assertIsNotNone(match, key)
                return match.group(1)
            self.assertEqual(value("CPACK_PACKAGE_NAME"), "Lunola Forma")
            self.assertEqual(value("CPACK_PACKAGE_VENDOR"), "Pujo Setyo")
            self.assertEqual(value("CPACK_RPM_PACKAGE_NAME"), "blender")
            self.assertNotIn("foundation@blender.org", config)
            contact = re.search(r'set\(CPACK_PACKAGE_CONTACT "([^"]*)"\)', config)
            self.assertTrue(contact is None or contact.group(1) == "")
            self.assertEqual(value("CPACK_PACKAGE_EXECUTABLES"), "blender-launcher;Lunola Forma 5.4")
            self.assertEqual(value("CPACK_CREATE_DESKTOP_LINKS"), "blender-launcher")
            self.assertEqual(value("CPACK_PACKAGE_INSTALL_DIRECTORY"), "Blender Foundation/Blender 5.4")
            self.assertEqual(value("CPACK_PACKAGE_INSTALL_REGISTRY_KEY"), "Blender Foundation/Blender 5.4")
            expected_guid = str(uuid.uuid5(uuid.UUID("507F933F-5898-404A-9A05-18282FD491A6"),
                                          "Blender Foundation/Blender 5.4")).upper()
            self.assertEqual(value("CPACK_WIX_UPGRADE_GUID"), expected_guid)
            self.assertRegex(value("CPACK_PACKAGE_FILE_NAME"),
                             r"^lunola-forma-5\.4\.0-git[0-9]{8}\.unknown-windows64$")


if __name__ == "__main__":
    unittest.main(verbosity=2)
