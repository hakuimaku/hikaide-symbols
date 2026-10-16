#!/usr/bin/env python3
"""Compatibility entry point; delegates installed SVG editing to icon-accent."""
import argparse
from pathlib import Path
import subprocess
from accent_adapter import normalize, sync

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("color")
parser.add_argument("--icons-dir", type=Path)
args = parser.parse_args()
try:
    sync(normalize(args.color), args.icons_dir)
except (ValueError, OSError, subprocess.SubprocessError) as e:
    parser.exit(1, f"{e}\n")
