#!/usr/bin/env python3
"""Fail on packaging, SVG, alias and single-accent contract violations."""
import argparse
import configparser
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from theme import ROOT, THEME, NAME, CONTEXTS


def validate(theme=THEME, require_report=True):
    theme = Path(theme).resolve()
    ini = configparser.ConfigParser(interpolation=None)
    ini.read(theme / "index.theme")
    info = ini["Icon Theme"]
    assert info["Name"] == NAME and info["Comment"]
    assert info["Inherits"].split(",")[-1] == "hicolor", "hicolor fallback required"
    dirs = info["Directories"].split(",")
    assert len(dirs) == len(set(dirs)), "Duplicate directory"
    assert set(ini.sections()) == {"Icon Theme", *dirs}, "Undeclared index sections"
    all_colors = set()
    count = 0
    names = {}
    for directory in dirs:
        folder = theme / directory
        assert folder.is_dir() and folder.resolve().is_relative_to(theme), directory
        meta = ini[directory]
        assert meta["Context"] == CONTEXTS[folder.name]
        assert int(meta["Size"]) > 0
        assert meta["Type"] in {"Fixed", "Scalable"}
        if meta["Type"] == "Scalable":
            assert 0 < int(meta["MinSize"]) <= int(meta["Size"]) <= int(meta["MaxSize"])
        for svg in sorted(folder.glob("*.svg")):
            assert svg.is_file(), f"Broken alias: {svg}"
            assert svg.resolve().is_relative_to(theme), f"Escaping alias: {svg}"
            if svg.is_symlink():
                assert not Path(svg.readlink()).is_absolute(), "Absolute symlink"
            text = svg.read_text()
            assert "<!DOCTYPE" not in text and "<!ENTITY" not in text, f"XML entities forbidden: {svg}"
            assert not re.search(r"@[A-Z_]+@|\{\{", text), f"Unresolved token: {svg}"
            root = ET.fromstring(text)
            assert root.tag == "{http://www.w3.org/2000/svg}svg", svg
            view = list(map(float, root.attrib["viewBox"].split()))
            assert len(view) == 4 and view[2] > 0 and view[3] > 0, svg
            for dimension in ("width", "height"):
                assert float(root.attrib[dimension].removesuffix("px")) > 0, svg
            ids = [el.get("id") for el in root.iter() if el.get("id")]
            assert len(ids) == len(set(ids)), f"Duplicate SVG IDs: {svg}"
            for el in root.iter():
                tag = el.tag.rsplit("}", 1)[-1]
                assert tag not in {"image", "script", "foreignObject", "filter"}, f"Unsafe/expensive SVG: {svg}"
                for key, value in el.attrib.items():
                    assert not key.lower().startswith("on"), svg
                    if key.endswith("href"):
                        assert value.startswith("#"), f"External reference: {svg}"
                    for reference in re.findall(r"url\(\s*([^)]*)\)", value):
                        reference = reference.strip(" '\"")
                        assert reference.startswith("#") and reference[1:] in ids, f"Invalid paint reference: {svg}"
                    assert not re.search(r"(?:file:|data:|https?:|/home/|/tmp/)", value), svg
            styles = "\n".join(el.text or "" for el in root.iter() if el.tag.endswith("}style"))
            assert "@import" not in styles and not re.search(r"url\(\s*['\"]?(?!#)", styles), f"External stylesheet reference: {svg}"
            assert not re.search(r"ColorScheme-(?!Highlight\b)", text), f"Unexpected editable palette role: {svg}"
            colors = re.findall(r"\.ColorScheme-Highlight\s*\{\s*color:\s*(#[0-9a-fA-F]{6})\s*;\s*\}", styles)
            if "ColorScheme-Highlight" in text:
                assert len(colors) == 1, f"Multiple/invalid accent declarations: {svg}"
                all_colors.update(c.upper() for c in colors)
                for el in root.iter():
                    if "ColorScheme-Highlight" in el.get("class", "").split():
                        assert el.get("fill") == "currentColor" or el.get("stroke") == "currentColor", svg
            if svg.stem.endswith("-symbolic"):
                assert not colors and not re.search(r"<(?:linearGradient|radialGradient)", text), svg
                assert view == [0, 0, 16, 16], svg
            # Context is not a lookup namespace: repeated names must share artwork.
            variant = directory.split("/")[0]
            key = variant, svg.name
            assert key not in names or names[key] == text, f"Ambiguous icon name: {svg.name}"
            names[key] = text
            count += 1
    assert len(all_colors) == 1, f"Expected one editable accent: {all_colors}"
    for file in theme.rglob("*"):
        if file.suffix == ".svg":
            assert file.parent.relative_to(theme).as_posix() in dirs, f"Undeclared SVG directory: {file}"
        if file.suffix == ".png":
            from PIL import Image
            size = int(file.parent.parent.name.split("x")[0])
            with Image.open(file) as img:
                assert img.size == (size, size), file
    if require_report:
        assert (ROOT / "reports/uncovered-app-icons.txt").is_file(), "Run application scanner"
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("theme", nargs="?", type=Path, default=THEME)
    args = parser.parse_args()
    print(f"Validated {validate(args.theme)} SVG names; index, aliases, XML and accent contract OK")
