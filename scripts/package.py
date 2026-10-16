#!/usr/bin/env python3
"""Make a deterministic, symlink-preserving installable theme archive."""
import gzip
import hashlib
import tarfile
from theme import ROOT, THEME, NAME
from validate import validate


def package():
    validate()
    output = ROOT / "dist" / (NAME + ".tar.gz")
    with output.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for path in [THEME, *sorted(THEME.rglob("*"))]:
                if path.name == "icon-theme.cache":
                    continue
                info = archive.gettarinfo(str(path), arcname=str(path.relative_to(THEME.parent)))
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
    package()
