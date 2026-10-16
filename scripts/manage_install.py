#!/usr/bin/env python3
"""Non-root, staged installation with explicit replacement and ownership checks."""
import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from theme import THEME, NAME
from validate import validate

MARKER = "Hikaide-Symbols managed theme v1\n"


def owned(target):
    marker = target / ".hikaide-symbols"
    return not target.is_symlink() and marker.is_file() and not marker.is_symlink() and marker.read_text() == MARKER


def install(icons_dir, replace=False):
    validate()
    icons_dir = Path(icons_dir).expanduser().absolute()
    target = icons_dir / NAME
    if target.exists() or target.is_symlink():
        if not owned(target):
            raise ValueError(f"Refusing to overwrite an unmanaged theme: {target}")
        if not replace:
            raise ValueError("Theme already installed. Use --replace to replace this theme's files.")
    icons_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".hikaide-install-", dir=icons_dir) as work:
        staged = Path(work) / NAME
        shutil.copytree(THEME, staged, symlinks=True)
        cache = shutil.which("gtk4-update-icon-cache") or shutil.which("gtk-update-icon-cache")
        if cache:
            subprocess.run([cache, "--force", "--ignore-theme-index", str(staged)], check=True)
        previous = Path(work) / "previous"
        if target.exists():
            target.rename(previous)
        try:
            staged.rename(target)
        except OSError:
            if previous.exists():
                previous.rename(target)
            raise
    print(f"Installed {target}")
    return target


def uninstall(icons_dir):
    target = Path(icons_dir).expanduser().absolute() / NAME
    if not target.exists() and not target.is_symlink():
        print(f"Already absent: {target}")
        return
    if not owned(target):
        raise ValueError(f"Refusing to remove an unmanaged theme: {target}")
    shutil.rmtree(target)
    print(f"Removed {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "uninstall"])
    roots = parser.add_mutually_exclusive_group()
    roots.add_argument("--icons-dir", type=Path)
    roots.add_argument("--xdg", action="store_true", help="Use $XDG_DATA_HOME/icons")
    parser.add_argument("--replace", action="store_true", help="Replace an existing managed Hikaide-Symbols")
    args = parser.parse_args()
    root = args.icons_dir or ((Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share"))) / "icons") if args.xdg else Path.home() / ".icons")
    try:
        install(root, args.replace) if args.action == "install" else uninstall(root)
    except (ValueError, AssertionError, OSError, subprocess.CalledProcessError) as e:
        parser.exit(1, f"{e}\n")
