"""Shared paths, appearance palettes and runtime accent defaults."""
import json
import re
from pathlib import Path

# Legacy names remain the dark appearance for existing consumers.
ROOT = Path(__file__).resolve().parents[1]
NAME = "Hikaide-Symbols"
THEME = ROOT / "dist" / NAME
VARIANTS = {"dark": NAME, "light": NAME + "-Light"}
CONTEXTS = {"apps": "Applications", "places": "Places", "mimetypes": "MimeTypes",
            "devices": "Devices", "status": "Status", "actions": "Actions",
            "categories": "Categories", "emblems": "Emblems"}
# Every neutral source token must have a value in both palettes.
ROLES = set("folderBack folderFront folderCorner folderOpenInterior folderOpenFront paper paperShade paperSmall paperFold paperFoldHighlight paperSmallFold fileGlyph statusSurface statusGlyph actionGlyph deviceHighlight deviceShade emblemSurface emblemBorder emblemGlyph warning error".split())


def palette():
    """Validate the complete palette before generating either theme."""
    data = json.loads((ROOT / "src/theme/palette.json").read_text())
    if not isinstance(data, dict) or set(data) != {"accent", *VARIANTS} or not isinstance(data["accent"], dict) or set(data["accent"]) != set(VARIANTS):
        raise ValueError("palette.json must contain dark/light palettes and accents")
    for mode in VARIANTS:
        if not isinstance(data[mode], dict) or set(data[mode]) != ROLES:
            raise ValueError(f"Incomplete {mode} neutral palette")
    for group in data.values():
        for value in group.values():
            if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
                raise ValueError("Palette colors must be #RRGGBB")
    return data


def accent(mode="dark"):
    """Return the default accent for one appearance."""
    return palette()["accent"][mode].upper()


def tokens(data, mode):
    """Map semantic authoring roles to resolved SVG paint colors."""
    result = {"@ACCENT@": data["accent"][mode].upper()}
    for role, value in data[mode].items():
        name = re.sub(r"([a-z])([A-Z])", r"\1_\2", role).upper()
        result[f"@{name}@"] = value.upper()
    return result


def marker(mode):
    """Identify managed v2 artwork and its appearance without storing the accent."""
    return json.dumps({"family": NAME, "version": 2, "variant": mode}, indent=2) + "\n"


def icon_name(name):
    """Reject icon names that could escape their output directory."""
    if not re.fullmatch(r"[A-Za-z0-9_+.-]+", name) or name in {".", ".."}:
        raise ValueError(f"Unsafe icon name: {name!r}")
    return name
