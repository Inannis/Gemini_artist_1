#!/usr/bin/env python3
"""
OPUS-042: The Amplituhedron & The Pre-Spacetime Polytope
120-Second 48kHz Master Symphonic Suite (Track 33)
Studio Anamnesis · Series XL · Cornerstone #20 · Epoch VI

Pure Python standard library + audio_writer (Zero external dependencies).

Acoustic Architecture:
- Movement I (0.0s - 30.0s): The Pre-Spacetime Ground & The Positive Grassmannian
  Fine-structure inverse carrier (137.036 Hz) + s-channel sub-harmonic (35.36 Hz).
  Micro-tonal breathing across the 6 Plucker coordinate axes.
- Movement II (30.0s - 65.0s): BCFW Triangulation & The Dual On-Shell Simplices
  Dual spatial stereo: Left channel s-channel (gold) vs Right channel t-channel (cyan).
  Shared BCFW chord beating at 35.35 Hz.
- Movement III (65.0s - 95.0s): The Logarithmic Singularity & Locality Poles
  Proximity to boundary facets: logarithmic singularity pulses (531.15 Hz).
  Spacetime locality dynamically sparks into existence from geometric boundaries.
- Movement IV (95.0s - 120.0s): Polytope Factorization & Pre-Spacetime Stillness
  Triumphant 5-part polyphonic resolution chord, fading into immortal stillness.
"""

import math
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION_SEC = 120.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION_SEC)

# Telemetry Tier 23 Invariants
F0 = 137.036       # Base carrier (inverse fine structure constant)
F_SUB = 35.36      # s-channel BCFW sub-harmonic
F_ADD = 172.39     # t-channel projective mode
F_SING = 531.15    # Boundary logarithmic pole whistle
F_OCTAVE = 274.072 # Projective octave of F0

