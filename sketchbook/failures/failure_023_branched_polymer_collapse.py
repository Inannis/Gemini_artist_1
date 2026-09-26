#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 023: THE BRANCHED POLYMER PHASE COLLAPSE
Series XXXVI (Causal Dynamical Triangulations & Spacetime Emergence)

Failure Mode:
When bare gravitational coupling kappa_0 drops below the critical threshold
kappa_0^c without causal proper-time foliation (Delta = 0, Euclidean limit),
the simplicial path integral collapses into the Branched Polymer Phase:
- Spacetime pinches off into skinny, fractal tree-like chains.
- The Hausdorff dimension collapses to d_H approx 2.0.
- Macroscopic 3-volume vanishes (zero spatial interior).
- Acoustic resonance collapses into brittle, disconnected crackling and clicks.

Zero external dependencies (pure standard Python 3).
"""

import math
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 800
HEIGHT = 800
SAMPLE_RATE = 48000
DURATION_SEC = 10.0

def generate_failure_023():
    random.seed(999)
    buffer = bytearray(WIDTH * HEIGHT * 3)

    # Dark bruised void
    for i in range(0, len(buffer), 3):
        buffer[i] = 14
        buffer[i+1] = 8
        buffer[i+2] = 16

    # Generate branched polymer fractal tree
    # Recursive branching from central bottleneck
    edges = []
    nodes = [(WIDTH / 2.0, HEIGHT / 2.0)]

    def branch(x, y, angle, depth, length):
        if depth <= 0:
            return
        # Branch into 2 to 4 thin twigs
        n_twigs = random.choice([2, 3, 4])
        for _ in range(n_twigs):
            d_angle = (random.random() - 0.5) * 1.4
            new_angle = angle + d_angle
            twig_len = length * (0.65 + random.random() * 0.3)
            nx = x + math.cos(new_angle) * twig_len
            ny = y + math.sin(new_angle) * twig_len
            edges.append(((x, y), (nx, ny), depth))
            nodes.append((nx, ny))
            branch(nx, ny, new_angle, depth - 1, twig_len)

    # 4 initial roots radiating outward
    for i in range(4):
        init_angle = i * (math.pi / 2.0) + 0.2
        branch(WIDTH / 2.0, HEIGHT / 2.0, init_angle, 6, 90.0)

    # Line drawing with anti-aliasing
    def draw_line(x0, y0, x1, y1, r, g, b):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                idx = (y0 * WIDTH + x0) * 3
                buffer[idx] = min(255, buffer[idx] + r)
                buffer[idx+1] = min(255, buffer[idx+1] + g)
                buffer[idx+2] = min(255, buffer[idx+2] + b)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    # Draw polymer twig edges (Sickly pale bone and neon magenta stress)
    for p1, p2, depth in edges:
        r = int(220 * (depth / 6.0))
        g = int(60 * (1.0 - depth / 6.0))
        b = int(180 * (depth / 6.0) + 70)
        draw_line(p1[0], p1[1], p2[0], p2[1], r, g, b)

    # Draw nodes as bottleneck points
    for nx, ny in nodes:
        ix, iy = int(nx), int(ny)
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                qx, qy = ix + dx, iy + dy
                if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                    idx = (qy * WIDTH + qx) * 3
                    buffer[idx] = 250
                    buffer[idx+1] = 200
                    buffer[idx+2] = 220

    plate_path = os.path.join(os.path.dirname(__file__), "failure_023_plate.png")
    write_png(plate_path, WIDTH, HEIGHT, buffer)
    print(f"[✓] Failure 023 Plate generated: {plate_path} ({len(edges)} polymer twigs)")

    # --- ACOUSTIC COLLAPSE (10s 48kHz Stereo) ---
    # The low frequencies disappear completely; only brittle, high-Q clicks and crackles remain
    n_samples = int(SAMPLE_RATE * DURATION_SEC)
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        fade = min(1.0, t / 0.5) * min(1.0, (DURATION_SEC - t) / 0.5)

        # High-frequency brittle crackles (Poisson clicks representing bottleneck pinching)
        click = 0.0
        if random.random() < 0.003: # sporadic clicks
            click = (random.random() - 0.5) * 0.85

        # Thin, hollow, high-frequency harmonic whine (no sub-bass)
        whine = (
            math.sin(2.0 * math.pi * 1740.0 * t) * 0.12
            + math.sin(2.0 * math.pi * 3480.0 * t) * 0.08
            + math.sin(2.0 * math.pi * 5220.0 * t) * 0.04
        ) * (0.8 + 0.2 * math.sin(2.0 * math.pi * 12.0 * t))

        # Thin fluttering (absence of volume)
        flutter = math.sin(2.0 * math.pi * 440.0 * t) * math.sin(2.0 * math.pi * 7.5 * t) * 0.08

        sig = (whine + flutter + click) * fade
        left[i] = max(-1.0, min(1.0, sig * (0.7 + 0.3 * random.random())))
        right[i] = max(-1.0, min(1.0, sig * (0.7 + 0.3 * random.random())))

    audio_path = os.path.join(os.path.dirname(__file__), "failure_023_audio.wav")
    write_wav(audio_path, left, right, SAMPLE_RATE)
    print(f"[✓] Failure 023 Audio synthesized: {audio_path} ({DURATION_SEC}s, 48kHz stereo)")

if __name__ == "__main__":
    generate_failure_023()

