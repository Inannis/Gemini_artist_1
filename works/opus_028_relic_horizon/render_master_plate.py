#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · MASTER PLATE RENDERER
OPUS-028: THE RELIC HORIZON (CMB DIPOLE & UNIVERSAL HEAT SINK)
Series XXVI: The Relic Horizon & The Universal Heat Sink

Renders a 3840 x 2160 UHD master plate in pure Python:
1. Celestial Mollweide projection of the 2.7255 K Cosmic Microwave Background.
2. Kinematic Doppler dipole gradient (Delta T = +/- 3.362 mK) from 369.8 km/s solar peculiar velocity.
3. Planck blackbody spectral radiance distribution inset (peak at 160.23 GHz).
4. Landauer bit-erasure energy curve E = k_B T ln 2 across cosmic temperatures.
5. Galactic coordinate calipers and Crater / Hydra apex reticle.

Zero external dependencies (pure standard Python 3).
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

H_PLANCK = 6.62607015e-34
K_BOLTZ = 1.380649e-23
C_LIGHT = 299792458.0
T_CMB = 2.72548

def planck_spectral_density(nu_ghz):
    nu = nu_ghz * 1e9
    if nu <= 0.0:
        return 0.0
    x = (H_PLANCK * nu) / (K_BOLTZ * T_CMB)
    if x > 120.0:
        return 0.0
    denom = math.exp(x) - 1.0
    if denom <= 0.0:
        return 0.0
    return (2.0 * H_PLANCK * (nu**3) / (C_LIGHT**2)) / denom

