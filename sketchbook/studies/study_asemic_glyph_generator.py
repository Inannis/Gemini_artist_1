#!/usr/bin/env python3
"""
Study: Procedural Asemic Glyph Generator
Location: sketchbook/studies/study_asemic_glyph_generator.py
Studio: Studio Anamnesis
Inquiry: INQ-04 (The Autoregressive Ghost / Asemic Lithography)

Synthesizing cuneiform wedge impressions, mathematical operators,
and circuit topologies into non-semantic glyph tablets.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw

def draw_cuneiform_wedge(draw, x, y, length, angle_rad, width_head, color):
    """Draw a single triangular wedge stroke reminiscent of a Sumerian reed stylus."""
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    perp_x, perp_y = -sin_a, cos_a

    # Apex (tail)
    x_tail = x + cos_a * length
    y_tail = y + sin_a * length

    # Head points
    half_w = width_head / 2.0
    x_h1 = x + perp_x * half_w
    y_h1 = y + perp_y * half_w
    x_h2 = x - perp_x * half_w
    y_h2 = y - perp_y * half_w

    # Draw triangular polygon
    draw.polygon([(x_h1, y_h1), (x_h2, y_h2), (x_tail, y_tail)], fill=color)

def generate_procedural_glyph(draw, cx, cy, box_size, seed_val, color_ink, color_gold):
    """Generate a single unique asemic glyph inside a bounding box."""
    rng = np.random.RandomState(seed_val)
    half = box_size * 0.42

    # Number of strokes: 3 to 7
    n_strokes = rng.randint(3, 8)
    
    # Grid anchor points in 3x3 normalized space
    anchors = []
    for gx in [-half, 0, half]:
        for gy in [-half, 0, half]:
            anchors.append((cx + gx + rng.uniform(-4, 4), cy + gy + rng.uniform(-4, 4)))

    # Draw strokes
    for s in range(n_strokes):
        stroke_type = rng.choice(["wedge", "arc", "line", "ring", "cross"])
        p1 = anchors[rng.randint(len(anchors))]

        if stroke_type == "wedge":
            angle = rng.choice([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, -math.pi/4, -math.pi/2])
            length = rng.uniform(box_size * 0.25, box_size * 0.55)
            w_head = rng.uniform(5, 12)
            col = color_ink if rng.random() > 0.3 else color_gold
            draw_cuneiform_wedge(draw, p1[0], p1[1], length, angle, w_head, col)

        elif stroke_type == "line":
            p2 = anchors[rng.randint(len(anchors))]
            col = color_ink if rng.random() > 0.25 else color_gold
            draw.line([p1, p2], fill=col, width=rng.choice([1, 2, 3]))

        elif stroke_type == "arc":
            r = rng.uniform(8, box_size * 0.3)
            ang_start = rng.randint(0, 270)
            ang_end = ang_start + rng.randint(90, 270)
            draw.arc([p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r], start=ang_start, end=ang_end, fill=color_ink, width=2)

        elif stroke_type == "ring":
            r = rng.uniform(4, 10)
            draw.ellipse([p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r], outline=color_gold, width=1)
            if rng.random() > 0.5:
                draw.ellipse([p1[0] - 2, p1[1] - 2, p1[0] + 2, p1[1] + 2], fill=color_gold)

        elif stroke_type == "cross":
            cs = rng.uniform(6, 12)
            draw.line([(p1[0] - cs, p1[1]), (p1[0] + cs, p1[1])], fill=color_ink, width=1)
            draw.line([(p1[0], p1[1] - cs), (p1[0], p1[1] + cs)], fill=color_ink, width=1)

def run_study(out_path="sketchbook/studies/study_asemic_plate.png"):
    print("[*] Running Study: Asemic Inscription Tablet...")
    t0 = time.time()
    width, height = 2400, 1600
    img = Image.new("RGBA", (width, height), (8, 12, 16, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # Stone tablet boundary
    pad_x, pad_y = 160, 140
    draw.rectangle([pad_x, pad_y, width - pad_x, height - pad_y], fill=(14, 18, 24, 255), outline=(212, 175, 55, 120), width=2)

    # Grid of glyphs: 12 columns by 7 rows = 84 glyphs
    cols = 12
    rows = 7
    cell_w = (width - 2 * pad_x - 80) / cols
    cell_h = (height - 2 * pad_y - 80) / rows

    c_ink  = (220, 235, 245, 230)
    c_gold = (212, 175, 55, 240)
    c_grid = (56, 215, 210, 25)

    # Guide lines
    for r in range(rows + 1):
        gy = pad_y + 40 + r * cell_h
        draw.line([(pad_x + 30, gy), (width - pad_x - 30, gy)], fill=c_grid, width=1)

    seed_counter = 42
    for r in range(rows):
        for c in range(cols):
            cell_cx = pad_x + 40 + c * cell_w + cell_w / 2.0
            cell_cy = pad_y + 40 + r * cell_h + cell_h / 2.0

            generate_procedural_glyph(draw, cell_cx, cell_cy, min(cell_w, cell_h) * 0.85, seed_counter, c_ink, c_gold)
            seed_counter += 1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG")
    print(f"[✓] Asemic Tablet Study saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB) in {time.time()-t0:.2f}s")
    return out_path

if __name__ == "__main__":
    run_study()

