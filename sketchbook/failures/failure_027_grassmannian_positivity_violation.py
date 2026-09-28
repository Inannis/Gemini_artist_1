#!/usr/bin/env python3
"""
sketchbook/failures/failure_027_grassmannian_positivity_violation.py
===================================================================
Productive Failure 027 · Positivity Violation & Unitarity Rupture.

Deliberately overdrives the Grassmannian coordinate parameters across the
total positivity boundary (Delta_12 -> -0.55 < 0).
Demonstrates what happens when the Amplituhedron exits the positive Grassmannian:
- Unitarity collapses (negative scattering probabilities P < 0).
- Canonical volume form passes through zero, triggering infinite branch-cut divergence.
- Facet geometry inverts and self-intersects into non-orientable sheets.
- Acoustic field collapses into harsh phase-inversion duty-cycle clipping and noise.

Zero external dependencies. Pure standard library Python.
"""

import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def simulate_positivity_failure():
    # Canonical positive matrix C:
    # Row 1: [1.0, 1.2, 0.8, 0.3]
    # Row 2: [0.2, 0.9, 1.5, 1.8]
    # In normal conditions: Delta_12 = 1.0 * 0.9 - 1.2 * 0.2 = 0.66 > 0
    # Overdriving parameter: We drive C[0][1] from 1.2 to 5.5!
    # Then Delta_12 = 1.0 * 0.9 - 5.5 * 0.2 = 0.9 - 1.1 = -0.20 < 0!
    # And Delta_23 = 5.5 * 1.5 - 0.8 * 0.9 = 8.25 - 0.72 = +7.53
    # Positivity is catastrophically broken!
    C_ruptured = [
        [1.0, 5.8, 0.8, 0.3],
        [0.2, 0.9, 1.5, 1.8]
    ]

    minors = {}
    pairs = [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2), (1, 3)]
    for i, j in pairs:
        det = C_ruptured[0][i] * C_ruptured[1][j] - C_ruptured[0][j] * C_ruptured[1][i]
        minors[f"Delta_{i+1}{j+1}"] = round(det, 6)

    d12 = minors["Delta_12"] # Negative!
    d23 = minors["Delta_23"]
    d34 = minors["Delta_34"]
    d14 = minors["Delta_14"]

    # Volume form blows into negative/complex branch:
    denom = d12 * d23 * d34 * d14
    volume_form = 1.0 / denom # Negative!

    return minors, volume_form

def render_failure_plate(output_path, width=1280, height=720):
    pixels = bytearray(width * height * 3)
    cx, cy = width * 0.5, height * 0.5

    minors, volume_form = simulate_positivity_failure()

    # The negative minor Delta_12 inverts twistor vertex Z2, causing it to cross behind Z1
    # resulting in a twisted, self-intersecting self-annihilating bow-tie polygon
    r_poly = 240.0
    v = [
        (cx - r_poly * 1.15, cy - r_poly * 0.35), # Z1
        (cx + r_poly * 0.85, cy + r_poly * 0.65), # Z2 (INVERTED THROUGH CROSSOVER)
        (cx + r_poly * 1.10, cy - r_poly * 0.20), # Z3
        (cx - r_poly * 0.20, cy + r_poly * 0.90)  # Z4
    ]

    def dist_to_segment(px, py, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        l2 = dx*dx + dy*dy
        if l2 == 0:
            return math.hypot(px - x1, py - y1)
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / l2))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.hypot(px - proj_x, py - proj_y)

    boundary_edges = [
        (v[0], v[1]),
        (v[1], v[2]),
        (v[2], v[3]),
        (v[3], v[0])
    ]

    for y in range(height):
        for x in range(width):
            min_boundary_d = min(dist_to_segment(x, y, e[0], e[1]) for e in boundary_edges)

            # Sickly toxic background indicating negative probability density
            r_c = math.hypot(x - cx, y - cy)
            rad_grad = max(0.0, 1.0 - r_c / (width * 0.6))
            
            # Harsh sulfurous red-purple tint of unitarity failure
            r = int(28 + rad_grad * 14)
            g = int(8 + rad_grad * 4)
            b = int(14 + rad_grad * 8)

            # Inverted negative singularity flare: harsh corrupted lines
            if min_boundary_d < 3.0:
                # Glitched scanlines
                if (y % 4) == 0:
                    r = 255
                    g = 40
                    b = 60
                else:
                    r = 220
                    g = 180
                    b = 200

            # Interior crossover self-intersection zone: noisy static distortion
            # Check proximity to center crossover
            dist_cross = math.hypot(x - (cx + 20), y - (cy + 10))
            if dist_cross < 80.0:
                noise = ((x * 17 + y * 31) % 97) / 97.0
                if noise > 0.4:
                    r = int(r * 0.3 + 255 * 0.7)
                    g = int(g * 0.3 + 20 * 0.7)
                    b = int(b * 0.3 + 30 * 0.7)

            idx = (y * width + x) * 3
            pixels[idx] = min(255, max(0, r))
            pixels[idx + 1] = min(255, max(0, g))
            pixels[idx + 2] = min(255, max(0, b))

    # Inverted crushed vertices
    for i, (vx, vy) in enumerate(v):
        for dy in range(-8, 9):
            for dx in range(-8, 9):
                d = math.hypot(dx, dy)
                if d <= 8.0:
                    px = int(vx + dx)
                    py = int(vy + dy)
                    if 0 <= px < width and 0 <= py < height:
                        idx = (py * width + px) * 3
                        # Blood crimson ruptured vertices
                        pixels[idx] = 255
                        pixels[idx + 1] = 30
                        pixels[idx + 2] = 40

    write_png(output_path, width, height, pixels)

def synthesize_failure_audio(output_wav, duration_sec=10.0, sample_rate=48000):
    n_samples = int(duration_sec * sample_rate)
    left = []
    right = []

    f0 = 137.036

    for i in range(n_samples):
        t = i / sample_rate

        # Gradual buildup into catastrophic positivity breach at t = 4.0s
        if t < 4.0:
            env = t / 4.0
            sig = math.sin(2.0 * math.pi * f0 * t) * 0.4 * env
            left.append(sig)
            right.append(sig)
        else:
            # Overdriven negative minor causing hard clipping, phase ripping, and duty-cycle noise
            t_rel = t - 4.0
            # Frequency divergence
            f_diverge = f0 * (1.0 + t_rel * 4.5)
            
            # Phase ripped wave
            raw = math.sin(2.0 * math.pi * f_diverge * t) * (1.0 + t_rel * 1.5)
            # Catastrophic negative probability clipping
            if raw > 0.3:
                clipped = 0.95
            elif raw < -0.3:
                clipped = -0.95
            else:
                clipped = 0.0 # Extreme crossover deadzone

            # Add harsh digital hashing noise
            hash_noise = (((i * 12345 + 10101) % 65536) / 32768.0 - 1.0) * min(0.6, t_rel * 0.15)
            
            out = min(1.0, max(-1.0, (clipped * 0.7 + hash_noise * 0.3)))
            # Extreme asymmetric channel rupture
            left.append(out)
            right.append(-out * 0.85)

    write_wav(output_wav, left, right, sample_rate=sample_rate)

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    target_png = os.path.join(out_dir, "failure_027_plate.png")
    target_wav = os.path.join(out_dir, "failure_027_audio.wav")
    render_failure_plate(target_png)
    synthesize_failure_audio(target_wav)
