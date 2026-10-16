#!/usr/bin/env python3
"""Original vector interpretations of common app identities; no upstream artwork."""
import math
from draw_icons import glyph, lettering, primitive, symbolic, write, save_aliases


def path(d, fill, **attrs):
    return '<path d="' + d + '" fill="' + fill + '" ' + ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items()) + '/>'


def circle(x, y, r, color, **attrs):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" ' + ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items()) + '/>'


def rect(x, y, w, h, r, color, **attrs):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{color}" ' + ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items()) + '/>'


def grad(a, b, id="ink"):
    return f'<defs><linearGradient id="{id}" x2=".4" y2="1"><stop stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'


def plate(a, b):
    return primitive("app", "plate").replace("@TOP@", a).replace("@BOTTOM@", b)


def roundel(a, b):
    return grad(a, b) + circle(32, 33, 27, "#000", opacity=".2") + circle(32, 31, 27, "url(#ink)") + path("M12 18Q30-3 51 16", "none", stroke="#fff", stroke_opacity=".18", stroke_width="1")


def sign(symbol, color="#f2f5fc", x=16, y=15, scale=1.33):
    g = glyph(symbol, color, 2.4) if symbol in SYMBOLS else lettering(symbol, color)
    return f'<g transform="translate({x} {y}) scale({scale})">{g}</g>'


# Glyph lookup is separate from brand-specific paths below.
from draw_icons import P as SYMBOLS


