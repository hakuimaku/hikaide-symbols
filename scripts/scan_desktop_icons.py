#!/usr/bin/env python3
"""Read real launcher Icon= values without executing desktop files."""
import argparse
import configparser
import json
import os
from pathlib import Path
from theme import ROOT, THEME


def desktop_dirs():
    return [Path.home() / ".local/share/applications", Path.home() / ".local/share/flatpak/exports/share/applications",
            Path("/usr/local/share/applications"), Path("/usr/share/applications"),
            Path("/var/lib/flatpak/exports/share/applications")]


def scan(paths=None, theme=THEME):
    available = {p.stem for p in (theme / "scalable").glob("*/*.svg")}
    rows, seen = [], set()
    for directory in desktop_dirs() if paths is None else paths:
        for desktop in sorted(Path(directory).glob("*.desktop")):
            if desktop.name in seen:
                continue
            seen.add(desktop.name)
            ini = configparser.ConfigParser(interpolation=None, strict=False)
            try:
                ini.read(desktop, encoding="utf-8")
                entry = ini["Desktop Entry"]
                icon = entry.get("Icon", "")
                desktop_envs = set(os.environ.get("XDG_CURRENT_DESKTOP", "").split(":"))
                only = set(filter(None, entry.get("OnlyShowIn", "").split(";")))
                excluded = set(filter(None, entry.get("NotShowIn", "").split(";")))
                visible = not any(entry.get(k, "false").lower() == "true" for k in ("Hidden", "NoDisplay"))
                visible &= (not only or bool(only & desktop_envs)) and not bool(excluded & desktop_envs)
                rows.append({"desktop_file": str(desktop), "name": entry.get("Name", desktop.stem),
                             "icon": icon, "flatpak_id": entry.get("X-Flatpak", ""), "visible": visible,
                             "covered": not Path(icon).is_absolute() and icon.removesuffix(".svg").removesuffix(".png") in available,
                             "absolute_icon": Path(icon).is_absolute()})
            except (configparser.Error, KeyError, UnicodeError) as e:
                rows.append({"desktop_file": str(desktop), "error": str(e), "covered": False, "visible": False})
    return sorted(rows, key=lambda r: (not r["visible"], r["covered"], r.get("name", "").casefold()))


def write_reports(rows):
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "desktop-icons.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    missing = [r for r in rows if not r["covered"]]
    lines = ["Local application icon coverage (visible missing launchers first)",
             "Absolute Icon= paths bypass theme lookup; no desktop files were modified.",
             "Frequency data unavailable; within visibility groups sorted by application name.", ""]
    for row in missing:
        lines.append(f"{'VISIBLE' if row['visible'] else 'hidden ':7} | {row.get('name', '?')} | Icon={row.get('icon', '?')} | "
                     f"Flatpak={row.get('flatpak_id') or '-'} | {row['desktop_file']}" +
                     (" | absolute path: theme cannot override" if row.get("absolute_icon") else ""))
    (reports / "uncovered-app-icons.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", type=Path, default=THEME)
    args = parser.parse_args()
    rows = scan(theme=args.theme)
    write_reports(rows)
    print(f"Scanned {len(rows)} launchers: {sum(r['covered'] for r in rows)} covered; see reports/")
