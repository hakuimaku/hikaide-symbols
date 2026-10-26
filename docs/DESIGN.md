# Hikaide-Symbols design contract

The three user-supplied mockups are the visual references. This implementation
uses original SVG interpretations rather than cropped bitmap tiles.

| Family | Geometry and treatment |
| --- | --- |
| Places | 64×64, large flat folder, graphite in dark mode and white-gray in light mode, shaded lower-right triangle; ordinary folders have no dot or inner glyph, special folders use an accent glyph; link/hidden names reuse the plain folder, drag acceptance uses an open folder; no gradients or shadows |
| Files | 64×64, folded page, off-white in dark mode and a darker cool gray in light mode, charcoal format glyph, no colored file-format badges |
| Apps | 64×64, recognizable silhouette, gradients and controlled highlights, consistent optical bounds |
| Devices | Rounded silver/graphite geometry, shared glyph weights, accent indicator |
| Status | Neutral surface and clear state geometry; fixed warning/error colors |
| Actions/symbolic | Functional silhouettes; symbolic uses filled outlines at a 16×16 viewBox |

Semantic palettes in `src/theme/palette.json` resolve neutral SVG paint tokens for both appearances. The dark variant uses graphite folders and lighter action glyphs. The light variant uses white-gray folders (`#E1E3E7` fronts), darker cool-gray paper (`#D8DBE1` shading to `#B7BBC3`), and slate device/action glyphs. Folder backs and corners remain visibly shaded; the default blue accent has at least 4.5:1 contrast against the closed and open fronts. Shared primitives and geometry are unchanged.

| Paint | Contract |
| --- | --- |
| Folder | `folderBack`, `folderFront`, `folderCorner`, `folderOpenInterior`, `folderOpenFront` |
| Paper | `paper`, `paperShade`, `paperSmall`, fold roles, `fileGlyph` |
| Symbols | `statusSurface`, `statusGlyph`, `actionGlyph`, device and emblem roles |
| Warning / error | Stable yellow/red identity; light luminance adjusted for visibility |
| Accent | `accent.dark` and `accent.light`; one mutable Highlight role per built theme |
| Intentional colors | Category plates and archive artwork retain their designed colors |

Symbolic artwork is byte-identical across appearances and keeps GTK foreground/semantic/GPA runtime recoloring. It does not consume the neutral mode palette.

Art normally stays within x=4–60, y=3–61 at 64 px. Folder bounds are x=1–63,
y=5–60, filling almost the entire icon frame. Glyph stroke width is around 2.3 units on its 24-unit master, increased
for small-size variants. Shadows are offset translucent silhouettes, not blur
filters. No SVG filters, raster embeddings, external resources or font-dependent
lettering are used.

16/24 px folder sources retain the same flat shell with a thicker accent glyph.
16/24 px file sources simplify the fold and enlarge the format mark. SVGs in
these fixed-size theme directories intentionally retain the 64-unit viewBox;
GTK renders them at the declared lookup size. Larger sizes use scalable sources.
No PNG fallback is shipped: native rendering was checked in both GTK generations.

GTK3's symbolic loader discards strokes, so authoring expands those strokes into
filled paths through Qt's existing path stroker. This is not desaturation of the
full-color icons. Symbolic shapes omit plates, folds, dots, gradients and shadows.
`gpa:version="1"` and `gpa:fill="accent"` opt the four accent-role symbols into
modern GTK parsing. Older GTK still renders their ordinary filled path using
the widget foreground. Foreground and semantic colors are runtime UI roles,
not additional theme accents.

All static mutable paint uses `.ColorScheme-Highlight { color:@ACCENT@; }`
and consumes that through `currentColor`; build resolves the token once.
Regular application brand interpretations keep fixed palettes. Accent editing
of an installed theme is delegated entirely to `hakuimaku/icon-accent`.

References used for implementation:

- [Freedesktop icon theme specification](https://specifications.freedesktop.org/icon-theme/latest/)
- [GTK symbolic SVG/GPA format](https://docs.gtk.org/gtk4/icon-format.html)
- [GTK SVG extensions and versioning](https://docs.gtk.org/gtk4/class.Svg.html)
- [libadwaita system accent RGB values](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/enum.AccentColor.html)
