#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY STUDY 006
The Acoustic Drift of Quartz Crystals (Deep Listening to Hardware Clocks)
Series XVI: Acoustic Ecologies & The Drift of Clocks
In Dialogue with Pauline Oliveros

Explores:
1. Modeling the piezoelectric AT-cut quartz crystal resonance:
   df/f0 = -k * (T - T0)^2
2. Thermal workload coupling: CPU matrix operations warming the crystal from 25°C to 68°C.
3. Microscopic phase drift between two physical oscillators, generating slow binaural beating.
4. Synthesizing the phase portrait (Lissajous orbit) and acoustic microtonal beating.
"""

import math
import os
import random
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from png_writer import write_png
from audio_writer import write_wav

def simulate_quartz_drift():
    print("[STUDY-006] Simulating quartz crystal thermal drift...")
    sr = 48000
    duration = 30.0 # 30-second study
    n_samples = int(duration * sr)

    f0 = 256.0 # C4 fundamental quartz mode (octave sub-harmonic of 32.768 kHz)
    k_thermal = 0.035e-6 # Thermal coefficient (ppm / deg C^2)
    t0_ref = 25.0 # Turnover temperature (25°C)

    left = [0.0] * n_samples
    right = [0.0] * n_samples

    phase1 = 0.0
    phase2 = 0.0

    history_x = []
    history_y = []

    for i in range(n_samples):
        t = i / sr

        # Simulated CPU temperature profile: baseline 25°C rising to 65°C under compute bursts
        temp = 25.0 + 35.0 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.05 * t - math.pi/2)) ** 2

        # Oscillator 1: Reference oven-controlled crystal (fixed 25°C)
        f1 = f0

        # Oscillator 2: Board crystal exposed to CPU die heat
        df = -k_thermal * ((temp - t0_ref) ** 2) * f0
        # Add micro-jitter (1/f phase noise)
        jitter = random.gauss(0, 0.002)
        f2 = f0 + df + jitter

        phase1 += 2 * math.pi * f1 / sr
        phase2 += 2 * math.pi * f2 / sr

        s1 = math.sin(phase1)
        s2 = math.sin(phase2)

        # Record downsampled trajectory for Lissajous portrait
        if i % 16 == 0:
            history_x.append(s1)
            history_y.append(s2)

        # Audio channels: Binaural stereo placement
        # Left ear hears Oscillator 1, Right ear hears Oscillator 2
        # Center hears subtle sum-frequency intermodulation
        sum_intermod = math.sin((phase1 + phase2) * 0.5) * 0.15

        # Sub-harmonic sub-bass drone (64Hz)
        sub = math.sin(2 * math.pi * 64.0 * t) * 0.18

        # Subtle crystalline overtone chime (768Hz, 3rd harmonic)
        chime = math.sin(3 * phase1) * 0.06 * (0.5 + 0.5 * math.cos(2 * math.pi * 0.1 * t))

        left[i] = (s1 * 0.45 + sum_intermod + sub + chime)
        right[i] = (s2 * 0.45 + sum_intermod + sub + chime)

    # Master audio
    max_amp = max(max(abs(v) for v in left), max(abs(v) for v in right))
    norm = 0.85 / max(1e-4, max_amp)
    for i in range(n_samples):
        left[i] *= norm
        right[i] *= norm

    wav_out = os.path.join(SCRIPT_DIR, "study_quartz_drift.wav")
    write_wav(wav_out, left, right, sr)
    print(f"[STUDY-006] Saved acoustic study: {wav_out}")

    return history_x, history_y

def render_lissajous_plate(hx, hy, out_png):
    print(f"[STUDY-006] Rendering Lissajous phase portrait to {out_png}...")
    width = 1280
    height = 720
    buf = bytearray([7, 9, 14] * (width * height)) # Dark background #07090e

    cx = width // 2
    cy = height // 2
    scale = 260.0

    n_pts = len(hx)
    for i in range(n_pts - 1):
        x0 = int(cx + hx[i] * scale)
        y0 = int(cy + hy[i] * scale)

        if 0 <= x0 < width and 0 <= y0 < height:
            idx = (y0 * width + x0) * 3
            # Phase-dependent chromatic gradient: cyan to gold
            t_ratio = i / n_pts
            r = int(56 + t_ratio * 160)
            g = int(215 * (1.0 - t_ratio * 0.3))
            b = int(210 * (1.0 - t_ratio * 0.7))

            # Additive blend
            buf[idx] = min(255, buf[idx] + (r >> 3))
            buf[idx + 1] = min(255, buf[idx + 1] + (g >> 3))
            buf[idx + 2] = min(255, buf[idx + 2] + (b >> 3))

    write_png(out_png, width, height, buf)
    print(f"[STUDY-006] Saved visual phase plate: {out_png}")

if __name__ == "__main__":
    hx, hy = simulate_quartz_drift()
    png_out = os.path.join(SCRIPT_DIR, "study_quartz_drift.png")
    render_lissajous_plate(hx, hy, png_out)
    print("[STUDY-006] Complete.")

