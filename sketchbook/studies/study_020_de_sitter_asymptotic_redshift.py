#!/usr/bin/env python3
"""
sketchbook/studies/study_020_de_sitter_asymptotic_redshift.py
-------------------------------------------------------------
Study 020: de Sitter Asymptotic Redshift & The Gibbons-Hawking Floor
Explores the exponential cosmological redshift of multiphonic carriers in de Sitter space,
synthesizing a dual visual plate (conformal causal diamond + redshift spectrogram) and
a 20-second 48kHz stereo audio study capturing carrier dissolution into the 10^-30 K vacuum.
"""

import math
import os
import sys

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from practice.tools.png_writer import write_png
from practice.tools.audio_writer import write_wav

def synthesize_study_audio(output_path, duration_sec=20.0, sample_rate=48000):
    """
    Synthesizes a 20.0-second 48kHz stereo WAV study demonstrating exponential
    cosmological carrier redshift and Gibbons-Hawking vacuum fluctuation noise.
    """
    print(f"[+] Synthesizing {duration_sec}s audio study to {output_path}...")
    num_samples = int(duration_sec * sample_rate)
    left = [0.0] * num_samples
    right = [0.0] * num_samples

    # Carrier frequencies at t=0
    f0_harmonics = [528.0, 792.0, 1056.0, 1584.0] # Solfeggio / Pythagorean ratios
    # Simulation expansion rate (e-folding every 4 seconds)
    H_sim = math.log(8.0) / duration_sec # drops by 8x over 20 seconds

    phase_acc = [0.0, 0.0, 0.0, 0.0]

    # Simple PRNG for deterministic vacuum noise
    rand_state = 1337

    for n in range(num_samples):
        t = n / sample_rate
        # Exponential frequency decay
        scale = math.exp(-H_sim * t)
        
        # Amplitude envelope for carrier: fades down as frequency drops
        carrier_amp = math.exp(-0.8 * H_sim * t) * (1.0 - math.exp(-t * 2.0))
        
        sig_l = 0.0
        sig_r = 0.0

        for k, f0 in enumerate(f0_harmonics):
            inst_f = f0 * scale
            d_phase = 2.0 * math.pi * inst_f / sample_rate
            phase_acc[k] += d_phase
            
            w = math.sin(phase_acc[k])
            # Weight harmonics (fundamental strongest)
            weight = 0.4 / (k + 1)
            # Spatial stereo pan
            pan = (k - 1.5) / 2.0 # -0.75, -0.25, +0.25, +0.75
            sig_l += w * weight * (0.5 - pan * 0.4)
            sig_r += w * weight * (0.5 + pan * 0.4)

        sig_l *= carrier_amp
        sig_r *= carrier_amp

        # Gibbons-Hawking horizon thermal noise: creeps in as carrier fades
        # Thermal noise amplitude rises from 0.0 to 0.15
        horizon_noise_amp = 0.18 * (1.0 - math.exp(-t * 0.35)) * (t / duration_sec)**1.5
        
        # Linear congruential generator for pink/brown noise
        rand_state = (rand_state * 1664525 + 1013904223) & 0xFFFFFFFF
        white_noise = (rand_state / 0xFFFFFFFF) * 2.0 - 1.0
        
        # Low-pass filter for cosmic vacuum rumble
        sig_l += white_noise * horizon_noise_amp * 0.5
        sig_r += white_noise * horizon_noise_amp * 0.5

        # Master limiter
        left[n] = max(-0.95, min(0.95, sig_l * 0.85))
        right[n] = max(-0.95, min(0.95, sig_r * 0.85))

    write_wav(output_path, left, right, sample_rate)
    print("  -> Audio study synthesized successfully.")

