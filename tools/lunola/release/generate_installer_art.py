# SPDX-License-Identifier: GPL-2.0-or-later
"""Generate resized white-background integrations of approved Lunola artwork."""
import argparse
import hashlib
import json
from pathlib import Path

APPROVED_HASHES = {
    'lunola-forma-logo.png': '9e2c53a548d398c536b929ab4dac0fa38702cf75294a2f1c14c847111e5ccdda',
    'lunola-forma-icon.png': 'e89ba124051b61175a05dfefb0d24f44c0fa6e7dd6eec23dd8dcb005a95bf111',
    'lunola-forma-splash-art.png': '18decbf5337fe62c178f32f04769fdd0adea4480cb0dcfc2a3c7ac9e29089bdc',
}

from PIL import Image, ImageDraw, ImageFont


def generate(approved, font_path, output):
    approved, font_path, output = approved.resolve(), font_path.resolve(), output.resolve()
    if output == approved or output.is_relative_to(approved) or approved.is_relative_to(output):
        raise ValueError('Unsafe output: approved source directory overlap')
    if font_path == output or font_path.is_relative_to(output):
        raise ValueError('Unsafe output: font source overlap')
    for name in ('LunolaDialog.bmp', 'LunolaBanner.bmp', 'manifest.json'):
        target = output / name
        if target.is_symlink() or (target.exists() and (not target.is_file() or target.stat().st_nlink != 1)):
            raise ValueError(f'Unsafe output: linked or nonregular target {name}')
    for name, expected in APPROVED_HASHES.items():
        if hashlib.sha256((approved / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Unapproved asset hash: {name}')
    font = ImageFont.truetype(str(font_path), 12)
    dialog = Image.new('RGB', (493, 312), 'white')
    banner = Image.new('RGB', (493, 58), 'white')
    for canvas, name, size, position in (
        (dialog, 'lunola-forma-logo.png', (144, 48), (10, 30)),
        (dialog, 'lunola-forma-splash-art.png', (144, 144), (10, 105)),
        (banner, 'lunola-forma-icon.png', (54, 54), (434, 2)),
    ):
        with Image.open(approved / name) as source:
            resized = source.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
        composite = Image.alpha_composite(Image.new('RGBA', size, 'white'), resized).convert('RGB')
        canvas.paste(composite, position)
    draw = ImageDraw.Draw(dialog)
    bounds = draw.textbbox((10, 276), 'by Pujo Setyo', font=font, anchor='lt')
    if bounds[2] > 164 or bounds[3] > 312:
        raise ValueError('Byline does not fit the sidebar with this font')
    draw.text((10, 276), 'by Pujo Setyo', font=font, fill=(40, 40, 40), anchor='lt')
    output.mkdir(parents=True, exist_ok=True)
    dialog.save(output / 'LunolaDialog.bmp', format='BMP')
    banner.save(output / 'LunolaBanner.bmp', format='BMP')
    originals = {}
    for name, expected in APPROVED_HASHES.items():
        with Image.open(approved / name) as source:
            originals[name] = {'sha256': expected, 'dimensions': list(source.size), 'mode': source.mode}
    manifest = {
        'schema_version': 1,
        'originals': originals,
        'font': {'source': font_path.as_posix(), 'sha256': hashlib.sha256(font_path.read_bytes()).hexdigest(), 'size_px': 12},
        'placements': {
            'logo': {'source': 'lunola-forma-logo.png', 'bitmap': 'LunolaDialog.bmp', 'xy': [10, 30], 'dimensions': [144, 48]},
            'splash': {'source': 'lunola-forma-splash-art.png', 'bitmap': 'LunolaDialog.bmp', 'xy': [10, 105], 'dimensions': [144, 144]},
            'icon': {'source': 'lunola-forma-icon.png', 'bitmap': 'LunolaBanner.bmp', 'xy': [434, 2], 'dimensions': [54, 54]},
        },
        'byline': {'text': 'by Pujo Setyo', 'xy': [10, 276], 'color_rgb': [40, 40, 40], 'anchor': 'lt', 'bounds': list(bounds)},
        'native_text_zones': {'LunolaDialog.bmp': [164, 0, 493, 312], 'LunolaBanner.bmp': [0, 0, 420, 58]},
        'recipe': {'resize': 'LANCZOS', 'alpha': 'RGBA alpha-composite on opaque white'},
        'derivatives': {},
    }
    for name, image in (('LunolaDialog.bmp', dialog), ('LunolaBanner.bmp', banner)):
        manifest['derivatives'][name] = {'sha256': hashlib.sha256((output / name).read_bytes()).hexdigest(), 'dimensions': list(image.size), 'mode': 'RGB', 'format': 'BMP'}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approved-assets', required=True, type=Path)
    parser.add_argument('--font', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    generate(args.approved_assets.resolve(), args.font.resolve(), args.output.resolve())
    print('Generated 2 installer bitmap derivatives.')


if __name__ == '__main__':
    main()