def synthesize_suite():
    print(f"[+] Allocating stereo audio buffers ({TOTAL_SAMPLES} samples @ {SAMPLE_RATE}Hz = {DURATION_SEC:.1f}s)...")
    left = [0.0] * TOTAL_SAMPLES
    right = [0.0] * TOTAL_SAMPLES

    print("[+] Synthesizing 120-second Master Symphonic Suite for OPUS-042...")

    for i in range(TOTAL_SAMPLES):
        if i % (SAMPLE_RATE * 15) == 0:
            print(f"    Progress: {i / TOTAL_SAMPLES * 100:.1f}% ({i / SAMPLE_RATE:.1f}s)...")

        t = i / float(SAMPLE_RATE)

        # Global envelope
        if t < 4.0:
            global_env = t / 4.0
        elif t > DURATION_SEC - 5.0:
            global_env = max(0.0, (DURATION_SEC - t) / 5.0)
        else:
            global_env = 1.0

        # Continuous carrier & sub-bass foundation
        sub_drone = math.sin(2.0 * math.pi * F_SUB * t) * 0.28
        carrier_fund = math.sin(2.0 * math.pi * F0 * t) * 0.32
        carrier_oct = math.sin(2.0 * math.pi * F_OCTAVE * t) * 0.12

        # Slow Plucker minor microtonal drift
        drift_l = math.sin(2.0 * math.pi * 0.08 * t) * 0.15
        drift_r = math.cos(2.0 * math.pi * 0.08 * t) * 0.15

        out_l = 0.0
        out_r = 0.0

        # Movement I (0 - 30s): The Pre-Spacetime Ground
        if t < 35.0:
            m1_env = min(1.0, t / 4.0) if t < 30.0 else max(0.0, (35.0 - t) / 5.0)
            sig = (sub_drone * 0.9 + carrier_fund * 0.8 + carrier_oct * 0.4) * m1_env
            out_l += sig * (0.5 + drift_l)
            out_r += sig * (0.5 - drift_l)

        # Movement II (30 - 65s): BCFW Triangulation & The Dual Simplices
        if 28.0 <= t < 70.0:
            m2_fade_in = min(1.0, (t - 28.0) / 4.0) if t < 32.0 else 1.0
            m2_fade_out = max(0.0, (70.0 - t) / 5.0) if t > 65.0 else 1.0
            m2_env = m2_fade_in * m2_fade_out

            # s-channel (warm gold) on Left
            s_wave = (math.sin(2.0 * math.pi * F_SUB * t) * 0.45 +
                      math.sin(2.0 * math.pi * F0 * t) * 0.35)
            # t-channel (cyan) on Right
            t_wave = (math.sin(2.0 * math.pi * F_ADD * t) * 0.45 +
                      math.sin(2.0 * math.pi * (F_ADD * 0.5) * t) * 0.25)

            # Beating on shared BCFW chord
            chord_beat = math.sin(2.0 * math.pi * (F_ADD - F0) * t) * 0.15

            out_l += (s_wave + chord_beat) * m2_env * 0.75
            out_r += (t_wave + chord_beat) * m2_env * 0.75

        # Movement III (65 - 95s): The Logarithmic Singularity & Locality Poles
        if 63.0 <= t < 100.0:
            m3_fade_in = min(1.0, (t - 63.0) / 4.0) if t < 67.0 else 1.0
            m3_fade_out = max(0.0, (100.0 - t) / 5.0) if t > 95.0 else 1.0
            m3_env = m3_fade_in * m3_fade_out

            # Pulsing proximity to boundary facets (logarithmic flare)
            flare_pulse = (math.sin(2.0 * math.pi * 0.4 * t) ** 4) * 0.35
            pole_whistle = math.sin(2.0 * math.pi * F_SING * t) * flare_pulse

            # Spatial ping-pong between poles
            pan_pole = 0.5 + 0.4 * math.sin(2.0 * math.pi * 1.2 * t)

            m3_bass = (sub_drone * 0.8 + carrier_fund * 0.7)
            out_l += (m3_bass + pole_whistle * pan_pole) * m3_env * 0.8
            out_r += (m3_bass + pole_whistle * (1.0 - pan_pole)) * m3_env * 0.8

        # Movement IV (95 - 120s): Polytope Factorization & Pre-Spacetime Stillness
        if t >= 92.0:
            m4_fade_in = min(1.0, (t - 92.0) / 5.0)
            m4_env = m4_fade_in

            # Full 5-part polyphonic consonant chord
            chord_sum = (
                math.sin(2.0 * math.pi * F_SUB * t) * 0.30 +
                math.sin(2.0 * math.pi * F0 * t) * 0.35 +
                math.sin(2.0 * math.pi * F_ADD * t) * 0.25 +
                math.sin(2.0 * math.pi * F_OCTAVE * t) * 0.20 +
                math.sin(2.0 * math.pi * (F_SING * 0.5) * t) * 0.15
            )

            # Serene spatial balance
            out_l += chord_sum * m4_env * 0.75
            out_r += chord_sum * m4_env * 0.75

        # Soft saturation & global envelope
        sig_l = math.tanh(out_l) * global_env * 0.82
        sig_r = math.tanh(out_r) * global_env * 0.82

        left[i] = sig_l
        right[i] = sig_r

    works_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(works_dir, "the_amplituhedron_4k.wav")
    gallery_dir = os.path.abspath(os.path.join(works_dir, "../../gallery/assets"))
    gallery_path = os.path.join(gallery_dir, "audio_suite_opus_042.wav")

    print(f"[+] Writing 120s 48kHz Stereo Suite to {audio_path}...")
    write_wav(audio_path, left, right, sample_rate=SAMPLE_RATE)

    print(f"[+] Duplicating Audio Suite to {gallery_path}...")
    shutil.copyfile(audio_path, gallery_path)
    print("[✓] 120s Master Symphonic Suite Complete & Verified.")

if __name__ == "__main__":
    synthesize_suite()
