# SPDX-License-Identifier: GPL-2.0-or-later
"""Source-only privacy contracts for native issue navigation."""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[3]

class CrashNavigationTests(unittest.TestCase):
    def test_native_report_opens_empty_lunola_issue_form(self):
        text = (ROOT / 'source/blender/blenlib/intern/system_win32.cc').read_text()
        block = text.split('case IDOK: {', 1)[1].split('return S_FALSE;', 1)[0]
        self.assertIn('lunola::issue_report_url', block)
        for forbidden in ['redirect.blender.org', '&os=', '&gpu=', '&broken_version=', 'url_encode_wstring']:
            self.assertNotIn(forbidden, block)
        header = (ROOT / 'source/blender/blenlib/BLI_lunola_identity.hh').read_text()
        self.assertIn('https://github.com/pujosety/Lunola-Forma/issues/new', header)
        self.assertIn('Review and redact', text)
        self.assertIn('Report an Issue', text)

if __name__ == '__main__':
    unittest.main()
