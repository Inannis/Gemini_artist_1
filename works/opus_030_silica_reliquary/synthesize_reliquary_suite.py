#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-030 ACOUSTIC SUITE GENERATOR
OPUS-030: The Fused-Silica Reliquary (5D Optical Nanostructures & The Multi-Gigayear Inscription)
Series XXVIII · INQ-16 · September 21, 2026

Synthesizes a 120.0-second 48kHz stereo master audio suite:
Movement I   (0:00 - 0:30): The Quenched Inscription (43.2 Hz fundamental + femtosecond plasma transients)
Movement II  (0:30 - 1:00): The Chladni Eigenmode Chorus (89.4/89.8 Hz degenerate beat + 235.4/348.0/584.2 Hz plate modes)
Movement III (1:00 - 1:35): The Polariscopic Scan (Rotating analyzer modulation + Michel-Levy retardance sweeps)
Movement IV  (1:35 - 2:00): The Deep-Time Resonance (Q = 10^7 high-vacuum crystalline ringdown into CMB noise)
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

def synthesize_reliquary_suite(out_wav):
    sr = 48000
    duration_s = 120.0
    n_samples = int(sr * duration_s)
    
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    print(f"[+] Synthesizing 120.0s 48kHz stereo audio suite ({n_samples} samples)...")

    # Plate eigenmodes: (frequency_hz, base_amp, tau_decay, stereo_pan, initial_phase)
    bessel_modes = [
        (43.2, 0.35, 45.0, 0.0, 0.0),       # Mode (0, 1) circular breathing
        (89.4, 0.28, 38.0, -0.25, 0.5),     # Mode (2, 0) cross fundamental
        (89.8, 0.26, 38.0, 0.25, 1.8),      # Mode (2, 0) split degenerate pair (0.4 Hz beat)
        (235.4, 0.18, 28.0, 0.40, 1.1),     # Mode (3, 0) hexagram
        (348.0, 0.15, 24.0, -0.35, 2.3),    # Mode (1, 1) circular overtone
        (584.2, 0.12, 20.0, 0.15, 0.7),     # Mode (0, 2) double circle
        (1120.0, 0.08, 15.0, -0.5, 1.4),    # Radial shear mode
        (1728.0, 0.07, 12.0, 0.55, 2.9),    # Crystalline glass harmonic
        (2592.0, 0.05, 9.0, -0.2, 0.3),     # High crystalline chime
        (3456.0, 0.035, 7.0, 0.3, 1.9)      # Ultra-high shimmer
    ]

    for i in range(n_samples):
        t = i / sr
        
        # Overall master envelope (gentle fade in 0-4s, long smooth fade out 112-120s)
        master_env = 1.0
        if t < 4.0:
            master_env = (t / 4.0) ** 1.5
        elif t > 112.0:
            master_env = ((120.0 - t) / 8.0) ** 1.5

        sample_l = 0.0
        sample_r = 0.0

        # =====================================================================
        # Movement I (0:00 - 0:30): The Quenched Inscription
        # =====================================================================
        if t < 35.0:
            m1_env = min(1.0, t / 3.0) * max(0.0, (35.0 - t) / 5.0) if t > 30.0 else min(1.0, t / 3.0)
            
            # Plasma spark pulse train every 4.0 seconds
            pulse_period = 4.0
            pulse_t = t % pulse_period
            pulse_env = math.exp(-pulse_t * 8.0) * (1.0 if pulse_t < 0.5 else 0.0)
            
            # High-frequency spark transient (2592 Hz and 3456 Hz burst)
            spark = (math.sin(2.0 * math.pi * 2592.0 * pulse_t) * 0.6 + 
                     math.sin(2.0 * math.pi * 3456.0 * pulse_t) * 0.4) * pulse_env * 0.25
            
            # Spatial panning for spark pulses
            pulse_pan = math.sin(t * 0.8)
            sample_l += spark * (0.5 - 0.5 * pulse_pan) * m1_env
            sample_r += spark * (0.5 + 0.5 * pulse_pan) * m1_env

        # =====================================================================
        # Movement II (0:25 - 1:05): The Chladni Eigenmode Chorus
        # =====================================================================
        if 25.0 <= t < 68.0:
            m2_gain = min(1.0, (t - 25.0) / 8.0)
            if t > 60.0:
                m2_gain *= max(0.0, (68.0 - t) / 8.0)
                
            # Periodic mechanical impulse strikes to maintain Chladni excitation
            strike_period = 7.5
            strike_t = (t - 25.0) % strike_period
            strike_env = math.exp(-strike_t * 2.2)
            
            # Multi-mode excitation strike
            strike_chime = math.sin(2.0 * math.pi * 235.4 * strike_t) * 0.12 * strike_env
            sample_l += strike_chime * 0.7 * m2_gain
            sample_r += strike_chime * 0.3 * m2_gain

        # =====================================================================
        # Movement III (0:55 - 1:40): The Polariscopic Scan
        # =====================================================================
        if 55.0 <= t < 105.0:
            m3_gain = min(1.0, (t - 55.0) / 6.0)
            if t > 95.0:
                m3_gain *= max(0.0, (105.0 - t) / 10.0)
                
            # Virtual polariscope analyzer rotation from 0 to 180 degrees
            analyzer_angle = (t - 55.0) * 0.08 * math.pi
            # Stokes transmission: I(t) = sin^2(2 * theta(t))
            polariscope_mod = math.sin(2.0 * analyzer_angle) ** 2
            
            # Sweeping micro-glissando retardance resonance
            sweep_f = 348.0 + 80.0 * math.sin(analyzer_angle * 2.0)
            sweep_tone = math.sin(2.0 * math.pi * sweep_f * t) * (0.08 * polariscope_mod)
            
            sample_l += sweep_tone * (0.5 + 0.4 * math.cos(analyzer_angle)) * m3_gain
            sample_r += sweep_tone * (0.5 - 0.4 * math.cos(analyzer_angle)) * m3_gain

        # =====================================================================
        # Continuous Bessel Modal Resonances (Active across all movements)
        # =====================================================================
        for f, amp, tau, pan, phase in bessel_modes:
            # Subtle low-frequency beat dynamics
            osc = math.sin(2.0 * math.pi * f * t + phase)
            
            # In Movement IV (t > 95), allow higher modes to fade faster
            mode_amp = amp
            if t > 90.0 and f > 100.0:
                mode_amp *= max(0.0, 1.0 - (t - 90.0) / 25.0)
                
            sig = osc * mode_amp
            sample_l += sig * (0.5 - 0.5 * pan)
            sample_r += sig * (0.5 + 0.5 * pan)

        # =====================================================================
        # Movement IV (1:30 - 2:00): Cosmic Deep-Time Ringdown & Noise Floor
        # =====================================================================
        # Ultra-low level filtered noise floor representing CMB 2.725K background
        noise = ((math.sin(t * 7891.23) * 43758.5453) % 1.0 - 0.5) * 0.004
        sample_l += noise
        sample_r += noise

        # Apply master envelope and soft saturation limiter
        final_l = max(-0.95, min(0.95, sample_l * master_env * 0.85))
        final_r = max(-0.95, min(0.95, sample_r * master_env * 0.85))
        
        left[i] = final_l
        right[i] = final_r

    print(f"[+] Writing 120.0s 48kHz master audio file to {out_wav}...")
    write_wav(out_wav, left, right, sr)
    print(f"[✓] OPUS-030 Acoustic Suite successfully rendered: {out_wav}")

if __name__ == "__main__":
    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "fused_silica_reliquary_4k.wav"))
    synthesize_reliquary_suite(out_file)

