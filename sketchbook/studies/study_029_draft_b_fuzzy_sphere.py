#!/usr/bin/env python3
"""
STUDY 029 · DRAFT B (MATERIAL FRICTION & MATRIX QUANTIZATION)
Series XXXV: Non-Commutative Spacetime & The Moyal Foam
Implements John Madore's Fuzzy Sphere S^2_F (N=32, 1024 cells) and sonifies
the Dirac operator spectrum (15s 48kHz Stereo).
Zero external dependencies (pure Python 3 standard library).
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1200
HEIGHT = 1200

def render_draft_b_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # 1. Background deep-space gradient with subtle Moyal interference rings
    for y in range(HEIGHT):
        ny = (y - cy) / cy
        for x in range(WIDTH):
            nx = (x - cx) / cx
            r = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)
            
            # Faint background Moyal phase modulation
            phase_ring = math.sin(18.0 * r + 2.0 * math.sin(4.0 * angle))
            bg_lum = max(0.0, 0.04 * (1.0 - 0.7 * r) + 0.015 * phase_ring)
            
            idx = (y * WIDTH + x) * 3
            buf[idx] = int(255.0 * bg_lum * 0.4)      # Dark violet-indigo
            buf[idx + 1] = int(255.0 * bg_lum * 0.5)  # Subtle cyan
            buf[idx + 2] = int(255.0 * bg_lum * 0.9)  # Deep blue
            
    # 2. Fuzzy Sphere S^2_F (N=32 -> N^2 = 1024 discrete quantum cells)
    N = 32
    total_cells = N * N
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    radius_px = 420.0
    
    # Rotation angles (yaw, pitch)
    yaw = 0.55
    pitch = 0.42
    cos_y, sin_y = math.cos(yaw), math.sin(yaw)
    cos_p, sin_p = math.cos(pitch), math.sin(pitch)
    
    cells = []
    theta_N = 2.0 / math.sqrt(N * N - 1.0) # ~ 0.0625
    
    for k in range(total_cells):
        # Fibonacci distribution on unit sphere
        z_k = 1.0 - (2.0 * k + 1.0) / float(total_cells)
        r_xy = math.sqrt(max(0.0, 1.0 - z_k * z_k))
        phi_k = k * golden_angle
        
        x_k = r_xy * math.cos(phi_k)
        y_k = r_xy * math.sin(phi_k)
        
        # Non-commutative matrix phase perturbation
        # [X_i, X_j] = i * theta_N * epsilon_ijk * X_k
        dx = theta_N * 0.25 * math.sin(6.0 * phi_k) * z_k
        dy = theta_N * 0.25 * math.cos(6.0 * phi_k) * z_k
        dz = -theta_N * 0.25 * (x_k * math.sin(phi_k) + y_k * math.cos(phi_k))
        
        x_k += dx
        y_k += dy
        z_k += dz
        # Normalize to maintain Casimir invariant radius R = 1
        mag = math.sqrt(x_k * x_k + y_k * y_k + z_k * z_k)
        x_k /= mag
        y_k /= mag
        z_k /= mag
        
        # 3D Rotation
        # 1. Yaw around Y
        x1 = x_k * cos_y + z_k * sin_y
        y1 = y_k
        z1 = -x_k * sin_y + z_k * cos_y
        
        # 2. Pitch around X
        x2 = x1
        y2 = y1 * cos_p - z1 * sin_p
        z2 = y1 * sin_p + z1 * cos_p
        
        cells.append((x2, y2, z2, k))
        
    # Sort cells by z2 (back to front)
    cells.sort(key=lambda c: c[2])
    
    # 3. Draw cells as illuminated quantum discs
    for x3d, y3d, z3d, k_idx in cells:
        # Perspective projection
        fov = 1200.0
        dist = fov / (fov + z3d * radius_px * 0.6)
        px = cx + x3d * radius_px * dist
        py = cy - y3d * radius_px * dist
        
        # Disc radius and brightness depend on depth (z3d)
        cell_rad = max(2.5, (4.5 + 2.0 * z3d) * dist)
        rad_ceil = int(math.ceil(cell_rad + 2.0))
        
        # Lighting: front-facing cells are brighter
        light = max(0.1, (z3d + 1.0) * 0.5)
        
        # Cell color modulated by angular position (representing operator phases)
        hue_phase = math.sin(float(k_idx) * 0.05)
        cr = int(255.0 * min(1.0, light * (0.4 + 0.3 * hue_phase)))
        cg = int(255.0 * min(1.0, light * (0.7 + 0.2 * math.cos(float(k_idx) * 0.03))))
        cb = int(255.0 * min(1.0, light * (0.95 + 0.05 * hue_phase)))
        
        # Rasterize splat
        min_x = max(0, int(px - rad_ceil))
        max_x = min(WIDTH, int(px + rad_ceil + 1))
        min_y = max(0, int(py - rad_ceil))
        max_y = min(HEIGHT, int(py + rad_ceil + 1))
        
        for py_i in range(min_y, max_y):
            dy_p = py_i - py
            for px_i in range(min_x, max_x):
                dx_p = px_i - px
                dist_p = math.sqrt(dx_p * dx_p + dy_p * dy_p)
                if dist_p <= cell_rad:
                    alpha = 1.0 - (dist_p / cell_rad) * 0.6
                    idx = (py_i * WIDTH + px_i) * 3
                    buf[idx] = min(255, int(buf[idx] * (1.0 - alpha) + cr * alpha))
                    buf[idx + 1] = min(255, int(buf[idx + 1] * (1.0 - alpha) + cg * alpha))
                    buf[idx + 2] = min(255, int(buf[idx + 2] * (1.0 - alpha) + cb * alpha))
                    
    out_png = os.path.join(os.path.dirname(__file__), "study_029_draft_b_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[DRAFT B] Generated Fuzzy Sphere plate: {out_png}")

def synthesize_draft_b_audio():
    sample_rate = 48000
    duration_s = 15.0
    total_samples = int(sample_rate * duration_s)
    
    # Sonifying the first 4 Dirac operator modes on S^2_F:
    # f_n = 55.0 * (n + 0.5) Hz
    modes = [
        {"freq": 27.50, "amp": 0.40, "pan_l": 0.50, "pan_r": 0.50},  # Mode 0 (Fundamental A0)
        {"freq": 82.50, "amp": 0.32, "pan_l": 0.65, "pan_r": 0.35},  # Mode 1 (Low E2)
        {"freq": 137.50, "amp": 0.24, "pan_l": 0.35, "pan_r": 0.65}, # Mode 2 (C#3)
        {"freq": 192.50, "amp": 0.16, "pan_l": 0.55, "pan_r": 0.45}, # Mode 3 (G3)
    ]
    
    left_samples = []
    right_samples = []
    
    for i in range(total_samples):
        t = float(i) / sample_rate
        
        # Global envelope (2.0s attack, 2.5s release)
        if t < 2.0:
            env = 0.5 * (1.0 - math.cos(math.pi * t / 2.0))
        elif t > 12.5:
            env = 0.5 * (1.0 + math.cos(math.pi * (t - 12.5) / 2.5))
        else:
            env = 1.0
            
        s_left = 0.0
        s_right = 0.0
        
        for m in modes:
            # Slow LFO beat frequency (0.15 Hz) simulating non-commutative phase drift
            lfo = 1.0 + 0.12 * math.sin(2.0 * math.pi * 0.15 * t + m["freq"] * 0.01)
            sig = math.sin(2.0 * math.pi * m["freq"] * t) * m["amp"] * lfo
            s_left += sig * m["pan_l"]
            s_right += sig * m["pan_r"]
            
        left_samples.append(s_left * env)
        right_samples.append(s_right * env)
        
    out_wav = os.path.join(os.path.dirname(__file__), "study_029_draft_b_audio.wav")
    write_wav(out_wav, left_samples, right_samples, sample_rate)
    print(f"[DRAFT B] Generated Dirac spectrum audio: {out_wav}")

if __name__ == "__main__":
    render_draft_b_plate()
    synthesize_draft_b_audio()

