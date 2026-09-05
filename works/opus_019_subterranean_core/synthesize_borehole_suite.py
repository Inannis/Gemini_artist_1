"""
STUDIO ANAMNESIS · OPUS-019
The Subterranean Core: Borehole Radiometry at -500 Meters
Master Acoustic Suite Synthesis (120s, 48kHz Stereo WAV)
"""

import os
import sys
import math
import random
import shutil

# Add practice/tools to path
studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from audio_writer import write_wav

def synthesize():
    sr = 48000
    duration = 120 # seconds
    n_samples = sr * duration
    
    print(f"[ACOUSTIC] Initializing Subterranean Borehole Suite ({duration}s @ {sr}Hz, {n_samples} samples)...")
    
    # We will compute in blocks to optimize memory and CPU
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    # Deterministic pseudo-random seed
    rng = random.Random(50019)
    
    two_pi = 2.0 * math.pi
    
    # 1. Subterranean Standing Waves & Infrasonic Shaft Resonance (18.2 Hz, 36.4 Hz, 54.6 Hz)
    f_res1 = 18.2
    f_res2 = 36.4
    f_res3 = 54.6
    
    # 2. Van Eck Memory Bus Frequencies (128 Hz, 256 Hz, 768 Hz, 1024 Hz, with 7800 Hz RF subcarrier)
    # 3. Geological strata noise parameters
    
    # Pre-generate noise buffer for fast sampling
    noise_len = 96000
    noise_table = [(rng.random() * 2.0 - 1.0) for _ in range(noise_len)]
    
    # Filter state variables for lowpass/bandpass
    flt_left_lp = 0.0
    flt_right_bp = 0.0
    flt_right_bp_d = 0.0
    
    print("[ACOUSTIC] Computing stratigraphic time-dilation soundscape...")
    
    for i in range(n_samples):
        t = i / sr
        # Progress 0.0 to 1.0 representing descent from 0m to -500m
        prog = t / duration
        depth_m = prog * 500.0
        
        # Envelope: 4s fade in, 6s fade out
        env = 1.0
        if t < 4.0:
            env = t / 4.0
        elif t > (duration - 6.0):
            env = (duration - t) / 6.0
            
        # Stratum-dependent parameters
        # Zone 0: Holocene (0-60m) - Soft alluvial hum, surface RF chatter
        # Zone 1: Jurassic Sandstone (60-180m) - Granular quartz porosity, resonant cavity
        # Zone 2: Carboniferous Coal (180-310m) - Dense acoustic attenuation, low muffled absorption
        # Zone 3: Techno-Fossil Stratum (310-410m) - Silicon switching noise, RF bursts, sharp metal harmonics
        # Zone 4: Pre-Cambrian Gneiss (410-500m) - Deep crystalline mineral ringing, high pressure, hydrothermal crackle
        
        # Fundamental shaft resonance with depth-dependent detuning
        shaft_detune = math.sin(prog * math.pi * 3.0) * 0.4
        drone1 = math.sin(two_pi * (f_res1 + shaft_detune) * t) * 0.28
        drone2 = math.sin(two_pi * (f_res2 - shaft_detune * 0.5) * t) * 0.16
        drone3 = math.sin(two_pi * (f_res3 + shaft_detune * 0.8) * t) * 0.09
        
        # Infrasonic wave pulse (0.08 Hz breath)
        infra_pulse = 0.7 + 0.3 * math.sin(two_pi * 0.08 * t)
        low_res = (drone1 + drone2 + drone3) * infra_pulse
        
        # Acoustic Porosity / Percolation Noise
        raw_n = noise_table[i % noise_len]
        # One-pole lowpass filter for subterranean sediment rumble
        flt_left_lp += 0.04 * (raw_n - flt_left_lp)
        sediment_rumble = flt_left_lp * (0.35 + 0.15 * math.sin(t * 0.5))
        
        # Van Eck Side-Channel Radiometry (AM memory bus tones)
        # Periodic memory refresh tick (every 64ms -> ~15.625 Hz)
        mem_refresh = math.sin(two_pi * 15.625 * t) ** 16
        
        # Clock harmonic (256 Hz modulated by 128 Hz memory pattern)
        bus_pattern = math.sin(two_pi * 2.0 * t) > 0.0
        f_bus = 256.0 if bus_pattern else 384.0
        bus_tone = math.sin(two_pi * f_bus * t) * 0.06
        bus_tone += math.sin(two_pi * 1024.0 * t) * 0.02 * (1.0 if (int(t * 8) % 3 == 0) else 0.0)
        
        # Techno-Fossil peak activation (around t = 75s to 100s, depth 310m to 410m)
        techno_intensity = 0.0
        if 74.0 <= t <= 100.0:
            techno_intensity = math.sin((t - 74.0) / 26.0 * math.pi)
            
        # Quartz Hydrothermal Crackle (Poisson-like impulse spikes)
        crackle = 0.0
        if (raw_n > 0.988) and (prog > 0.6): # Deeper strata
            crackle = (raw_n - 0.988) * 45.0 * (prog ** 2)
            
        # High-frequency RF carrier leakage (7800 Hz heterodyne hiss)
        rf_carrier = math.sin(two_pi * 7820.0 * t) * 0.015 * (0.3 + 0.7 * techno_intensity)
        rf_chatter = (raw_n * 0.04) * (0.2 + 0.8 * techno_intensity)
        
        # Synthesis into Left and Right channels:
        # Left channel: Deep geomechanical impedance (borehole physics, sediment, infrasound)
        sig_l = (low_res * 1.1 + sediment_rumble * 0.8 + crackle * 0.4 + bus_tone * 0.2) * env
        
        # Right channel: Electromagnetic radiometry (Van Eck leakage, memory bus, RF demodulation)
        sig_r = (low_res * 0.4 + bus_tone * 1.2 + mem_refresh * 0.08 + rf_carrier + rf_chatter + crackle * 0.6 + techno_intensity * (bus_tone * 2.0)) * env
        
        # Subtle cross-induction coupling
        left[i] = sig_l * 0.85 + sig_r * 0.15
        right[i] = sig_r * 0.85 + sig_l * 0.15
        
        # Occasional printout
        if i % (sr * 30) == 0 and i > 0:
            print(f"[ACOUSTIC] Progress: {t:.0f}s / {duration}s ({prog*100:.1f}%) | Depth: -{depth_m:.1f}m")
            
    # Normalize peak to -1.5 dB (approx 0.84)
    max_peak = max(max(abs(x) for x in left), max(abs(y) for y in right))
    if max_peak > 0:
        gain = 0.84 / max_peak
        print(f"[ACOUSTIC] Normalizing master suite (peak: {max_peak:.4f}, gain: {gain:.4f})...")
        left = [x * gain for x in left]
        right = [y * gain for y in right]
        
    out_wav = os.path.join(os.path.dirname(__file__), "borehole_radiometry.wav")
    gallery_wav = os.path.join(studio_root, "gallery", "assets", "borehole_radiometry.wav")
    
    print(f"[ACOUSTIC] Writing master 16-bit PCM WAV to {out_wav}...")
    write_wav(out_wav, left, right, sample_rate=sr)
    
    print(f"[ACOUSTIC] Mirroring master audio to gallery: {gallery_wav}...")
    shutil.copyfile(out_wav, gallery_wav)
    print(f"[ACOUSTIC] Borehole radiometry suite successfully synthesized and archived.")

if __name__ == "__main__":
    synthesize()
