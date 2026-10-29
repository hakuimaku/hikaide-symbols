#!/usr/bin/env python3
"""Check real xdg-mime/GIO icon names against the built theme."""
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path
from theme import ROOT, THEME


def audit():
    import gi
    from gi.repository import Gio
    samples = {"sample.txt": "Hello world\n", "sample.md": "# A document\n", "sample.py": "#!/usr/bin/env python3\nprint('hello')\n",
               "sample.js": "const value = 1;\n", "sample.json": '{"hello":1}\n', "sample.yaml": "hello: world\n",
               "sample.toml": '[hello]\nvalue = 1\n', "sample.html": "<!doctype html><html><title>Hello</title></html>",
               "sample.css": "body { color: red; }\n", "sample.svg": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"/>',
               "sample.pdf": "%PDF-1.7\n1 0 obj<</Type/Catalog>>endobj\n%%EOF\n", "sample.desktop": "[Desktop Entry]\nName=Test\nType=Application\nExec=true\n",
               "sample.code-workspace": "{\n  \"folders\": []\n}\n"}
    available = {p.stem for p in (THEME / "scalable/mimetypes").glob("*.svg")}
    results = []
    with tempfile.TemporaryDirectory(prefix="hikaide-mime-") as tmp:
        base = Path(tmp)
        for name, text in samples.items():
            (base / name).write_text(text)
        with zipfile.ZipFile(base / "sample.zip", "w") as archive:
            archive.writestr("hello.txt", "hello")
        for file in sorted(base.iterdir()):
            mime = subprocess.check_output(["xdg-mime", "query", "filetype", str(file)], text=True).strip()
            names = Gio.content_type_get_icon(mime).get_names()
            matches = [name for name in names if name in available]
            assert matches, (file.name, mime, names)
            results.append({"sample": file.name, "mime": mime, "gio_icon_names": list(names), "resolved": matches})
    (ROOT / "reports/mimetype-audit.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"xdg-mime + GIO: {len(results)} real sample files resolve")


if __name__ == "__main__":
    audit()
