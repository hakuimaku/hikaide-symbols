#!/usr/bin/env python3
"""Stage, install and remove the managed appearance pair with rollback."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from theme import THEME, NAME, VARIANTS, marker
from validate import validate

# Recognize v1 only for migration of the legacy dark theme.
LEGACY_MARKER = "Hikaide-Symbols managed theme v1\n"


def owned(target):
    """Check exact managed metadata and reject symlinked destinations."""
    metadata = target / ".hikaide-symbols.json"
    mode = next((mode for mode, name in VARIANTS.items() if name == target.name), None)
    if target.is_symlink() or not target.is_dir() or mode is None or metadata.is_symlink():
        return False
    if metadata.is_file():
        try:
            return json.loads(metadata.read_text()) == json.loads(marker(mode))
        except (ValueError, TypeError):
            return False
    metadata = target / ".hikaide-symbols"
    return (mode == "dark" and not metadata.is_symlink() and metadata.is_file()
            and metadata.read_text() == LEGACY_MARKER)


def check_targets(root, replace):
    """Refuse unsafe targets before any member of the pair changes."""
    for name in VARIANTS.values():
        target = Path(root) / name
        if target.exists() or target.is_symlink():
            if not owned(target):
                raise ValueError(f"Refusing to overwrite an unmanaged theme: {target}")
            if not replace:
                raise ValueError("Theme already installed. Use --replace to replace this theme's files.")


def replace_pair(staged, root):
    """Commit both staged trees, or remove both when staged is None."""
    root = Path(root)
    previous = Path(tempfile.mkdtemp(prefix=".hikaide-previous-", dir=root))
    committed = []
    try:
        for name in VARIANTS.values():
            target = root / name
            if target.exists():
                target.rename(previous / name)
        if staged is not None:
            for name in VARIANTS.values():
                target = root / name
                (staged / name).rename(target)
                committed.append(target)
    except OSError:
        # Keep backups outside temporary staging if rollback itself fails.
        try:
            for target in reversed(committed):
                shutil.rmtree(target)
            for backup in previous.iterdir():
                backup.rename(root / backup.name)
        except OSError as error:
            raise OSError(f"Rollback failed; recover previous themes from {previous}: {error}") from error
        previous.rmdir()
        raise
    shutil.rmtree(previous)


def install(icons_dir, replace=False):
    """Validate and cache both staged appearances before replacing the pair."""
    icons_dir = Path(icons_dir).expanduser().resolve()
    for name in VARIANTS.values():
        source = THEME.parent / name
        if source.is_symlink():
            raise ValueError(f"Refusing symlinked build output: {source}")
        validate(source)
        target = icons_dir / name
        if target == source or target in source.parents or source in target.parents:
            raise ValueError("Installation destination must be outside build output")
    check_targets(icons_dir, replace)
    icons_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".hikaide-install-", dir=icons_dir) as work:
        for name in VARIANTS.values():
            staged = Path(work) / name
            shutil.copytree(THEME.parent / name, staged, symlinks=True)
            cache = shutil.which("gtk4-update-icon-cache") or shutil.which("gtk-update-icon-cache")
            if cache:
                subprocess.run([cache, "--force", "--ignore-theme-index", str(staged)], check=True)
            validate(staged)
        replace_pair(Path(work), icons_dir)
    print(f"Installed appearance pair in {icons_dir}")
    return icons_dir / NAME


def uninstall(icons_dir):
    """Remove only a fully recognized pair, restoring it on rename failure."""
    root = Path(icons_dir).expanduser().resolve()
    check_targets(root, replace=True)
    if root.exists():
        replace_pair(None, root)
    print(f"Removed managed appearance pair from {root}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "uninstall"])
    roots = parser.add_mutually_exclusive_group()
    roots.add_argument("--icons-dir", type=Path)
    roots.add_argument("--xdg", action="store_true", help="Use $XDG_DATA_HOME/icons")
    parser.add_argument("--replace", action="store_true", help="Replace the existing managed appearance pair")
    args = parser.parse_args()
    root = args.icons_dir or ((Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share"))) / "icons") if args.xdg else Path.home() / ".icons")
    try:
        install(root, args.replace) if args.action == "install" else uninstall(root)
    except (ValueError, AssertionError, OSError, subprocess.CalledProcessError) as e:
        parser.exit(1, f"{e}\n")
