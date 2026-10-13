# SPDX-License-Identifier: GPL-2.0-or-later
"""Real-input installer derivative tests; no installer or GUI execution."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / 'tools/lunola/release/generate_installer_art.py'
APPROVED = None
FONT = None
HASHES = {
    'lunola-forma-logo.png': '9e2c53a548d398c536b929ab4dac0fa38702cf75294a2f1c14c847111e5ccdda',
    'lunola-forma-icon.png': 'e89ba124051b61175a05dfefb0d24f44c0fa6e7dd6eec23dd8dcb005a95bf111',
    'lunola-forma-splash-art.png': '18decbf5337fe62c178f32f04769fdd0adea4480cb0dcfc2a3c7ac9e29089bdc',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class InstallerArtTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / 'release/windows/installer_lunola'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='.qa-', dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'output'
        self.before = {name: digest(APPROVED / name) for name in HASHES}
        self.assertEqual(self.before, HASHES)
        self.addCleanup(self.assert_originals_unchanged)

    def assert_originals_unchanged(self):
        self.assertEqual({name: digest(APPROVED / name) for name in HASHES}, self.before)

    def run_generator(self, approved=None, output=None):
        return subprocess.run(
            [sys.executable, str(GENERATOR), '--approved-assets', str(approved or APPROVED),
             '--font', str(FONT), '--output', str(output or self.output)],
            capture_output=True, text=True,
        )

    def generate(self, output=None):
        result = self.run_generator(output=output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def composite(self, name, size):
        with Image.open(APPROVED / name) as image:
            resized = image.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
        return Image.alpha_composite(Image.new('RGBA', size, 'white'), resized).convert('RGB')

    def test_rejects_unapproved_bytes_before_writing(self):
        import shutil
        copied = self.root / 'copied'
        shutil.copytree(APPROVED, copied)
        for name in HASHES:
            with self.subTest(asset=name):
                original = (copied / name).read_bytes()
                (copied / name).write_bytes(original + b'unapproved')
                result = self.run_generator(approved=copied)
                self.assertNotEqual(result.returncode, 0, 'Unknown hash accepted')
                self.assertIn('Unapproved asset hash', result.stderr)
                self.assertFalse(self.output.exists())
                (copied / name).write_bytes(original)

    def test_rejects_source_overlapping_outputs_without_mutation(self):
        import shutil
        copied = self.root / 'copied'
        shutil.copytree(APPROVED, copied)
        before = {p.relative_to(copied).as_posix(): digest(p) for p in copied.rglob('*') if p.is_file()}
        for output in (copied, copied / 'nested', self.root):
            with self.subTest(output=output):
                result = self.run_generator(approved=copied, output=output)
                self.assertNotEqual(result.returncode, 0, 'Source-overlapping output accepted')
                self.assertIn('Unsafe output', result.stderr)
                after = {p.relative_to(copied).as_posix(): digest(p) for p in copied.rglob('*') if p.is_file()}
                self.assertEqual(after, before)
                self.assertFalse((output / 'LunolaDialog.bmp').exists())

    def test_manifest_provenance_and_duplicate_generation_are_deterministic(self):
        self.generate()
        manifest_path = self.output / 'manifest.json'
        self.assertTrue(manifest_path.is_file(), 'Missing provenance manifest')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        originals = {}
        for name, expected in HASHES.items():
            with Image.open(APPROVED / name) as image:
                originals[name] = {'sha256': expected, 'dimensions': list(image.size), 'mode': image.mode}
        self.assertEqual(manifest['originals'], originals)
        self.assertEqual(manifest['font'], {'source': FONT.as_posix(), 'sha256': digest(FONT), 'size_px': 12})
        self.assertEqual(manifest['placements'], {
            'logo': {'source': 'lunola-forma-logo.png', 'bitmap': 'LunolaDialog.bmp', 'xy': [10, 30], 'dimensions': [144, 48]},
            'splash': {'source': 'lunola-forma-splash-art.png', 'bitmap': 'LunolaDialog.bmp', 'xy': [10, 105], 'dimensions': [144, 144]},
            'icon': {'source': 'lunola-forma-icon.png', 'bitmap': 'LunolaBanner.bmp', 'xy': [434, 2], 'dimensions': [54, 54]},
        })
        self.assertEqual(manifest['byline']['text'], 'by Pujo Setyo')
        self.assertEqual(manifest['byline']['xy'], [10, 276])
        self.assertEqual(manifest['byline']['color_rgb'], [40, 40, 40])
        self.assertEqual(manifest['native_text_zones'], {'LunolaDialog.bmp': [164, 0, 493, 312], 'LunolaBanner.bmp': [0, 0, 420, 58]})
        self.assertEqual(manifest['recipe']['resize'], 'LANCZOS')
        self.assertEqual(manifest['recipe']['alpha'], 'RGBA alpha-composite on opaque white')
        for name, size in [('LunolaDialog.bmp', [493, 312]), ('LunolaBanner.bmp', [493, 58])]:
            self.assertEqual(manifest['derivatives'][name], {'sha256': digest(self.output / name), 'dimensions': size, 'mode': 'RGB', 'format': 'BMP'})
        self.assertEqual(sorted(p.name for p in self.output.iterdir()), ['LunolaBanner.bmp', 'LunolaDialog.bmp', 'manifest.json'])
        second = self.root / 'second'
        self.generate(output=second)
        self.assertEqual({p.name: digest(p) for p in self.output.iterdir()}, {p.name: digest(p) for p in second.iterdir()})
        self.generate()
        self.assertEqual({p.name: digest(p) for p in self.output.iterdir()}, {p.name: digest(p) for p in second.iterdir()})

    def test_rejects_aliased_output_files_without_source_mutation(self):
        import os
        import shutil
        copied = self.root / 'copied'
        shutil.copytree(APPROVED, copied)
        self.output.mkdir()
        for name in ('LunolaDialog.bmp', 'LunolaBanner.bmp', 'manifest.json'):
            with self.subTest(target=name):
                source = copied / 'lunola-forma-logo.png'
                original = source.read_bytes()
                target = self.output / name
                target.unlink(missing_ok=True)
                os.link(source, target)
                try:
                    result = self.run_generator(approved=copied)
                    self.assertNotEqual(result.returncode, 0, 'Aliased output accepted')
                    self.assertIn('Unsafe output', result.stderr)
                    self.assertEqual(source.read_bytes(), original)
                finally:
                    target.unlink()
                    source.write_bytes(original)

    def test_rejects_font_inside_output_directory(self):
        import shutil
        self.output.mkdir()
        font_copy = self.output / 'font.ttf'
        shutil.copyfile(FONT, font_copy)
        result = subprocess.run(
            [sys.executable, str(GENERATOR), '--approved-assets', str(APPROVED),
             '--font', str(font_copy), '--output', str(self.output)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, 'Font-containing output accepted')
        self.assertIn('Unsafe output', result.stderr)
        self.assertEqual(digest(font_copy), digest(FONT))
        self.assertEqual([p.name for p in self.output.iterdir()], ['font.ttf'])

    def test_native_bitmap_layout_exact_composites_and_byline(self):
        self.generate()
        with Image.open(self.output / 'LunolaDialog.bmp') as image:
            self.assertEqual((image.format, image.size, image.mode), ('BMP', (493, 312), 'RGB'))
            dialog = image.copy()
        with Image.open(self.output / 'LunolaBanner.bmp') as image:
            self.assertEqual((image.format, image.size, image.mode), ('BMP', (493, 58), 'RGB'))
            banner = image.copy()
        expected = Image.new('RGB', (493, 312), 'white')
        expected.paste(self.composite('lunola-forma-logo.png', (144, 48)), (10, 30))
        expected.paste(self.composite('lunola-forma-splash-art.png', (144, 144)), (10, 105))
        ImageDraw.Draw(expected).text((10, 276), 'by Pujo Setyo', font=ImageFont.truetype(str(FONT), 12), fill=(40, 40, 40), anchor='lt')
        self.assertEqual(dialog.tobytes(), expected.tobytes())
        self.assertEqual(dialog.crop((164, 0, 493, 312)).getextrema(), ((255, 255),) * 3)
        expected_banner = Image.new('RGB', (493, 58), 'white')
        expected_banner.paste(self.composite('lunola-forma-icon.png', (54, 54)), (434, 2))
        self.assertEqual(banner.tobytes(), expected_banner.tobytes())
        self.assertEqual(banner.crop((0, 0, 420, 58)).getextrema(), ((255, 255),) * 3)
        text_bounds = ImageDraw.Draw(expected).textbbox((10, 276), 'by Pujo Setyo', font=ImageFont.truetype(str(FONT), 12), anchor='lt')
        self.assertLessEqual(text_bounds[2], 164)
        self.assertLessEqual(text_bounds[3], 312)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approved-assets', type=Path, required=True)
    parser.add_argument('--font', type=Path, required=True)
    args, remaining = parser.parse_known_args()
    APPROVED = args.approved_assets.resolve()
    FONT = args.font.resolve()
    print('Test module:', Path(__file__).resolve(), flush=True)
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
