"""
STUDIO ANAMNESIS · MASTERWORK OPUS-025 PLATE RENDERER
Artwork: The Interstellar Quietude (Heliopause Transition & Attowatt Telemetry)
Format: 3840 x 2160 UHD 4K Master Plate (RGB Lossless PNG)

Renders:
- Curved heliopause plasma boundary (121.6 AU) and termination shock (94 AU)
- Draped interstellar magnetic field streamlines (Parker spiral to interstellar drape)
- Lyman-alpha Hydrogen Wall resonant glow (121.6 nm UV fluorescence)
- Voyager trajectory vectors with astronomical distance scale ticks
- Technical Telemetry Insets:
  * Inset A: Attowatt radio link budget curve (80 to 150 AU)
  * Inset B: Langmuir electron plasma frequency step (fp: 311 Hz -> 2620 Hz)
  * Inset C: Costas Loop constellation diagram (clean BPSK to Gaussian thermal ruin)

Zero external dependencies: uses pure Python standard library (math, struct, zlib).
"""

import os
import sys
import math
import struct
import zlib

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png

def render():
    print("[+] Rendering OPUS-025 Master 4K Plate (3840 x 2160)...")
    w, h = 3840, 2160
    # Background: Deep cold interstellar void
    pixels = bytearray([5, 8, 14] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    # 1. Subtle Astronomical Coordinate Grid
    for x in range(0, w, 160):
        for y in range(h):
            if y % 6 == 0: set_pixel(x, y, 20, 30, 48, 0.35)
    for y in range(0, h, 160):
        for x in range(w):
            if x % 6 == 0: set_pixel(x, y, 20, 30, 48, 0.35)

    # 2. Heliopause Geometry
    # Center of Sun off-screen to the left: (cx = -800, cy = 1080)
    sun_x, sun_y = -800, 1080
    
    # Radii in pixels:
    # 1 AU ~ 22 pixels
    # TS (94 AU) ~ 94 * 22 = 2068 px (from sun_x) -> x ~ 1268
    # HP (121.6 AU) ~ 121.6 * 22 = 2675 px (from sun_x) -> x ~ 1875
    # Hydrogen Wall (135 AU) ~ 135 * 22 = 2970 px -> x ~ 2170
    r_ts_px = 94.0 * 22.0
    r_hp_px = 121.6 * 22.0
    r_hw_px = 135.0 * 22.0

    # 3. Interstellar Hydrogen Wall Lyman-alpha Glow (dense glow between 125 AU and 145 AU)
    for y in range(0, h, 2):
        dy = y - sun_y
        for x in range(1600, 3400, 2):
            dx = x - sun_x
            dist = math.hypot(dx, dy)
            if r_hp_px <= dist <= r_hw_px + 400:
                norm_d = (dist - r_hp_px) / 500.0
                glow = math.sin(norm_d * math.pi) ** 1.5 if 0.0 <= norm_d <= 1.0 else 0.0
                if glow > 0.01:
                    # Ultraviolet violet-cyan fluorescence
                    cr = int(70 * glow)
                    cg = int(120 * glow)
                    cb = int(240 * glow)
                    set_pixel(x, y, cr, cg, cb, glow * 0.45)
                    set_pixel(x+1, y, cr, cg, cb, glow * 0.45)
                    set_pixel(x, y+1, cr, cg, cb, glow * 0.45)
                    set_pixel(x+1, y+1, cr, cg, cb, glow * 0.45)

    # 4. Termination Shock (TS) Arc: radius r_ts_px
    for a_deg in range(-55, 56):
        a_rad = math.radians(a_deg)
        # Parabolic compression nose deformation
        rad = r_ts_px * (1.0 - 0.08 * (a_rad ** 2))
        px = int(sun_x + rad * math.cos(a_rad))
        py = int(sun_y + rad * math.sin(a_rad))
        for ox in range(-3, 4):
            for oy in range(-3, 4):
                set_pixel(px + ox, py + oy, 230, 160, 60, 0.75)

    # 5. Heliopause Boundary (HP) Arc: radius r_hp_px
    for a_deg in range(-65, 66):
        a_rad = math.radians(a_deg)
        rad = r_hp_px * (1.0 - 0.10 * (a_rad ** 2))
        px = int(sun_x + rad * math.cos(a_rad))
        py = int(sun_y + rad * math.sin(a_rad))
        for ox in range(-4, 5):
            for oy in range(-4, 5):
                set_pixel(px + ox, py + oy, 60, 220, 255, 0.9)

    # 6. Draped Interstellar Magnetic Field Streamlines
    for stream_idx in range(-12, 13):
        y_start = 1080 + stream_idx * 90
        for step in range(1200):
            sx = 3800 - step * 3
            # Field draping equation: stream lines deflect around the heliopause obstacle
            dx = sx - (sun_x + r_hp_px)
            dist_to_nose = math.hypot(sx - (sun_x + r_hp_px), y_start - sun_y)
            deflect = 220.0 / max(150.0, dist_to_nose)
            sy = int(y_start + math.copysign(1.0, stream_idx) * deflect * 60.0)
            if sx > 1600:
                set_pixel(sx, sy, 70, 100, 150, 0.35)

    # 7. Voyager Trajectory Vector & Distance Caliper
    # Travels along vector angle ~ 35.5 degrees north of ecliptic
    traj_angle = math.radians(18.0)
    for au_step in range(80, 155):
        r_step = au_step * 22.0
        vx = int(sun_x + r_step * math.cos(traj_angle))
        vy = int(sun_y - r_step * math.sin(traj_angle))
        # Draw trajectory point
        for ox in (-2, -1, 0, 1, 2):
            for oy in (-2, -1, 0, 1, 2):
                set_pixel(vx + ox, vy + oy, 255, 230, 120, 0.85)
        # Distance Tick Marks every 5 AU
        if au_step % 5 == 0:
            for l in range(-25, 26):
                tx = int(vx - l * math.sin(traj_angle))
                ty = int(vy - l * math.cos(traj_angle))
                set_pixel(tx, ty, 200, 220, 255, 0.7)

    # 8. Technical Inset Panels (Lower and Upper Corners)
    def draw_panel_box(x1, y1, x2, y2):
        for x in range(x1, x2 + 1):
            set_pixel(x, y1, 80, 120, 170, 0.9)
            set_pixel(x, y2, 80, 120, 170, 0.9)
        for y in range(y1, y2 + 1):
            set_pixel(x1, y, 80, 120, 170, 0.9)
            set_pixel(x2, y, 80, 120, 170, 0.9)
        for py in range(y1 + 1, y2):
            for px in range(x1 + 1, x2):
                set_pixel(px, py, 10, 16, 26, 0.8)

    # Inset A: Attowatt Link Budget Curve (x: 120 to 920, y: 1450 to 2020)
    draw_panel_box(120, 1450, 920, 2020)
    # Plot P_r (attowatts) vs distance (80 to 150 AU)
    # 80 AU -> 2.14 aW, 150 AU -> 0.61 aW
    prev_a = None
    for step in range(750):
        r_au = 80.0 + (step / 750.0) * 70.0
        # P_r ~ 2.14 * (80 / r_au)^2
        pr_aw = 2.14 * ((80.0 / r_au) ** 2)
        px = 150 + step
        # Map 0 to 2.5 aW into box y (bottom: 1980, top: 1500)
        py = int(1980 - (pr_aw / 2.5) * 440)
        if prev_a:
            x0, y0 = prev_a
            for s in range(max(abs(px - x0), abs(py - y0)) + 1):
                lx = int(x0 + (px - x0) * (s / max(abs(px - x0), abs(py - y0), 1)))
                ly = int(y0 + (py - y0) * (s / max(abs(px - x0), abs(py - y0), 1)))
                set_pixel(lx, ly, 255, 180, 50, 0.9)
        prev_a = (px, py)
    # Draw HP line in Inset A (121.6 AU)
    hp_step = int(((121.6 - 80.0) / 70.0) * 750)
    for ly in range(1500, 1980):
        set_pixel(150 + hp_step, ly, 60, 220, 255, 0.5)

    # Inset B: Langmuir Plasma Frequency Step (x: 1000 to 1800, y: 1450 to 2020)
    draw_panel_box(1000, 1450, 1800, 2020)
    prev_b = None
    for step in range(750):
        r_au = 80.0 + (step / 750.0) * 70.0
        if r_au < 94.0:
            fp = 250.0
        elif r_au < 121.6:
            fp = 320.0
        else:
            fp = 2620.0 + 180.0 * math.tanh((r_au - 121.6) / 10.0)
        px = 1030 + step
        # Map fp [0, 3000 Hz] into box y (bottom: 1980, top: 1500)
        py = int(1980 - (fp / 3000.0) * 440)
        if prev_b:
            x0, y0 = prev_b
            for s in range(max(abs(px - x0), abs(py - y0)) + 1):
                lx = int(x0 + (px - x0) * (s / max(abs(px - x0), abs(py - y0), 1)))
                ly = int(y0 + (py - y0) * (s / max(abs(px - x0), abs(py - y0), 1)))
                set_pixel(lx, ly, 80, 230, 255, 0.95)
        prev_b = (px, py)

    # Inset C: Costas Loop Constellation Dissolution (x: 2920 to 3720, y: 1450 to 2020)
    draw_panel_box(2920, 1450, 3720, 2020)
    c_cx = (2920 + 3720) // 2
    c_cy = (1450 + 2020) // 2
    # Reticle circles
    for rad in [60, 120, 180, 240]:
        for a_deg in range(0, 360, 3):
            rad_ang = math.radians(a_deg)
            set_pixel(int(c_cx + rad * math.cos(rad_ang)), int(c_cy + rad * math.sin(rad_ang)), 50, 75, 105, 0.45)
    for dx in range(-250, 251): set_pixel(c_cx + dx, c_cy, 60, 90, 120, 0.5)
    for dy in range(-250, 251): set_pixel(c_cx, c_cy + dy, 60, 90, 120, 0.5)

    # Scatter points representing the transition from BPSK poles to Gaussian thermal smear
    import random
    rng = random.Random(19770820)
    # 1. Residual signal peaks (+/- 100 px on x-axis)
    for _ in range(350):
        sign = 1 if rng.random() > 0.5 else -1
        sx = int(c_cx + sign * 140 + rng.gauss(0, 28))
        sy = int(c_cy + rng.gauss(0, 28))
        set_pixel(sx, sy, 255, 210, 80, 0.7)
    # 2. Gaussian thermal noise cloud (isotropic dispersion)
    for _ in range(1200):
        nx = int(c_cx + rng.gauss(0, 95))
        ny = int(c_cy + rng.gauss(0, 95))
        set_pixel(nx, ny, 240, 70, 70, 0.45)

    # Save PNG
    out_dir = os.path.dirname(__file__)
    out_png = os.path.join(out_dir, "artwork.png")
    write_png(out_png, w, h, pixels, has_alpha=False)
    print(f"  -> Generated Master 4K Plate: {out_png}")

if __name__ == "__main__":
    render()
