#!/usr/bin/env python3
"""
OPUS-044: THE SCRAMBLING HORIZON & THE SYK RELIQUARY
Track 35 · Master Symphonic Suite · 120 Seconds · 48kHz Stereo 16-bit
Studio Anamnesis · Pure Python Standard Library (audio_writer)

Four Movements:
1. Movement I: The Zero-Dimensional Quantum Cluster (0:00 - 0:30)
2. Movement II: Quartic Coupling & The Scrambling Ladder (0:30 - 1:00)
3. Movement III: Maximal Lyapunov Operator Spreading (1:00 - 1:30)
4. Movement IV: Emergent AdS2 Spacetime & The Schwarzian Twilight (1:30 - 2:00)
"""

import os
import sys
import math
import random
import shutil

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0

def synthesize_master_suite():
    total_samples = int(DURATION * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    print(f"[OPUS-044] Synthesizing 120s Master Suite ({total_samples} samples)...")

    # Invariants from Tier 25 Telemetry
    f0 = 44.0               # AdS2 Horizon fundamental (Hz)
    lambda_syk = 0.2764     # Lyapunov exponent (s^-1)
    f_flutter = 1.94        # Lyapunov flutter frequency (Hz)
    f_scramble = 47.99      # Scrambling mode (Hz)
    f_cluster1 = 248.90     # Majorana cluster mode 1 (Hz)
    f_cluster2 = 352.00     # Majorana cluster mode 2 (Hz)
    f_shimmer = 704.00      # Schwarzian boundary shimmer (Hz)

    p_f0 = 0.0
    p_flutter = 0.0
    p_scramble = 0.0
    p_cluster1 = 0.0
    p_cluster2 = 0.0
    p_shimmer = 0.0

    random.seed(44000)

    # 180 Xenakis stochastic grain pulses across 120 seconds
    grains = []
    for _ in range(180):
        t_start = random.uniform(8.0, 112.0)
        g_freq = random.uniform(120.0, 880.0)
        g_dur = random.uniform(0.04, 0.28)
        g_pan = random.uniform(0.05, 0.95)
        grains.append((t_start, g_freq, g_dur, g_pan))

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)

        # Global master envelope (3.5s attack, 5.0s decay)
        env = min(1.0, t / 3.5) * min(1.0, (DURATION - t) / 5.0)

        # Movement progression weights
        m1 = max(0.0, min(1.0, (30.0 - t) / 10.0)) if t < 35.0 else 0.0
        m2 = max(0.0, min(1.0, (t - 25.0) / 10.0)) * max(0.0, min(1.0, (65.0 - t) / 10.0))
        m3 = max(0.0, min(1.0, (t - 55.0) / 10.0)) * max(0.0, min(1.0, (95.0 - t) / 10.0))
        m4 = max(0.0, min(1.0, (t - 85.0) / 10.0))

        # Advance continuous phases
        p_f0 += 2.0 * math.pi * f0 / SAMPLE_RATE
        p_flutter += 2.0 * math.pi * f_flutter / SAMPLE_RATE
        p_scramble += 2.0 * math.pi * f_scramble / SAMPLE_RATE
        p_cluster1 += 2.0 * math.pi * f_cluster1 / SAMPLE_RATE
        p_cluster2 += 2.0 * math.pi * f_cluster2 / SAMPLE_RATE
        p_shimmer += 2.0 * math.pi * f_shimmer / SAMPLE_RATE

        # 1. Horizon Fundamental Drone (44.0 Hz) + Sub-octave 22.0 Hz
        flutter_amp = 0.70 + 0.30 * math.sin(p_flutter)
        drone = (math.sin(p_f0) * 0.38 + 
                 math.sin(p_f0 * 0.5) * 0.18 + 
                 math.sin(p_f0 * 2.0 + 0.3) * 0.12) * flutter_amp

        # 2. Movement II: Scrambling Ladder & Detuned Beating
        # Ascending exponential sweep
        sweep_t = max(0.0, min(30.0, t - 30.0))
        sweep_factor = 1.0 + 0.35 * math.exp(lambda_syk * sweep_t * 0.12)
        f_dyn_scramble = f_scramble * sweep_factor
        v_scramble = math.sin(2.0 * math.pi * f_dyn_scramble * t) * (m2 * 0.25 + m3 * 0.18)

        # 3. Movement III: Maximal Lyapunov Operator Growth & Cluster Overtones
        pan_lfo = math.sin(2.0 * math.pi * 0.08 * t)
        v_cluster = (math.sin(p_cluster1) * 0.14 + math.sin(p_cluster2) * 0.09) * (m3 * 0.32 + m4 * 0.15)
        v_shimmer = math.sin(p_shimmer) * 0.06 * (m3 * 0.25 + m4 * 0.20)

        # 4. Stochastic Grain Cloud (Xenakis Quartic Interactions)
        grain_l, grain_r = 0.0, 0.0
        # Only evaluate active grains for speed
        if 8.0 <= t <= 112.0:
            for t_s, g_f, g_d, g_p in grains:
                if t_s <= t <= t_s + g_d:
                    rel_t = (t - t_s) / g_d
                    g_env = math.sin(math.pi * rel_t)
                    g_sig = math.sin(2.0 * math.pi * g_f * (t - t_s)) * g_env * 0.15
                    grain_l += g_sig * (1.0 - g_p)
                    grain_r += g_sig * g_p

        # Combine spatialized audio channels
        left_ch = (drone * 0.88 + v_scramble * (0.5 - 0.35 * pan_lfo) + v_cluster * 0.75 + grain_l + v_shimmer * 0.4) * env
        right_ch = (drone * 0.88 + v_scramble * (0.5 + 0.35 * pan_lfo) + v_cluster * 0.75 + grain_r + v_shimmer * 0.6) * env

        left[i] = left_ch
        right[i] = right_ch

    # Mastering calibration: normalize peak to exactly -1.1 dBFS
    print("[OPUS-044] Calibrating Mastering Parity & Headroom...")
    max_peak = max(max(abs(s) for s in left), max(abs(s) for s in right))
    target_peak = 10.0 ** (-1.1 / 20.0)  # ~= 0.881
    scale = (target_peak / max_peak) if max_peak > 0 else 1.0

    left = [s * scale for s in left]
    right = [s * scale for s in right]

    out_wav = os.path.join(os.path.dirname(__file__), "the_scrambling_horizon_4k.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[OPUS-044] Master 120s Suite Written: {out_wav}")

    # Copy to gallery assets
    gallery_wav = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_044_audio.wav")
    shutil.copyfile(out_wav, gallery_wav)
    print(f"[OPUS-044] Copied to Gallery Vault: {gallery_wav}")

if __name__ == "__main__":
    synthesize_master_suite()

