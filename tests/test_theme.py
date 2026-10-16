"""Behavioral checks for the actual built package and external accent CLI."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tarfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from theme import ROOT, THEME, NAME, accent
from validate import validate
from manage_install import install, uninstall
from scan_desktop_icons import scan
from accent_adapter import detect, normalize
from package import package


def fingerprint(folder):
    return {str(p.relative_to(folder)): ("link", str(p.readlink())) if p.is_symlink() else ("file", hashlib.sha256(p.read_bytes()).hexdigest())
            for p in folder.rglob("*") if p.is_file() or p.is_symlink()}


class ThemeTests(unittest.TestCase):
    def test_required_coverage(self):
        required = json.loads((ROOT / "tests/required-icons.json").read_text())
        for family, names in required.items():
            for name in names:
                with self.subTest(family=family, name=name):
                    self.assertTrue((THEME / "scalable" / family / (name + ".svg")).is_file())
                    if family in {"actions", "status", "places", "devices"}:
                        self.assertTrue((THEME / "symbolic" / family / (name + "-symbolic.svg")).is_file())
        self.assertGreaterEqual(len(list((THEME / "scalable/apps").glob("*.svg"))), 120)
        self.assertGreaterEqual(len(list((THEME / "scalable/mimetypes").glob("*.svg"))), 80)

    def test_build_is_deterministic(self):
        before = fingerprint(THEME)
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True, capture_output=True)
        self.assertEqual(before, fingerprint(THEME))

    def test_flat_folders_fill_frame_and_share_accent(self):
        from PIL import Image
        import io
        from render_png import render
        for variant in ("scalable", "16x16", "24x24"):
            for file in (THEME / variant / "places").glob("*.svg"):
                if file.is_symlink():
                    continue
                root = ET.fromstring(file.read_text())
                self.assertFalse(any(el.tag.endswith(("Gradient", "filter")) for el in root.iter()), file)
                circles = [el for el in root.iter() if el.tag.endswith("}circle")]
                self.assertEqual(circles, [], file)
                plain = file.stem in {"folder", "folder-open"}
                groups = [el for el in root.iter() if el.tag.endswith("}g")]
                self.assertEqual(len(groups), 0 if plain else 1, file)
                self.assertEqual("ColorScheme-Highlight" in file.read_text(), not plain, file)
                self.assertFalse(any(el.get("id") == "hidden-label" for el in root.iter()), file)
                for el in root.iter():
                    tag = el.tag.rsplit("}", 1)[-1]
                    if tag == "g":
                        self.assertIn("ColorScheme-Highlight", el.get("class", ""), file)
                        self.assertTrue(el.get("stroke") == "currentColor" or el.get("fill") == "currentColor", file)
                for size in (16, 24, 64):
                    image = Image.open(io.BytesIO(render(file, size))).convert("RGBA")
                    left, top, right, bottom = image.getbbox()
                    self.assertGreaterEqual(right - left, size * .95, file)
                    self.assertGreaterEqual(bottom - top, size * .85, file)
                    if size == 64:
                        self.assertEqual(image.getpixel((58, 55)), (23, 25, 26, 255), file)
                        self.assertEqual(image.getpixel((5, 55)), (48, 50, 51, 255) if file.stem != "folder-open" else (56, 59, 61, 255), file)

    def test_folder_drop_uses_open_artwork_and_legacy_states_are_plain(self):
        from render_png import render
        for variant in ("scalable", "16x16", "24x24", "symbolic"):
            folder = THEME / variant / "places"
            suffix = "-symbolic.svg" if variant == "symbolic" else ".svg"
            opened = folder / ("folder-open" + suffix)
            dropped = folder / ("folder-drag-accept" + suffix)
            self.assertEqual(dropped.resolve(), opened)
            for name in ("folder-link", "folder-hidden", "folder-hidden-link"):
                self.assertEqual((folder / (name + suffix)).resolve(), folder / ("folder" + suffix))
            for size in (16, 24, 32, 48, 64):
                self.assertNotEqual(render(opened, size), render(folder / ("folder" + suffix), size))

    def test_validator_rejects_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / NAME
            shutil.copytree(THEME, folder, symlinks=True)
            file = folder / "scalable/places/folder-documents.svg"
            original = file.read_text()
            bad = [original.replace('viewBox="0 0 64 64"', 'viewBox="0 0 0 0"'),
                   original.replace("#5294E2", "#5294E2; background:red"),
                   original.replace("</svg>", '<image href="file:///etc/passwd"/></svg>'),
                   original.replace("</svg>", '<script>alert(1)</script></svg>'),
                   original.replace('fill="#303233"', 'fill="url(/etc/passwd)"'),
                   original.replace("</style>", '.ColorScheme-Secondary { color:#ABCDEF; }</style>')]
            for value in bad:
                file.write_text(value)
                with self.assertRaises(AssertionError):
                    validate(folder)
            file.write_text(original)
            link = folder / "scalable/places/folder-home.svg"
            link.unlink()
            link.symlink_to("missing.svg")
            with self.assertRaises(AssertionError):
                validate(folder)

    def test_gio_does_not_automatically_select_folder_variants(self):
        from gi.repository import Gio
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ordinary").mkdir()
            (root / ".hidden").mkdir()
            (root / "linked").symlink_to("ordinary", target_is_directory=True)
            rows = []
            for name, hidden, linked in (("ordinary", False, False), (".hidden", True, False), ("linked", False, True)):
                info = Gio.File.new_for_path(str(root / name)).query_info(
                    "standard::icon,standard::is-hidden,standard::is-symlink", Gio.FileQueryInfoFlags.NONE, None)
                self.assertEqual(info.get_is_hidden(), hidden)
                self.assertEqual(info.get_is_symlink(), linked)
                rows.append({"name": name, "hidden": hidden, "symlink": linked, "icon_names": list(info.get_icon().get_names())})
            self.assertTrue(all(row["icon_names"] == rows[0]["icon_names"] for row in rows))
            self.assertIn("folder", rows[0]["icon_names"])
            (ROOT / "reports/folder-state-lookup.json").write_text(json.dumps(rows, indent=2) + "\n")

    def test_archive_is_deterministic_and_relocatable(self):
        archive = ROOT / "dist" / (NAME + ".tar.gz")
        package()
        before = archive.read_bytes()
        package()
        self.assertEqual(before, archive.read_bytes())
        with tarfile.open(archive) as stream:
            members = stream.getmembers()
            self.assertTrue(any(m.name == NAME + "/index.theme" for m in members))
            self.assertTrue(any(m.issym() for m in members))
            for member in members:
                self.assertTrue(Path(member.name).is_relative_to(NAME))
                self.assertNotIn("..", Path(member.name).parts)
                self.assertEqual(member.mtime, 0)
                if member.issym():
                    self.assertFalse(Path(member.linkname).is_absolute())
                    self.assertNotIn("..", Path(member.linkname).parts)

    def test_scan_uses_exact_icons_and_user_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            user, system = Path(tmp) / "user", Path(tmp) / "system"
            user.mkdir(); system.mkdir()
            (system / "test.desktop").write_text("[Desktop Entry]\nName=System\nIcon=firefox\n")
            (user / "test.desktop").write_text("[Desktop Entry]\nName=User\nIcon=Alacritty\nX-Flatpak=org.alacritty.Alacritty\n")
            (system / "case.desktop").write_text("[Desktop Entry]\nName=Wrong case\nIcon=FIREFOX\n")
            (system / "absolute.desktop").write_text("[Desktop Entry]\nName=Absolute\nIcon=/opt/test.png\n")
            (system / "hidden.desktop").write_text("[Desktop Entry]\nName=Hidden\nIcon=firefox\nHidden=true\n")
            (system / "lstopo.desktop").write_text("[Desktop Entry]\nName=Hardware Locality lstopo\nIcon=hwloc\n")
            rows = scan([user, system])
            self.assertEqual(len(rows), 5)
            self.assertTrue(next(r for r in rows if r["icon"] == "hwloc")["covered"])
            row = next(r for r in rows if r["name"] == "User")
            self.assertEqual(row["icon"], "Alacritty")
            self.assertEqual(row["flatpak_id"], "org.alacritty.Alacritty")
            self.assertTrue(row["covered"])
            self.assertFalse(next(r for r in rows if r["name"] == "Wrong case")["covered"])
            self.assertFalse(next(r for r in rows if r["name"] == "Absolute")["covered"])
            self.assertFalse(next(r for r in rows if r["name"] == "Hidden")["visible"])

    def test_safe_install_upgrade_and_uninstall(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / NAME
            target.mkdir()
            (target / "precious.txt").write_text("preserve me")
            for action in (lambda: install(root, replace=True), lambda: uninstall(root)):
                with self.assertRaises(ValueError):
                    action()
            self.assertEqual((target / "precious.txt").read_text(), "preserve me")
            shutil.rmtree(target)
            install(root)
            validate(target)
            with self.assertRaises(ValueError):
                install(root)
            install(root, replace=True)
            self.assertTrue((target / "scalable/apps/org.mozilla.firefox.svg").is_symlink())
            if shutil.which("gtk-update-icon-cache"):
                self.assertTrue((target / "icon-theme.cache").is_file())
            uninstall(root)
            self.assertFalse(target.exists())
            target.symlink_to(THEME, target_is_directory=True)
            with self.assertRaises(ValueError):
                uninstall(root)
            target.unlink()

    def test_accent_adapters(self):
        self.assertEqual(normalize("#abcDEF"), "#ABCDEF")
        for value in ("red", "#fff", "#000000;bad", "../../file"):
            with self.assertRaises(ValueError):
                normalize(value)
        with patch.dict(os.environ, {"XDG_CURRENT_DESKTOP": "niri"}):
            with self.assertRaises(ValueError):
                detect()
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"XDG_CURRENT_DESKTOP": "KDE", "XDG_CONFIG_HOME": tmp}):
            (Path(tmp) / "kdeglobals").write_text("[General]\nAccentColor=122,162,247\n")
            self.assertEqual(detect(), "#7AA2F7")
        result = subprocess.CompletedProcess([], 0, "'purple'\n", "")
        with patch.dict(os.environ, {"XDG_CURRENT_DESKTOP": "ubuntu:GNOME"}), patch("accent_adapter.subprocess.run", return_value=result):
            self.assertEqual(detect(), "#9141AC")

    @unittest.skipUnless(shutil.which("icon-accent"), "external icon-accent is not installed")
    def test_external_accent_change_and_byte_exact_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "icons"
            theme = root / NAME
            shutil.copytree(THEME, theme, symlinks=True)
            env = {**os.environ, "XDG_STATE_HOME": str(Path(tmp) / "state")}
            command = [shutil.which("icon-accent"), "--icons-dir", str(root)]
            run = lambda *args: subprocess.run(command + list(args), env=env, check=True, capture_output=True, text=True)
            report = json.loads(run("inspect", NAME, "--json").stdout)
            self.assertEqual([c.upper() for c in report["editable_accents"]], [accent()])
            self.assertGreater(report["gtk_symbolic"], 0)
            self.assertGreater(report["gtk_gpa_accent"], 0)
            self.assertFalse(report["invalid_svg"])
            before = {p.relative_to(theme): p.read_bytes() for p in theme.rglob("*.svg") if not p.is_symlink()}
            links = {p.relative_to(theme): str(p.readlink()) for p in theme.rglob("*.svg") if p.is_symlink()}
            color_b = "#7AA2F7" if accent() != "#7AA2F7" else "#E57399"
            run("set", color_b, "--theme", NAME)
            changed = 0
            for path, data in before.items():
                after = (theme / path).read_bytes()
                expected = re.sub(rb"(\.ColorScheme-Highlight\s*\{\s*color:)#[A-Fa-f0-9]{6}",
                                  lambda m: m[1] + color_b.lower().encode(), data)
                self.assertEqual(after, expected, path)
                changed += after != data
            self.assertEqual(changed, report["editable_svg_files"])
            self.assertEqual([c.upper() for c in json.loads(run("inspect", NAME, "--json").stdout)["editable_accents"]], [color_b])
            midway = fingerprint(theme)
            run("set", color_b, "--theme", NAME)
            self.assertEqual(midway, fingerprint(theme))
            run("restore", NAME)
            self.assertTrue(all((theme / path).read_bytes() == data for path, data in before.items()))
            self.assertEqual(links, {p.relative_to(theme): str(p.readlink()) for p in theme.rglob("*.svg") if p.is_symlink()})


if __name__ == "__main__":
    unittest.main(verbosity=2)
