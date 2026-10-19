# Hikaide-Symbols — QA, 2026-10-16

The implementation covers all eight icon families. Build, validation and native GTK
checks pass. The current suite runs 11 tests: 10 pass and the external accent
change/restore test is skipped because `icon-accent` is not currently installed. Interactive desktop acceptance is only partially exercised; the
unchecked session tests below are not claimed as passed.

## Delivered coverage

| Family | Canonical scalable SVG files | Resolved regular names including aliases |
| --- | ---: | ---: |
| Places | 30 | 57 |
| Mimetypes | 50 | 197 |
| Devices | 27 | 27 |
| Status | 29 | 77 |
| Actions | 52 | 73 |
| Categories | 11 | 11 |
| Emblems | 10 | 10 |

Applications fall back to `Adwaita,breeze,hicolor` via theme inheritance.

Additionally: 159 canonical symbolic SVGs, 16/24 px optimized places/mimetypes,
689 relative symlink aliases across all directories. The installable tree has
528 regular SVG files and 1,217 SVG paths in total. File counts include size
variants and reused concepts; they are not a count of distinct designs.

The frozen [required-icon fixture](../tests/required-icons.json) covers all
29 places, 88 mimetypes, 27 devices, 29 statuses,
39 actions, 11 categories and 10 emblems tracked by the required-icon fixture.

## Checks run

| Check | Result and evidence |
| --- | --- |
| Build + validation | PASS: correct index, declared directories, hicolor inheritance, XML/viewBox, safe paint references, aliases, collisions, no raster/filter/script/external resource, no unresolved token |
| Unit/integration suite | PASS: 10 tests; 1 external accent test skipped (CLI unavailable); `python3 -m unittest discover -s tests -v` |
| Determinism | PASS: full build file hashes/symlinks identical on repeat; two archives byte-identical |
| Installation | PASS: clean install, update, cache creation, alias preservation, uninstall in temporary user-owned directory |
| Destructive-operation guards | PASS: unmanaged directory and symlink refused; unrelated test file preserved; repeat install requires `--replace` |
| Native GTK3 | PASS: 3.24.52, 3,195 lookups at 16/24/32/48/64 px, canonical regular and all symbolic rendering, scale-2 lookup and 64 px pixbuf, foreground recoloring |
| Native GTK4 | PASS: 4.24.1, same 3,195 lookups, regular/symbolic rendering, scale-2 lookup, foreground recoloring, GPA runtime accent A/B |
| hicolor fallback | PASS: both GTK versions resolve a sentinel that exists only in a temporary hicolor theme |
| GTK3/4 file chooser | PASS: actual `Gtk.FileChooserWidget` construction with the process theme; no interactive chooser flow asserted |
| Settings icon | PASS: actual GTK image widget constructed with `preferences-system`; no desktop settings application review asserted |
| Nautilus + Thunar | PASS: both start and remain alive for four seconds under private Broadway/D-Bus, GTK query confirms Hikaide-Symbols; startup smoke only |
| MIME naming | PASS: 13 real files queried by `xdg-mime`, GIO icon names resolve into this theme |
| Accent contract | Earlier baseline PASS (not rerun; CLI currently unavailable): external installed icon-accent detects exactly one editable accent; 139 eligible SVG files; 165 symbolic targets, 4 with GPA accent |
| Accent A → B → restore | Earlier baseline PASS; current test skipped (CLI unavailable): all eligible SVGs change only the highlight declaration; fixed artwork and all other SVGs stay unchanged; repeat set is idempotent; original bytes and symlinks restored |
| Desktop accent adapters | PASS: strict manual input, KDE RGB fixture, GNOME named-color fixture; standalone WM with no explicit color fails safely |
| Preview review | Rendered eight contact sheets at all five target sizes on dark/light surfaces; inspected places, mimetypes, status, app overview and native GTK4 sheet |
| Provenance | Original paths only; no imported third-party art. MIT license and provenance included in theme archive |

GTK3 initially discarded stroke-only symbolics. Sources were corrected to filled
outlines, and the final native tests pass. GTK4 runtime accent requires the
`gpa:version="1"` opt-in alongside the accent paint role; the final tests check
that changing only the fifth symbolic color changes the rendered accent shape.

Evidence (raw JSON/text reports are generated locally and are not committed):

- Native GTK report: `runtime-gtk.json`; [GTK3 rendering](../previews/runtime-gtk3.png), [GTK4 rendering](../previews/runtime-gtk4.png)
- File-manager startup diagnostics: `desktop-smoke.json`
- MIME audit: `mimetype-audit.json`; desktop icon scan: `desktop-icons.json`; uncovered app report: `uncovered-app-icons.txt`
- icon-accent inspection: `accent-inspection.json`
- [App overview](../previews/overview-apps.png), [folders](../previews/preview-places.png), [files](../previews/preview-mimetypes.png)

The isolated Nautilus smoke session logs unavailable desktop portal/network
services; Thunar logs missing optional thumbnailer plugins on this machine.
These are retained in diagnostics. The smoke test does not establish that those
services work or that every file-manager window was visually reviewed.

## Local coverage and remaining manual checks

The machine runs Niri. Scanner found 116 desktop entries, including 61 visible
launchers: 58 entries overall and 42 visible launchers resolve within this theme.
Missing local applications are deliberately reported rather than assigned an
unrelated branded icon. Absolute `Icon=` paths bypass theme lookup.

No system/user Flatpak export directory exists here. Common Flatpak IDs resolve
as theme aliases and a scanner Flatpak-ID fixture passes, but actual Flatpak
launchers/sandboxes have not been tested.

Still to check in a real selected desktop session:

