# Folder states

| Icon name | Appearance |
| --- | --- |
| `folder` | Plain graphite folder |
| `folder-open` | Open folder with a dark interior and a sloped front flap |
| `folder-drag-accept` | Alias of `folder-open`, for a folder accepting a dragged item |
| `folder-link`, `folder-hidden`, `folder-hidden-link` | Compatibility aliases of the plain `folder` |

Folders have flat colors, no gradients or shadows, and a solid dark triangle at
the lower-right corner. Link folders have no accent dot. Hidden folders have no
lettering on their tab. Special folders retain their accent-colored glyphs.

Regular states are available in scalable, 16 px and 24 px directories. Symbolic
state names are also provided; open symbolic artwork differs from the closed
folder. The drag-accept aliases prevent the missing state name from resolving
to another theme's artwork.

[Thunar's state selection](https://raw.githubusercontent.com/xfce-mirror/thunar/master/thunar/thunar-file.c)
requests `folder-drag-accept` for an ordinary directory in the drop state and
`folder-open` for an opened directory. The theme supplies both names. Each file
manager decides when it requests a state icon; this does not make a folder
permanently open after a file is dropped.

Symlink emblems and hidden-item opacity remain file-manager behavior. The theme
adds no background watcher, custom folder metadata or file-manager patch.
