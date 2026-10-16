#!/usr/bin/env python3
"""Render SVGs with librsvg; contact sheets need Pillow, not the theme itself."""
import argparse
import io
import subprocess
from pathlib import Path
from theme import ROOT, THEME


def render(path, size):
    return subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path)],
                          check=True, capture_output=True).stdout


def contact_sheet(family, theme=THEME):
    from PIL import Image, ImageDraw, ImageFont
    icons = [p for p in sorted((theme / "scalable" / family).glob("*.svg")) if not p.is_symlink()]
    if not icons:
        return
    font_path = subprocess.run(["fc-match", "-f", "%{file}", "sans"], capture_output=True, text=True, check=True).stdout
    try:
        font = ImageFont.truetype(font_path, 12)
        title = ImageFont.truetype(font_path, 24)
    except OSError:
        font = title = ImageFont.load_default()
    columns, cell_w, cell_h = 4, 300, 126
    rows = (len(icons) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w + 32, rows * cell_h + 98), "#101318")
    draw = ImageDraw.Draw(sheet)
    draw.text((24, 18), f"Hikaide-Symbols / {family}", fill="#edf0f6", font=title)
    draw.text((24, 56), "16 / 24 / 32 / 48 / 64 px  ·  SVG artwork on dark and light surfaces", fill="#9ca9ba", font=font)
    for i, path in enumerate(icons):
        x, y = 16 + i % columns * cell_w, 86 + i // columns * cell_h
        draw.rounded_rectangle((x, y, x + 288, y + 116), radius=9, fill="#1c222b")
        draw.rectangle((x + 5, y + 60, x + 280, y + 88), fill="#e7e9ed")
        offset = x + 12
        for size in (16, 24, 32, 48, 64):
            small = theme / f"{size}x{size}" / family / path.name
            raster = Image.open(io.BytesIO(render(small if small.exists() else path, size))).convert("RGBA")
            sheet.paste(raster, (offset, y + 62 - size), raster)
            light = raster.resize((min(size, 24), min(size, 24)), Image.Resampling.LANCZOS)
            sheet.paste(light, (offset, y + 62), light)
            offset += size + 13
        draw.text((x + 10, y + 96), path.stem[:39], fill="#bcc6d5", font=font)
    target = ROOT / "previews" / f"preview-{family}.png"
    target.parent.mkdir(exist_ok=True)
    sheet.save(target)
    print(target.relative_to(ROOT))
    if family == "places":
        states = ["folder", "folder-open", "folder-drag-accept", "folder-documents"]
        preview = Image.new("RGB", (800, 220), "#101318")
        labels = ImageDraw.Draw(preview)
        for column, name in enumerate(states):
            artwork = Image.open(io.BytesIO(render(theme / "scalable/places" / (name + ".svg"), 128))).convert("RGBA")
            preview.paste(artwork, (column * 200 + 36, 25), artwork)
            labels.text((column * 200 + 12, 174), name, fill="#bcc6d5", font=font)
        preview.save(ROOT / "previews/folder-states.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("families", nargs="*", default=["places", "mimetypes", "apps", "devices", "status", "actions", "categories", "emblems"])
    args = parser.parse_args()
    for family in args.families:
        contact_sheet(family)
