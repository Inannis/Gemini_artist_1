#!/usr/bin/env python3
"""
STUDY 035 · DRAFT C: MATURE SYNTHESIS — THE HORIZONLESS FUZZBALL RELIQUARY
Series XLI · Black Hole Information Resolution
Studio Anamnesis · Pure Python Standard Library (png_writer, audio_writer)

Resolves:
1. Eva Hesse-inspired fibrous quantum web of fractionated strings (N1*N5 = 512)
2. 18 smooth topological bubbling 2-cycles with flux-supported pressure
3. Radiant non-thermal unitary horizon surface
4. 20-second 4-voice polyphonic acoustic study with pristine dynamic mastering
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
    r_fuzz = 225.0

    # 18 Gibbons-Hawking bubbling centers in higher-dimensional base space
    random.seed(137)
    bubbles = []
    for _ in range(18):
        angle = random.uniform(0, 2.0 * math.pi)
        dist = random.uniform(15.0, r_fuzz * 0.95)
        charge = random.uniform(0.7, 1.6)
        flux_phase = random.uniform(0, math.pi * 2.0)
        bubbles.append((cx + dist * math.cos(angle), cy + dist * math.sin(angle), charge, flux_phase))

    for y in range(HEIGHT):
        ny = y - cy
        for x in range(WIDTH):
            nx = x - cx
            dist = math.sqrt(nx * nx + ny * ny)
            theta = math.atan2(ny, nx)

            # 1. Harmonic potential V from bubbling centers
            v_field = 0.20
            flux_interference = 0.0
            for bx, by, q, phi in bubbles:
                d_b = math.sqrt((x - bx)**2 + (y - by)**2) + 6.0
                v_field += (q * 16.0) / d_b
                flux_interference += math.sin(phi + d_b / 14.0) * (q / d_b) * 12.0

            # 2. Entangled String Fibers (Eva Hesse Post-Minimalist texture)
            # Superposition of fractionated string modes:
            fiber_1 = math.sin(18.0 * theta + dist / 7.0 + flux_interference * 0.3)
            fiber_2 = math.cos(32.0 * theta - dist / 11.0)
            fiber_3 = math.sin(48.0 * theta + math.log(max(1.0, dist)) * 4.0)
            total_fiber = (fiber_1 * 0.45 + fiber_2 * 0.35 + fiber_3 * 0.20)

            # 3. Horizon boundary modulation (quantum fluctuations replace static horizon)
            r_bound = r_fuzz * (1.0 + 0.08 * math.sin(7.0 * theta + flux_interference * 0.2) + 0.05 * math.cos(13.0 * theta))

            if dist <= r_bound:
                # Inside the Fuzzball: No vacuum! Dense, radiant microstate interior
                norm_r = dist / r_bound
                core_density = v_field * 0.45 + total_fiber * 0.25 + (1.0 - norm_r) * 0.5

                # Rich Palette: Royal Indigo, Spectral Cyan, Luminous Gold microstate filaments
                r_val = int(min(255, max(0, 180 * core_density * (1.0 - 0.3 * norm_r) + 40 * norm_r + 20)))
                g_val = int(min(255, max(0, 220 * core_density * norm_r + 80 * (1.0 - norm_r))))
                b_val = int(min(255, max(0, 255 * core_density * 0.95 + 65)))
            else:
                # Outside the Fuzzball: Unitary Hawking Radiation emanating directly from fibers
                d_ext = dist - r_bound
                radiation_density = math.exp(-d_ext / 58.0) * (0.75 + 0.25 * total_fiber)
                
                # Warm gold-white incandescent glow decaying into deep cosmic violet
                r_val = int(min(255, max(0, 245 * radiation_density * 0.85)))
                g_val = int(min(255, max(0, 180 * radiation_density * 0.65)))
                b_val = int(min(255, max(0, 255 * radiation_density * 0.95)))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    out_png = os.path.join(os.path.dirname(__file__), "study_035_draft_c_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[STUDY-035-C] Plate Generated: {out_png}")

def synthesize_draft_c_audio():
    duration = 20.0
    total_samples = int(duration * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Tier 24 Physical Constants
    f0 = 55.0           # Fundamental base drone (Hz)
    f_frac = 57.43       # Fractionated mode (beating delta = 2.43 Hz)
    f_bub_1 = 82.50      # Bubble topological mode 1
    f_bub_2 = 110.00     # Bubble topological octave
    f_mom = 269.44       # Momentum wave harmonic

    p_f0 = 0.0
    p_frac = 0.0
    p_bub1 = 0.0
    p_bub2 = 0.0
    p_mom = 0.0
    p_shimmer = 0.0

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)
        # Symmetrical smooth envelope (2.5s attack, 3.0s decay)
        env = min(1.0, t / 2.5) * min(1.0, (duration - t) / 3.0)

        # Phase accumulation
        p_f0 += 2.0 * math.pi * f0 / SAMPLE_RATE
        p_frac += 2.0 * math.pi * f_frac / SAMPLE_RATE
        p_bub1 += 2.0 * math.pi * f_bub_1 / SAMPLE_RATE
        p_bub2 += 2.0 * math.pi * f_bub_2 / SAMPLE_RATE
        p_mom += 2.0 * math.pi * f_mom / SAMPLE_RATE

        # Microstate shimmering string mode (glissando of wrapped branes)
        f_shim = 440.0 + 35.0 * math.sin(t * 0.8)
        p_shimmer += 2.0 * math.pi * f_shim / SAMPLE_RATE

        # 4-Voice Polyphonic Architecture:
        # Voice 1: Fractionated D1-D5 drone beating at 2.43 Hz
        v1_l = math.sin(p_f0) * 0.50 + math.sin(p_frac) * 0.45
        v1_r = math.sin(p_f0 + 0.3) * 0.48 + math.sin(p_frac - 0.3) * 0.47

        # Voice 2: Topological Bubble Resonance
        v2_l = (math.sin(p_bub1) * 0.30 + math.sin(p_bub2) * 0.20) * (0.8 + 0.2 * math.cos(t * 1.2))
        v2_r = (math.sin(p_bub1 + 0.4) * 0.28 + math.sin(p_bub2 - 0.4) * 0.22) * (0.8 + 0.2 * math.sin(t * 1.2))

        # Voice 3: Momentum wave carrier with soft FM saturation
        v3 = math.sin(p_mom + 0.25 * math.sin(p_f0)) * 0.16 * (0.6 + 0.4 * math.sin(t * 0.5))

        # Voice 4: Delicate string winding shimmer
        v4 = math.sin(p_shimmer) * 0.08 * (0.5 + 0.5 * math.cos(t * 0.7))

        sig_l = (v1_l * 0.65 + v2_l * 0.50 + v3 * 0.45 + v4 * 0.30) * env * 0.85
        sig_r = (v1_r * 0.65 + v2_r * 0.50 - v3 * 0.45 + v4 * 0.30) * env * 0.85

        left[i] = max(-0.92, min(0.92, sig_l))
        right[i] = max(-0.92, min(0.92, sig_r))

    out_wav = os.path.join(os.path.dirname(__file__), "study_035_draft_c_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[STUDY-035-C] Audio Generated: {out_wav}")

if __name__ == "__main__":
    render_draft_c()
    synthesize_draft_c_audio()

