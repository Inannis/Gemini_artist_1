#!/usr/bin/env python3
"""
STUDY 036 · DRAFT C: MATURE SYNTHESIS — THE SCRAMBLING HORIZON & SYK BULK GEOMETRY
Series XLII · Quantum Chaos & Holographic Operator Spreading
Studio Anamnesis · Pure Python Standard Library (png_writer, audio_writer)

Mature synthesis integrating:
1. 32 Majorana fermion nodes with hyperbolic Poincaré geodesics and multi-chords
2. Concentric operator-spreading wavefronts propagating inward at maximal Lyapunov speed
3. Schwarzian boundary soft-mode fluctuations undulating along the AdS2 perimeter
4. Nuanced chromatic stratification: obsidian base, cobalt depth, electric cyan, radiant amber, and incandescent white
5. 20-second 48kHz polyphonic acoustic suite calibrated with harmonic_spectrum_analyzer
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

def render_draft_c():
    buffer = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_disc = 270.0
    N = 32

    random.seed(2026)
    
    # 1. Compute Majorana boundary nodes with Schwarzian boundary fluctuations:
    # Cutoff curve: r(theta) = R_0 + sum_k c_k cos(k theta + phi_k)
    nodes = []
    for i in range(N):
        theta = 2.0 * math.pi * i / N
        # Schwarzian reparametrization fluctuation modes (k = 2, 3, 4)
        fluc = 5.2 * math.cos(2.0 * theta + 0.4) + 3.1 * math.sin(3.0 * theta - 0.8) + 1.8 * math.cos(5.0 * theta + 1.2)
        r_node = r_disc + fluc
        px = cx + r_node * math.cos(theta)
        py = cy + r_node * math.sin(theta)
        nodes.append((px, py, theta))

    # Sample all-to-all quartic couplings J_ijkl
    sigma_J = math.sqrt(6.0 / (N ** 3))
    chords = []
    for i in range(N):
        for j in range(i + 1, N):
            prob = 0.32
            if random.random() < prob:
                coupling = random.gauss(0.0, sigma_J * 50.0)
                chords.append((i, j, coupling))

    # 2. Render pixel buffer (Hyperbolic AdS2 bulk + OTOC operator wave)
    for y in range(HEIGHT):
        ny = y - cy
        for x in range(WIDTH):
            nx = x - cx
            dist = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)

            # Deep obsidian-slate background with subtle radial gradation
            dist_center = math.sqrt(nx*nx + ny*ny)
            bg_lum = max(4, int(14 - dist_center / 65.0))
            r_val = bg_lum
            g_val = bg_lum + 2
            b_val = bg_lum + 7

            if dist < r_disc + 12.0:
                norm_u = min(0.98, dist / r_disc)
                # Poincaré metric factor: ds^2 = 4 (dx^2 + dy^2) / (1 - u^2)^2
                poincare_conf = 1.0 / max(0.04, (1.0 - norm_u**2))

                # OTOC Operator spreading front:
                # Radial wave moving from boundary (norm_u = 1) toward center (norm_u = 0)
                wave1 = math.sin(12.0 * math.log(norm_u + 0.04) - 2.5 * angle)
                wave2 = math.cos(18.0 * (1.0 - norm_u) + angle * 3.0)
                front = (wave1 * 0.6 + wave2 * 0.4)

                # Core holographic condensation
                core_glow = math.exp(-(norm_u * 3.2)**2) * 1.8
                edge_glow = math.exp(-((norm_u - 1.0) / 0.12)**2) * 1.4

                # Color synthesis:
                # Center: deep cobalt & violet AdS interior
                # Spreading front: radiant gold and amber
                # Boundary: electric cyan Schwarzian boundary
                r_val = int(min(255, r_val + core_glow * 45 + edge_glow * 110 + max(0.0, front) * 65 * norm_u))
                g_val = int(min(255, g_val + core_glow * 35 + edge_glow * 140 + max(0.0, front) * 85 * norm_u))
                b_val = int(min(255, b_val + core_glow * 120 + edge_glow * 180 + max(0.0, front) * 40 * (1.0 - norm_u)))
            else:
                # Exterior asymptotic thermal decay
                d_ext = dist - r_disc
                ext_falloff = math.exp(-d_ext / 28.0) * 0.4
                r_val = int(min(255, r_val + ext_falloff * 90))
                g_val = int(min(255, g_val + ext_falloff * 70))
                b_val = int(min(255, b_val + ext_falloff * 110))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    # 3. Draw Hyperbolic Geodesic Chords
    for i, j, coupling in chords:
        p1 = nodes[i]
        p2 = nodes[j]
        # Hyperbolic curvature: pull chord midpoint toward center based on boundary distance
        th1, th2 = p1[2], p2[2]
        d_th = abs(th1 - th2)
        if d_th > math.pi:
            d_th = 2.0 * math.pi - d_th
        pull = math.sin(d_th / 2.0) * 0.85

        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0
        ctrl_x = mid_x * (1.0 - pull) + cx * pull
        ctrl_y = mid_y * (1.0 - pull) + cy * pull

        # Color based on coupling polarity
        if coupling > 0:
            cr, cg, cb = 224, 182, 60   # Radiant Amber Gold
        else:
            cr, cg, cb = 64, 220, 215   # Electric Horizon Cyan

        alpha = min(0.65, abs(coupling) * 2.8 + 0.15)
        steps = 180
        for s in range(steps):
            t = s / float(steps)
            qx = (1 - t)**2 * p1[0] + 2 * (1 - t) * t * ctrl_x + t**2 * p2[0]
            qy = (1 - t)**2 * p1[1] + 2 * (1 - t) * t * ctrl_y + t**2 * p2[1]
            px, py = int(qx), int(qy)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                idx = (py * WIDTH + px) * 3
                buffer[idx] = int(min(255, buffer[idx] * (1.0 - alpha) + cr * alpha))
                buffer[idx + 1] = int(min(255, buffer[idx + 1] * (1.0 - alpha) + cg * alpha))
                buffer[idx + 2] = int(min(255, buffer[idx + 2] * (1.0 - alpha) + cb * alpha))

    # 4. Draw Majorana Nodes and Boundary Halo
    for px, py, theta in nodes:
        ipx, ipy = int(px), int(py)
        node_radius = 6
        for dy in range(-node_radius, node_radius + 1):
            for dx in range(-node_radius, node_radius + 1):
                d_sq = dx*dx + dy*dy
                if d_sq <= node_radius*node_radius:
                    qx, qy = ipx + dx, ipy + dy
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        idx = (qy * WIDTH + qx) * 3
                        fade = 1.0 - (math.sqrt(d_sq) / float(node_radius))
                        buffer[idx] = int(min(255, buffer[idx] + 255 * fade))
                        buffer[idx + 1] = int(min(255, buffer[idx + 1] + 240 * fade))
                        buffer[idx + 2] = int(min(255, buffer[idx + 2] + 200 * fade))

    out_png = os.path.join(os.path.dirname(__file__), "study_036_draft_c_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[STUDY-036-C] Plate Generated: {out_png}")

def synthesize_draft_c_audio():
    duration = 20.0
    total_samples = int(duration * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Invariants from Tier 25:
    f0 = 44.0               # Horizon fundamental (Hz)
    lambda_syk = 0.2764     # Lyapunov exponent (s^-1)
    f_flutter = 1.94        # Flutter frequency (Hz)
    t_star = 11.03          # Fast scrambling time (s)

    random.seed(2026)
    # 75 stochastic grain events (Xenakis quartic triggers)
    grains = []
    for _ in range(75):
        t_start = random.uniform(0.5, duration - 1.5)
        g_freq = random.uniform(140.0, 960.0)
        g_dur = random.uniform(0.03, 0.22)
        g_pan = random.uniform(0.05, 0.95)
        grains.append((t_start, g_freq, g_dur, g_pan))

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)

        # Master envelope
        if t < 2.5:
            env = t / 2.5
        elif t > duration - 2.5:
            env = (duration - t) / 2.5
        else:
            env = 1.0

        # Voice 1: 44.0 Hz deep AdS2 horizon fundamental with 88.0 Hz second harmonic
        flutter_amp = 0.65 + 0.35 * math.sin(2.0 * math.pi * f_flutter * t)
        v1 = math.sin(2.0 * math.pi * f0 * t) * 0.32 * flutter_amp
        v1 += math.sin(2.0 * math.pi * (f0 * 2.0) * t + 0.3) * 0.12 * flutter_amp
        v1 += math.sin(2.0 * math.pi * (f0 * 3.0) * t + 0.6) * 0.05

        # Voice 2: Ascending Lyapunov operator spreading sweep
        # Sweep accelerates at rate lambda_syk
        sweep_ratio = math.exp(lambda_syk * min(t, t_star) * 0.25)
        f_sweep = f0 * (1.0 + 0.45 * sweep_ratio)
        pan_sweep = math.sin(2.0 * math.pi * 0.15 * t)
        v2 = math.sin(2.0 * math.pi * f_sweep * t) * 0.18

        # Voice 3: Majorana cluster overtone ladder (248.9 Hz & 352.0 Hz)
        v3 = (math.sin(2.0 * math.pi * 248.9 * t) * 0.12 +
              math.sin(2.0 * math.pi * 352.0 * t + 0.5) * 0.08)
        # Intensity peaks around t = t_star (11.03 s)
        scramble_bell = math.exp(-((t - t_star) ** 2) / 12.0)
        v3 *= (0.3 + 0.7 * scramble_bell)

        # Voice 4: Stochastic Xenakis grain pulses
        v4_l, v4_r = 0.0, 0.0
        for t_s, g_f, g_d, g_p in grains:
            if t_s <= t <= t_s + g_d:
                rel_t = (t - t_s) / g_d
                g_env = math.sin(math.pi * rel_t)
                g_sig = math.sin(2.0 * math.pi * g_f * (t - t_s)) * g_env * 0.12
                v4_l += g_sig * (1.0 - g_p)
                v4_r += g_sig * g_p

        # Voice 5: High-frequency Schwarzian boundary shimmer (704.0 Hz, 880.0 Hz)
        v5 = math.sin(2.0 * math.pi * 704.0 * t) * 0.04 * math.sin(2.0 * math.pi * 0.25 * t)**2

        sig_l = (v1 * 0.85 + v2 * (0.5 - 0.3 * pan_sweep) + v3 * 0.5 + v4_l + v5 * 0.4) * env
        sig_r = (v1 * 0.85 + v2 * (0.5 + 0.3 * pan_sweep) + v3 * 0.5 + v4_r + v5 * 0.6) * env

        left[i] = sig_l
        right[i] = sig_r

    # Master calibration: ensure peak is strictly <= -1.2 dBFS
    max_peak = max(max(abs(s) for s in left), max(abs(s) for s in right))
    target_peak = 10.0 ** (-1.2 / 20.0)  # ~= 0.871
    scale = (target_peak / max_peak) if max_peak > 0 else 1.0

    left = [s * scale for s in left]
    right = [s * scale for s in right]

    out_wav = os.path.join(os.path.dirname(__file__), "study_036_draft_c_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[STUDY-036-C] Audio Generated: {out_wav} (Peak scaled to -1.2 dBFS)")

if __name__ == "__main__":
    render_draft_c()
    synthesize_draft_c_audio()

