"""Phase B only: deterministic derivatives of the three approved originals.
Requires Python >=3.10 and Pillow==12.3.0; never imports Blender modules.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct

import PIL
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PILLOW_VERSION = "12.3.0"
ICON_SIZES = (16, 24, 32, 48, 64, 96, 128, 256)
LINUX_SIZES = ICON_SIZES + (512,)
APPROVED = {
    "lunola-forma-logo.png": ("9e2c53a548d398c536b929ab4dac0fa38702cf75294a2f1c14c847111e5ccdda", (2172, 724), "RGBA"),
    "lunola-forma-icon.png": ("e89ba124051b61175a05dfefb0d24f44c0fa6e7dd6eec23dd8dcb005a95bf111", (1254, 1254), "RGBA"),
    "lunola-forma-splash-art.png": ("18decbf5337fe62c178f32f04769fdd0adea4480cb0dcfc2a3c7ac9e29089bdc", (1254, 1254), "RGB"),
}
TAGLINE = "Professional 3D Creation Suite"
ATTRIBUTION = "Based on Blender"
PANEL_COLOR = (247, 245, 241)
TEXT_COLOR = (39, 43, 54)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_original(path: Path, name: str) -> None:
    digest, dimensions, mode = APPROVED[name]
    if sha256(path) != digest:
        raise ValueError(f"Approved hash mismatch: {path}")
    with Image.open(path) as image:
        image.load()
        if image.size != dimensions or image.mode != mode or image.format != "PNG":
            raise ValueError(f"Approved image format mismatch: {path}")


def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Filter premultiplied channels, then restore straight alpha for PNG/ICO.

    No matte, cropping, color conversion, thresholding or art reconstruction.
    RGBa is Pillow's premultiplied 8-bit RGBA representation. RGB sources
    use the same Lanczos filter directly. All callers preserve aspect ratio.
    """
    if image.mode == "RGBA":
        return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    return image.resize(size, Image.Resampling.LANCZOS)


def png_bytes(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=False, compress_level=9)
    return buffer.getvalue()


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png_bytes(image))


def write_ico(frames: dict[int, Image.Image], path: Path) -> None:
    """Explicit PNG-backed Windows ICO; no implicit frame resampling/dropping."""
    payloads = [(size, png_bytes(frames[size])) for size in ICON_SIZES]
    offset = 6 + 16 * len(payloads)
    directory = bytearray(struct.pack("<HHH", 0, 1, len(payloads)))
    for size, payload in payloads:
        directory.extend(struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0,
                                     1, 32, len(payload), offset))
        offset += len(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(directory) + b"".join(payload for _, payload in payloads))


def splash(logo: Image.Image, art: Image.Image) -> Image.Image:
    canvas = Image.new("RGB", (1000, 500), PANEL_COLOR)
    canvas.paste(resize(art, (500, 500)), (500, 0))
    panel_logo = resize(logo, (420, 140))
    canvas.paste(panel_logo, (40, 125), panel_logo.getchannel("A"))
    draw = ImageDraw.Draw(canvas)
    # Pillow's packaged scalable default font avoids machine font dependencies.
    draw.text((40, 294), TAGLINE, font=ImageFont.load_default(size=23), fill=TEXT_COLOR)
    draw.text((40, 407), ATTRIBUTION, font=ImageFont.load_default(size=18), fill=TEXT_COLOR)
    return canvas


