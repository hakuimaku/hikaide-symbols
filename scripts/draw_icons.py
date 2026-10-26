#!/usr/bin/env python3
"""Author the house SVG families from small vector primitives.

Run explicitly to regenerate artwork; build.py preserves manual source SVG edits.
Glyph coordinates are 24 units; symbolic artwork is drawn separately at 16 units.
"""
import json
from html import escape
from theme import ROOT

P = {
    "minus": "M3 12h18",
    "folder": "M3 8V6h6l3 3h9v12H3Z",
    "folder-open": "M3 12V6h6l3 3h9v3M3 21l-2-9h22l-4 9Z",
    "home": "M12 2.5 2 11.5h3v9.5h5v-7.5h4v7.5h5v-9.5h3Z",
    "monitor": "M2 3h20v14H2ZM8 22h8m-4-5v5",
    "document": "M5 2h9l5 5v15H5Zm9 0v6h5M8 12h8m-8 4h8",
    "download": "M10 2h4v11h5l-7 7-7-7h5ZM3 23h18",
    "upload": "M10 22h4V11h5l-7-7-7 7h5ZM3 1h18",
    "music": "M9 17V5l12-3v13M9 9l12-3M9 17a3 3 0 1 1-3-3q3 0 3 3Zm12-2a3 3 0 1 1-3-3q3 0 3 3Z",
    "image": "M2 3h20v18H2ZM3 18l6-7 5 5 3-3 5 5M18 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z",
    "users": "M15 3a4 4 0 1 1 0 8 4 4 0 0 1 0-8ZM8 22v-3a7 7 0 0 1 14 0v3ZM5 6a3 3 0 1 1 0 6m1 3q-5 0-5 7h4",
    "template": "M5 2h10l4 4v16H5Zm3 4v2m0 3v2m0 3v2m4-12h2m-2 12h3",
    "film": "M2 2h20v20H2ZM7 2v20M17 2v20M2 7h5m-5 5h5m-5 5h5m10-10h5m-5 5h5m-5 5h5",
    "chart": "M3 13h3v9H3Zm8-10h3v19h-3Zm8 6h3v13h-3Z",
    "code": "M7 6 1 12l6 6M17 6l6 6-6 6M14 2l-4 20",
    "briefcase": "M2 7h20v15H2Zm6 0V2h8v5M2 13h20m-11 0v3h2v-3",
    "archive": "M2 3h20v5H2Zm2 5v14h16V8M9 13h6",
    "archive-stack": "M2.5 5.5 a9.5 3 0 1 0 19 0 a9.5 3 0 1 0-19 0Z M2.5 8 a9.5 3 0 0 0 19 0 v3.5 a9.5 3 0 0 1-19 0Z M2.5 12.5 a9.5 3 0 0 0 19 0 v3.5 a9.5 3 0 0 1-19 0Z M2.5 17 a9.5 3 0 0 0 19 0 v3.5 a9.5 3 0 0 1-19 0Z",
    "exit": "M9 3H3v18h6m5-14 5 5-5 5m5-5H7",
    "document-properties": "M4 2h9l5 5v15H4Zm9 0v5h5M8 12h8m-4-2v4M8 17h8m-6-2v4",
    "addon": "M4 7h4a3 3 0 0 1 6 0h4v4a3 3 0 0 1 0 6v4h-4a3 3 0 0 0-6 0h-4v-4a3 3 0 0 0 0-6Z",
    "help-about": "M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 7v8m0-12v1.5",
    "send": "m2 12 20-9-9 20-3-8Zm8 3 11-11",
    "trash": "M5 7v15h14V7M2 5h20M8 5V2h8v3M9 10v8m6-8v8",
    "network": "M12 3 3 20h18ZM15 3a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM6 20a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm18 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
    "share": "M5 12 19 4M5 12l14 8M8 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM22 4a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm0 16a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
    "cloud": "M6 20a5 5 0 0 1-1-10 7 7 0 0 1 14-2 6 6 0 0 1-1 12Z",
    "clock": "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0ZM12 5v7l4 3",
    "heart": "M12 21 3 12C-3 5 7-2 12 6c5-8 15-1 9 6Z",
    "star": "m12 1 3 7 8 1-6 6 2 8-7-4-7 4 2-8-6-6 8-1Z",
    "search": "M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Zm-2 5 7 7",
    "remote": "M2 3h20v14H2ZM8 22h8m-4-5v5M8 9h8m-3-3 3 3-3 3",
    "drive": "m5 4-3 12v6h20v-6L19 4ZM2 16h20m-5 3h1",
    "globe": "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0ZM2 12h20M12 2c-7 7-7 13 0 20 7-7 7-13 0-20ZM5 6h14M5 18h14",
    "lock": "M5 11h14v12H5Zm3 0V6a4 4 0 0 1 8 0v5M12 16v3",
    "unlock": "M5 11h14v12H5Zm3 0V6a4 4 0 0 1 8 0M12 16v3",
    "check": "m3 12 6 6L22 4",
    "link": "m9 15 6-6M8 18l-2 2a4 4 0 0 1-6-6l4-4a4 4 0 0 1 6 0m4-4 2-2a4 4 0 0 1 6 6l-4 4a4 4 0 0 1-6 0",
    "sync": "M3 10a9 9 0 0 1 16-5l3 4M22 2v7h-7M21 14a9 9 0 0 1-16 5l-3-4m0 7v-7h7",
    "error": "M5 5l14 14M19 5 5 19",
    "info": "M12 10v9m0-14v1",
    "warning": "m12 2 11 20H1Zm0 7v6m0 3v1",
    "question": "M7 7a5 5 0 0 1 10 0c0 4-5 3-5 7m0 5v1",
    "play": "m5 2 17 10L5 22Z",
    "pause": "M5 3h4v18H5Zm10 0h4v18h-4Z",
    "stop": "M4 4h16v16H4Z",
    "sound": "M2 9h5l6-6v18l-6-6H2ZM17 8q4 4 0 8m3-12q8 8 0 16",
    "mic": "M9 4a3 3 0 0 1 6 0v8a3 3 0 0 1-6 0Zm-4 6v2a7 7 0 0 0 14 0v-2M12 19v4m-4 0h8",
    "battery": "M2 6h18v12H2Zm18 4h3v4h-3M5 9h12v6H5Z",
    "lua": "M10.5 7a6.5 6.5 0 1 0 0 13 6.5 6.5 0 1 0 0-13M10.5 10.5a3 3 0 1 0 0 6 3 3 0 1 0 0-6M17.5 4.5a2 2 0 1 0 0 4 2 2 0 1 0 0-4",
    "bolt": "M14 1 4 14h7l-1 9 10-13h-7Z",
    "bluetooth": "m6 6 13 12-7 5V1l7 5L6 18",
    "wifi": "M1 7q11-10 22 0M5 12q7-7 14 0m-10 5q3-3 6 0m-3 4h.01",
    "ethernet": "M3 3h18v14h-5v5H8v-5H3ZM7 7v5m5-5v5m5-5v5",
    "laptop": "M4 3h16v14H4ZM4 17l-3 5h22l-3-5",
    "usb": "M9 1h6v6h3v16H6V7h3Zm2 2v2m2-2v2",
    "disc": "M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0Zm-7 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
    "camera": "M2 7h5l2-4h6l2 4h5v15H2Zm15 7a5 5 0 1 1-10 0 5 5 0 0 1 10 0Z",
    "video-camera": "M2 5h13v14H2ZM15 9l7-4v14l-7-5",
    "chip": "M5 5h14v14H5Zm4 4h6v6H9ZM8 1v4m8-4v4M8 19v4m8-4v4M1 8h4m-4 8h4m14-8h4m-4 8h4",
    "headphones": "M3 14V9a9 9 0 0 1 18 0v5M3 12h4v10H3Zm14 0h4v10h-4Z",
    "speaker": "M5 1h14v22H5Zm11 15a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM13 6a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z",
    "keyboard": "M1 5h22v15H1ZM4 9h1m3 0h1m3 0h1m3 0h1m3 0h1M4 13h1m3 0h1m3 0h1m3 0h1m3 0h1M7 17h10",
    "mouse": "M5 8a7 7 0 0 1 14 0v8a7 7 0 0 1-14 0Zm7-7v8m-7 1h14",
    "touchpad": "M2 4h20v17H2ZM2 16h20m-10 0v5",
    "gamepad": "M8 6h8q5-4 6 3l1 9q-1 6-7-1H8q-6 7-7 1l1-9q1-7 6-3ZM7 9v6m-3-3h6m7-2h.01m3 4h.01",
    "phone": "M6 1h12v22H6Zm4 19h4",
    "tablet": "M3 1h18v22H3Zm8 19h2",
    "printer": "M6 9V1h12v8M6 18H2V9h20v9h-4M6 14h12v9H6Z",
    "scanner": "M2 12h20v10H2ZM3 12 6 2l15 7M6 18h12",
    "terminal": "m3 5 7 7-7 7m9 1h9",
    "gear": "m9 2 1 3h4l1-3 4 2-1 3 2 2 3-1 1 5-3 1-1 3 2 2-4 3-2-2h-4l-2 2-4-3 2-2-1-3-3-1 1-5 3 1 2-2-1-3Zm7 10a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z",
    "box": "m12 1 10 5v12l-10 5-10-5V6Zm0 10L2 6m10 5L22 6m-10 5v12M7 3l10 5v6",
    "text": "M4 5h16M4 10h16M4 15h16M4 20h10",
    "spreadsheet": "M2 3h20v18H2ZM2 9h20M2 15h20M9 3v18m6-18v18",
    "pie": "M11 2a10 10 0 1 0 11 11H11Zm4-1v9h9a10 10 0 0 0-9-9Z",
    "presentation": "M2 3h20v15H2Zm10 15v5m-6 0 6-5 6 5M6 7h12v7H6Z",
    "pdf": "M7 20c4-6 9-19 4-19-4 0 1 14 8 14 8 0-1-6-13-1-9 4-3 10 1 6Z",
    "vector": "M3 5h18M12 5C1 5 1 21 3 21M12 5c11 0 11 16 9 16M10 3h4v4h-4ZM1 19h4v4H1Zm18 0h4v4h-4Z",
    "wave": "M2 10v4m5-8v12m5-17v22m5-17v12m5-8v4",
    "config": "M2 6h20M2 18h20M8 2v8M16 14v8",
    "braces": "M9 2H6v7l-3 3 3 3v7h3M15 2h3v7l3 3-3 3v7h-3",
    "hash": "M9 2 6 22M18 2l-3 20M2 8h20M1 16h20",
    "diamond": "m6 3-5 6 11 14L23 9l-5-6ZM1 9h22M6 3l6 20 6-20",
    "coffee": "M5 10h12v7q0 5-6 5t-6-5Zm12 1h3q5 6-3 6M9 7c-7-5 8-3 1-7m5 7c-5-4 6-4 2-7",
    "calendar": "M2 4h20v18H2ZM2 9h20M7 1v6m10-6v6M7 13h3v4H7Zm7 0h3v4h-3Z",
    "mail": "M2 4h20v16H2ZM2 4l10 9L22 4M2 20l7-8m13 8-7-8",
    "chat": "M2 2h20v15H10l-6 6v-6H2ZM6 7h12M6 12h8",
    "pen": "m3 16 13-14 6 5L9 21l-7 2Zm10-11 6 5M3 16l6 5",
    "brush": "m8 15 9-13 5 4-10 12ZM8 15c-6-3-2 6-7 7 8 2 14-2 7-7Z",
    "cube": "m12 1 10 5v12l-10 5L2 18V6Zm0 10L2 6m10 5 10-5m-10 5v12",
    "eye": "M1 12Q12-3 23 12 12 27 1 12Zm15 0a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z",
    "shield": "m12 1 10 4v8q-1 7-10 10-9-3-10-10V5Z",
    "calculator": "M3 1h18v22H3ZM6 4h12v5H6ZM6 13h3m6 0h3M6 18h3m6-2v5m-2-2h4",
    "scissors": "M8 16 20 2M8 8l12 14M8 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm0 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
    "clipboard": "M7 4H3v19h18V4h-4M8 2h8v5H8ZM7 12h10M7 17h10",
    "save": "M2 2h17l3 3v17H2ZM6 2v7h11V2M6 14h12v8H6Z",
    "new": "M5 2h10l4 4v7M5 2v20h8M18 15v8m-4-4h8",
    "copy": "M7 7h15v15H7ZM3 17H1V1h16v2",
    "select": "M2 2h4m3 0h6m3 0h4v4m0 3v6m0 3v4h-4m-3 0H9m-3 0H2v-4m0-3V9m0-3V2",
    "list": "M2 4h1m4 0h15M2 12h1m4 0h15M2 20h1m4 0h15",
    "grid": "M2 2h7v7H2Zm13 0h7v7h-7ZM2 15h7v7H2Zm13 0h7v7h-7Z",
    "map": "m1 5 7-3 8 3 7-3v17l-7 3-8-3-7 3Zm7-3v17m8-14v17",
    "pin": "M12 23S3 13 3 9a9 9 0 0 1 18 0c0 4-9 14-9 14Zm3-14a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z",
    "sun": "M17 12a5 5 0 1 1-10 0 5 5 0 0 1 10 0ZM12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2",
    "book": "M12 5Q7 1 1 3v18q6-2 11 2 5-4 11-2V3q-6-2-11 2Zm0 0v18",
    "key": "M14 9a6 6 0 1 1-6-7 6 6 0 0 1 6 7Zm-3 4 10 10m-6-6 3-3m0 6 3-3",
    "power": "M12 1v11M6 4a10 10 0 1 0 12 0",
}


