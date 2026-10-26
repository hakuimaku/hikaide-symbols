#!/usr/bin/env python3
"""Render SVGs with librsvg; contact sheets need Pillow, not the theme itself."""
import argparse
import io
import subprocess
from pathlib import Path
from theme import ROOT, THEME, VARIANTS


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


def appearance_sheets():
    """Render target and cross-background diagnostics at common lookup sizes."""
    from PIL import Image, ImageDraw, ImageFont, ImageChops
    samples = {
        "places": ["folder", "folder-open", "folder-documents", "user-trash-full"],
        "mimetypes": ["text-x-generic", "application-pdf", "text-x-python", "application-zip"],
        "devices": ["computer", "drive-harddisk", "camera-photo", "printer"],
        "status": ["dialog-information", "dialog-warning", "dialog-error", "network-wireless-signal-excellent"],
        "actions": ["edit-copy", "document-save", "edit-delete", "system-search"],
    }
    font_path = subprocess.check_output(["fc-match", "-f", "%{file}", "sans"], text=True)
    font = ImageFont.truetype(font_path, 13)
    target = ROOT / "previews"
    target.mkdir(exist_ok=True)
    for mode, name in VARIANTS.items():
        for background in VARIANTS:
            color = "#101010" if background == "dark" else "#f7f7f7"
            foreground = "#d8d8d8" if background == "dark" else "#1b1b1b"
            sheet = Image.new("RGB", (1120, 720), color)
            draw = ImageDraw.Draw(sheet)
            draw.text((18, 16), f"{name} on {background} / 16, 24, 48, 64 px", fill=foreground, font=font)
            for row, (family, icons) in enumerate(samples.items()):
                for column, icon in enumerate(icons):
                    x, y = column * 280 + 16, row * 132 + 50
                    draw.text((x, y), icon, fill=foreground, font=font)
                    offset = x
                    for size in (16, 24, 48, 64):
                        theme = THEME.parent / name
                        small = theme / f"{size}x{size}" / family / f"{icon}.svg"
                        source = small if small.exists() else theme / "scalable" / family / f"{icon}.svg"
                        image = Image.open(io.BytesIO(render(source, size))).convert("RGBA")
                        assert image.getbbox(), f"Empty preview: {source}"
                        tile = Image.new("RGB", image.size, color)
                        tile.paste(image, mask=image.getchannel("A"))
                        difference = ImageChops.difference(tile, Image.new("RGB", image.size, color))
                        assert max(channel[1] for channel in difference.getextrema()) > 25, source
                        sheet.paste(tile, (offset, y + 25 + (64 - size) // 2))
                        offset += size + 12
            suffix = "" if mode == background else "-sanity"
            output = target / f"preview-{mode}-on-{background}{suffix}.png"
            sheet.save(output)
            print(output.relative_to(ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("families", nargs="*", default=["places", "mimetypes", "devices", "status", "actions", "categories", "emblems"])
    parser.add_argument("--appearances", action="store_true", help="render both target and cross-background sheets")
    args = parser.parse_args()
    if args.appearances:
        appearance_sheets()
    else:
        for family in args.families:
            contact_sheet(family)
