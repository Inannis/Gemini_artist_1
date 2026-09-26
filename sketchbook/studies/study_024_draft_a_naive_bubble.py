#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 024 (DRAFT A: NAIVE BASELINE)
The Naive Bubble Nucleation (Sterile Euclidean Geometry)
Renders a naive, textbook circular bubble in a static 2D plane.
Exposes the sterility of uncritical, non-relativistic geometric representation.
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 1920
HEIGHT = 1080

def render_draft_a():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_bubble = 340.0 # Arbitrary static radius
    wall_thickness = 18.0

    print("[DRAFT A] Rendering naive Euclidean bubble...")
    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3

            if dist < r_bubble - wall_thickness:
                # Inside true vacuum: naive flat dark gray
                r = 20
                g = 22
                b = 28
            elif dist <= r_bubble + wall_thickness:
                # Bubble wall: smooth Gaussian profile
                d_wall = abs(dist - r_bubble) / wall_thickness
                intensity = math.exp(-d_wall * d_wall * 2.5)
                r = int(240 * intensity)
                g = int(180 * intensity)
                b = int(70 * intensity)
            else:
                # Outside false vacuum: sterile blue grid
                grid_x = (x % 60 == 0)
                grid_y = (y % 60 == 0)
                if grid_x or grid_y:
                    r = 45
                    g = 55
                    b = 80
                else:
                    r = 15
                    g = 20
                    b = 35

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    out_path = os.path.join(os.path.dirname(__file__), "study_024_draft_a_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT A] Plate generated: {out_path}")

if __name__ == "__main__":
    render_draft_a()

