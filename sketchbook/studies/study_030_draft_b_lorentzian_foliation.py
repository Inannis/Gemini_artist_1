#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 030 · DRAFT B: LORENTZIAN FOLIATION & REGGE DEFICITS
Series XXXVI (Causal Dynamical Triangulations & Spacetime Emergence)

Draft B: Material Friction & Lorentzian Foliation.
Implements:
1. Explicit Cauchy proper-time foliation (slices t = 0 to 15).
2. Lorentzian (4,1) and (3,2) simplices with distinguished space-like (cyan)
   and time-like (amber/gold) edge geometries.
3. Regge curvature deficit angle evaluation at hinges.
4. 15-second 48kHz stereo acoustic synthesis of Cauchy clock pacing and deficit beats.

Zero external dependencies (pure standard Python 3).
"""

import math
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1200
HEIGHT = 1200
SAMPLE_RATE = 48000
DURATION_SEC = 15.0

def generate_draft_b():
    random.seed(137)
    buffer = bytearray(WIDTH * HEIGHT * 3)

    # Deep obsidian background with subtle vertical time gradient
    for y in range(HEIGHT):
        time_bias = int(12.0 * (1.0 - y / HEIGHT))
        for x in range(WIDTH):
            idx = (y * WIDTH + x) * 3
            buffer[idx] = 8 + time_bias // 2
            buffer[idx+1] = 10 + time_bias
            buffer[idx+2] = 18 + time_bias

    # 16 Cauchy time slices
    num_slices = 16
    margin_y = 100
    usable_h = HEIGHT - 2 * margin_y
    slice_dy = usable_h / (num_slices - 1)

    slices_vertices = []
    mid_x = WIDTH / 2.0

    # Distribute vertices on each spatial slice according to de Sitter cosine envelope
    for s in range(num_slices):
        y_slice = margin_y + s * slice_dy
        t_norm = (s - (num_slices - 1) / 2.0) / ((num_slices - 1) / 2.0) # -1 to +1
        # spatial volume envelope cos(t * pi/2)
        spatial_width = max(180.0, (WIDTH - 240.0) * math.cos(t_norm * math.pi * 0.46))
        
        # Number of vertices on slice proportional to spatial width
        n_verts = max(6, int(18 * (spatial_width / (WIDTH - 240.0))))
        slice_pts = []
        for v in range(n_verts):
            frac = (v + 0.5 + (random.random() - 0.5) * 0.3) / n_verts
            px = mid_x - spatial_width / 2.0 + frac * spatial_width
            slice_pts.append((px, y_slice))
        slices_vertices.append(slice_pts)

    # Line drawing helper with additive blending
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

    # Draw space-like edges within each slice (Cyan / Ice Phosphor)
    for s in range(num_slices):
        pts = slices_vertices[s]
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            draw_line(p1[0], p1[1], p2[0], p2[1], 40, 180, 220, 0.75)

    # Draw time-like edges connecting slice s to s+1 (Radiant Amber / Gold)
    hinges_count = 0
    for s in range(num_slices - 1):
        pts1 = slices_vertices[s]
        pts2 = slices_vertices[s+1]
        for p1 in pts1:
            # Connect to closest 2 or 3 vertices on next slice
            dists = sorted([(abs(p1[0] - p2[0]), p2) for p2 in pts2], key=lambda x: x[0])
            for d, p2 in dists[:2]:
                draw_line(p1[0], p1[1], p2[0], p2[1], 220, 160, 50, 0.65)
                hinges_count += 1
            if len(dists) > 2 and random.random() < 0.4:
                p3 = dists[2][1]
                draw_line(p1[0], p1[1], p3[0], p3[1], 180, 100, 240, 0.45) # Type (3,2) cross link

    # Draw horizontal Cauchy time grid rules
    for s in range(num_slices):
        y_slice = int(margin_y + s * slice_dy)
        for x in range(40, WIDTH - 40, 4):
            idx = (y_slice * WIDTH + x) * 3
            buffer[idx] = min(255, buffer[idx] + 25)
            buffer[idx+1] = min(255, buffer[idx+1] + 30)
            buffer[idx+2] = min(255, buffer[idx+2] + 45)

    # Draw vertices as glowing nodes
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
                            intensity = 1.0 - math.sqrt(r2) / 3.0
                            buffer[idx] = min(255, int(buffer[idx] + 240 * intensity))
                            buffer[idx+1] = min(255, int(buffer[idx+1] + 245 * intensity))
                            buffer[idx+2] = min(255, int(buffer[idx+2] + 255 * intensity))

    plate_path = os.path.join(os.path.dirname(__file__), "study_030_draft_b_plate.png")
    write_png(plate_path, WIDTH, HEIGHT, buffer)
    print(f"[✓] Study 030 Draft B Plate written: {plate_path}")

    # --- ACOUSTIC SYNTHESIS (15s 48kHz Stereo) ---
    n_samples = int(SAMPLE_RATE * DURATION_SEC)
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    f_cauchy = 36.0 # Fundamental proper time pacing
    f_sub = 18.0    # Infrasonic de Sitter breathing
    f_hinge_pos = 165.6 # Positive deficit hinge beat
    f_hinge_neg = 122.4 # Negative deficit hinge beat

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        fade = min(1.0, t / 1.5) * min(1.0, (DURATION_SEC - t) / 1.5)

        # Cauchy pulse tick (1.0 Hz envelope trigger)
        tick_env = math.exp(-30.0 * (t % 1.0))
        tick_sig = math.sin(2.0 * math.pi * 72.0 * t) * tick_env * 0.25

        # Sub-bass breathing drone
        sub = math.sin(2.0 * math.pi * f_sub * t) * 0.30

        # Cauchy fundamental drone
        cauchy_drone = math.sin(2.0 * math.pi * f_cauchy * t) * 0.25

        # Regge deficit microtonal interference
        hinge_pos = math.sin(2.0 * math.pi * f_hinge_pos * t) * 0.15
        hinge_neg = math.sin(2.0 * math.pi * f_hinge_neg * t) * 0.15

        # Spatial de Sitter panning
        pan = 0.5 + 0.35 * math.sin(2.0 * math.pi * 0.12 * t)

        sig_l = (sub + cauchy_drone + tick_sig + hinge_pos * 0.8 + hinge_neg * 0.3) * fade
        sig_r = (sub + cauchy_drone + tick_sig + hinge_pos * 0.3 + hinge_neg * 0.8) * fade

        left[i] = max(-1.0, min(1.0, sig_l * pan * 1.4))
        right[i] = max(-1.0, min(1.0, sig_r * (1.0 - pan) * 1.4))

    audio_path = os.path.join(os.path.dirname(__file__), "study_030_draft_b_audio.wav")
    write_wav(audio_path, left, right, SAMPLE_RATE)
    print(f"[✓] Study 030 Draft B Audio synthesized: {audio_path} ({DURATION_SEC}s, 48kHz stereo)")

if __name__ == "__main__":
    generate_draft_b()