def theme_preview(frames: dict[int, Image.Image], about: Image.Image) -> Image.Image:
    """Native-size icon rows on light/dark backgrounds, plus full-color logo."""
    canvas = Image.new("RGB", (1200, 1060))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)
    for row, (background, foreground, label) in enumerate([
        ((247, 245, 241), (39, 43, 54), "Light"),
        ((28, 30, 35), (235, 235, 235), "Dark"),
    ]):
        y = row * 530
        draw.rectangle((0, y, 1199, y + 529), fill=background)
        draw.text((24, y + 16), f"{label}: native-size icons / unchanged full-color About logo", font=font, fill=foreground)
        x = 24
        for size in ICON_SIZES:
            image = frames[size]
            canvas.paste(image, (x, y + 72 + (256 - size) // 2), image.getchannel("A"))
            draw.text((x, y + 342), str(size), font=font, fill=foreground)
            x += size + 24
        logo = resize(about, (420, 140))
        canvas.paste(logo, (24, y + 378), logo.getchannel("A"))
        enlarged = frames[16].resize((128, 128), Image.Resampling.NEAREST)
        canvas.paste(enlarged, (840, y + 382), enlarged.getchannel("A"))
        draw.text((990, y + 414), "16px, 8x", font=font, fill=foreground)
    return canvas


def generate(output: Path = ROOT, source: Path | None = None) -> dict:
    if PIL.__version__ != PILLOW_VERSION:
        raise RuntimeError(f"Reproducibility requires Pillow=={PILLOW_VERSION}; got {PIL.__version__}")
    output = output.resolve()
    # The implementation owns this directory only, including test temporary dirs.
    if output != ROOT and ROOT not in output.parents:
        raise ValueError("Output must be within release/datafiles/lunola")
    original_dir = output / "originals"
    origin = source.resolve() if source else original_dir
    # Verify all inputs before any writes; never overwrite an existing original.
    for name in APPROVED:
        verify_original(origin / name, name)
        target = original_dir / name
        if target.exists():
            verify_original(target, name)
    original_dir.mkdir(parents=True, exist_ok=True)
    for name in APPROVED:
        target = original_dir / name
        if not target.exists():
            shutil.copyfile(origin / name, target)
        verify_original(target, name)
    with Image.open(original_dir / "lunola-forma-icon.png") as image:
        icon = image.copy()
    with Image.open(original_dir / "lunola-forma-logo.png") as image:
        logo = image.copy()
    with Image.open(original_dir / "lunola-forma-splash-art.png") as image:
        art = image.copy()
    paths = []
    frames = {size: resize(icon, (size, size)) for size in LINUX_SIZES}
    for size, image in frames.items():
        path = output / f"derived/linux/{size}x{size}/lunola-forma.png"
        save_png(image, path)
        paths.append(path)
    ico_path = output / "derived/windows/lunola-forma.ico"
    write_ico(frames, ico_path)
    paths.append(ico_path)
    about = resize(logo, (1086, 362))
    for image, relative in [
        (about, "derived/about/lunola-forma-logo.png"),
        (splash(logo, art), "derived/splash/lunola-forma-splash.png"),
        (theme_preview(frames, about), "previews/light-dark.png"),
    ]:
        path = output / relative
        save_png(image, path)
        paths.append(path)
    records = []
    for path in sorted(paths):
        record = {"path": path.relative_to(output).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
        if path.suffix == ".png":
            with Image.open(path) as image:
                record.update(dimensions=list(image.size), mode=image.mode)
        else:
            record.update(format="ICO", frame_sizes=list(ICON_SIZES), encoding="PNG/RGBA", bit_depth=32)
        records.append(record)
    manifest = {
        "schema": 1, "phase": "B - preparation only, not integrated",
        "generator": "generate_assets.py", "pillow": PILLOW_VERSION,
        "resize": "Lanczos; RGBA -> premultiplied RGBa -> resize -> straight RGBA",
        "originals": [{"path": f"originals/{name}", "sha256": info[0], "dimensions": list(info[1]), "mode": info[2]} for name, info in APPROVED.items()],
        "outputs": records,
        "splash": {"dimensions": [1000, 500], "left_panel": [0, 0, 500, 500],
                   "panel_rgb": list(PANEL_COLOR), "art_rect": [500, 0, 1000, 500],
                   "logo_rect": [40, 125, 460, 265], "tagline": TAGLINE,
                   "tagline_origin": [40, 294], "tagline_size": 23,
                   "attribution": ATTRIBUTION, "attribution_origin": [40, 407], "attribution_size": 18,
                   "text_rgb": list(TEXT_COLOR), "font": "Pillow packaged default scalable font",
                   "version_baked": False, "runtime_overlay": "Deferred to integration; upstream runtime supplies actual version"},
        "rights": "Brand asset rights unspecified; no license grant inferred. Preserve upstream notices during later integration.",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Approved original directory for first-run byte copies")
    args = parser.parse_args()
    manifest = generate(source=args.source)
    print(f"Generated {len(manifest['outputs'])} outputs; verified {len(APPROVED)} approved original hashes.")
    print(f"Windows ICO frames: {', '.join(map(str, ICON_SIZES))}")
    print("Splash: 1000x500; artwork 500x500; full logo 420x140; no baked version.")


if __name__ == "__main__":
    main()
