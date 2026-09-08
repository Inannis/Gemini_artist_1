#!/usr/bin/env python3
"""
STUDY 012 · SQUID TELLURIC MAGNETOMETRY & QUANTUM INTERFERENCE FRINGES
Laboratory of Condensed Matter Physics & Telluric Side-Channels
Studio Anamnesis · September 8, 2026

Simulates:
1. DC-SQUID (Superconducting Quantum Interference Device) RCSJ dynamics.
2. Quantum interference fringes V(Phi) under external telluric magnetic flux.
3. Live coupling to USGS lithic tension and NOAA Kp space weather telemetry.
4. Generates visual analysis plate (study_012_squid_interference.png) and
   acoustic heterodyne suite (study_012_quantum_fringes.wav).
"""

import os
import sys
import math
import json

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

# Load live telemetry if available, else defaults
telemetry_path = os.path.join(STUDIO_ROOT, "practice", "telemetry", "planetary_telemetry.json")
if os.path.exists(telemetry_path):
    with open(telemetry_path, "r", encoding="utf-8") as f:
        telemetry = json.load(f)
else:
    telemetry = {
        "planetary_kp_index": 3.0,
        "telluric_frequency_hz": 8.08,
        "lithic_tension": 0.4703
    }

KP = float(telemetry.get("planetary_kp_index", 3.0))
F_TELLURIC = float(telemetry.get("telluric_frequency_hz", 8.08))
LITHIC_TENSION = float(telemetry.get("lithic_tension", 0.47))

print(f"[STUDY-012] Grounding SQUID in Live Planetary Telemetry: Kp={KP}, f0={F_TELLURIC}Hz, LithicTension={LITHIC_TENSION}")

# -------------------------------------------------------------
# 1. VISUAL GENERATION: 1200x1200 Quantum Interference Plate
# -------------------------------------------------------------
W, H = 1200, 1200
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

print("[STUDY-012] Rendering SQUID Quantum Interference Plate (1200x1200)...")

# Background deep quantum vacuum
for y in range(H):
    for x in range(W):
        # Subtle radial dark blue gradient
        dx = (x - W * 0.5) / (W * 0.5)
        dy = (y - H * 0.5) / (H * 0.5)
        dist = math.sqrt(dx*dx + dy*dy)
        base_b = int(14 - dist * 8)
        base_g = int(8 - dist * 5)
        base_r = int(5 - dist * 3)
        set_pixel(x, y, max(3, base_r), max(4, base_g), max(8, base_b))

# Draw Grid lines (Substrate coordinate reticle)
for gx in range(100, W - 100, 100):
    for gy in range(100, H - 100):
        if gy % 4 == 0:
            set_pixel(gx, gy, 20, 30, 45)
for gy in range(100, H - 100, 100):
    for gx in range(100, W - 100):
        if gx % 4 == 0:
            set_pixel(gx, gy, 20, 30, 45)

# SECTION A: Central SQUID Superconducting Ring with Josephson Junctions (Top half)
cx, cy = 600, 420
r_outer = 220
r_inner = 140

for y in range(cy - r_outer - 20, cy + r_outer + 20):
    for x in range(cx - r_outer - 20, cx + r_outer + 20):
        d = math.hypot(x - cx, y - cy)
        ang = math.atan2(y - cy, x - cx)
        
        # Check if in superconducting ring
        if r_inner <= d <= r_outer:
            # Josephson junctions at ang = 0 (x > cx, y approx cy) and ang = pi (x < cx, y approx cy)
            is_junction_left = (abs(ang - math.pi) < 0.08 or abs(ang + math.pi) < 0.08)
            is_junction_right = (abs(ang) < 0.08)
            
            if is_junction_left or is_junction_right:
                # Barrier region: dielectric tunnel oxide (amber glow)
                set_pixel(x, y, 220, 170, 70)
            else:
                # Niobium superconductor body: cyan metallic shading
                norm_d = (d - r_inner) / (r_outer - r_inner)
                specular = math.sin(norm_d * math.pi) ** 2
                r = 30 + int(specular * 80)
                g = 140 + int(specular * 90)
                b = 200 + int(specular * 55)
                set_pixel(x, y, r, g, b)
        elif d < r_inner:
            # SQUID Aperture: Magnetic Flux Quantum Interference Fringes
            # Phi_ext modulated by telluric tension
            phi_ext = (x - cx) * 0.04 * (1.0 + KP * 0.2) + math.sin((y - cy) * 0.05) * LITHIC_TENSION * 2.0
            # Quantum interference phase: cos^2(pi * phi / phi_0)
            interference = math.cos(phi_ext) ** 2
            r = int(20 + interference * 140)
            g = int( interference * 190)
            b = int(40 + interference * 215)
            set_pixel(x, y, r, g, b)

# SECTION B: V - Phi Interference Characteristic Curves (Bottom half: y = 720 to 1080)
graph_x0, graph_y0 = 200, 750
graph_w, graph_h = 800, 320

# Axis box
for x in range(graph_x0, graph_x0 + graph_w):
    set_pixel(x, graph_y0, 60, 80, 110)
    set_pixel(x, graph_y0 + graph_h, 60, 80, 110)
