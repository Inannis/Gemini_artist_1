#!/usr/bin/env python3
"""
sketchbook/studies/study_033_draft_a_naive_pentagons.py
======================================================
Study 033 · Draft A: Naive Euclidean Pentagon Lattice (Naive Baseline).

Attempt to depict the HaPPY quantum error-correcting tensor network.
Renders regular pentagons in flat Euclidean 2D space with uniform line weights
and static radial color gradients.

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
    
    # Background: flat dark gray
    for i in range(width * height):
        pixels[i*3] = 18
        pixels[i*3 + 1] = 20
        pixels[i*3 + 2] = 26
        
    def draw_pentagon(x0, y0, radius, color):
        points = []
        for i in range(5):
            angle = i * (2.0 * math.pi / 5.0) - math.pi * 0.5
            px = x0 + radius * math.cos(angle)
            py = y0 + radius * math.sin(angle)
            points.append((px, py))
            
        for i in range(5):
            p1 = points[i]
            p2 = points[(i + 1) % 5]
            steps = int(max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))) * 2
            if steps == 0:
                continue
            for s in range(steps):
                t = s / steps
                x = int(p1[0] + t * (p2[0] - p1[0]))
                y = int(p1[1] + t * (p2[1] - p1[1]))
                if 0 <= x < width and 0 <= y < height:
                    idx = (y * width + x) * 3
                    pixels[idx] = color[0]
                    pixels[idx + 1] = color[1]
                    pixels[idx + 2] = color[2]

    # Draw central pentagon
    draw_pentagon(cx, cy, 70, (212, 175, 55))
    
    # Draw ring 1 (5 pentagons)
    for i in range(5):
        ang = i * (2.0 * math.pi / 5.0) - math.pi * 0.5
        rx = cx + 130 * math.cos(ang)
        ry = cy + 130 * math.sin(ang)
        draw_pentagon(rx, ry, 60, (56, 189, 248))
        
    # Draw ring 2 (10 pentagons in Euclidean circle)
    for i in range(10):
        ang = i * (2.0 * math.pi / 10.0)
        rx = cx + 240 * math.cos(ang)
        ry = cy + 240 * math.sin(ang)
        draw_pentagon(rx, ry, 50, (168, 85, 247))
        
    write_png(output_path, width, height, pixels)
    print(f"[Study 033 Draft A] Successfully written: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_033_draft_a_plate.png"))
    render_draft_a(out)
