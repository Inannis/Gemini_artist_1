#!/usr/bin/env python3
"""
STUDY 029 · DRAFT A (NAIVE BASELINE)
Series XXXV: Non-Commutative Spacetime & The Moyal Foam
Direct algorithmic transcription of a naive 2D Moyal deformed grid.
A baseline study intended for rigorous critique.
Zero external dependencies (pure Python 3 standard library).
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 1200
HEIGHT = 1200

def render_draft_a():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Naive deformation parameter (constant scalar)
    theta_naive = 0.15
    grid_freq = 16.0
    
    for y in range(HEIGHT):
        ny = (y - cy) / cy  # [-1, 1]
        for x in range(WIDTH):
            nx = (x - cx) / cx  # [-1, 1]
            
            # Naive 2D coordinate displacement
            # Pretending [x, y] = i*theta is simply an optical sin shear
            dx = theta_naive * math.sin(grid_freq * ny)
            dy = -theta_naive * math.sin(grid_freq * nx)
            
            u = nx + dx
            v = ny + dy
            
            # Distance from center in deformed space
            r = math.sqrt(u * u + v * v)
            
            # Naive Cartesian grid lines
            line_u = math.cos(grid_freq * math.pi * u)
            line_v = math.cos(grid_freq * math.pi * v)
            grid_val = max(0.0, (line_u + line_v) * 0.5)
            grid_sharp = math.pow(grid_val, 8.0)
            
            # Center radial glow
            core_glow = math.exp(-3.0 * r)
            
            # Color assignment (naive monochrome blue-cyan)
            r_val = int(255.0 * min(1.0, 0.1 * grid_sharp + 0.1 * core_glow))
            g_val = int(255.0 * min(1.0, 0.4 * grid_sharp + 0.6 * core_glow))
            b_val = int(255.0 * min(1.0, 0.7 * grid_sharp + 0.9 * core_glow))
            
            idx = (y * WIDTH + x) * 3
            buf[idx] = r_val
            buf[idx + 1] = g_val
            buf[idx + 2] = b_val
            
    out_path = os.path.join(os.path.dirname(__file__), "study_029_draft_a_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT A] Generated naive Moyal grid plate: {out_path}")

if __name__ == "__main__":
    render_draft_a()

