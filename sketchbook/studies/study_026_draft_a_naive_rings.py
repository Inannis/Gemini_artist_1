#!/usr/bin/env python3
"""
STUDY 026 · DRAFT A (NAIVE BASELINE)
Series XXXII: Conformal Cyclic Cosmology & The Penrose Crossover
Direct algorithmic transcription of concentric Hawking point rings.
A baseline study intended for formal critique.
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 1280
HEIGHT = 720

def render_draft_a():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Ring radii in pixels (naive scaling: 1 deg = 18 px)
    r1 = 4.2 * 18.0   # 75.6 px
    r2 = 11.8 * 18.0  # 212.4 px
    r3 = 24.5 * 18.0  # 441.0 px
    w = 1.2 * 18.0    # 21.6 px
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3
            
            # Ambient background: simple dark blue gradient
            bg_b = int(25 + 15 * max(0.0, 1.0 - dist / 500.0))
            r = 8
            g = 12
            b = bg_b
            
            # Simple Gaussian ring additions
            for target_r in [r1, r2, r3]:
                d = abs(dist - target_r)
                if d < w * 2.0:
                    intensity = math.exp(-0.5 * (d / (w * 0.5)) ** 2)
                    r = int(min(255, r + 200 * intensity))
                    g = int(min(255, g + 180 * intensity))
                    b = int(min(255, b + 240 * intensity))
                    
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b
            
    out_path = os.path.join(os.path.dirname(__file__), "study_026_draft_a_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT A] Generated Naive Rings study: {out_path}")

if __name__ == "__main__":
    render_draft_a()

