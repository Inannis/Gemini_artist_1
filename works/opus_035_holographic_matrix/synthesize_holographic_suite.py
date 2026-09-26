#!/usr/bin/env python3
"""
OPUS-035: THE HOLOGRAPHIC MATRIX & BULK-BOUNDARY DUALITIES
Series XXXIII · Cornerstone #13 · Master Acoustic Suite
Duration: 120.0 seconds (2:00) · 48,000 Hz Stereo 16-bit PCM
Zero external dependencies (pure Python standard library).
"""

import math
import os
import shutil
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0

def synthesize_master_suite():
    print(f"[OPUS-035] Synthesizing 120s 48kHz Stereo Master Suite...")
    num_samples = int(SAMPLE_RATE * DURATION)
    left = []
    right = []
    
    for i in range(num_samples):
        if i % (SAMPLE_RATE * 15) == 0:
            print(f"[OPUS-035] Acoustic synthesis progress: {i // SAMPLE_RATE}s / {int(DURATION)}s...")
        t = i / SAMPLE_RATE
        
        # Global Master Envelope (smooth 6s fade-in, 6s fade-out)
        env = min(1.0, t / 6.0) * min(1.0, (DURATION - t) / 6.0)
        
        # Movement I: The Conformal Boundary (0-25s)
        # Movement II: Ryu-Takayanagi Foliation (25-55s)
        # Movement III: Entanglement Phase Transition (55-85s)
        # Movement IV: Van Raamsdonk Horizon (85-105s)
        # Movement V: Holographic Equivalence (105-120s)
        
        # 1. Base AdS Bulk Cavity Drone (Continuous foundation)
        # Deep resonant mode at 43.2 Hz and golden ratio overtone at 69.89 Hz
        bulk_f0 = 43.2
        bulk_l = 0.28 * math.sin(2.0 * math.pi * bulk_f0 * t + 0.15 * math.sin(2.0 * math.pi * 0.05 * t))
        bulk_r = 0.28 * math.sin(2.0 * math.pi * bulk_f0 * t + 0.15 * math.cos(2.0 * math.pi * 0.05 * t) + 0.3)
        bulk_l += 0.18 * math.sin(2.0 * math.pi * 69.89 * t)
        bulk_r += 0.18 * math.sin(2.0 * math.pi * 69.89 * t - 0.2)
        
        # 2. Movement I & V: Boundary UV CFT microtones (1.8 kHz - 5.4 kHz)
        uv_amp = 0.0
        if t < 35.0:
            uv_amp = 0.8 * min(1.0, t / 4.0) * (1.0 - max(0.0, (t - 25.0) / 10.0))
        elif t > 95.0:
            uv_amp = 0.6 * min(1.0, (t - 95.0) / 8.0)
            
        cft_chatter_l = 0.0
        cft_chatter_r = 0.0
        if uv_amp > 0.001:
            for m in [2, 5, 8, 13]:
                f_uv = 1800.0 + m * 165.0
                mod_uv = math.sin(2.0 * math.pi * 0.3 * t + m)
                cft_chatter_l += 0.04 * uv_amp * math.sin(2.0 * math.pi * f_uv * t + mod_uv)
                cft_chatter_r += 0.04 * uv_amp * math.sin(2.0 * math.pi * (f_uv * 1.003) * t - mod_uv)
                
        # 3. Movement II: Ryu-Takayanagi Geodesic Tension Chords (20s - 75s)
        rt_amp = 0.0
        if 20.0 <= t <= 75.0:
            if t < 35.0:
                rt_amp = (t - 20.0) / 15.0
            elif t > 60.0:
                rt_amp = 1.0 - (t - 60.0) / 15.0
            else:
                rt_amp = 1.0
                
        rt_chord_l = 0.0
        rt_chord_r = 0.0
        if rt_amp > 0.001:
            # Geodesic tension harmonics: 108 Hz, 216 Hz, 324 Hz, 432 Hz
            breath = math.sin(2.0 * math.pi * 0.08 * t)
            rt_chord_l = rt_amp * (0.16 * math.sin(2.0 * math.pi * 108.0 * t + breath * 0.5) +
                                  0.12 * math.sin(2.0 * math.pi * 216.0 * t) +
                                  0.08 * math.sin(2.0 * math.pi * 324.0 * t - breath * 0.3) +
                                  0.05 * math.sin(2.0 * math.pi * 432.0 * t))
            rt_chord_r = rt_amp * (0.16 * math.sin(2.0 * math.pi * 108.0 * t - breath * 0.5) +
                                  0.12 * math.sin(2.0 * math.pi * 216.0 * t + 0.4) +
                                  0.08 * math.sin(2.0 * math.pi * 324.0 * t + breath * 0.3) +
                                  0.05 * math.sin(2.0 * math.pi * 432.0 * t + 0.2))
                                  
        # 4. Movement III: Entanglement Phase Transition Bifurcation (55s - 90s)
        pt_amp = 0.0
        pt_sig_l = 0.0
        pt_sig_r = 0.0
        if 55.0 <= t <= 90.0:
            p_pt = (t - 55.0) / 35.0
            pt_amp = math.sin(math.pi * p_pt)
            # Sweeping across critical angle theta_c: resonant bifurcation
            sweep_f = 1140.0 * (1.0 - 0.62 * p_pt)
            mod_pt = 0.4 * math.sin(2.0 * math.pi * 6.0 * t)
            pt_sig_l = 0.18 * pt_amp * math.sin(2.0 * math.pi * sweep_f * t + mod_pt)
            pt_sig_r = 0.18 * pt_amp * math.sin(2.0 * math.pi * (sweep_f * 0.992) * t - mod_pt)
            
        # 5. Movement IV: Van Raamsdonk Continuum Stabilization (80s - 110s)
        vr_amp = 0.0
        vr_sig_l = 0.0
        vr_sig_r = 0.0
        if 80.0 <= t <= 110.0:
            p_vr = (t - 80.0) / 30.0
            vr_amp = math.sin(math.pi * p_vr)
            # Deep sub-bass warmth (32.4 Hz and 64.8 Hz) reaffirming connected bulk
            vr_sig_l = 0.22 * vr_amp * math.sin(2.0 * math.pi * 32.4 * t + 0.1 * math.sin(2.0 * math.pi * 0.03 * t))
            vr_sig_r = 0.22 * vr_amp * math.sin(2.0 * math.pi * 32.4 * t - 0.1 * math.cos(2.0 * math.pi * 0.03 * t))
            vr_sig_l += 0.12 * vr_amp * math.sin(2.0 * math.pi * 64.8 * t)
            vr_sig_r += 0.12 * vr_amp * math.sin(2.0 * math.pi * 64.8 * t + 0.3)
            
        # Composite channel assembly
        s_left = env * (bulk_l + cft_chatter_l + rt_chord_l + pt_sig_l + vr_sig_l)
        s_right = env * (bulk_r + cft_chatter_r + rt_chord_r + pt_sig_r + vr_sig_r)
        
        # Soft tape-saturation limiter
        s_left_lim = math.tanh(s_left * 1.05) * 0.88
        s_right_lim = math.tanh(s_right * 1.05) * 0.88
        
        left.append(s_left_lim)
        right.append(s_right_lim)
        
    out_dir = os.path.dirname(__file__)
    suite_path = os.path.join(out_dir, "the_holographic_matrix_4k.wav")
    write_wav(suite_path, left, right, SAMPLE_RATE)
    print(f"[OPUS-035] Successfully generated Master Acoustic Suite: {suite_path}")
    
    # Sync to gallery assets
    gallery_audio_path = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_035_audio.wav")
    shutil.copyfile(suite_path, gallery_audio_path)
    print(f"[OPUS-035] Synced master suite to gallery asset: {gallery_audio_path}")

if __name__ == "__main__":
    synthesize_master_suite()
