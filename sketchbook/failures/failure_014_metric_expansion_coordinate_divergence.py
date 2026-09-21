#!/usr/bin/env python3
"""
sketchbook/failures/failure_014_metric_expansion_coordinate_divergence.py
------------------------------------------------------------------------
Productive Failure 014: Metric Expansion Coordinate Divergence & Singularity Blowout
Simulates the catastrophic failure mode when de Sitter expansion is integrated in
naive non-relativistic Galilean coordinates: velocities exceed c, Doppler shifts hit
division-by-zero singularities (v=c), coordinates overflow to infinity, and the audio
engine blows out into full-scale square-wave distortion.
"""

import math
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from practice.tools.png_writer import write_png
from practice.tools.audio_writer import write_wav

def simulate_failure_visual(output_path, width=1200, height=600):
    """
    Renders visual coordinate explosion: particles exceeding horizon speed
    wrap around coordinate boundaries, generating violent horizontal/vertical tearing
    and blown-out over-saturated clusters.
    """
    print(f"[+] Simulating visual coordinate divergence to {output_path}...")
    buf = bytearray(width * height * 3)

    # Base noise and broken scanlines
    for y in range(height):
        for x in range(width):
            idx = (y * width + x) * 3
            # Violent coordinate tearing bands
            if (y % 17 == 0) or ((x + y * 3) % 43 == 0 and y > 200):
                buf[idx] = 255; buf[idx+1] = 60; buf[idx+2] = 60 # Red error lines
            else:
                buf[idx] = 12; buf[idx+1] = 6; buf[idx+2] = 8

    # Simulate 5,000 diverging particles
    for i in range(5000):
        # Naive exponential divergence without conformal boundary
        angle = (i / 5000.0) * math.pi * 2.0
        # Initial radius
        r0 = 10.0 + (i % 80) * 2.0
        # Time integration step that breaches horizon
        t_step = (i % 100) * 0.15
        # Exponential runaway: r = r0 * e^(H * t)
        r_runaway = r0 * math.exp(0.08 * t_step * t_step)

        # Coordinate wrap-around failure (modulus overflow simulation)
        px = int(width / 2 + math.cos(angle) * r_runaway) % width
        py = int(height / 2 + math.sin(angle) * r_runaway) % height

        # Draw exploded particle cluster
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = (px + dx) % width, (py + dy) % height
                idx = (ny * width + nx) * 3
                buf[idx] = min(255, buf[idx] + 200)
                buf[idx+1] = min(255, buf[idx+1] + 120)
                buf[idx+2] = min(255, buf[idx+2] + 80)

    write_png(output_path, width, height, buf)
    print("  -> Visual failure plate generated.")

def simulate_failure_audio(output_path, duration_sec=10.0, sample_rate=48000):
    """
    Synthesizes acoustic singularity: Doppler shift 1 / (1 - v/c) where v -> c,
    triggering infinite frequency surge and violent 100% duty-cycle square wave clip.
    """
    print(f"[+] Synthesizing acoustic singularity blowout to {output_path}...")
    num_samples = int(duration_sec * sample_rate)
    left = [0.0] * num_samples
    right = [0.0] * num_samples

    phase = 0.0
    f0 = 440.0

    for n in range(num_samples):
        t = n / sample_rate
        # v increases toward and beyond c at t = 5.0 seconds
        v_ratio = (t / 5.0) # at t=5.0, v = c!
        
        if v_ratio < 0.98:
            # Approaching singularity
            doppler_factor = 1.0 / max(0.001, 1.0 - v_ratio)
            inst_f = min(18000.0, f0 * doppler_factor)
            phase += 2.0 * math.pi * inst_f / sample_rate
            sig = math.sin(phase) * (1.0 + v_ratio * 2.0)
        else:
            # Singularity breached: severe numerical clipping / square-wave blowout
            sig = 1.0 if (n % 4 < 2) else -1.0 # 24kHz square wave blast

        # Hard saturation clip
        left[n] = max(-1.0, min(1.0, sig))
        right[n] = max(-1.0, min(1.0, -sig))

    write_wav(output_path, left, right, sample_rate)
    print("  -> Audio failure synthesized.")

def main():
    failures_dir = os.path.join(PROJECT_ROOT, "sketchbook/failures")
    os.makedirs(failures_dir, exist_ok=True)

    img_path = os.path.join(failures_dir, "failure_014_coordinate_divergence.png")
    wav_path = os.path.join(failures_dir, "failure_014_superluminal_clip.wav")

    simulate_failure_visual(img_path)
    simulate_failure_audio(wav_path)
    print("[✓] Failure 014 artifacts successfully produced.")

if __name__ == "__main__":
    main()
