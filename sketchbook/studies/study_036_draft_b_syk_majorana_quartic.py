#!/usr/bin/env python3
"""
STUDY 036 · DRAFT B: SYK MAJORANA CLUSTER & ALL-TO-ALL QUARTIC COUPLINGS
Series XLII · Quantum Chaos & Operator Spreading
Studio Anamnesis · Pure Python Standard Library (png_writer, audio_writer)

Introduces:
1. N = 32 Majorana fermion boundary nodes in a non-local interaction ring
2. Gaussian random quartic couplings J_ijkl with color-coded polarity (amber vs cyan)
3. Emergent holographic bulk interior field with operator spreading wave
4. 15-second 48kHz stereo acoustic study sonifying the 44.0 Hz horizon fundamental and Lyapunov flutter
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

def render_draft_b():
    buffer = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_boundary = 260.0

    N = 32
    random.seed(137)
    
    # Calculate Majorana node coordinates on boundary ring
    nodes = []
    for i in range(N):
        theta = 2.0 * math.pi * i / N
        # Add slight Schwarzian thermal jitter to boundary positions
        r_jit = r_boundary + 3.5 * math.sin(7.0 * theta)
        px = cx + r_jit * math.cos(theta)
        py = cy + r_jit * math.sin(theta)
        nodes.append((px, py, theta))

    # Sample random all-to-all quartic couplings J_ijkl
    # sigma_J = sqrt(6 / N^3) ~= 0.0135
    sigma_J = math.sqrt(6.0 / (N ** 3))
    chords = []
    for i in range(N):
        for j in range(i + 1, N):
            # Probability of connecting edge in active projection
            if random.random() < 0.28:
                weight = random.gauss(0.0, sigma_J * 45.0)
                chords.append((i, j, weight))

    # 1. Background bulk field rendering
    for y in range(HEIGHT):
        ny = y - cy
        for x in range(WIDTH):
            nx = x - cx
            dist = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)

            # Deep cosmic background
            bg_dark = max(0, 12 - int(dist / 40.0))
            r_val = bg_dark
            g_val = bg_dark + 2
            b_val = bg_dark + 8

            if dist < r_boundary:
                # Interior emergent bulk: operator spreading wave
                # Wave expands from boundary toward center as t -> t_*
                norm_r = dist / r_boundary
                bulk_metric = 1.0 / (1.0 - (norm_r * 0.94)**2 + 0.05)
                wave_phase = math.sin(8.0 * math.log(norm_r + 0.08) - angle * 2.0)
                glow = min(1.0, 0.25 * bulk_metric * (0.6 + 0.4 * wave_phase))
                
                # Warm amber and deep teal bulk illumination
                r_val = int(min(255, r_val + glow * 55 * (1.0 - norm_r) + 20 * norm_r))
                g_val = int(min(255, g_val + glow * 40 + 15 * norm_r))
                b_val = int(min(255, b_val + glow * 70 * norm_r + 10))
            else:
                # Exterior asymptotic horizon decay
                d_ext = dist - r_boundary
                glow_ext = math.exp(-d_ext / 35.0) * 0.5
                r_val = int(min(255, r_val + glow_ext * 80))
                g_val = int(min(255, g_val + glow_ext * 50))
                b_val = int(min(255, b_val + glow_ext * 90))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    # 2. Draw non-local quartic coupling chords (hyperbolic arcs curved toward center)
    for i, j, weight in chords:
        p1 = nodes[i]
        p2 = nodes[j]
        
        # Color based on coupling polarity
        if weight >= 0:
            cr, cg, cb = 212, 175, 55  # Amber / Gold (positive coupling)
        else:
            cr, cg, cb = 56, 215, 210  # Electric Cyan (negative coupling)

        mag = min(1.0, abs(weight) * 2.2)
        steps = 140
        for s in range(steps):
            t = s / float(steps)
            # Quadratic bezier curving toward origin
            # Midpoint pulled toward (cx, cy)
            qx = (1 - t)**2 * p1[0] + 2 * (1 - t) * t * (cx + 0.15 * (p1[0] + p2[0] - 2*cx)) + t**2 * p2[0]
            qy = (1 - t)**2 * p1[1] + 2 * (1 - t) * t * (cy + 0.15 * (p1[1] + p2[1] - 2*cy)) + t**2 * p2[1]
            
            px, py = int(qx), int(qy)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                idx = (py * WIDTH + px) * 3
                alpha = mag * 0.45
                buffer[idx] = int(min(255, buffer[idx] * (1.0 - alpha) + cr * alpha))
                buffer[idx + 1] = int(min(255, buffer[idx + 1] * (1.0 - alpha) + cg * alpha))
                buffer[idx + 2] = int(min(255, buffer[idx + 2] * (1.0 - alpha) + cb * alpha))

    # 3. Draw Majorana boundary nodes
    for px, py, theta in nodes:
        ipx, ipy = int(px), int(py)
        node_radius = 5
        for dy in range(-node_radius, node_radius + 1):
            for dx in range(-node_radius, node_radius + 1):
                d_sq = dx*dx + dy*dy
                if d_sq <= node_radius*node_radius:
                    qx, qy = ipx + dx, ipy + dy
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        idx = (qy * WIDTH + qx) * 3
                        # Radiant golden-white node
                        fade = 1.0 - math.sqrt(d_sq) / float(node_radius)
                        buffer[idx] = int(min(255, buffer[idx] + 255 * fade))
                        buffer[idx + 1] = int(min(255, buffer[idx + 1] + 230 * fade))
                        buffer[idx + 2] = int(min(255, buffer[idx + 2] + 160 * fade))

    out_png = os.path.join(os.path.dirname(__file__), "study_036_draft_b_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[STUDY-036-B] Plate Generated: {out_png}")

def synthesize_draft_b_audio():
    duration = 15.0
    total_samples = int(duration * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Telemetry Tier 25 invariants:
    f0 = 44.0               # Horizon fundamental (Hz)
    f_flutter = 1.94        # Lyapunov flutter (Hz)
    f_scramble = 47.99      # Scrambling mode (Hz)
    f_cluster = 248.90      # Majorana cluster mode (Hz)

    random.seed(137)
    # Generate 40 stochastic grain triggers
    grains = []
    for _ in range(50):
        t_start = random.uniform(0.5, duration - 1.5)
        g_freq = random.uniform(180.0, 720.0)
        g_dur = random.uniform(0.04, 0.18)
        g_pan = random.uniform(0.1, 0.9)
        grains.append((t_start, g_freq, g_dur, g_pan))

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)
        
        # Envelope: gradual rise, sustained scrambling, smooth fadeout
        if t < 2.0:
            env = t / 2.0
        elif t > duration - 2.0:
            env = (duration - t) / 2.0
        else:
            env = 1.0

        # Voice 1: Deep horizon drone (44.0 Hz) with Lyapunov flutter amplitude modulation
        flutter_amp = 0.5 + 0.5 * math.sin(2.0 * math.pi * f_flutter * t)
        v1 = math.sin(2.0 * math.pi * f0 * t) * (0.35 + 0.15 * flutter_amp)
        v1 += 0.12 * math.sin(2.0 * math.pi * (f0 * 2.0) * t + 0.4)

        # Voice 2: Scrambling detuned mode (47.99 Hz) with slow stereo spatialization
        pan_phase = math.sin(2.0 * math.pi * 0.12 * t)
        v2 = math.sin(2.0 * math.pi * f_scramble * t) * 0.22

        # Voice 3: Majorana cluster overtone (248.9 Hz) emerging at mid-scrambling time
        t_mid = 7.5
        emerge = math.exp(-((t - t_mid) ** 2) / 10.0)
        v3 = math.sin(2.0 * math.pi * f_cluster * t) * 0.18 * emerge

        # Voice 4: Stochastic grain bursts (Xenakis quartic events)
        v4_l, v4_r = 0.0, 0.0
        for t_s, g_f, g_d, g_p in grains:
            if t_s <= t <= t_s + g_d:
                rel_t = (t - t_s) / g_d
                g_env = math.sin(math.pi * rel_t)
                g_sig = math.sin(2.0 * math.pi * g_f * (t - t_s)) * g_env * 0.14
                v4_l += g_sig * (1.0 - g_p)
                v4_r += g_sig * g_p

        # Combine channels
        sig_l = (v1 * 0.85 + v2 * (0.5 - 0.3 * pan_phase) + v3 * 0.6 + v4_l) * env
        sig_r = (v1 * 0.85 + v2 * (0.5 + 0.3 * pan_phase) + v3 * 0.6 + v4_r) * env

        left[i] = sig_l
        right[i] = sig_r

    # Mastering normalization: ensure peak is strictly <= -1.2 dBFS
    max_peak = max(max(abs(s) for s in left), max(abs(s) for s in right))
    target_peak = 10.0 ** (-1.2 / 20.0)  # ~= 0.871
    scale = (target_peak / max_peak) if max_peak > 0 else 1.0

    left = [s * scale for s in left]
    right = [s * scale for s in right]

    out_wav = os.path.join(os.path.dirname(__file__), "study_036_draft_b_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[STUDY-036-B] Audio Generated: {out_wav} (Peak scaled to -1.2 dBFS)")

if __name__ == "__main__":
    render_draft_b()
    synthesize_draft_b_audio()

