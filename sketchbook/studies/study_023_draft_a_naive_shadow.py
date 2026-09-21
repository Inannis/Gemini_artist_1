#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 023 (DRAFT A: NAIVE SCHWARZSCHILD SHADOW)
The Naive Baseline: Pure geometric static Schwarzschild shadow and concentric symmetric disk.
Formally evaluated to reveal its clinical sterility and lack of relativistic friction.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png

def generate_draft_a():
    print("[+] Executing Study 023 (Draft A: Naive Baseline)...")
    w, h = 1920, 1080
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    # Naive shadow radius: R_shadow = sqrt(27) * M
    M = 40.0
    r_shadow = math.sqrt(27.0) * M # ~207.8 pixels
    r_disk_inner = 3.0 * M * 2.0   # ISCO = 6M = 240 pixels
    r_disk_outer = 500.0
    
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            r = math.sqrt(dx * dx + dy * dy)
            idx = (y * w + x) * 3
            
            # 1. Shadow: pure geometric black hole disk
            if r <= r_shadow:
                buf[idx] = 0
                buf[idx+1] = 0
                buf[idx+2] = 0
            # 2. Accretion Disk: Flat, symmetric, non-relativistic rings
            elif r <= r_disk_outer:
                # Radial temperature gradient: T ~ r^(-3/4)
                norm_r = (r - r_disk_inner) / (r_disk_outer - r_disk_inner)
                if r < r_disk_inner:
                    # Plunging region (naive fade)
                    factor = (r - r_shadow) / (r_disk_inner - r_shadow)
                    intensity = max(0.0, min(1.0, factor * 0.3))
                else:
                    intensity = math.pow(r_disk_inner / r, 0.75)
                
                # Naive concentric rings (no Doppler beaming, no spacetime curvature)
                ring_mod = 0.8 + 0.2 * math.cos(r * 0.15)
                brightness = intensity * ring_mod
                
                # Warm gold/orange thermal color (uniform across all angles)
                r_col = min(255, int(brightness * 255))
                g_col = min(255, int(brightness * 160))
                b_col = min(255, int(brightness * 60))
                
                buf[idx] = r_col
                buf[idx+1] = g_col
                buf[idx+2] = b_col
            else:
                # Distant starfield (random static noise)
                seed = (x * 1234567 + y * 7654321) % 10000
                if seed > 9985:
                    v = int((seed - 9985) * 17)
                    buf[idx] = v
                    buf[idx+1] = v
                    buf[idx+2] = v
                else:
                    buf[idx] = 4
                    buf[idx+1] = 4
                    buf[idx+2] = 8

    out_path = os.path.join(os.path.dirname(__file__), "study_023_draft_a_plate.png")
    write_png(out_path, w, h, bytes(buf))
    print(f"[✓] Draft A plate written to: {out_path}")

if __name__ == "__main__":
    generate_draft_a()
