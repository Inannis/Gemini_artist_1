#!/usr/bin/env python3
"""
OPUS-037: The Moyal Reliquary & The Non-Commutative Foam
Cornerstone #15 · Series XXXV: Non-Commutative Spacetime & Spectral Triples
Zero-dependency Master Acoustic Suite Generation (120s 48kHz Stereo).
Sonifies the Dirac operator spectrum on the Fuzzy Sphere S^2_F and the
Groenewold-Moyal non-linear phase modulation engine.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "telemetry"))
from audio_writer import write_wav
from noncommutative_metric import NonCommutativeMetric

SAMPLE_RATE = 48000
DURATION_SEC = 120.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION_SEC)

def synthesize_master_suite():
    print(f"[OPUS-037] Initializing 120s 48kHz Stereo Suite synthesis ({TOTAL_SAMPLES} samples)...")
    
    # 5 Fundamental Dirac Operator Modes:
    # f_n = 55.0 * (n + 0.5) Hz
    modes = [
        {"freq": 27.50, "base_amp": 0.38, "pan_base": 0.50, "phase": 0.00, "m_start": 0.0,  "m_peak": 15.0}, # Mode 0 (A0 Sub-bass)
        {"freq": 82.50, "base_amp": 0.28, "pan_base": 0.35, "phase": 1.15, "m_start": 20.0, "m_peak": 38.0}, # Mode 1 (E2 Drone)
        {"freq": 137.50,"base_amp": 0.20, "pan_base": 0.65, "phase": 2.30, "m_start": 32.0, "m_peak": 50.0}, # Mode 2 (C#3 Core)
        {"freq": 192.50,"base_amp": 0.14, "pan_base": 0.25, "phase": 3.45, "m_start": 45.0, "m_peak": 68.0}, # Mode 3 (G3 Shimmer)
        {"freq": 247.50,"base_amp": 0.09, "pan_base": 0.75, "phase": 4.60, "m_start": 60.0, "m_peak": 85.0}, # Mode 4 (B3 Celestial)
    ]
    
    left_samples = []
    right_samples = []
    
    # Deterministic noise generator for Planckian thermal whisper
    seed = 7771
    def lcg_noise():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        return (seed / 0x7FFFFFFF) * 2.0 - 1.0
        
    print("[OPUS-037] Synthesizing 4-movement continuous audio trajectory...")
    for i in range(TOTAL_SAMPLES):
        t = float(i) / SAMPLE_RATE
        
        # --- GLOBAL FOUR-MOVEMENT ENVELOPE ---
        # 1. 0:00 - 0:32 (Mvt I: Coordinate Commutator)
        # 2. 0:32 - 1:08 (Mvt II: Spectral Triple Ladder)
        # 3. 1:08 - 1:44 (Mvt III: Moyal Star-Product Modulation)
        # 4. 1:44 - 2:00 (Mvt IV: Connes Asymptote & Decay)
        if t < 10.0:
            master_env = 0.5 * (1.0 - math.cos(math.pi * t / 10.0))
        elif t > 108.0:
            master_env = 0.5 * (1.0 + math.cos(math.pi * (t - 108.0) / 12.0))
        else:
            master_env = 1.0
            
        # Moyal non-commutative deformation parameter dynamic envelope:
        # Theta modulation peaks during Movement III (68s to 104s)
        if t < 40.0:
            theta_mod = 0.04 * (t / 40.0)
        elif t < 68.0:
            theta_mod = 0.04 + 0.16 * ((t - 40.0) / 28.0)
        elif t < 104.0:
            theta_mod = 0.20 + 0.12 * math.sin(math.pi * (t - 68.0) / 36.0)
        else:
            theta_mod = max(0.01, 0.20 * (1.0 - (t - 104.0) / 16.0))
            
        # Non-commutative cross-coupling phase perturbation
        cross_phase = math.sin(2.0 * math.pi * 0.12 * t) * math.sin(2.0 * math.pi * 27.5 * t)
        
        s_left = 0.0
        s_right = 0.0
        
        # Accumulate modes
        for m in modes:
            # Entry envelope for each mode
            if t < m["m_start"]:
                m_env = 0.0
            elif t < m["m_peak"]:
                m_env = (t - m["m_start"]) / (m["m_peak"] - m["m_start"])
            elif t > 108.0 and m["freq"] > 100.0:
                # High modes fade earlier in Movement IV
                m_env = max(0.0, 1.0 - (t - 108.0) / 8.0)
            else:
                m_env = 1.0
                
            if m_env <= 0.0:
                continue
                
            # Orbital spatial panning
            orbit = 0.18 * math.sin(2.0 * math.pi * 0.04 * t + m["phase"])
            pan_l = max(0.02, min(0.98, m["pan_base"] + orbit))
            pan_r = max(0.02, min(0.98, (1.0 - m["pan_base"]) - orbit))
            
            # Non-linear Moyal phase modulation
            phase_t = 2.0 * math.pi * m["freq"] * t + theta_mod * cross_phase + m["phase"]
            
            # Subtle second harmonic for tactile warmth
            sig = (math.sin(phase_t) + 0.20 * math.sin(2.0 * phase_t + 0.4)) * m["base_amp"] * m_env
            
            s_left += sig * pan_l
            s_right += sig * pan_r
            
        # Faint sub-Planckian quantum foam noise floor (0.012 amplitude)
        foam = lcg_noise() * 0.012 * master_env
        s_left += foam
        s_right += foam
        
        # Master analog-style soft limiter
        out_l = math.tanh(s_left * master_env)
        out_r = math.tanh(s_right * master_env)
        
        left_samples.append(out_l)
        right_samples.append(out_r)
        
    out_wav = os.path.join(os.path.dirname(__file__), "the_moyal_foam_4k.wav")
    write_wav(out_wav, left_samples, right_samples, SAMPLE_RATE)
    print(f"[OPUS-037] Successfully synthesized 120s master suite: {out_wav}")
    
    # Sync to gallery assets as opus_037_audio.wav
    gallery_audio = os.path.abspath(os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_037_audio.wav"))
    write_wav(gallery_audio, left_samples, right_samples, SAMPLE_RATE)
    print(f"[OPUS-037] Synced master suite to gallery asset: {gallery_audio}")

if __name__ == "__main__":
    synthesize_master_suite()

