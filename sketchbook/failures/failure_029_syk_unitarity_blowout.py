#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 029: SUPER-LYAPUNOV UNBOUNDED CHAOS & UNITARITY BLOWOUT
Series XLII · Quantum Chaos Limits & The Maldacena-Shenker-Stanford Bound
Studio Anamnesis · Pure Python Standard Library (png_writer, audio_writer)

Experimental Hypothesis:
What happens if the quantum chaos Lyapunov exponent lambda_L is artificially forced
past the universal Maldacena-Shenker-Stanford (MSS) bound:
    lambda_L > 2 * pi * k_B * T / hbar = 2 * pi / beta
and the random interaction tensor J_ijkl is given non-Hermitian positive feedback?

Catastrophic Phenomena Observed:
1. Operator Norm Divergence: Commutator norm C(t) = -<[W(t), V(0)]^2> explodes exponentially without saturation.
2. Unitarity Rupture: Quantum state norms exceed unity (<psi|psi> >> 1), violating probability conservation.
3. Spacetime Boundary Tearing: The dual Jackiw-Teitelboim AdS2 boundary curve self-intersects and ruptures.
4. Optical Blowout: Over-saturated white-hot and incandescent crimson tear lines piercing the Poincaré disk.
5. Acoustic Catastrophe: The Lyapunov exponential chirp exceeds Nyquist frequency, producing harsh aliasing and rail clipping.
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
    r_boundary = 260.0
    N = 32

    random.seed(999)

    # In an overdriven non-unitary regime, Majorana nodes rupture outwards
    nodes = []
    for i in range(N):
        theta = 2.0 * math.pi * i / N
        # Super-exponential radial displacement
        blowout = math.exp(random.uniform(0.2, 1.8)) * 35.0
        r_node = r_boundary + blowout
        px = cx + r_node * math.cos(theta)
        py = cy + r_node * math.sin(theta)
        nodes.append((px, py, theta))

    # Base background: thermal runaway noise and torn coordinate grid
    for y in range(HEIGHT):
        ny = y - cy
        for x in range(WIDTH):
            nx = x - cx
            dist = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)

            # Unbounded operator explosion metric
            # Divergence factor grows exponentially near boundary and core
            divergence = math.exp(max(0.0, (dist - r_boundary * 0.5) / 55.0)) * 0.08
            plasma_noise = math.sin(dist * 0.15 + angle * 12.0) * math.cos(dist * 0.08 - angle * 8.0)

            # Blowout burn: hot white-magenta and blinding crimson
            burn = min(1.0, divergence + 0.3 * abs(plasma_noise))
            
            if dist < 65.0:
                # Core rupture: naked singularity blowout
                r_val = 255
                g_val = 255
                b_val = 255
            elif dist < r_boundary + 80.0:
                r_val = int(min(255, 180 * burn + 75))
                g_val = int(min(255, 30 * burn + 10))
                b_val = int(min(255, 90 * burn + 30))
            else:
                # Exterior blown-out thermal fallout
                r_val = int(min(255, 60 * burn + 15))
                g_val = int(min(255, 10 * burn))
                b_val = int(min(255, 25 * burn + 5))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    # Draw violently jagged, ruptured chords tearing through space
    for i in range(N):
        for j in range(i + 1, N):
            if random.random() < 0.22:
                p1 = nodes[i]
                p2 = nodes[j]
                
                # Uncontrolled jagged random walk connecting nodes (tearing)
                steps = 60
                cur_x, cur_y = p1[0], p1[1]
                for s in range(steps):
                    frac = s / float(steps)
                    target_x = (1 - frac) * p1[0] + frac * p2[0]
                    target_y = (1 - frac) * p1[1] + frac * p2[1]
                    
                    # Random transverse shockwave displacement
                    cur_x = target_x + random.gauss(0, 18.0)
                    cur_y = target_y + random.gauss(0, 18.0)
                    
                    ipx, ipy = int(cur_x), int(cur_y)
                    if 0 <= ipx < WIDTH and 0 <= ipy < HEIGHT:
                        idx = (ipy * WIDTH + ipx) * 3
                        # Incandescent white and electric magenta
                        buffer[idx] = 255
                        buffer[idx + 1] = min(255, buffer[idx + 1] + 180)
                        buffer[idx + 2] = min(255, buffer[idx + 2] + 220)

    out_png = os.path.join(os.path.dirname(__file__), "failure_029_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[FAILURE-029] Plate Generated: {out_png}")

def synthesize_failure_audio():
    duration = 15.0
    total_samples = int(duration * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    f0 = 44.0
    # Overdriven super-Lyapunov growth rate: 5x the MSS bound!
    lambda_super = 1.65  # s^-1 (exceeds 2pi/beta ~= 0.314)

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)
        
        # Exponentially escalating chaos frequency
        # Quickly exceeds 10 kHz and crosses Nyquist
        f_runaway = f0 * math.exp(lambda_super * t * 0.42)
        
        # Super-exponential amplitude blowout
        amp_runaway = math.exp(lambda_super * t * 0.28) * 0.15

        # Raw oscillator
        phase = 2.0 * math.pi * f_runaway * t
        raw_sig = math.sin(phase) * amp_runaway

        # In the second half, trigger non-unitary square-wave clipping
        if t > 6.0:
            # Overdrive gain
            overdrive = (t - 6.0) * 8.0
            raw_sig = raw_sig * (1.0 + overdrive)
            # Hard digital rail clipping
            if raw_sig > 1.0:
                raw_sig = 0.98
            elif raw_sig < -1.0:
                raw_sig = -0.98
            # Add stochastic aliasing bursts
            if random.random() < 0.05:
                raw_sig = random.choice([-0.95, 0.95])

        # Terminal silence after total blowout (t > 13.5 s)
        if t > 13.5:
            raw_sig *= max(0.0, (14.2 - t) / 0.7)

        left[i] = max(-0.99, min(0.99, raw_sig))
        right[i] = max(-0.99, min(0.99, raw_sig * 0.92))

    out_wav = os.path.join(os.path.dirname(__file__), "failure_029_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[FAILURE-029] Audio Generated: {out_wav}")

if __name__ == "__main__":
    render_failure_plate()
    synthesize_failure_audio()

