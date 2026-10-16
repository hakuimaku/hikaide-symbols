# Folder states: artwork and file-manager integration

The theme includes explicit regular SVG assets for these appearances:

| Icon name | Appearance |
| --- | --- |
| `folder` | Plain graphite folder, no internal glyph or dot |
| `folder-link` | Plain folder with an accent dot inside the upper-right corner |
| `folder-hidden` | Plain folder with vector lettering “hidden” on the upper-left tab |
| `folder-hidden-link` | The hidden label and accent dot together |

All variants keep the solid dark lower-right triangle, flat colors and large
folder silhouette. They are available in scalable and 16/24 px directories.
The hidden label is original path geometry, not SVG text, so it needs no font.
At small menu sizes the complete word is necessarily too small to read; inspect
the 64 px or larger rendering for the label.

**These are explicit appearance assets, not an automatic filesystem rule.**
Installing them alone does not cause Nautilus or Thunar to select them for every
hidden directory or directory symlink. No folders, metadata or desktop launchers
are modified by the theme build/install scripts.

## Why a theme alone cannot switch these states

A local GIO query for `standard::icon` returns the same themed icon names for a
normal directory, a hidden directory and a valid symlink to a directory. The
separate `standard::is-hidden` and `standard::is-symlink` attributes indicate the
states; an SVG or `index.theme` has no filesystem-condition hook.

[Nautilus](https://raw.githubusercontent.com/GNOME/nautilus/main/src/nautilus-file.c)
adds its own symbolic-link emblem. It supports per-file custom icon metadata,
but choosing a state-specific icon automatically requires integration that reads
the state and supplies that custom icon. A generic symlink emblem also applies
to linked files, not only folders.

[Thunar's renderer](https://raw.githubusercontent.com/xfce-mirror/thunar/master/thunar/thunar-icon-renderer.c)
places the first emblem at the lower right and reduces opacity for hidden items.
The theme cannot move that emblem to the upper right or replace the opacity rule
with a word on the folder tab. The installed Thunar library is version 4.20.10;
support must be verified against that version before implementing an adapter.

Consequently, changing the global symlink emblem to a dot would not implement
the requested upper-right, folder-only behavior in both applications. That
emblem remains unchanged. No background watcher, injected library or modified
file-manager binary is installed as part of this icon-theme change.

To obtain the exact automatic appearance in both managers, the file managers
need to choose `folder-link`, `folder-hidden` or `folder-hidden-link` from their
own state-aware icon selection path. That is a separate integration change;
the SVG variants are ready for it.
