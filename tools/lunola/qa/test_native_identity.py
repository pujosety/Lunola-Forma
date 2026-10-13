# SPDX-License-Identifier: GPL-2.0-or-later
"""Curated native source contracts; not GUI or binary execution evidence."""
import json
from pathlib import Path
import re
import subprocess
import unittest
ROOT = Path(__file__).resolve().parents[3]
MANIFEST = json.loads((Path(__file__).parent / 'native_identity_manifest.json').read_text())

def non_literal_code(text):
    return re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"', '', text, flags=re.S)

class NativeIdentityTests(unittest.TestCase):
    def test_audited_display_literals_are_product_or_format_names(self):
        for entry in MANIFEST['changes']:
            with self.subTest(file=entry['file'], original=entry['original']):
                text = (ROOT / entry['file']).read_text(encoding='utf-8')
                self.assertIn(entry['replacement'], text)
                self.assertNotIn(entry['original'], text)

    def test_display_only_edits_preserve_all_non_literal_native_code(self):
        for name in sorted({e['file'] for e in MANIFEST['changes']}):
            with self.subTest(file=name):
                original = subprocess.check_output(['git', 'show', 'f55fdf13a57992398b3b1535e5da5b879774d0cf:' + name], cwd=ROOT).decode('utf-8').replace('\r\n', '\n')
                current = (ROOT / name).read_text(encoding='utf-8')
                # Reconstruct only the exact curated literal-line replacements.
                # This catches every edit outside the manifest without a C++ lexer heuristic.
                expected = original
                for entry in MANIFEST['changes']:
                    if entry['file'] == name:
                        expected = expected.replace(entry['original'], entry['replacement'])
                for entry in MANIFEST.get('navigation_changes', []):
                    if entry['file'] == name:
                        expected = expected.replace(entry['original'], entry['replacement'])
                self.assertEqual(expected, current)
                self.assertEqual(original.splitlines()[:3], current.splitlines()[:3])

    def test_cli_and_resource_symbol_exceptions_are_unchanged(self):
        for entry in MANIFEST['exceptions']:
            with self.subTest(file=entry['file']):
                self.assertIn(entry['original'], (ROOT / entry['file']).read_text(encoding='utf-8'))

if __name__ == '__main__':
    unittest.main()
