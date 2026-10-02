#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 038 · DRAFT C (MATURE SYNTHESIS)
The mature synthesis of Holographic Renormalization Group Flow and the Wheeler-DeWitt Quantum Foam.
Combines multi-scale domain wall warped geometry, Wheeler-DeWitt metric wavefunctional interference,
trans-Planckian bubbling foam lattices, and a 20-second 5-voice polyphonic acoustic suite.
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import random
import struct
import sys
import wave

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png

def render_draft_c_plate(width=1920, height=1080):
    buf = bytearray(width * height * 3)
    # Deep basalt substrate background
    bg_r, bg_g, bg_b = 6, 8, 12
    for i in range(width * height):
        buf[i*3] = bg_r
        buf[i*3+1] = bg_g
        buf[i*3+2] = bg_b

    def blend_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            cur_r = buf[idx]
            cur_g = buf[idx+1]
            cur_b = buf[idx+2]
            buf[idx]   = max(0, min(255, int(cur_r * (1.0 - alpha) + r * alpha)))
            buf[idx+1] = max(0, min(255, int(cur_g * (1.0 - alpha) + g * alpha)))
            buf[idx+2] = max(0, min(255, int(cur_b * (1.0 - alpha) + b * alpha)))

    z_UV = 0.15
    z_IR = 9.00
    z_planck = 0.065
    margin_x = 120
    margin_y = 90
    usable_w = width - 2 * margin_x
    usable_h = height - 2 * margin_y

    # 1. Background Wheeler-DeWitt wavefunctional probability density field |Psi[h]|^2
    # Generates subtle hyperbolic interference fringes on superspace
    for y in range(margin_y, height - margin_y, 4):
        v = (y - margin_y) / usable_h
        zv = z_UV * math.exp(v * math.log(z_IR / z_UV))
        for x in range(margin_x, width - margin_x, 4):
            u = (x - margin_x) / usable_w
            kx = (u - 0.5) * 8.0
            kz = (zv - 1.0) * 3.5
            # Hyperbolic supermetric signature (- + +)
            phase = kz**2 - kx**2
            psi2 = 0.5 * (1.0 + math.cos(phase * 1.5))
            fringe_weight = 0.08 * (1.0 - 0.4 * v)
            fr = int(40 * psi2)
            fg = int(60 * psi2 + 20 * v)
            fb = int(90 * psi2 * (1.0 - v) + 10)
            for dy in range(4):
                for dx in range(4):
                    blend_pixel(x + dx, y + dy, fr, fg, fb, fringe_weight)

    # 2. Holographic domain wall metric foliation (64 warped layers)
    num_layers = 64
    for l_idx in range(num_layers):
        v_layer = l_idx / (num_layers - 1)
        z_layer = z_UV * math.exp(v_layer * math.log(z_IR / z_UV))
        # Running coupling
        g_l = 1.633 / math.sqrt(1.0 + (1.633**2 / 0.10**2 - 1.0) * math.pow(z_layer / z_IR, 0.80))
        warp_shift = 0.15 * (g_l**2) * math.sin(v_layer * math.pi)

        base_y = margin_y + (v_layer + warp_shift * 0.12) * usable_h

        # Metric fluctuation variance: Delta g ~ ell_P / z
        jitter_amp = 24.0 * (z_planck / z_layer)**1.35

        # Palette: UV (iridescent cyan/cobalt) -> Crossover (electric teal) -> IR (burnished amber/gold)
        r_col = int(25 + 225 * (v_layer**1.3))
        g_col = int(160 + 75 * math.sin(v_layer * math.pi * 0.9) - 85 * (v_layer**1.5))
        b_col = int(245 * (1.0 - v_layer**0.7) + 30 * v_layer)

        # Draw contour line with multi-frequency quantum jitter
        for x in range(margin_x, width - margin_x, 2):
            px_norm = (x - margin_x) / usable_w
            fluc1 = jitter_amp * math.sin(px_norm * 18.0 + l_idx * 0.8)
            fluc2 = (jitter_amp * 0.45) * math.cos(px_norm * 42.0 - l_idx * 1.5)
            # Trans-Planckian micro-spikes near boundary
            spike = 0.0
            if z_layer < 0.35:
                spike = (jitter_amp * 0.8) * math.sin(px_norm * 110.0 + l_idx * 3.7)

            py = int(base_y + fluc1 + fluc2 + spike)
            alpha = max(0.25, min(0.95, 0.40 + 0.55 * (1.0 - v_layer * 0.35)))
            blend_pixel(x, py, r_col, g_col, b_col, alpha)
            blend_pixel(x, py + 1, r_col, g_col, b_col, alpha * 0.6)

    # 3. Callan-Symanzik beta flow streamlines (84 graceful curves)
    num_streams = 84
    for s_idx in range(num_streams):
        x_orig = margin_x + int((s_idx / (num_streams - 1)) * usable_w)
        curr_x = float(x_orig)
        for step in range(400):
            v_s = step / 399.0
            z_s = z_UV * math.exp(v_s * math.log(z_IR / z_UV))
            curr_y = margin_y + v_s * usable_h

            # Beta flow curvature: converges toward IR focus points
            dx = 1.6 * math.sin(curr_x * 0.004 + z_s * 1.2) * (1.0 - v_s * 0.4)
            if z_s < 0.45:
                # Stochastic quantum walk perturbation near boundary
                dx += 3.2 * (z_planck / z_s) * math.sin(curr_y * 0.15 + s_idx)

            curr_x += dx
            px = int(curr_x)
            py = int(curr_y)

            # Color along streamline
            sr = int(45 + 195 * v_s)
            sg = int(185 - 85 * v_s)
            sb = int(235 - 175 * v_s)
            blend_pixel(px, py, sr, sg, sb, 0.40)

    # 4. Trans-Planckian Wheeler-DeWitt Foam Micro-Apertures & Virtual Wormholes
    rng = random.Random(137)
    num_foam_cells = 850
    for _ in range(num_foam_cells):
        fx = rng.randint(margin_x - 10, width - margin_x + 10)
        fy = rng.randint(margin_y - 30, margin_y + 110)
        dist_bdry = max(0, fy - margin_y)
        weight = math.exp(-dist_bdry / 28.0)
        rad = rng.randint(2, 7)
        # Brilliant phosphorescent turquoise and white cores
        cr = int(210 * weight + 45)
        cg = int(245 * weight + 70)
        cb = int(255 * weight)
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                d2 = dx*dx + dy*dy
                if d2 <= rad*rad:
                    alpha_cell = 0.42 * weight * (1.0 - d2 / (rad*rad))
                    blend_pixel(fx + dx, fy + dy, cr, cg, cb, alpha_cell)

    out_path = os.path.join(os.path.dirname(__file__), "study_038_draft_c_plate.png")
    write_png(out_path, width, height, buf)
    print(f"Rendered Study 038 Draft C Plate to {out_path}")

