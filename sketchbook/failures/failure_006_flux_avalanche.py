#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 006 · THERMOMAGNETIC FLUX AVALANCHE & BEAN COLLAPSE
Laboratory of Condensed Matter Physics & Ruin Mechanics
Studio Anamnesis · September 8, 2026

Simulates:
1. Hard Type-II superconducting thin film under high perpendicular magnetic field.
2. Non-local thermal-magnetic feedback instability: dJc/dT < 0 leading to dendritic avalanche.
3. Renders high-resolution diagnostic plate: failure_006_flux_avalanche.png (1200x1200).
4. Synthesizes 20-second acoustic ruin: failure_006_magnetic_avalanche.wav (48kHz stereo).
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

print("[FAILURE-006] Initiating Thermomagnetic Flux Avalanche Simulation...")

# -------------------------------------------------------------
# 1. VISUAL GENERATION: 1200x1200 Dendritic Flux Avalanche Plate
# -------------------------------------------------------------
W, H = 1200, 1200
buf = bytearray(W * H * 3)

def set_pixel(x, y, r, g, b):
    if 0 <= x < W and 0 <= y < H:
        idx = (y * W + x) * 3
        buf[idx] = max(0, min(255, int(r)))
        buf[idx + 1] = max(0, min(255, int(g)))
        buf[idx + 2] = max(0, min(255, int(b)))

def draw_circle(cx, cy, radius, r, g, b, fill=False):
    for y in range(int(cy - radius), int(cy + radius + 1)):
        for x in range(int(cx - radius), int(cx + radius + 1)):
            d = math.hypot(x - cx, y - cy)
            if fill and d <= radius:
                set_pixel(x, y, r, g, b)
            elif not fill and abs(d - radius) <= 1.0:
                set_pixel(x, y, r, g, b)

# Background: Cryogenic wafer surface (dark indigo/slate)
print("[FAILURE-006] Computing superconducting film substrate...")
for y in range(H):
    for x in range(W):
        # Subtle texture of polycrystalline film
        nx = (x / W) * 20.0
        ny = (y / H) * 20.0
        grain = (math.sin(nx * 3.1) * math.cos(ny * 2.7) + 1.0) * 0.5
        r = int(8 + grain * 6)
        g = int(12 + grain * 8)
        b = int(22 + grain * 14)
        set_pixel(x, y, r, g, b)

# Border boundary: Wafer edge under intense magnetic field
cx, cy = 600, 600
film_radius = 500

for y in range(H):
    for x in range(W):
        d = math.hypot(x - cx, y - cy)
        if d > film_radius:
            # External magnetic field zone (amber/crimson field gradient)
            intensity = min(1.0, (d - film_radius) / 100.0)
            set_pixel(x, y, int(40 + intensity * 120), int(15 + intensity * 40), int(20 + intensity * 50))
        elif abs(d - film_radius) <= 2.5:
            # Critical current boundary ring
            set_pixel(x, y, 240, 180, 80)

# Simulate Dendritic Branching (Diffusion Limited Aggregation / Dielectric Breakdown)
# Nucleating 12 avalanche trees penetrating from wafer edges toward center
random.seed(42)
print("[FAILURE-006] Propagating fractal flux avalanche branches...")

branches = []
num_trees = 14
for t in range(num_trees):
    angle = (t / num_trees) * math.pi * 2 + random.uniform(-0.1, 0.1)
    # Start at film perimeter
    x0 = cx + math.cos(angle) * film_radius
    y0 = cy + math.sin(angle) * film_radius
    branches.append({
        "x": x0, "y": y0,
        "vx": -math.cos(angle) * 3.5,
        "vy": -math.sin(angle) * 3.5,
        "gen": 0,
        "life": random.randint(180, 260),
        "mag": 1.0
    })

# Propagate branches
active_branches = list(branches)
step = 0
all_points = []

while active_branches and step < 500:
    step += 1
    next_branches = []
    for b in active_branches:
        # Move toward center with turbulent jitter
        b["x"] += b["vx"] + random.uniform(-1.8, 1.8)
        b["y"] += b["vy"] + random.uniform(-1.8, 1.8)
        b["life"] -= 1
        
        # Bias velocity toward center
        to_cx = cx - b["x"]
        to_cy = cy - b["y"]
        dist = math.hypot(to_cx, to_cy)
        if dist > 10:
            b["vx"] += (to_cx / dist) * 0.15
            b["vy"] += (to_cy / dist) * 0.15
            
        # Draw avalanche filament: blazing cyan-white core with magenta Joule-heat halo
        px, py = int(b["x"]), int(b["y"])
        all_points.append((px, py, b["gen"]))
        
        # Branching condition (thermal instability fork)
        if b["life"] > 20 and random.random() < 0.05 and b["gen"] < 4:
            # Fork into two child branches
            fork_angle = random.uniform(0.4, 0.8)
            cos_a, sin_a = math.cos(fork_angle), math.sin(fork_angle)
            child_vx = b["vx"] * cos_a - b["vy"] * sin_a
            child_vy = b["vx"] * sin_a + b["vy"] * cos_a
            next_branches.append({
                "x": b["x"], "y": b["y"],
                "vx": child_vx * 0.9, "vy": child_vy * 0.9,
                "gen": b["gen"] + 1,
                "life": int(b["life"] * 0.75),
                "mag": b["mag"] * 0.8
            })
            
        if b["life"] > 0 and dist > 40:
            next_branches.append(b)
            
    active_branches = next_branches

