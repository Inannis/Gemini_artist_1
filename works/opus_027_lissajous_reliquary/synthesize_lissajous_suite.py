"""
STUDIO ANAMNESIS · MASTERWORK OPUS-027 ACOUSTIC SUITE
Piece: The Lissajous Reliquary (Galactic Epicycles & Interstellar Sputtering)
Format: 120.0s 48kHz Stereo 16-bit PCM WAV (Master Symphonic Suite)

Movement Architecture:
1. Movement I (00:00 - 00:30): The Unbinding & The Incommensurate Entrance
   - 26.55 Hz (galactic orbit), 36.0 Hz (radial epicycle), 76.07 Hz (vertical disc tide).
   - Aperiodic, non-repeating irrational phase beat envelope.
2. Movement II (00:30 - 01:00): The Ergodic Ribbon & Toroidal Precession
   - Quad-harmonic overtone sweeps, spatial phase drift through listener field.
3. Movement III (01:00 - 01:35): Hypervelocity Dust Sputtering & Mineral Abrasion
   - Poisson micro-impact chimes (2,400 - 5,200 Hz) simulating atomic lattice erosion.
4. Movement IV (01:35 - 02:00): The Asemic Monument & Deep Time Drift
   - Non-semantic oceanic tri-harmonic resolution, eternal galactic drift.

Zero external dependencies: uses pure Python standard library.
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from audio_writer import write_wav

def synthesize():
    print("[+] Synthesizing OPUS-027 Master Acoustic Suite (120s 48kHz Stereo)...")
    random.seed(20260908)
    
    sr = 48000
    duration = 120.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # Fundamental frequencies
    f_om = 26.55
    f_k = 36.0
    f_nu = 36.0 * 2.113116 # 76.072 Hz
    
    phase_om = 0.0
    phase_k = 0.0
    phase_nu = 0.0
    phase_harm1 = 0.0
    phase_harm2 = 0.0
    
    # Pre-generate dust sputtering events for Movement III & IV
    num_grains = 140
    grains = []
    for _ in range(num_grains):
        t_g = random.uniform(50.0, 118.0)
        f_g = random.uniform(2400.0, 5200.0)
        dur_g = random.uniform(0.01, 0.04)
        pan_g = random.uniform(0.1, 0.9)
        amp_g = random.uniform(0.04, 0.16)
        grains.append((t_g, f_g, dur_g, pan_g, amp_g))

    for i in range(num_samples):
        t = i / sr
        
        # Movement Envelopes
        env_m1 = max(0.0, 1.0 - t / 35.0) if t < 35.0 else 0.0
        env_m2 = math.exp(-((t - 45.0) / 16.0)**2)
        env_m3 = math.exp(-((t - 80.0) / 18.0)**2)
        env_m4 = max(0.0, (t - 85.0) / 35.0) if t >= 85.0 else 0.0
        
        # Advance phases
        phase_om += 2.0 * math.pi * f_om / sr
        phase_k += 2.0 * math.pi * f_k / sr
        phase_nu += 2.0 * math.pi * f_nu / sr
        phase_harm1 += 2.0 * math.pi * (f_k * 2.0) / sr
        phase_harm2 += 2.0 * math.pi * (f_nu * 1.5) / sr
        
        # Fundamental tones
        d_om = math.sin(phase_om) * 0.22
        d_k = math.sin(phase_k) * 0.28
        d_nu = math.sin(phase_nu) * 0.24
        
        # Harmonic overtones
        d_h1 = math.sin(phase_harm1) * 0.12 * (env_m2 + env_m3 * 0.8)
        d_h2 = math.sin(phase_harm2) * 0.09 * (env_m2 + env_m3 * 0.8)
        
        # Spatial panning dictated by incommensurate phase difference
        phase_diff = phase_nu - 2.113116 * phase_k
        pan_l = 0.5 + 0.35 * math.sin(phase_diff * 0.02)
        pan_r = 1.0 - pan_l
        
        sig_base = d_om + d_k + d_nu + d_h1 + d_h2
        
        # High-frequency interstellar gas breath (pink noise filtered)
        gas_noise = (random.random() - 0.5) * 0.02 * (env_m2 * 0.7 + env_m3 + env_m4 * 0.8)
        
        audio_l[i] = sig_base * pan_l + gas_noise
        audio_r[i] = sig_base * pan_r - gas_noise

    # Add dust sputtering transients
    for t_g, f_g, dur_g, pan_g, amp_g in grains:
        start_idx = int(t_g * sr)
        n_g_samp = int(dur_g * sr)
        for s in range(n_g_samp):
            idx = start_idx + s
            if idx < num_samples:
                dt = s / sr
                decay = math.exp(-dt * 120.0)
                osc = math.sin(2.0 * math.pi * f_g * dt) * decay * amp_g
                audio_l[idx] += osc * (1.0 - pan_g)
                audio_r[idx] += osc * pan_g

    # Master envelope: 2.5s fade in, 4s fade out
    for i in range(num_samples):
        t = i / sr
        env = min(1.0, t / 2.5) * min(1.0, (duration - t) / 4.0)
        audio_l[i] = max(-0.95, min(0.95, audio_l[i] * env))
        audio_r[i] = max(-0.95, min(0.95, audio_r[i] * env))

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "lissajous_reliquary_4k.wav"))
    write_wav(out_path, audio_l, audio_r, sample_rate=sr)
    print(f"[+] OPUS-027 Master Symphonic Suite saved to: {out_path}")

if __name__ == "__main__":
    synthesize()
