#!/usr/bin/env python3
"""
works/opus_029_causal_horizon/synthesize_causal_suite.py
--------------------------------------------------------
OPUS-029: The Causal Horizon (De Sitter Metric Expansion & Gibbons-Hawking Radiation)
120.0-Second 48kHz Master Symphonic Suite Synthesizer
Zero external dependencies (pure standard Python 3 + studio audio_writer).
"""

import math
import os
import shutil
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from practice.tools.audio_writer import write_wav

DURATION_SEC = 120.0
SAMPLE_RATE = 48000

def synthesize_causal_suite(output_path):
    print(f"[+] Synthesizing 120.0s 48kHz stereo master suite to {output_path}...")
    num_samples = int(DURATION_SEC * SAMPLE_RATE)
    left = [0.0] * num_samples
    right = [0.0] * num_samples

    # Carrier fundamental harmonics
    f0_list = [528.0, 792.0, 1056.0, 1584.0] # High-conformal carrier
    phase_acc = [0.0, 0.0, 0.0, 0.0]
    
    # Sub-bass cosmological baseline drone
    f_sub = 43.2
    phase_sub = 0.0

    # Noise generator state
    rand_state = 421337

    print("[+] Calculating multi-movement trajectory across 120 seconds...")

    for n in range(num_samples):
        t = n / SAMPLE_RATE
        sig_l = 0.0
        sig_r = 0.0

        # --- MOVEMENT 1: The Conformal Diamond (0:00 - 0:30) ---
        if t < 30.0:
            m1_env = math.sin((t / 30.0) * math.pi * 0.5) if t < 4.0 else 1.0
            # Steady high-precision carrier
            for k, f0 in enumerate(f0_list):
                d_phase = 2.0 * math.pi * f0 / SAMPLE_RATE
                phase_acc[k] += d_phase
                w = math.sin(phase_acc[k])
                pan = (k - 1.5) / 2.0 # -0.75 to +0.75
                amp = (0.28 / (k + 1)) * m1_env
                sig_l += w * amp * (0.5 - pan * 0.35)
                sig_r += w * amp * (0.5 + pan * 0.35)

            # Sub-bass baseline
            phase_sub += 2.0 * math.pi * f_sub / SAMPLE_RATE
            sub_w = math.sin(phase_sub) * 0.15 * m1_env
            sig_l += sub_w
            sig_r += sub_w

        # --- MOVEMENT 2: Metric Expansion & Exponential Redshift (0:30 - 1:00) ---
        elif 30.0 <= t < 60.0:
            t_rel = t - 30.0
            # H_sim e-folding rate: frequency decays by 6x over 30s
            H_rate = math.log(6.0) / 30.0
            scale = math.exp(-H_rate * t_rel)
            decay_amp = math.exp(-0.4 * H_rate * t_rel)

            for k, f0 in enumerate(f0_list):
                inst_f = f0 * scale
                d_phase = 2.0 * math.pi * inst_f / SAMPLE_RATE
                phase_acc[k] += d_phase
                w = math.sin(phase_acc[k])
                pan = (k - 1.5) / 2.0
                amp = (0.28 / (k + 1)) * decay_amp
                sig_l += w * amp * (0.5 - pan * 0.35)
                sig_r += w * amp * (0.5 + pan * 0.35)

            # Sub-bass expanding downward
            f_sub_inst = f_sub * scale
            phase_sub += 2.0 * math.pi * f_sub_inst / SAMPLE_RATE
            sub_w = math.sin(phase_sub) * 0.18 * decay_amp
            sig_l += sub_w
            sig_r += sub_w

        # --- MOVEMENT 3: Infrasonic Descent & Horizon Crossing (1:00 - 1:35) ---
        elif 60.0 <= t < 95.0:
            t_rel = t - 60.0
            # Rapid descent into infrasound (< 20 Hz)
            H_rate_fast = math.log(8.0) / 35.0
            scale_fast = (1.0 / 6.0) * math.exp(-H_rate_fast * t_rel)
            fading_amp = max(0.0, 1.0 - (t_rel / 35.0)**1.2) * 0.55

            for k, f0 in enumerate(f0_list):
                inst_f = max(0.5, f0 * scale_fast)
                d_phase = 2.0 * math.pi * inst_f / SAMPLE_RATE
                phase_acc[k] += d_phase
                w = math.sin(phase_acc[k])
                # Inter-channel time dilation micro-delay
                d_dilation = math.sin(phase_acc[k] * 0.98)
                amp = (0.24 / (k + 1)) * fading_amp
                sig_l += w * amp * 0.6
                sig_r += d_dilation * amp * 0.6

            # Gibbons-Hawking vacuum noise entering
            gh_rise = (t_rel / 35.0)**1.5 * 0.18
            rand_state = (rand_state * 1664525 + 1013904223) & 0xFFFFFFFF
            wn = (rand_state / 0xFFFFFFFF) * 2.0 - 1.0
            sig_l += wn * gh_rise
            sig_r += wn * gh_rise * 0.95

        # --- MOVEMENT 4: The Gibbons-Hawking Vacuum & Eternal Quietude (1:35 - 2:00) ---
        else:
            t_rel = t - 95.0
            # All deterministic carrier is extinguished
            # Only 10^-30 K horizon thermal quantum fluctuation rumbles
            fadeout = max(0.0, 1.0 - (t_rel / 25.0)**0.8)
            gh_amp = 0.22 * fadeout

            rand_state = (rand_state * 1664525 + 1013904223) & 0xFFFFFFFF
            wn1 = (rand_state / 0xFFFFFFFF) * 2.0 - 1.0
            rand_state = (rand_state * 1664525 + 1013904223) & 0xFFFFFFFF
            wn2 = (rand_state / 0xFFFFFFFF) * 2.0 - 1.0

            # Low frequency gentle breathing rumble (0.5 to 4 Hz pseudo-pulsation)
            breath = (math.sin(t_rel * 0.45) * 0.5 + 0.5) * gh_amp
            sig_l += wn1 * breath
            sig_r += wn2 * breath

        # Global soft limiter
        left[n] = max(-0.95, min(0.95, sig_l * 0.88))
        right[n] = max(-0.95, min(0.95, sig_r * 0.88))

    write_wav(output_path, left, right, SAMPLE_RATE)
    print("  -> 120.0s master audio suite synthesized successfully.")

def main():
    works_dir = os.path.dirname(os.path.abspath(__file__))
    output_wav = os.path.join(works_dir, "causal_horizon_4k.wav")
    synthesize_causal_suite(output_wav)

    # Copy to gallery assets
    gallery_asset = os.path.join(PROJECT_ROOT, "gallery/assets/causal_horizon_4k.wav")
    shutil.copyfile(output_wav, gallery_asset)
    print(f"[+] Synchronized audio suite to gallery asset: {gallery_asset}")

if __name__ == "__main__":
    main()
