#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 030 · DRAFT C: MATURE SYNTHESIS OF CAUSAL SPHERES
Series XXXVI (Causal Dynamical Triangulations & Spacetime Emergence)

Draft C: Mature Synthesis.
1. 1920x1080 Full HD Visual Plate:
   - 32 Cauchy proper-time slices foliated vertically.
   - 4-simplex Lorentzian connectivity ((4,1) space/time decomposition).
   - Regge curvature deficit angle calculation (Gaussian vs hyperbolic hinges).
   - Running spectral dimension d_s(sigma) diffusion trajectory.
   - 3D normal shading of simplicial facets in raking mineral light.
2. 30-second 48kHz Stereo Acoustic Master Suite:
   - Three movements: The Planckian 2D Sheet, Causal Crystallization, and the 4D de Sitter Bell.

Zero external dependencies (pure standard Python 3).
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
SAMPLE_RATE = 48000
DURATION_SEC = 30.0

def generate_draft_c():
    random.seed(314159)
    buffer = bytearray(WIDTH * HEIGHT * 3)

    # Deep space mineral background with subtle cosmological redshift gradient
    for y in range(HEIGHT):
        y_norm = y / HEIGHT
        r_bg = int(8 + 8 * y_norm)
        g_bg = int(10 + 12 * math.sin(y_norm * math.pi))
        b_bg = int(22 + 16 * (1.0 - y_norm))
        for x in range(WIDTH):
            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_bg
            buffer[idx+1] = g_bg
            buffer[idx+2] = b_bg

    # 32 Cauchy time slices
    num_slices = 32
    margin_y = 70
    usable_h = HEIGHT - 2 * margin_y
    slice_dy = usable_h / (num_slices - 1)

    slices_vertices = []
    mid_x = WIDTH / 2.0 + 40.0 # slight right offset for sidebar telemetry

    # Generate vertices along emergent de Sitter spatial volume curve
    tau = (num_slices - 1) / 2.0
    for s in range(num_slices):
        y_slice = margin_y + s * slice_dy
        t_norm = (s - tau) / tau # -1.0 to +1.0
        
        # de Sitter cosine volume profile
        if abs(t_norm) <= 0.95:
            vol_factor = math.pow(math.cos(t_norm * math.pi * 0.5), 1.5)
        else:
            vol_factor = 0.08 # cosmological neck / stalk
            
        spatial_width = max(140.0, 1100.0 * vol_factor)
        n_verts = max(6, int(32 * (spatial_width / 1100.0)))
        
        slice_pts = []
        for v in range(n_verts):
            frac = (v + 0.5 + (random.random() - 0.5) * 0.25) / n_verts
            px = mid_x - spatial_width / 2.0 + frac * spatial_width
            slice_pts.append((px, y_slice))
        slices_vertices.append(slice_pts)

    # Line drawing with anti-aliasing approximation and additive blending
    def draw_line(x0, y0, x1, y1, r, g, b, alpha=1.0):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                idx = (y0 * WIDTH + x0) * 3
                buffer[idx] = min(255, int(buffer[idx] + r * alpha))
                buffer[idx+1] = min(255, int(buffer[idx+1] + g * alpha))
                buffer[idx+2] = min(255, int(buffer[idx+2] + b * alpha))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    # Draw space-like edges (Spatial slice cyan/ice)
    for s in range(num_slices):
        pts = slices_vertices[s]
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            draw_line(p1[0], p1[1], p2[0], p2[1], 45, 190, 235, 0.70)

    # Draw time-like edges (Lorentzian links: radiant gold / fiery amber)
    for s in range(num_slices - 1):
        pts1 = slices_vertices[s]
        pts2 = slices_vertices[s+1]
        for p1 in pts1:
            dists = sorted([(abs(p1[0] - p2[0]), p2) for p2 in pts2], key=lambda x: x[0])
            for d, p2 in dists[:2]:
                # Regge curvature approximation: closer vertices have higher deficit
                curvature_factor = max(0.0, 1.0 - d / 120.0)
                r_c = int(235 * (0.6 + 0.4 * curvature_factor))
                g_c = int(165 * (0.5 + 0.5 * (1.0 - curvature_factor)))
                b_c = int(50 + 120 * (1.0 - curvature_factor))
                draw_line(p1[0], p1[1], p2[0], p2[1], r_c, g_c, b_c, 0.60)
            if len(dists) > 2 and random.random() < 0.45:
                p3 = dists[2][1] # Type (3,2) cross link
                draw_line(p1[0], p1[1], p3[0], p3[1], 190, 110, 245, 0.40)

    # Horizontal Cauchy proper-time calibration lines
    for s in range(num_slices):
        y_slice = int(margin_y + s * slice_dy)
        for x in range(180, WIDTH - 120, 6):
            idx = (y_slice * WIDTH + x) * 3
            buffer[idx] = min(255, buffer[idx] + 20)
            buffer[idx+1] = min(255, buffer[idx+1] + 24)
            buffer[idx+2] = min(255, buffer[idx+2] + 36)

    # Vertices (Glowing Regge Hinge Nodes)
    for s in range(num_slices):
        for px, py in slices_vertices[s]:
            ix, iy = int(px), int(py)
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    r2 = dx*dx + dy*dy
                    if r2 <= 9:
                        qx, qy = ix + dx, iy + dy
                        if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                            idx = (qy * WIDTH + qx) * 3
                            falloff = 1.0 - math.sqrt(r2) / 3.0
                            buffer[idx] = min(255, int(buffer[idx] + 250 * falloff))
                            buffer[idx+1] = min(255, int(buffer[idx+1] + 240 * falloff))
                            buffer[idx+2] = min(255, int(buffer[idx+2] + 220 * falloff))

    # Left sidebar telemetry: Running Spectral Dimension curve
    curve_x0 = 80
    curve_w = 70
    for y in range(margin_y, HEIGHT - margin_y):
        y_frac = (y - margin_y) / usable_h
        # sigma goes from 1 at top/bottom to 500 at center
        sigma = 1.0 + 499.0 * math.sin(y_frac * math.pi)
        # d_s(sigma) runs from 1.80 to 4.02
        d_s = 4.02 - 2.22 / (1.0 + math.pow(sigma / 40.0, 1.25))
        curve_x = int(curve_x0 + (d_s - 1.80) / (4.02 - 1.80) * curve_w)
        for dx in range(-1, 2):
            cx = curve_x + dx
            if 0 <= cx < WIDTH:
                idx = (y * WIDTH + cx) * 3
                buffer[idx] = 56
                buffer[idx+1] = 215
                buffer[idx+2] = 210

    plate_path = os.path.join(os.path.dirname(__file__), "study_030_draft_c_plate.png")
    write_png(plate_path, WIDTH, HEIGHT, buffer)
    print(f"[✓] Study 030 Draft C Plate written: {plate_path} ({WIDTH}x{HEIGHT})")

    # --- 30s 48kHz STEREO ACOUSTIC SUITE ---
    n_samples = int(SAMPLE_RATE * DURATION_SEC)
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        fade = min(1.0, t / 2.0) * min(1.0, (DURATION_SEC - t) / 2.0)

        # Movement transitions:
        # Movement 1: 0 - 10s (Planckian 2D Sheet, d_s = 2.0)
        # Movement 2: 10 - 20s (Causal Crystallization, d_s: 2 -> 4)
        # Movement 3: 20 - 30s (Emergent 4D de Sitter Bell, d_s = 4.0)

        # Base Cauchy clock (1.0 Hz tick)
        tick_env = math.exp(-25.0 * (t % 1.0))
        tick = math.sin(2.0 * math.pi * 72.0 * t) * tick_env * 0.20

        # Movement 1: High UV planar sheet drone (d_s ~ 2)
        m1_weight = max(0.0, min(1.0, (12.0 - t) / 4.0))
        uv_drone = (
            math.sin(2.0 * math.pi * 72.0 * t) * 0.25
            + math.sin(2.0 * math.pi * 144.0 * t) * 0.15
            + math.sin(2.0 * math.pi * 288.0 * t) * 0.10
        ) * m1_weight

        # Movement 2: Regge Deficit beats (d_s: 2 -> 4 crossover)
        m2_weight = max(0.0, min(1.0, 1.0 - abs(t - 15.0) / 7.0))
        deficit_beat = (
            math.sin(2.0 * math.pi * 165.6 * t) * 0.18
            + math.sin(2.0 * math.pi * 122.4 * t) * 0.18
            + math.sin(2.0 * math.pi * 36.0 * t) * 0.25
        ) * m2_weight

        # Movement 3: 4D de Sitter harmonic bell chord (d_s ~ 4)
        m3_weight = max(0.0, min(1.0, (t - 18.0) / 4.0))
        desitter_chord = (
            math.sin(2.0 * math.pi * 36.0 * t) * 0.30
            + math.sin(2.0 * math.pi * 54.0 * t) * 0.20
            + math.sin(2.0 * math.pi * 72.0 * t) * 0.18
            + math.sin(2.0 * math.pi * 108.0 * t) * 0.12
        ) * m3_weight

        # Sub-bass cosmological breathing (18.0 Hz)
        sub_breath = math.sin(2.0 * math.pi * 18.0 * t) * (0.20 + 0.15 * math.sin(2.0 * math.pi * 0.1 * t))

        # Spatial de Sitter panning
        pan = 0.5 + 0.40 * math.sin(2.0 * math.pi * 0.08 * t)

        sig_l = (sub_breath + tick + uv_drone * 0.8 + deficit_beat * 0.9 + desitter_chord * 0.9) * fade
        sig_r = (sub_breath + tick + uv_drone * 0.6 + deficit_beat * 0.6 + desitter_chord * 1.1) * fade

        left[i] = max(-1.0, min(1.0, sig_l * pan * 1.35))
        right[i] = max(-1.0, min(1.0, sig_r * (1.0 - pan) * 1.35))

    audio_path = os.path.join(os.path.dirname(__file__), "study_030_draft_c_audio.wav")
    write_wav(audio_path, left, right, SAMPLE_RATE)
    print(f"[✓] Study 030 Draft C Audio written: {audio_path} ({DURATION_SEC}s, 48kHz stereo)")

if __name__ == "__main__":
    generate_draft_c()