def brand(name):
    if name == "hwloc":
        return (plate("#647f9c", "#30475f") +
                path("M32 24v16M16 40v-8h32v8", "none", stroke="#e6eef7", stroke_width="2.5", stroke_linejoin="round") +
                rect(23, 11, 18, 14, 3, "#d9e5ef") + rect(28, 15, 8, 6, 1, "#536e89") +
                rect(10, 39, 13, 13, 3, "#8bbee3") + rect(26, 39, 13, 13, 3, "#9ed4ba") +
                rect(42, 39, 13, 13, 3, "#b6b1e3"))
    if name in {"firefox", "librewolf", "floorp", "thunderbird"}:
        blue = "#63d5fb" if name == "librewolf" else "#a7a0ff" if name == "floorp" else "#429ef0" if name == "thunderbird" else "#9c50e8"
        orange = "#daefff" if name == "librewolf" else "#6b65c7" if name == "floorp" else "#2077d2" if name == "thunderbird" else "#ff9e24"
        out = grad(blue, "#4825a5") + circle(32, 33, 24, "url(#ink)")
        out += path("M18 8 20 19Q7 15 8 27C0 47 22 64 43 55 61 48 64 28 53 15l-1 15-9-12 3 16q-6-6-15-4l-9 7q8 10 20 3-7 19-25 8C3 38 14 30 22 28l8-8-9-2Z", orange)
        out += path("M12 31Q9 52 34 54 15 60 7 43Z", "#ee4668" if name == "firefox" else blue)
        if name == "thunderbird":
            out += rect(20, 26, 29, 20, 3, "#edf4fa") + path("m20 27 14 11 15-11", "none", stroke="#538fc0", stroke_width="2")
        return out
    if name in {"google-chrome", "chromium"}:
        a, b, c = ("#ed514d", "#f6cf45", "#24af70") if name == "google-chrome" else ("#9dd6fa", "#4c99d9", "#286eb4")
        return (circle(32, 33, 27, "#000", opacity=".18") + circle(32, 31, 27, a) +
                path("M32 31h27A27 27 0 0 1 18 55Z", b) + path("M32 31 18 55A27 27 0 0 1 8 17l14 23Z", c) +
                circle(32, 31, 13, "#f4f7fc") + grad("#50c7fc", "#1262d4") + circle(32, 31, 10.5, "url(#ink)"))
    if name == "brave-browser":
        return grad("#ff9e30", "#ee3f0d") + path("m17 5 5 2h20l5-2 10 12-4 27-21 16-21-16-4-27Z", "url(#ink)") + path("m21 16 11 4 11-4 7 7-8 14-4-4 3-7-6 2v9l6 7-9 7-9-7 6-7v-9l-6-2 3 7-4 4-8-14Z", "#fff4e9")
    if name == "vivaldi":
        return plate("#ff6266", "#d90a20") + circle(32, 31, 21, "#fff6f7") + path("M19 22 29 41q3 5 7 0l10-19", "none", stroke="#e32940", stroke_width="7", stroke_linecap="round")
    if name == "microsoft-edge":
        return grad("#36e2a4", "#087cbb") + path("M7 39C-3 8 40-9 56 14q12 24-14 28 12-13-1-20-14-7-22 9Z", "url(#ink)") + grad("#19b6ee", "#1740ab", "blue") + path("M7 28q8-13 28-9-15 3-14 15 6 19 34 9-6 18-29 16Q4 56 7 28Z", "url(#blue)") + path("M22 32q0 13 20 10-15 10-23-3Z", "#06448c")
    if name == "opera":
        return grad("#ff555e", "#d00030") + '<ellipse cx="32" cy="31" rx="25" ry="28" fill="url(#ink)"/>' + '<ellipse cx="34" cy="31" rx="13" ry="22" fill="#1c2330"/>' + path("M34 9q16-5 22 12-4-20-22-18Z", "#ff858c")
    if name == "zen-browser":
        return plate("#e8cfb2", "#9f836f") + path("M19 19h27L19 43h27M19 24h20M25 38h21", "none", stroke="#342d2b", stroke_width="3.2", stroke_linejoin="round")
    if name == "tor-browser":
        return roundel("#c18aec", "#5e3096") + path("M32 8q-22 15-18 31 4 17 18 17 15-1 18-17 4-15-18-31Z", "#e3c4f4") + path("M32 10q-13 28 0 45m0-45q14 28 0 45m0-45v45", "none", stroke="#9252bf", stroke_width="2") + path("m30 10 2-9 5 1-3 9Z", "#7eb15b")
    if name in {"code", "code-oss", "vscodium"}:
        color = "#258cda" if name != "vscodium" else "#539bc6"
        return grad("#36bcff", color) + path("m44 3 15 7v43l-15 8-27-22-9 8-6-4V20l6-4 9 8Zm0 14L23 32l21 16ZM8 25v13l8-6Z", "url(#ink)", fill_rule="evenodd") + path("M44 3v58l15-8V10Z", color)
    if name in {"jetbrains-idea", "jetbrains-pycharm", "jetbrains-webstorm", "jetbrains-clion", "jetbrains-rider", "android-studio"}:
        colors = {"jetbrains-idea": ("#ff4090", "#584cfa", "IJ"), "jetbrains-pycharm": ("#a4e936", "#25bcb3", "PY"),
                  "jetbrains-webstorm": ("#36e2ed", "#3477ec", "WS"), "jetbrains-clion": ("#28c793", "#2a94ea", "CL"),
                  "jetbrains-rider": ("#e94a78", "#af47ef", "RD"), "android-studio": ("#73dba0", "#3e8ccf", "A")}
        a, b, letters = colors[name]
        return grad(a, b) + path("M5 6h36l17 21-5 31-30 2L3 39Z", "url(#ink)") + path("M20 3 59 19 51 54 9 61 3 28Z", a, opacity=".5") + rect(13, 13, 39, 39, 1, "#11151f") + sign(letters, x=17, y=16, scale=1.3) + path("M20 45h14", "none", stroke="#f7f8fa", stroke_width="3")
    if name in {"neovim", "vim"}:
        return grad("#4ee1a3", "#138d70") + path("M9 4 49 49V4l9 9v39l-10 8L9 16v44l-8-8V13Z", "url(#ink)") + path("m9 4 10 10v38L9 60Z", "#3e89c7") + path("M49 4 58 13v39l-9 8Z", "#176d4b")
    if name == "sublime-text":
        return plate("#49515a", "#20252c") + path("m17 20 31-10v12l-19 6 19 5v12L17 55V43l20-6-20-5Z", "#ffa51e")
    if name == "cursor":
        return grad("#b6c0cb", "#5d6a7a") + path("m32 3 26 15v29L32 62 6 47V18Z", "url(#ink)") + path("m15 18 36 5-14 13-5 18-6-19Z", "#fafcff") + path("m26 35 11 1-5 18Z", "#9da7b5")
    if name in {"github-desktop", "git-gui"}:
        return roundel("#c47af3", "#613197") + path("M17 19 18 10l8 5q7-2 13 0l8-5 1 9q7 10-1 19-4 4-11 4v14h-8V44q-12 2-15-8l-6-4q3-6 8 1 4 6 9 3-12-3-12-12Z", "#faf6ff")
    if name == "zed":
        return plate("#f2f5f8", "#b9c8d7") + path("M17 19h30L17 44h30M17 24h23M24 39h23", "none", stroke="#273a4c", stroke_width="3")
    if name == "emacs":
        return roundel("#9d7ed8", "#5a448f") + path("M47 16Q4 10 23 28l13 7Q-2 49 44 49M23 28h20", "none", stroke="#e0c3ff", stroke_width="5", stroke_linecap="round")
    if name in {"notion", "typora", "zotero", "joplin", "standard-notes"}:
        a, b, label, fg = {"notion": ("#fff", "#d6d8dd", "N", "#191b21"), "typora": ("#fff", "#d7dee7", "T", "#374452"), "zotero": ("#f3f5f7", "#bbc3cf", "Z", "#d02934"), "joplin": ("#62a7ed", "#2250a3", "J", "#fff"), "standard-notes": ("#a292f2", "#6554b9", "N", "#fff")}[name]
        return plate(a, b) + (rect(12, 12, 40, 39, 2, "none", stroke="#1c2029", stroke_width="2") if name == "notion" else '') + sign(label, fg, 14, 13, 1.5)
    if name == "obsidian":
        return grad("#c09aff", "#5b31b9") + path("m34 3 16 11 8 24-17 23-25-7-9-19 10-23Z", "url(#ink)") + path("m34 3-7 24 14 34 1-30Z", "#9d6ce7") + path("m7 35 20-8-11 27Z", "#7150b6") + path("m42 31 16 7-8-24Z", "#cba4ff")
    if name.startswith("libreoffice-"):
        symbol, color = {"libreoffice-startcenter": ("document", "#419f64"), "libreoffice-writer": ("text", "#328bcb"), "libreoffice-calc": ("spreadsheet", "#38a064"), "libreoffice-impress": ("presentation", "#e58b44")}[name]
        return path("M12 4h29l12 12v43H12Z", color) + path("M15 7h23l12 12v37H15Z", "#e9eef3") + path("M41 4h12v12Z", color) + sign(symbol, color, 20, 24, 1)
    if name == "onlyoffice-desktopeditors":
        return path("m6 44 26-13 26 13-26 14Z", "#f24a46") + path("m6 31 26-13 26 13-26 14Z", "#f3cd35") + path("m6 18 26-13 26 13-26 14Z", "#27b7e4")
    if name in {"wps-office", "microsoft-office"}:
        return grad("#ff8b27", "#d61442") + path("m13 12 24-9 15 9v41l-15 8-24-10V20l12-4v30l12 5V13l-12 4Z", "url(#ink)")
    if name in {"discord", "vesktop"}:
        return grad("#8094ff", "#444de0") + path("M16 14 25 11l2 5h10l2-5 9 3q9 12 10 28l-13 9-5-6q6-2 8-5-16 9-32 0 2 4 8 5l-5 6-13-9q1-16 10-28Z", "url(#ink)") + circle(23, 31, 5, "#172345") + circle(41, 31, 5, "#172345")
    if name == "telegram":
        return roundel("#52d3ff", "#0486d2") + path("m12 29 41-16-8 38-13-10-7 7 1-14 19-16-24 16Z", "#f0f9ff") + path("m26 34 19-16-13 23-7 7Z", "#9dd6f2")
    if name in {"signal-desktop", "whatsapp"}:
        a, b = ("#4f9cff", "#2674e1") if name == "signal-desktop" else ("#55df98", "#149e65")
        return roundel(a, b) + path("M49 30a17 17 0 1 0-30 11l-5 9 11-4a17 17 0 0 0 24-16Z", "none", stroke="#f7fbff", stroke_width="2.4", stroke_dasharray="4 2" if name == "signal-desktop" else "none") + (path("M23 21q-5 14 15 22l6-6-6-4-3 4q-7-4-8-9l3-3-4-5Z", "#fff") if name == "whatsapp" else '')
    if name == "element":
        return roundel("#36dfb7", "#009776") + ''.join(path("M28 12q18-4 18 13", "none", stroke="#fff", stroke_width="5", stroke_linecap="round", transform=f"rotate({a} 32 32)") for a in (0, 120, 240))
    if name == "slack":
        return ''.join(rect(x, y, w, h, 4, c) for x, y, w, h, c in [(9, 24, 22, 9, "#36c5f0"), (23, 9, 9, 22, "#36c5f0"), (34, 9, 9, 22, "#2eb67d"), (35, 24, 22, 9, "#2eb67d"), (35, 35, 22, 9, "#ecb22e"), (35, 36, 9, 22, "#ecb22e"), (23, 36, 9, 22, "#e01e5a"), (9, 35, 22, 9, "#e01e5a")])
    if name in {"zoom", "teams"}:
        return plate("#5cb5ff" if name == "zoom" else "#9697ef", "#0e59e5" if name == "zoom" else "#454bb1") + (sign("video-camera", scale=1.5, x=13, y=13) if name == "zoom" else circle(44, 17, 6, "#b7b5fb") + rect(33, 27, 22, 22, 6, "#5a62c4") + rect(9, 17, 29, 31, 4, "#484cbb") + sign("T", x=11, y=18, scale=1))
    if name == "spotify":
        return roundel("#38ed88", "#00b453") + ''.join(path(d, "none", stroke="#072c1b", stroke_width=w, stroke_linecap="round") for d, w in [("M14 23q18-6 37 3", 5), ("M16 33q16-5 32 3", 4), ("M19 43q13-4 26 2", 3)])
    if name == "vlc":
        return grad("#ffb644", "#f36b12") + path("m7 50 8-5h34l8 5v8H7Z", "url(#ink)") + path("m28 4 9 0 15 49H12Z", "url(#ink)") + path("m24 17 16 0 3 9H21Zm-8 25 31 0-3-9H19Z", "#fff1db")
    if name in {"mpv", "celluloid"}:
        return (roundel("#ad80db", "#4e246e") + circle(32, 31, 20, "none", stroke="#d3b3ee", stroke_width="2") if name == "mpv" else plate("#6588f5", "#a03cad") + ''.join(circle(x, y, 2, "#edc1eb") for x in (12, 52) for y in (13, 31, 49))) + path("m25 19 20 12-20 12Z", "#fff")
    if name == "obs":
        return roundel("#42464c", "#111316") + circle(32, 31, 25, "none", stroke="#c7cdd4", stroke_width="1.5") + ''.join(path("M32 31C10 36 11 14 24 12c-5 7-1 15 8 19Z", "#ecf0f3", transform=f"rotate({a} 32 31)") for a in (0, 120, 240))
    if name == "gimp":
        return path("M7 20q17 8 42-9l6-8q7 30-10 43-14 12-34-1Q1 40 7 20Z", "#716a58") + '<ellipse cx="23" cy="30" rx="7" ry="9" fill="#f3eee5"/><ellipse cx="40" cy="26" rx="8" ry="10" fill="#f3eee5"/>' + circle(25, 31, 3, "#252b30") + circle(39, 27, 3, "#252b30") + path("M10 39q16 11 30-2", "none", stroke="#282e34", stroke_width="2.5") + path("m41 39 18 17-2 5-20-19Z", "#bf7734")
    if name in {"krita", "darktable", "rawtherapee"}:
        colors = ["#f1459d", "#f58342", "#f9d541", "#64c554", "#2dcde1", "#4269dd", "#8d4bdf"]
        out = ''
        for i, color in enumerate(colors):
            a, b = i*math.tau/7, (i+1)*math.tau/7
            out += path(f'M32 31  {32+26*math.cos(a):.3f} {31+26*math.sin(a):.3f} A26 26 0 0 1 {32+26*math.cos(b):.3f} {31+26*math.sin(b):.3f}Z', color)
        out += circle(32, 31, 11, "#28303b" if name != "krita" else "#f6c5df")
        if name == "krita":
            out += path("m10 6 40 45 5-3-41-45Z", "#262d36") + path("m48 47 7 2 4 10-10-5Z", "#d9af64")
        return out
    if name == "inkscape":
        return path("M32 3 59 39 46 46l-9-3-12 6-20-9Z", "#11161e") + path("m32 3 13 17-9-4-5 8-6-9-7 9Z", "#f0f2f5") + path("M15 49q8 10 20 3t15 1q-13 12-24 8Z", "#151b23")
    if name == "blender":
        return path("M29 8 45 20 60 30q8 24-19 29Q19 62 18 43L5 48 1 42l19-15H7v-7h23L21 12Z", "#f28c28") + '<ellipse cx="40" cy="38" rx="16" ry="13" fill="#f0f3f6"/>' + '<ellipse cx="40" cy="38" rx="11" ry="9" fill="#247fbd"/>' + '<ellipse cx="40" cy="38" rx="7" ry="6" fill="#1b334c"/>'
    if name == "figma-linux":
        return rect(13, 4, 19, 19, 9, "#f76c5e") + rect(32, 4, 19, 19, 9, "#ff9685") + rect(13, 23, 19, 19, 9, "#a26bf0") + circle(41.5, 32.5, 9.5, "#38b7ee") + path("M13 42h19v9a9.5 9.5 0 1 1-19-9Z", "#36ce94")
    if name == "godot":
        return path("m7 22 5-12 8 4 5-8 7 5 7-5 5 8 8-4 5 12-4 29q-21 14-43 0Z", "#5398c7") + circle(23, 30, 5, "#fff") + circle(42, 30, 5, "#fff") + circle(23, 30, 2.5, "#254867") + circle(42, 30, 2.5, "#254867") + path("M13 43h10v5h18v-5h10M32 33v7", "none", stroke="#e7f4fd", stroke_width="3")
    if name == "steam":
        return roundel("#315779", "#112437") + circle(43, 22, 12, "none", stroke="#e4eef8", stroke_width="4") + circle(43, 22, 7, "none", stroke="#e4eef8", stroke_width="2") + path("m6 37 18 9 15-14-6-8-12 15-15-7Z", "#e4eef8") + circle(24, 44, 7, "#315779", stroke="#e4eef8", stroke_width="2")
    if name in {"docker", "podman", "podman-desktop"}:
        a = "#259fee" if name == "docker" else "#b47ce1"
        return ''.join(rect(7+x*8, 12+y*8, 7, 7, 1, a) for x, y in [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (1, 1), (2, 1), (3, 1), (3, 0)]) + path("M3 37h47q6-5 7-13 9 8 1 13-4 23-30 23Q7 61 3 37Z", a) + circle(17, 43, 1.5, "#d9f4ff")
    if name == "wine":
        return path("M20 4h24l-2 24q-2 11-10 11t-10-11Z", "#e5e9ef") + path("M21 19q11-4 22 0l-1 9q-2 11-10 11t-10-11Z", "#b62d50") + path("M32 39v18m-10 2h20", "none", stroke="#cdd7e1", stroke_width="3", stroke_linecap="round")
    if name == "nextcloud":
        return circle(32, 31, 12, "none", stroke="#25b5f3", stroke_width="6") + circle(10, 31, 8, "none", stroke="#25b5f3", stroke_width="5") + circle(54, 31, 8, "none", stroke="#25b5f3", stroke_width="5")
    if name == "kubernetes":
        return grad("#559cff", "#2457cc") + path("m32 2 23 10 8 26-17 23H18L1 38l8-26Z", "url(#ink)") + circle(32, 31, 16, "none", stroke="#f5f8ff", stroke_width="2.6") + ''.join(path("M32 9v44", "none", stroke="#fff", stroke_width="2.6", transform=f"rotate({a} 32 31)") for a in (0, 51.43, 102.86, 154.29)) + circle(32, 31, 4, "#559cff")
    if name in {"kitty", "Alacritty", "foot", "wezterm", "com.mitchellh.ghostty", "utilities-terminal", "gnome-terminal", "org.gnome.Terminal", "konsole", "xterm"}:
        if name == "Alacritty":
            return plate("#34414a", "#182028") + path("m31 10-18 39 10-4 9-23 9 23 10 4-18-39Z", "#f28c64")
        if name == "kitty":
            return plate("#444b55", "#252b34") + path("M17 25 15 13l12 8h10l12-8-2 12q11 24-15 25-26-1-15-25Z", "#d6c09a") + circle(25, 33, 2, "#334354") + circle(39, 33, 2, "#334354") + path("m29 39 3 3 3-3", "#80664c")
        if name == "com.mitchellh.ghostty":
            return plate("#467cc1", "#254578") + path("M16 47V28q0-17 16-17t16 17v23l-7-5-7 5-8-5-10 5Z", "#f1f6ff") + circle(27, 29, 2.8, "#223a5f") + circle(38, 29, 2.8, "#223a5f")
        return plate("#454f59", "#171f27") + sign("terminal", "#b4e0af" if name == "foot" else "#cfb2f6" if name == "wezterm" else "#f2f5f8", 14, 16, 1.4)
    return None


