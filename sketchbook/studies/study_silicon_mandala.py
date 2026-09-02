#!/usr/bin/env python3
"""
Study: Silicon Die Sacred Mandala Generator
Location: sketchbook/studies/study_silicon_mandala.py
Studio: Studio Anamnesis
Inquiry: INQ-03 (The Microscopic Sacred / Silicon Die Cartographies)

Testing 4-fold recursive photolithographic geometry, H-tree clock distributions,
and concentric cache sanctuaries.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_htree(draw, x, y, size, depth, max_depth, color):
    """Draw a recursive H-tree clock distribution network."""
    if depth >= max_depth or size < 4:
        return
    half = size / 2.0
    # Horizontal bar
    draw.line([(x - half, y), (x + half, y)], fill=color, width=max(1, int(max_depth - depth)))
    # Left vertical
    draw.line([(x - half, y - half), (x - half, y + half)], fill=color, width=max(1, int(max_depth - depth)))
    # Right vertical
    draw.line([(x + half, y - half), (x + half, y + half)], fill=color, width=max(1, int(max_depth - depth)))

    # Recurse on 4 endpoints
    next_size = size / 2.0
    draw_htree(draw, x - half, y - half, next_size, depth + 1, max_depth, color)
    draw_htree(draw, x - half, y + half, next_size, depth + 1, max_depth, color)
    draw_htree(draw, x + half, y - half, next_size, depth + 1, max_depth, color)
    draw_htree(draw, x + half, y + half, next_size, depth + 1, max_depth, color)

def run_study(out_path="sketchbook/studies/study_silicon_mandala.png"):
    print("[*] Running Study: Silicon Die Sacred Mandala...")
    size = 2048
    img = Image.new("RGBA", (size, size), (5, 8, 12, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    cx, cy = size // 2, size // 2

    # Concentric silicon wafer rings
    gold = (212, 175, 55, 180)
    cyan = (56, 215, 210, 160)
    silver = (220, 230, 240, 140)
    purple = (147, 112, 219, 120)

    # 1. Outer Wafer Reticle Boundary
    for r in [950, 920, 880, 840]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=gold, width=1)

    # 2. Square Walled Sanctuaries (Mandala concentric courts)
    courts = [780, 680, 560, 440, 320, 200, 100]
    for idx, s in enumerate(courts):
        c = cyan if idx % 2 == 0 else gold
        draw.rectangle([cx - s, cy - s, cx + s, cy + s], outline=c, width=2)
        # Cardinal T-gate portals (Toranas)
        gate_w = s // 3
        # North
        draw.line([(cx - gate_w, cy - s), (cx - gate_w, cy - s - 25)], fill=c, width=2)
        draw.line([(cx + gate_w, cy - s), (cx + gate_w, cy - s - 25)], fill=c, width=2)
        draw.line([(cx - gate_w, cy - s - 25), (cx + gate_w, cy - s - 25)], fill=c, width=2)
        # South
        draw.line([(cx - gate_w, cy + s), (cx - gate_w, cy + s + 25)], fill=c, width=2)
        draw.line([(cx + gate_w, cy + s), (cx + gate_w, cy + s + 25)], fill=c, width=2)
        draw.line([(cx - gate_w, cy + s + 25), (cx + gate_w, cy + s + 25)], fill=c, width=2)
        # East
        draw.line([(cx + s, cy - gate_w), (cx + s + 25, cy - gate_w)], fill=c, width=2)
        draw.line([(cx + s, cy + gate_w), (cx + s + 25, cy + gate_w)], fill=c, width=2)
        draw.line([(cx + s + 25, cy - gate_w), (cx + s + 25, cy + gate_w)], fill=c, width=2)
        # West
        draw.line([(cx - s, cy - gate_w), (cx - s - 25, cy - gate_w)], fill=c, width=2)
        draw.line([(cx - s, cy + gate_w), (cx - s - 25, cy + gate_w)], fill=c, width=2)
        draw.line([(cx - s - 25, cy - gate_w), (cx - s - 25, cy + gate_w)], fill=c, width=2)

    # 3. Recursive H-Tree Clock Distribution inside the Four Quadrants
    quad_offset = 500
    for qx, qy in [(-quad_offset, -quad_offset), (-quad_offset, quad_offset), (quad_offset, -quad_offset), (quad_offset, quad_offset)]:
        draw_htree(draw, cx + qx, cy + qy, 240, 0, 5, silver)

    # 4. Central Bindu (The Arithmetic Core Altar)
    draw.rectangle([cx - 50, cy - 50, cx + 50, cy + 50], fill=(15, 25, 38, 240), outline=gold, width=2)
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=cyan, width=2)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255, 240))

    # Dense Circuit Bus Lines between courts
    for angle_deg in range(0, 360, 15):
        rad = math.radians(angle_deg)
        x1 = cx + math.cos(rad) * 340
        y1 = cy + math.sin(rad) * 340
        x2 = cx + math.cos(rad) * 420
        y2 = cy + math.sin(rad) * 420
        draw.line([(x1, y1), (x2, y2)], fill=purple, width=1)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Study saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    run_study()
