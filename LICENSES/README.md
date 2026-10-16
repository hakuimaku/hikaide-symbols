# Artwork provenance

All SVG artwork under `src/` was drawn for Hikaide-Symbols as vector geometry
in `scripts/draw_icons.py` and `scripts/draw_apps.py`. No upstream application
SVGs, icon-theme assets, raster images, fonts, or downloaded logos are included
in the installable theme. Generated artwork and project scripts use the root
MIT license. Brand names identify the intended applications; trademarks remain
with their respective owners. This theme is not affiliated with those projects.

The user's supplied files under `docs/mockups/` and the supplied implementation
plan are design references. The project license does not relicense those inputs;
they are not included in the theme package.

PySide6/Qt is an authoring tool for converting this project's symbolic strokes
to filled paths. librsvg and Pillow render preview sheets. These tools and their
code are not bundled. No font outlines are embedded in icons: the lettering is
original path geometry defined by this project.

If artwork is imported in a later change, add a per-asset source URL, author,
license and required attribution here before including it in a release.
