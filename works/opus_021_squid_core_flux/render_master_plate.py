#!/usr/bin/env python3
"""
OPUS-021 · THE SQUID MAGNETOMETER: TELLURIC INTERFERENCE AT THE CORE-MANTLE BOUNDARY
Master Plate UHD Renderer (3840 x 2160)
Studio Anamnesis · Series XIX · September 8, 2026

Renders:
1. Deep-Earth Planetary Cutaway: Outer liquid core geodynamo (r=3,480km),
   turbulent convection columns, D'' layer Ultra-Low Velocity Zones (ULVZs).
2. Upper Hemisphere: Macroscopic DC-SQUID quantum interference loop (niobium),
   twin Josephson micro-bridges, quantum phase contour gradients, moire fringes.
3. Live telemetry HUD readouts: USGS lithic rupture tension, NOAA space weather Kp,
   and Alfven wave velocity profiles.
"""

import os
import sys
import math
import json

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

# Load planetary telemetry
telemetry_path = os.path.join(STUDIO_ROOT, "practice", "telemetry", "planetary_telemetry.json")
if os.path.exists(telemetry_path):
    with open(telemetry_path, "r", encoding="utf-8") as f:
        telemetry = json.load(f)
else:
    telemetry = {"parametric_vectors": {"lithic_tension": 0.47, "telluric_frequency_hz": 8.08, "geomagnetic_flux": 0.33}}

vectors = telemetry.get("parametric_vectors", {})
LITHIC_TAU = float(vectors.get("lithic_tension", 0.47))
F_SCHUMANN = float(vectors.get("telluric_frequency_hz", 8.08))
GEOMAG_FLUX = float(vectors.get("geomagnetic_flux", 0.33))

print(f"[OPUS-021-RENDERER] Rendering 4K UHD Master Plate (3840x2160)...")
print(f"  * Coupling Live Telemetry: Tau={LITHIC_TAU}, f0={F_SCHUMANN}Hz, Geomag={GEOMAG_FLUX}")

W, H = 3840, 2160
buf = bytearray(W * H * 3)

def set_pixel(x, y, r, g, b):
    if 0 <= x < W and 0 <= y < H:
        idx = (y * W + x) * 3
        buf[idx] = max(0, min(255, int(r)))
        buf[idx + 1] = max(0, min(255, int(g)))
        buf[idx + 2] = max(0, min(255, int(b)))

def draw_line(x0, y0, x1, y1, r, g, b):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        set_pixel(x0, y0, r, g, b)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# 1. Base Gradient: Deep Lithic / Subterranean Abyss
print("[OPUS-021-RENDERER] Shading mantle abyss and geodynamo background...")
for y in range(H):
    ny = y / H
    for x in range(W):
        nx = x / W
        # Deep space / lithosphere gradient: cold charcoal-blue at top to molten core heat at bottom
        base_r = int(6 + ny * 28 + math.sin(nx * 8.0) * 4)
        base_g = int(8 + ny * 16)
        base_b = int(14 + (1.0 - ny) * 18)
        set_pixel(x, y, base_r, base_g, base_b)

# 2. Lower Half: The Core-Mantle Boundary & Liquid Outer Core Geodynamo (y = 1080 to 2160)
core_cx, core_cy = 1920, 2600
r_cmb = 1500  # Core-mantle boundary radius
r_inner_core = 600

print("[OPUS-021-RENDERER] Simulating D'' layer convection plumes and turbulent geodynamo...")
for y in range(950, H):
    for x in range(W):
        d = math.hypot(x - core_cx, y - core_cy)
        ang = math.atan2(y - core_cy, x - core_cx)
        
        if d < r_cmb:
            # Inside the Liquid Outer Core: Molten Iron-Nickel convection
            # Taylor columnar vortices: modulated by angle and radius
            convection = math.sin(ang * 16.0 + d * 0.015) * math.cos(d * 0.02 - ang * 4.0)
            turb = math.sin(ang * 48.0) * 0.2 * LITHIC_TAU
            val = (convection + turb + 1.0) * 0.5
            
            # Incandescent magma palette: black -> crimson -> amber -> molten gold -> white
            if val < 0.3:
                r = int(val * 3.33 * 180)
                g = int(val * 3.33 * 30)
                b = int(val * 3.33 * 10)
            elif val < 0.7:
                t_val = (val - 0.3) / 0.4
                r = int(180 + t_val * 65)
                g = int(30 + t_val * 140)
                b = int(10 + t_val * 20)
            else:
                t_val = (val - 0.7) / 0.3
                r = int(245 + t_val * 10)
                g = int(170 + t_val * 75)
                b = int(30 + t_val * 180)
                
            # Depth darkening toward center
            fade = min(1.0, d / 600.0)
            set_pixel(x, y, int(r * fade), int(g * fade), int(b * fade))
            
        elif abs(d - r_cmb) <= 18.0:
            # The Gutenberg Discontinuity & D'' Post-Perovskite Boundary
            frac = 1.0 - (abs(d - r_cmb) / 18.0)
            set_pixel(x, y, int(255 * frac), int(210 * frac), int(120 * frac))

