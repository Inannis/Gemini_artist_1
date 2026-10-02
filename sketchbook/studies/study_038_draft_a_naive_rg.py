#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 038 · DRAFT A (NAIVE BASELINE)
A naive, sterile linear visualization of Holographic Renormalization Group flow.
Treats radial depth z as a simple, uniform horizontal ladder with a naive gradient,
ignoring non-conformal scalar backreaction, Callan-Symanzik beta flow, and Wheeler-DeWitt quantum foam.
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png

def render_draft_a(width=1200, height=800):
    buf = bytearray(width * height * 3)
    bg_r, bg_g, bg_b = 10, 12, 16

    for i in range(width * height):
        buf[i*3] = bg_r
        buf[i*3+1] = bg_g
        buf[i*3+2] = bg_b

    def set_pixel(x, y, r, g, b):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buf[idx] = max(0, min(255, int(r)))
            buf[idx+1] = max(0, min(255, int(g)))
            buf[idx+2] = max(0, min(255, int(b)))

    # Draw naive linear horizontal scale slices
    num_slices = 32
    margin_x = 80
    margin_y = 60
    usable_h = height - 2 * margin_y

    for s in range(num_slices):
        y_slice = int(margin_y + (s / (num_slices - 1)) * usable_h)
        # Naive linear gradient: UV (top, cyan) to IR (bottom, amber)
        t = s / (num_slices - 1)
        r_col = int(40 + 200 * t)
        g_col = int(180 - 40 * t)
        b_col = int(220 - 180 * t)

        # Draw sterile straight horizontal line
        for x in range(margin_x, width - margin_x):
            set_pixel(x, y_slice, r_col, g_col, b_col)
            # Add naive uniform tick marks
            if x % 40 == 0:
                for dy in range(-4, 5):
                    set_pixel(x, y_slice + dy, r_col, g_col, b_col)

    # Draw naive straight vertical boundary rails
    for y in range(margin_y, height - margin_y):
        set_pixel(margin_x, y, 160, 170, 190)
        set_pixel(width - margin_x, y, 160, 170, 190)

    out_path = os.path.join(os.path.dirname(__file__), "study_038_draft_a_plate.png")
    write_png(out_path, width, height, buf)
    print(f"Rendered Study 038 Draft A to {out_path}")

if __name__ == "__main__":
    render_draft_a()