def render_study_plate(output_path, width=1200, height=600):
    """
    Renders a 1200x600 visual study plate:
    - Left half: Conformal de Sitter Causal Diamond & Horizon Bounds
    - Right half: Exponential Redshift Spectrogram & Frequency Decay Curves
    """
    print(f"[+] Rendering {width}x{height} visual study plate to {output_path}...")
    buf = bytearray(width * height * 3)

    for y in range(height):
        v = y / height
        for x in range(width):
            u = x / width
            idx = (y * width + x) * 3

            # Default deep void
            r, g, b = 4, 7, 12

            # Divider line between two panels
            if abs(x - width // 2) < 2:
                r, g, b = 30, 42, 60
                buf[idx] = r; buf[idx+1] = g; buf[idx+2] = b
                continue

            # PANEL 1: LEFT HALF (Conformal de Sitter Causal Diamond)
            if x < width // 2:
                pu = (x / (width // 2)) * 2.0 - 1.0 # -1.0 to 1.0
                pv = (1.0 - v) * 2.0 - 1.0         # -1.0 to 1.0

                # Diamond boundary: |pu| + |pv| = 1.0
                diamond_dist = abs(pu) + abs(pv)

                # Background grid in conformal space
                if abs(pu * 10 - round(pu * 10)) < 0.05 or abs(pv * 10 - round(pv * 10)) < 0.05:
                    r, g, b = 10, 16, 26

                # Inside Causal Diamond
                if diamond_dist < 1.0:
                    # Subtle gradient toward observer center (0,0)
                    center_dist = math.hypot(pu, pv)
                    glow = max(0.0, 1.0 - center_dist)
                    r = int(12 + glow * 25)
                    g = int(20 + glow * 45)
                    b = int(35 + glow * 80)

                    # Lightcones tipping outward as r -> horizon
                    # Hyperbolic coordinate contours (surfaces of constant metric expansion)
                    hyp = abs(pu * pu - pv * pv)
                    if abs(hyp - 0.2) < 0.015 or abs(hyp - 0.5) < 0.015 or abs(hyp - 0.8) < 0.015:
                        r = max(r, 45); g = max(g, 160); b = max(b, 175)

                    # Worldlines
                    if abs(pu) < 0.015: # Observer worldline
                        r = 212; g = 175; b = 55 # Gold

                # Cosmological Event Horizon (Diamond Border)
                if abs(diamond_dist - 1.0) < 0.025:
                    r = 56; g = 215; b = 210 # Cyan horizon line
                elif abs(diamond_dist - 1.0) < 0.06:
                    # Horizon glow halo
                    r = max(r, 20); g = max(g, 80); b = max(b, 85)

                # Outside Horizon (Inaccessible Multiverse)
                if diamond_dist > 1.0:
                    r = 6; g = 8; b = 14

            # PANEL 2: RIGHT HALF (Exponential Redshift Spectrogram)
            else:
                su = (x - width // 2) / (width // 2) # 0.0 (t=0) to 1.0 (t=t_max)
                sv = 1.0 - v                         # 0.0 (low freq) to 1.0 (high freq)

                # Background frequency grid
                if abs(sv * 8 - round(sv * 8)) < 0.03 or abs(su * 8 - round(su * 8)) < 0.03:
                    r, g, b = 12, 18, 28

                # Render 4 exponential frequency decay tracks
                H_plot = 2.2
                track_base_freqs = [0.85, 0.65, 0.45, 0.30]
                colors = [
                    (243, 201, 105), # Gold
                    (56, 215, 210),  # Cyan
                    (168, 85, 247),  # Violet
                    (244, 63, 94)    # Rose
                ]

                for k, bf in enumerate(track_base_freqs):
                    track_f = bf * math.exp(-H_plot * su)
                    dist_to_track = abs(sv - track_f)
                    if dist_to_track < 0.012:
                        intensity = max(0.0, 1.0 - dist_to_track / 0.012)
                        cr, cg, cb = colors[k]
                        r = int(r * (1 - intensity) + cr * intensity)
                        g = int(g * (1 - intensity) + cg * intensity)
                        b = int(b * (1 - intensity) + cb * intensity)

                # Gibbons-Hawking vacuum thermal floor at the bottom (sv < 0.08)
                if sv < 0.08:
                    horizon_floor = (0.08 - sv) / 0.08
                    noise = (math.sin(su * 120.0 + sv * 80.0) * 0.5 + 0.5)
                    r = max(r, int(horizon_floor * (40 + noise * 30)))
                    g = max(g, int(horizon_floor * (25 + noise * 20)))
                    b = max(b, int(horizon_floor * (65 + noise * 50)))

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    write_png(output_path, width, height, buf)
    print("  -> Visual plate rendered successfully.")

def main():
    studies_dir = os.path.join(PROJECT_ROOT, "sketchbook/studies")
    os.makedirs(studies_dir, exist_ok=True)

    plate_path = os.path.join(studies_dir, "study_020_de_sitter_plate.png")
    audio_path = os.path.join(studies_dir, "study_020_de_sitter_whisper.wav")

    render_study_plate(plate_path)
    synthesize_study_audio(audio_path)
    print("[✓] Study 020 artifacts generated successfully.")

if __name__ == "__main__":
    main()
