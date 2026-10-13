"""Host-side product presentation tests; not Blender GUI/runtime evidence."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
WM = REPO / 'scripts/startup/bl_operators/wm.py'
AUDIT = REPO.parent / 'audit/product-identity'


class Layout:
    """Record real draw-method UI declarations without invoking Blender."""
    def __init__(self, recent=False):
        self.events = []
        self.recent = recent

    def split(self, **kwargs):
        return self

    def column(self, **kwargs):
        return self

    def row(self, **kwargs):
        return self

    def label(self, **kwargs):
        self.events.append(('label', kwargs, None))

    def separator(self, **kwargs):
        pass

    def template_recent_files(self, **kwargs):
        return self.recent

    def operator(self, name, **kwargs):
        props = types.SimpleNamespace()
        self.events.append((name, kwargs, props))
        return props


def draw_menu(name, recent=False, backend='DEFAULT', offline=False):
    tree = ast.parse(WM.read_text(encoding='utf-8'))
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name)
    app = types.SimpleNamespace(version_string='5.4.0 Alpha', build_commit_date=b'2026-10-12',
                                build_commit_time=b'12:34:56', build_hash=b'de6e3c4fb918',
                                build_branch=b'brand/lunola-forma', online_access=not offline,
                                online_access_override=offline)
    bpy = types.SimpleNamespace(app=app, types=types.SimpleNamespace(TOPBAR_MT_file_new=
                                types.SimpleNamespace(draw_ex=lambda *a, **k: None)))
    namespace = dict(Menu=object, bpy=bpy, iface_=lambda value: value)
    module = types.ModuleType('_bpy')
    module._ghost_backend = lambda: backend
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(WM), 'exec'), namespace)
    layout = Layout(recent)
    menu = namespace[name]()
    menu.layout = layout
    with patch.dict(sys.modules, {'_bpy': module}):
        menu.draw(types.SimpleNamespace())
    return layout.events


class Presentation(unittest.TestCase):
    def test_product_byline_and_compact_upstream_legal_section(self):
        events = draw_menu('WM_MT_splash_about')
        labels = [kw['text'] for kind, kw, _ in events if kind == 'label']
        self.assertIn('by Pujo Setyo', labels)
        self.assertIn('Lunola Forma is free software', labels)
        self.assertIn('Licensed under the GNU General Public License', labels)
        self.assertIn('License & Source', labels)
        self.assertIn('Upstream: Blender', labels)
        self.assertNotIn('Based on Blender', labels)
        license_buttons = [p.url for kind, kw, p in events if kw.get('text') == 'GNU GPL License & Source']
        self.assertEqual(license_buttons, ['https://www.blender.org/about/license/'])
        authors = [p.type for kind, kw, p in events if kw.get('text') == 'Upstream Authors']
        self.assertEqual(authors, ['CREDITS'])

    def test_no_optional_upstream_promotion_in_about_or_splash(self):
        for menu in ('WM_MT_splash', 'WM_MT_splash_about'):
            for recent in (False, True):
                events = draw_menu(menu, recent)
                texts = [kw.get('text', '') for _, kw, _ in events]
                for unwanted in ('Donate to Blender', 'Blender Store', 'Blender Website', 'Blender Credits',
                                 'Get Involved', 'User Communities', "What's New", 'Blender Release Notes'):
                    self.assertNotIn(unwanted, texts)
                presets = [getattr(p, 'type', '') for _, _, p in events if p]
                self.assertNotIn('FUND', presets)
                self.assertNotIn('BLENDER', presets)
                self.assertNotIn('RELEASE_NOTES', presets)

    def test_actual_build_metadata_and_backend_are_preserved(self):
        labels = [kw['text'] for kind, kw, _ in draw_menu('WM_MT_splash_about', backend='WAYLAND') if kind == 'label']
        for expected in ('Version: 5.4.0 Alpha', 'Date: 2026-10-12 12:34:56', 'Hash: de6e3c4fb918',
                         'Branch: brand/lunola-forma', 'Windowing Environment: WAYLAND'):
            self.assertIn(expected, labels)

    def test_splash_keeps_file_actions_manual_and_offline_notice(self):
        events = draw_menu('WM_MT_splash', offline=True)
        actions = [kind for kind, _, _ in events]
        self.assertIn('wm.open_mainfile', actions)
        self.assertIn('wm.recover_last_session', actions)
        self.assertIn('MANUAL', [getattr(p, 'type', '') for _, _, p in events if p])
        self.assertIn('Running in Offline Mode', [kw.get('text') for _, kw, _ in events])
        events = draw_menu('WM_MT_splash', recent=True)
        self.assertIn('TOPBAR_MT_file_open_recent', [getattr(p, 'menu_idname', '') for _, _, p in events if p])

    def test_only_two_owned_classes_changed(self):
        before = ast.parse((AUDIT / 'wm-before.py').read_text(encoding='utf-8'))
        after = ast.parse(WM.read_text(encoding='utf-8'))
        owned = {'WM_MT_splash', 'WM_MT_splash_about'}
        for tree in (before, after):
            tree.body = [n for n in tree.body if not (isinstance(n, ast.ClassDef) and n.name in owned)]
        self.assertEqual(ast.dump(before), ast.dump(after))
        prefix = WM.read_bytes().split(b'class WM_MT_splash(Menu):')[0]
        self.assertEqual(prefix, (AUDIT / 'wm-before.py').read_bytes().split(b'class WM_MT_splash(Menu):')[0])


def expected_splash():
    from PIL import Image, ImageDraw, ImageFont
    base = HERE.parent
    expected = Image.new('RGB', (1000, 500), (247, 245, 241))
    with Image.open(base / 'originals/lunola-forma-splash-art.png') as art:
        expected.paste(art.resize((500, 500), Image.Resampling.LANCZOS), (500, 0))
    with Image.open(base / 'originals/lunola-forma-logo.png') as logo:
        resized = logo.convert('RGBa').resize((420, 140), Image.Resampling.LANCZOS).convert('RGBA')
        expected.paste(resized, (40, 125), resized.getchannel('A'))
    draw = ImageDraw.Draw(expected)
    draw.text((40, 294), 'Professional 3D Creation Suite', font=ImageFont.load_default(size=23), fill=(39, 43, 54))
    draw.text((40, 407), 'by Pujo Setyo', font=ImageFont.load_default(size=18), fill=(39, 43, 54))
    return expected


class ProductAssets(unittest.TestCase):
    def test_new_variant_pixels_match_approved_art_and_requested_byline(self):
        from PIL import Image
        path = HERE / 'lunola-forma-splash.png'
        self.assertTrue(path.is_file(), 'New separately owned product splash is missing')
        with Image.open(path) as image:
            self.assertEqual(image.format, 'PNG')
            self.assertEqual(image.size, (1000, 500))
            self.assertEqual(image.mode, 'RGB')
            self.assertEqual(image.tobytes(), expected_splash().tobytes())

    def test_embedded_splash_has_product_byline(self):
        from PIL import Image
        with Image.open(REPO / 'release/datafiles/splash.png') as image:
            self.assertEqual(hashlib.sha256(image.tobytes()).hexdigest(),
                             hashlib.sha256(expected_splash().tobytes()).hexdigest())

    def test_only_byline_rectangle_changed_from_phase_b(self):
        from PIL import Image, ImageChops
        path = HERE / 'lunola-forma-splash.png'
        self.assertTrue(path.is_file(), 'New variant is missing')
        with Image.open(path) as actual, Image.open(HERE.parent / 'derived/splash/lunola-forma-splash.png') as original:
            box = ImageChops.difference(actual, original).getbbox()
            self.assertIsNotNone(box)
            self.assertGreaterEqual(box[0], 40)
            self.assertGreaterEqual(box[1], 407)
            self.assertLessEqual(box[2], 240)
            self.assertLessEqual(box[3], 435)
            self.assertEqual(actual.crop((500, 0, 1000, 500)).tobytes(), original.crop((500, 0, 1000, 500)).tobytes())
            self.assertEqual(actual.crop((40, 125, 460, 265)).tobytes(), original.crop((40, 125, 460, 265)).tobytes())

    def test_phase_b_files_and_approved_originals_unchanged(self):
        for name, digest in json.loads((AUDIT / 'before-hashes.json').read_text()).items():
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256(Path(name).read_bytes()).hexdigest(), digest)

    def test_manifest_pins_sources_recipe_and_embedded_identity(self):
        path = HERE / 'manifest.json'
        self.assertTrue(path.is_file(), 'Separate product identity manifest is missing')
        manifest = json.loads(path.read_text())
        self.assertEqual(manifest['recipe']['byline'], 'by Pujo Setyo')
        self.assertFalse(manifest['recipe']['version_baked'])
        self.assertEqual(manifest['recipe']['edit_rect'], [40, 407, 240, 435])
        self.assertEqual(manifest['pillow'], '12.3.0')
        for record in manifest['inputs'] + manifest['outputs']:
            source = HERE / record['path']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), record['sha256'])
        output = HERE / 'lunola-forma-splash.png'
        self.assertEqual(output.read_bytes(), (REPO / 'release/datafiles/splash.png').read_bytes())
        self.assertEqual(len(manifest['outputs']), 1)

    def load_generator(self):
        import importlib.util
        path = HERE / 'generate_splash.py'
        self.assertTrue(path.is_file(), 'Separate reproducible recipe is missing')
        spec = importlib.util.spec_from_file_location('product_splash_generator', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_reproducible_recipe_does_not_modify_inputs(self):
        import tempfile
        generator = self.load_generator()
        with tempfile.TemporaryDirectory(prefix='.recipe-test-', dir=HERE) as temp:
            regenerated = generator.generate(Path(temp))
            self.assertEqual(regenerated, json.loads((HERE / 'manifest.json').read_text()))
            self.assertEqual((Path(temp) / 'lunola-forma-splash.png').read_bytes(), (HERE / 'lunola-forma-splash.png').read_bytes())
        self.test_phase_b_files_and_approved_originals_unchanged()

    def test_generator_rejects_writes_outside_variant_folder(self):
        generator = self.load_generator()
        with self.assertRaisesRegex(ValueError, 'product-identity'):
            generator.generate(HERE.parent)

    def test_modified_input_rejected_before_output_write(self):
        import tempfile
        generator = self.load_generator()
        with tempfile.TemporaryDirectory(prefix='.input-test-', dir=HERE) as temp:
            base = Path(temp)
            phase_b = base / 'bad.png'
            phase_b.write_bytes(b'not the pinned Phase B splash')
            output = base / 'output'
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                generator.generate(output, source=phase_b)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
