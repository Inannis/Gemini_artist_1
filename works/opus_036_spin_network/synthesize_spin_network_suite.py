#!/usr/bin/env python3
"""
OPUS-036: THE QUANTUM GEOMETRY FOAM & THE SPIN NETWORK RELIQUARY
Cornerstone #14 · Series XXXIV: Quantum Gravity Foam & Spin Networks
Master Acoustic Suite · Duration: 120.0 seconds (2:00)
48,000 Hz Stereo 16-bit PCM · Pure Python standard library (zero external dependencies).
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0

def synthesize_master_suite():
    print(f"[OPUS-036] Synthesizing 120s 48kHz Stereo Master Suite...")
    num_samples = int(SAMPLE_RATE * DURATION)
    left = []
    right = []
    
    # Area ladder frequencies for j in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    # f_j = 86.4 * sqrt(j*(j+1))
    spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    area_freqs = [86.4 * math.sqrt(j * (j + 1.0)) for j in spins]
    # [74.82, 122.19, 167.31, 211.64, 255.57, 299.21]
    
    for i in range(num_samples):
        if i % (SAMPLE_RATE * 15) == 0:
            print(f"[OPUS-036] Acoustic synthesis progress: {i // SAMPLE_RATE}s / {int(DURATION)}s...")
        t = i / SAMPLE_RATE
        
        # Global Master Envelope (smooth 6s fade-in, 6s fade-out)
        env = min(1.0, t / 6.0) * min(1.0, (DURATION - t) / 6.0)
        
        # 1. Base Quantum Foam Cosmological Ground Drone (Continuous)
        # Deep resonant oscillation at 36.0 Hz and sub-harmonic 18.0 Hz
        drift = 0.12 * math.sin(2.0 * math.pi * 0.04 * t)
        drone_l = 0.26 * math.sin(2.0 * math.pi * (36.0 + drift) * t) + 0.14 * math.sin(2.0 * math.pi * 54.0 * t)
        drone_r = 0.26 * math.sin(2.0 * math.pi * (36.0 - drift) * t + 0.25) + 0.14 * math.sin(2.0 * math.pi * 54.0 * t - 0.2)
        # Infrasonic pressure pulse at 18.0 Hz
        drone_l += 0.10 * math.sin(2.0 * math.pi * 18.0 * t)
        drone_r += 0.10 * math.sin(2.0 * math.pi * 18.0 * t)
        
        # 2. Movement I & II: Area Spectrum Ladder Chords (15s - 75s and 100s - 120s)
        ladder_amp = 0.0
        if 15.0 <= t <= 75.0:
            if t < 30.0:
                ladder_amp = (t - 15.0) / 15.0
            elif t > 60.0:
                ladder_amp = 1.0 - (t - 60.0) / 15.0
            else:
                ladder_amp = 1.0
        elif t >= 98.0:
            ladder_amp = 0.7 * min(1.0, (t - 98.0) / 10.0)
            
        ladder_l = 0.0
        ladder_r = 0.0
        if ladder_amp > 0.001:
            for idx, f in enumerate(area_freqs):
                pan_phase = idx * 0.8
                breath = 0.5 + 0.5 * math.sin(2.0 * math.pi * (0.07 + idx * 0.015) * t)
                harmonic_w = (0.15 / math.sqrt(idx + 1.0)) * ladder_amp * breath
                ladder_l += harmonic_w * math.sin(2.0 * math.pi * f * t + pan_phase)
                ladder_r += harmonic_w * math.sin(2.0 * math.pi * (f * 1.0035) * t - pan_phase)
                
        # 3. Movement III: The Loop Quantum Bounce (50s - 88s)
        # Cosmic contraction halts at rho_crit, Hubble rate H -> 0, then bounces
        bounce_sig_l = 0.0
        bounce_sig_r = 0.0
        if 50.0 <= t <= 88.0:
            p_b = (t - 50.0) / 38.0
            b_env = math.sin(math.pi * p_b)
            # Deceleration and inversion
            h_rate = abs(math.cos(math.pi * p_b))
            f_bounce = 28.0 + 180.0 * (h_rate ** 1.5)
            # Seismic sub-bass sweep
            b_wave = math.sin(2.0 * math.pi * f_bounce * t)
            # Quantum geometry repulsion resonance
            repulsion = 0.22 * b_env * math.sin(2.0 * math.pi * 96.0 * t + 0.4 * math.sin(2.0 * math.pi * 3.5 * t))
            bounce_sig_l = b_env * (0.35 * b_wave + repulsion)
            bounce_sig_r = b_env * (0.35 * b_wave - repulsion)
            
        # 4. Movement IV: Intertwiner Volume Quanta & Puncture Grain (75s - 110s)
        intertwiner_l = 0.0
        intertwiner_r = 0.0
        if 72.0 <= t <= 112.0:
            p_int = (t - 72.0) / 40.0
            int_env = math.sin(math.pi * p_int)
            # Micro-punctures: high-frequency resonance rings (1440 Hz & 2880 Hz)
            pulse_mod = (t * 8.0) % 1.0
            if pulse_mod < 0.04:
                decay = math.exp(-pulse_mod * 80.0)
                ring_val = math.sin(2.0 * math.pi * 2160.0 * t) * decay * 0.25 * int_env
                if int(t * 8.0) % 2 == 0:
                    intertwiner_l += ring_val
                else:
                    intertwiner_r += ring_val
            # Delicate bell harmonic of spatial intertwiner
            bell = 0.08 * int_env * math.sin(2.0 * math.pi * 720.0 * t + 0.1 * math.sin(2.0 * math.pi * 0.2 * t))
            intertwiner_l += bell
            intertwiner_r += bell * 0.98
            
        # 5. Master Stereo Mix & Soft Limiter
        mix_l = env * (drone_l * 0.70 + ladder_l * 0.65 + bounce_sig_l * 0.75 + intertwiner_l * 0.50)
        mix_r = env * (drone_r * 0.70 + ladder_r * 0.65 + bounce_sig_r * 0.75 + intertwiner_r * 0.50)
        
        # Soft-knee saturation
        s_left = math.tanh(mix_l * 1.08)
        s_right = math.tanh(mix_r * 1.08)
        
        left.append(s_left)
        right.append(s_right)
        
    out_master = os.path.join(os.path.dirname(__file__), "the_spin_network_4k.wav")
    write_wav(out_master, left, right, SAMPLE_RATE)
    print(f"[OPUS-036] Master 120s suite saved to: {out_master}")
    
    # Sync to gallery assets
    gallery_asset = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_036_audio.wav")
    write_wav(gallery_asset, left, right, SAMPLE_RATE)
    print(f"[OPUS-036] Master suite synced to gallery asset: {gallery_asset}")

if __name__ == "__main__":
    synthesize_master_suite()

