#!/usr/bin/env python3
"""Make a deterministic, symlink-preserving installable theme archive."""
import gzip
import hashlib
import tarfile
from theme import ROOT, THEME, NAME, VARIANTS
from validate import validate


def package(theme=THEME):
    """Archive one validated appearance with reproducible timestamps and aliases."""
    validate(theme)
    name = theme.name
    output = ROOT / "dist" / (name + ".tar.gz")
    with output.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for path in [theme, *sorted(theme.rglob("*"))]:
                if path.name == "icon-theme.cache":
                    continue
                info = archive.gettarinfo(str(path), arcname=str(path.relative_to(theme.parent)))
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ""
                if info.isfile():
                    with path.open("rb") as stream:
                        archive.addfile(info, stream)
                else:
                    archive.addfile(info)
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{checksum}  {output.name}\n")
    print(f"{output.relative_to(ROOT)} ({output.stat().st_size:,} bytes)\nSHA256 {checksum}")


if __name__ == "__main__":
    for name in VARIANTS.values():
        package(THEME.parent / name)
