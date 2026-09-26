#!/usr/bin/env python3
"""
Study 032 · Draft A: Naive Entanglement Baseline
Studio Anamnesis · Series XXXVIII · INQ-26

Naive premise: Depicting ER = EPR as two disconnected circles in flat Euclidean space
connected by a single straight line, without hyperbolic curvature, Kruskal horizons,
or negative energy shockwaves.
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH, HEIGHT = 800, 800

def generate_draft_a():
    img = bytearray(WIDTH * HEIGHT * 3)
    
    # Left and Right centers
    c_left = (WIDTH * 0.28, HEIGHT * 0.5)
    c_right = (WIDTH * 0.72, HEIGHT * 0.5)
    r_boundary = 120.0
    
    for y in range(HEIGHT):
        row_offset = y * WIDTH * 3
        for x in range(WIDTH):
            # Distance to left and right circles
            d_l = math.hypot(x - c_left[0], y - c_left[1])
            d_r = math.hypot(x - c_right[0], y - c_right[1])
            
            # Distance to connecting horizontal segment
            d_line = abs(y - HEIGHT * 0.5) if (c_left[0] <= x <= c_right[0]) else 999.0
            
            r, g, b = 10, 12, 18
            
            # Boundary rings
            if abs(d_l - r_boundary) < 3.0:
                r, g, b = 56, 215, 208
            elif d_l < r_boundary:
                # Flat interior
                val = int(25 + 40 * (1.0 - d_l / r_boundary))
                r, g, b = val // 2, val, val
                
            if abs(d_r - r_boundary) < 3.0:
                r, g, b = 212, 175, 55
            elif d_r < r_boundary:
                val = int(25 + 40 * (1.0 - d_r / r_boundary))
                r, g, b = val, int(val * 0.8), val // 3
                
            # Straight connecting line (naive entanglement)
            if d_line < 2.0:
                r, g, b = 240, 240, 240
            elif d_line < 6.0:
                blend = (6.0 - d_line) / 4.0
                r = int(r * (1 - blend) + 160 * blend)
                g = int(g * (1 - blend) + 160 * blend)
                b = int(b * (1 - blend) + 200 * blend)
                
            pixel_idx = row_offset + x * 3
            img[pixel_idx] = max(0, min(255, r))
            img[pixel_idx + 1] = max(0, min(255, g))
            img[pixel_idx + 2] = max(0, min(255, b))
            
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_032_draft_a_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, bytes(img))
    print(f"[✓] Study 032 Draft A rendered: {out_path}")

if __name__ == "__main__":
    generate_draft_a()
