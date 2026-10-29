# Technical documentation

Commands below run from the repository root. See [documentation index](README.md) for design, folder states, and QA.

## Build and install

Building the existing SVG sources requires Python 3.9 or newer and the Python standard library. Run these commands from the repository root:

```sh
python3 scripts/build.py
python3 scripts/validate.py
./scripts/install.sh
```

One build validates and writes `dist/Hikaide-Symbols/` and `dist/Hikaide-Symbols-Light/`. The installer stages both trees under `~/.icons` and refreshes the icon cache when a GTK cache tool is available. No root access is needed.

Select **Hikaide-Symbols** (dark) or **Hikaide-Symbols-Light** (light) in GNOME Tweaks, Xfce Appearance, or your desktop's icon theme selector. On GNOME, you can also run:

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

`--replace` replaces both installed themes with the current build, including its accent and artwork. Preserve any installed customizations first. Use the same directory option you used during installation.

To uninstall, first select another icon theme, then run:

```sh
./scripts/uninstall.sh
# For an XDG installation:
./scripts/uninstall.sh --xdg
```

## Accent color

Each appearance has one editable accent. Special-folder glyphs share that color; intentional category colors remain fixed, while warning/error colors retain their hues with readable light-mode luminance.

For a build-time accent, edit the `accent` object in `src/theme/palette.json` to the values below, leaving both neutral palettes intact, then rebuild and install:

```json
{"dark": "#5294E2", "light": "#2E65A3"}
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

The mutation adapters accept `--variant light` to select `Hikaide-Symbols-Light`; the default remains dark for compatibility. They update one explicit theme per invocation. HakuSpace owns accent-pair reconciliation and must update both themes when an accent changes, with rollback, before selecting a mode. Mode switches should only change the selected theme name.

The adapters also accept `--icons-dir` when changing an installation outside the default lookup path. Synchronization runs when invoked; no background service is installed.

Symbolic icons use GTK foreground and semantic colors. Four symbolic icons also declare a runtime accent role for GTK versions that support it; older GTK renders their filled shapes with the foreground color. See the [design contract](DESIGN.md) for details.

## Coverage

| Family | Canonical scalable icons | Regular icon names, including aliases |
| --- | ---: | ---: |
| Places | 30 | 57 |
| File types | 52 | 215 |
| Devices | 27 | 43 |
| Status | 29 | 77 |
| Actions | 52 | 73 |
| Categories | 11 | 11 |
| Emblems | 10 | 10 |

Application icons fall back to `Adwaita,breeze,hicolor` cleanly, with standalone system utilities lacking upstream icons (such as `hwloc`) provided directly.

There are also 159 canonical symbolic icons and optimized 16/24 px variants for folders and file types. Each generated theme contains 535 SVG files and 769 relative symlink aliases: 1,304 SVG paths in total. These counts include size variants and aliases, rather than 1,304 distinct designs.

Coverage varies by installed applications. Run the local launcher scan after building:

```sh
python3 scripts/scan_desktop_icons.py
```

Missing names appear in `reports/uncovered-app-icons.txt`. Machine-specific reports and generated build output are gitignored; the curated [QA summary](QA.md) is included in the repository.

## Editing and validation

Editable SVGs live under `src/`, grouped by icon family. Shared geometry lives in `src/primitives/`, alias manifests in `src/aliases/`, and semantic palettes and accents in `src/theme/palette.json`. Regular SVG paint tokens such as `@FOLDER_FRONT@` are resolved during builds; preview the built SVGs rather than unresolved source tokens. Symbolic source paints remain runtime-semantic.

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
python3 scripts/render_png.py --appearances
python3 scripts/runtime_test.py --isolated
python3 scripts/desktop_smoke.py
```

To create a deterministic release archive and SHA-256 checksum:

```sh
python3 scripts/package.py
```

An archive and SHA-256 sidecar are written for each theme: `dist/Hikaide-Symbols.tar.gz` and `dist/Hikaide-Symbols-Light.tar.gz`. The archive preserves relative icon aliases and includes the project license and artwork provenance.

## Managed appearance metadata

New builds carry `.hikaide-symbols.json` with exactly `family: "Hikaide-Symbols"`, `version: 2`, and `variant: "dark"|"light"`. The installer recognizes the exact v1 `.hikaide-symbols` marker only for dark-theme migration. It refuses unmanaged or symlinked targets before modifying either sibling. Cache generation and validation finish for both staged trees before replacement. Update, uninstall and build rename failures restore the previous pair; backups remain available if restoration itself fails.

The paired outputs are asset contracts for HakuSpace. This repository does not select GTK themes, write GNOME color-scheme preferences, extract wallpaper colors, or alter saved Hikai mode preferences.
