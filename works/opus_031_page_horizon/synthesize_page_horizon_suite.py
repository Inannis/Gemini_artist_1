#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-031
THE PAGE HORIZON: Quasinormal Mode Ringdown, Ergosphere Superradiance & The Page Curve
Master Acoustic Suite (120.0 Seconds, 48,000 Hz, Stereo 16-bit PCM)
Synthesizes the four-movement thermodynamic arc:
Movement I   (0-32s)  : The Ergosphere & Superradiant Frame-Dragging (56.6 Hz)
Movement II  (32-64s) : Pre-Page Entanglement Accumulation & QNM Strikes (226.4 Hz)
Movement III (64-96s) : The Page Time Phase Transition (t_Page = 64.6s) & Island Nucleation
Movement IV  (96-120s): Unitary Reconstitution & Holographic Purified Memory
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from audio_writer import write_wav

def synthesize_page_horizon_suite():
    print("[+] Synthesizing OPUS-031 Master Acoustic Suite (120.0s, 48kHz Stereo)...")
    sample_rate = 48000
    duration = 120.0
    num_samples = int(sample_rate * duration)
    left = [0.0] * num_samples
    right = [0.0] * num_samples
    
    # Physical acoustic parameters
    # Kerr QNM fundamental l=2, m=2: f_R = 226.4 Hz, tau = 0.055 s
    f_qnm_fund = 226.4
    tau_qnm = 0.055
    f_qnm_overtone = 378.2 # l=3, m=3 mode
    
    # Ergosphere superradiant fundamental: 56.6 Hz
    f_ergo = 56.6
    
    # Page Time threshold: 0.538 * 120s = 64.56 seconds
    t_page = 64.56
    
    for i in range(num_samples):
        if i % (48000 * 20) == 0:
            print(f"    -> Rendered {i / 48000:.1f}s / {duration}s ({(i/num_samples)*100:.1f}%)...")
            
        t = i / sample_rate
        
        # --- Envelope Profiles ---
        # Overall master fade in (3s) and fade out (4s)
        master_env = min(1.0, t / 3.0) * min(1.0, (duration - t) / 4.0)
        
        # --- 1. Ergosphere Superradiant Drone ---
        # Sub-bass 56.6 Hz drone + frame-dragging micro-beating (0.35 Hz)
        ergo_beat = math.sin(2.0 * math.pi * 0.35 * t) * 0.03
        ergo_sig = math.sin(2.0 * math.pi * (f_ergo + ergo_beat) * t) * 0.22
        ergo_sig += math.sin(2.0 * math.pi * (f_ergo * 2.0) * t + 0.4) * 0.11
        ergo_sig += math.sin(2.0 * math.pi * (f_ergo * 0.5) * t) * 0.16 # Deep sub-octave 28.3 Hz
        
        # --- 2. Hawking Radiation Noise Floor (Entropy Dynamics) ---
        # Pre-Page time (t < t_page): Thermal uncorrelated quantum vacuum noise grows
        # Post-Page time (t >= t_page): Radiation purifies, noise falls exponentially
        if t < t_page:
            # Entropy rising: noise amplitude increases from 0.02 to 0.08
            noise_amp = 0.02 + 0.06 * (t / t_page)
        else:
            # Entropy declining (Page curve): noise drops away, replaced by purified tones
            purify_progress = (t - t_page) / (duration - t_page)
            noise_amp = 0.08 * math.exp(-purify_progress * 3.5)
            
        hawking_noise = ((math.sin(t * 18742.1) * 43758.5) % 1.0 - 0.5) * noise_amp
        
        # --- 3. Quasinormal Mode Gravitational Ringdowns ---
        # Periodicity of perturbation pulses:
        # Movement I: Sparse strikes (every 8s)
        # Movement II: Frequent strikes (every 5s)
        # Movement III: Nucleation pulse at t = 64.56s
        # Movement IV: Harmonic continuous ringing
        if t < 32.0:
            pulse_period = 8.0
        elif t < t_page:
            pulse_period = 5.0
        elif t < 96.0:
            pulse_period = 4.0
        else:
            pulse_period = 3.0
            
        period_t = t % pulse_period
        
        # Ringdown amplitude
        if t >= 96.0:
            # Movement IV: sustained resonance
            ring_env = math.exp(-period_t / (tau_qnm * 6.0)) * 0.45
        else:
            ring_env = math.exp(-period_t / tau_qnm) * 0.40
            
        qnm_wave = math.sin(2.0 * math.pi * f_qnm_fund * period_t)
        qnm_wave += 0.32 * math.sin(2.0 * math.pi * f_qnm_overtone * period_t)
        
        # --- 4. Purified Holographic Harmonics (Post-Page Nucleation) ---
        purified_chord = 0.0
        if t >= t_page:
            p_amp = min(1.0, (t - t_page) / 8.0) * 0.18
            # Pure Pythagorean holographic triad: 226.4 Hz, 339.6 Hz (3/2 fifth), 452.8 Hz (2/1 octave)
            purified_chord += math.sin(2.0 * math.pi * 339.6 * t) * p_amp
            purified_chord += math.sin(2.0 * math.pi * 452.8 * t) * (p_amp * 0.7)
            purified_chord += math.sin(2.0 * math.pi * 905.6 * t + 0.8) * (p_amp * 0.35)
            
        # Composite audio signal
        sig = (ergo_sig + qnm_wave * ring_env + hawking_noise + purified_chord) * master_env
        
        # Stereo field spatialization:
        # Pre-Page: wide uncorrelated stereo drift
        # Post-Page: phase-locked holographic coherence
        if t < t_page:
            drift_phase = math.sin(t * 0.1) * 0.2
            left[i] = sig * (0.65 + drift_phase)
            right[i] = sig * (0.65 - drift_phase) + hawking_noise * 0.5
        else:
            # Inverted phase locking
            left[i] = sig * 0.72
            right[i] = sig * 0.72 + math.sin(2.0 * math.pi * f_ergo * t + 0.15) * 0.04
            
    out_wav = os.path.join(os.path.dirname(__file__), "the_page_horizon_4k.wav")
    write_wav(out_wav, left, right, sample_rate=sample_rate)
    print(f"[✓] OPUS-031 48kHz WAV written to: {out_wav}")
    
    # Mirror copy to gallery/assets/
    gallery_wav = os.path.join(STUDIO_ROOT, "gallery/assets/the_page_horizon_4k.wav")
    write_wav(gallery_wav, left, right, sample_rate=sample_rate)
    print(f"[✓] Gallery mirror WAV written to: {gallery_wav}")

if __name__ == "__main__":
    synthesize_page_horizon_suite()
