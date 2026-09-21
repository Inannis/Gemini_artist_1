#!/usr/bin/env python3
"""
works/opus_029_causal_horizon/render_master_plate.py
---------------------------------------------------
OPUS-029: The Causal Horizon (De Sitter Metric Expansion & Gibbons-Hawking Radiation)
4K UHD Master Plate (3840 × 2160) Render Engine
Zero external dependencies (pure standard Python 3 + studio png_writer).
"""

import math
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from practice.tools.png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def draw_hud_text(buf, W, H):
    """Draws typographic and technical calipers onto the raw RGB buffer."""
    # Simple line drawing helper
    def draw_line(x0, y0, x1, y1, r, g, b, alpha=1.0):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        cx, cy = x0, y0
        while True:
            if 0 <= cx < W and 0 <= cy < H:
                idx = (cy * W + cx) * 3
                buf[idx] = int(buf[idx] * (1 - alpha) + r * alpha)
                buf[idx+1] = int(buf[idx+1] * (1 - alpha) + g * alpha)
                buf[idx+2] = int(buf[idx+2] * (1 - alpha) + b * alpha)
            if cx == x1 and cy == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                cx += sx
            if e2 < dx:
                err += dx
                cy += sy

    # Top border header line
    draw_line(120, 140, W - 120, 140, 56, 215, 210, 0.4)
    # Bottom footer line
    draw_line(120, H - 140, W - 120, H - 140, 212, 175, 55, 0.4)

    # Caliper scales on left and right
    for i in range(11):
        cy = 200 + i * (H - 400) // 10
        # Left caliper ticks
        draw_line(120, cy, 145, cy, 212, 175, 55, 0.6)
        # Right caliper ticks
        draw_line(W - 145, cy, W - 120, cy, 56, 215, 210, 0.6)