# Apps without a separate brand drawing use a concrete object, not a generic initial tile.
CONCEPT_APPS = {
    "logseq": ("network", "#58b5d4", "#285b82"), "anki": ("star", "#77bee9", "#2a5191"),
    "calibre": ("book", "#e2a34e", "#825121"), "evolution": ("mail", "#8bb8dc", "#3c658d"),
    "fractal": ("chat", "#b587eb", "#7041ae"), "mattermost": ("chat", "#4c9ce7", "#2055a5"),
    "audacious": ("A", "#a8aeb7", "#555e6a"), "rhythmbox": ("speaker", "#d0d8e2", "#828e9f"),
    "amberol": ("music", "#f1b56a", "#bd6b3e"), "lollypop": ("disc", "#d998e8", "#8b429d"),
    "kdenlive": ("film", "#5da5e9", "#315cb0"), "shotcut": ("film", "#48b5d8", "#175b88"),
    "handbrake": ("video-camera", "#b5d77b", "#458151"), "pitivi": ("film", "#c19bde", "#686099"),
    "easyeffects": ("wave", "#8f9cf0", "#5159a7"), "pavucontrol": ("config", "#78aeea", "#3e65a5"),
    "digikam": ("camera", "#6ba9ed", "#315f9e"), "scribus": ("pen", "#62b5e2", "#3063a6"),
    "freecad": ("gear", "#e17c77", "#a83c43"), "openscad": ("cube", "#efbd47", "#b58b24"),
    "org.gnome.Nautilus": ("folder", "#6cc6ff", "#257ed0"), "dolphin": ("folder", "#6bbce6", "#2d70ac"),
    "thunar": ("folder", "#afc7de", "#54718f"), "nemo": ("folder", "#9ccc84", "#558644"),
    "pcmanfm": ("folder", "#7da8d6", "#3d6eaa"), "pcmanfm-qt": ("folder", "#88bdea", "#3a81b5"),
    "caja": ("folder", "#b0c586", "#668246"), "org.gnome.Settings": ("gear", "#d1d9e2", "#7f8c9e"),
    "systemsettings": ("config", "#b7c7dc", "#607991"), "gnome-system-monitor": ("chart", "#88d7ac", "#267057"),
    "plasma-systemmonitor": ("chart", "#8cbfe4", "#3d7099"), "gnome-disks": ("drive", "#c9d5df", "#7d8c9d"),
    "gparted": ("drive", "#afd280", "#638c3d"), "baobab": ("pie", "#efa063", "#b65640"),
    "gnome-software": ("briefcase", "#7cb9f1", "#2e6ec6"), "org.kde.discover": ("briefcase", "#71c1e8", "#3074ae"),
    "pamac-manager": ("box", "#78cbb9", "#307e6b"), "timeshift": ("clock", "#91c7a1", "#3c825c"),
    "bleachbit": ("brush", "#89b4ed", "#3b6aa7"), "org.gnome.Calculator": ("calculator", "#a5b8cc", "#576d86"),
    "kcalc": ("calculator", "#87b8df", "#3f7ba8"), "org.gnome.TextEditor": ("pen", "#b1c7dc", "#6385a5"),
    "kate": ("pen", "#89bcea", "#366fa7"), "gedit": ("pen", "#d6b296", "#916447"),
    "loupe": ("image", "#96baf2", "#496caf"), "eog": ("eye", "#9ac9e2", "#4a829f"),
    "org.gnome.FileRoller": ("archive", "#dfa977", "#9d6735"), "ark": ("archive", "#9fbce0", "#547ea7"),
    "gnome-screenshot": ("select", "#b8c9d9", "#647f98"), "flameshot": ("camera", "#e78489", "#ab4257"),
    "keepassxc": ("key", "#93c987", "#4c8a4a"), "bitwarden": ("shield", "#6c9eeb", "#315eb5"),
    "seahorse": ("key", "#dfbd7a", "#a17b3f"), "copyq": ("clipboard", "#89c7b7", "#3e8876"),
    "networkmanager": ("wifi", "#75c4ec", "#3178ae"), "nm-connection-editor": ("globe", "#78b6e7", "#346d9d"),
    "blueman": ("bluetooth", "#75b8f0", "#2e69bb"), "filezilla": ("F", "#e37a77", "#ad3944"),
    "transmission": ("download", "#db8c85", "#a34348"), "qbittorrent": ("download", "#7caef1", "#3f6ab7"),
    "deluge": ("download", "#78c0ec", "#387eae"), "syncthing": ("sync", "#82c2e2", "#3785ae"),
    "remmina": ("remote", "#83b3dc", "#3f729e"), "wireshark": ("wave", "#7aa8e1", "#3e66a4"),
    "lutris": ("gamepad", "#edb764", "#b47a32"), "heroic": ("shield", "#7ac6e9", "#3675ad"),
    "bottles": ("archive", "#7bbbd4", "#396e9e"), "protonup-qt": ("P", "#a5adcb", "#5c638c"),
    "prismlauncher": ("diamond", "#d29ee4", "#735baa"), "minecraft": ("cube", "#8fc36a", "#5e7c3e"),
    "virt-manager": ("monitor", "#8cb7dc", "#4a749d"), "virtualbox": ("cube", "#8ec0e7", "#417aaf"),
    "gnome-boxes": ("cube", "#a4c5e2", "#5c83ad"), "qemu": ("chip", "#e5a269", "#aa693b"),
    "org.gnome.Calendar": ("calendar", "#e79d98", "#ba5c66"), "org.gnome.Contacts": ("users", "#a3b8da", "#5a789e"),
    "org.gnome.Clocks": ("clock", "#bacbde", "#6e859d"), "org.gnome.Weather": ("sun", "#edc974", "#c39542"),
    "org.gnome.Maps": ("map", "#a5c9ac", "#61876a"), "org.gnome.Characters": ("A", "#c3b0db", "#81619e"),
    "org.gnome.Logs": ("list", "#b7c4d1", "#6c7c91"), "org.gnome.Connections": ("remote", "#89c5d5", "#427e95"),
    "org.gnome.Extensions": ("chip", "#9ac78c", "#557e44"), "org.gnome.Tweaks": ("config", "#afbfcc", "#607c91"),
    "org.gnome.Evince": ("document", "#e1ab83", "#a96f47"), "org.gnome.SimpleScan": ("scanner", "#b4cbd6", "#688695"),
    "org.gnome.SoundRecorder": ("mic", "#dd9f9b", "#a35e65"), "org.kde.okular": ("document", "#83b6dc", "#3e78a0"),
    "org.kde.gwenview": ("image", "#a9c79e", "#63875c"), "org.kde.spectacle": ("camera", "#89b5df", "#446f9e"),
    "org.kde.kdeconnect": ("phone", "#7cbfd5", "#3d7e9d"),
    "localsend": ("share", "#f4b775", "#bc7c38"), "waydroid": ("phone", "#8ecb8c", "#438653"),
    "btop": ("chart", "#ab9ee0", "#665298"), "CMakeSetup": ("cube", "#ce9b99", "#934e58"),
    "nwg-look": ("brush", "#b4c7e0", "#6889b2"), "rofi": ("grid", "#94bddb", "#4c779b"),
    "fcitx": ("keyboard", "#a4c9df", "#557f9f"), "gammastep": ("sun", "#e3b887", "#a87946"),
    "antigravity": ("A", "#b8a4e0", "#5b4d91"), "kolourpaint": ("brush", "#a0cbb0", "#578361"),
}


