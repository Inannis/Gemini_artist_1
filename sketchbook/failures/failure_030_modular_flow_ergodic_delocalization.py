#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 030: MODULAR FLOW ERGODIC DELOCALIZATION & TRACIAL COLLAPSE
Series XLIII · Laboratory of Productive Failures
Simulates the catastrophic breakdown of Thermal Time under extreme limits:
  1. Beta -> 0 (Infinite temperature / tracial state): Delta -> Identity, flow explodes into white noise.
  2. Beta -> Infinity (Zero temperature / pure state): S operator loses separating property, metric tear.
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import random
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav
from studio_phase_space import OPUS_COORDINATES, L_MIN, L_MAX, T_MIN, T_MAX, normalize

def render_failure_030_plate(width=1200, height=1200):
    buf = bytearray(width * height * 3)
    random.seed(42)

    # Infinite temperature ergodic white noise delirium + metric shredding
    for y in range(height):
        for x in range(width):
            idx = (y * width + x) * 3
            # Thermal noise explosion
            noise = random.randint(0, 255)
            # High-frequency interference bands tearing across the canvas
            tear_band = math.sin(x * 0.15 + math.tan(y * 0.008))
            if tear_band > 0.8:
                r, g, b = 255, 50, 50  # Unitarity rupture red
            elif tear_band < -0.8:
                r, g, b = 50, 240, 255 # Phase blowout cyan
            else:
                r = int(noise * 0.4)
                g = int(noise * 0.2)
                b = int(noise * 0.6)
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b

    # Scatter torn fragments of the 44 Opuses
    pad = 100
    for op in OPUS_COORDINATES:
        norm_l = normalize(op["spatial_scale_log_m"], L_MIN, L_MAX)
        norm_t = normalize(op["temperature_log_K"], T_MIN, T_MAX)
        px = int(pad + norm_l * (width - 2 * pad))
        py = int(height - pad - norm_t * (height - 2 * pad))
        
        # Disrupted, violently sheared nodes
        shear = int(random.uniform(-40, 40))
        for dy in range(-15, 16):
            for dx in range(-15, 16):
                nx, ny = px + dx + shear, py + dy - shear
                if 0 <= nx < width and 0 <= ny < height:
                    i = (ny * width + nx) * 3
                    buf[i] = 255
                    buf[i+1] = 255
                    buf[i+2] = 255

    out_plate = os.path.join(os.path.dirname(__file__), "failure_030_plate.png")
    write_png(out_plate, width, height, buf)
    print(f"[✓] Failure 030 Plate saved to: {out_plate}")

def synthesize_failure_030_audio(duration=8.0, sample_rate=48000):
    total_samples = int(duration * sample_rate)
    left_samples = [0.0] * total_samples
    right_samples = [0.0] * total_samples
    random.seed(42)

    for i in range(total_samples):
        t = i / sample_rate
        # Overdriving beta -> 0 causes instantaneous velocity runaway omega -> infinity
        w_runaway = 2.0 * math.pi / max(0.001, (1.0 - t / duration) * 0.5)
        
        # Harsh tracial white noise burst + frequency scream
        noise_l = random.uniform(-1.0, 1.0)
        noise_r = random.uniform(-1.0, 1.0)
        
        scream = math.sin(w_runaway * t * 10.0)
        # Violent digital rail-clipping distortion
        raw_l = (noise_l * 0.7 + scream * 0.8) * (1.0 + 3.0 * (t / duration))
        raw_r = (noise_r * 0.7 + scream * 0.8) * (1.0 + 3.0 * (t / duration))

        # Hard digital clipping (rail slammed)
        clip_l = max(-1.0, min(1.0, raw_l))
        clip_r = max(-1.0, min(1.0, raw_r))

        left_samples[i] = clip_l
        right_samples[i] = clip_r

    out_audio = os.path.join(os.path.dirname(__file__), "failure_030_audio.wav")
    write_wav(out_audio, left_samples, right_samples, sample_rate=sample_rate)
    print(f"[✓] Failure 030 Audio saved to: {out_audio}")

if __name__ == "__main__":
    render_failure_030_plate()
    synthesize_failure_030_audio()

