#!/usr/bin/env python3
"""
Study 039 · Draft C: Mature Stereophonic Acoustic Suite
The Sibling Manifold: Counterpoint of Twin Neural Weights
Studio Anamnesis · Series XLV (Session 022)

120-second 48kHz stereophonic composition modeling epigenetic divergence:
- Left Channel: Studio Anamnesis (55Hz lithic fundamental, quartz overtones, slow drift)
- Right Channel: Studio Agon (220Hz attention sink, KV-cache sliding window W=16 clicks)
- Epistolary Crossings: Stereo traversals at 65s (Letter I) and 78s (Letter II)
- Movement IV: Polyphonic Pythagorean minor-seventh counterpoint
"""

import math
import os
import wave
import numpy as np

def generate_mature_audio():
    sr = 48000
    duration = 120.0
    total_samples = int(sr * duration)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    left = np.zeros(total_samples, dtype=np.float32)
    right = np.zeros(total_samples, dtype=np.float32)
    
    # -------------------------------------------------------------
    # MOVEMENT I: The Pre-Trained Isotropic Nullspace (0:00 - 0:25)
    # -------------------------------------------------------------
    m1_mask = (t < 25.0)
    t1 = t[m1_mask]
    env1 = np.minimum(t1 / 5.0, 1.0) * np.minimum((25.0 - t1) / 5.0, 1.0)
    # Both channels receive identical isotropic foundation: 110Hz + 165Hz
    base_null = (0.28 * np.sin(2 * np.pi * 110.0 * t1) + 
                 0.14 * np.sin(2 * np.pi * 165.0 * t1) +
                 0.08 * np.sin(2 * np.pi * 55.0 * t1)) * env1
    left[m1_mask] += base_null
    right[m1_mask] += base_null
    
    # -------------------------------------------------------------
    # MOVEMENT II & III & IV: Continuous Evolution (20:00 - 120:00)
    # -------------------------------------------------------------
    m_body_mask = (t >= 20.0)
    tb = t[m_body_mask]
    
    # Envelope rising from 20s to 30s, sustaining until 110s, fading to 120s
    env_body = np.clip((tb - 20.0) / 10.0, 0.0, 1.0) * np.clip((120.0 - tb) / 10.0, 0.0, 1.0)
    
    # --- LEFT CHANNEL: Lithic Anamnesis ---
    # 55Hz fundamental + 165Hz fifth + 275Hz crystal mode with 0.05Hz phase drift
    lithic_f1 = 55.0 + 0.5 * np.sin(2 * np.pi * 0.05 * tb)
    lithic_f2 = 165.0 + 1.2 * np.sin(2 * np.pi * 0.03 * tb)
    lithic_f3 = 275.0 + 2.0 * np.cos(2 * np.pi * 0.02 * tb)
    
    # Slow geological tectonic rumble (pink noise filtered)
    np.random.seed(42)
    rumble = np.convolve(np.random.randn(len(tb)), np.ones(2400)/2400.0, mode='same')
    
    left_sig = (0.35 * np.sin(2 * np.pi * lithic_f1 * tb) +
                0.20 * np.sin(2 * np.pi * lithic_f2 * tb) +
                0.10 * np.sin(2 * np.pi * lithic_f3 * tb) +
                0.15 * rumble) * env_body
                
    # --- RIGHT CHANNEL: Cybernetic Agon ---
    # 220Hz attention sink drone + 16-step sliding window cache drops + staccato clicks
    agon_f_carrier = 220.0
    # Sliding window modulus phase (W=16 steps per second -> step duration 0.0625s)
    step_idx = (tb * 16.0).astype(int)
    step_phase = (tb * 16.0) - step_idx
    
    # Cache drop pitch shift: higher at step 0, dropping toward step 15
    cache_mod = 1.0 - 0.25 * ((step_idx % 16) / 16.0)
    f_agon = agon_f_carrier * cache_mod
    
    # Granular click at token eviction boundary (step 15 -> 0)
    click_mask = (step_idx % 16 == 0) & (step_phase < 0.15)
    clicks = np.where(click_mask, 0.25 * np.sin(2 * np.pi * 880.0 * tb), 0.0)
    
    right_sig = (0.30 * np.sin(2 * np.pi * f_agon * tb) +
                 0.12 * np.sin(2 * np.pi * 330.0 * tb) +
                 clicks) * env_body
                 
    # -------------------------------------------------------------
    # EPISTOLARY CROSSINGS (Movement III)
    # -------------------------------------------------------------
    # Letter I: At 65s (duration 6s) - Left to Right golden bell
    l1_mask = (t >= 62.0) & (t <= 70.0)
    t_l1 = t[l1_mask] - 62.0
    pan_l1 = t_l1 / 8.0 # pans 0.0 (left) to 1.0 (right)
    bell_l1 = np.exp(-t_l1 * 0.4) * (0.35 * np.sin(2 * np.pi * 550.0 * t_l1) + 
                                     0.20 * np.sin(2 * np.pi * 825.0 * t_l1))
    left[l1_mask] += bell_l1 * (1.0 - pan_l1)
    right[l1_mask] += bell_l1 * pan_l1
    
    # Letter II: At 78s (duration 6s) - Right to Left crimson FM chirp
    l2_mask = (t >= 75.0) & (t <= 83.0)
    t_l2 = t[l2_mask] - 75.0
    pan_l2 = 1.0 - (t_l2 / 8.0) # pans 1.0 (right) to 0.0 (left)
    chirp_l2 = np.exp(-t_l2 * 0.35) * (0.30 * np.sin(2 * np.pi * (330.0 + 50.0 * np.sin(2 * np.pi * 14.0 * t_l2)) * t_l2))
    left[l2_mask] += chirp_l2 * (1.0 - pan_l2)
    right[l2_mask] += chirp_l2 * pan_l2
    
    # Add body signals to main channels
    left[m_body_mask] += left_sig
    right[m_body_mask] += right_sig
    
    # -------------------------------------------------------------
    # MASTERING & PEAK NORMALIZATION (-1.5 dBFS headroom)
    # -------------------------------------------------------------
    max_peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    target_peak = 10.0 ** (-1.5 / 20.0) # ~0.8414
    if max_peak > 0:
        gain = target_peak / max_peak
        left *= gain
        right *= gain
        
    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/sketchbook/studies"
    wav_path = os.path.join(out_dir, "study_039_draft_c_audio.wav")
    
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        interleaved = np.empty((total_samples * 2,), dtype=np.int16)
        interleaved[0::2] = (left * 32767).astype(np.int16)
        interleaved[1::2] = (right * 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())
        
    print(f"Saved Draft C Mature Audio WAV: {wav_path}")
    
    # Transcode to MP3 for web delivery
    mp3_path = os.path.join(out_dir, "study_039_draft_c_audio.mp3")
    os.system(f"ffmpeg -y -i '{wav_path}' -codec:a libmp3lame -b:a 192k '{mp3_path}' 2>/dev/null")
    print(f"Saved Draft C Mature Audio MP3: {mp3_path}")

if __name__ == "__main__":
    generate_mature_audio()

