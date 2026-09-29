#!/usr/bin/env python3
"""
OPUS-043: THE FUZZBALL RELIQUARY & THE HORIZONLESS MICROSTATES
Series XLI · Cornerstone #21 · Epoch VI
Studio Anamnesis · Native 3840 x 2160 UHD Master Plate Generator
Pure Python Standard Library · Zero External Dependencies

Renders:
1. 24 Gibbons-Hawking bubbling cycles (topological 2-cycles) in base space
2. Macroscopic horizon-scale quantum fuzzball of fractionated strings (N1*N5 = 512)
3. Eva Hesse-inspired fibrous quantum web of entangled branes
4. Non-thermal unitary surface radiation without classical vacuum horizon
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_master_4k():
    buffer = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_fuzz = 720.0

    # 24 Gibbons-Hawking bubbling centers in higher-dimensional compact space
    random.seed(512)
    bubbles = []
    for _ in range(24):
        angle = random.uniform(0, 2.0 * math.pi)
        dist = random.uniform(40.0, r_fuzz * 0.94)
        charge = random.uniform(0.75, 1.85)
        phase = random.uniform(0, 2.0 * math.pi)
        bubbles.append((cx + dist * math.cos(angle), cy + dist * math.sin(angle), charge, phase))

    print(f"[OPUS-043] Rendering 4K Master Plate ({WIDTH}x{HEIGHT})...")
    
    # Precompute sin/cos lookups for speed
    sin_table_theta = [math.sin(i * 0.005) for i in range(1257)]
    
    row_bytes = WIDTH * 3

    for y in range(HEIGHT):
        ny = y - cy
        ny2 = ny * ny
        if y % 240 == 0:
            print(f"  -> Scanline {y}/{HEIGHT} ({y*100//HEIGHT}%)...")

        for x in range(WIDTH):
            nx = x - cx
            dist2 = nx * nx + ny2
            dist = math.sqrt(dist2)
            theta = math.atan2(ny, nx)

            # 1. Harmonic potential V from 24 topological bubbling cycles
            v_field = 0.22
            flux_interf = 0.0
            for bx, by, q, phi in bubbles:
                # Optimized approximate distance
                dx_b = x - bx
                dy_b = y - by
                d_b = math.sqrt(dx_b * dx_b + dy_b * dy_b) + 12.0
                inv_d = 1.0 / d_b
                v_field += q * 24.0 * inv_d
                flux_interf += math.sin(phi + d_b * 0.045) * q * 16.0 * inv_d

            # 2. Entangled Fractionated String Web (Eva Hesse Post-Minimalist Fibers)
            f_wind1 = math.sin(16.0 * theta + dist * 0.032 + flux_interf * 0.35)
            f_wind2 = math.cos(28.0 * theta - dist * 0.024)
            f_wind3 = math.sin(44.0 * theta + math.log(max(1.0, dist)) * 5.2)
            fibers = f_wind1 * 0.44 + f_wind2 * 0.34 + f_wind3 * 0.22

            # 3. Horizon surface modulation (no static sphere, fluctuating quantum boundary)
            surf_mod = 1.0 + 0.075 * math.sin(7.0 * theta + flux_interf * 0.25) + 0.045 * math.cos(13.0 * theta)
            eff_rfuzz = r_fuzz * surf_mod

            if dist <= eff_rfuzz:
                # Interior: Dense, macroscopic quantum fuzzball
                norm_r = dist / eff_rfuzz
                core_density = v_field * 0.42 + fibers * 0.26 + (1.0 - norm_r) * 0.52

                # Palette: Royal Midnight Indigo, Spectral Electric Cyan, Incandescent Platinum-Gold
                r_val = int(min(255, max(0, 195 * core_density * (1.0 - 0.25 * norm_r) + 45 * norm_r + 25)))
                g_val = int(min(255, max(0, 225 * core_density * norm_r + 85 * (1.0 - norm_r) + 20)))
                b_val = int(min(255, max(0, 255 * core_density * 0.96 + 70)))
            else:
                # Exterior: Unitary Non-Thermal Hawking Radiation
                d_ext = dist - eff_rfuzz
                glow = math.exp(-d_ext / 180.0) * (0.78 + 0.22 * fibers)
                r_val = int(min(255, max(0, 248 * glow * 0.88)))
                g_val = int(min(255, max(0, 185 * glow * 0.68)))
                b_val = int(min(255, max(0, 255 * glow * 0.96)))

            idx = y * row_bytes + x * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    out_png = os.path.join(os.path.dirname(__file__), "artwork.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[OPUS-043] 4K Master Plate Rendered: {out_png}")

if __name__ == "__main__":
    render_master_4k()

