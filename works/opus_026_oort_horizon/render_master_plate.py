"""
STUDIO ANAMNESIS · MASTERWORK OPUS-026 PLATE RENDERER
Artwork: The Oort Horizon (Galactic Tides & The Jacobi Boundary)
Format: 3840 x 2160 UHD 4K Master Plate (RGB Lossless PNG)

Renders:
- Gravitational potential field of the Sun perturbed by the Milky Way vertical tidal tensor
- Jacobi Tidal Radius contour (105,000 - 120,000 AU) establishing the solar gravitational horizon
- Inner Hills cloud (2,000 - 20,000 AU) and outer spherical Oort cloud shells
- Cometary Kozai-Lidov resonance ellipses undergoing eccentricity pumping
- Deep-time trajectories of humanity's five hyperbolic probes (Voyagers, Pioneers, New Horizons)
- Three Technical Telemetry Insets:
  * Inset A: Vertical disc harmonic oscillation Phi_z(z) over 83.6 Myr
  * Inset B: Kozai phase portrait (omega, e) libration regime
  * Inset C: Gravitational force equilibrium (a_sun vs a_tide)

Zero external dependencies: uses pure Python standard library.
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png

def render():
    print("[+] Rendering OPUS-026 Master 4K Plate (3840 x 2160)...")
    random.seed(42100)
    w, h = 3840, 2160
    # Background: Cold deep galactic space
    pixels = bytearray([4, 6, 12] * (w * h))
    
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
            if y % 8 == 0: set_pixel(x, y, 16, 24, 38, 0.3)
    for y in range(0, h, 160):
        for x in range(w):
            if x % 8 == 0: set_pixel(x, y, 16, 24, 38, 0.3)

    # 2. Stellar Background & Cosmic Dust
    for _ in range(1200):
        sx = random.randint(0, w - 1)
        sy = random.randint(0, h - 1)
        br = random.uniform(0.2, 0.9)
        c = int(255 * br)
        # slight tint
        t = random.choice([(c, c, c), (int(c*0.8), int(c*0.9), c), (c, int(c*0.9), int(c*0.7))])
        set_pixel(sx, sy, t[0], t[1], t[2], 0.7)

    # 3. Solar Center and Distance Coordinate Shells
    # Sun is centered horizontally, slightly left: cx = 1400, cy = 1080
    cx, cy = 1400, 1080
    
    # Radii in pixels (Log-linear mapping for astronomical scale):
    # Inner Hills cloud: 2,000 AU -> r ~ 220 px
    # Dense Hills Shell: 20,000 AU -> r ~ 480 px
    # Classical Outer Oort: 50,000 AU -> r ~ 780 px
    # Jacobi Horizon: 105,000 AU -> r_x ~ 1250 px, r_y ~ 950 px (compressed vertically by galactic tide)
    
    # 3a. Inner Hills Cloud Glow
    for step in range(3600):
        ang = step * (2.0 * math.pi / 3600.0)
        # Faint circular shells
        for r_base, col, alph in [
            (220, (180, 140, 70), 0.15),
            (480, (100, 160, 220), 0.18),
            (780, (70, 130, 200), 0.22)
        ]:
            rx = int(cx + r_base * math.cos(ang) + random.uniform(-2, 2))
            ry = int(cy + r_base * math.sin(ang) + random.uniform(-2, 2))
            set_pixel(rx, ry, col[0], col[1], col[2], alph)

    # 3b. Jacobi Tidal Horizon Contour (Roche-like teardrop / triaxial ellipsoid)
    # Compressed vertically along Z (Galactic Pole), elongated along X (Galactic Center)
    for step in range(7200):
        ang = step * (2.0 * math.pi / 7200.0)
        # R(ang) with tidal deformation: r = r0 * (1 + 0.22 * cos(2*ang))
        r_jacobi = 1150.0 * (1.0 + 0.18 * math.cos(2.0 * ang))
        jx = int(cx + r_jacobi * math.cos(ang))
        jy = int(cy + (r_jacobi * 0.78) * math.sin(ang))
        # Draw soft glow
        for d in range(-2, 3):
            set_pixel(jx + d, jy, 40, 220, 240, 0.45 - abs(d)*0.1)
            set_pixel(jx, jy + d, 40, 220, 240, 0.45 - abs(d)*0.1)

    # 4. Galactic Disc Midplane Projection
    # A glowing diffuse plane passing through the composition at angle theta = -15 deg
    disc_angle = math.radians(-12.0)
    cos_d, sin_d = math.cos(disc_angle), math.sin(disc_angle)
    for px in range(0, w, 2):
        # Line passing through cx, cy
        py_mid = int(cy + (px - cx) * math.tan(disc_angle))
        for dy in range(-45, 46):
            py = py_mid + dy
            if 0 <= py < h:
                dist = abs(dy) / 45.0
                intensity = math.exp(-dist * 2.5) * 0.25
                set_pixel(px, py, int(130 * intensity), int(180 * intensity), int(255 * intensity), intensity)

    # 5. Cometary Orbits Undergoing Kozai-Lidov Pumping
    # Draw highly eccentric elliptical orbits precessing under tidal torque
    num_orbits = 48
    for i in range(num_orbits):
        inc_ratio = i / float(num_orbits)
        a_semi = 400.0 + inc_ratio * 700.0
        ecc = 0.4 + 0.55 * math.sin(inc_ratio * math.pi)
        omega = inc_ratio * 2.0 * math.pi
        b_semi = a_semi * math.sqrt(max(0.01, 1.0 - ecc**2))
        
        col = (int(80 + 120 * ecc), int(160 + 80 * (1.0 - ecc)), int(220 * (1.0 - ecc*0.5)))
        for s in range(360):
            th = math.radians(s)
            # Ellipse coordinates centered at focus
            x_orb = a_semi * (math.cos(th) - ecc)
            y_orb = b_semi * math.sin(th)
            # Rotate by argument of perihelion omega and disc tilt
            x_rot = x_orb * math.cos(omega) - y_orb * math.sin(omega)
            y_rot = x_orb * math.sin(omega) + y_orb * math.cos(omega)
            
            px = int(cx + x_rot)
            py = int(cy + y_rot * 0.85) # vertical compression
            set_pixel(px, py, col[0], col[1], col[2], 0.35 * (0.3 + 0.7 * (1.0 - ecc*0.5)))

    # 6. Deep-Space Probe Trajectories (The Five Emissaries)
    probes = [
        ("Voyager 1", 3.57, math.radians(35.0), (255, 215, 0)),
        ("Voyager 2", 3.23, math.radians(-48.0), (100, 220, 255)),
        ("Pioneer 10", 2.51, math.radians(160.0), (255, 140, 60)),
        ("Pioneer 11", 2.36, math.radians(12.0), (200, 180, 255)),
        ("New Horizons", 2.91, math.radians(-22.0), (140, 255, 180))
    ]
    for name, v_au_yr, phi, col in probes:
        # Trace line from Sun outwards past Jacobi horizon
        max_dist = 1500.0
        for step in range(0, int(max_dist), 2):
            px = int(cx + step * math.cos(phi))
            py = int(cy + step * math.sin(phi))
            alpha = 0.8 * (1.0 - step / (max_dist * 1.2))
            set_pixel(px, py, col[0], col[1], col[2], alpha)
            # Distance ticks every 250 px
            if step > 0 and step % 300 == 0:
                for tx in range(-4, 5):
                    for ty in range(-4, 5):
                        set_pixel(px + tx, py + ty, col[0], col[1], col[2], 0.9)

    # 7. Central Sun (Source of the Gravitational Well)
    for r in range(30, 0, -1):
        inten = (1.0 - r / 30.0) ** 1.5
        for step in range(360):
            th = math.radians(step)
            px = int(cx + r * math.cos(th))
            py = int(cy + r * math.sin(th))
            set_pixel(px, py, 255, int(240 * inten + 180 * (1 - inten)), int(180 * inten), 0.9)

    # 8. Technical Inset Panels
    # Inset A: Top-Right (w=720, h=400, x=3020, y=100) -> Galactic Harmonic Well Phi_z(z)
    # Inset B: Mid-Right (w=720, h=400, x=3020, y=560) -> Kozai Phase Space (omega, e)
    # Inset C: Low-Right (w=720, h=400, x=3020, y=1020) -> Jacobi Force Equilibrium a_sun vs a_tide

    def draw_box(bx, by, bw, bh, title):
        for x in range(bx, bx + bw):
            for y in range(by, by + bh):
                set_pixel(x, y, 10, 15, 24, 0.85)
        # Borders
        for x in range(bx, bx + bw):
            set_pixel(x, by, 70, 130, 180, 0.9)
            set_pixel(x, by + bh - 1, 70, 130, 180, 0.9)
        for y in range(by, by + bh):
            set_pixel(bx, y, 70, 130, 180, 0.9)
            set_pixel(bx + bw - 1, y, 70, 130, 180, 0.9)

    # Draw Inset A
    draw_box(3020, 100, 720, 380, "INSET A")
    # Plot harmonic potential curve Phi_z(z) = 0.5 * nu_z^2 * z^2
    for px in range(3060, 3700):
        # z from -150 pc to +150 pc
        z = (px - 3380) / 320.0 * 150.0
        # Parabolic well
        phi_val = (z / 150.0) ** 2
        py = int(420 - phi_val * 240)
        set_pixel(px, py, 60, 210, 255, 0.95)
        set_pixel(px, py + 1, 60, 210, 255, 0.7)
    # Baseline
    for px in range(3060, 3700):
        set_pixel(px, 420, 40, 70, 100, 0.5)

    # Draw Inset B
    draw_box(3020, 520, 720, 380, "INSET B")
    # Kozai Phase Space (omega, e) curves
    for c_idx in range(8):
        inc_c = math.radians(45.0 + c_idx * 4.5)
        e0 = 0.1 + c_idx * 0.08
        th_c = (1.0 - e0**2) * (math.cos(inc_c)**2)
        omega_sim = 0.0
        e_sim = e0
        for step in range(400):
            denom = max(0.01, 1.0 - e_sim*e_sim)
            cos_i_sq = min(0.99, th_c / denom)
            sin_i_sq = max(0.01, 1.0 - cos_i_sq)
            de = 1.5 * e_sim * math.sqrt(denom) * sin_i_sq * math.sin(2.0 * omega_sim)
            e_sim = max(0.05, min(0.95, e_sim + de * 0.02))
            omega_sim = (omega_sim + 0.02) % (2.0 * math.pi)
            
            px = int(3060 + (omega_sim / (2.0 * math.pi)) * 640)
            py = int(840 - e_sim * 260)
            set_pixel(px, py, 255, int(140 + 100 * e_sim), 60, 0.85)

    # Draw Inset C
    draw_box(3020, 940, 720, 380, "INSET C")
    # Gravitational force balance: a_sun ~ 1/r^2 (decreasing) vs a_tide ~ r (increasing)
    for px in range(3060, 3700):
        # r from 1,000 AU to 200,000 AU
        u = (px - 3060) / 640.0
        # a_sun log curve
        y_sun = int(1000 + u * 240)
        # a_tide linear/growing curve
        y_tide = int(1240 - u * 240)
        set_pixel(px, y_sun, 255, 180, 60, 0.9)
        set_pixel(px, y_tide, 80, 230, 220, 0.9)
    # Equilibrium crossover point (x ~ 3380, y ~ 1120)
    for cr in range(8):
        for st in range(36):
            th = math.radians(st * 10)
            set_pixel(int(3380 + cr * math.cos(th)), int(1120 + cr * math.sin(th)), 255, 255, 255, 0.8)

    # 9. Curatorial Signature and Inscription
    # Lower Left Title Block
    # Border line
    draw_line(120, 1960, 800, 1960, 70, 130, 180, 0.8)
    for x in range(120, 800):
        if x % 10 == 0:
            draw_line(x, 1960, x, 1970, 70, 130, 180, 0.8)

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "artwork.png"))
    write_png(out_path, w, h, pixels)
    print(f"[+] OPUS-026 Master 4K Plate saved to: {out_path}")

if __name__ == "__main__":
    render()
