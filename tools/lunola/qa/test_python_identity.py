# SPDX-License-Identifier: GPL-2.0-or-later
"""Host/source identity checks; not Blender runtime or GUI certification."""
import ast
from pathlib import Path
import runpy
import subprocess
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[3]
STARTUP = 'scripts/modules/_bpy_internal/system_info/url_prefill_startup.py'


def source(path):
    return (ROOT / path).read_text(encoding='utf-8')


COPY_CHANGES = {
    'scripts/startup/bl_ui/space_userpref.py': [
        ('Load Factory Blender Preferences', 'Load Factory Lunola Forma Preferences'),
        ('Blender Version', 'Blender Engine Version'),
        ('A restart of Blender is required', 'A restart of Lunola Forma is required'),
        ('Open blend files with this Blender version', 'Open blend files with this Lunola Forma version'),
    ],
    'scripts/startup/bl_operators/assets.py': [
        ('Blender sub-process exited with error code {:d}', 'Lunola Forma sub-process exited with error code {:d}'),
    ],
    'scripts/startup/bl_operators/project.py': [
        ('Project configuration is newer than this version of Blender supports',
         'Project configuration is newer than this version of Lunola Forma supports'),
    ],
    'scripts/startup/bl_operators/image.py': [
        ('and Blender has rights to launch it', 'and Lunola Forma has rights to launch it'),
    ],
    'scripts/startup/bl_operators/image_as_planes.py': [
        ('Force reload the image if it is already opened elsewhere in Blender',
         'Force reload the image if it is already opened elsewhere in Lunola Forma'),
    ],
    'scripts/addons_core/rigify/ui.py': [
        ('Get active/selected colors from current Blender theme', 'Get active/selected colors from current Lunola Forma theme'),
        ("Set the color palette to match Blender's active theme for selected and active bones",
         "Set the color palette to match Lunola Forma's active theme for selected and active bones"),
    ],
    'scripts/addons_core/bl_pkg/bl_extension_ops.py': [
        ('If the lock was held by a Blender instance that exited unexpectedly,',
         'If the lock was held by a Lunola Forma or upstream Blender instance that exited unexpectedly,'),
        ('Launch Blender without --offline-mode', 'Launch Lunola Forma without --offline-mode'),
        ('either wait until the operation is finished or restart Blender',
         'either wait until the operation is finished or restart Lunola Forma'),
        ('Warning! Before unlocking, ensure another instance of Blender is not running.',
         'Warning! Before unlocking, ensure no Lunola Forma or upstream Blender instance is using this repository.'),
        ('Blender was launched in offline mode, which cannot be changed at runtime',
         'Lunola Forma was launched in offline mode, which cannot be changed at runtime'),
        ('Allow Blender to access the internet.', 'Allow Lunola Forma to access the internet.'),
        ('However, Blender cannot prevent third-party add-ons from',
         'However, Lunola Forma cannot prevent third-party add-ons from'),
    ],
    'scripts/modules/_bpy_internal/system_info/text_generate_runtime.py': [
        ('= Blender {:s} System Information =', '= Lunola Forma {:s} System Information ='),
        ('title("Blender")', 'title("Blender Engine Build")'),
        ('Blender was built', 'Lunola Forma was built'),
    ],
    STARTUP: [
        ('Follow our guide to collect this information:', 'Follow the upstream Blender guide to collect this information:'),
        ('Blender did not provide any build information. Blender may be corrupt or blocked from running.',
         'Lunola Forma did not provide any build information. Lunola Forma may be corrupt or blocked from running.'),
        ("Please try reinstalling Blender and double check your anti-virus isn't blocking it from running.",
         "Please try reinstalling Lunola Forma and double check your anti-virus isn't blocking it from running."),
    ],
    'scripts/addons_core/bl_pkg/bl_extension_ui.py': [
        ('Add-ons previously shipped with Blender are now available from extensions.blender.org.',
         'Add-ons previously shipped with upstream Blender are now available from extensions.blender.org.'),
        ("Blender's extension repository", 'Upstream Blender extension repository'),
        ('Visit Extensions Platform', 'Visit Upstream Blender Extensions'),
        ('Internet access is required to install and update online extensions.',
         'Internet access is required for the selected upstream or third-party extension repositories.'),
    ],
}


BASELINE = 'f55fdf13a57992398b3b1535e5da5b879774d0cf'


def baseline_source(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT).decode('utf-8')


