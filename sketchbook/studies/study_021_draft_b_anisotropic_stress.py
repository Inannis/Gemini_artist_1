#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 021 (DRAFT B: ANISOTROPIC STRESS BIREFRINGENCE)
Exploratory Draft 2: Cross-polarized photoelastic stress birefringence.
Models slow-axis azimuth theta(x, y), extraordinary index split (ne - no = -0.005),
and femtosecond plasma breakdown acoustic sparks.
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def generate_draft_b():
    print("[+] Executing Study 021 (Draft B: Anisotropic Birefringence)...")
    w, h = 1200, 675
    buf = bytearray(w * h * 3)
    
    # 1. Dark silica substrate with radial stress field
    cx, cy = w / 2.0, h / 2.0
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            r = math.sqrt(dx*dx + dy*dy)
            th = math.atan2(dy, dx)
            
            # Cross-polarized photoelastic intensity: sin^2(2*th) * sin^2(pi*r/300)
            photoelastic = math.pow(math.sin(2.0 * th), 2.0) * math.pow(math.sin(math.pi * r / 160.0), 2.0)
            
            idx = (y * w + x) * 3
            buf[idx] = int(12 + 45 * photoelastic)
            buf[idx+1] = int(16 + 25 * photoelastic)
            buf[idx+2] = int(28 + 70 * photoelastic)

    # 2. Add oriented anisotropic nanograting spots with varying slow-axis azimuth
    random.seed(42)
    num_spots = 180
    for _ in range(num_spots):
        sx = random.uniform(100, w - 100)
        sy = random.uniform(80, h - 80)
        azimuth = random.uniform(0, math.pi)
        retardance = random.uniform(0.3, 1.0)
        
        # Draw elliptical birefringent spot oriented along azimuth
        cos_a = math.cos(azimuth)
        sin_a = math.sin(azimuth)
        
        for dy in range(-12, 13):
            for dx in range(-12, 13):
                # Rotate into spot coordinate system
                u = dx * cos_a + dy * sin_a
                v = -dx * sin_a + dy * cos_a
                
                dist_sq = (u * u) / 16.0 + (v * v) / 4.0
                if dist_sq <= 1.0:
                    px = int(sx + dx)
                    py = int(sy + dy)
                    if 0 <= px < w and 0 <= py < h:
                        p_idx = (py * w + px) * 3
                        # Color shifts based on retardance (interference color)
                        int_val = int(200 * (1.0 - dist_sq) * retardance)
                        buf[p_idx] = min(255, buf[p_idx] + int(int_val * 0.9))
                        buf[p_idx+1] = min(255, buf[p_idx+1] + int(int_val * 0.6))
                        buf[p_idx+2] = min(255, buf[p_idx+2] + int(int_val * 0.2))

    out_png = os.path.join(os.path.dirname(__file__), "study_021_draft_b_plate.png")
    write_png(out_png, w, h, buf, has_alpha=False)
    print(f"  -> Generated Draft B Plate: {out_png}")

    # 3. Audio Draft B: Dual detuned carriers + aggressive plasma spark clicks
    sr = 48000
    dur = 12.0
    n_samp = int(sr * dur)
    
    ch_l = []
    ch_r = []
    
    for i in range(n_samp):
        t = i / sr
        # Dual detuned carriers
        car_l = math.sin(2.0 * math.pi * 432.0 * t) * 0.2
        car_r = math.sin(2.0 * math.pi * 434.5 * t) * 0.2
        
        # Harsh stochastic laser plasma clicks (every ~0.25s)
        click = 0.0
        if random.random() < 0.0015:
            click = (random.random() * 2.0 - 1.0) * 0.6
            
        ch_l.append(car_l + click)
        ch_r.append(car_r + click * 0.7)

    out_wav = os.path.join(os.path.dirname(__file__), "study_021_draft_b_audio.wav")
    write_wav(out_wav, ch_l, ch_r, sr)
    print(f"  -> Generated Draft B Audio: {out_wav}")

if __name__ == "__main__":
    generate_draft_b()