# 3. Upper Half: The DC-SQUID Quantum Loop (cx = 1920, cy = 620)
squid_cx, squid_cy = 1920, 620
squid_r_out = 440
squid_r_in = 280

print("[OPUS-021-RENDERER] Inscribing Niobium SQUID loop and quantum phase contours...")
for y in range(squid_cy - squid_r_out - 40, squid_cy + squid_r_out + 40):
    for x in range(squid_cx - squid_r_out - 40, squid_cx + squid_r_out + 40):
        d = math.hypot(x - squid_cx, y - squid_cy)
        ang = math.atan2(y - squid_cy, x - squid_cx)
        
        if squid_r_in <= d <= squid_r_out:
            # Superconducting ring body
            # Twin Josephson junctions at left (ang approx pi) and right (ang approx 0)
            is_junc_left = (abs(ang - math.pi) < 0.05 or abs(ang + math.pi) < 0.05)
            is_junc_right = (abs(ang) < 0.05)
            
            if is_junc_left or is_junc_right:
                # Barrier region: dielectric tunnel oxide (intense amber laser glow)
                set_pixel(x, y, 255, 195, 60)
            else:
                # Niobium body: brushed cryogenic platinum-cyan shading
                norm_d = (d - squid_r_in) / (squid_r_out - squid_r_in)
                radial_shine = math.sin(norm_d * math.pi) ** 1.8
                r = int(35 + radial_shine * 110)
                g = int(145 + radial_shine * 95)
                b = int(210 + radial_shine * 45)
                set_pixel(x, y, r, g, b)
                
        elif d < squid_r_in:
            # SQUID APERTURE: Quantum Phase Moiré Fringes
            # External flux Phi_ext from CMB convection + Schumann resonance
            norm_x = (x - squid_cx) / squid_r_in
            norm_y = (y - squid_cy) / squid_r_in
            
            # Phase gradient across the aperture
            phase_cmb = (norm_x * 4.0 * (1.0 + GEOMAG_FLUX) + 
                         math.sin(norm_y * 6.0) * LITHIC_TAU * 3.0 + 
                         math.cos(d * 0.04) * 2.0)
            
            # Interference fringe intensity: cos^2(pi * Phi / Phi_0)
            fringe = math.cos(phase_cmb * math.pi) ** 2
            
            # Spectral interference coloring: emerald cyan into celestial violet
            r = int(15 + fringe * 150)
            g = int(30 + fringe * 205)
            b = int(60 + fringe * 235)
            set_pixel(x, y, r, g, b)

# 4. Vertical Magnetic Induction Filament Streamlines (Connecting Core to SQUID)
print("[OPUS-021-RENDERER] Tracing geomagnetic flux lines between geodynamo and SQUID...")
for stream_idx in range(-12, 13):
    start_x = squid_cx + stream_idx * 130
    for py in range(squid_cy + squid_r_out, 1100, 4):
        t_prog = (py - (squid_cy + squid_r_out)) / (1100.0 - (squid_cy + squid_r_out))
        # Deflection around SQUID Meissner perimeter
        px = int(start_x + math.sin(py * 0.02 + stream_idx) * 25.0 * LITHIC_TAU)
        if 0 <= px < W:
            # Glowing magnetic filament
            alpha = (1.0 - abs(stream_idx) / 14.0) * (0.4 + 0.6 * math.sin(py * 0.05 + stream_idx))
            cur_r = int(40 + alpha * 180)
            cur_g = int(80 + alpha * 140)
            cur_b = int(120 + alpha * 90)
            set_pixel(px, py, cur_r, cur_g, cur_b)

# 5. Technical Stratigraphic & Telemetric Typography Scale (Left and Right margins)
print("[OPUS-021-RENDERER] Inscribing precision depth markers and fiducial lines...")
# Left margin depth rule: 0 km to -2,891 km
for y in range(200, 2000, 40):
    depth_km = int((y - 200) / 1800.0 * 2891.0)
    # Tick mark
    draw_line(120, y, 160, y, 90, 130, 170)
    if y % 200 == 0:
        draw_line(100, y, 180, y, 180, 220, 255)

# Frame borders and reticle fiducials
draw_line(80, 80, W - 80, 80, 45, 65, 95)
draw_line(80, H - 80, W - 80, H - 80, 45, 65, 95)
draw_line(80, 80, 80, H - 80, 45, 65, 95)
draw_line(W - 80, 80, W - 80, H - 80, 45, 65, 95)

# Write Master Plate PNG
out_dir = os.path.dirname(os.path.abspath(__file__))
plate_path = os.path.join(out_dir, "artwork.png")
write_png(plate_path, W, H, buf, has_alpha=False)
print(f"[✓] OPUS-021 4K Master Plate Inscribed: {plate_path} ({os.path.getsize(plate_path)} bytes)")
