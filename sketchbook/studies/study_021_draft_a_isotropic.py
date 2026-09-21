#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 021 (DRAFT A: ISOTROPIC VOXEL GRID)
Exploratory Draft 1: Naive isotropic laser focal density in fused silica.
Tests pure geometric voxel lattices before introducing stress birefringence.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def generate_draft_a():
    print("[+] Executing Study 021 (Draft A: Isotropic Grid)...")
    w, h = 1200, 675
    buf = bytearray(w * h * 3)
    
    # 1. Background: Raw transparent fused silica (dark blue-gray)
    for y in range(h):
        for x in range(w):
            idx = (y * w + x) * 3
            buf[idx] = 8
            buf[idx+1] = 12
            buf[idx+2] = 20

    # 2. Draw rigid isotropic voxel grid (Draft A hypothesis: simple 2D pitch)
    pitch_x = 24
    pitch_y = 24
    
    for gy in range(40, h - 40, pitch_y):
        for gx in range(60, w - 60, pitch_x):
            # Naive uniform spots
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    r = math.sqrt(dx*dx + dy*dy)
                    if r <= 3.0:
                        px = gx + dx
                        py = gy + dy
                        if 0 <= px < w and 0 <= py < h:
                            p_idx = (py * w + px) * 3
                            intensity = int(180 * (1.0 - r / 3.0))
                            buf[p_idx] = min(255, buf[p_idx] + intensity // 2)
                            buf[p_idx+1] = min(255, buf[p_idx+1] + intensity)
                            buf[p_idx+2] = min(255, buf[p_idx+2] + intensity)

    out_png = os.path.join(os.path.dirname(__file__), "study_021_draft_a_plate.png")
    write_png(out_png, w, h, buf, has_alpha=False)
    print(f"  -> Generated Draft A Plate: {out_png}")

    # 3. Audio Draft A: High-pitched rigid sinusoidal tone (cold, uniform)
    sr = 48000
    dur = 12.0
    n_samp = int(sr * dur)
    freq0 = 1200.0 # High piercing tone
    
    ch_l = []
    ch_r = []
    for i in range(n_samp):
        t = i / sr
        # Rigid pure sine with minor 4Hz tremolo
        s = math.sin(2.0 * math.pi * freq0 * t) * 0.25 * (1.0 + 0.1 * math.sin(2.0 * math.pi * 4.0 * t))
        ch_l.append(s)
        ch_r.append(s)

    out_wav = os.path.join(os.path.dirname(__file__), "study_021_draft_a_audio.wav")
    write_wav(out_wav, ch_l, ch_r, sr)
    print(f"  -> Generated Draft A Audio: {out_wav}")

if __name__ == "__main__":
    generate_draft_a()