# Exact non-copy UI adjustments allowed by this review. Comparing the complete
# AST against the pinned source plus this allowlist protects contracts and flow,
# not merely a handful of expected labels. No Blender module is imported.
STRUCTURAL_CHANGES = {
    'scripts/modules/rna_keymap_ui.py': [
        ('if not text:\n        text = "Blender (default)"',
         'if not text or kc_active.name == "Blender":\n        text = "Lunola Forma (Blender-compatible)"'),
    ],
    'scripts/startup/bl_ui/space_userpref.py': [
        ('text="Documentation", icon=',
         'text="Add-on Documentation" if user_addon else "Upstream Add-on Documentation", icon='),
        ('text="Report a Bug", icon=',
         'text="Report Add-on Bug" if user_addon else "Report Upstream Add-on Bug", icon='),
        ('text=text, icon=\'URL\').url = url_prefix + url_ext',
         'text="Upstream: " + text, icon=\'URL\').url = url_prefix + url_ext'),
    ],
    'scripts/addons_core/bl_pkg/bl_extension_ui.py': [
        ('col_a.label(text="Website")\n        col_b.link(url=item_doc_url',
         'col_a.label(text="Upstream Add-on Website" if addon_type == ADDON_TYPE_LEGACY_CORE '
         'else "Add-on / Extension Website")\n        col_b.link(url=item_doc_url'),
        ('col_a.label(text="Feedback", text_ctxt=i18n_contexts.editor_preferences)',
         'col_a.label(text="Upstream Add-on Feedback" if addon_type == ADDON_TYPE_LEGACY_CORE '
         'else "Add-on / Extension Feedback", text_ctxt=i18n_contexts.editor_preferences)'),
        ('"wm.url_open",\n        text="",\n        icon=\'URL\',\n        emboss=False,',
         '"wm.url_open",\n        text="Upstream Extension Manual",\n        icon=\'URL\',\n        emboss=False,'),
    ],
    'scripts/modules/_bpy_internal/system_info/text_generate_runtime.py': [
        ('    output.write(header)\n    output.write(lilies)',
         '    output.write(header)\n    output.write(lilies)\n'
         '    output.write("Lunola Forma by Pujo Setyo; based on the Blender engine.\\n")\n'
         '    output.write("Review and redact local paths and add-on details before sharing this file.\\n")'),
    ],
}


