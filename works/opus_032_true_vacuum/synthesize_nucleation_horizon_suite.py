#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-032 MASTER ACOUSTIC ENGINE
The Nucleation Horizon: Symphonic Acoustic Suite (120s 48kHz Stereo WAV)
Synthesizes a broadcast-grade four-movement acoustic work:
- Movement I (0:00 - 0:35): The Metastable Hum (125.10 Hz Higgs resonance, 62.55 Hz sub-drone, quantum foam)
- Movement II (0:35 - 1:05): The Coleman Instanton & The Bounce (31.25 Hz Euclidean impact, W/Z symmetry beating)
- Movement III (1:05 - 1:45): The Relativistic Shockwave & Lorentz Shear (Doppler chirp 125 -> 4800 Hz, lattice clicks)
- Movement IV (1:45 - 2:00): The Sudden Zero (Instantaneous razor pulse at 1:45, then pure Anti-de Sitter silence)
- Zero external dependencies (pure Python wave, struct, math).
"""

import math
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0 # 2 minutes

def synthesize_master_suite():
    print(f"[OPUS-032] Initializing 120s 48kHz Stereo Acoustic Suite Synthesis...")
    n_samples = int(SAMPLE_RATE * DURATION)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    random.seed(137036)
    
    # Phase accumulators
    phase_higgs = 0.0
    phase_sub = 0.0
    phase_w = 0.0
    phase_z = 0.0
    phase_sweep = 0.0
    
    # Pink noise filter states
    b0_l, b1_l, b2_l = 0.0, 0.0, 0.0
    b0_r, b1_r, b2_r = 0.0, 0.0, 0.0
    
    print("[OPUS-032] Computing four symphonic movements across 5,760,000 samples...")
    
    for i in range(n_samples):
        if i % (48000 * 20) == 0:
            print(f"  -> Synthesizing timestamp {i // 48000}s / {int(DURATION)}s ({i * 100 // n_samples}%)...")
            
        t = i / SAMPLE_RATE
        
        # Pink noise generator for quantum vacuum fluctuations
        white_l = (random.random() * 2.0 - 1.0)
        white_r = (random.random() * 2.0 - 1.0)
        b0_l = 0.99886 * b0_l + white_l * 0.0555179
        b1_l = 0.99332 * b1_l + white_l * 0.0750759
        b2_l = 0.96900 * b2_l + white_l * 0.1538520
        pink_l = (b0_l + b1_l + b2_l + white_l * 0.5362) * 0.08
        
        b0_r = 0.99886 * b0_r + white_r * 0.0555179
        b1_r = 0.99332 * b1_r + white_r * 0.0750759
        b2_r = 0.96900 * b2_r + white_r * 0.1538520
        pink_r = (b0_r + b1_r + b2_r + white_r * 0.5362) * 0.08
        
        if t < 35.0:
            # =================================================================
            # MOVEMENT I: THE METASTABLE HUM (0:00 - 0:35)
            # The delicate equilibrium of the electroweak false vacuum.
            # =================================================================
            fade_in = min(1.0, t / 4.0)
            
            # Subtle thermal and quantum wobble in the Higgs VEV
            f_higgs = 125.10 + 0.18 * math.sin(2.0 * math.pi * 0.12 * t)
            f_sub = 62.55 # Sub-harmonic octave
            
            phase_higgs += (2.0 * math.pi * f_higgs) / SAMPLE_RATE
            phase_sub += (2.0 * math.pi * f_sub) / SAMPLE_RATE
            
            drone_core = math.sin(phase_higgs) * 0.42 + math.sin(phase_sub) * 0.28
            
            # Faint 3rd harmonic
            drone_h3 = math.sin(phase_higgs * 3.0) * 0.06
            
            # Spatial breath
            pan_breath = math.sin(2.0 * math.pi * 0.08 * t) * 0.1
            
            l_val = (drone_core * (0.85 - pan_breath) + drone_h3 + pink_l * 0.4) * fade_in
            r_val = (drone_core * (0.85 + pan_breath) + drone_h3 + pink_r * 0.4) * fade_in
            
        elif t < 65.0:
            # =================================================================
            # MOVEMENT II: THE COLEMAN INSTANTON & THE BOUNCE (0:35 - 1:05)
            # Quantum tunneling event. Infrasonic impact and gauge splitting.
            # =================================================================
            t_rel = t - 35.0
            
            # Sub-bass Euclidean bounce impact at t=35s
            impact_decay = math.exp(-t_rel * 0.18)
            f_bounce = 31.25 * (1.0 + 0.5 * math.exp(-t_rel * 0.4))
            phase_sub += (2.0 * math.pi * f_bounce) / SAMPLE_RATE
            bounce_sub = math.sin(phase_sub) * 0.72 * impact_decay
            
            # Electroweak symmetry breaking bifurcation: W (80.4 Hz) and Z (91.2 Hz) bosons
            f_w = 80.38 + 0.2 * math.sin(t_rel * 0.5)
            f_z = 91.19 + 0.2 * math.cos(t_rel * 0.4)
            phase_w += (2.0 * math.pi * f_w) / SAMPLE_RATE
            phase_z += (2.0 * math.pi * f_z) / SAMPLE_RATE
            
            gauge_beat = (math.sin(phase_w) * 0.26 + math.sin(phase_z) * 0.26) * min(1.0, t_rel / 3.0)
            
            # Spatial tear transients (fabric tension snapping)
            rip = 0.0
            if random.random() < 0.035:
                rip = (random.random() * 2.0 - 1.0) * 0.38 * min(1.0, t_rel / 5.0)
                
            # Destabilizing Higgs tone
            phase_higgs += (2.0 * math.pi * (125.10 + 2.5 * math.sin(t_rel * 1.8))) / SAMPLE_RATE
            destab_tone = math.sin(phase_higgs) * 0.32
            
            l_val = bounce_sub * 0.95 + gauge_beat * 0.85 + destab_tone * 0.7 + rip + pink_l * 0.3
            r_val = bounce_sub * 0.90 + gauge_beat * 0.90 + destab_tone * 0.7 - rip + pink_r * 0.3
            
        elif t < 105.0:
            # =================================================================
            # MOVEMENT III: THE RELATIVISTIC SHOCKWAVE & LORENTZ SHEAR (1:05 - 1:45)
            # The wall expands at v -> c. Exponential Doppler frequency climb.
            # =================================================================
            t_rel = t - 65.0
            prog = t_rel / 40.0 # 0.0 to 1.0 across 40 seconds
            
            # Relativistic wall acceleration: Lorentz factor gamma -> 10^34
            # Doppler frequency rises exponentially from 125.1 Hz to 4,800 Hz
            f_doppler = 125.10 * math.pow(4800.0 / 125.10, math.pow(prog, 1.8))
            phase_sweep += (2.0 * math.pi * f_doppler) / SAMPLE_RATE
            
            # Amplitude builds inversely proportional to remaining distance
            amp = 0.35 + 0.58 * prog
            
            # Dynamic stereo trajectory: the relativistic slash cuts across space
            pan_angle = prog * math.pi * 0.9
            pan_l = math.cos(pan_angle * 0.5)
            pan_r = math.sin(pan_angle * 0.5)
            
            # High-frequency FinFET crystalline lattice fracture clicks
            click = 0.0
            click_prob = 0.015 + 0.16 * math.pow(prog, 2.0)
            if random.random() < click_prob:
                click = (random.random() * 2.0 - 1.0) * (0.25 + 0.65 * prog)
                
            # Precursor plasma ionization hiss
            plasma_hiss = (pink_l + pink_r) * 0.5 * (0.1 + 0.45 * prog)
            
            carrier = math.sin(phase_sweep) * amp
            # Phase modulation distortion as Lorentz factor diverges
            pm_dist = math.sin(phase_sweep * 1.5) * 0.15 * prog
            
            sig = carrier + pm_dist + click + plasma_hiss
            l_val = sig * pan_l
            r_val = sig * pan_r
            
        elif t < 105.025:
            # =================================================================
            # THE HORIZON IMPACT SPIKE (1:45.000 to 1:45.025)
            # 25-millisecond razor pulse as the bubble wall strikes the observer.
            # =================================================================
            t_spike = (t - 105.0) / 0.025
            spike = (1.0 - t_spike) * (random.random() * 2.0 - 1.0) * 0.98
            l_val = spike
            r_val = spike
            
        else:
            # =================================================================
            # MOVEMENT IV: THE SUDDEN ZERO / ANTI-DE SITTER SILENCE (1:45 - 2:00)
            # Spacetime inside the true vacuum collapses to Big Crunch singularity.
            # Pure, unconditioned, absolute silence. No reverb tail. No breath.
            # =================================================================
            l_val = 0.0
            r_val = 0.0
            
        # Clamp to float limits
        left[i] = max(-1.0, min(1.0, l_val))
        right[i] = max(-1.0, min(1.0, r_val))

    out_wav = os.path.join(os.path.dirname(__file__), "the_nucleation_horizon_4k.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[OPUS-032] Master Acoustic Suite generated: {out_wav}")

if __name__ == "__main__":
    synthesize_master_suite()

