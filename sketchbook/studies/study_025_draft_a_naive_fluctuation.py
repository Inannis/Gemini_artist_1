#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 025 (DRAFT A: NAIVE BASELINE)
The Naive Thermal Fluctuation (Sterile White Gaussian Noise)
Renders a naive, textbook circular cosmological horizon with flat Gaussian noise.
Exposes the sterility of treating quantum thermal recurrence as simple statistical television static.
"""

import math
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 1920
HEIGHT = 1080

def render_draft_a():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_horizon = 420.0

    print("[DRAFT A] Rendering naive thermal fluctuation plate...")
    random.seed(42)

    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3

            # Naive white noise simulating thermal bath
            noise = random.gauss(0.0, 1.0)
            base = int(max(0, min(255, 30 + noise * 25)))

            if abs(dist - r_horizon) < 2.5:
                # Flat white boundary circle
                r, g, b = 255, 255, 255
            elif dist < r_horizon:
                # Inside horizon: slight blue-grey tint
                r = min(255, base + 15)
                g = min(255, base + 20)
                b = min(255, base + 35)
            else:
                # Outside horizon: darker static
                r = int(base * 0.4)
                g = int(base * 0.4)
                b = int(base * 0.6)

            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_025_draft_a_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[+] Draft A Plate written to: {out_path}")

if __name__ == "__main__":
    render_draft_a()

