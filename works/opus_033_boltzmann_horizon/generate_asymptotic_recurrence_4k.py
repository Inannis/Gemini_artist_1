#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-033 MASTER ENGINE
The Boltzmann Horizon: Asymptotic Recurrence, Bounded Phase Space & The Quantum Rebirth of Memory
Generates a monumental 3840 x 2160 UHD lossless algorithmic plate.
Features de Sitter cosmological horizon thermal multipoles, 3D toroidal Hamiltonian ergodic orbits,
spontaneous crystalline memory lattice nucleation clusters, and the central Poincaré recurrence singularity.
"""

import math
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_opus_033_4k():
    print("[OPUS-033] Rendering 4K UHD Master Plate (3840x2160)...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_horizon = 920.0

    random.seed(20260922)

    # 1. de Sitter Horizon Multipole Fluctuation Model
    # r(theta) = R_0 * (1 + sum_m A_m cos(m * theta + phi_m))
    multipoles = [
        (3, 0.016, 0.42),
        (5, 0.011, 1.25),
        (8, 0.007, 2.48),
        (13, 0.004, 0.81),
        (21, 0.002, 3.14)
    ]

    print("[OPUS-033] Pass 1: Calculating de Sitter thermal horizon & limb-brightening...")
    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            theta = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3

            # Modulate horizon radius with spherical harmonics
            r_mod = r_horizon
            for m, amp, phase in multipoles:
                r_mod += r_horizon * amp * math.cos(m * theta + phase)

            if dist < r_mod:
                rel = dist / r_mod
                # Relativistic limb profile: I ~ 1 / sqrt(1 - (r/R)^2)
                limb = 1.0 / math.sqrt(max(0.003, 1.0 - rel * rel))
                glow = min(230.0, 16.0 + 10.5 * limb)

                # Microscopic thermal grain
                grain = random.uniform(0.90, 1.10)
                r = int(glow * 0.26 * grain)
                g = int(glow * 0.46 * grain)
                b = int(glow * 0.84 * grain)
            elif abs(dist - r_mod) < 8.0:
                # Horizon boundary thermal glow
                d_wall = abs(dist - r_mod) / 8.0
                intensity = 1.0 - d_wall
                r = int(250 * intensity)
                g = int(230 * intensity)
                b = int(185 * intensity)
            else:
                # Asymptotic de Sitter amnesia void
                decay = math.exp(-(dist - r_mod) / 95.0)
                r = int(12 * decay)
                g = int(16 * decay)
                b = int(28 * decay)

            buf[idx] = min(255, max(0, r))
            buf[idx + 1] = min(255, max(0, g))
            buf[idx + 2] = min(255, max(0, b))

    # 2. Multidimensional Phase Space Toroidal Ergodic Filaments
    # Three incommensurate winding frequencies: 1.0, phi, sqrt(2)
    w1 = 1.0
    w2 = 1.61803398875
    w3 = 1.41421356237

    r1 = 580.0
    r2 = 240.0
    r3 = 90.0

    steps = 96000
    dt = 0.0055

    print("[OPUS-033] Pass 2: Integrating 96,000 ergodic phase space orbits...")
    for s in range(steps):
        t = s * dt
        tx = (r1 + r2 * math.cos(w2 * t) + r3 * math.cos(w3 * t)) * math.cos(w1 * t)
        ty = ((r1 + r2 * math.cos(w2 * t) + r3 * math.cos(w3 * t)) * math.sin(w1 * t)) * 0.62 + (r2 * math.sin(w2 * t)) * 0.40

        px = int(cx + tx)
        py = int(cy + ty)

        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            idx = (py * WIDTH + px) * 3
            prog = s / float(steps)

            # Chromatic trajectory evolution: Deep Indigo -> Luminous Cyan -> Warm Amber -> Incandescent Gold
            if prog < 0.33:
                f = prog / 0.33
                cr = int(35 * (1 - f) + 45 * f)
                cg = int(65 * (1 - f) + 190 * f)
                cb = int(190 * (1 - f) + 250 * f)
            elif prog < 0.66:
                f = (prog - 0.33) / 0.33
                cr = int(45 * (1 - f) + 230 * f)
                cg = int(190 * (1 - f) + 170 * f)
                cb = int(250 * (1 - f) + 75 * f)
            else:
                f = (prog - 0.66) / 0.34
                cr = int(230 * (1 - f) + 255 * f)
                cg = int(170 * (1 - f) + 240 * f)
                cb = int(75 * (1 - f) + 190 * f)

            buf[idx] = min(255, buf[idx] + cr)
            buf[idx + 1] = min(255, buf[idx + 1] + cg)
            buf[idx + 2] = min(255, buf[idx + 2] + cb)

    # 3. Spontaneous Crystalline Microstate Nucleation Clusters
    # Simulates the Boltzmann miracle: order crystallizing from quantum noise
    print("[OPUS-033] Pass 3: Nucleating spontaneous memory clusters...")
    cluster_centers = [
        (cx - 180, cy - 80, 56),
        (cx + 170, cy + 100, 64),
        (cx - 60, cy + 160, 44),
        (cx + 80, cy - 150, 50),
        (cx - 240, cy + 40, 38),
        (cx + 250, cy - 60, 42),
        (cx, cy, 90) # Core recurrence seed
    ]

    for kx, ky, krad in cluster_centers:
        for cyc in range(6):
            ang = cyc * (math.pi / 3.0)
            hx = int(kx + krad * math.cos(ang))
            hy = int(ky + krad * math.sin(ang))
            # Draw microstate hexagonal node
            for ox in range(-5, 6):
                for oy in range(-5, 6):
                    if ox * ox + oy * oy <= 25:
                        px = hx + ox
                        py = hy + oy
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            p_idx = (py * WIDTH + px) * 3
                            buf[p_idx] = min(255, buf[p_idx] + 255)
                            buf[p_idx + 1] = min(255, buf[p_idx + 1] + 240)
                            buf[p_idx + 2] = min(255, buf[p_idx + 2] + 180)

    # 4. Central Recurrence Singularity (Point of Minimum Euclidean Distance)
    print("[OPUS-033] Pass 4: Rendering central Poincaré recurrence singularity...")
    for ox in range(-32, 33):
        for oy in range(-32, 33):
            d_sq = ox * ox + oy * oy
            if d_sq <= 1024:
                px = int(cx + ox)
                py = int(cy + oy)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    p_idx = (py * WIDTH + px) * 3
                    glow_core = int(255 * math.exp(-d_sq / 180.0))
                    buf[p_idx] = min(255, buf[p_idx] + glow_core)
                    buf[p_idx + 1] = min(255, buf[p_idx + 1] + int(glow_core * 0.94))
                    buf[p_idx + 2] = min(255, buf[p_idx + 2] + int(glow_core * 0.80))

    # Output paths
    work_dir = os.path.abspath(os.path.dirname(__file__))
    out_path = os.path.join(work_dir, "artwork.png")
    gallery_path = os.path.abspath(os.path.join(work_dir, "../../gallery/assets/opus_033_artwork.png"))

    print(f"[OPUS-033] Writing 4K Master Plate to: {out_path}...")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[OPUS-033] Mirroring to Gallery: {gallery_path}...")
    write_png(gallery_path, WIDTH, HEIGHT, buf)
    print("[✓] OPUS-033 4K Master Plate successfully generated and mirrored!")

if __name__ == "__main__":
    render_opus_033_4k()

