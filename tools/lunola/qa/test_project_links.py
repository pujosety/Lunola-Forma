# SPDX-License-Identifier: GPL-2.0-or-later
"""Host contracts for product links; these are not application runtime tests."""
import importlib.util
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[3]
MODULE = ROOT / 'scripts/modules/_lunola_urls.py'

class ProjectLinksTests(unittest.TestCase):
    def test_startup_labels_do_not_rename_saved_presets(self):
        wm = (ROOT / 'scripts/startup/bl_operators/wm.py').read_text(encoding='utf-8')
        quick = wm.split('class WM_MT_splash_quick_setup(Menu):', 1)[1].split('\n\nclass ', 1)[0]
        self.assertIn('Lunola Forma Dark', quick)
        self.assertIn('text = "Lunola Forma"', quick)
        self.assertNotIn('Lunola Forma (Blender-compatible)', quick)
        self.assertIn('prefs.view', quick)
        self.assertNotIn('kc.name =', quick)
        self.assertNotIn('Import Blender', quick)
        top = (ROOT / 'scripts/startup/bl_ui/space_topbar.py').read_text(encoding='utf-8')
        self.assertIn('Load Factory Lunola Forma Settings', top)

    def test_help_and_about_use_product_navigation(self):
        help_source = (ROOT / 'scripts/startup/bl_ui/space_topbar.py').read_text(encoding='utf-8')
        help_menu = help_source.split('class TOPBAR_MT_help(Menu):', 1)[1].split('\n\nclass ', 1)[0]
        for label in ['Lunola Forma Documentation', 'Report an Issue', 'Feature Requests', 'Lunola Forma GitHub', 'Licenses & Open Source Credits', 'About Lunola Forma']:
            self.assertIn(label, help_menu)
        self.assertNotIn('https://www.blender.org/support', help_menu)
        wm = (ROOT / 'scripts/startup/bl_operators/wm.py').read_text(encoding='utf-8')
        about = wm.split('class WM_MT_splash_about(Menu):', 1)[1].split('\n\nclass ', 1)[0]
        self.assertIn('Based on Blender, an open-source 3D creation application.', about)
        self.assertIn('Professional 3D Creation Suite', about)
        self.assertIn('LUNOLA_PROJECT_URL', about)
        self.assertIn('credits = layout.column', about)
        self.assertIn('text="Upstream GPL"', about)
        self.assertIn('bpy.app.build_hash', about)
        bug = wm.split('def _url_from_bug():', 1)[1].split('@staticmethod', 1)[0]
        self.assertIn('LUNOLA_BUG_REPORT_URL', bug)
        self.assertNotIn('url_from_blender', bug)

    def test_product_destinations_are_centralized_and_privacy_safe(self):
        self.assertTrue(MODULE.is_file(), 'Missing centralized Lunola URL module')
        spec = importlib.util.spec_from_file_location('_lunola_urls', MODULE)
        urls = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(urls)
        self.assertEqual(urls.LUNOLA_PROJECT_URL, 'https://github.com/pujosety/Lunola-Forma')
        self.assertEqual(urls.LUNOLA_DOCS_URL, urls.LUNOLA_PROJECT_URL + '#readme')
        self.assertEqual(urls.LUNOLA_ISSUES_URL, urls.LUNOLA_PROJECT_URL + '/issues')
        self.assertEqual(urls.LUNOLA_FEATURE_REQUEST_URL, urls.LUNOLA_ISSUES_URL + '/new')
        self.assertEqual(urls.LUNOLA_BUG_REPORT_URL, urls.LUNOLA_ISSUES_URL + '/new')
        self.assertFalse(urlsplit(urls.LUNOLA_BUG_REPORT_URL).query, 'No private system data in issue URLs')
        self.assertEqual(urls.LUNOLA_RELEASES_URL, urls.LUNOLA_PROJECT_URL + '/releases')
        self.assertNotEqual(urls.LUNOLA_RELEASE_NOTES_URL, urls.LUNOLA_RELEASES_URL, 'Empty releases require a useful fallback')
        self.assertIsNone(urls.LUNOLA_TUTORIALS_URL, 'Do not invent a tutorial collection')

if __name__ == '__main__':
    unittest.main()
