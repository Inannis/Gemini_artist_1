#!/usr/bin/env python3
"""
OPUS-041: The Holographic Code & The Entanglement Wedge
120-Second 48kHz Master Symphonic Suite (Track 32)
Studio Anamnesis · Series XXXIX · Cornerstone #19

Pure Python standard library + audio_writer (Zero external dependencies).

Acoustic Architecture:
- Movement I (0.0s - 35.0s): The Hyperbolic Vacuum & The Pentagonal Code
  Infrasonic AdS fundamental (48 Hz) + Golden-ratio syndrome chords (77.67, 125.67, 203.34, 329.0 Hz).
- Movement II (35.0s - 80.0s): The Boundary Erasure & Ryu-Takayanagi Tension
  Stochastic erasure noise on Region B (Right) vs Dong-Harlow-Wall reconstruction on Region A (Left).
  Minimal geodesic gamma_A vibrational tension.
- Movement III (80.0s - 120.0s): Holographic Sanctuary & The Incorruptible Logical Qubit
  Harmonic resolution: 24k gold bulk chord radiating across both stereo channels.
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

# Constants from Telemetry Tier 22
F_FUNDAMENTAL = 48.0
PHI = (1.0 + math.sqrt(5.0)) / 2.0
SYNDROMES = [round(F_FUNDAMENTAL * (PHI ** k), 2) for k in range(5)]
# [48.0, 77.67, 125.67, 203.34, 329.0]
CARRIER_HZ = 125.67


def synthesize_suite():
    print(f"[+] Allocating stereo audio buffers ({TOTAL_SAMPLES} samples @ {SAMPLE_RATE}Hz = {DURATION_SEC:.1f}s)...")
    left = [0.0] * TOTAL_SAMPLES
    right = [0.0] * TOTAL_SAMPLES

    print("[+] Synthesizing 120-second Master Symphonic Suite...")

    for i in range(TOTAL_SAMPLES):
        if i % (SAMPLE_RATE * 15) == 0:
            print(f"    Progress: {i / TOTAL_SAMPLES * 100:.1f}% ({i / SAMPLE_RATE:.1f}s)...")

        t = i / float(SAMPLE_RATE)

        # Base fundamental waves
        sub_bass = math.sin(2.0 * math.pi * (F_FUNDAMENTAL * 0.5) * t) * 0.22
        fund = math.sin(2.0 * math.pi * F_FUNDAMENTAL * t) * 0.28
        carrier = math.sin(2.0 * math.pi * CARRIER_HZ * t) * 0.35

        # Pentagonal golden-ratio harmonic field
        golden_sum = (
            0.18 * math.sin(2.0 * math.pi * SYNDROMES[1] * t) +
            0.15 * math.sin(2.0 * math.pi * SYNDROMES[3] * t) +
            0.10 * math.sin(2.0 * math.pi * SYNDROMES[4] * t)
        )

        # Pseudo-random deterministic noise generator
        h = math.sin(i * 127.135) * math.sin(i * 311.753)
        noise = (h - math.floor(h)) * 2.0 - 1.0

        # Movement orchestration
        if t < 35.0:
            # --- MOVEMENT I: The Hyperbolic Vacuum & The Pentagonal Code ---
            env = min(1.0, t / 5.0)
            # Spatial breath: slow sinusoidal stereo drift
            pan = math.sin(2.0 * math.pi * 0.05 * t) * 0.35

            base_sig = (sub_bass + fund + carrier + golden_sum) * env
            sig_l = base_sig * (0.85 - pan)
            sig_r = base_sig * (0.85 + pan)

        elif t < 80.0:
            # --- MOVEMENT II: The Boundary Erasure & Ryu-Takayanagi Tension ---
            m2_prog = (t - 35.0) / 45.0

            # Tension build
            rt_flutter = math.sin(2.0 * math.pi * 4.5 * (t - 35.0))
            geodesic_chime = (
                0.16 * math.sin(2.0 * math.pi * 377.01 * t) +
                0.12 * math.sin(2.0 * math.pi * 628.35 * t)
            ) * (0.8 + 0.2 * rt_flutter)

            # Left Channel: Entanglement Wedge reconstruction (Dong-Harlow-Wall operator)
            # Resilient, purified harmonic resonance holding the central logical qubit
            recon_carrier = math.sin(2.0 * math.pi * CARRIER_HZ * t + 0.1 * math.sin(2.0 * math.pi * 0.8 * t))
            sig_l = (
                fund * 0.3 +
                recon_carrier * 0.45 +
                geodesic_chime * 0.4 +
                golden_sum * 0.3
            )

            # Right Channel: Boundary Region B erasure stress test
            # Stochastic phase-flips, bit-erasure bursts, and static interference
            erasure_intensity = math.sin(m2_prog * math.pi) ** 1.5
            erasure_burst = 1.0 if (int(t * 12) % 5 == 0) else 0.25
            sig_r = (
                fund * 0.2 * (1.0 - erasure_intensity * 0.6) +
                recon_carrier * 0.25 * (1.0 - erasure_intensity * 0.8) +
                noise * 0.42 * erasure_intensity * erasure_burst +
                geodesic_chime * 0.25
            )

        else:
            # --- MOVEMENT III: Holographic Sanctuary & The Incorruptible Logical Qubit ---
            m3_prog = (t - 80.0) / 40.0
            fade_out = 1.0 - max(0.0, (t - 112.0) / 8.0)

            # Radiant 24k Gold Bulk Chord:
            # Frequencies: 125.67, 251.34, 377.01, 502.68, 628.35 Hz
            gold_chord = (
                0.32 * math.sin(2.0 * math.pi * 125.67 * t) +
                0.26 * math.sin(2.0 * math.pi * 251.34 * t) +
                0.20 * math.sin(2.0 * math.pi * 377.01 * t) +
                0.15 * math.sin(2.0 * math.pi * 502.68 * t) +
                0.10 * math.sin(2.0 * math.pi * 628.35 * t) +
                sub_bass * 0.3
            )

            # Subtle spatial shimmer
            shimmer_l = 0.06 * math.sin(2.0 * math.pi * (125.67 + 0.35) * t)
            shimmer_r = 0.06 * math.sin(2.0 * math.pi * (125.67 - 0.35) * t)

            sig_l = (gold_chord + shimmer_l) * fade_out
            sig_r = (gold_chord + shimmer_r) * fade_out

        # Master limiter & ceiling (-0.5 dB headroom)
        left[i] = max(-0.92, min(0.92, sig_l * 0.82))
        right[i] = max(-0.92, min(0.92, sig_r * 0.82))

    out_opus = os.path.abspath(os.path.join(os.path.dirname(__file__), "the_holographic_code_4k.wav"))
    out_gallery = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../gallery/assets/opus_041_audio.wav"))

    print(f"[+] Writing 120s master audio to {out_opus}...")
    write_wav(out_opus, left, right, SAMPLE_RATE)

    print(f"[+] Copying master audio to {out_gallery}...")
    shutil.copyfile(out_opus, out_gallery)
    print("[+] 120s Symphonic Suite generated and synced successfully!")


if __name__ == "__main__":
    synthesize_suite()