ALIASES = {
    "firefox": "firefox-esr org.mozilla.firefox org.mozilla.Firefox", "google-chrome": "google-chrome-stable com.google.Chrome",
    "chromium": "chromium-browser org.chromium.Chromium", "brave-browser": "brave brave-browser-stable com.brave.Browser",
    "vivaldi": "vivaldi-stable com.vivaldi.Vivaldi", "microsoft-edge": "microsoft-edge-stable com.microsoft.Edge",
    "opera": "com.opera.Opera", "librewolf": "io.gitlab.librewolf-community", "floorp": "one.ablaze.floorp",
    "zen-browser": "zen app.zen_browser.zen", "tor-browser": "torbrowser torbrowser-launcher org.torproject.torbrowser-launcher",
    "utilities-terminal": "terminal org.gnome.Console kgx", "Alacritty": "alacritty org.alacritty.Alacritty",
    "kitty": "kitty-open", "foot": "footclient foot-server", "wezterm": "org.wezfurlong.wezterm",
    "com.mitchellh.ghostty": "ghostty", "konsole": "org.kde.konsole",
    "code": "vscode visual-studio-code com.visualstudio.code com.microsoft.VSCode", "code-oss": "codeoss",
    "vscodium": "codium com.vscodium.codium", "zed": "dev.zed.Zed zeditor", "cursor": "cursor-ai co.anysphere.cursor",
    "jetbrains-idea": "idea intellij-idea-ultimate intellij-idea-community com.jetbrains.IntelliJ-IDEA-Community com.jetbrains.IntelliJ-IDEA-Ultimate",
    "jetbrains-pycharm": "pycharm pycharm-community pycharm-professional com.jetbrains.PyCharm-Community com.jetbrains.PyCharm-Professional",
    "jetbrains-webstorm": "webstorm com.jetbrains.WebStorm", "jetbrains-clion": "clion com.jetbrains.CLion",
    "jetbrains-rider": "rider com.jetbrains.Rider", "sublime-text": "sublime_text com.sublimetext.three",
    "neovim": "nvim io.neovim.nvim", "vim": "gvim vim.gvim", "emacs": "emacsclient org.gnu.emacs",
    "github-desktop": "io.github.shiftey.Desktop", "android-studio": "com.google.AndroidStudio",
    "libreoffice-startcenter": "libreoffice org.libreoffice.LibreOffice", "libreoffice-writer": "writer",
    "libreoffice-calc": "calc", "libreoffice-impress": "impress", "onlyoffice-desktopeditors": "onlyoffice org.onlyoffice.desktopeditors",
    "wps-office": "wps-office-wps wps-office-et wps-office-wpp", "notion": "notion-app notion-desktop",
    "obsidian": "md.obsidian.Obsidian", "typora": "io.typora.Typora", "zotero": "org.zotero.Zotero",
    "logseq": "com.logseq.Logseq", "joplin": "net.cozic.joplin_desktop", "standard-notes": "standardnotes org.standardnotes.standardnotes",
    "anki": "net.ankiweb.Anki", "calibre": "com.calibre_ebook.calibre", "discord": "com.discordapp.Discord",
    "vesktop": "dev.vencord.Vesktop", "telegram": "telegram-desktop org.telegram.desktop",
    "signal-desktop": "signal org.signal.Signal", "element": "element-desktop im.riot.Riot",
    "slack": "com.slack.Slack", "zoom": "Zoom us.zoom.Zoom", "teams": "teams-for-linux com.github.IsmaelMartinez.teams_for_linux",
    "thunderbird": "org.mozilla.Thunderbird", "evolution": "org.gnome.Evolution", "fractal": "org.gnome.Fractal",
    "mattermost": "mattermost-desktop com.mattermost.Desktop", "whatsapp": "whatsapp-desktop",
    "spotify": "com.spotify.Client", "vlc": "org.videolan.VLC", "mpv": "io.mpv.Mpv",
    "celluloid": "io.github.celluloid_player.Celluloid", "audacious": "org.atheme.audacious",
    "rhythmbox": "org.gnome.Rhythmbox", "amberol": "io.bassi.Amberol", "lollypop": "org.gnome.Lollypop",
    "obs": "obs-studio com.obsproject.Studio", "kdenlive": "org.kde.kdenlive", "shotcut": "org.shotcut.Shotcut",
    "handbrake": "ghb fr.handbrake.ghb", "pitivi": "org.pitivi.Pitivi", "easyeffects": "com.github.wwmm.easyeffects",
    "pavucontrol": "org.pulseaudio.pavucontrol", "gimp": "org.gimp.GIMP", "krita": "org.kde.krita",
    "inkscape": "org.inkscape.Inkscape", "blender": "org.blender.Blender", "darktable": "org.darktable.Darktable",
    "rawtherapee": "com.rawtherapee.RawTherapee", "digikam": "org.kde.digikam", "scribus": "net.scribus.Scribus",
    "freecad": "FreeCAD org.freecad.FreeCAD", "openscad": "org.openscad.OpenSCAD", "figma-linux": "figma io.github.Figma_Linux.figma_linux",
    "godot": "godot4 org.godotengine.Godot", "org.gnome.Nautilus": "nautilus system-file-manager",
    "dolphin": "org.kde.dolphin", "thunar": "Thunar org.xfce.thunar", "nemo": "nemo-folder",
    "pcmanfm": "pcmanfm-folder", "pcmanfm-qt": "pcmanfm-qt-folder", "caja": "caja-folder",
    "org.gnome.Settings": "gnome-control-center", "gnome-system-monitor": "org.gnome.SystemMonitor",
    "plasma-systemmonitor": "org.kde.plasma-systemmonitor", "gnome-disks": "org.gnome.DiskUtility gnome-disk-utility",
    "gparted": "gpartedbin org.gnome.GParted org.kde.partitionmanager partitionmanager",
    "baobab": "org.gnome.baobab org.kde.filelight filelight", "gnome-software": "org.gnome.Software",
    "pamac-manager": "system-software-install", "timeshift": "timeshift-gtk", "bleachbit": "org.bleachbit.BleachBit",
    "org.gnome.Calculator": "gnome-calculator accessories-calculator", "kcalc": "org.kde.kcalc",
    "org.gnome.TextEditor": "text-editor", "kate": "org.kde.kate", "gedit": "org.gnome.gedit",
    "loupe": "org.gnome.Loupe", "eog": "org.gnome.eog", "org.gnome.FileRoller": "file-roller",
    "ark": "org.kde.ark", "gnome-screenshot": "org.gnome.Screenshot", "flameshot": "org.flameshot.Flameshot",
    "keepassxc": "org.keepassxc.KeePassXC", "bitwarden": "com.bitwarden.desktop", "seahorse": "org.gnome.seahorse",
    "copyq": "com.github.hluk.copyq", "networkmanager": "nm-applet", "nm-connection-editor": "preferences-system-network",
    "blueman": "blueman-manager blueman-adapters", "filezilla": "org.filezillaproject.Filezilla",
    "transmission": "transmission-gtk com.transmissionbt.Transmission", "qbittorrent": "org.qbittorrent.qBittorrent",
    "deluge": "deluge-gtk org.deluge_torrent.deluge", "nextcloud": "Nextcloud com.nextcloud.desktopclient.nextcloud",
    "syncthing": "syncthing-gtk me.kozec.syncthingtk", "remmina": "org.remmina.Remmina",
    "wireshark": "org.wireshark.Wireshark", "steam": "com.valvesoftware.Steam", "lutris": "net.lutris.Lutris",
    "heroic": "heroic-games-launcher com.heroicgameslauncher.hgl", "bottles": "com.usebottles.bottles",
    "wine": "wine-winecfg winecfg winetricks", "protonup-qt": "net.davidotek.pupgui2", "prismlauncher": "org.prismlauncher.PrismLauncher",
    "minecraft": "minecraft-launcher com.mojang.Minecraft", "docker": "docker-desktop com.docker.docker",
    "podman-desktop": "io.podman_desktop.PodmanDesktop", "virt-manager": "virt-viewer remote-viewer",
    "virtualbox": "virtualbox-vbox OracleVMVirtualBox", "gnome-boxes": "org.gnome.Boxes", "qemu": "qemu-system-x86_64",
    "org.gnome.Calendar": "gnome-calendar", "org.gnome.Contacts": "gnome-contacts", "org.gnome.Clocks": "gnome-clocks",
    "org.gnome.Weather": "gnome-weather", "org.gnome.Maps": "gnome-maps", "org.gnome.Characters": "gnome-characters",
    "org.gnome.Logs": "gnome-logs", "org.gnome.Connections": "gnome-connections", "org.gnome.Extensions": "org.gnome.Extensions.desktop gnome-extensions",
    "org.gnome.Tweaks": "gnome-tweaks", "org.gnome.Evince": "evince org.gnome.Papers", "org.gnome.SimpleScan": "simple-scan",
    "org.gnome.SoundRecorder": "gnome-sound-recorder", "org.kde.okular": "okular", "org.kde.gwenview": "gwenview",
    "org.kde.spectacle": "spectacle", "org.kde.kdeconnect": "kdeconnect kdeconnect-indicator",
    "localsend": "org.localsend.localsend_app", "waydroid": "waydroid-launcher", "btop": "htop",
    "nwg-look": "preferences-desktop-theme", "fcitx": "fcitx5 fcitx-lotus", "gammastep": "gammastep-indicator",
}


