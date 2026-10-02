#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 038 · DRAFT B (MATERIAL FRICTION)
Incorporates non-conformal domain wall warping, Callan-Symanzik beta flow streamlines,
scale-dependent metric jitter, and synthesizes a 15-second 48kHz stereo acoustic trial.
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import struct
import sys
import wave

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png

def render_draft_b_plate(width=1600, height=1000):
    buf = bytearray(width * height * 3)
    # Deep obsidian background
    bg_r, bg_g, bg_b = 8, 10, 15
    for i in range(width * height):
        buf[i*3] = bg_r
        buf[i*3+1] = bg_g
        buf[i*3+2] = bg_b

    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            cur_r = buf[idx]
            cur_g = buf[idx+1]
            cur_b = buf[idx+2]
            buf[idx]   = int(cur_r * (1.0 - alpha) + r * alpha)
            buf[idx+1] = int(cur_g * (1.0 - alpha) + g * alpha)
            buf[idx+2] = int(cur_b * (1.0 - alpha) + b * alpha)

    z_UV = 0.20
    z_IR = 8.00
    z_planck = 0.08
    margin_x = 100
    margin_y = 80
    usable_w = width - 2 * margin_x
    usable_h = height - 2 * margin_y

    # 1. Draw non-conformal domain wall warp contours (logarithmic radial slicing)
    num_slices = 48
    for s in range(num_slices):
        u = s / (num_slices - 1)
        # Logarithmic radial depth with backreaction
        z_val = z_UV * math.exp(u * math.log(z_IR / z_UV))
        # Callan-Symanzik running coupling
        g_val = 1.633 / math.sqrt(1.0 + (1.633**2 / 0.10**2 - 1.0) * math.pow(z_val / z_IR, 0.80))
        warp_corr = 0.12 * (g_val**2)
        y_slice = int(margin_y + (u + warp_corr * 0.15) * usable_h)

        # Scale-dependent metric jitter variance: Delta x ~ ell_P / z
        jitter_amp = 18.0 * (z_planck / z_val)**1.2

        # Color: transition from electric cyan-violet (UV) to rich amber-bronze (IR)
        r_col = int(30 + 210 * u)
        g_col = int(140 + 60 * math.sin(u * math.pi) - 70 * u)
        b_col = int(240 - 200 * u)

        # Draw warped horizontal contour with metric jitter
        for x in range(margin_x, width - margin_x, 2):
            phase = (x - margin_x) * 0.02
            # Metric fluctuation wave from Wheeler-DeWitt supermetric
            fluct = jitter_amp * math.sin(phase * 4.0 + s * 1.3) * math.cos(phase * 2.5)
            # Higher jitter near UV boundary
            if z_val < 0.6:
                fluct += (jitter_amp * 0.8) * math.sin(phase * 15.0 + s)
            py = int(y_slice + fluct)
            alpha = max(0.2, min(0.9, 0.3 + 0.6 * (1.0 - u * 0.4)))
            set_pixel(x, py, r_col, g_col, b_col, alpha)
            set_pixel(x, py + 1, r_col, g_col, b_col, alpha * 0.7)

    # 2. Draw Callan-Symanzik beta flow streamlines descending into the bulk
    num_streamlines = 72
    for str_idx in range(num_streamlines):
        x_start = margin_x + int((str_idx / (num_streamlines - 1)) * usable_w)
        curr_x = float(x_start)
        for step in range(300):
            u_step = step / 299.0
            z_step = z_UV * math.exp(u_step * math.log(z_IR / z_UV))
            curr_y = margin_y + u_step * usable_h

            # Beta flow vector: streamlines bend inward or outward based on coupling gradient
            dx = 1.2 * math.sin((curr_x * 0.005) + z_step * 1.5) * (1.0 - u_step * 0.5)
            # Add quantum foam scatter near UV
            if z_step < 0.5:
                dx += 2.5 * (z_planck / z_step) * math.sin(curr_y * 0.1)

            curr_x += dx
            px = int(curr_x)
            py = int(curr_y)

            # Color blend along streamline
            sr = int(60 + 180 * u_step)
            sg = int(180 - 80 * u_step)
            sb = int(220 - 150 * u_step)
            set_pixel(px, py, sr, sg, sb, 0.45)

    # 3. Wheeler-DeWitt quantum foam micro-apertures at the UV boundary (top)
    import random
    rng = random.Random(42)
    num_foam_cells = 450
    for _ in range(num_foam_cells):
        fx = rng.randint(margin_x, width - margin_x)
        fy = rng.randint(margin_y - 20, margin_y + 80)
        # Intensity falls off rapidly as we move away from the boundary
        dist_from_bdry = max(0, fy - margin_y)
        foam_weight = math.exp(-dist_from_bdry / 25.0)
        cell_r = rng.randint(2, 6)
        cr = int(180 * foam_weight + 50)
        cg = int(220 * foam_weight + 80)
        cb = int(255 * foam_weight)
        for dy in range(-cell_r, cell_r + 1):
            for dx in range(-cell_r, cell_r + 1):
                if dx*dx + dy*dy <= cell_r*cell_r:
                    set_pixel(fx + dx, fy + dy, cr, cg, cb, 0.35 * foam_weight)

    out_path = os.path.join(os.path.dirname(__file__), "study_038_draft_b_plate.png")
    write_png(out_path, width, height, buf)
    print(f"Rendered Study 038 Draft B Plate to {out_path}")

