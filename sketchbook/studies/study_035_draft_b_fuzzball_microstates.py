#!/usr/bin/env python3
"""
STUDY 035 · DRAFT B: FUZZBALL MICROSTATES & BUBBLING GEOMETRIES
Series XLI · Black Hole Information Resolution
Studio Anamnesis · Pure Python Standard Library (png_writer, audio_writer)

Introduces:
1. Multi-center Gibbons-Hawking bubbling cycles (topological 2-cycles)
2. Fractionated string windings crossing the horizon radius
3. Multi-spectral quantum palette (deep violet, cobalt, incandescent gold)
4. 15-second acoustic study sonifying the fractionated string ladder
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
    r_fuzz = 220.0

    # 12 Gibbons-Hawking bubbling centers inside the horizon-scale fuzzball
    random.seed(42)
    centers = []
    for _ in range(14):
        angle = random.uniform(0, 2.0 * math.pi)
        dist = random.uniform(20.0, r_fuzz * 0.92)
        charge = random.uniform(0.6, 1.4)
        centers.append((cx + dist * math.cos(angle), cy + dist * math.sin(angle), charge))

    # Render image buffer
    for y in range(HEIGHT):
        ny = y - cy
        for x in range(WIDTH):
            nx = x - cx
            dist = math.sqrt(nx * nx + ny * ny)

            # Harmonic function V from Gibbons-Hawking centers
            v_potential = 0.15
            for c_x, c_y, q in centers:
                d_c = math.sqrt((x - c_x)**2 + (y - c_y)**2) + 8.0
                v_potential += q * 18.0 / d_c

            # Fractionated string interference wave
            # High-order winding phases: N1 * N5 ~ 512
            theta = math.atan2(ny, nx)
            string_phase = math.sin(16.0 * theta + dist / 8.0) * math.cos(24.0 * theta - dist / 12.0)
            
            # Surface bubbling boundary
            surface_mod = 1.0 + 0.12 * math.sin(8.0 * theta) + 0.08 * math.cos(14.0 * theta)
            eff_rfuzz = r_fuzz * surface_mod

            if dist < eff_rfuzz:
                # Interior: dense quantum fuzzball of vibrating strings and bubbles
                norm_d = dist / eff_rfuzz
                intensity = (v_potential * 0.45 + string_phase * 0.25 + (1.0 - norm_d) * 0.4)
                
                # Palette: deep cosmic violet to glowing cyan and incandescent core
                r_val = int(min(255, max(0, 160 * intensity * (1.0 - 0.4 * norm_d) + 30)))
                g_val = int(min(255, max(0, 210 * intensity * norm_d + 20)))
                b_val = int(min(255, max(0, 255 * intensity + 45)))
            else:
                # Exterior: Hawking radiation emanating from the vibrating surface
                d_ext = dist - eff_rfuzz
                ext_glow = math.exp(-d_ext / 55.0) * (0.8 + 0.2 * string_phase)
                r_val = int(min(255, max(0, 240 * ext_glow * 0.7)))
                g_val = int(min(255, max(0, 150 * ext_glow * 0.5)))
                b_val = int(min(255, max(0, 255 * ext_glow * 0.9)))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    out_png = os.path.join(os.path.dirname(__file__), "study_035_draft_b_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[STUDY-035-B] Plate Generated: {out_png}")

def synthesize_draft_b_audio():
    duration = 15.0
    total_samples = int(duration * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Acoustic parameters from Tier 24 telemetry:
    f0 = 55.0         # Base A1 fundamental
    f_frac = 57.43     # Fractionated string mode (beating delta = 2.43 Hz)
    f_mom = 269.44     # Momentum harmonic
    f_bub = 82.50      # Bubbling cycle mode

    p_f0 = 0.0
    p_frac = 0.0
    p_mom = 0.0
    p_bub = 0.0

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)
        # Envelope: 1.5s fade-in, 2.0s fade-out
        env = min(1.0, t / 1.5) * min(1.0, (duration - t) / 2.0)

        # Update phases
        p_f0 += 2.0 * math.pi * f0 / SAMPLE_RATE
        p_frac += 2.0 * math.pi * f_frac / SAMPLE_RATE
        p_mom += 2.0 * math.pi * f_mom / SAMPLE_RATE
        p_bub += 2.0 * math.pi * f_bub / SAMPLE_RATE

        # Microstate interference
        drone = (math.sin(p_f0) * 0.55 + math.sin(p_frac) * 0.45) # 2.43 Hz acoustic beating
        bubble = math.sin(p_bub + 0.3 * math.sin(p_f0)) * 0.25
        mom = math.sin(p_mom) * 0.12 * (0.5 + 0.5 * math.sin(t * 1.5))

        sig_l = (drone * 0.7 + bubble * 0.5 + mom * 0.6) * env * 0.88
        sig_r = (drone * 0.65 + bubble * 0.55 - mom * 0.5) * env * 0.88

        left[i] = max(-1.0, min(1.0, sig_l))
        right[i] = max(-1.0, min(1.0, sig_r))

    out_wav = os.path.join(os.path.dirname(__file__), "study_035_draft_b_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[STUDY-035-B] Audio Generated: {out_wav}")

if __name__ == "__main__":
    render_draft_b()
    synthesize_draft_b_audio()