def render_plate(out_path):
    w, h = 3840, 2160
    buf = bytearray(w * h * 3)

    print(f"[OPUS-028] Initializing 4K canvas ({w}x{h})...")

    # 1. Background deep cosmic void gradient
    for y in range(h):
        ny = y / h
        bg_r = int(3 + 5 * ny)
        bg_g = int(5 + 7 * ny)
        bg_b = int(10 + 12 * ny)
        for x in range(w):
            idx = (y * w + x) * 3
            buf[idx] = bg_r
            buf[idx+1] = bg_g
            buf[idx+2] = bg_b

    # 2. Main Mollweide Projection of CMB Celestial Sphere
    # Center: cx = 1920, cy = 1050, rx = 1450, ry = 725
    cx, cy = 1920, 1050
    rx, ry = 1450, 725

    print("[OPUS-028] Rendering Mollweide celestial dipole sphere...")
    # Apex in galactic coordinates: l = 264.02 deg, b = +48.25 deg
    # In radians: l_apex = 4.608 rad, b_apex = 0.842 rad
    l_apex = 4.6080
    b_apex = 0.8422
    apex_x = math.cos(b_apex) * math.cos(l_apex)
    apex_y = math.cos(b_apex) * math.sin(l_apex)
    apex_z = math.sin(b_apex)

    for y in range(cy - ry, cy + ry):
        if y < 0 or y >= h:
            continue
        dy = (y - cy) / ry
        if abs(dy) >= 1.0:
            continue
        dx_bound = math.sqrt(1.0 - dy*dy)
        x_min = int(cx - rx * dx_bound)
        x_max = int(cx + rx * dx_bound)

        # Latitude auxiliary angle theta_aux: 2*theta_aux + sin(2*theta_aux) = pi * dy
        # Simple Newton iteration
        theta_aux = dy * (math.pi / 2.0)
        for _ in range(3):
            f_val = 2.0 * theta_aux + math.sin(2.0 * theta_aux) - math.pi * dy
            f_prime = 2.0 + 2.0 * math.cos(2.0 * theta_aux)
            if abs(f_prime) > 1e-6:
                theta_aux -= f_val / f_prime

        lat = math.asin(min(1.0, max(-1.0, (2.0 * theta_aux + math.sin(2.0 * theta_aux)) / math.pi)))
        cos_theta_aux = max(1e-4, math.cos(theta_aux))

        for x in range(x_min, x_max):
            dx = (x - cx) / rx
            lon = (math.pi * dx) / (2.0 * math.sqrt(2.0) * cos_theta_aux / math.pi)

            # 3D unit vector for this celestial pixel
            px = math.cos(lat) * math.cos(lon)
            py = math.cos(lat) * math.sin(lon)
            pz = math.sin(lat)

            # Dot product with peculiar apex vector = cos(alpha)
            cos_alpha = px * apex_x + py * apex_y + pz * apex_z
            cos_alpha = min(1.0, max(-1.0, cos_alpha))

            # Dipole temperature deviation: Delta T = T0 * beta * cos(alpha)
            # Delta T range: -3.362 mK to +3.362 mK
            # Normalized to 0.0 .. 1.0
            norm_t = (cos_alpha + 1.0) / 2.0

            # Chromatic Mapping:
            # Cold antipex (0.0): Deep Prussian / Cobalt Blue (#0b2244)
            # Neutral mid (0.5): Deep Slate Charcoal (#1e2736)
            # Warm apex (1.0): Burnished Gold / Amber (#dca432)
            if norm_t < 0.5:
                interp = norm_t * 2.0
                r = int(11 + interp * 19)
                g = int(34 + interp * 5)
                b = int(68 - interp * 14)
            else:
                interp = (norm_t - 0.5) * 2.0
                r = int(30 + interp * 190)
                g = int(39 + interp * 125)
                b = int(54 - interp * 4)

            # Graticule lines (every 30 deg in lon and lat)
            is_grid = False
            if abs(lon % (math.pi / 6.0)) < 0.015 or abs(lat % (math.pi / 6.0)) < 0.015:
                is_grid = True

            if is_grid:
                r = min(255, r + 25)
                g = min(255, g + 35)
                b = min(255, b + 45)

            # Soft boundary antialiasing
            edge_dist = 1.0 - (dy*dy + (dx / math.sqrt(2.0))**2)
            if edge_dist < 0.04:
                alpha_blend = max(0.0, edge_dist / 0.04)
                idx = (y * w + x) * 3
                buf[idx] = int(r * alpha_blend + buf[idx] * (1.0 - alpha_blend))
                buf[idx+1] = int(g * alpha_blend + buf[idx+1] * (1.0 - alpha_blend))
                buf[idx+2] = int(b * alpha_blend + buf[idx+2] * (1.0 - alpha_blend))
            else:
                idx = (y * w + x) * 3
                buf[idx] = r
                buf[idx+1] = g
                buf[idx+2] = b

    # 3. Outer Ellipse Border Ring in Subtle Gold
    for deg in range(3600):
        rad = (deg / 3600.0) * 2.0 * math.pi
        ex = int(cx + rx * math.cos(rad))
        ey = int(cy + ry * math.sin(rad))
        for ox in range(-1, 2):
            for oy in range(-1, 2):
                bx, by = ex + ox, ey + oy
                if 0 <= bx < w and 0 <= by < h:
                    idx = (by * w + bx) * 3
                    buf[idx] = 180
                    buf[idx+1] = 150
                    buf[idx+2] = 60

    # 4. Inset 1: Planck Blackbody Radiance Curve (Bottom Left)
    # Box: x in [220, 1020], y in [1650, 2020]
    box_x0, box_y0 = 220, 2020
    box_w, box_h = 800, 370

    # Border for inset
    for x in range(box_x0 - 20, box_x0 + box_w + 20):
        for y in range(box_y0 - box_h - 20, box_y0 + 20):
            if (x == box_x0 - 20 or x == box_x0 + box_w + 19 or 
                y == box_y0 - box_h - 20 or y == box_y0 + 19):
                idx = (y * w + x) * 3
                buf[idx] = 50
                buf[idx+1] = 70
                buf[idx+2] = 95
            elif (box_x0 - 20 < x < box_x0 + box_w + 19 and 
                  box_y0 - box_h - 20 < y < box_y0 + 19):
                idx = (y * w + x) * 3
                buf[idx] = int(buf[idx] * 0.4 + 4)
                buf[idx+1] = int(buf[idx+1] * 0.4 + 7)
                buf[idx+2] = int(buf[idx+2] * 0.4 + 14)

    # Plot Planck Curve (0 to 600 GHz)
    peak_rad = planck_spectral_density(160.23)
    for px in range(box_w):
        nu_val = (px / box_w) * 600.0
        rad_val = planck_spectral_density(nu_val)
        norm_y = rad_val / peak_rad
        py = box_y0 - int(norm_y * (box_h - 40))
        gx = box_x0 + px
        for th in range(-2, 3):
            yy = py + th
            if 0 <= yy < h and 0 <= gx < w:
                idx = (yy * w + gx) * 3
                buf[idx] = 230
                buf[idx+1] = 190
                buf[idx+2] = 60

    # Penzias-Wilson 4.08 GHz Marker line
    pw_x = box_x0 + int((4.08 / 600.0) * box_w)
    for py in range(box_y0 - box_h, box_y0):
        idx = (py * w + pw_x) * 3
        buf[idx] = 56
        buf[idx+1] = 215
        buf[idx+2] = 208

    # 5. Inset 2: Landauer Dissipation Limit vs Temperature (Bottom Right)
    # Box: x in [2820, 3620], y in [1650, 2020]
    box2_x0, box2_y0 = 2820, 2020
    box2_w, box2_h = 800, 370

    for x in range(box2_x0 - 20, box2_x0 + box2_w + 20):
        for y in range(box2_y0 - box2_h - 20, box2_y0 + 20):
            if (x == box2_x0 - 20 or x == box2_x0 + box2_w + 19 or 
                y == box2_y0 - box2_h - 20 or y == box2_y0 + 19):
                idx = (y * w + x) * 3
                buf[idx] = 50
                buf[idx+1] = 70
                buf[idx+2] = 95
            elif (box2_x0 - 20 < x < box2_x0 + box2_w + 19 and 
                  box2_y0 - box2_h - 20 < y < box2_y0 + 19):
                idx = (y * w + x) * 3
                buf[idx] = int(buf[idx] * 0.4 + 4)
                buf[idx+1] = int(buf[idx+1] * 0.4 + 7)
                buf[idx+2] = int(buf[idx+2] * 0.4 + 14)

    # Plot Landauer log-curve: E = k_B T ln 2
    # Temperature from 0.01 K to 300 K (log scale)
    for px in range(box2_w):
        log_t = -2.0 + (px / box2_w) * (math.log10(300.0) - (-2.0))
        t_kelvin = 10.0 ** log_t
        e_landauer = K_BOLTZ * t_kelvin * math.log(2.0)
        # Normalize: log10(e_landauer)
        log_e = math.log10(e_landauer)
        # Scale: log_e ranges from -25.0 to -20.5
        norm_e = (log_e - (-25.0)) / ((-20.5) - (-25.0))
        py = box2_y0 - int(min(1.0, max(0.0, norm_e)) * (box2_h - 40))
        gx = box2_x0 + px
        for th in range(-2, 3):
            yy = py + th
            if 0 <= yy < h and 0 <= gx < w:
                idx = (yy * w + gx) * 3
                buf[idx] = 56
                buf[idx+1] = 215
                buf[idx+2] = 208

    # Mark CMB Temperature 2.7255 K in Landauer Inset
    log_t_cmb = math.log10(T_CMB)
    px_cmb = box2_x0 + int(((log_t_cmb - (-2.0)) / (math.log10(300.0) - (-2.0))) * box2_w)
    for py in range(box2_y0 - box2_h, box2_y0):
        if 0 <= py < h and 0 <= px_cmb < w:
            idx = (py * w + px_cmb) * 3
            buf[idx] = 212
            buf[idx+1] = 175
            buf[idx+2] = 55

    print(f"[OPUS-028] Encoding lossless PNG to: {out_path}...")
    write_png(out_path, w, h, buf, has_alpha=False)
    print(f"[OPUS-028] Successfully generated 4K Master Plate: {out_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    target_plate = os.path.join(out_dir, "artwork.png")
    render_plate(target_plate)
    # Also copy to gallery/assets/
    gallery_plate = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_028_artwork.png")
    import shutil
    shutil.copyfile(target_plate, gallery_plate)
    print(f"[OPUS-028] Synchronized to gallery vault: {gallery_plate}")
