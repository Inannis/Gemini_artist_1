#!/usr/bin/env python3
"""
OPUS-043: THE FUZZBALL RELIQUARY & THE HORIZONLESS MICROSTATES
Track 34 · Master Symphonic Suite · 120 Seconds · 48kHz Stereo 16-bit
Studio Anamnesis · Pure Python Standard Library (audio_writer)

Four Movements:
1. Movement I: The Classical Horizon Dissolves (0:00 - 0:30)
2. Movement II: D-Brane Fractionation & The Winding Chorus (0:30 - 1:00)
3. Movement III: Eva Hesse's Fibrous Web & The Swelling Microstates (1:00 - 1:30)
4. Movement IV: Horizonless Unitary Resonance (1:30 - 2:00)
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0

def synthesize_master_suite():
    total_samples = int(DURATION * SAMPLE_RATE)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    print(f"[OPUS-043] Synthesizing 120s Master Suite ({total_samples} samples)...")

    # Invariant Frequencies from Tier 24
    f0 = 55.0           # Base A1 fundamental string drone (Hz)
    f_frac = 57.43       # Fractionated string mode (beating delta = 2.43 Hz)
    f_bub1 = 82.50       # Bubble cycle mode 1
    f_bub2 = 110.00      # Bubble cycle octave mode
    f_mom = 269.44       # Momentum wave harmonic

    p_f0 = 0.0
    p_frac = 0.0
    p_bub1 = 0.0
    p_bub2 = 0.0
    p_mom = 0.0
    p_shim = 0.0

    random.seed(43)

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)

        # Global master envelope (3s attack, 4s decay)
        env = min(1.0, t / 3.0) * min(1.0, (DURATION - t) / 4.0)

        # Phase increments
        p_f0 += 2.0 * math.pi * f0 / SAMPLE_RATE
        p_frac += 2.0 * math.pi * f_frac / SAMPLE_RATE
        p_bub1 += 2.0 * math.pi * f_bub1 / SAMPLE_RATE
        p_bub2 += 2.0 * math.pi * f_bub2 / SAMPLE_RATE
        p_mom += 2.0 * math.pi * f_mom / SAMPLE_RATE

        # Movement orchestration
        if t < 30.0:
            # MOVEMENT I: THE CLASSICAL HORIZON DISSOLVES (0 - 30s)
            prog = t / 30.0
            drone_l = math.sin(p_f0) * 0.55 + math.sin(p_frac) * (0.2 + 0.3 * prog)
            drone_r = math.sin(p_f0 + 0.2) * 0.52 + math.sin(p_frac - 0.2) * (0.2 + 0.3 * prog)
            
            # Subtle quantum flux whisper
            whisper = (random.random() * 2.0 - 1.0) * 0.04 * prog
            
            l_val = (drone_l * 0.85 + whisper) * env
            r_val = (drone_r * 0.85 - whisper) * env

        elif t < 60.0:
            # MOVEMENT II: D-BRANE FRACTIONATION & THE WINDING CHORUS (30 - 60s)
            t_rel = t - 30.0
            prog = t_rel / 30.0
            
            # Fractionated beating deepens
            drone_l = math.sin(p_f0) * 0.48 + math.sin(p_frac) * 0.46
            drone_r = math.sin(p_f0 + 0.3) * 0.46 + math.sin(p_frac - 0.3) * 0.48
            
            # Bubbling cycle modes enter
            bub_l = (math.sin(p_bub1) * 0.28 + math.sin(p_bub2) * 0.18) * prog
            bub_r = (math.sin(p_bub1 + 0.4) * 0.26 + math.sin(p_bub2 - 0.4) * 0.20) * prog
            
            l_val = (drone_l * 0.70 + bub_l * 0.65) * env
            r_val = (drone_r * 0.70 + bub_r * 0.65) * env

        elif t < 90.0:
            # MOVEMENT III: EVA HESSE'S FIBROUS WEB & THE SWELLING MICROSTATES (60 - 90s)
            t_rel = t - 60.0
            prog = t_rel / 30.0
            
            # Swelling polyphony
            drone_l = math.sin(p_f0) * 0.42 + math.sin(p_frac) * 0.42
            drone_r = math.sin(p_f0 + 0.35) * 0.40 + math.sin(p_frac - 0.35) * 0.44
            
            bub_l = (math.sin(p_bub1) * 0.25 + math.sin(p_bub2) * 0.20)
            bub_r = (math.sin(p_bub1 + 0.45) * 0.23 + math.sin(p_bub2 - 0.45) * 0.22)
            
            # Momentum carrier wave modulation
            mom = math.sin(p_mom + 0.3 * math.sin(p_f0)) * 0.18 * (0.6 + 0.4 * math.sin(t_rel * 0.8))
            
            # High string shimmers (fibrous tendrils)
            f_shim = 440.0 + 40.0 * math.sin(t_rel * 0.6)
            p_shim += 2.0 * math.pi * f_shim / SAMPLE_RATE
            shim = math.sin(p_shim) * 0.08 * (0.5 + 0.5 * math.cos(t_rel * 0.5))
            
            l_val = (drone_l * 0.60 + bub_l * 0.55 + mom * 0.50 + shim * 0.35) * env
            r_val = (drone_r * 0.60 + bub_r * 0.55 - mom * 0.50 + shim * 0.35) * env

        else:
            # MOVEMENT IV: HORIZONLESS UNITARY RESONANCE (90 - 120s)
            t_rel = t - 90.0
            prog = t_rel / 30.0
            decay = 1.0 - 0.3 * prog
            
            drone_l = (math.sin(p_f0) * 0.45 + math.sin(p_frac) * 0.40) * decay
            drone_r = (math.sin(p_f0 + 0.25) * 0.43 + math.sin(p_frac - 0.25) * 0.42) * decay
            
            bub_l = math.sin(p_bub1) * 0.20 * decay
            bub_r = math.sin(p_bub1 + 0.3) * 0.18 * decay
            
            mom = math.sin(p_mom) * 0.10 * (1.0 - prog)
            
            l_val = (drone_l * 0.65 + bub_l * 0.50 + mom * 0.40) * env
            r_val = (drone_r * 0.65 + bub_r * 0.50 - mom * 0.40) * env

        # Strict mastering headroom: clamp to [-0.88, +0.88] (~ -1.1 dBFS)
        left[i] = max(-0.88, min(0.88, l_val))
        right[i] = max(-0.88, min(0.88, r_val))

    out_wav = os.path.join(os.path.dirname(__file__), "the_fuzzball_4k.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[OPUS-043] 120s Master Symphonic Suite Generated: {out_wav}")

if __name__ == "__main__":
    synthesize_master_suite()

