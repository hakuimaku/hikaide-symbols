"""Shared paths and the single source accent; no runtime dependencies."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "Hikaide-Symbols"
THEME = ROOT / "dist" / NAME
CONTEXTS = {"apps": "Applications", "mimetypes": "MimeTypes", "places": "Places",
            "devices": "Devices", "status": "Status", "actions": "Actions",
            "categories": "Categories", "emblems": "Emblems"}


def accent():
    data = json.loads((ROOT / "src/theme/accent.json").read_text())
    if set(data) != {"accent"} or not re.fullmatch(r"#[0-9A-Fa-f]{6}", data["accent"]):
        raise ValueError("accent.json must contain exactly one #RRGGBB accent")
    return data["accent"].upper()


def icon_name(name):
    if not re.fullmatch(r"[A-Za-z0-9_+.-]+", name) or name in {".", ".."}:
        raise ValueError(f"Unsafe icon name: {name!r}")
    return name
