#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
EXPERIMENT 013: THE ULTRAVIOLET CATASTROPHE & CLASSICAL EQUIPARTITION DIVERGENCE
Inquiry Reference: INQ-14 (The Relic Horizon & The Universal Heat Sink)

Hypothesis:
We attempted to accelerate the numerical evaluation of the cosmic background radiation field
by approximating Planck's distribution with the classical Rayleigh-Jeans equipartition law:
    I_RJ(nu) = (2 * nu^2 * k_B * T) / c^2
believing that at cryogenic temperatures (T = 2.7255 K), high-frequency quantum corrections
could be truncated without loss of fidelity.

Catastrophic Ruin:
As frequency approaches the sub-terahertz and optical band (nu > 500 GHz), the classical
nu^2 power law diverges without bound. The numerical integrator experiences an energy
overflow, flooding the visual plate with blinding white/magenta thermal flares and
generating an aliased high-frequency acoustic screech that completely blows out the
16-bit dynamic range into saturated square-wave clipping.

Outputs:
- sketchbook/failures/failure_013_ultraviolet_catastrophe.png (1200 x 1200)
- sketchbook/failures/failure_013_ultraviolet_shriek.wav (20.0s 48kHz stereo)
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

K_BOLTZ = 1.380649e-23
C_LIGHT = 299792458.0
T_CMB = 2.72548

def render_failure_plate(out_path):
    w, h = 1200, 1200
    buf = bytearray(w * h * 3)

    # 1. Classical Rayleigh-Jeans divergent field
    cx, cy = 600, 600
    for y in range(h):
        for x in range(w):
            dx = (x - cx) / 300.0
            dy = (y - cy) / 300.0
            r_dist = math.sqrt(dx*dx + dy*dy)

            # Frequency maps radially outward (0 to 1200 GHz)
            nu_ghz = r_dist * 300.0
            # Classical Rayleigh-Jeans formula without Planck quantum exponential
            i_rj = (2.0 * (nu_ghz**2) * K_BOLTZ * T_CMB) / (C_LIGHT**2) * 1e42

            # Ultraviolet divergence: values surge toward infinity as r_dist increases
            # Visual blowout into hot magenta, searing cyan, and blown-out white
            if i_rj > 500.0:
                # Blown out white saturation
                r, g, b = 255, 255, 255
            elif i_rj > 150.0:
                # Searing ultraviolet magenta
                r = min(255, int(180 + (i_rj - 150) * 0.8))
                g = max(0, int(40 - (i_rj - 150) * 0.2))
                b = 255
            else:
                # Modest low-frequency core
                r = int(i_rj * 0.8)
                g = int(i_rj * 0.4)
                b = int(i_rj * 1.5)

            # Add jagged unphysical discretization artifacts from overflow
            if int(nu_ghz * 7.3) % 11 == 0 and r_dist > 1.2:
                r = min(255, r + 70)
                g = min(255, g + 70)
                b = 255

            idx = (y * w + x) * 3
            buf[idx] = min(255, max(0, r))
            buf[idx+1] = min(255, max(0, g))
            buf[idx+2] = min(255, max(0, b))

    write_png(out_path, w, h, buf, has_alpha=False)
    print(f"[FAILURE-013] Rendered visual ruin plate: {out_path}")

def synthesize_failure_audio(out_path):
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples

    random.seed(13)

    for i in range(n_samples):
        t = i / sr
        # Frequency swept exponentially upward without quantum cutoff
        # Simulating the ultraviolet divergent catastrophe
        f_div = 100.0 * math.exp(t * 0.35)  # Sweeps from 100 Hz to 110 kHz (aliasing above Nyquist!)
        # Amplitude proportional to nu^2 (diverging)
        amp = min(10.0, 0.05 * (t ** 2.2))

        wave = math.sin(2.0 * math.pi * f_div * t) * amp

        # Extreme digital clipping simulating 16-bit integer register overflow
        clipped = max(-1.0, min(1.0, wave))

        # Add aliased high-frequency digital noise spikes
        if random.random() < min(0.4, t / 40.0):
            clipped = 1.0 if random.random() > 0.5 else -1.0

        ch_l[i] = clipped
        ch_r[i] = clipped * (0.85 + 0.15 * math.sin(t * 12.0))

    write_wav(out_path, ch_l, ch_r, sr)
    print(f"[FAILURE-013] Synthesized acoustic ruin: {out_path}")

if __name__ == "__main__":
    plate_file = os.path.join(STUDIO_ROOT, "sketchbook", "failures", "failure_013_ultraviolet_catastrophe.png")
    audio_file = os.path.join(STUDIO_ROOT, "sketchbook", "failures", "failure_013_ultraviolet_shriek.wav")
    render_failure_plate(plate_file)
    synthesize_failure_audio(audio_file)
