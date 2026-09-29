#!/usr/bin/env python3
"""
STUDY 035 · DRAFT A: THE NAIVE SCHWARZSCHILD SPHERE
Series XLI · Black Hole Horizons & Microstate Geometry Explorations
Studio Anamnesis · Pure Python Standard Library Baseline

A naive, flat baseline representing the classical general relativity view:
A sterile, featureless black disk with a simple smooth radial blur.
Designed specifically to undergo rigorous formal critique.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 1200
HEIGHT = 675

def render_draft_a():
    buffer = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_horizon = 200.0

    for y in range(HEIGHT):
        ny = (y - cy)
        for x in range(WIDTH):
            nx = (x - cx)
            dist = math.sqrt(nx * nx + ny * ny)
            
            # Simple radial falloff outside horizon, pure pitch black inside
            if dist <= r_horizon:
                r_val = 0
                g_val = 0
                b_val = 0
            else:
                # Naive smooth glow
                factor = math.exp(-(dist - r_horizon) / 45.0)
                # Flat yellow-orange gradient
                r_val = int(255 * factor)
                g_val = int(140 * factor)
                b_val = int(40 * factor)
                
            idx = (y * WIDTH + x) * 3
            buffer[idx] = max(0, min(255, r_val))
            buffer[idx + 1] = max(0, min(255, g_val))
            buffer[idx + 2] = max(0, min(255, b_val))
            
    out_png = os.path.join(os.path.dirname(__file__), "study_035_draft_a_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[STUDY-035-A] Generated: {out_png}")

if __name__ == "__main__":
    render_draft_a()

