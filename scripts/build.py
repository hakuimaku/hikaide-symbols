#!/usr/bin/env python3
"""Compile editable SVG sources into a deterministic, relocatable GTK theme."""
import shutil
import tempfile
from pathlib import Path
from theme import ROOT, THEME, NAME, CONTEXTS, VARIANTS, palette, tokens, marker
from make_aliases import make_aliases


def build_variant(output, mode, data):
    """Compile one appearance from the shared source SVGs and alias manifests."""
    output.mkdir()
    directories = []
    sections = []
    for family in CONTEXTS:
        for variant in ("scalable", "symbolic", "16x16", "24x24"):
            source = ROOT / "src" / family if variant == "scalable" else ROOT / "src" / variant / family
            files = sorted(source.glob("*.svg"))
            if not files:
                continue
            directory = f"{variant}/{family}"
            directories.append(directory)
            (output / directory).mkdir(parents=True)
            for svg in files:
                if svg.is_symlink():
                    raise ValueError(f"Source artwork must not be symlinked: {svg}")
                text = svg.read_text()
                for token, value in tokens(data, mode).items():
                    text = text.replace(token, value)
                (output / directory / svg.name).write_text(text)
            size = 16 if variant == "symbolic" else int(variant.split("x")[0]) if "x" in variant else 64
            kind = "Fixed" if "x" in variant else "Scalable"
            sections.append(f"[{directory}]\nSize={size}\nContext={CONTEXTS[family]}\nType={kind}\n" +
                            ("MinSize=8\nMaxSize=512\n" if kind == "Scalable" else ""))
    header = (ROOT / "index.theme.in").read_text().replace("@DIRECTORIES@", ",".join(directories))
    (output / "index.theme").write_text(header.replace(NAME, VARIANTS[mode]) + "\n" + "\n".join(sections))
    (output / ".hikaide-symbols.json").write_text(marker(mode))
    for name in ("LICENSE", "LICENSES"):
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, output / name)
        elif source.is_file():
            shutil.copy2(source, output / name)
    aliases = make_aliases(output)
    # Validate before replacing the last successful build.
    from validate import validate
    validate(output, require_report=False)

    return aliases


def build():
    """Validate both outputs before replacing the managed pair with rollback."""
    data = palette()
    if (ROOT / "src").is_symlink() or any(p.is_symlink() for p in (ROOT / "src").rglob("*")):
        raise ValueError("Source artwork must not contain symlinks")
    THEME.parent.mkdir(exist_ok=True)
    from manage_install import check_targets, replace_pair
    check_targets(THEME.parent, replace=True)
    with tempfile.TemporaryDirectory(prefix=".build-", dir=THEME.parent) as work:
        for mode, name in VARIANTS.items():
            count = build_variant(Path(work) / name, mode, data)
            print(f"Built {name}: {count} aliases; accent {data['accent'][mode]}")
        replace_pair(Path(work), THEME.parent)
    from scan_desktop_icons import scan, write_reports
    write_reports(scan(theme=THEME))


if __name__ == "__main__":
    build()