- Full browsing, file properties and chooser interaction in Nautilus/Thunar.
- Launcher, tray and settings application visual review with the theme selected.
- Logout/login persistence and application cache refresh after changing themes.
- GNOME session accent change through the real settings service.
- Plasma runtime Highlight interpretation and accent-source detection.
- Actual Flatpak integration and physical HiDPI monitor behavior.

After the user selected the theme, the revised flat folder artwork was installed
to `~/.icons/Hikaide-Symbols` and its icon cache refreshed. The update checked
that no custom artwork, accent, aliases or extra files would be overwritten.
GTK runtime test settings remain process-local; no global selection setting,
system icon or desktop file was changed.

## Installable artifact

`dist/Hikaide-Symbols.tar.gz` — 73,013 bytes at this build.

SHA-256:

```text
4be185e113804a88f42c0b26b79d80e4b97f9f198f8e518f47844261ece39703
```

The matching `.sha256` file is next to the archive. The package contains only
the installable theme, ownership marker, license and provenance. Mockups,
machine-specific reports and preview PNGs are not bundled.

## Folder states and drag acceptance

Removed the upper-right link dot and the hidden tab lettering. Legacy
`folder-link`, `folder-hidden` and `folder-hidden-link` names are now relative
aliases of the plain folder, including symbolic names. No hidden lettering
primitive remains in the source tree.

Added `folder-drag-accept` aliases to `folder-open` in scalable, 16 px, 24 px
and symbolic directories. The open artwork has a flat dark interior and a
sloped front flap. Open symbolic geometry also differs from the closed folder.
All regular folders retain their large silhouette, flat colors and solid dark
lower-right triangle. Special-folder glyphs retain the shared accent.

Regression checks render open and closed states at 16/24/32/48/64 px and verify
that drag acceptance resolves to the open artwork. Native GTK3 and GTK4 also
render both regular and symbolic drop states, assert equality with the open
state and inequality with the closed state, and resolve them within this theme.
Both full native runs pass with 3,195 lookups per GTK version.

Updated 20 folder paths in the installed theme and refreshed the GTK icon cache.
The update compared existing artwork against the previous sources, validated
the installed result, and checked fingerprints of every unrelated file. The
installed accent `#6d85ae` and all unrelated files were preserved. Native GTK3/4
lookup of the installed drag-accept names is checked separately.

Interactive dragging in Nautilus/Thunar has not been exercised in this update.
The file managers decide when to request an open/drop icon and retain control
of their native link emblems and hidden-item opacity.

See the [folder preview](../previews/preview-places.png),
[state preview](../previews/folder-states.png), and
[folder-state notes](FOLDER_STATES.md).

## Hardware Locality lstopo icon fix

The installed `/usr/share/applications/lstopo.desktop` requests `Icon=hwloc`,
but no hwloc artwork was present in the theme or the installed hwloc package.
Added an original CPU/topology SVG under that exact name and included it in
the authoring generator. The launcher scanner regression fixture now checks
this case. The original fix passed all ten tests. Native GTK lookup and rendering pass at
16/24/32/64/128 px, and the installed theme resolves and renders it at 32 px.
Only the new app asset and icon cache were written to the installed theme;
existing icons, accent and desktop files were preserved. The launcher UI
itself was not reopened or inspected. See [icon preview](../previews/hwloc.png).

## Tray status, context menu actions, home, archive, and app fallback updates

1. **Missing Tray & Context Menu Icons (fixing black/purple checkerboard glitch)**:
   - Fcitx5 and Blueman menus request standard action names (`application-exit`, `document-properties`, `application-x-addon`, `help-about`, `configure`, `document-send`) that were previously absent from the actions family, resulting in unrendered icons. Added canonical SVGs in `scalable/actions` and `symbolic/actions` along with aliases (`system-log-out`, `exit`, `preferences-plugin`, `plugin`, `help-contents`, `blueman-send`).
   - Added tray status aliases for `nm-applet` (`nm-signal-00` through `nm-signal-100`, `network-wifi`, `nm-device-wireless`) and `blueman-tray` (`blueman-tray`, `blueman-active`, `blueman-disabled`) in both `scalable/status` and `symbolic/status`.
2. **HOME Icon Geometry**:
   - Replaced hollow double-line stroke outline with a solid filled silhouette house featuring a cutout doorway, matching the design in `docs/mockups/Bảng biểu tượng thư mục tối hiện đại.png`. Updated `user-home` and `start-here` across scalable, 16px, 24px, and symbolic directories.
3. **Archive Mimetype Glyph**:
   - Updated `application-zip` and its aliases (`application-x-tar`, `application-x-7z-compressed`, `application-x-rar`, `application-x-bzip2`, `application-x-gzip`, `application-x-xz`, `application-zstd`, `package-x-generic`, etc.) to a minimal isometric yellow-orange cardboard box ("thùng vàng cam cơ bản") with tape and warm tones (`#f2ae43`, `#db902b`, `#bf771b`, `#fce1a6`), preserving flat minimal styling. Database files (`application-x-sqlite3`) retain the cylinder disc stack.
4. **Application Fallback (Inheritance)**:
   - Removed custom application icons from Hikaide-Symbols; the theme now exclusively scopes to folders (`places`), files (`mimetypes`), and symbols (`actions`, `status`, `devices`, `categories`, `emblems`).
   - Configured `Inherits=Adwaita,breeze,hicolor` in `index.theme` so launcher and window manager applications cleanly fall back to system Adwaita or Breeze icon sets.
5. **Validation & Verification**:
   - Tested under GTK3 and GTK4 icon theme lookup; all folder, file, and symbol icons resolve from Hikaide-Symbols, while applications resolve via inherited themes. All unit tests pass cleanly.
