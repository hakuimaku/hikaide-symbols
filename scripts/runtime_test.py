#!/usr/bin/env python3
"""Isolated GTK3/4 theme lookup, rendering, HiDPI, fallback and widget smoke checks.

Uses a private Gtk.IconTheme and per-process settings. Does not select the theme
for the running desktop, change dconf, or touch installed icon themes.
"""
import argparse
import atexit
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from theme import ROOT, THEME, NAME


def run_gtk(version):
    import gi
    gi.require_version("Gtk", version + ".0")
    from gi.repository import Gtk, Gdk, GLib
    from PIL import Image, ImageDraw, ImageFont
    Gtk.init_check()
    display = Gdk.Display.get_default()
    if display is None:
        raise RuntimeError("No display connection; run with display access or a Broadway test display")
    sizes = (16, 24, 32, 48, 64)
    theme = Gtk.IconTheme.new()
    renderer = None
    if version == "3":
        defaults = Gtk.IconTheme.get_default().get_search_path()
        theme.set_search_path([str(THEME.parent), *defaults])
        theme.set_custom_theme(NAME)
        # This settings object exists only in this test process.
        Gtk.Settings.get_default().set_property("gtk-icon-theme-name", NAME)
        Gtk.IconTheme.get_default().prepend_search_path(str(THEME.parent))
    else:
        gi.require_version("Gsk", "4.0")
        from gi.repository import Gsk, Graphene
        defaults = Gtk.IconTheme.get_for_display(display).get_search_path()
        theme.set_search_path([str(THEME.parent), *defaults])
        theme.set_theme_name(NAME)
        Gtk.IconTheme.get_for_display(display).add_search_path(str(THEME.parent))
        Gtk.Settings.get_default().set_property("gtk-icon-theme-name", NAME)
        renderer = Gsk.CairoRenderer.new()
        renderer.realize(None)
        atexit.register(lambda: renderer.unrealize() if renderer.is_realized() else None)

    def rgba(value):
        c = Gdk.RGBA()
        assert c.parse(value)
        return c

    def lookup(name, size, scale=1):
        if version == "3":
            info = theme.lookup_icon_for_scale(name, size, scale, Gtk.IconLookupFlags.FORCE_SIZE)
            assert info is not None, name
            return info, Path(info.get_filename())
        info = theme.lookup_icon(name, None, size, scale, Gtk.TextDirection.NONE, Gtk.IconLookupFlags(0))
        assert info is not None and info.get_file() is not None, name
        return info, Path(info.get_file().get_path())

    def render(name, size, fg="#e8edf5", accent="#5294e2"):
        info, path = lookup(name, size)
        assert path.is_relative_to(THEME), (name, path)
        if version == "3":
            pixbuf = info.load_symbolic(rgba(fg), rgba("#36a467"), rgba("#d7a43e"), rgba("#df5258"))[0] if name.endswith("-symbolic") else info.load_icon()
            assert (pixbuf.get_width(), pixbuf.get_height()) == (size, size), (name, size)
            ok, data = pixbuf.save_to_bufferv("png", [], [])
            assert ok
        else:
            snapshot = Gtk.Snapshot()
            if name.endswith("-symbolic"):
                colors = [rgba(c) for c in (fg, "#df5258", "#d7a43e", "#36a467", accent)]
                info.snapshot_symbolic(snapshot, size, size, colors)
            else:
                info.snapshot(snapshot, size, size)
            node = snapshot.to_node()
            assert node is not None, name
            rect = Graphene.Rect()
            rect.init(0, 0, size, size)
            texture = renderer.render_texture(node, rect)
            data = texture.save_to_png_bytes().get_data()
        image = Image.open(io.BytesIO(data)).convert("RGBA")
        assert image.getbbox() is not None, f"Empty rendered icon: {name}"
        return image

    required = json.loads((ROOT / "tests/required-icons.json").read_text())
    regular_names = sorted({n for names in required.values() for n in names})
    symbolic_names = sorted({p.stem for p in (THEME / "symbolic").glob("*/*.svg")})
    checked = 0
    for name in regular_names + symbolic_names:
        for size in sizes:
            _, path = lookup(name, size)
            assert path.is_relative_to(THEME), f"Unexpected fallback: {name} -> {path}"
            checked += 1
    for folder in (THEME / "scalable").iterdir():
        for file in folder.glob("*.svg"):
            if not file.is_symlink():
                render(file.stem, 32)
    for name in symbolic_names:
        render(name, 16)
    for suffix in ("", "-symbolic"):
        for size in sizes:
            dropped = render("folder-drag-accept" + suffix, size)
            assert dropped.tobytes() == render("folder-open" + suffix, size).tobytes(), "Drop icon must use open artwork"
            assert dropped.tobytes() != render("folder" + suffix, size).tobytes(), "Open folder must differ from closed folder"
    for name in ("folder", "application-pdf", "firefox", "document-save-symbolic"):
        info, path = lookup(name, 32, scale=2)
        assert path.is_relative_to(THEME)
        if version == "3":
            pixbuf = info.load_icon()
            assert (pixbuf.get_width(), pixbuf.get_height()) == (64, 64)

    red = render("document-save-symbolic", 24, fg="#ff0000")
    blue = render("document-save-symbolic", 24, fg="#0000ff")
    assert red.tobytes() != blue.tobytes(), "Symbolic foreground recoloring failed"
    gpa = "legacy foreground fallback (GTK3)"
    if version == "4" and Gtk.get_minor_version() >= 22:
        green = render("object-select-symbolic", 24, fg="#ff0000", accent="#00ff00")
        purple = render("object-select-symbolic", 24, fg="#ff0000", accent="#aa00ff")
        assert green.tobytes() != purple.tobytes(), "GTK4 GPA accent did not recolor"
        assert green.getchannel("G").getextrema()[1] > 180 and green.getchannel("R").getextrema()[1] < 64, "GPA accent is not green"
        gpa = "runtime accent A/B verified"

    with tempfile.TemporaryDirectory(prefix="hikaide-fallback-") as tmp:
        fallback = Path(tmp) / "hicolor"
        icons = fallback / "scalable/apps"
        icons.mkdir(parents=True)
        (fallback / "index.theme").write_text("[Icon Theme]\nName=Hicolor\nComment=Test fallback\nDirectories=scalable/apps\n[scalable/apps]\nSize=64\nType=Scalable\nMinSize=1\nMaxSize=512\nContext=Applications\n")
        probe = icons / "hikaide-fallback-probe.svg"
        probe.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="20" fill="#5294e2"/></svg>')
        theme.set_search_path([str(THEME.parent), tmp, *defaults])
        _, path = lookup("hikaide-fallback-probe", 32)
        assert path == probe, f"hicolor fallback failed: {path}"

    # Real GTK widgets, without mapping windows into the user's desktop.
    chooser = Gtk.FileChooserWidget(action=Gtk.FileChooserAction.OPEN)
    if version == "3":
        chooser.set_current_folder(str(ROOT / "docs"))
        settings = Gtk.Grid()
        settings.add(Gtk.Image.new_from_icon_name("preferences-system", Gtk.IconSize.DIALOG))
        chooser.destroy()
        settings.destroy()
    else:
        from gi.repository import Gio
        chooser.set_current_folder(Gio.File.new_for_path(str(ROOT / "docs")))
        settings = Gtk.Grid()
        settings.attach(Gtk.Image.new_from_icon_name("preferences-system"), 0, 0, 1, 1)
    context = GLib.MainContext.default()
    deadline = time.monotonic() + .25
    while time.monotonic() < deadline and context.pending():
        context.iteration(False)

    sample = ["folder", "folder-drag-accept", "folder-home", "folder-download", "application-pdf", "text-x-python", "firefox", "vscode",
              "org.mozilla.firefox", "org.gnome.Nautilus", "document-save-symbolic", "network-wireless-signal-good-symbolic",
              "battery-level-50-symbolic", "object-select-symbolic", "folder-home-symbolic"]
    sheet = Image.new("RGB", (960, len(sample) * 90 + 70), "#121820")
    draw = ImageDraw.Draw(sheet)
    font_path = subprocess.check_output(["fc-match", "-f", "%{file}", "sans"], text=True)
    font = ImageFont.truetype(font_path, 15)
    draw.text((20, 20), f"GTK{version} native rendering / 16 · 24 · 32 · 48 · 64 px", font=font, fill="white")
    for row, name in enumerate(sample):
        y = 70 + row * 90
        draw.text((20, y + 22), name, font=font, fill="#bfc9d9")
        x = 460
        for size in sizes:
            img = render(name, size)
            sheet.paste(img, (x, y + (64 - size) // 2), img)
            x += size + 24
    output = ROOT / "previews" / f"runtime-gtk{version}.png"
    output.parent.mkdir(exist_ok=True)
    sheet.save(output)
    if renderer:
        renderer.unrealize()
    result = {"gtk": f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}",
              "lookup_checks": checked, "sizes": list(sizes), "scale_2_lookup": "pass",
              "regular_and_symbolic_rendering": "pass", "foreground_recolor": "pass", "gpa_accent": gpa,
              "hicolor_fallback": "pass", "file_chooser_widget": "constructed", "settings_icon_widget": "constructed",
              "desktop_settings_changed": False, "preview": str(output.relative_to(ROOT))}
    print(json.dumps(result, indent=2))
    return result


def all_versions():
    results = []
    for version in ("3", "4"):
        process = subprocess.run([sys.executable, __file__, "--gtk", version],
                                 env={**os.environ, "GSETTINGS_BACKEND": "memory", "GSK_RENDERER": "cairo"},
                                 capture_output=True, text=True, timeout=60)
        if process.stderr:
            print(process.stderr, file=sys.stderr)
        if process.returncode:
            raise RuntimeError(f"GTK{version} failed ({process.returncode}): {process.stdout}")
        results.append(json.loads(process.stdout))
    target = ROOT / "reports/runtime-gtk.json"
    target.write_text(json.dumps(results, indent=2) + "\n")
    print(target.read_text())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gtk", choices=["3", "4"])
    args = parser.parse_args()
    run_gtk(args.gtk) if args.gtk else all_versions()
