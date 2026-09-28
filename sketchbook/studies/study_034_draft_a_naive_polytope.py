#!/usr/bin/env python3
"""
sketchbook/studies/study_034_draft_a_naive_polytope.py
======================================================
Study 034 · Draft A: Naive Euclidean Polytope Wireframe (Naive Baseline).

Attempt to depict the Amplituhedron and positive Grassmannian geometry.
Renders a naive 2D geometric wireframe polygon in flat Euclidean space
with uniform stroke weight and arbitrary color-wheel fills.

Zero external dependencies. Pure standard library Python.
"""

import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

def render_draft_a(output_path, width=1280, height=720):
    pixels = bytearray(width * height * 3)
    cx, cy = width * 0.5, height * 0.5

    # Background: flat neutral gray
    for i in range(width * height):
        pixels[i*3] = 16
        pixels[i*3 + 1] = 18
        pixels[i*3 + 2] = 22

    def draw_line(x1, y1, x2, y2, color, thickness=1):
        steps = int(max(abs(x2 - x1), abs(y2 - y1))) * 2
        if steps == 0:
            return
        for s in range(steps + 1):
            t = s / steps
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            for dy in range(-thickness, thickness + 1):
                for dx in range(-thickness, thickness + 1):
                    px = x + dx
                    py = y + dy
                    if 0 <= px < width and 0 <= py < height:
                        idx = (py * width + px) * 3
                        pixels[idx] = color[0]
                        pixels[idx + 1] = color[1]
                        pixels[idx + 2] = color[2]

    # Naive Draft A: Draw two overlapping regular polygons (octagon and square)
    # attempting to represent "multidimensional projection"
    n_verts = 8
    radius = 240
    outer_points = []
    for i in range(n_verts):
        angle = i * (2.0 * math.pi / n_verts) - math.pi * 0.5
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        outer_points.append((px, py))

    # Inner vertices
    inner_points = []
    inner_radius = 110
    for i in range(n_verts):
        angle = i * (2.0 * math.pi / n_verts) - math.pi * 0.5 + (math.pi / n_verts)
        px = cx + inner_radius * math.cos(angle)
        py = cy + inner_radius * math.sin(angle)
        inner_points.append((px, py))

    # Draw outer ring edges
    for i in range(n_verts):
        p1 = outer_points[i]
        p2 = outer_points[(i + 1) % n_verts]
        draw_line(p1[0], p1[1], p2[0], p2[1], (180, 190, 210), thickness=1)

    # Draw inner ring edges
    for i in range(n_verts):
        p1 = inner_points[i]
        p2 = inner_points[(i + 1) % n_verts]
        draw_line(p1[0], p1[1], p2[0], p2[1], (100, 150, 220), thickness=1)

    # Connect outer to inner
    for i in range(n_verts):
        p_out = outer_points[i]
        p_in1 = inner_points[i]
        p_in2 = inner_points[(i - 1) % n_verts]
        draw_line(p_out[0], p_out[1], p_in1[0], p_in1[1], (80, 100, 140), thickness=1)
        draw_line(p_out[0], p_out[1], p_in2[0], p_in2[1], (80, 100, 140), thickness=1)

    # Cross connections through center
    for i in range(n_verts // 2):
        p1 = outer_points[i]
        p2 = outer_points[i + n_verts // 2]
        draw_line(p1[0], p1[1], p2[0], p2[1], (50, 70, 90), thickness=1)

    # Simple center dot
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            if dx*dx + dy*dy <= 16:
                idx = (int(cy + dy) * width + int(cx + dx)) * 3
                pixels[idx] = 240
                pixels[idx + 1] = 200
                pixels[idx + 2] = 80

    write_png(output_path, width, height, pixels)

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    target_png = os.path.join(out_dir, "study_034_draft_a_plate.png")
    render_draft_a(target_png)