def synthesize_draft_c_audio(duration=20.0, sample_rate=48000):
    num_samples = int(duration * sample_rate)
    left_channel = []
    right_channel = []

    # Frequency architecture
    f_ir_fund = 43.20      # Deep macroscopic Kirchhoff-Love fundamental
    f_ir_fifth = 64.80     # Fifth harmonic
    f_wdw_flutter = 86.40  # Wheeler-DeWitt metric fluctuation carrier
    f_c_overtone = 129.60  # Holographic c-function overtone
    f_uv_start = 302.40    # UV mode start frequency

    for n in range(num_samples):
        t = n / sample_rate
        frac = t / duration

        # Master envelope (2.0s fade in, 3.0s fade out)
        fade_in = min(1.0, t / 2.0)
        fade_out = min(1.0, (duration - t) / 3.0)
        master_env = fade_in * fade_out

        # Simulated radial bulk depth: z increases from 0.35 (UV) to 7.50 (deep IR)
        z_t = 0.35 * math.exp(frac * math.log(7.50 / 0.35))
        # Running UV mode frequency sweeping downward as high modes are integrated out
        f_uv_t = f_uv_start * math.pow(0.35 / z_t, 0.60)

        # Voice 1: Macroscopic IR Fundamental (43.2 Hz & 64.8 Hz)
        # Amplitude swells as listener descends into the bulk
        ir_gain = (0.22 + 0.52 * (frac**0.8))
        mod_ir = 1.0 + 0.08 * math.sin(2.0 * math.pi * 0.055 * t)
        v1 = ir_gain * mod_ir * (math.sin(2.0 * math.pi * f_ir_fund * t) + 0.38 * math.sin(2.0 * math.pi * f_ir_fifth * t))

        # Voice 2: Wheeler-DeWitt Metric Flutter (86.4 Hz)
        # High jitter at start, smoothing out into pure harmonic resonance
        flutter_rate = 3.2 * (1.0 - frac * 0.7)
        flutter_amp = 0.18 * math.exp(-frac * 1.8)
        v2 = 0.22 * math.sin(2.0 * math.pi * f_wdw_flutter * t + flutter_amp * math.sin(2.0 * math.pi * flutter_rate * t))

        # Voice 3: Holographic Central Charge c(z) Overtone (129.6 Hz -> 86.4 Hz)
        # Tracks the monotonic thinning of degrees of freedom
        f_c_t = 86.40 + (129.60 - 86.40) * math.exp(-frac * 2.2)
        v3_gain = 0.16 * math.exp(-frac * 1.5)
        v3 = v3_gain * math.sin(2.0 * math.pi * f_c_t * t)

        # Voice 4: Callan-Symanzik Swept UV Tone (302.4 Hz downward sweep)
        uv_gain = 0.24 * (1.0 - frac**0.65)
        v4 = uv_gain * math.sin(2.0 * math.pi * f_uv_t * t + 0.15 * math.sin(2.0 * math.pi * 4.2 * t))

        # Voice 5: Trans-Planckian Granular Quantum Foam Crackle
        # Dense stochastic micro-grains at the UV boundary, vanishing in the deep IR
        foam_gain = 0.20 * math.exp(-frac * 4.2)
        # Non-linear chaotic grain generator
        grain_carrier = math.sin(t * 18765.4) * math.cos(t * 9432.1)
        grain_trigger = math.sin(t * 142.3)
        v5 = foam_gain * grain_carrier if abs(grain_trigger) > 0.72 else 0.0

        # Stereo Panning & Spatial Width
        # IR drone is centered; UV modes pan across stereo field; foam grains sparkle wide
        uv_pan = 0.5 + 0.35 * math.sin(2.0 * math.pi * 0.12 * t)
        foam_pan = 0.5 + 0.45 * math.cos(2.0 * math.pi * 0.35 * t)

        sample_l = master_env * (v1 * 0.75 + v2 * 0.60 + v3 * 0.50 + v4 * (1.0 - uv_pan) + v5 * (1.0 - foam_pan))
        sample_r = master_env * (v1 * 0.75 + v2 * 0.60 + v3 * 0.50 + v4 * uv_pan + v5 * foam_pan)

        left_channel.append(sample_l)
        right_channel.append(sample_r)

    # Master calibration: strictly target -1.10 dBFS peak headroom (amplitude 0.881)
    max_peak = max(max(abs(s) for s in left_channel), max(abs(s) for s in right_channel))
    target_peak = 0.8810  # -1.10 dBFS
    scale = target_peak / max_peak if max_peak > 0 else 1.0

    wav_path = os.path.join(os.path.dirname(__file__), "study_038_draft_c_audio.wav")
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            sl = max(-32767, min(32767, int(left_channel[i] * scale * 32767)))
            sr = max(-32767, min(32767, int(right_channel[i] * scale * 32767)))
            frames.extend(struct.pack("<hh", sl, sr))
        wf.writeframes(frames)

    print(f"Synthesized Study 038 Draft C Audio (20s) to {wav_path}")
    print(f"Mastering: Scale {scale:.4f}, Peak -1.10 dBFS verified.")

if __name__ == "__main__":
    render_draft_c_plate()
    synthesize_draft_c_audio()
