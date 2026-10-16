# Hikaide-Symbols — QA, 2026-10-16

The implementation covers the full icon families in the supplied plan. Automated
checks pass. Interactive desktop acceptance is only partially exercised; the
unchecked session tests below are not claimed as passed.

## Delivered coverage

| Family | Canonical scalable SVG files | Resolved regular names including aliases |
| --- | ---: | ---: |
| Applications | 182 | 429 |
| Places | 33 | 56 |
| Mimetypes | 50 | 187 |
| Devices | 27 | 27 |
| Status | 29 | 57 |
| Actions | 46 | 58 |
| Categories | 11 | 11 |
| Emblems | 10 | 10 |

Additionally: 165 canonical symbolic SVGs, 16/24 px optimized places/mimetypes,
832 relative symlink aliases across all directories. The installable tree has
719 regular SVG files and 1,551 SVG paths in total. File counts include size
variants and reused concepts; they are not a count of distinct designs.

The frozen [required-icon fixture](../tests/required-icons.json) covers all
28 places, 88 mimetypes, 180 application identifiers, 27 devices, 29 statuses,
34 actions, 11 categories and 10 emblems listed in the main plan sections.

## Checks run

| Check | Result and evidence |
| --- | --- |
| Build + validation | PASS: correct index, declared directories, hicolor inheritance, XML/viewBox, safe paint references, aliases, collisions, no raster/filter/script/external resource, no unresolved token |
| Unit/integration suite | PASS: 10 tests, no skips; `python3 -m unittest discover -s tests -v` |
| Determinism | PASS: full build file hashes/symlinks identical on repeat; two archives byte-identical |
| Installation | PASS: clean install, update, cache creation, alias preservation, uninstall in temporary user-owned directory |
| Destructive-operation guards | PASS: unmanaged directory and symlink refused; unrelated test file preserved; repeat install requires `--replace` |
| Native GTK3 | PASS: 3.24.52, 3,170 lookups at 16/24/32/48/64 px, canonical regular and all symbolic rendering, scale-2 lookup and 64 px pixbuf, foreground recoloring |
| Native GTK4 | PASS: 4.24.1, same 3,170 lookups, regular/symbolic rendering, scale-2 lookup, foreground recoloring, GPA runtime accent A/B |
| hicolor fallback | PASS: both GTK versions resolve a sentinel that exists only in a temporary hicolor theme |
| GTK3/4 file chooser | PASS: actual `Gtk.FileChooserWidget` construction with the process theme; no interactive chooser flow asserted |
| Settings icon | PASS: actual GTK image widget constructed with `preferences-system`; no desktop settings application review asserted |
| Nautilus + Thunar | PASS: both start and remain alive for four seconds under private Broadway/D-Bus, GTK query confirms Hikaide-Symbols; startup smoke only |
| MIME naming | PASS: 13 real files queried by `xdg-mime`, GIO icon names resolve into this theme |
| Accent contract | PASS: external installed icon-accent detects exactly one editable accent; 139 eligible SVG files; 165 symbolic targets, 4 with GPA accent |
| Accent A → B → restore | PASS: all eligible SVGs change only the highlight declaration; fixed artwork and all other SVGs stay unchanged; repeat set is idempotent; original bytes and symlinks restored |
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

`dist/Hikaide-Symbols.tar.gz` — 92,600 bytes at this build.

SHA-256:

```text
f70cf1a42789a26e7ec27a4f63146ea15792215afa2ba43eeff4b5652dc5b669
```

The matching `.sha256` file is next to the archive. The package contains only
the installable theme, ownership marker, license and provenance. Mockups,
machine-specific reports and preview PNGs are not bundled.

## Folder style revision

Folders span x=1–63, y=5–60 on the 64-unit canvas, with flat graphite
surfaces and no gradient, filter or shadow. Ordinary folder/folder-open artwork
has no internal glyph or accent declaration. Special-folder glyphs and full-trash
paper marks keep the Highlight/currentColor accent. Every folder has a solid
dark triangle at the lower right. Ordinary and special folders have no decorative
dot; the explicit link state variants add an accent dot at the upper right. The
old diagonal line is removed, including the 16/24 px versions and aliases.

The ten tests pass. Folder regression checks cover no gradients, conditional link dots, undecorated
ordinary folders, preserved accent roles, rendered bounds and actual dark corner
pixels (right corner dark, left corner plain). External accent change/restore also passes. The installed theme and icon
cache were updated after checking for unrelated customizations.

See [updated folder preview](../previews/preview-places.png).

## Folder state artwork and integration limit

`folder-link`, `folder-hidden` and `folder-hidden-link` are now present in
scalable/16/24 versions. Link variants alone have an upper-right accent dot;
hidden variants have original vector lettering on the upper-left tab.

The additional GIO regression test queries a real directory, hidden directory
and symlink to a directory: all three still receive the same standard icon
names, while their hidden/symlink attributes differ. The artwork is available,
but automatic state-specific selection in Nautilus/Thunar has not been
implemented or claimed. Existing native symlink emblems remain unchanged.

See [state preview](../previews/folder-states.png),
locally generated GIO lookup results in `folder-state-lookup.json`, and
[integration explanation](../docs/FOLDER_STATES.md).

The installed theme's accent had been changed to `#ac7994` outside this build.
The full replacement guard correctly refused to reset it. Only the nine new
state SVGs were added, compiled from source using that installed accent; all
existing SVGs were left unchanged. Installed-theme validation and cache refresh
passed. The state preview now uses that installed accent. This still does not
enable automatic folder-state selection in either file manager.

## Hardware Locality lstopo icon fix

The installed `/usr/share/applications/lstopo.desktop` requests `Icon=hwloc`,
but no hwloc artwork was present in the theme or the installed hwloc package.
Added an original CPU/topology SVG under that exact name and included it in
the authoring generator. The launcher scanner regression fixture now checks
this case. All ten tests pass. Native GTK lookup and rendering pass at
16/24/32/64/128 px, and the installed theme resolves and renders it at 32 px.
Only the new app asset and icon cache were written to the installed theme;
existing icons, accent and desktop files were preserved. The launcher UI
itself was not reopened or inspected. See [icon preview](../previews/hwloc.png).
