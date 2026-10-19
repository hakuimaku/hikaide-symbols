#!/usr/bin/env python3
"""Explicit artwork regeneration. Normal builds read the existing source SVGs."""
from draw_icons import places, mimetypes, system_families

if __name__ == "__main__":
    places()
    mimetypes()
    system_families()
    print("Regenerated original SVG artwork and alias manifests in src/")
