#!/usr/bin/env python3
"""Explicit artwork regeneration. Normal builds read the existing source SVGs."""
from draw_icons import places, mimetypes, system_families
from draw_apps import apps

if __name__ == "__main__":
    places()
    mimetypes()
    system_families()
    apps()
    print("Regenerated original SVG artwork and alias manifests in src/")
