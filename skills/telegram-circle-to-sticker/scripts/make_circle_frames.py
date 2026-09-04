#!/usr/bin/env python3
"""Apply a circular alpha mask to a numbered PNG frame sequence."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

if len(sys.argv) != 3:
    raise SystemExit("Usage: make_circle_frames.py INPUT_DIR OUTPUT_DIR")
src, dst = map(Path, sys.argv[1:])
dst.mkdir(parents=True, exist_ok=True)
paths = sorted(src.glob("*.png"))
if not paths:
    raise SystemExit(f"No PNG frames found in {src}")
for i, path in enumerate(paths):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, w - 1, h - 1), fill=255)
    im.putalpha(mask)
    im.save(dst / f"{i:04d}.png")
print(f"Wrote {len(paths)} RGBA frames to {dst}")
