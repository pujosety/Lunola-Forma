"""Real Phase B asset checks; no Blender runtime or integration claims."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import shutil
from unittest.mock import patch
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest

from PIL import Image, ImageDraw, ImageFont
import generate_assets as gen

ROOT = Path(__file__).resolve().parent
APPROVED_SOURCE = None


def pixels_equal(test: unittest.TestCase, actual: Image.Image, expected: Image.Image) -> None:
    test.assertEqual(actual.mode, expected.mode)
    test.assertEqual(actual.size, expected.size)
    test.assertEqual(actual.tobytes(), expected.tobytes())


def independent_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    if image.mode == "RGBA":
        return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    return image.resize(size, Image.Resampling.LANCZOS)


def read_ico():
    data = (ROOT / "derived/windows/lunola-forma.ico").read_bytes()
    reserved, kind, count = struct.unpack_from("<HHH", data)
    entries = []
    for i in range(count):
        width, height, colors, reserved_entry, planes, depth, length, offset = struct.unpack_from("<BBBBHHII", data, 6 + 16 * i)
        entries.append({"size": (width or 256, height or 256), "colors": colors,
                        "reserved": reserved_entry, "planes": planes, "depth": depth,
                        "length": length, "offset": offset, "payload": data[offset:offset + length]})
    return (reserved, kind, count), entries, data


class Assets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    def test_01_approved_hashes_dimensions_and_modes(self):
        for name, (digest, size, mode) in gen.APPROVED.items():
            with self.subTest(name=name):
                path = ROOT / "originals" / name
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
                with Image.open(path) as image:
                    image.load()
                    self.assertEqual(image.format, "PNG")
                    self.assertEqual(image.size, size)
                    self.assertEqual(image.mode, mode)

    def test_02_original_byte_identity(self):
        if APPROVED_SOURCE is None:
            # The pinned SHA256 checks identity when the external input folder
            # is unavailable, but the executed acceptance run supplies it.
            for name in gen.APPROVED:
                gen.verify_original(ROOT / "originals" / name, name)
        else:
            for name in gen.APPROVED:
                with self.subTest(name=name):
                    self.assertEqual((APPROVED_SOURCE / name).read_bytes(), (ROOT / "originals" / name).read_bytes())

    def test_03_linux_png_dimensions_and_transparency(self):
        for size in (16, 24, 32, 48, 64, 96, 128, 256, 512):
            with self.subTest(size=size), Image.open(ROOT / f"derived/linux/{size}x{size}/lunola-forma.png") as image:
                image.load()
                self.assertEqual(image.format, "PNG")
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.size, (size, size))
                self.assertEqual(image.getchannel("A").getextrema(), (0, 255))
                for xy in [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]:
                    self.assertEqual(image.getpixel(xy)[3], 0)
                self.assertTrue(any(0 < a < 255 for a in image.getchannel("A").tobytes()))

    def test_04_linux_pixels_match_approved_premultiplied_resize(self):
        with Image.open(ROOT / "originals/lunola-forma-icon.png") as icon:
            for size in gen.LINUX_SIZES:
                with self.subTest(size=size), Image.open(ROOT / f"derived/linux/{size}x{size}/lunola-forma.png") as image:
                    pixels_equal(self, image, independent_resize(icon, (size, size)))

    def test_05_ico_directory_sizes_depth_offsets(self):
        header, entries, data = read_ico()
        self.assertEqual(header, (0, 1, 8))
        self.assertEqual([entry["size"] for entry in entries], [(n, n) for n in (16, 24, 32, 48, 64, 96, 128, 256)])
        expected_offset = 6 + 16 * 8
        for entry in entries:
            self.assertEqual(entry["offset"], expected_offset)
            self.assertEqual((entry["colors"], entry["reserved"], entry["planes"], entry["depth"]), (0, 0, 1, 32))
            self.assertGreater(entry["length"], 0)
            self.assertEqual(len(entry["payload"]), entry["length"])
            self.assertTrue(entry["payload"].startswith(b"\x89PNG\r\n\x1a\n"))
            expected_offset += entry["length"]
        self.assertEqual(expected_offset, len(data))

    def test_06_every_ico_frame_decodes_with_identical_rgba_pixels(self):
        _, entries, _ = read_ico()
        for entry in entries:
            size = entry["size"][0]
            with self.subTest(size=size), Image.open(io.BytesIO(entry["payload"])) as image, Image.open(ROOT / f"derived/linux/{size}x{size}/lunola-forma.png") as png:
                image.load()
                pixels_equal(self, image, png)
                self.assertEqual(image.getchannel("A").getextrema(), (0, 255))

    def test_07_ico_reader_exposes_all_eight_frames(self):
        with Image.open(ROOT / "derived/windows/lunola-forma.ico") as ico:
            self.assertEqual(ico.format, "ICO")
            self.assertEqual(ico.ico.sizes(), {(n, n) for n in gen.ICON_SIZES})
            for size in gen.ICON_SIZES:
                with self.subTest(size=size), Image.open(ROOT / f"derived/linux/{size}x{size}/lunola-forma.png") as png:
                    pixels_equal(self, ico.ico.getimage((size, size)), png)

    def test_08_full_color_about_logo_and_alpha(self):
        with Image.open(ROOT / "derived/about/lunola-forma-logo.png") as about, Image.open(ROOT / "originals/lunola-forma-logo.png") as source:
            self.assertEqual(about.size, (1086, 362))
            self.assertEqual(about.mode, "RGBA")
            self.assertEqual(about.getchannel("A").getextrema(), (0, 255))
            pixels_equal(self, about, independent_resize(source, (1086, 362)))

    def test_09_splash_1000x500_and_uncropped_undistorted_art(self):
        with Image.open(ROOT / "derived/splash/lunola-forma-splash.png") as splash, Image.open(ROOT / "originals/lunola-forma-splash-art.png") as source:
            self.assertEqual(splash.size, (1000, 500))
            self.assertEqual(splash.mode, "RGB")
            pixels_equal(self, splash.crop((500, 0, 1000, 500)), independent_resize(source, (500, 500)))
            self.assertEqual(splash.getpixel((0, 0)), (247, 245, 241))
            self.assertEqual(splash.getpixel((499, 499)), (247, 245, 241))

    def test_10_splash_complete_logo_and_only_requested_text(self):
        # Independent reconstruction verifies full artwork, margins, literal
        # attribution/tagline and absence of any additional baked version text.
        expected = Image.new("RGB", (1000, 500), (247, 245, 241))
        with Image.open(ROOT / "originals/lunola-forma-splash-art.png") as art:
            expected.paste(independent_resize(art, (500, 500)), (500, 0))
        with Image.open(ROOT / "originals/lunola-forma-logo.png") as logo:
            resized = independent_resize(logo, (420, 140))
            expected.paste(resized, (40, 125), resized.getchannel("A"))
        draw = ImageDraw.Draw(expected)
        draw.text((40, 294), "Professional 3D Creation Suite", font=ImageFont.load_default(size=23), fill=(39, 43, 54))
        draw.text((40, 407), "Based on Blender", font=ImageFont.load_default(size=18), fill=(39, 43, 54))
        with Image.open(ROOT / "derived/splash/lunola-forma-splash.png") as actual:
            pixels_equal(self, actual, expected)
        self.assertFalse(self.manifest["splash"]["version_baked"])

    def test_11_text_bounds_stay_on_left_panel(self):
        draw = ImageDraw.Draw(Image.new("RGB", (1000, 500)))
        for text, origin, size in [("Professional 3D Creation Suite", (40, 294), 23), ("Based on Blender", (40, 407), 18)]:
            box = draw.textbbox(origin, text, font=ImageFont.load_default(size=size))
            self.assertGreaterEqual(box[0], 0)
            self.assertGreaterEqual(box[1], 265)
            self.assertLessEqual(box[2], 460)
            self.assertLessEqual(box[3], 470)

    def test_12_hidden_rgb_does_not_create_resize_halos(self):
        # Different black/white fully transparent surrounds must produce the
        # same visible pixels when correctly premultiplied before filtering.
        black = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        white = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
        for image in (black, white):
            ImageDraw.Draw(image).rectangle((8, 8, 23, 23), fill=(255, 64, 0, 255))
        first, second = gen.resize(black, (16, 16)), gen.resize(white, (16, 16))
        pixels_equal(self, first, second)
        for background in [(247, 245, 241, 255), (28, 30, 35, 255)]:
            pixels_equal(self, Image.alpha_composite(Image.new("RGBA", first.size, background), first), Image.alpha_composite(Image.new("RGBA", second.size, background), second))

    def test_13_manifest_hashes_file_inventory_dimensions(self):
        outputs = self.manifest["outputs"]
        self.assertEqual(len(outputs), 13)
        self.assertEqual(len({record["path"] for record in outputs}), 13)
        actual_paths = {p.relative_to(ROOT).as_posix() for base in [ROOT / "derived", ROOT / "previews"] for p in base.rglob("*") if p.is_file()}
        # Phase B remains exactly 13 outputs. Only this independently pinned,
        # optional Phase C derivative extends the checkout inventory.
        phase_c_path = "derived/about/lunola_forma_about_light.png"
        expected_paths = {record["path"] for record in outputs}
        if phase_c_path in actual_paths:
            expected_paths.add(phase_c_path)
            path = ROOT / phase_c_path
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             "d89d950392b3d4367a96dc188cb0719bb80c198bf280c211e95abe554f995a93")
            source_path = ROOT / "derived/about/lunola-forma-logo.png"
            self.assertEqual(hashlib.sha256(source_path.read_bytes()).hexdigest(),
                             "31d98ea42646dda99af22962b290bf41e5095bc5fda80b21b3ef534cdbb59abc")
            with Image.open(path) as actual, Image.open(source_path) as source:
                actual.load()
                self.assertEqual(actual.format, "PNG")
                self.assertEqual(actual.size, (1086, 362))
                self.assertEqual(actual.mode, "RGBA")
                self.assertEqual(actual.getchannel("A").getextrema(), (255, 255))
                expected = Image.new("RGBA", source.size, (255, 255, 255, 255))
                expected.alpha_composite(source.convert("RGBA"))
                pixels_equal(self, actual, expected)
        self.assertEqual(actual_paths, expected_paths)
        for record in self.manifest["originals"] + outputs:
            path = ROOT / record["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record["sha256"])
            if "bytes" in record:
                self.assertEqual(path.stat().st_size, record["bytes"])
            if "dimensions" in record:
                with Image.open(path) as image:
                    self.assertEqual(list(image.size), record["dimensions"])
                    self.assertEqual(image.mode, record["mode"])

    def test_14_byte_reproducible_clean_generation(self):
        with tempfile.TemporaryDirectory(prefix=".asset-test-", dir=ROOT) as temp:
            regenerated = gen.generate(Path(temp), ROOT / "originals")
            self.assertEqual(regenerated, self.manifest)
            self.assertEqual((Path(temp) / "manifest.json").read_bytes(), (ROOT / "manifest.json").read_bytes())
            for record in self.manifest["originals"] + self.manifest["outputs"]:
                self.assertEqual((Path(temp) / record["path"]).read_bytes(), (ROOT / record["path"]).read_bytes())

    def test_15_corrupted_original_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory(prefix=".asset-test-", dir=ROOT) as temp:
            base = Path(temp)
            source = base / "source"
            source.mkdir()
            for name in gen.APPROVED:
                (source / name).write_bytes((ROOT / "originals" / name).read_bytes())
            (source / "lunola-forma-icon.png").write_bytes(b"not approved")
            destination = base / "output"
            with self.assertRaisesRegex(ValueError, "Approved hash mismatch"):
                gen.generate(destination, source)
            self.assertFalse(destination.exists())

    def test_16_preview_both_theme_panels(self):
        with Image.open(ROOT / "previews/light-dark.png") as image:
            self.assertEqual(image.size, (1200, 1060))
            self.assertEqual(image.getpixel((1199, 0)), (247, 245, 241))
            self.assertEqual(image.getpixel((1199, 530)), (28, 30, 35))

    @contextmanager
    def isolated_inventory(self, with_phase_c=True):
        # Copies only; never mutate checkout artwork or regenerate Phase B.
        with tempfile.TemporaryDirectory(prefix=".inventory-test-", dir=ROOT) as temp:
            base = Path(temp)
            paths = [r["path"] for r in self.manifest["originals"] + self.manifest["outputs"]]
            if with_phase_c:
                paths.append("derived/about/lunola_forma_about_light.png")
            for relative in paths:
                destination = base / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                source_path = ROOT / relative
                if source_path.is_file():
                    shutil.copyfile(source_path, destination)
                else:
                    # The optional Phase C asset need not exist in a Phase B
                    # checkout. Build this fixture ONLY inside the temp scope.
                    self.assertEqual(relative, "derived/about/lunola_forma_about_light.png")
                    with Image.open(base / "derived/about/lunola-forma-logo.png") as source:
                        fixture = Image.new("RGBA", source.size, (255, 255, 255, 255))
                        fixture.alpha_composite(source.convert("RGBA"))
                        fixture.save(destination)
            with patch(__name__ + ".ROOT", base):
                yield base

    def test_17_known_phase_c_derivative_accepted_in_isolation(self):
        with self.isolated_inventory():
            self.test_13_manifest_hashes_file_inventory_dimensions()

    def test_18_phase_b_inventory_without_optional_phase_c(self):
        with self.isolated_inventory(with_phase_c=False):
            self.test_13_manifest_hashes_file_inventory_dimensions()

    def test_19_unknown_extras_rejected_in_isolation(self):
        for relative in ("derived/about/unknown.png", "previews/unknown.txt"):
            with self.subTest(path=relative), self.isolated_inventory() as base:
                extra = base / relative
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_bytes(b"unexpected extra")
                with self.assertRaisesRegex(AssertionError, "Items in the first set but not the second"):
                    self.test_13_manifest_hashes_file_inventory_dimensions()

    def test_20_modified_known_phase_c_derivative_rejected(self):
        with self.isolated_inventory() as base:
            path = base / "derived/about/lunola_forma_about_light.png"
            # Decodable same-size RGBA PNG with one changed RGB pixel.
            with Image.open(path) as image:
                image.load()
                image.putpixel((0, 0), (254, 255, 255, 255))
                image.save(path)
            with self.assertRaisesRegex(AssertionError, "d89d950392b3d4367a96dc188cb0719bb80c198bf280c211e95abe554f995a93"):
                self.test_13_manifest_hashes_file_inventory_dimensions()


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed = []

    def addSuccess(self, test):
        self.passed.append(test.id())
        super().addSuccess(test)


def main():
    global APPROVED_SOURCE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approved-source", type=Path, help="Compare original bytes against external approved inputs")
    args = parser.parse_args()
    APPROVED_SOURCE = args.approved_source
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(Assets))
    report = {"scope": "Phase B assets only; no application integration or runtime QA", "tests_run": result.testsRun,
              "passed": result.passed, "failures": [{"test": str(t), "traceback": trace} for t, trace in result.failures],
              "errors": [{"test": str(t), "traceback": trace} for t, trace in result.errors],
              "external_original_byte_comparison": APPROVED_SOURCE is not None, "success": result.wasSuccessful()}
    (ROOT / "test-results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Phase B assets: {len(result.passed)}/{result.testsRun} PASS; {len(result.failures)} failures; {len(result.errors)} errors.")
    print("Result: test-results.json (asset-only evidence, not Blender runtime verification).")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
