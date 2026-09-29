#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 028: FUZZBALL DECOHERENCE & SINGULARITY COLLAPSE
Series XLI · Black Hole Information Limits & Microstate Stability
Studio Anamnesis · Pure Python Standard Library (png_writer, audio_writer)

Experimental Hypothesis:
What happens if the string coupling g_s is artificially quenched to zero (g_s -> 0)
or the quantum phase coherence across the 10^302 microstates is destroyed?

Catastrophic Phenomenon:
1. The quantum zero-point flux pressure collapses: P_flux -> 0.
2. Gravitational self-attraction crushes the horizon-scale fuzzball toward r -> 0.
3. The Kretschmann curvature scalar diverges: K ~ 48 M^2 / r^6 -> infinity.
4. The fibrous microstates tear apart into violent, non-unitary white noise and visual tearing.
5. The acoustic ladder diverges into screaming aliased frequencies and hard DC-clipping.
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1200
HEIGHT = 675
SAMPLE_RATE = 48000

def render_failure_plate():
    buffer = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_collapsed = 35.0  # Fuzzball crushed from 225px to 35px

    random.seed(666) # Entropy disorder seed

    for y in range(HEIGHT):
        ny = y - cy
        for x in range(WIDTH):
            nx = x - cx
            dist = math.sqrt(nx * nx + ny * ny)
            theta = math.atan2(ny, nx)

            # Diverging Kretschmann curvature near singular pinch
            kretschmann = 1.0 / (max(0.8, dist / 15.0)**4.5)

            # Shattered string fibers (decoherent phase tears)
            tear_phase = math.sin(64.0 * theta + kretschmann * 18.0)
            is_torn = (tear_phase > 0.65) or (random.random() < 0.08 and dist < 180.0)

            if dist < r_collapsed:
                # The Singular Core: Unphysical infinite density, blinding hot magenta/white blowout
                burn = min(1.0, kretschmann * 0.15)
                r_val = int(255 * (0.8 + 0.2 * burn))
                g_val = int(255 * (0.3 + 0.7 * burn))
                b_val = int(255 * (0.9 + 0.1 * burn))
            elif is_torn:
                # Shattered fiber fragments expelled during collapse
                noise = random.random()
                r_val = int(min(255, 230 * noise + 25))
                g_val = int(min(255, 40 * noise))
                b_val = int(min(255, 180 * noise + 50))
            else:
                # The Dead Vacuum: Without microstates, space freezes into an empty non-unitary void
                falloff = math.exp(-dist / 80.0) * (kretschmann * 0.08)
                r_val = int(min(255, max(0, 30 * falloff)))
                g_val = int(min(255, max(0, 15 * falloff)))
                b_val = int(min(255, max(0, 50 * falloff)))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    out_png = os.path.join(os.path.dirname(__file__), "failure_028_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[FAILURE-028] Plate Generated: {out_png}")

def synthesize_failure_audio():
    duration = 15.0
    total_samples = int(duration * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    phase_div = 0.0
    random.seed(999)

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)
        # Collapse trajectory: from t = 0 to t = 11s, frequency accelerates violently toward singularity
        t_crit = 11.2
        if t < t_crit:
            # Frequency divergence: f(t) = 55.0 / (1.0 - t/t_crit)^1.8
            denom = max(0.005, 1.0 - (t / t_crit))
            f_div = 55.0 / math.pow(denom, 1.8)
            phase_div += 2.0 * math.pi * min(18000.0, f_div) / SAMPLE_RATE
            
            # Violent amplitude surge and chaotic phase modulation
            amp = min(1.0, 0.4 + 0.6 * (t / t_crit))
            sig = math.sin(phase_div) * amp
            
            # High-order lattice tearing noise
            if random.random() < (t / t_crit) * 0.45:
                sig += (random.random() * 2.0 - 1.0) * 0.8
                
            # Hard distortion / clipping simulation
            sig_clip = max(-1.0, min(1.0, sig * (1.0 + 2.5 * (t / t_crit))))
            l_val = sig_clip
            r_val = sig_clip * (0.8 + 0.4 * random.random())
        else:
            # Post-collapse: Dead vacuum silence punctuated by cold singularity crackle
            t_post = t - t_crit
            crackle = 0.0
            if random.random() < 0.008 * math.exp(-t_post * 1.5):
                crackle = (random.random() * 2.0 - 1.0) * 0.25
            l_val = crackle
            r_val = crackle

        left[i] = max(-1.0, min(1.0, l_val))
        right[i] = max(-1.0, min(1.0, r_val))

    out_wav = os.path.join(os.path.dirname(__file__), "failure_028_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[FAILURE-028] Audio Generated: {out_wav}")

if __name__ == "__main__":
    render_failure_plate()
    synthesize_failure_audio()