def apps():
    names = (
        "firefox google-chrome chromium brave-browser vivaldi microsoft-edge opera librewolf floorp zen-browser tor-browser "
        "utilities-terminal gnome-terminal org.gnome.Terminal konsole kitty Alacritty foot wezterm com.mitchellh.ghostty xterm "
        "code code-oss vscodium zed jetbrains-idea jetbrains-pycharm jetbrains-webstorm jetbrains-clion jetbrains-rider sublime-text neovim vim emacs cursor github-desktop "
        "libreoffice-startcenter libreoffice-writer libreoffice-calc libreoffice-impress onlyoffice-desktopeditors wps-office microsoft-office notion obsidian typora zotero logseq joplin standard-notes anki calibre "
        "discord vesktop telegram signal-desktop element slack zoom teams thunderbird evolution fractal mattermost whatsapp "
        "spotify vlc mpv celluloid audacious rhythmbox amberol lollypop obs kdenlive shotcut handbrake pitivi easyeffects pavucontrol "
        "gimp krita inkscape blender darktable rawtherapee digikam scribus freecad openscad figma-linux godot "
        "org.gnome.Nautilus dolphin thunar nemo pcmanfm pcmanfm-qt caja org.gnome.Settings systemsettings gnome-system-monitor plasma-systemmonitor gnome-disks gparted baobab gnome-software org.kde.discover pamac-manager timeshift bleachbit "
        "org.gnome.Calculator kcalc org.gnome.TextEditor kate gedit loupe eog org.gnome.FileRoller ark gnome-screenshot flameshot keepassxc bitwarden seahorse copyq "
        "networkmanager nm-connection-editor blueman filezilla transmission qbittorrent deluge nextcloud syncthing remmina wireshark "
        "steam lutris heroic bottles wine protonup-qt prismlauncher minecraft docker podman podman-desktop virt-manager virtualbox gnome-boxes qemu kubernetes "
        "android-studio org.gnome.Calendar org.gnome.Contacts org.gnome.Clocks org.gnome.Weather org.gnome.Maps org.gnome.Characters org.gnome.Logs org.gnome.Connections org.gnome.Extensions org.gnome.Tweaks org.gnome.Evince org.gnome.SimpleScan org.gnome.SoundRecorder org.kde.okular org.kde.gwenview org.kde.spectacle org.kde.kdeconnect "
        "localsend waydroid btop CMakeSetup nwg-look rofi fcitx gammastep antigravity kolourpaint hwloc").split()
    for name in names:
        body = brand(name)
        if body is None:
            symbol, a, b = CONCEPT_APPS[name]
            body = plate(a, b) + sign(symbol)
        write("apps", name, body)
    # Common app concepts for GTK: native monochrome geometry, never desaturated logos.
    for name, symbol in {"utilities-terminal": "terminal", "system-file-manager": "folder", "accessories-calculator": "calculator",
                         "preferences-system": "gear", "text-editor": "pen", "web-browser": "globe", "multimedia-player": "play",
                         "help-browser": "question", "org.gnome.Nautilus": "folder", "org.gnome.Settings": "gear",
                         "org.gnome.Calculator": "calculator", "org.gnome.TextEditor": "pen"}.items():
        symbolic("apps", name, symbol)
    save_aliases("apps", {"scalable/apps": {k: v.split() for k, v in ALIASES.items()}})


if __name__ == "__main__":
    apps()
