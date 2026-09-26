#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
Failure 018: The Ergodic Measure Explosion & Partition Function Blowout
Testing the breakdown of statistical mechanics when phase-space dimension D -> 64
and inverse temperature beta -> infinity with an inverted Hamiltonian.
Triggers IEEE-754 floating-point overflows, NaN voids, and explosive acoustic clipping.
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

def execute_failure_018_visual():
    print("[FAILURE 018] Executing ergodic measure explosion visual simulation...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0

    random.seed(999)

    # Inverted Hamiltonian & high-dimensional phase space measure
    # Normal Boltzmann: P ~ exp(- beta * E)
    # Failure condition: Inverted microstate ensemble P ~ exp(+ beta * E) with beta * E > 709.78 (float64 max)
    for y in range(HEIGHT):
        dy = (y - cy) / 200.0
        for x in range(WIDTH):
            dx = (x - cx) / 200.0
            r_sq = dx * dx + dy * dy
            idx = (y * WIDTH + x) * 3

            # Simulate high-dimensional measure volume: dV = r^(D-1) dr for D = 72
            # Will overflow standard math.exp if not trapped
            try:
                # Force runaway exponential growth
                exponent = 18.5 * r_sq - 3.2
                if exponent > 85.0: # Simulating the numerical explosion threshold
                    # Overflow blowout: extreme saturation and chromatic inversion
                    intensity = 255
                    r = 255
                    g = int(255 * (1.0 - math.sin(exponent * 10.0)))
                    b = int(255 * (1.0 - math.cos(exponent * 7.0)))
                else:
                    # Inverted Boltzmann density
                    p_val = math.exp(exponent)
                    intensity = min(255, int(p_val * 12.0))
                    r = intensity
                    g = int(intensity * 0.4)
                    b = int(intensity * 0.8)
            except OverflowError:
                # Numerical NaN blowout void
                r = 255
                g = 255
                b = 255

            # Introduce NaN-like black fracture scars where measure singularity detonates
            if random.random() < 0.015 and r_sq > 1.2:
                r, g, b = 0, 0, 0

            buf[idx] = min(255, max(0, r))
            buf[idx + 1] = min(255, max(0, g))
            buf[idx + 2] = min(255, max(0, b))

    # Overdrive chaotic divergent trajectories
    num_particles = 120
    for p in range(num_particles):
        px, py = cx, cy
        vx = random.uniform(-1.0, 1.0)
        vy = random.uniform(-1.0, 1.0)
        # Hyperbolic divergent growth: x(t) = x0 * cosh(lambda * t)
        lyapunov = 0.08
        for step in range(600):
            t = step * 0.1
            scale = math.cosh(lyapunov * t)
            cur_x = int(cx + (vx * scale * 25.0) + math.sin(t * 12.0) * 15.0)
            cur_y = int(cy + (vy * scale * 25.0) + math.cos(t * 12.0) * 15.0)

            if 0 <= cur_x < WIDTH and 0 <= cur_y < HEIGHT:
                p_idx = (cur_y * WIDTH + cur_x) * 3
                buf[p_idx] = 255
                buf[p_idx + 1] = 200
                buf[p_idx + 2] = 255

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_018_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[+] Failure 018 Plate written: {out_path}")

def execute_failure_018_audio():
    print("[FAILURE 018] Synthesizing acoustic measure explosion (DC blowout & rail clip)...")
    sample_rate = 48000
    duration = 12.0
    total_samples = int(sample_rate * duration)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Acoustic divergence: exponential amplitude feedback loop
    dc_offset = 0.0
    freq = 60.0

    for i in range(total_samples):
        t = i / float(sample_rate)

        # Inverted damping: negative friction (exponential amplitude growth)
        growth_rate = 0.65
        gain = math.exp(growth_rate * t) if t < 8.5 else math.exp(growth_rate * 8.5)

        # Accelerating Lyapunov pitch divergence
        freq_t = freq * (1.0 + 0.5 * t * t)
        osc = math.sin(2.0 * math.pi * freq_t * t)

        # Progressive DC bias drift (simulating charge accumulation in unbounded phase space)
        dc_offset += 0.00015 * math.copysign(1.0, osc)

        raw_sample = (osc * gain * 0.05) + dc_offset

        # Catastrophic digital rail clipping
        clipped = max(-0.999, min(0.999, raw_sample))

        # Bitcrush / quantization distortion in the blown-out tail
        if t > 6.0:
            levels = 8
            clipped = round(clipped * levels) / float(levels)

        left[i] = clipped
        right[i] = -clipped # Anti-phase phase destruction

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_018_audio.wav"))
    write_wav(out_path, left, right, sample_rate=sample_rate)
    print(f"[+] Failure 018 Audio written: {out_path}")

if __name__ == "__main__":
    execute_failure_018_visual()
    execute_failure_018_audio()