def synthesize_draft_b_audio(duration=15.0, sample_rate=48000):
    num_samples = int(duration * sample_rate)
    left_channel = []
    right_channel = []

    # Frequency parameters
    f_ir_base = 43.20      # Deep macroscopic IR fundamental
    f_fifth = 64.80        # Fifth harmonic
    f_uv_start = 280.0     # UV mode start frequency

    # Synthesize multi-scale RG flow descent
    for n in range(num_samples):
        t = n / sample_rate
        frac = t / duration

        # Smooth envelope (fade-in 1.5s, fade-out 2.0s)
        fade_in = min(1.0, t / 1.5)
        fade_out = min(1.0, (duration - t) / 2.0)
        env = fade_in * fade_out

        # Simulated radial descent: z increases from 0.4 to 6.5 over duration
        z_t = 0.40 * math.exp(frac * math.log(6.5 / 0.40))
        # High-energy UV mode frequency sweeps downward
        f_uv_t = f_uv_start * math.pow(0.40 / z_t, 0.5)

        # 1. Macroscopic IR base drone (43.2 Hz and 64.8 Hz) - grows as we enter bulk
        ir_gain = 0.25 + 0.45 * frac
        s_ir = ir_gain * (math.sin(2.0 * math.pi * f_ir_base * t) + 0.4 * math.sin(2.0 * math.pi * f_fifth * t))

        # 2. Callan-Symanzik swept UV tone - decays as modes are integrated out
        uv_gain = (1.0 - frac * 0.8) * 0.30
        s_uv = uv_gain * math.sin(2.0 * math.pi * f_uv_t * t + 0.2 * math.sin(2.0 * math.pi * 3.5 * t))

        # 3. Trans-Planckian foam crackle (pseudo-random granular noise, concentrated at start)
        foam_gain = math.exp(-frac * 3.5) * 0.18
        # Simple chaotic generator for repeatable granular clicks
        grain = math.sin(t * 12345.67) * math.cos(t * 7891.23)
        s_foam = foam_gain * grain if abs(grain) > 0.6 else 0.0

        # Stereo positioning: UV high-modes pan left-to-right, IR anchors center
        pan = 0.5 + 0.3 * math.sin(2.0 * math.pi * 0.1 * t)
        sample_l = env * (s_ir * 0.7 + s_uv * (1.0 - pan) + s_foam * 0.8)
        sample_r = env * (s_ir * 0.7 + s_uv * pan + s_foam * 0.2)

        left_channel.append(sample_l)
        right_channel.append(sample_r)

    # Master calibration: target peak -1.00 dBFS (amplitude 0.891)
    max_val = max(max(abs(s) for s in left_channel), max(abs(s) for s in right_channel))
    target_peak = 0.89125  # -1.00 dBFS
    scale = target_peak / max_val if max_val > 0 else 1.0

    wav_path = os.path.join(os.path.dirname(__file__), "study_038_draft_b_audio.wav")
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

    print(f"Synthesized Study 038 Draft B Audio (15s) to {wav_path}")
    print(f"Mastering: Scale {scale:.4f}, Peak -1.00 dBFS verified.")

if __name__ == "__main__":
    render_draft_b_plate()
    synthesize_draft_b_audio()
