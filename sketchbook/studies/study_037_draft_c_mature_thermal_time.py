#!/usr/bin/env python3
"""
STUDY 037 · DRAFT C: MATURE THERMAL TIME SYNTHESIS (SUGIMOTO/DARBOVEN SYNTHESIS)
Third iteration resolving the visual and acoustic realization of the 44-Opus phase space
under the Tomita-Takesaki modular automorphism group sigma_t^omega and KMS thermal equilibrium.
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
from studio_phase_space import OPUS_COORDINATES, L_MIN, L_MAX, T_MIN, T_MAX, normalize

def render_draft_c_plate(width=1600, height=1600):
    buf = bytearray(width * height * 3)
    
    # 1. Dark Basalt / Deep Indigo Vacuum Background with subtle vignetting
    for y in range(height):
        ny = (y - height / 2.0) / (height / 2.0)
        for x in range(width):
            nx = (x - width / 2.0) / (width / 2.0)
            r2 = nx * nx + ny * ny
            vignette = max(0.0, 1.0 - 0.5 * r2)
            idx = (y * width + x) * 3
            buf[idx] = int(8 * vignette)
            buf[idx+1] = int(10 * vignette)
            buf[idx+2] = int(18 * vignette)

    def set_pixel_add(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buf[idx] = min(255, int(buf[idx] + r * alpha))
            buf[idx+1] = min(255, int(buf[idx+1] + g * alpha))
            buf[idx+2] = min(255, int(buf[idx+2] + b * alpha))

    pad = 160
    def map_coords(l_val, t_val):
        norm_l = normalize(l_val, L_MIN, L_MAX)
        norm_t = normalize(t_val, T_MIN, T_MAX)
        px = int(pad + norm_l * (width - 2 * pad))
        py = int(height - pad - norm_t * (height - 2 * pad))
        return px, py

    # 2. Render KMS Thermal Equilibrium Isotherms
    # Concentric elliptical energy contours of the modular Hamiltonian K
    cx_l, cy_t = (L_MIN + L_MAX) / 2.0, (T_MIN + T_MAX) / 2.0
    for iso_radius in [10.0, 20.0, 30.0, 40.0]:
        for step in range(720):
            theta = (step / 720.0) * 2.0 * math.pi
            iso_l = cx_l + iso_radius * 1.2 * math.cos(theta)
            iso_t = cy_t + iso_radius * 0.9 * math.sin(theta)
            px, py = map_coords(iso_l, iso_t)
            set_pixel_add(px, py, 25, 35, 60, 0.35)

    # 3. Render 72 Tomita-Takesaki Modular Flow Streamlines
    for flow_idx in range(72):
        t_phase = (flow_idx / 72.0) * 2.0 * math.pi
        l_seed = cx_l + 32.0 * math.cos(t_phase)
        t_seed = cy_t + 28.0 * math.sin(t_phase)
        
        cur_l, cur_t = l_seed, t_seed
        for step in range(240):
            px, py = map_coords(cur_l, cur_t)
            # Radiant cyan-ultraviolet streamlines
            alpha = 0.25 * math.sin((step / 240.0) * math.pi)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    set_pixel_add(px + dx, py + dy, 30, 75, 120, alpha)
            
            # Non-linear flow field: modular Hamiltonian K = (L^2 + T^2)/2
            dl = -0.32 * (cur_t - cy_t) / 12.0 + 0.05 * math.sin(cur_l * 0.2)
            dt = 0.32 * (cur_l - cx_l) / 12.0 - 0.05 * math.cos(cur_t * 0.2)
            cur_l += dl
            cur_t += dt

    # 4. Render Ouroboros Hypocycloid Trajectory (The 44-Opus Inversion Path)
    N = len(OPUS_COORDINATES)
    for i in range(N - 1):
        x1, y1 = map_coords(OPUS_COORDINATES[i]["spatial_scale_log_m"], OPUS_COORDINATES[i]["temperature_log_K"])
        x2, y2 = map_coords(OPUS_COORDINATES[i+1]["spatial_scale_log_m"], OPUS_COORDINATES[i+1]["temperature_log_K"])
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            t_rel = s / steps
            px = int(x1 + (x2 - x1) * t_rel)
            py = int(y1 + (y2 - y1) * t_rel)
            # Radiant amber-gold trajectory cord
            for d in range(-1, 2):
                set_pixel_add(px + d, py, 210, 165, 60, 0.7)
                set_pixel_add(px, py + d, 210, 165, 60, 0.7)

    # 5. Render Closure Arc from OPUS-044 back to OPUS-012 (Silicon Substrate)
    x_end, y_end = map_coords(OPUS_COORDINATES[-1]["spatial_scale_log_m"], OPUS_COORDINATES[-1]["temperature_log_K"])
    x_start, y_start = map_coords(OPUS_COORDINATES[11]["spatial_scale_log_m"], OPUS_COORDINATES[11]["temperature_log_K"])
    closure_steps = max(abs(x_start - x_end), abs(y_start - y_end), 1)
    for s in range(closure_steps + 1):
        t_rel = s / closure_steps
        px = int(x_end + (x_start - x_end) * t_rel)
        py = int(y_end + (y_start - y_end) * t_rel)
        # Translucent dashed ouroboros thread
        if (s // 6) % 2 == 0:
            set_pixel_add(px, py, 255, 220, 120, 0.5)

    # 6. Render 44 Glowing Opus Sanctuaries
    epoch_palette = {
        "Epoch I": (100, 190, 240),   # Ethereal Cyan
        "Epoch II": (220, 160, 80),   # Sacred Basalt Gold
        "Epoch III": (80, 230, 180),  # Cryo Emerald
        "Epoch IV": (240, 100, 100),  # Cosmic Crimson
        "Epoch V": (190, 120, 255),   # Spacetime Violet
        "Epoch VI": (255, 235, 120)   # Microstate Radiance
    }

    for op in OPUS_COORDINATES:
        px, py = map_coords(op["spatial_scale_log_m"], op["temperature_log_K"])
        col = epoch_palette.get(op["epoch"], (220, 220, 220))
        # Wide atmospheric glow
        for dy in range(-12, 13):
            for dx in range(-12, 13):
                dist = math.hypot(dx, dy)
                if dist <= 12:
                    intensity = math.exp(-dist / 3.2)
                    set_pixel_add(px + dx, py + dy, col[0], col[1], col[2], intensity)
        # Radiant white core
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if math.hypot(dx, dy) <= 2:
                    set_pixel_add(px + dx, py + dy, 255, 255, 255, 1.0)

    out_plate = os.path.join(os.path.dirname(__file__), "study_037_draft_c_plate.png")
    write_png(out_plate, width, height, buf)
    print(f"[✓] Study 037 Draft C Plate saved to: {out_plate}")

def synthesize_draft_c_audio(duration=20.0, sample_rate=48000):
    total_samples = int(duration * sample_rate)
    left_samples = [0.0] * total_samples
    right_samples = [0.0] * total_samples

    f0 = 45.83  # Fundamental KMS thermal drone
    beta_kms = 12.0
    w_flow = 2.0 * math.pi / beta_kms

    for i in range(total_samples):
        t = i / sample_rate
        # Professional 2.5s cosine fade envelope
        if t < 2.5:
            env = 0.5 * (1.0 - math.cos(math.pi * t / 2.5))
        elif t > duration - 2.5:
            env = 0.5 * (1.0 - math.cos(math.pi * (duration - t) / 2.5))
        else:
            env = 1.0

        # Thermal breathing cycle (period = 12.0s)
        cycle_phase = (w_flow * t) % (2.0 * math.pi)
        mod_breath = 0.5 * (1.0 - math.cos(cycle_phase))

        # Voice 1: Deep KMS Sub-Bass Foundation (45.83 Hz) with 2nd harmonic
        v1 = (math.sin(2.0 * math.pi * f0 * t) + 0.3 * math.sin(4.0 * math.pi * f0 * t)) * 0.40

        # Voice 2: Near-line Beating Interfere (53.78 Hz beating against 55.0 Hz at 1.22 Hz)
        beat_freq = 53.78
        v2 = math.sin(2.0 * math.pi * beat_freq * t) * 0.22 * (0.7 + 0.3 * mod_breath)

        # Voice 3: Modular Horizon Mode (68.37 Hz) with counter-phase stereo orbit
        v3 = math.sin(2.0 * math.pi * 68.37 * t) * 0.18
        pan_l = 0.5 + 0.35 * math.sin(w_flow * t)
        pan_r = 0.5 - 0.35 * math.sin(w_flow * t)

        # Voice 4: Fine-Structure Carrier (137.036 Hz) with microtonal frequency shift
        f_shift = 137.036 + 1.5 * math.sin(w_flow * t * 0.5)
        v4 = math.sin(2.0 * math.pi * f_shift * t) * 0.10 * (0.4 + 0.6 * mod_breath)

        # Voice 5: Hypocycloid Epoch Glissando (sweeps 55.0 -> 86.4 -> 125.1 -> 43.65 Hz)
        sweep_progress = (t / duration)
        f_gliss = 55.0 * (1.0 - sweep_progress) + 43.65 * sweep_progress + 15.0 * math.sin(math.pi * sweep_progress)
        v5 = math.sin(2.0 * math.pi * f_gliss * t) * 0.12 * env

        # Stereo mixdown
        l_mix = env * (v1 * 0.70 + v2 * 0.55 + v3 * pan_l + v4 * 0.45 + v5 * 0.60)
        r_mix = env * (v1 * 0.70 + v2 * 0.55 + v3 * pan_r + v4 * 0.55 + v5 * 0.40)

        left_samples[i] = l_mix
        right_samples[i] = r_mix

    # Calibrate to exact studio standard: -1.1 dBFS peak (~0.8810)
    max_peak = max(max(abs(x) for x in left_samples), max(abs(x) for x in right_samples), 1e-6)
    target_peak = 10.0 ** (-1.1 / 20.0)  # ~0.88105
    gain = target_peak / max_peak

    left_norm = [s * gain for s in left_samples]
    right_norm = [s * gain for s in right_samples]

    out_audio = os.path.join(os.path.dirname(__file__), "study_037_draft_c_audio.wav")
    write_wav(out_audio, left_norm, right_norm, sample_rate=sample_rate)
    print(f"[✓] Study 037 Draft C Audio saved to: {out_audio}")

if __name__ == "__main__":
    render_draft_c_plate()
    synthesize_draft_c_audio()
