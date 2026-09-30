#!/usr/bin/env python3
"""
STUDY 036 · DRAFT A: THE NAIVE DETERMINISTIC ATTRACTOR
Series XLII · SYK Quantum Chaos & Scrambling Explorations
Studio Anamnesis · Pure Python Standard Library Baseline

A naive, flat baseline representing classical low-dimensional deterministic chaos:
A simple 2D projection of the Lorenz butterfly attractor rendered as monochrome lines.
Designed specifically to undergo rigorous formal critique against quantum scrambling.
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
    
    # Lorenz attractor parameters (classical deterministic chaos)
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0
    
    x, y, z = 0.1, 0.0, 0.0
    dt = 0.005
    steps = 120000
    
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0 + 30
    scale = 16.0

    for i in range(steps):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x += dx
        y += dy
        z += dz
        
        # 2D projection (x vs z)
        px = int(cx + x * scale)
        py = int(cy - (z - 25.0) * scale)
        
        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            idx = (py * WIDTH + px) * 3
            # Accumulate naive white/cyan line brightness
            buffer[idx] = min(255, buffer[idx] + 25)
            buffer[idx + 1] = min(255, buffer[idx + 1] + 35)
            buffer[idx + 2] = min(255, buffer[idx + 2] + 45)
            
    out_png = os.path.join(os.path.dirname(__file__), "study_036_draft_a_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[STUDY-036-A] Generated: {out_png}")

if __name__ == "__main__":
    render_draft_a()

