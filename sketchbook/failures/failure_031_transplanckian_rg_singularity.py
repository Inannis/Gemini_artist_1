#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 031: TRANS-PLANCKIAN RG SINGULARITY & METRIC TEARING
Series XLIV · Laboratory of Productive Failures
Simulates the catastrophic failure of Holographic Renormalization when pushed
past the physical Planck barrier (z -> 0, z << ell_P) without counterterm subtraction:
  1. Landau pole blowout: running coupling g(mu) diverges, beta(g) -> infinity
  2. Curvature singularity: R_abcd R^abcd -> infinity, tearing the AdS bulk
  3. Wheeler-DeWitt supermetric degeneracy and topological foam destruction
  4. Audio blowout: Nyquist aliasing, explosive rail collision at 0.00 dBFS
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import random
import struct
import sys
import wave

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png

def render_failure_031_plate(width=1200, height=1200):
    buf = bytearray(width * height * 3)
    rng = random.Random(31)

    for y in range(height):
        # Normalized coordinate from IR bulk (bottom) to trans-Planckian boundary (top)
        v = (height - 1 - y) / (height - 1)
        z_sim = max(0.001, 5.0 * (1.0 - v)**2.2)

        # Landau pole singularity as z -> 0
        mu_sim = 1.0 / z_sim
        denom = 1.0 - 0.25 * math.log(max(1.001, mu_sim))
        is_singular = denom <= 0.05

        for x in range(width):
            idx = (y * width + x) * 3
            if is_singular or z_sim < 0.04:
                # Trans-Planckian singularity zone: chaotic white-hot tearing & raw memory noise
                noise = rng.randint(0, 255)
                tear = math.sin(x * 0.25 + math.tan(y * 0.02 + 0.1))
                if abs(tear) > 0.85:
                    r, g, b = 255, 40, 40   # Landau pole rupture red
                elif abs(tear) < 0.15:
                    r, g, b = 255, 255, 255 # Infinite curvature white
                else:
                    r, g, b = noise, int(noise * 0.8), 255 # Aliased foam blue
            else:
                # Distorted bulk streamlines fracturing as they approach the pole
                u = x / width
                stream = math.sin(u * 30.0 + 1.0 / z_sim)
                if abs(stream) > 0.7:
                    r = int(220 * v + 20)
                    g = int(120 * (1.0 - v))
                    b = int(240 * (1.0 - v * 0.5))
                else:
                    r = int(15 + 40 * v)
                    g = int(18 + 30 * v)
                    b = int(25 + 60 * v)

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    out_path = os.path.join(os.path.dirname(__file__), "failure_031_plate.png")
    write_png(out_path, width, height, buf)
    print(f"Rendered Failure 031 Plate to {out_path}")

def synthesize_failure_031_audio(duration=8.0, sample_rate=48000):
    num_samples = int(duration * sample_rate)
    left_channel = []
    right_channel = []

    for n in range(num_samples):
        t = n / sample_rate
        frac = t / duration

        # Simulated trajectory diving directly into the trans-Planckian singularity
        # Scale z plunges to zero: z(t) = 4.0 * (1.0 - frac)^2 + 0.0001
        z_t = max(0.0002, 4.0 * math.pow(max(0.0, 1.0 - frac), 2.5))
        mu_t = 1.0 / z_t

        # Frequency sweeps violently past Nyquist
        f_sweep = 43.20 * math.pow(mu_t, 1.8)

        # Landau pole divergence factor
        coupling = 1.0 / max(0.001, (1.0 - 0.22 * math.log(mu_t)))

        if frac > 0.65:
            # Overdrive rail collision: hard clipping at 0.00 dBFS, severe DC offset
            raw_val = coupling * math.sin(2.0 * math.pi * f_sweep * t)
            # Clip violently to full scale
            val_l = max(-1.0, min(1.0, raw_val * 8.0)) + 0.35  # Deliberate DC offset
            val_r = max(-1.0, min(1.0, -raw_val * 8.0)) + 0.35
        else:
            val_l = 0.3 * math.sin(2.0 * math.pi * f_sweep * t)
            val_r = 0.3 * math.sin(2.0 * math.pi * f_sweep * 1.05 * t)

        left_channel.append(val_l)
        right_channel.append(val_r)

    wav_path = os.path.join(os.path.dirname(__file__), "failure_031_audio.wav")
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            sl = max(-32767, min(32767, int(left_channel[i] * 32767)))
            sr = max(-32767, min(32767, int(right_channel[i] * 32767)))
            frames.extend(struct.pack("<hh", sl, sr))
        wf.writeframes(frames)

    print(f"Synthesized Failure 031 Audio (8s rail collision) to {wav_path}")

if __name__ == "__main__":
    render_failure_031_plate()
    synthesize_failure_031_audio()
