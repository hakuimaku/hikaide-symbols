#!/usr/bin/env python3
"""Alias manifests use JSON, a YAML 1.2 subset, to avoid a YAML dependency."""
import json
from pathlib import Path
from theme import ROOT, THEME, icon_name


def make_aliases(theme=THEME):
    count = 0
    for manifest in sorted((ROOT / "src/aliases").glob("*.yaml")):
        data = json.loads(manifest.read_text())
        for directory, families in data.items():
            folder = theme / directory
            if folder.resolve().parent.parent != theme.resolve():
                raise ValueError(f"Unsafe alias directory: {directory}")
            for canonical, names in families.items():
                target = folder / (icon_name(canonical) + ".svg")
                if not target.is_file() or target.is_symlink():
                    raise ValueError(f"Alias must target canonical artwork: {target}")
                for name in names:
                    alias = folder / (icon_name(name) + ".svg")
                    if alias.exists() or alias.is_symlink():
                        raise ValueError(f"Icon name collision: {alias}")
                    alias.symlink_to(target.name)
                    count += 1
    return count


if __name__ == "__main__":
    print(f"Created {make_aliases()} aliases")
