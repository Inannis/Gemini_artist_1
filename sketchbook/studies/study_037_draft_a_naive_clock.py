#!/usr/bin/env python3
"""
STUDY 037 · DRAFT A: NAIVE CLOCKWORK TIMELINE (BASELINE)
Exploratory study attempting to visualize the time of the studio canon
using a conventional Euclidean circular clock dial with 44 tick marks.
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import sys

# Ensure tools can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png

def render_draft_a(width=1200, height=1200):
    buf = bytearray(width * height * 3)
    bg_r, bg_g, bg_b = 15, 18, 24
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

    cx, cy = width // 2, height // 2
    r_outer = 450
    r_inner = 380

    # Draw circular dial ring
    for y in range(height):
        for x in range(width):
            dist = math.hypot(x - cx, y - cy)
            if abs(dist - r_outer) < 3.0:
                set_pixel(x, y, 180, 190, 205)
            elif abs(dist - r_inner) < 2.0:
                set_pixel(x, y, 80, 90, 110)

    # Draw 44 naive radial tick marks for the 44 Opuses
    for i in range(44):
        theta = (2.0 * math.pi * i) / 44.0 - math.pi / 2.0
        x1 = int(cx + (r_inner - 20) * math.cos(theta))
        y1 = int(cy + (r_inner - 20) * math.sin(theta))
        x2 = int(cx + (r_outer + 20) * math.cos(theta))
        y2 = int(cy + (r_outer + 20) * math.sin(theta))

        # Line trace
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            px = int(x1 + (x2 - x1) * (s / steps))
            py = int(y1 + (y2 - y1) * (s / steps))
            set_pixel(px, py, 220, 200, 140)

    # Draw mechanical clock hands
    for s in range(300):
        # Hour hand
        theta_h = math.pi / 4.0
        hx = int(cx + s * 0.7 * math.cos(theta_h))
        hy = int(cy + s * 0.7 * math.sin(theta_h))
        set_pixel(hx, hy, 240, 240, 250)

        # Minute hand
        theta_m = -math.pi / 3.0
        mx = int(cx + s * 1.1 * math.cos(theta_m))
        my = int(cy + s * 1.1 * math.sin(theta_m))
        set_pixel(mx, my, 200, 160, 80)

    out_path = os.path.join(os.path.dirname(__file__), "study_037_draft_a_plate.png")
    write_png(out_path, width, height, buf)
    print(f"[✓] Study 037 Draft A Plate saved to: {out_path}")
    return 0

if __name__ == "__main__":
    sys.exit(render_draft_a())
