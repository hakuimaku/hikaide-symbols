"""Read desktop accent settings and delegate mutations to icon-accent."""
import argparse
import configparser
import os
import re
import shutil
import subprocess
from pathlib import Path
from theme import NAME

# libadwaita's standalone accent RGB colors; desktop names select the same ACCENT role.
GNOME = dict(zip("blue teal green yellow orange red pink purple slate".split(),
                 "#3584E4 #2190A4 #3A944A #C88800 #ED5B00 #E62D42 #D56199 #9141AC #6F8396".split()))


def normalize(value):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise ValueError("Accent must be #RRGGBB")
    return value.upper()


def kde_color(value):
    if value.startswith("#"):
        return normalize(value)
    channels = [int(c) for c in value.split(",")]
    if len(channels) not in {3, 4} or any(not 0 <= c <= 255 for c in channels):
        raise ValueError("Invalid KDE RGB accent")
    return "#" + "".join(f"{c:02X}" for c in channels[:3])


def detect(color=None):
    if color is not None:
        return normalize(color)
    session = os.environ.get("XDG_CURRENT_DESKTOP", "").lower().split(":")
    if any(s in {"kde", "plasma"} for s in session):
        config = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "kdeglobals"
        ini = configparser.ConfigParser(interpolation=None)
        ini.read(config)
        value = ini.get("General", "AccentColor", fallback="") or ini.get("Colors:Selection", "BackgroundNormal", fallback="")
        if value:
            return kde_color(value)
    elif any("gnome" in s for s in session):
        result = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "accent-color"],
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            name = result.stdout.strip().strip("'")
            if name in GNOME:
                return GNOME[name]
    raise ValueError("No desktop accent available; pass --color '#RRGGBB' (required on standalone WMs)")


def sync(color, icons_dir=None):
    command = shutil.which("icon-accent")
    if not command:
        raise ValueError("Install https://github.com/hakuimaku/icon-accent and add icon-accent to PATH")
    args = [command]
    if icons_dir is not None:
        args += ["--icons-dir", str(Path(icons_dir).expanduser())]
    subprocess.run(args + ["set", normalize(color), "--theme", NAME], check=True)


def main(action):
    parser = argparse.ArgumentParser(description="One logical accent; static mutations handled by icon-accent")
    parser.add_argument("--color")
    if action == "sync":
        parser.add_argument("--icons-dir", type=Path)
    args = parser.parse_args()
    try:
        color = detect(args.color)
        if action == "detect":
            print(color)
        else:
            sync(color, args.icons_dir)
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        parser.exit(1, f"{e}\n")