class PythonIdentityTests(unittest.TestCase):
    def test_complete_ast_preserves_contracts_except_reviewed_changes(self):
        for path in sorted(set(COPY_CHANGES) | set(STRUCTURAL_CHANGES)):
            with self.subTest(path=path):
                expected = baseline_source(path)
                for old, new in COPY_CHANGES.get(path, []) + STRUCTURAL_CHANGES.get(path, []):
                    self.assertIn(old, expected, 'Invalid review allowlist')
                    expected = expected.replace(old, new)
                trees = [ast.parse(expected), ast.parse(source(path))]
                if path == STARTUP:
                    # Route body is executed separately; still compare its API
                    # signature and the complete explicit-upstream helper body.
                    for tree in trees:
                        main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
                        main.body = []
                self.assertEqual(ast.dump(trees[0]), ast.dump(trees[1]), path)
                notices = [line for line in baseline_source(path).splitlines() if 'SPDX-' in line]
                self.assertEqual(notices, [line for line in source(path).splitlines() if 'SPDX-' in line])

    def test_untouched_addon_service_and_template_sources(self):
        paths = [
            'scripts/modules/_bpy_internal/system_info/url_prefill_runtime.py',
            'scripts/modules/bpy/utils/__init__.py',
            'scripts/modules/addon_utils.py',
            'scripts/modules/_rna_manual_reference.py',
            'scripts/modules/_rna_info.py',
            'scripts/modules/_bl_i18n_utils/settings.py',
            'scripts/modules/_bpy_internal/http/downloader.py',
            'scripts/modules/_bpy_internal/assets/remote_library/asset_downloader.py',
            'scripts/modules/_bpy_internal/assets/remote_library/listing_downloader.py',
            'scripts/addons_core/bl_pkg/__init__.py',
            'scripts/addons_core/bl_pkg/cli/blender_ext.py',
            'scripts/addons_core/bl_pkg/bl_extension_notify.py',
            'scripts/addons_core/bl_pkg/extensions_map_from_legacy_addons.py',
            'scripts/addons_core/rigify/feature_set_list.py',
            'scripts/addons_core/io_scene_gltf2/blender/exp/exporter.py',
            'scripts/addons_core/io_scene_fbx/export_fbx_bin.py',
            'scripts/addons_core/io_mesh_uv_layout/export_uv_eps.py',
            'scripts/addons_core/io_mesh_uv_layout/export_uv_svg.py',
        ]
        paths.extend('scripts/startup/bl_app_templates_system/' + name + '/__init__.py'
                     for name in ('2D_Animation', 'Sculpting', 'Storyboarding', 'Video_Editing'))
        paths.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'scripts/addons_core').glob('*/__init__.py'))
        for path in sorted(set(paths)):
            with self.subTest(path=path):
                self.assertEqual(source(path), baseline_source(path), path)

    def test_safe_product_copy(self):
        for path, replacements in COPY_CHANGES.items():
            text = source(path)
            for old, new in replacements:
                with self.subTest(path=path, old=old):
                    self.assertTrue(old not in text, 'Old UI copy remains: ' + old)
                    self.assertTrue(new in text, 'Missing UI copy: ' + new)

    def test_keyconfig_display_alias_preserves_canonical_name(self):
        text = source('scripts/modules/rna_keymap_ui.py')
        tree = ast.parse(text)
        draw = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'draw_keymaps')
        alias = next(n for n in draw.body if isinstance(n, ast.If))
        self.assertIn('kc_active.name == \'Blender\'', ast.unparse(alias.test))
        self.assertIn('Lunola Forma (Blender-compatible)', ast.unparse(alias))
        self.assertTrue(all(not isinstance(n, ast.Attribute) or n.attr != 'name'
                            for n in ast.walk(draw) if isinstance(getattr(n, 'ctx', None), ast.Store)))
        self.assertIn('default_config = "Blender"', source('scripts/modules/bpy/utils/__init__.py'))

    def test_external_destination_labels(self):
        prefs = source('scripts/startup/bl_ui/space_userpref.py')
        extension = source('scripts/addons_core/bl_pkg/bl_extension_ui.py')
        for label in ('Upstream Add-on Documentation', 'Add-on Documentation',
                      'Report Upstream Add-on Bug', 'Report Add-on Bug', 'Upstream: '):
            self.assertTrue(label in prefs, 'Missing external label: ' + label)
        for label in ('Upstream Add-on Website', 'Add-on / Extension Website',
                      'Upstream Add-on Feedback', 'Add-on / Extension Feedback', 'Upstream Extension Manual'):
            self.assertTrue(label in extension, 'Missing external label: ' + label)
        # Evaluate only the conditional label expressions, not mocked bpy/UI.
        for text, flag, values in ((prefs, 'user_addon', (True, False)),
                                  (extension, 'addon_type', ('core', 'user', 'extension'))):
            nodes = [n for n in ast.walk(ast.parse(text)) if isinstance(n, ast.IfExp)
                     and any(isinstance(c, ast.Constant) and isinstance(c.value, str)
                             and 'Upstream Add-on' in c.value for c in ast.walk(n))]
            self.assertEqual(len(nodes), 2)
            for value in values:
                namespace = {flag: value, 'ADDON_TYPE_LEGACY_CORE': 'core'}
                for node in nodes:
                    label = eval(compile(ast.Expression(node), '<label-only>', 'eval'), {}, namespace)
                    upstream = value is False if flag == 'user_addon' else value == 'core'
                    self.assertEqual('Upstream' in label, upstream)

    def test_diagnostic_product_byline_keeps_engine_attribution(self):
        text = source('scripts/modules/_bpy_internal/system_info/text_generate_runtime.py')
        self.assertTrue('Lunola Forma by Pujo Setyo; based on the Blender engine.' in text)
        self.assertTrue('Review and redact local paths and add-on details before sharing this file.' in text)
        self.assertIn('bpy.app.version_string', text)
        self.assertIn('Blender Engine Build', text)

    def test_direct_script_entry_without_blender_or_module_path(self):
        # A fresh isolated host interpreter exercises __main__ with a browser
        # sink only; it is not an application startup/runtime test.
        program = '''import runpy, sys
from unittest.mock import patch
from urllib.parse import urlsplit
path = sys.argv[1]
assert 'bpy' not in sys.modules
with patch('webbrowser.open', return_value=True) as browser:
    try:
        runpy.run_path(path, run_name='__main__')
    except SystemExit as result:
        assert result.code == 0
    else:
        raise AssertionError('Missing CLI exit')
    browser.assert_called_once()
    url = browser.call_args.args[0]
    assert url == 'https://github.com/pujosety/Lunola-Forma/issues/new'
    assert not urlsplit(url).query
assert 'bpy' not in sys.modules
'''
        result = subprocess.run([__import__('sys').executable, '-I', '-B', '-c', program, str(ROOT / STARTUP)],
                                cwd=ROOT.parent, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('No system information is included.', result.stdout)
        self.assertNotIn('Collecting system information', result.stdout)

    def test_standalone_issue_route_does_not_collect_diagnostics(self):
        # Execute the real standalone entry point with only the browser sink
        # intercepted; no bpy, network requests, browser launch or config writes.
        namespace = runpy.run_path(str(ROOT / STARTUP))
        def forbidden():
            self.fail('Product routing must not call upstream diagnostics')
        namespace['main'].__globals__['url_from_blender'] = forbidden
        expected = runpy.run_path(str(ROOT / 'scripts/modules/_lunola_urls.py'))['LUNOLA_BUG_REPORT_URL']
        with patch('webbrowser.open', return_value=True) as browser:
            self.assertEqual(namespace['main'](), 0)
        browser.assert_called_once_with(expected)
        self.assertEqual(urlsplit(expected).query, '')
        self.assertEqual(urlsplit(expected).fragment, '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
