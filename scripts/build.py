#!/usr/bin/env python3
"""Compile editable SVG sources into a deterministic, relocatable GTK theme."""
import shutil
import tempfile
from pathlib import Path
from theme import ROOT, THEME, NAME, CONTEXTS, accent
from make_aliases import make_aliases


def build():
    color = accent()
    THEME.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".build-", dir=THEME.parent) as work:
        output = Path(work) / NAME
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
                    text = svg.read_text().replace("@ACCENT@", color)
                    (output / directory / svg.name).write_text(text)
                size = 16 if variant == "symbolic" else int(variant.split("x")[0]) if "x" in variant else 64
                kind = "Fixed" if "x" in variant else "Scalable"
                sections.append(f"[{directory}]\nSize={size}\nContext={CONTEXTS[family]}\nType={kind}\n" +
                                ("MinSize=8\nMaxSize=512\n" if kind == "Scalable" else ""))
        header = (ROOT / "index.theme.in").read_text().replace("@DIRECTORIES@", ",".join(directories))
        (output / "index.theme").write_text(header + "\n" + "\n".join(sections))
        (output / ".hikaide-symbols").write_text("Hikaide-Symbols managed theme v1\n")
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
        if THEME.is_symlink():
            raise ValueError("Refusing to replace a symlinked build directory")
        if THEME.exists():
            if not (THEME / ".hikaide-symbols").is_file():
                raise ValueError("Refusing to replace an unmanaged build directory")
            shutil.rmtree(THEME)
        shutil.move(str(output), THEME)
    from scan_desktop_icons import scan, write_reports
    write_reports(scan(theme=THEME))
    print(f"Built {NAME}: {len(list(THEME.rglob('*.svg')))} SVG names, {aliases} aliases; accent {color}")


if __name__ == "__main__":
    build()
