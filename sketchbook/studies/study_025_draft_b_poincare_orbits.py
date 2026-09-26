#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 025 (DRAFT B: MATERIAL FRICTION)
Poincaré Recurrence Orbits & The Shepard-Risset Pitch Spiral
Introduces Hamiltonian phase-space ergodic trajectories on a toroidal surface,
de Sitter thermal horizon limb-brightening, and a 15-second Shepard-Risset acoustic glissando.
"""

import math
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1920
HEIGHT = 1080

def render_draft_b_visual():
    print("[DRAFT B] Rendering phase-space ergodic orbits & thermal horizon...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_horizon = 440.0

    # 1. Background: de Sitter thermal field with exponential limb-brightening
    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3

            if dist < r_horizon:
                # Horizon interior: subtle Gibbons-Hawking thermal glow increasing toward horizon
                rel_d = dist / r_horizon
                # Thermal limb profile: I ~ 1 / sqrt(1 - (r/R)^2)
                limb = 1.0 / math.sqrt(max(0.01, 1.0 - rel_d * rel_d))
                glow = min(180, int(15.0 + 8.0 * limb))

                # Thermal noise grain
                grain = random.uniform(0.85, 1.15)
                r = int(glow * 0.35 * grain)
                g = int(glow * 0.55 * grain)
                b = int(glow * 0.90 * grain)
            elif abs(dist - r_horizon) < 4.0:
                # Horizon boundary: brilliant incandescent cyan-gold
                r = 230
                g = 210
                b = 160
            else:
                # Exterior: cold de Sitter amnesia void
                decay = math.exp(-(dist - r_horizon) / 45.0)
                r = int(12 * decay)
                g = int(16 * decay)
                b = int(28 * decay)

            buf[idx] = min(255, max(0, r))
            buf[idx + 1] = min(255, max(0, g))
            buf[idx + 2] = min(255, max(0, b))

    # 2. Ergodic Trajectories on a 2D-Projected Phase Space Torus
    # Incommensurate frequencies: omega_1 = 1.0, omega_2 = sqrt(5) - 1 (golden ratio section)
    omega_1 = 1.0
    omega_2 = 1.61803398875
    r_major = 280.0
    r_minor = 110.0

    num_steps = 18000
    dt = 0.015

    for step in range(num_steps):
        t = step * dt
        # Toroidal parametric curve
        tx = (r_major + r_minor * math.cos(omega_2 * t)) * math.cos(omega_1 * t)
        ty = (r_major + r_minor * math.cos(omega_2 * t)) * math.sin(omega_1 * t) * 0.65 + r_minor * math.sin(omega_2 * t) * 0.45

        px = int(cx + tx)
        py = int(cy + ty)

        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            idx = (py * WIDTH + px) * 3
            # Progression of recurrence: earlier orbits golden, later orbits cyan
            progress = step / float(num_steps)
            cr = int(240 * (1.0 - progress * 0.7))
            cg = int(180 * (1.0 - progress * 0.3) + 70 * progress)
            cb = int(80 * (1.0 - progress) + 240 * progress)

            # Additive blending
            buf[idx] = min(255, buf[idx] + cr)
            buf[idx + 1] = min(255, buf[idx + 1] + cg)
            buf[idx + 2] = min(255, buf[idx + 2] + cb)

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_025_draft_b_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[+] Draft B Plate written: {out_path}")

def render_draft_b_audio():
    print("[DRAFT B] Synthesizing 15-second Shepard-Risset acoustic glissando...")
    sample_rate = 48000
    duration = 15.0
    total_samples = int(sample_rate * duration)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Shepard-Risset parameters
    num_octaves = 8
    base_freq = 27.5 # A0
    sweep_rate = 0.08 # Octaves per second

    # Gaussian spectral envelope center & width (in octaves)
    f_center = 220.0
    octave_center = math.log2(f_center / base_freq)
    octave_sigma = 1.4

    for i in range(total_samples):
        t = i / float(sample_rate)
        # Phase within the cyclic octave sweep
        cyclic_t = (t * sweep_rate) % 1.0

        sample_sum = 0.0
        for oct_idx in range(num_octaves):
            oct_pos = oct_idx + cyclic_t
            freq = base_freq * math.pow(2.0, oct_pos)

            # Gaussian amplitude envelope
            dist_oct = oct_pos - octave_center
            amp = math.exp(-0.5 * (dist_oct / octave_sigma) ** 2)

            # Compute phase integral for exponential chirp
            # f(t) = f0 * 2^(sweep_rate * t) -> phase = 2*pi * f0 * 2^(sweep_rate * t) / (sweep_rate * ln(2))
            phase = (2.0 * math.pi * freq * t) % (2.0 * math.pi)
            sample_sum += amp * math.sin(phase)

        # Subtle Gibbons-Hawking thermal background noise
        noise = random.gauss(0.0, 0.015)
        mono_sample = (sample_sum * 0.18) + noise

        # Stereo spread: subtle panning oscillation
        pan = 0.5 + 0.15 * math.sin(2.0 * math.pi * 0.1 * t)
        left[i] = mono_sample * math.sqrt(1.0 - pan)
        right[i] = mono_sample * math.sqrt(pan)

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_025_draft_b_audio.wav"))
    write_wav(out_path, left, right, sample_rate=sample_rate)
    print(f"[+] Draft B Audio written: {out_path}")

if __name__ == "__main__":
    render_draft_b_visual()
    render_draft_b_audio()