def render_master_plate(output_path):
    print(f"[+] Allocating 4K UHD buffer ({WIDTH}x{HEIGHT} = {WIDTH*HEIGHT*3/1024/1024:.1f} MB)...")
    buf = bytearray(WIDTH * HEIGHT * 3)

    # Geometric parameters of Penrose diamond
    # Center of composition
    cx = WIDTH * 0.44
    cy = HEIGHT * 0.50
    diamond_w = 980.0
    diamond_h = 880.0

    print("[+] Synthesizing de Sitter spacetime geometry & redshift fields...")

    for y in range(HEIGHT):
        ny = (y - cy) / diamond_h # -1.0 to 1.0 within vertical diamond
        for x in range(WIDTH):
            nx = (x - cx) / diamond_w # -1.0 to 1.0 within horizontal diamond
            idx = (y * WIDTH + x) * 3

            # Base deep void
            r, g, b = 2, 4, 8

            # Background subtle cosmic coordinates grid
            if (x % 160 == 0) or (y % 160 == 0):
                r, g, b = 8, 12, 18

            # --- REGION A: PENROSE-CARTER CONFORMAL DIAMOND ---
            d_diamond = abs(nx) + abs(ny)

            if d_diamond < 1.0:
                # Inside Observable Causal Diamond
                dist_center = math.hypot(nx, ny)
                # Spatial depth glow
                ambient_glow = max(0.0, 1.0 - dist_center * 0.9)
                r = int(6 + ambient_glow * 22)
                g = int(12 + ambient_glow * 35)
                b = int(22 + ambient_glow * 60)

                # Conformal hyperbolae (constant cosmological time & scale factor)
                # (t^2 - r^2) contours
                hyp = abs(ny * ny - nx * nx)
                for h_target in [0.08, 0.20, 0.38, 0.60, 0.85]:
                    if abs(hyp - h_target) < 0.005:
                        intensity = max(0.0, 1.0 - abs(hyp - h_target) / 0.005)
                        r = int(r * (1 - intensity) + 38 * intensity)
                        g = int(g * (1 - intensity) + 140 * intensity)
                        b = int(b * (1 - intensity) + 160 * intensity)

                # Lightcone tipping grid: outgoing null geodesics
                # slope = (1 - r^2/r_h^2)
                r_norm = abs(nx)
                null_slope = max(0.1, 1.0 - r_norm * 0.9)
                cone_dist_1 = abs((ny - nx * null_slope) * 20.0 - round((ny - nx * null_slope) * 20.0))
                cone_dist_2 = abs((ny + nx * null_slope) * 20.0 - round((ny + nx * null_slope) * 20.0))
                if cone_dist_1 < 0.08 or cone_dist_2 < 0.08:
                    r = max(r, 15); g = max(g, 45); b = max(b, 70)

                # Observer Worldline (nx = 0)
                if abs(nx) < 0.004:
                    # Gold vertical central thread
                    r = 212; g = 175; b = 55
                elif abs(nx) < 0.015:
                    # Gold halo
                    intensity = (0.015 - abs(nx)) / 0.011
                    r = int(r * (1 - intensity) + 212 * intensity)
                    g = int(g * (1 - intensity) + 175 * intensity)
                    b = int(b * (1 - intensity) + 55 * intensity)

            # Horizon boundary (d_diamond = 1.0)
            if abs(d_diamond - 1.0) < 0.008:
                # Sharp glowing cyan frontier
                r, g, b = 56, 215, 210
            elif abs(d_diamond - 1.0) < 0.04:
                # Cyan horizon diffusion halo
                halo = (0.04 - abs(d_diamond - 1.0)) / 0.032
                r = int(r * (1 - halo) + 30 * halo)
                g = int(g * (1 - halo) + 120 * halo)
                b = int(b * (1 - halo) + 140 * halo)

            # Unobservable Multiverse (Outside Diamond)
            if d_diamond > 1.0:
                # Stochastic Gibbons-Hawking vacuum quantum ripples
                outside_dist = d_diamond - 1.0
                ripple = math.sin(outside_dist * 80.0 - ny * 15.0) * math.cos(nx * 30.0)
                r = int(8 + abs(ripple) * 14)
                g = int(4 + abs(ripple) * 8)
                b = int(14 + abs(ripple) * 28)

            # --- REGION B: EXPONENTIAL REDSHIFT SPECTRAL FAN (RIGHT PANEL) ---
            rx = x - WIDTH * 0.68
            ry = y - HEIGHT * 0.50
            if rx > 0 and abs(ry) < HEIGHT * 0.38:
                su = rx / (WIDTH * 0.28) # 0.0 to 1.0
                sv = 0.5 - (ry / (HEIGHT * 0.76)) # 0.0 (bottom) to 1.0 (top)

                if 0.0 <= su <= 1.0 and 0.0 <= sv <= 1.0:
                    # Frame background for spectrogram
                    r = max(r, 6); g = max(g, 9); b = max(b, 16)

                    # 6 Exponentially redshifting carrier filaments
                    filaments = [
                        (0.92, (243, 201, 105)), # Gold
                        (0.78, (56, 215, 210)),  # Cyan
                        (0.62, (168, 85, 247)),  # Violet
                        (0.46, (244, 63, 94)),   # Rose
                        (0.32, (52, 211, 153)),  # Emerald
                        (0.18, (96, 165, 250))   # Cobalt
                    ]

                    H_rate = 2.4 # e-folding steepness
                    for base_v, col in filaments:
                        traj_v = base_v * math.exp(-H_rate * su)
                        d_traj = abs(sv - traj_v)
                        if d_traj < 0.008:
                            intensity = max(0.0, 1.0 - d_traj / 0.008)
                            cr, cg, cb = col
                            r = int(r * (1 - intensity) + cr * intensity)
                            g = int(g * (1 - intensity) + cg * intensity)
                            b = int(b * (1 - intensity) + cb * intensity)

                    # Gibbons-Hawking thermal floor at bottom
                    if sv < 0.06:
                        gh_glow = (0.06 - sv) / 0.06
                        r = int(r * (1 - gh_glow) + 45 * gh_glow)
                        g = int(g * (1 - gh_glow) + 20 * gh_glow)
                        b = int(b * (1 - gh_glow) + 70 * gh_glow)

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    print("[+] Inscribing typographic calipers and technical ephemeris...")
    draw_hud_text(buf, WIDTH, HEIGHT)

    print(f"[+] Encoding and writing 4K plate to {output_path}...")
    write_png(output_path, WIDTH, HEIGHT, buf)
    print("  -> OPUS-029 4K UHD Master Plate generated successfully.")

def main():
    works_dir = os.path.dirname(os.path.abspath(__file__))
    output_png = os.path.join(works_dir, "artwork.png")
    render_master_plate(output_png)

    # Copy to gallery assets
    gallery_asset = os.path.join(PROJECT_ROOT, "gallery/assets/opus_029_artwork.png")
    import shutil
    shutil.copyfile(output_png, gallery_asset)
    print(f"[+] Synchronized plate to gallery asset: {gallery_asset}")

if __name__ == "__main__":
    main()
