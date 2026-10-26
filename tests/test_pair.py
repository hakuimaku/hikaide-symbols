"""Verify pair topology, migration and rollback without touching user themes."""
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from theme import THEME, NAME, VARIANTS, palette
from manage_install import install, uninstall, LEGACY_MARKER
from test_theme import fingerprint


class PairTests(unittest.TestCase):
    def test_matching_names_aliases_and_symbolic_bytes(self):
        """Only regular neutral paints and accents vary between appearances."""
        light = THEME.parent / VARIANTS["light"]
        dark_files = fingerprint(THEME)
        light_files = fingerprint(light)
        self.assertEqual(dark_files.keys(), light_files.keys())
        for path, value in dark_files.items():
            if value[0] == "link" or path.startswith("symbolic/"):
                self.assertEqual(value, light_files[path], path)
        self.assertEqual((THEME / "scalable/mimetypes/application-zip.svg").read_bytes(),
                         (light / "scalable/mimetypes/application-zip.svg").read_bytes())
        for icon in (THEME / "scalable/categories").glob("*.svg"):
            self.assertEqual(icon.read_bytes(), (light / "scalable/categories" / icon.name).read_bytes())
        for mode, name in VARIANTS.items():
            theme = THEME.parent / name
            metadata = json.loads((theme / ".hikaide-symbols.json").read_text())
            self.assertEqual(metadata, {"family": NAME, "version": 2, "variant": mode})
            warning = (theme / "scalable/status/dialog-warning.svg").read_text()
            error = (theme / "scalable/status/dialog-error.svg").read_text()
            self.assertIn(palette()[mode]["warning"], warning)
            self.assertIn(palette()[mode]["error"], error)

    def test_legacy_upgrade_and_pair_removal(self):
        """Migrate the v1 dark-only installation and remove both managed variants."""
        with tempfile.TemporaryDirectory(prefix="icons with spaces ") as directory:
            root = Path(directory)
            target = root / NAME
            target.mkdir()
            (target / ".hikaide-symbols").write_text(LEGACY_MARKER)
            install(root, replace=True)
            self.assertTrue((root / VARIANTS["light"] / "index.theme").is_file())
            uninstall(root)
            self.assertFalse(target.exists())
            self.assertFalse((root / VARIANTS["light"]).exists())

    def test_unmanaged_light_prevents_update_and_uninstall(self):
        """Refuse before mutating the recognized dark sibling."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install(root)
            light = root / VARIANTS["light"]
            (light / ".hikaide-symbols.json").write_text("unmanaged")
            before = fingerprint(root / NAME)
            for action in (lambda: install(root, replace=True), lambda: uninstall(root)):
                with self.assertRaises(ValueError):
                    action()
                self.assertEqual(before, fingerprint(root / NAME))

    def test_second_commit_failure_restores_pair(self):
        """A failed second replacement restores both previous trees exactly."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install(root)
            before = {name: fingerprint(root / name) for name in VARIANTS.values()}
            rename = Path.rename

            def fail_light(source, target):
                """Fail only the staged light commit, allowing rollback renames."""
                if source.parent.name.startswith(".hikaide-install-") and source.name == VARIANTS["light"]:
                    raise OSError("simulated second commit failure")
                return rename(source, target)

            with patch.object(Path, "rename", fail_light), self.assertRaises(OSError):
                install(root, replace=True)
            self.assertEqual(before, {name: fingerprint(root / name) for name in VARIANTS.values()})

    def test_cache_failure_preserves_pair(self):
        """A second cache failure cannot change either installed tree."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install(root)
            before = {name: fingerprint(root / name) for name in VARIANTS.values()}
            with patch("manage_install.shutil.which", return_value="/fake/cache"), \
                 patch("manage_install.subprocess.run", side_effect=[None, subprocess.CalledProcessError(1, "cache")]), \
                 self.assertRaises(subprocess.CalledProcessError):
                install(root, replace=True)
            self.assertEqual(before, {name: fingerprint(root / name) for name in VARIANTS.values()})

    def test_failed_restore_keeps_recoverable_backups(self):
        """Even a rollback failure preserves both previous trees outside staging."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install(root)
            before = {name: fingerprint(root / name) for name in VARIANTS.values()}
            rename = Path.rename

            def fail_commit_and_restore(source, target):
                """Fail the light commit and every rollback restore."""
                if (source.parent.name.startswith(".hikaide-install-") and source.name == VARIANTS["light"]
                        or source.parent.name.startswith(".hikaide-previous-")):
                    raise OSError("simulated storage failure")
                return rename(source, target)

            with patch.object(Path, "rename", fail_commit_and_restore), self.assertRaisesRegex(OSError, "Rollback failed"):
                install(root, replace=True)
            backups = list(root.glob(".hikaide-previous-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(before, {name: fingerprint(backups[0] / name) for name in VARIANTS.values()})

    def test_uninstall_rename_failure_restores_pair(self):
        """Uninstall validates and moves both targets before deleting anything."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            install(root)
            before = {name: fingerprint(root / name) for name in VARIANTS.values()}
            rename = Path.rename

            def fail_light(source, target):
                """Fail the second removal while permitting the dark restore."""
                if source == root / VARIANTS["light"]:
                    raise OSError("simulated removal failure")
                return rename(source, target)

            with patch.object(Path, "rename", fail_light), self.assertRaises(OSError):
                uninstall(root)
            self.assertEqual(before, {name: fingerprint(root / name) for name in VARIANTS.values()})

    def test_second_build_failure_preserves_outputs(self):
        """A failed light build leaves the last successful dist pair intact."""
        import build
        before = {name: fingerprint(THEME.parent / name) for name in VARIANTS.values()}
        compile_variant = build.build_variant

        def fail_light(output, mode, data):
            """Simulate validation failure after generating the first variant."""
            if mode == "light":
                raise ValueError("invalid light source")
            return compile_variant(output, mode, data)

        with patch.object(build, "build_variant", fail_light), self.assertRaises(ValueError):
            build.build()
        self.assertEqual(before, {name: fingerprint(THEME.parent / name) for name in VARIANTS.values()})

    def test_source_symlink_is_rejected(self):
        """Do not compile artwork reached through external source symlinks."""
        import build
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "src/places").symlink_to(THEME / "scalable/places", target_is_directory=True)
            with patch.object(build, "ROOT", root), self.assertRaises(ValueError):
                build.build()

    def test_invalid_palette_is_rejected(self):
        """Reject malformed colors and incomplete role sets before building."""
        original = (THEME.parents[1] / "src/theme/palette.json").read_text()
        invalid = json.loads(original)
        invalid["accent"]["light"] = "#fff;invalid"
        with patch.object(Path, "read_text", return_value=json.dumps(invalid)), self.assertRaises(ValueError):
            palette()
        del invalid["light"]["folderFront"]
        with patch.object(Path, "read_text", return_value=json.dumps(invalid)), self.assertRaises(ValueError):
            palette()
