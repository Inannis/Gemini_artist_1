#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 025 (DRAFT C: MATURE SYNTHESIS)
The Boltzmann Horizon: Phase-Space Ergodicity & Thermal Reconstitution
Mature algorithmic synthesis combining de Sitter horizon thermal modulation,
multidimensional toroidal phase space orbits, spontaneous crystalline microstate nucleation,
and a 30-second 4-movement acoustic suite featuring Shepard-Risset recurrence glissandi.
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

def render_draft_c_visual():
    print("[DRAFT C] Rendering mature synthesis visual plate...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_horizon = 460.0

    random.seed(137)

    # 1. Background de Sitter Thermal Horizon with Multipole Fluctuations
    # r(theta) = R_0 * (1 + sum_m A_m cos(m*theta + phi_m))
    multipoles = [
        (3, 0.015, 0.4),
        (5, 0.010, 1.2),
        (8, 0.007, 2.5),
        (13, 0.004, 0.8)
    ]

    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            theta = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3

            # Modulated horizon boundary
            r_mod = r_horizon
            for m, amp, phase in multipoles:
                r_mod += r_horizon * amp * math.cos(m * theta + phase)

            if dist < r_mod:
                rel = dist / r_mod
                # Thermal profile with vacuum energy well
                limb = 1.0 / math.sqrt(max(0.005, 1.0 - rel * rel))
                glow = min(220, 14.0 + 9.5 * limb)

                # Microscopic thermal grain
                grain = random.uniform(0.88, 1.12)
                r = int(glow * 0.28 * grain)
                g = int(glow * 0.48 * grain)
                b = int(glow * 0.82 * grain)
            elif abs(dist - r_mod) < 5.0:
                # Boundary thermal glow
                d_wall = abs(dist - r_mod) / 5.0
                intensity = 1.0 - d_wall
                r = int(245 * intensity)
                g = int(225 * intensity)
                b = int(180 * intensity)
            else:
                # Asymptotic de Sitter amnesia void
                decay = math.exp(-(dist - r_mod) / 55.0)
                r = int(10 * decay)
                g = int(14 * decay)
                b = int(24 * decay)

            buf[idx] = min(255, max(0, r))
            buf[idx + 1] = min(255, max(0, g))
            buf[idx + 2] = min(255, max(0, b))

    # 2. Multidimensional Phase Space Toroidal Ergodic Filaments
    # Three incommensurate frequencies: 1.0, phi (1.618033...), sqrt(2) (1.414213...)
    w1 = 1.0
    w2 = 1.61803398875
    w3 = 1.41421356237

    r1 = 290.0
    r2 = 120.0
    r3 = 45.0

    steps = 32000
    dt = 0.009

    for s in range(steps):
        t = s * dt
        tx = (r1 + r2 * math.cos(w2 * t) + r3 * math.cos(w3 * t)) * math.cos(w1 * t)
        ty = ((r1 + r2 * math.cos(w2 * t) + r3 * math.cos(w3 * t)) * math.sin(w1 * t)) * 0.62 + (r2 * math.sin(w2 * t)) * 0.40

        px = int(cx + tx)
        py = int(cy + ty)

        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            idx = (py * WIDTH + px) * 3
            prog = s / float(steps)

            # Palette: Deep indigo -> Luminous cyan -> Warm amber -> Incandescent gold
            if prog < 0.33:
                f = prog / 0.33
                cr = int(30 * (1 - f) + 40 * f)
                cg = int(60 * (1 - f) + 180 * f)
                cb = int(180 * (1 - f) + 240 * f)
            elif prog < 0.66:
                f = (prog - 0.33) / 0.33
                cr = int(40 * (1 - f) + 220 * f)
                cg = int(180 * (1 - f) + 160 * f)
                cb = int(240 * (1 - f) + 70 * f)
            else:
                f = (prog - 0.66) / 0.34
                cr = int(220 * (1 - f) + 255 * f)
                cg = int(160 * (1 - f) + 235 * f)
                cb = int(70 * (1 - f) + 180 * f)

            buf[idx] = min(255, buf[idx] + cr)
            buf[idx + 1] = min(255, buf[idx + 1] + cg)
            buf[idx + 2] = min(255, buf[idx + 2] + cb)

    # 3. Spontaneous Crystalline Microstate Nucleation Clusters
    # Randomly assemble discrete hexagonal/rectilinear memory lattice fragments near center
    cluster_centers = [
        (cx - 90, cy - 40, 28),
        (cx + 85, cy + 50, 32),
        (cx - 30, cy + 80, 22),
        (cx + 40, cy - 75, 25),
        (cx, cy, 45) # Core recurrence seed
    ]

    for kx, ky, krad in cluster_centers:
        for cyc in range(6):
            ang = cyc * (math.pi / 3.0)
            hx = int(kx + krad * math.cos(ang))
            hy = int(ky + krad * math.sin(ang))
            # Draw microstate node
            for ox in range(-3, 4):
                for oy in range(-3, 4):
                    if ox * ox + oy * oy <= 9:
                        px = hx + ox
                        py = hy + oy
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            p_idx = (py * WIDTH + px) * 3
                            buf[p_idx] = min(255, buf[p_idx] + 255)
                            buf[p_idx + 1] = min(255, buf[p_idx + 1] + 235)
                            buf[p_idx + 2] = min(255, buf[p_idx + 2] + 160)

    # 4. Central Recurrence Singularity (The Exact Return)
    for ox in range(-15, 16):
        for oy in range(-15, 16):
            d_sq = ox * ox + oy * oy
            if d_sq <= 225:
                px = int(cx + ox)
                py = int(cy + oy)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    p_idx = (py * WIDTH + px) * 3
                    glow_core = int(255 * math.exp(-d_sq / 50.0))
                    buf[p_idx] = min(255, buf[p_idx] + glow_core)
                    buf[p_idx + 1] = min(255, buf[p_idx + 1] + int(glow_core * 0.92))
                    buf[p_idx + 2] = min(255, buf[p_idx + 2] + int(glow_core * 0.75))

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_025_draft_c_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[+] Draft C Plate written: {out_path}")

def render_draft_c_audio():
    print("[DRAFT C] Synthesizing 30-second 4-movement acoustic suite...")
    sample_rate = 48000
    duration = 30.0
    total_samples = int(sample_rate * duration)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Fundamental frequencies of earlier Cornerstones for Movement IV Return:
    # OPUS-014 (Lithic): 78.4 Hz
    # OPUS-030 (Silica Plate): 43.2 Hz
    # OPUS-031 (Teukolsky): 226.4 Hz
    # OPUS-032 (Higgs Tone): 125.1 Hz
    f_cornerstones = [43.2, 78.4, 125.1, 226.4]

    for i in range(total_samples):
        t = i / float(sample_rate)

        # Movement I: The Gibbons-Hawking Void (0.0s - 8.0s)
        # Deep 32.768 Hz sub-bass drone with stochastic quantum noise clicks
        env_m1 = max(0.0, min(1.0, 1.0 - (t - 6.0) / 2.0)) if t >= 6.0 else (min(1.0, t / 1.5))
        m1_drone = 0.25 * math.sin(2.0 * math.pi * 32.768 * t) + 0.12 * math.sin(2.0 * math.pi * 65.536 * t)
        m1_shot = random.gauss(0.0, 0.02) if random.random() < 0.12 else 0.0
        m1_sig = (m1_drone + m1_shot) * env_m1

        # Movement II: The Shepard-Risset Recurrence Spiral (6.0s - 18.0s)
        env_m2 = 0.0
        if 6.0 <= t <= 18.0:
            if t < 8.0:
                env_m2 = (t - 6.0) / 2.0
            elif t > 16.0:
                env_m2 = (18.0 - t) / 2.0
            else:
                env_m2 = 1.0

        m2_sig = 0.0
        if env_m2 > 0.0:
            t_m2 = t - 6.0
            sweep_rate = 0.10 # octaves/sec
            num_octaves = 8
            base_freq = 27.5
            cyclic_t = (t_m2 * sweep_rate) % 1.0
            octave_center = math.log2(220.0 / base_freq)
            octave_sigma = 1.4

            for oct_idx in range(num_octaves):
                oct_pos = oct_idx + cyclic_t
                freq = base_freq * math.pow(2.0, oct_pos)
                dist_oct = oct_pos - octave_center
                amp = math.exp(-0.5 * (dist_oct / octave_sigma) ** 2)
                phase = (2.0 * math.pi * freq * t) % (2.0 * math.pi)
                m2_sig += amp * math.sin(phase)
            m2_sig = (m2_sig * 0.22) * env_m2

        # Movement III: Spontaneous Crystalline Microstate Assembly (15.0s - 24.0s)
        env_m3 = 0.0
        if 15.0 <= t <= 24.0:
            if t < 17.0:
                env_m3 = (t - 15.0) / 2.0
            elif t > 22.0:
                env_m3 = (24.0 - t) / 2.0
            else:
                env_m3 = 1.0

        m3_sig = 0.0
        if env_m3 > 0.0:
            # Quartz crystal chimes (Bessel modal frequencies of 120mm wafer)
            chimes = [43.2, 89.4, 235.4, 520.1, 1040.2]
            for c_idx, cf in enumerate(chimes):
                t_strike = (t * (c_idx + 1.3)) % 1.2
                decay = math.exp(-t_strike * 4.5)
                m3_sig += 0.08 * math.sin(2.0 * math.pi * cf * t) * decay
            m3_sig = m3_sig * env_m3

        # Movement IV: The Poincaré Recurrence Chord (22.0s - 30.0s)
        env_m4 = 0.0
        if t >= 22.0:
            t_m4 = t - 22.0
            if t_m4 < 2.5:
                env_m4 = t_m4 / 2.5
            else:
                env_m4 = max(0.0, 1.0 - (t_m4 - 2.5) / 5.5)

        m4_sig = 0.0
        if env_m4 > 0.0:
            for f_val in f_cornerstones:
                m4_sig += 0.15 * math.sin(2.0 * math.pi * f_val * t)
                m4_sig += 0.06 * math.sin(2.0 * math.pi * f_val * 2.0 * t)
            m4_sig = m4_sig * env_m4

        # Combine all movements
        sample_val = m1_sig + m2_sig + m3_sig + m4_sig

        # Soft saturation to prevent clipping
        sample_val = math.tanh(sample_val)

        # Dynamic spatial imaging
        pan = 0.5 + 0.20 * math.sin(2.0 * math.pi * 0.08 * t)
        left[i] = sample_val * math.sqrt(1.0 - pan)
        right[i] = sample_val * math.sqrt(pan)

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_025_draft_c_audio.wav"))
    write_wav(out_path, left, right, sample_rate=sample_rate)
    print(f"[+] Draft C Audio written: {out_path}")

if __name__ == "__main__":
    render_draft_c_visual()
    render_draft_c_audio()

