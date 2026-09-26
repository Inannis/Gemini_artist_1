#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-038: THE SIMPLICIAL FOLIATION & THE CAUSAL FOAM
120-Second 48kHz Stereo Acoustic Master Suite
Series XXXVI (Causal Dynamical Triangulations · Cornerstone #16)

Structure of the 5-Movement Suite:
- Movement I: The Primordial 2D Sheet (d_s approx 2.0) [0:00 - 0:24]
- Movement II: The Causal Foliation & Simplicial Assembly [0:24 - 0:48]
- Movement III: Regge Curvature Deficit Dissonance [0:48 - 1:12]
- Movement IV: The Dimensional Crossover (d_s: 2 -> 4) [1:12 - 1:36]
- Movement V: The Cosmological de Sitter Bell (d_s = 4.02) [1:36 - 2:00]

Zero external dependencies (pure standard Python 3).
"""

import math
import random
import os
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION_SEC = 120.0

def synthesize_master_suite():
    print(f"[+] Initializing 120s 48kHz Master Acoustic Engine ({int(SAMPLE_RATE * DURATION_SEC):,} stereo frames)...")
    random.seed(161803)
    n_samples = int(SAMPLE_RATE * DURATION_SEC)
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    # Fundamental tuning
    f_cauchy = 36.0        # Cauchy proper-time pacing fundamental
    f_sub = 18.0           # Infrasonic de Sitter breathing
    f_flat = 144.0         # Flat hinge carrier
    f_hinge_pos = 165.6    # Positive curvature deficit mode
    f_hinge_neg = 122.4    # Negative curvature deficit mode

    for i in range(n_samples):
        t = i / SAMPLE_RATE

        # Master studio envelope (3s fade-in, 4s fade-out)
        master_env = min(1.0, t / 3.0) * min(1.0, (DURATION_SEC - t) / 4.0)

        # Cauchy proper-time horological tick (1.0 Hz pulse)
        tick_phase = t % 1.0
        tick_env = math.exp(-24.0 * tick_phase)
        tick_sig = math.sin(2.0 * math.pi * 72.0 * t) * tick_env * 0.18

        # --- MOVEMENT 1: The Primordial 2D Sheet (0 - 24s) ---
        m1_w = max(0.0, min(1.0, (26.0 - t) / 6.0)) if t < 28.0 else 0.0
        # Planar 2-pole resonance, zero spatial reverb, high UV jitters
        uv_jitter = math.sin(2.0 * math.pi * 288.0 * t + 0.3 * math.sin(2.0 * math.pi * 8.0 * t)) * 0.08
        planar_drone = (
            math.sin(2.0 * math.pi * 72.0 * t) * 0.22
            + math.sin(2.0 * math.pi * 144.0 * t) * 0.14
            + uv_jitter
        ) * m1_w

        # --- MOVEMENT 2: Causal Foliation & Simplicial Assembly (24 - 48s) ---
        m2_w = max(0.0, min(1.0, 1.0 - abs(t - 36.0) / 14.0))
        cauchy_bass = (
            math.sin(2.0 * math.pi * f_cauchy * t) * 0.28
            + math.sin(2.0 * math.pi * (f_cauchy * 1.5) * t) * 0.16
        ) * m2_w

        # --- MOVEMENT 3: Regge Deficit Dissonance (48 - 72s) ---
        m3_w = max(0.0, min(1.0, 1.0 - abs(t - 60.0) / 14.0))
        # Microtonal beating between positive (+57 deg) and negative (-17 deg) deficits
        deficit_chords = (
            math.sin(2.0 * math.pi * f_flat * t) * 0.18
            + math.sin(2.0 * math.pi * f_hinge_pos * t) * 0.15
            + math.sin(2.0 * math.pi * f_hinge_neg * t) * 0.15
            + math.sin(2.0 * math.pi * (f_cauchy * 2.0) * t) * 0.20
        ) * m3_w

        # --- MOVEMENT 4: The Dimensional Crossover (72 - 96s) ---
        m4_w = max(0.0, min(1.0, 1.0 - abs(t - 84.0) / 14.0))
        # Glissando interpolating from 2-pole planar to 4-pole spatial reverb
        sweep_freq = 72.0 + 36.0 * math.sin((t - 72.0) / 24.0 * math.pi * 0.5)
        crossover_drone = (
            math.sin(2.0 * math.pi * sweep_freq * t) * 0.22
            + math.sin(2.0 * math.pi * (sweep_freq * 1.5) * t) * 0.14
            + math.sin(2.0 * math.pi * f_cauchy * t) * 0.25
        ) * m4_w

        # --- MOVEMENT 5: The Cosmological de Sitter Bell (96 - 120s) ---
        m5_w = max(0.0, min(1.0, (t - 92.0) / 8.0))
        # Full 4D spatial chord: 36, 54, 72, 108 Hz
        desitter_polyphony = (
            math.sin(2.0 * math.pi * 36.0 * t) * 0.32
            + math.sin(2.0 * math.pi * 54.0 * t) * 0.22
            + math.sin(2.0 * math.pi * 72.0 * t) * 0.18
            + math.sin(2.0 * math.pi * 108.0 * t) * 0.12
            + math.sin(2.0 * math.pi * 144.0 * t) * 0.08
        ) * m5_w

        # Continuous Sub-bass Infrasonic Breathing (18.0 Hz modulated by de Sitter volume)
        t_cosmological = (t / DURATION_SEC) * math.pi
        desitter_volume_envelope = math.pow(max(0.05, math.sin(t_cosmological)), 1.5)
        infrasonic_breath = math.sin(2.0 * math.pi * f_sub * t) * 0.22 * desitter_volume_envelope

        # Spatial Stereophonic Panning (slow cosmological rotation)
        pan = 0.5 + 0.38 * math.sin(2.0 * math.pi * 0.04 * t)

        sig_l = (
            infrasonic_breath
            + tick_sig
            + planar_drone * 0.85
            + cauchy_bass * 0.90
            + deficit_chords * 0.95
            + crossover_drone * 0.90
            + desitter_polyphony * 0.90
        ) * master_env

        sig_r = (
            infrasonic_breath
            + tick_sig
            + planar_drone * 0.65
            + cauchy_bass * 0.75
            + deficit_chords * 0.70
            + crossover_drone * 0.85
            + desitter_polyphony * 1.05
        ) * master_env

        left[i] = max(-1.0, min(1.0, sig_l * pan * 1.35))
        right[i] = max(-1.0, min(1.0, sig_r * (1.0 - pan) * 1.35))

    out_dir = os.path.dirname(__file__)
    audio_path = os.path.join(out_dir, "the_causal_foam_4k.wav")
    print(f"[+] Writing 120s master WAV suite to {audio_path}...")
    write_wav(audio_path, left, right, SAMPLE_RATE)

    # Sync to gallery assets
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_038_audio.wav"))
    shutil.copyfile(audio_path, gallery_asset)
    print(f"[✓] OPUS-038 Master Acoustic Suite synthesized & synced to {gallery_asset}")

if __name__ == "__main__":
    synthesize_master_suite()

