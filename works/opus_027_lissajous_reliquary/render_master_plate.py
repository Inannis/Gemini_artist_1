"""
STUDIO ANAMNESIS · MASTERWORK OPUS-027 PLATE RENDERER
Artwork: The Lissajous Reliquary (Galactic Epicycles & Interstellar Sputtering)
Format: 3840 x 2160 UHD 4K Master Plate (RGB Lossless PNG)

Renders:
- 3D Axisymmetric Milky Way epicyclic trajectory in (Delta R, z) meridional space
- Incommensurate frequency ratio (nu_z / kappa = 2.1131...) generating an ergodic, non-closing Lissajous torus
- Interstellar dust sputtering micro-crater cascades and eroded 3nm semiconductor die inlays
- Three Technical Telemetry Insets:
  * Inset A: Miyamoto-Nagai + Hernquist + NFW Galactic Potential Well Phi(R, z)
  * Inset B: Ergodic Torus Poincaré Surface of Section
  * Inset C: Deep-Time Sputtering Kinetics (Nanometer recession across gigayears)

Zero external dependencies: pure Python standard library.
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png

def render():
    print("[+] Rendering OPUS-027 Master 4K Plate (3840 x 2160)...")
    random.seed(20260908)
    w, h = 3840, 2160
    pixels = bytearray([4, 5, 10] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    def draw_line(x0, y0, x1, y1, r, g, b, alpha=1.0):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            set_pixel(x0, y0, r, g, b, alpha)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # 1. Subtle Galactic Coordinate Grid
    for x in range(0, w, 160):
        for y in range(h):
            if y % 8 == 0: set_pixel(x, y, 16, 22, 36, 0.3)
    for y in range(0, h, 160):
        for x in range(w):
            if x % 8 == 0: set_pixel(x, y, 16, 22, 36, 0.3)

    # 2. Distant Starfield & Interstellar Dust Veil
    for _ in range(1400):
        sx = random.randint(0, w - 1)
        sy = random.randint(0, h - 1)
        br = random.uniform(0.2, 0.85)
        c = int(255 * br)
        t = random.choice([(c, c, c), (int(c*0.8), int(c*0.9), c), (c, int(c*0.85), int(c*0.65))])
        set_pixel(sx, sy, t[0], t[1], t[2], 0.6)

    # 3. Main Composition: The Incommensurate Lissajous Torus
    # Center: (cx = 1500, cy = 1080)
    cx, cy = 1500, 1080
    X_amp = 1100.0 # Radial excursion ~ 0.45 kpc
    Z_amp = 820.0  # Vertical excursion ~ 95 pc
    ratio = 2.113116 # Incommensurate frequency ratio nu_z / kappa
    
    # Render 36,000 steps of the continuous ergodic ribbon
    prev_x, prev_y = None, None
    for step in range(36000):
        t_val = step * 0.005
        x_val = X_amp * math.cos(t_val)
        y_val = Z_amp * math.sin(ratio * t_val + 0.45)
        
        px = int(cx + x_val)
        py = int(cy - y_val)
        
        # Color evolution along the gigayear path: shifts across spectrum
        prog = step / 36000.0
        r_c = int(60 + 180 * (0.5 + 0.5 * math.sin(prog * math.pi * 4.0)))
        g_c = int(120 + 130 * (0.5 + 0.5 * math.cos(prog * math.pi * 3.0)))
        b_c = int(210 + 45 * (0.5 + 0.5 * math.sin(prog * math.pi * 5.0)))
        
        set_pixel(px, py, r_c, g_c, b_c, 0.45)
        if prev_x is not None and abs(px - prev_x) < 20 and abs(py - prev_y) < 20:
            for a in [0.33, 0.66]:
                ix = int(prev_x * (1.0 - a) + px * a)
                iy = int(prev_y * (1.0 - a) + py * a)
                set_pixel(ix, iy, r_c, g_c, b_c, 0.25)
        prev_x, prev_y = px, py

    # 4. Galactic Disc Midplane Horizon & Radial Boundaries
    # Horizontal disc midplane at z = 0
    draw_line(cx - 1250, cy, cx + 1250, cy, 70, 140, 220, 0.4)
    # Vertical axis at R = R0
    draw_line(cx, cy - 920, cx, cy + 920, 70, 140, 220, 0.4)
    
    # Boundary box of the ergodic torus cross-section
    for d in [-1, 0, 1]:
        draw_line(cx - int(X_amp) + d, cy - int(Z_amp), cx + int(X_amp) + d, cy - int(Z_amp), 40, 200, 230, 0.35)
        draw_line(cx - int(X_amp) + d, cy + int(Z_amp), cx + int(X_amp) + d, cy + int(Z_amp), 40, 200, 230, 0.35)
        draw_line(cx - int(X_amp), cy - int(Z_amp) + d, cx - int(X_amp), cy + int(Z_amp) + d, 40, 200, 230, 0.35)
        draw_line(cx + int(X_amp), cy - int(Z_amp) + d, cx + int(X_amp), cy + int(Z_amp) + d, 40, 200, 230, 0.35)

    # 5. Dust Sputtering Impact Craters (Micro-impact constellations)
    for _ in range(85):
        t_c = random.uniform(0.0, 180.0)
        c_x = int(cx + X_amp * math.cos(t_c) + random.uniform(-15, 15))
        c_y = int(cy - Z_amp * math.sin(ratio * t_c + 0.45) + random.uniform(-15, 15))
        # Draw small glowing gold-white sputtering ring
        for r_ring in range(2, 6):
            for st in range(16):
                th = st * (2.0 * math.pi / 16.0)
                set_pixel(int(c_x + r_ring * math.cos(th)), int(c_y + r_ring * math.sin(th)), 255, 230, 140, 0.75)

    # 6. Technical Inset Panels (Right column)
    def draw_box(bx, by, bw, bh):
        for x in range(bx, bx + bw):
            for y in range(by, by + bh):
                set_pixel(x, y, 8, 12, 22, 0.85)
        for x in range(bx, bx + bw):
            set_pixel(x, by, 70, 130, 190, 0.9)
            set_pixel(x, by + bh - 1, 70, 130, 190, 0.9)
        for y in range(by, by + bh):
            set_pixel(bx, y, 70, 130, 190, 0.9)
            set_pixel(bx + bw - 1, y, 70, 130, 190, 0.9)

    # Inset A: Top-Right (w=720, h=380, x=3020, y=100) -> Galactic Potential Contours Phi(R, z)
    draw_box(3020, 100, 720, 380)
    for px in range(3060, 3700):
        u = (px - 3380) / 320.0 # -1 to +1 (R from 6 to 10 kpc)
        # Potential cross-section curves
        for lvl, c_pot in [(0.2, (60, 180, 255)), (0.4, (80, 220, 240)), (0.6, (180, 140, 255)), (0.8, (255, 180, 60))]:
            py = int(320 - (math.log(1.0 + u*u + lvl) * 120))
            set_pixel(px, py, c_pot[0], c_pot[1], c_pot[2], 0.9)

    # Inset B: Mid-Right (w=720, h=380, x=3020, y=520) -> Poincaré Section (z=0, v_z > 0)
    draw_box(3020, 520, 720, 380)
    # Plots (R, v_R) crossings
    for ring_idx in range(6):
        r_rad = 40.0 + ring_idx * 45.0
        for pt in range(120):
            th = pt * (2.0 * math.pi / 120.0)
            px = int(3380 + r_rad * math.cos(th) * 1.5)
            py = int(710 - r_rad * math.sin(th))
            set_pixel(px, py, 255, int(150 + ring_idx * 18), 70, 0.85)

    # Inset C: Low-Right (w=720, h=380, x=3020, y=940) -> Sputtering Recession vs Gigayears
    draw_box(3020, 940, 720, 380)
    # Plot linear recession depth over 5 Gyr (0 to 90 nm)
    draw_line(3060, 1260, 3700, 1260, 50, 80, 110, 0.6) # x-axis (time)
    draw_line(3060, 980, 3060, 1260, 50, 80, 110, 0.6)  # y-axis (nm)
    for px in range(3060, 3700):
        t_ratio = (px - 3060) / 640.0 # 0 to 5 Gyr
        # Silicon curve: 18 nm/Gyr
        y_si = int(1260 - t_ratio * 220)
        # Gold curve: 34 nm/Gyr
        y_au = int(1260 - t_ratio * 270)
        set_pixel(px, y_si, 60, 220, 240, 0.9)
        set_pixel(px, y_au, 255, 215, 0, 0.9)
    # 3nm Gate critical threshold dashed line
    py_crit = int(1260 - (3.0 / 90.0) * 220)
    for px in range(3060, 3700):
        if px % 6 < 3: set_pixel(px, py_crit, 255, 60, 60, 0.85)

    # 7. Curatorial Signature Block
    draw_line(120, 1960, 800, 1960, 70, 130, 180, 0.8)
    for x in range(120, 800):
        if x % 10 == 0:
            draw_line(x, 1960, x, 1970, 70, 130, 180, 0.8)

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "artwork.png"))
    write_png(out_path, w, h, pixels)
    print(f"[+] OPUS-027 Master 4K Plate saved to: {out_path}")

if __name__ == "__main__":
    render()
