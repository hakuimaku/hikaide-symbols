# Technical documentation

Commands below run from the repository root. See [documentation index](README.md) for design, folder states, and QA.

## Build and install

Building the existing SVG sources requires Python 3.9 or newer and the Python standard library. Run these commands from the repository root:

```sh
python3 scripts/build.py
python3 scripts/validate.py
./scripts/install.sh
```

The build is written to `dist/Hikaide-Symbols/`. The installer copies it to `~/.icons/Hikaide-Symbols` and refreshes the icon cache when a GTK cache tool is available. No root access is needed.

Select **Hikaide-Symbols** in GNOME Tweaks, Xfce Appearance, or your desktop's icon theme selector. On GNOME, you can also run:

```sh
gsettings set org.gnome.desktop.interface icon-theme 'Hikaide-Symbols'
```

To use the XDG icon directory instead:

```sh
./scripts/install.sh --xdg
```

This installs to `$XDG_DATA_HOME/icons`, or `~/.local/share/icons` when that variable is unset. A custom directory can be selected with `--icons-dir /path/to/icons`.

To update an existing installation managed by these scripts:

```sh
python3 scripts/build.py
./scripts/install.sh --replace
```

`--replace` replaces the installed theme with the current build, including its accent and artwork. Preserve any installed customizations first. Use the same directory option you used during installation.

To uninstall, first select another icon theme, then run:

```sh
./scripts/uninstall.sh
# For an XDG installation:
./scripts/uninstall.sh --xdg
```

## Accent color

The theme has one editable accent. Special-folder glyphs share that color; application palettes and semantic warning/error colors remain fixed.

For a build-time accent, edit `src/theme/accent.json`, then rebuild and install:

```json
{"accent": "#5294E2"}
```

To recolor an installed theme, install [icon-accent](https://github.com/hakuimaku/icon-accent) and make it available on `PATH`:

```sh
icon-accent set '#AC7994' --theme Hikaide-Symbols
icon-accent restore Hikaide-Symbols
```

The included adapters delegate installed SVG changes to that tool:

```sh
./scripts/set-accent.py '#AC7994'
./scripts/detect-accent
./scripts/sync-accent
```

Detection reads supported GNOME or KDE desktop accent settings. On a standalone window manager, pass a color explicitly:

```sh
./scripts/sync-accent --color '#AC7994'
```

The adapters also accept `--icons-dir` when changing an installation outside the default lookup path. Synchronization runs when invoked; no background service is installed.

Symbolic icons use GTK foreground and semantic colors. Four symbolic icons also declare a runtime accent role for GTK versions that support it; older GTK renders their filled shapes with the foreground color. See the [design contract](DESIGN.md) for details.

## Coverage

| Family | Canonical scalable icons | Regular icon names, including aliases |
| --- | ---: | ---: |
| Places | 30 | 57 |
| File types | 50 | 197 |
| Devices | 27 | 43 |
| Status | 29 | 77 |
| Actions | 52 | 73 |
| Categories | 11 | 11 |
| Emblems | 10 | 10 |

Application icons are not custom-drawn; the theme inherits from `Adwaita,breeze,hicolor` so applications fall back to system and desktop icons cleanly.

There are also 159 canonical symbolic icons and optimized 16/24 px variants for folders and file types. The generated theme contains 528 SVG files and 721 relative symlink aliases: 1,249 SVG paths in total. These counts include size variants and aliases, rather than 1,249 distinct designs.

Coverage varies by installed applications. Run the local launcher scan after building:

```sh
python3 scripts/scan_desktop_icons.py
```

Missing names appear in `reports/uncovered-app-icons.txt`. Machine-specific reports and generated build output are gitignored; the curated [QA summary](QA.md) is included in the repository.

## Editing and validation

Editable SVGs live under `src/`, grouped by icon family. Shared geometry lives in `src/primitives/`, alias manifests in `src/aliases/`, and the accent setting in `src/theme/accent.json`. A normal build uses these sources directly.

To regenerate the original artwork from its Python drawing definitions, use `python3 scripts/generate_sources.py`. This requires PySide6 with QtSvg and **overwrites generated SVG sources and alias manifests**, including manual edits to those files.

To validate a build and run the test suite:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The checks cover theme structure, required names, SVG validity, aliases, deterministic output, installation guards, folder styling, and accent handling. Some integration checks require GTK/GIO, SVG rendering tools, and the external `icon-accent` command. Native GTK rendering and desktop testing details, dependencies, and remaining manual checks are recorded in the [QA summary](QA.md).

To regenerate the family preview sheets, install `rsvg-convert`, Pillow, and Fontconfig, then run:

```sh
python3 scripts/render_png.py
```

To create a deterministic release archive and SHA-256 checksum:

```sh
python3 scripts/package.py
```

The files are written to `dist/Hikaide-Symbols.tar.gz` and `dist/Hikaide-Symbols.tar.gz.sha256`. The archive preserves relative icon aliases and includes the project license and artwork provenance.