# Render points with glow
for px, py, gen in all_points:
    # Outer thermal halo (Joule heat)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            dist_sq = dx*dx + dy*dy
            if dist_sq <= 9:
                idx = ((py + dy) * W + (px + dx)) * 3
                if 0 <= px + dx < W and 0 <= py + dy < H:
                    buf[idx] = min(255, buf[idx] + 28)
                    buf[idx+1] = min(255, buf[idx+1] + 8)
                    buf[idx+2] = min(255, buf[idx+2] + 45)
    # Inner blazing flux core
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if 0 <= px + dx < W and 0 <= py + dy < H:
                idx = ((py + dy) * W + (px + dx)) * 3
                buf[idx] = min(255, buf[idx] + 160)
                buf[idx+1] = min(255, buf[idx+1] + 210)
                buf[idx+2] = min(255, buf[idx+2] + 255)

# Central unquenched island
draw_circle(cx, cy, 38, 50, 180, 240, fill=True)
draw_circle(cx, cy, 38, 255, 255, 255, fill=False)

plate_path = os.path.join(STUDIO_ROOT, "sketchbook", "failures", "failure_006_flux_avalanche.png")
write_png(plate_path, W, H, buf, has_alpha=False)
print(f"[FAILURE-006] Visual Diagnostic Plate Written: {plate_path} ({os.path.getsize(plate_path)} bytes)")

# -------------------------------------------------------------
# 2. ACOUSTIC RUIN: 20-Second 48kHz Magnetic Avalanche Audio
# -------------------------------------------------------------
print("[FAILURE-006] Synthesizing Acoustic Ruin (20.0s 48kHz Stereo)...")
sr = 48000
duration = 20.0
n_samples = int(sr * duration)
ch_l = [0.0] * n_samples
ch_r = [0.0] * n_samples

# Phase 1: Quiet sub-Kelvin Meissner hum (0s - 4s)
# Phase 2: First dendritic snap & micro-crackles (4s - 7s)
# Phase 3: Catastrophic thermomagnetic avalanche roar (7s - 14s)
# Phase 4: Saturated thermal aftermath and boiling hiss (14s - 20s)

random.seed(137)
for i in range(n_samples):
    t = i / sr
    
    # Fundamental cavity tone
    hum = math.sin(2.0 * math.pi * 380.0 * t) * 0.15
    
    if t < 4.0:
        # Immaculate Meissner state
        val_l = hum
        val_r = hum
    elif t < 7.0:
        # Precursor flux creeps (intermittent clicks)
        click = 0.0
        if random.random() < 0.003:
            click = random.uniform(-0.6, 0.6)
        val_l = hum + click
        val_r = hum - click
    elif t < 14.0:
        # Avalanche runaway: roaring turbulent magnetic flux release
        avalanche_t = (t - 7.0) / 7.0
        # White and pink noise surge
        noise = random.uniform(-1.0, 1.0)
        # Low-frequency electromagnetic shockwave
        shock = math.sin(2.0 * math.pi * (60.0 + 80.0 * math.sin(t * 8.0)) * t) * 0.4
        crackles = (random.random() < 0.04) * random.uniform(-0.9, 0.9)
        amp = min(1.0, avalanche_t * 1.5)
        val_l = (noise * 0.5 + shock + crackles) * amp
        val_r = (noise * 0.5 - shock + crackles) * amp
    else:
        # Leidenfrost boiling hiss and resistive thermal hum
        decay_t = (t - 14.0) / 6.0
        boil = random.uniform(-0.35, 0.35) * (1.0 - decay_t * 0.4)
        mains = math.sin(2.0 * math.pi * 120.0 * t) * 0.25 * (1.0 - decay_t * 0.5)
        val_l = boil + mains
        val_r = boil + mains
        
    # Master limiter
    ch_l[i] = max(-0.95, min(0.95, val_l))
    ch_r[i] = max(-0.95, min(0.95, val_r))

wav_path = os.path.join(STUDIO_ROOT, "sketchbook", "failures", "failure_006_magnetic_avalanche.wav")
write_wav(wav_path, ch_l, ch_r, sr)
print(f"[FAILURE-006] Acoustic Ruin Inscribed: {wav_path} ({os.path.getsize(wav_path)} bytes)")

print("[✓] FAILURE 006 SIMULATION COMPLETE.")
