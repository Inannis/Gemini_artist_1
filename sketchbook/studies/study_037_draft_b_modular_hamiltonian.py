#!/usr/bin/env python3
"""
STUDY 037 · DRAFT B: MODULAR HAMILTONIAN & FLOW TRAJECTORIES (MATERIAL FRICTION)
Second iteration visualizing the 44-Opus canon through authentic physical phase space
and Tomita-Takesaki modular flow lines sigma_t^omega.
Includes 15-second acoustic synthesis of modular thermal drone.
Pure Python Standard Library · Zero External Dependencies
"""

import json
import math
import os
import struct
import sys

# Ensure studio tools can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

# Import phase space coordinates from studio_phase_space tool
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from studio_phase_space import OPUS_COORDINATES, L_MIN, L_MAX, T_MIN, T_MAX, normalize

def render_draft_b_plate(width=1200, height=1200):
    buf = bytearray(width * height * 3)
    # Deep obsidian-indigo background
    for y in range(height):
        for x in range(width):
            idx = (y * width + x) * 3
            # Subtle radial vignette
            nx = (x - width / 2) / (width / 2)
            ny = (y - height / 2) / (height / 2)
            r2 = nx * nx + ny * ny
            val = max(0.0, 1.0 - 0.4 * r2)
            buf[idx] = int(12 * val)
            buf[idx+1] = int(14 * val)
            buf[idx+2] = int(22 * val)

    def set_pixel_additive(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buf[idx] = min(255, int(buf[idx] + r * alpha))
            buf[idx+1] = min(255, int(buf[idx+1] + g * alpha))
            buf[idx+2] = min(255, int(buf[idx+2] + b * alpha))

    # Map (L, T) to pixel coordinates (with 100px padding)
    pad = 120
    def map_coords(l_val, t_val):
        norm_l = normalize(l_val, L_MIN, L_MAX)
        norm_t = normalize(t_val, T_MIN, T_MAX)
        px = int(pad + norm_l * (width - 2 * pad))
        py = int(height - pad - norm_t * (height - 2 * pad))
        return px, py

    # 1. Render Tomita-Takesaki Modular Flow Geodesic Streamlines
    beta_kms = 12.0
    for flow_idx in range(36):
        # Streamline starting from various phase positions
        t_phase = (flow_idx / 36.0) * 2.0 * math.pi
        l_seed = (L_MIN + L_MAX) / 2.0 + 28.0 * math.cos(t_phase)
        t_seed = (T_MIN + T_MAX) / 2.0 + 25.0 * math.sin(t_phase)
        
        # Trace geodesic trajectory under modular operator Delta^{it}
        cur_l, cur_t = l_seed, t_seed
        for step in range(180):
            px, py = map_coords(cur_l, cur_t)
            # Subtle cyan/indigo streamline
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    set_pixel_additive(px + dx, py + dy, 18, 45, 75, 0.4)
            # Velocity vector from modular Hamiltonian K = -ln(rho)
            dl = -0.35 * (cur_t - (T_MIN + T_MAX) / 2.0) / 15.0
            dt = 0.35 * (cur_l - (L_MIN + L_MAX) / 2.0) / 15.0
            cur_l += dl
            cur_t += dt

    # 2. Render Canon Hypocycloid Trajectory (OPUS-001 -> OPUS-044)
    N = len(OPUS_COORDINATES)
    for i in range(N - 1):
        x1, y1 = map_coords(OPUS_COORDINATES[i]["spatial_scale_log_m"], OPUS_COORDINATES[i]["temperature_log_K"])
        x2, y2 = map_coords(OPUS_COORDINATES[i+1]["spatial_scale_log_m"], OPUS_COORDINATES[i+1]["temperature_log_K"])
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            px = int(x1 + (x2 - x1) * (s / steps))
            py = int(y1 + (y2 - y1) * (s / steps))
            # Gold / amber trajectory line
            set_pixel_additive(px, py, 140, 110, 40, 0.7)

    # 3. Render 44 Opus Nodes
    epoch_colors = {
        "Epoch I": (80, 160, 220),    # Cyan
        "Epoch II": (190, 140, 70),   # Ochre
        "Epoch III": (70, 210, 160),  # Emerald
        "Epoch IV": (210, 90, 90),    # Crimson
        "Epoch V": (170, 100, 230),   # Violet
        "Epoch VI": (255, 200, 80)    # Radiant Gold
    }

    for op in OPUS_COORDINATES:
        px, py = map_coords(op["spatial_scale_log_m"], op["temperature_log_K"])
        col = epoch_colors.get(op["epoch"], (200, 200, 200))
        # Draw glowing halo
        for dy in range(-8, 9):
            for dx in range(-8, 9):
                dist = math.hypot(dx, dy)
                if dist <= 8:
                    intensity = math.exp(-dist / 2.5)
                    set_pixel_additive(px + dx, py + dy, col[0], col[1], col[2], intensity)
        # Node center
        set_pixel_additive(px, py, 255, 255, 255, 1.0)

    out_plate = os.path.join(os.path.dirname(__file__), "study_037_draft_b_plate.png")
    write_png(out_plate, width, height, buf)
    print(f"[✓] Study 037 Draft B Plate saved to: {out_plate}")

def synthesize_draft_b_audio(duration=15.0, sample_rate=48000):
    total_samples = int(duration * sample_rate)
    left_samples = [0.0] * total_samples
    right_samples = [0.0] * total_samples

    f0 = 45.83  # Fundamental KMS thermal drone
    beta_kms = 12.0
    w_flow = 2.0 * math.pi / beta_kms

    for i in range(total_samples):
        t = i / sample_rate
        # Envelope: 2s fade-in, 2s fade-out
        env = 1.0
        if t < 2.0:
            env = t / 2.0
        elif t > duration - 2.0:
            env = (duration - t) / 2.0

        # Modular breathing modulation
        mod_breathing = 0.5 * (1.0 + math.sin(w_flow * t - math.pi / 2.0))

        # Voice 1: Sub-bass dilaton carrier (45.83 Hz)
        v1 = math.sin(2.0 * math.pi * f0 * t) * 0.45

        # Voice 2: Near-line thermal beating (53.78 Hz - 55.0 Hz interference)
        v2 = math.sin(2.0 * math.pi * 53.78 * t) * 0.25 * (0.6 + 0.4 * mod_breathing)

        # Voice 3: KMS modular overtone (68.37 Hz) with stereo panning
        v3 = math.sin(2.0 * math.pi * 68.37 * t) * 0.18
        pan3_l = 0.5 + 0.3 * math.sin(w_flow * t)
        pan3_r = 1.0 - pan3_l

        # Voice 4: High-register thermal whisper (137.036 Hz fine structure harmonic)
        v4 = math.sin(2.0 * math.pi * 137.036 * t) * 0.08 * mod_breathing

        l_val = env * (v1 * 0.7 + v2 * 0.5 + v3 * pan3_l + v4 * 0.4)
        r_val = env * (v1 * 0.7 + v2 * 0.5 + v3 * pan3_r + v4 * 0.6)

        left_samples[i] = l_val
        right_samples[i] = r_val

    # Normalize to -1.0 dBFS (peak = 0.8912)
    max_peak = max(max(abs(x) for x in left_samples), max(abs(x) for x in right_samples), 1e-6)
    target_peak = 10.0 ** (-1.0 / 20.0)  # ~0.8912
    gain = target_peak / max_peak

    left_norm = [s * gain for s in left_samples]
    right_norm = [s * gain for s in right_samples]

    out_audio = os.path.join(os.path.dirname(__file__), "study_037_draft_b_audio.wav")
    write_wav(out_audio, left_norm, right_norm, sample_rate=sample_rate)
    print(f"[✓] Study 037 Draft B Audio saved to: {out_audio}")

if __name__ == "__main__":
    render_draft_b_plate()
    synthesize_draft_b_audio()