def glyph(name, color="currentColor", width=2.3):
    return f'<path d="{P[name]}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'


def svg(name, body, size=64, accent=False):
    style = '<style id="current-color-scheme">.ColorScheme-Highlight { color:@ACCENT@; }</style>' if accent else ''
    gpa = ' gpa:version="1"' if 'gpa:fill="accent"' in body else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:gpa="https://www.gtk.org/grappa"{gpa} width="{size}" height="{size}" viewBox="0 0 {size} {size}">\n'
            f'<title>{escape(name)}</title>\n{style}\n{body}\n</svg>\n')


def write(family, name, body, size=64, accent=False):
    path = ROOT / "src" / family / f"{name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    if family.startswith("symbolic/"):
        from outline_symbolic import outline
        geometry = outline(svg(name, body, size))
        role = ' gpa:fill="accent"' if 'gpa:stroke="accent"' in body else ''
        body = f'<path d="{geometry}" fill="#2e3436" fill-rule="evenodd"{role}/>'
    path.write_text(svg(name, body, size, accent))


def primitive(family, name="shell"):
    return (ROOT / "src/primitives" / family / f"{name}.svg").read_text()


def trash_body(name, width=2.3):
    is_full = name == "user-trash-full"
    stroke_w = "2.8" if width > 2.5 else "2.6"
    handle_w = "3.5" if width > 2.5 else "3"

    parts = []
    if is_full:
        parts.append('<path d="m22 16-4-8 9-3 5 11" fill="@PAPER@"/>')
        parts.append('<path d="m33 16 6-9 9 4-5 9" fill="@PAPER_SMALL@"/>')
        parts.append('<path d="m25 13 9-5 7 5" fill="@PAPER_SHADE@"/>')
        parts.append('<g transform="rotate(-12 12 14)">')
        parts.append(f'<path d="M24 10V6q0-2 2-2h12q2 0 2 2v4" fill="none" stroke="@FOLDER_BACK@" stroke-width="{handle_w}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append('<rect x="10" y="11" width="44" height="6" rx="2.5" fill="@FOLDER_BACK@"/>')
        parts.append('</g>')
    else:
        parts.append(f'<path d="M24 10V6q0-2 2-2h12q2 0 2 2v4" fill="none" stroke="@FOLDER_BACK@" stroke-width="{handle_w}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append('<rect x="10" y="11" width="44" height="6" rx="2.5" fill="@FOLDER_BACK@"/>')

    parts.append('<path d="M14 16h36l-3.5 38q-.5 4-4.5 4H22q-4 0-4.5-4Z" fill="@FOLDER_FRONT@"/>')
    parts.append('<path d="M18 54l-.5 4q-.5 4 4.5 4h20q4 0 4.5-4l-.5-4Z" fill="@FOLDER_CORNER@"/>')
    parts.append(f'<g class="ColorScheme-Highlight" stroke="currentColor"><path d="M26 24v22M32 24v22M38 24v22" fill="none" stroke="currentColor" stroke-width="{stroke_w}" stroke-linecap="round"/></g>')
    return "".join(parts)


def places():
    data = {
        "folder": "folder", "folder-open": "folder-open", "user-home": "home", "user-desktop": "monitor",
        "folder-documents": "document", "folder-download": "download", "folder-music": "music",
        "folder-pictures": "image", "folder-publicshare": "users", "folder-templates": "template",
        "folder-videos": "film", "folder-projects": "chart", "folder-code": "code", "folder-work": "briefcase",
        "folder-archive": "archive", "user-trash": "trash", "user-trash-full": "trash", "folder-network": "network",
        "folder-remote": "remote", "folder-shared": "share", "folder-cloud": "cloud", "folder-recent": "clock",
        "folder-favorites": "heart", "folder-important": "star", "folder-saved-search": "search",
        "folder-devices": "drive", "network-workgroup": "globe", "network-server": "drive",
        "user-bookmarks": "book", "start-here": "home"}
    shell = primitive("folder")
    for name, symbol in data.items():
        for family, width in (("places", 2.3), ("16x16/places", 2.7), ("24x24/places", 2.7)):
            if name in {"user-trash", "user-trash-full"}:
                body = trash_body(name, width)
                write(family, name, body, accent=True)
                continue
            body = shell
            if name == "folder-open":
                body += '<path d="M5 23q0-3 3-3h48q3 0 3 3v27H5Z" fill="@FOLDER_OPEN_INTERIOR@"/>'
                body += '<path d="M1 36q0-4 4-4l50-6q8-1 8 6v21q0 7-7 7H8q-7 0-7-7Z" fill="@FOLDER_OPEN_FRONT@"/>'
            if name == "user-trash-full":
                body += '<path d="m28 30-3-6 6-2 4 8m0 0 4-5 6 3-2 4" fill="none" class="ColorScheme-Highlight" stroke="currentColor" stroke-width="2.6"/>'
            decorated = name not in {"folder", "folder-open"}
            if decorated:
                if symbol == "home":
                    body += f'<g transform="translate(19 28) scale(1.1)" class="ColorScheme-Highlight" fill="currentColor"><path d="{P[symbol]}" fill="currentColor"/></g>'
                else:
                    body += f'<g transform="translate(19 28) scale(1.1)" class="ColorScheme-Highlight" stroke="currentColor">{glyph(symbol, width=width)}</g>'
            body += primitive("folder", "corner")
            write(family, name, body, accent=decorated)
        symbolic("places", name, symbol)
    aliases = {"folder": ["inode-directory", "gtk-directory", "folder-visiting", "folder-link", "folder-hidden", "folder-hidden-link"],
               "folder-open": ["folder-drag-accept"],
               "user-home": ["folder-home", "gnome-fs-home", "go-home"],
               "user-desktop": ["folder-desktop", "desktop"],
               "folder-download": ["folder-downloads"], "folder-publicshare": ["folder-public"],
               "folder-pictures": ["folder-photos"], "folder-favorites": ["folder-favorite"],
               "folder-saved-search": ["folder-search"], "user-trash": ["folder-trash", "gnome-fs-trash-empty"],
               "user-trash-full": ["gnome-fs-trash-full"], "folder-recent": ["document-open-recent"],
               "folder-remote": ["folder-ssh", "folder-sftp"], "folder-network": ["network", "gnome-fs-network"],
               "folder-cloud": ["folder-nextcloud", "folder-owncloud"], "folder-shared": ["folder-share"]}
    # Action go-home is separately drawn; keep lookups unambiguous across contexts.
    aliases["user-home"].remove("go-home")
    manifests = {f"{v}/places": aliases for v in ("scalable", "16x16", "24x24")}
    manifests["symbolic/places"] = {k + "-symbolic": [n + "-symbolic" for n in ns] for k, ns in aliases.items()}
    save_aliases("places", manifests)
    return data


def symbolic(family, name, symbol):
    # Dedicated 16px geometry: remove surfaces, folds, gradients, status dots and shadows.
    if symbol == "home":
        g = f'<path d="{P[symbol]}" fill="currentColor"/>'
    else:
        g = glyph(symbol, width=2.57)
    if name in {"object-select", "emblem-default", "folder-favorites", "folder-important"}:
        g = g.replace('<path ', '<path gpa:stroke="accent" ')
    body = f'<g transform="translate(1 1) scale(.5833333333)" color="#2e3436">{g}</g>'
    write(f"symbolic/{family}", name + "-symbolic", body, size=16)


def save_aliases(family, data):
    path = ROOT / "src/aliases" / f"{family}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


LETTERS = {
    "A": "M0 10 3 0l3 10M1 6h4", "B": "M0 10V0h3q5 0 2 5 4 5-2 5Z M0 5h4",
    "C": "M6 1Q0-3 0 5t6 4", "D": "M0 0h2q8 0 3 9l-3 1H0Z", "E": "M6 0H0v10h6M0 5h5",
    "F": "M6 0H0v10M0 5h5", "G": "M6 1Q0-3 0 5t6 4V5H3", "H": "M0 0v10M6 0v10M0 5h6",
    "I": "M0 0h6M3 0v10M0 10h6", "J": "M0 0h6v7q0 5-6 2", "K": "M0 0v10M6 0 0 5l6 5",
    "L": "M0 0v10h6", "M": "M0 10V0l3 6 3-6v10", "N": "M0 10V0l6 10V0",
    "O": "M3 0Q0 0 0 5t3 5q3 0 3-5T3 0Z", "P": "M0 10V0h3q6 0 1 5H0",
    "Q": "M3 0Q0 0 0 5t3 5q3 0 3-5T3 0ZM3 7l4 4", "R": "M0 10V0h3q6 0 1 5H0m3 0 3 5",
    "S": "M6 1Q0-2 0 3t3 2q3 0 3 3t-6 1", "T": "M0 0h6M3 0v10", "U": "M0 0v7q0 6 6 0V0",
    "V": "M0 0 3 10 6 0", "W": "M0 0 1 10 3 5l2 5L6 0", "X": "M0 0l6 10M6 0 0 10",
    "Y": "M0 0l3 5 3-5M3 5v5", "Z": "M0 0h6L0 10h6", "1": "M1 2 3 0v10M0 10h6",
    "2": "M0 2q3-5 6 0t-6 8h6", "3": "M0 0h6L3 4q6 0 3 5t-6 0", "7": "M0 0h6L2 10",
    "+": "M0 5h6M3 2v6", "#": "M2 0 1 10M5 0 4 10M0 3h6M0 7h6",
}


def lettering(text, color="@FILE_GLYPH@", box=24):
    scale = min(1.7, box / (len(text) * 9))
    width = (len(text) * 9 - 3) * scale
    return f'<g transform="translate({(24-width)/2:g} {12-5*scale:g}) scale({scale:g})">' + ''.join(
        f'<path transform="translate({i*9} 0)" d="{LETTERS[c]}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        for i, c in enumerate(text)) + '</g>'


def mimetypes():
    # Canonical glyphs are shared by genuinely equivalent formats, via relative symlinks.
    data = {
        "text-x-generic": ("text", "text-plain text-rtf text-richtext application-rtf application-x-empty application-x-zerosize text-x-log text-x-patch text-x-diff"),
        "application-msword": ("W", "application-vnd.openxmlformats-officedocument.wordprocessingml.document application-vnd.ms-word"),
        "application-vnd.ms-excel": ("spreadsheet", "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        "application-vnd.ms-powerpoint": ("pie", "application-vnd.openxmlformats-officedocument.presentationml.presentation"),
        "application-pdf": ("pdf", "application-x-pdf"),
        "text-markdown": ("M", "text-x-markdown text-x-readme"),
        "application-vnd.oasis.opendocument.text": ("document", "application-vnd.oasis.opendocument.text-template"),
        "application-vnd.oasis.opendocument.spreadsheet": ("spreadsheet", "application-vnd.oasis.opendocument.spreadsheet-template text-csv text-tab-separated-values x-office-spreadsheet"),
        "application-vnd.oasis.opendocument.presentation": ("presentation", "application-vnd.oasis.opendocument.presentation-template"),
        "image-x-generic": ("image", "image-jpeg image-jpg image-webp image-heic image-heif image-tiff image-bmp image-x-icon image-avif image-vnd.microsoft.icon"),
        "image-raw": ("camera", "image-x-dcraw image-x-adobe-dng image-x-canon-cr2 image-x-canon-cr3 image-x-nikon-nef image-x-sony-arw"),
        "image-svg+xml": ("vector", "image-svg+xml-compressed image-x-eps application-postscript"),
        "image-png": ("checker", ""), "image-gif": ("film", ""),
        "application-x-photoshop": ("PS", "image-vnd.adobe.photoshop image-x-psd"),
        "application-illustrator": ("AI", "application-vnd.adobe.illustrator"),
        "audio-x-generic": ("music", "audio-mpeg audio-flac audio-x-flac audio-x-wav audio-wav audio-vnd.wave audio-aac audio-ogg application-ogg audio-x-m4a audio-mp4 audio-alac audio-aiff audio-x-aiff audio-opus audio-x-vorbis+ogg"),
        "audio-midi": ("wave", "audio-x-midi"), "application-x-cue": ("disc", "application-x-cdrdao-toc"),
        "video-x-generic": ("play", "video-mp4 video-x-matroska video-x-msvideo video-quicktime video-x-ms-wmv video-x-flv video-webm video-m4v video-x-m4v video-3gpp video-mpeg video-ogg video-x-ogm+ogg"),
        "application-zip": ("archive-box", "application-x-rar application-vnd.rar application-x-7z-compressed application-x-tar application-gzip application-x-gzip application-x-xz application-x-bzip application-x-bzip2 application-zstd application-x-zstd application-x-compressed-tar application-x-xz-compressed-tar application-x-bzip-compressed-tar application-x-lzma application-x-lz4 application-x-archive application-x-cpio application-x-lha application-x-lzh application-x-lzop application-x-zoo application-x-ace application-x-gtar application-x-tarz package-x-generic"),
        "application-x-iso9660-image": ("disc", "application-x-cd-image application-x-raw-disk-image application-x-apple-diskimage"),
        "application-octet-stream": ("chip", "application-x-firmware"),
        "text-html": ("code", "application-xhtml+xml text-x-qml"), "text-css": ("braces", "text-x-scss text-x-sass"),
        "application-javascript": ("JS", "text-javascript application-x-javascript"),
        "text-x-python": ("PY", "text-x-python3 application-x-python-bytecode"),
        "application-x-php": ("PHP", "text-x-php"), "application-x-ruby": ("diamond", "text-x-ruby"),
        "text-x-go": ("GO", ""), "text-x-java": ("coffee", "text-x-java-source application-java-archive application-x-java-archive"),
        "text-x-c": ("C", "text-x-csrc text-x-chdr"), "text-x-c++src": ("C+", "text-x-c++hdr"),
        "text-x-shellscript": ("hash", "application-x-shellscript text-x-script text-x-makefile"),
        "text-x-config": ("config", "application-x-desktop text-x-ini application-x-wine-extension-ini application-x-theme text-x-cmake"),
        "application-json": ("braces", "application-ld+json"), "application-xml": ("code", "text-xml"),
        "text-yaml": ("Y", "application-yaml application-x-yaml text-x-yaml"), "text-toml": ("T", "application-toml"),
        "text-x-rust": ("R", "text-rust"), "text-x-kotlin": ("K", ""), "text-x-swift": ("S", ""),
        "text-x-typescript": ("TS", "application-typescript text-typescript"),
        "text-x-lua": ("lua", ""),
        "application-x-executable": ("gear", "application-x-sharedlib application-x-object application-x-pie-executable application-x-ms-dos-executable"),
        "application-x-appimage": ("box", "application-vnd.appimage application-x-iso9660-appimage"),
        "application-vnd.flatpak": ("cube", "application-vnd.flatpak.ref application-vnd.flatpak.repo"),
        "application-x-rpm": ("box", "application-vnd.debian.binary-package application-x-deb application-x-alpm-package application-x-archlinux-package"),
        "application-x-font-ttf": ("T", "font-ttf font-otf application-x-font-otf application-font-woff font-woff font-woff2"),
        "application-x-sqlite3": ("archive-stack", "application-vnd.sqlite3 application-sql text-x-sql"),
        "application-x-bittorrent": ("download", ""),
    }
    aliases = {}
    for name, (symbol, names) in data.items():
        if name == "application-zip":
            box_body = ('<path d="M4 22h56v31q0 6-6 6H10q-6 0-6-6Z" fill="#ea9f30"/>'
                        '<path d="M60 47 47 59h7q6 0 6-6Z" fill="#b0630b"/>'
                        '<rect x="28" y="13" width="8" height="46" fill="#fce5b4"/>'
                        '<rect x="24" y="34" width="16" height="6.5" rx="3.25" fill="#9c5406"/>'
                        '<rect x="2" y="13" width="60" height="13" rx="3.5" fill="#d6871e"/>'
                        '<rect x="28" y="13" width="8" height="13" fill="#fce5b4"/>')
            write("mimetypes", name, box_body)
            for size in (16, 24):
                write(f"{size}x{size}/mimetypes", name, box_body)
        else:
            if symbol == "checker":
                g = ''.join(f'<rect x="{2+x*4}" y="{2+y*4}" width="4" height="4" fill="@FILE_GLYPH@"/>' for x in range(5) for y in range(5) if (x+y)%2 == 0)
            elif symbol == "archive-stack":
                g = f'<path d="{P[symbol]}" fill="@FILE_GLYPH@"/>'
            else:
                g = glyph(symbol, "@FILE_GLYPH@", 2.5) if symbol in P else lettering(symbol)
            body = primitive("file") + f'<g transform="translate(20 25)">{g}</g>'
            write("mimetypes", name, body)
            for size in (16, 24):
                body = '<path d="M14 4h27l11 11v43H12V6q0-2 2-2Z" fill="@PAPER_SMALL@"/><path d="M41 4v11h11" fill="@PAPER_SMALL_FOLD@"/>'
                body += f'<g transform="translate(18 24) scale(1.16)">{g}</g>'
                write(f"{size}x{size}/mimetypes", name, body)
        if names:
            aliases[name] = names.split()
    save_aliases("mimetypes", {f"{v}/mimetypes": aliases for v in ("scalable", "16x16", "24x24")})


def system_families():
    devices = dict(zip(
        "computer computer-laptop computer-desktop drive-harddisk drive-harddisk-system drive-removable-media drive-optical media-flash media-removable camera-photo camera-video audio-card audio-headphones audio-headset audio-speakers input-keyboard input-mouse input-touchpad input-gaming phone tablet printer scanner battery network-wired network-wireless bluetooth".split(),
        "monitor laptop monitor drive drive drive disc drive drive camera video-camera chip headphones headphones speaker keyboard mouse touchpad gamepad phone tablet printer scanner battery ethernet wifi bluetooth".split()))
    for name, symbol in devices.items():
        body = '<rect x="9" y="10" width="46" height="46" rx="12" fill="#000" opacity=".14"/>'
        body += '<defs><linearGradient id="metal" x2=".4" y2="1"><stop stop-color="@DEVICE_HIGHLIGHT@"/><stop offset="1" stop-color="@DEVICE_SHADE@"/></linearGradient></defs>'
        body += f'<g transform="translate(11 10) scale(1.75)">{glyph(symbol, "url(#metal)", 2.4)}</g>'
        body += '<circle cx="50" cy="49" r="3" class="ColorScheme-Highlight" fill="currentColor"/>'
        # Identical names across contexts must resolve identically.
        if name == "network-wired":
            body = status_body(name)
        write("devices", name, body, accent=True)
        if name == "network-wired":
            write("symbolic/devices", name + "-symbolic", status_geometry(name), size=16)
        else:
            symbolic("devices", name, symbol)
    statuses = (
        "network-wireless-signal-excellent network-wireless-signal-good network-wireless-signal-ok network-wireless-signal-weak network-wireless-offline network-wired network-vpn bluetooth-active bluetooth-disabled audio-volume-high audio-volume-medium audio-volume-low audio-volume-muted microphone-sensitivity-high microphone-sensitivity-muted battery-full battery-good battery-low battery-caution battery-empty battery-charging user-available user-away user-busy user-offline dialog-information dialog-warning dialog-error dialog-question").split()
    for name in statuses:
        write("status", name, status_body(name), accent="ColorScheme-Highlight" in status_body(name))
        write("symbolic/status", name + "-symbolic", status_geometry(name), size=16)
    actions = {
        "document-new": "new", "document-open": "folder", "document-save": "save", "document-save-as": "save-as",
        "document-print": "printer", "edit-cut": "scissors", "edit-copy": "copy", "edit-paste": "clipboard",
        "edit-delete": "trash", "edit-undo": "undo", "edit-redo": "redo", "edit-find": "search", "edit-select-all": "select",
        "go-back": "left", "go-forward": "right", "go-up": "up", "go-down": "down", "go-home": "home",
        "view-refresh": "sync", "view-grid": "grid", "view-list": "list", "view-sort-ascending": "sort-up",
        "view-sort-descending": "sort-down", "window-close": "error", "list-add": "plus", "list-remove": "minus",
        "media-playback-start": "play", "media-playback-pause": "pause", "media-playback-stop": "stop",
        "media-skip-forward": "next", "media-skip-backward": "previous", "zoom-in": "zoom-in", "zoom-out": "zoom-out",
        "zoom-fit-best": "fit", "window-minimize": "minus", "window-maximize": "square", "window-restore": "copy",
        "open-menu": "list", "pan-start": "left", "pan-end": "right", "pan-up": "up", "pan-down": "down",
        "object-select": "check", "process-stop": "error", "system-shutdown": "power", "system-lock-screen": "lock",
        "application-exit": "exit", "document-properties": "document-properties", "application-x-addon": "addon",
        "help-about": "help-about", "configure": "gear", "document-send": "send"}
    P.update({"left": "m15 3-9 9 9 9", "right": "m9 3 9 9-9 9", "up": "m3 15 9-9 9 9", "down": "m3 9 9 9 9-9",
              "save-as": "M2 2h17l3 3v7M2 2v20h8M6 2v7h11V2m-4 16 7-7 3 3-7 7-5 1Z",
              "plus": "M12 3v18M3 12h18", "minus": "M3 12h18", "square": "M3 3h18v18H3Z",
              "undo": "M8 3 2 9l6 6M2 9h13q7 0 7 6t-7 6", "redo": "m16 3 6 6-6 6m6-6H9q-7 0-7 6t7 6",
              "sort-up": "M2 19h12M2 12h8M2 5h4m11 2 3-4 3 4m-3-4v18",
              "sort-down": "M2 5h12M2 12h8M2 19h4m11-2 3 4 3-4m-3 4V3",
              "next": "m2 3 13 9-13 9Zm18 0v18", "previous": "m22 3-13 9 13 9ZM4 3v18",
              "zoom-in": P["search"] + "M6 10h8m-4-4v8", "zoom-out": P["search"] + "M6 10h8",
              "fit": "M3 9V3h6m6 0h6v6m0 6v6h-6m-6 0H3v-6"})
    for name, symbol in actions.items():
        if symbol == "home":
            write("actions", name, f'<g transform="translate(10 10) scale(1.83)"><path d="{P[symbol]}" fill="@ACTION_GLYPH@"/></g>')
        else:
            write("actions", name, f'<g transform="translate(10 10) scale(1.83)">{glyph(symbol, "@ACTION_GLYPH@", 2.4)}</g>')
        symbolic("actions", name, symbol)
    categories = dict(zip(
        "applications-accessories applications-development applications-games applications-graphics applications-internet applications-multimedia applications-office applications-system applications-utilities preferences-desktop preferences-system".split(),
        "briefcase code gamepad brush globe film document gear config monitor gear".split()))
    for i, (name, symbol) in enumerate(categories.items()):
        color = ["#759ae5", "#8e89db", "#64bca5", "#e6a86d"][i % 4]
        body = primitive("app", "plate").replace("@TOP@", color).replace("@BOTTOM@", "#283348")
        body += f'<g transform="translate(16 15) scale(1.33)">{glyph(symbol, "#f1f3f8", 2.4)}</g>'
        write("categories", name, body)
        symbolic("categories", name, symbol)
    emblems = dict(zip(
        "emblem-default emblem-favorite emblem-important emblem-readonly emblem-shared emblem-synchronizing emblem-symbolic-link emblem-unreadable emblem-downloads emblem-photos".split(),
        "check star warning lock share sync link error download image".split()))
    for name, symbol in emblems.items():
        body = '<circle cx="32" cy="32" r="26" fill="@EMBLEM_SURFACE@" stroke="@EMBLEM_BORDER@" stroke-width="2"/>'
        body += f'<g transform="translate(16 16) scale(1.33)">{glyph(symbol, "@EMBLEM_GLYPH@", 2.6)}</g>'
        write("emblems", name, body)
        symbolic("emblems", name, symbol)
    manifests = {"scalable/actions": {"view-grid": ["view-app-grid"], "view-list": ["view-list-details"],
        "open-menu": ["application-menu"], "window-close": ["dialog-close"], "edit-find": ["system-search"]},
        "symbolic/actions": {"view-grid-symbolic": ["view-app-grid-symbolic"], "view-list-symbolic": ["view-list-details-symbolic"],
        "open-menu-symbolic": ["application-menu-symbolic"], "window-close-symbolic": ["dialog-close-symbolic"],
        "edit-find-symbolic": ["system-search-symbolic"], "pan-end-symbolic": ["pan-start-symbolic-rtl"], "pan-start-symbolic": ["pan-end-symbolic-rtl"]}}
    for variant, suffix in (("scalable", ""), ("symbolic", "-symbolic")):
        action_aliases = {
            "go-forward": ["go-next"], "go-back": ["go-previous"],
            "view-grid": ["view-grid-large", "view-grid-small"],
            "view-list": ["view-list-bullet"], "edit-delete": ["user-trash-action"],
            "window-close": ["window-close-button"],
            "application-exit": ["system-log-out", "exit", "xfce4-session-logout"],
            "help-about": ["help-contents", "help-info"],
            "application-x-addon": ["preferences-plugin", "plugin"],
            "document-send": ["blueman-send", "mail-send"],
        }
        target = manifests[f"{variant}/actions"]
        for k, names in action_aliases.items():
            target.setdefault(k + suffix, []).extend(n + suffix for n in names)
        target = manifests.setdefault(f"{variant}/status", {})
        for level in range(0, 101, 10):
            state = "empty" if level == 0 else "caution" if level <= 10 else "low" if level <= 30 else "good" if level < 90 else "full"
            target.setdefault("battery-" + state + suffix, []).append(f"battery-level-{level}" + suffix)
            target.setdefault("battery-charging" + suffix, []).append(f"battery-level-{level}-charging" + suffix)
        target.setdefault("battery-full" + suffix, []).extend(n + suffix for n in ["battery-full-charged", "battery-level-100-charged"])
        status_aliases = {
            "network-wireless-signal-excellent": [
                "nm-signal-100", "network-wireless-100", "network-wifi", "wifi", "nm-device-wireless"
            ],
            "network-wireless-signal-good": [
                "network-wireless-connected", "network-wireless-acquiring", "nm-signal-75", "network-wireless-75"
            ],
            "network-wireless-signal-ok": [
                "nm-signal-50", "network-wireless-50"
            ],
            "network-wireless-signal-weak": [
                "nm-signal-25", "network-wireless-25"
            ],
            "network-wireless-offline": [
                "nm-signal-00", "network-wireless-0", "nm-no-connection", "network-wireless-disabled"
            ],
            "network-wired": ["network-wired-connected"],
            "bluetooth-active": [
                "bluetooth-acquiring", "blueman-tray", "blueman-active", "bluetooth-paired"
            ],
            "bluetooth-disabled": [
                "blueman-disabled", "bluetooth-disconnected"
            ],
        }
        for k, names in status_aliases.items():
            target.setdefault(k + suffix, []).extend(n + suffix for n in names)
        device_aliases = {
            "drive-harddisk": [
                "drive", "drive-harddisk-solidstate", "drive-harddisk-root", "drive-partition"
            ],
            "drive-removable-media": [
                "drive-removable-media-usb", "drive-removable-media-usb-pendrive", "drive-removable",
                "drive-harddisk-usb", "usbpendrive", "media-removable-usb", "media-usb"
            ],
            "media-flash": [
                "media-flash-sd", "media-flash-sd-mmc", "media-flash-memory-stick",
                "media-flash-smart-media", "media-memory"
            ],
        }
        target = manifests.setdefault(f"{variant}/devices", {})
        for k, names in device_aliases.items():
            target.setdefault(k + suffix, []).extend(n + suffix for n in names)
    save_aliases("generic", manifests)


def status_geometry(name, symbolic=True):
    color = "#2e3436" if symbolic else "@STATUS_GLYPH@"
    group = lambda s: f'<g color="{color}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{s}</g>'
    muted = any(k in name for k in ("muted", "offline", "disabled"))
    cross = '<path d="m10 10 4 4m0-4-4 4"/>' if muted else ''
    if name.startswith("network-wireless"):
        strength = 0 if muted else {"weak": 1, "ok": 2, "good": 3, "excellent": 4}[name.rsplit("-", 1)[-1]]
        arcs = ['<circle cx="8" cy="13" r="1" fill="currentColor" stroke="none"/>',
                '<path d="M5 10q3-3 6 0"/>', '<path d="M3 7q5-5 10 0"/>', '<path d="M1 4q7-6 14 0"/>']
        return group(''.join(arcs[:strength]) + (('<path d="M2 5q6-5 12 0" opacity=".35"/>' + cross) if muted else ''))
    if name.startswith("battery"):
        level = {"full": 10, "good": 7, "low": 4, "caution": 2, "empty": 0, "charging": 7}[name.split("-")[-1]]
        bar = f'<rect x="2.5" y="6" width="{level}" height="4" fill="currentColor" stroke="none"/>' if level else ''
        if name.endswith("charging"):
            bar = '<path d="m8 4-3 5h3l-1 3 4-5H8Z" fill="currentColor" stroke="none"/>'
        return group('<path d="M1 4.5h12v7H1ZM13 7h2v2h-2"/>' + bar)
    if name.startswith("audio-volume"):
        level = 0 if muted else {"low": 1, "medium": 2, "high": 3}[name.rsplit("-", 1)[-1]]
        arcs = ['<path d="M10 6q2 2 0 4"/>', '<path d="M12 4q4 4 0 8"/>', '<path d="M14 2q6 6 0 12"/>']
        return group('<path d="M1 6h3l4-4v12l-4-4H1Z" fill="currentColor" stroke="none"/>' + ''.join(arcs[:max(0, level-1)]) + cross)
    if name.startswith("user-"):
        symbol = {"available": "check", "away": "clock", "busy": "minus", "offline": "error"}[name.split("-")[-1]]
    elif name.startswith("dialog-"):
        symbol = {"information": "info", "warning": "warning", "error": "error", "question": "question"}[name.split("-")[-1]]
        circle = '<circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.2"/>' if symbol != "warning" else ''
        return f'<g color="{color}">{circle}<g transform="translate(3 3) scale(.4166667)">{glyph(symbol, width=3)}</g></g>' if circle else f'<g transform="translate(1 1) scale(.5833333)" color="{color}">{glyph(symbol, width=2.57)}</g>'
    else:
        symbol = "mic" if name.startswith("microphone") else "bluetooth" if name.startswith("bluetooth") else "lock" if name.endswith("vpn") else "ethernet"
    body = f'<g transform="translate(1 1) scale(.5833333)" color="{color}">{glyph(symbol, width=2.57)}</g>'
    return body + (group(cross) if muted else '')


def status_body(name):
    semantic = "@WARNING@" if name in {"battery-caution", "battery-low", "dialog-warning", "user-away"} else "@ERROR@" if name in {"dialog-error", "battery-empty", "user-busy"} else None
    geom = status_geometry(name, symbolic=False)
    if semantic:
        geom = geom.replace("@STATUS_GLYPH@", semantic)
    accent_dot = '' if semantic else '<circle cx="54" cy="52" r="2.5" class="ColorScheme-Highlight" fill="currentColor"/>'
    return '<rect x="5" y="5" width="54" height="54" rx="14" fill="@STATUS_SURFACE@"/>' + f'<g transform="translate(8 8) scale(3)">{geom}</g>' + accent_dot


if __name__ == "__main__":
    places()
    mimetypes()
    system_families()
