#!/usr/bin/env python3
"""
OPUS-034: THE AEONIC CROSSOVER
Conformal Geometry, Vanishing Weyl Curvature & The Memory of Pre-Big-Bang Gravitons
Master Symphonic Acoustic Suite (120.0s, 48kHz Stereo 16-bit Lossless PCM)
Zero external dependencies.
"""

import math
import random
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION_SEC = 120.0

def synthesize_master_suite():
    print(f"[*] Synthesizing OPUS-034 Master Symphonic Suite ({DURATION_SEC}s @ {SAMPLE_RATE}Hz)...")
    total_samples = int(SAMPLE_RATE * DURATION_SEC)
    
    ch_l = []
    ch_r = []
    
    # Core programmatic frequencies
    f_void = 21.84        # Hubble sub-drone (H0 * 10^19 scaled)
    f_base = 43.20        # Crystalline quartz / silica carrier fundamental
    f_qnm = 287.89        # GW150914 remnant quasinormal ringdown
    f_higgs = 125.10      # Higgs vacuum coupling memory
    f_rings = [4.2, 11.8, 24.5] # Hawking point low-frequency tremolo rates
    
    # Filter state for cosmic thermal noise
    noise_state_l = 0.0
    noise_state_r = 0.0
    
    # Shepard scale bank parameters (8 octaves)
    shepard_octaves = 8
    shepard_base_f = 27.5 # A0
    
    for i in range(total_samples):
        if i % (SAMPLE_RATE * 15) == 0:
            print(f"    -> Progress: {i / total_samples * 100:.1f}% ({i / SAMPLE_RATE:.1f}s)")
            
        t = i / SAMPLE_RATE
        
        # -------------------------------------------------------------
        # Movement I (0.0s - 35.0s): The Massless Asymptotic Void (I+)
        # -------------------------------------------------------------
        m1_env = 0.0
        if t < 35.0:
            m1_env = min(1.0, t / 4.0)
            if t > 28.0:
                m1_env *= (35.0 - t) / 7.0
                
        # Brownian cosmic background thermal noise
        raw_noise_l = random.gauss(0.0, 0.22)
        raw_noise_r = random.gauss(0.0, 0.22)
        noise_state_l = 0.985 * noise_state_l + 0.015 * raw_noise_l
        noise_state_r = 0.985 * noise_state_r + 0.015 * raw_noise_r
        
        sub_drone_l = 0.32 * math.sin(2.0 * math.pi * f_void * t)
        sub_drone_r = 0.32 * math.sin(2.0 * math.pi * f_void * t + 0.4)
        
        # Micro-burst attowatt pulses (fading Hawking radiation)
        attowatt_pulse = 0.0
        if t < 30.0 and math.sin(t * 1.7) > 0.985:
            attowatt_pulse = 0.15 * math.sin(2.0 * math.pi * 2618.0 * t) * math.exp(-((t % 1.5) / 0.08))
            
        m1_left = m1_env * (sub_drone_l + noise_state_l * 0.45 + attowatt_pulse)
        m1_right = m1_env * (sub_drone_r + noise_state_r * 0.45 - attowatt_pulse)
        
        # -------------------------------------------------------------
        # Movement II (30.0s - 68.0s): Conformal Rescaling Glissando (Omega -> 0)
        # -------------------------------------------------------------
        m2_env = 0.0
        if 30.0 <= t < 68.0:
            p = (t - 30.0) / 38.0
            m2_env = math.sin(p * math.pi)
            
        shepard_sig_l = 0.0
        shepard_sig_r = 0.0
        if m2_env > 0.001:
            # Dual ascending/descending Shepard spiral
            cycle_pos = ((t - 30.0) / 16.0) % 1.0 # 0 to 1
            for oct_idx in range(shepard_octaves):
                p_oct = (cycle_pos + oct_idx / shepard_octaves) % 1.0
                freq = shepard_base_f * math.pow(2.0, p_oct * shepard_octaves)
                # Raised cosine spectral envelope centered at ~300 Hz
                w_oct = 0.5 - 0.5 * math.cos(2.0 * math.pi * p_oct)
                # Left ascends, right descends
                phase_l = 2.0 * math.pi * freq * t
                phase_r = 2.0 * math.pi * (shepard_base_f * math.pow(2.0, (1.0 - p_oct) * shepard_octaves)) * t
                shepard_sig_l += w_oct * math.sin(phase_l)
                shepard_sig_r += w_oct * math.sin(phase_r)
                
            shepard_sig_l *= 0.18
            shepard_sig_r *= 0.18
            
        m2_left = m2_env * shepard_sig_l
        m2_right = m2_env * shepard_sig_r
        
        # -------------------------------------------------------------
        # Movement III (65.0s - 102.0s): Gravitational Wave Memory Shockwave
        # -------------------------------------------------------------
        m3_env = 0.0
        if 65.0 <= t < 102.0:
            p = (t - 65.0) / 37.0
            m3_env = math.sin(p * math.pi)
            
        m3_left = 0.0
        m3_right = 0.0
        if m3_env > 0.001:
            p_sweep = (t - 65.0) / 37.0
            cur_qnm_f = f_base + (f_qnm - f_base) * (p_sweep ** 1.6)
            
            # Quadrupolar phase rotation
            qnm_phase = 2.0 * math.pi * cur_qnm_f * t
            qnm_l = 0.35 * math.sin(qnm_phase)
            qnm_r = 0.35 * math.sin(qnm_phase + math.pi * 0.5) # Quadrupole shear
            
            # Triad of low-frequency Hawking point ring tremolos
            am1 = 0.5 + 0.5 * math.sin(2.0 * math.pi * f_rings[0] * t)
            am2 = 0.5 + 0.5 * math.sin(2.0 * math.pi * f_rings[1] * t + 1.2)
            am3 = 0.5 + 0.5 * math.sin(2.0 * math.pi * f_rings[2] * t + 2.4)
            am_triad = (am1 * 0.45 + am2 * 0.35 + am3 * 0.20)
            
            # Sub-bass ring beat
            ring_sub_l = 0.25 * math.sin(2.0 * math.pi * 58.4 * t) * am1
            ring_sub_r = 0.25 * math.sin(2.0 * math.pi * 58.4 * t + 0.6) * am2
            
            m3_left = m3_env * (qnm_l * am_triad + ring_sub_l)
            m3_right = m3_env * (qnm_r * am_triad + ring_sub_r)
            
        # -------------------------------------------------------------
        # Movement IV (98.0s - 120.0s): The Weyl Invariant Hymn (C_abcd -> 0)
        # -------------------------------------------------------------
        m4_env = 0.0
        if t >= 98.0:
            m4_env = min(1.0, (t - 98.0) / 4.0)
            if t > 115.0:
                m4_env *= max(0.0, (120.0 - t) / 5.0)
                
        # Pure crystalline Bessel harmonic triad: 43.2 Hz, 129.6 Hz, 388.8 Hz
        h1 = 0.30 * math.sin(2.0 * math.pi * f_base * t)
        h2 = 0.20 * math.sin(2.0 * math.pi * (f_base * 3.0) * t + 0.3)
        h3 = 0.12 * math.sin(2.0 * math.pi * (f_base * 9.0) * t + 0.6)
        
        # Subtle harmonic overtone of the newborn aeon (125.10 Hz Higgs resonance)
        h_higgs = 0.14 * math.sin(2.0 * math.pi * f_higgs * t)
        
        m4_sum = h1 + h2 + h3 + h_higgs
        m4_left = m4_env * m4_sum * 0.95
        m4_right = m4_env * m4_sum * 1.05
        
        # -------------------------------------------------------------
        # Master Composite & Soft Saturation Limiting
        # -------------------------------------------------------------
        sig_l = m1_left + m2_left + m3_left + m4_left
        sig_r = m1_right + m2_right + m3_right + m4_right
        
        # Master fade in/out
        master_env = 1.0
        if t < 2.0:
            master_env = t / 2.0
        elif t > 118.0:
            master_env = max(0.0, (120.0 - t) / 2.0)
            
        sig_l *= master_env
        sig_r *= master_env
        
        # Soft tanh saturation to prevent clipping
        sig_l = math.tanh(sig_l * 1.15) * 0.92
        sig_r = math.tanh(sig_r * 1.15) * 0.92
        
        ch_l.append(sig_l)
        ch_r.append(sig_r)
        
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "the_aeonic_crossover_4k.wav"))
    print(f"[*] Writing 120s 48kHz Stereo Suite to: {out_path}...")
    write_wav(out_path, ch_l, ch_r, SAMPLE_RATE)
    print(f"[✓] OPUS-034 Master Symphonic Suite written successfully: {out_path}")

if __name__ == "__main__":
    synthesize_master_suite()