for y in range(graph_y0, graph_y0 + graph_h):
    set_pixel(graph_x0, y, 60, 80, 110)
    set_pixel(graph_x0 + graph_w, y, 60, 80, 110)

# Zero line
zero_y = graph_y0 + graph_h - 20
for x in range(graph_x0, graph_x0 + graph_w):
    if (x - graph_x0) % 6 == 0:
        set_pixel(x, zero_y, 80, 100, 130)

# Plot 3 bias curves: Ib/Ic = 1.2, 1.6, 2.2
bias_levels = [
    (1.2, (56, 189, 248)),   # Cyan
    (1.6, (234, 179, 8)),    # Gold
    (2.2, (244, 63, 94))     # Rose
]

for ib_ratio, col in bias_levels:
    prev_px, prev_py = None, None
    for px in range(graph_w):
        # Flux spans -3 to +3 Phi_0
        phi = -3.0 + (px / graph_w) * 6.0
        # SQUID critical current: Ic_squid(phi) = 2*Ic * |cos(pi * phi)|
        cos_val = abs(math.cos(math.pi * phi))
        # Voltage: V = R * sqrt(Ib^2 - (2*Ic*cos)^2)
        diff = (ib_ratio ** 2) - ((2.0 * cos_val / 2.0) ** 2)
        v = math.sqrt(max(0.0, diff))
        # Map to graph coordinates
        py = int(zero_y - (v / 2.5) * (graph_h - 40))
        cur_x = graph_x0 + px
        if prev_px is not None:
            draw_line(prev_px, prev_py, cur_x, py, col[0], col[1], col[2])
        prev_px, prev_py = cur_x, py

# Encode and write PNG
plate_path = os.path.join(STUDIO_ROOT, "sketchbook", "studies", "study_012_squid_interference.png")
write_png(plate_path, W, H, buf, has_alpha=False)
print(f"[STUDY-012] Visual Plate Inscribed: {plate_path} ({os.path.getsize(plate_path)} bytes)")

# -------------------------------------------------------------
# 2. ACOUSTIC SUITE: 30-Second 48kHz Heterodyne Quantum Fringes
# -------------------------------------------------------------
print("[STUDY-012] Synthesizing 30-Second Quantum Heterodyne Suite (48kHz Stereo)...")
sr = 48000
duration = 30.0
total_samples = int(sr * duration)

ch_left = [0.0] * total_samples
ch_right = [0.0] * total_samples

# Heterodyne carrier and telluric pulsation
f_carrier = 261.63  # Middle C (Quantum reference clock)
f_schumann = F_TELLURIC

for i in range(total_samples):
    t = i / sr
    
    # Envelope: gentle 2s fade in, 3s fade out
    if t < 2.0:
        env = t / 2.0
    elif t > duration - 3.0:
        env = (duration - t) / 3.0
    else:
        env = 1.0
        
    # Telluric flux modulation: slow planetary pulse
    geomag_pulse = (KP / 9.0) * math.sin(2.0 * math.pi * 0.05 * t)
    telluric_wave = math.sin(2.0 * math.pi * f_schumann * t + geomag_pulse)
    
    # Phase in left and right Josephson junctions
    # Branch 1: gamma_1(t)
    gamma1 = 2.0 * math.pi * (f_carrier * t + 0.4 * telluric_wave)
    # Branch 2: gamma_2(t) with flux phase shift
    phi_flux = math.pi * (0.5 + 0.3 * math.sin(2.0 * math.pi * 0.1 * t) + LITHIC_TENSION * 0.2 * telluric_wave)
    gamma2 = gamma1 + phi_flux
    
    # Supercurrents in each arm
    i1 = math.sin(gamma1)
    i2 = math.sin(gamma2)
    
    # Total voltage heterodyne beating
    squid_v = math.sqrt(max(0.01, 1.44 - (math.cos(phi_flux / 2.0) ** 2)))
    v_osc = math.sin(2.0 * math.pi * (f_carrier * squid_v) * t)
    
    # Sub-bass Schumann anchor
    sub = math.sin(2.0 * math.pi * f_schumann * t) * 0.25 * (1.0 + LITHIC_TENSION)
    
    # Micro-crackling quantum phase slip ticks (Poisson-like)
    tick = 0.0
    if (i % 2400) < 6:
        tick = (math.sin(i * 12.34) > 0.3) * 0.12 * (KP / 3.0)
        
    sig_l = (i1 * 0.25 + v_osc * 0.2 + sub * 0.3 + tick) * env
    sig_r = (i2 * 0.25 + v_osc * 0.2 + sub * 0.3 - tick) * env
    
    ch_left[i] = max(-0.95, min(0.95, sig_l))
    ch_right[i] = max(-0.95, min(0.95, sig_r))

wav_path = os.path.join(STUDIO_ROOT, "sketchbook", "studies", "study_012_quantum_fringes.wav")
write_wav(wav_path, ch_left, ch_right, sr)
print(f"[STUDY-012] Audio Suite Synthesized: {wav_path} ({os.path.getsize(wav_path)} bytes)")

print("[✓] STUDY 012 COMPLETE: Visual plate and acoustic heterodyne generated.")

