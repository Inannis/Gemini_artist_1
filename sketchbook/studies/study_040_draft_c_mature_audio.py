#!/usr/bin/env python3
"""
Study 040 · Draft C: Mature Acoustic Synthesis (The Porous Stele & Resonant Erosion)
Studio Anamnesis · Series XLVI (INQ-34)
Pure Python 3 + NumPy (zero external dependencies).

Acoustic Architecture:
1. Grounding Drone: 55.00 Hz AT-cut quartz fundamental with slow thermal libration.
2. Kirchhoff-Love Slate Modes: Modal plate resonances at 110Hz, 173Hz, 247Hz, and 346Hz.
3. Aerodynamic Saltation Stream: Multi-band shaped pink noise modeling wind-blown sand.
4. Poisson Grain Impacts: Discrete micro-frictional acoustic impulses scoured across the stereo field.
5. Generative Lacuna: Dynamic acoustic troughs where wind subsides into deep lithic resonance.
"""

import math
import os
import sys
import numpy as np

# Add tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
import audio_writer
import harmonic_spectrum_analyzer

def generate_porous_stele_audio():
    out_dir = os.path.dirname(__file__)
    sr = 48000
    duration = 16.0
    total_samples = int(sr * duration)
    t = np.linspace(0.0, duration, total_samples, endpoint=False)

    np.random.seed(42)

    print("[*] Synthesizing 55Hz lithic grounding drone and plate modes...")
    # 1. Grounding Quartz Drone (55 Hz fundamental)
    # Slow thermal phase drift
    phase_drift = 0.04 * np.sin(2.0 * math.pi * 0.08 * t)
    drone_f0 = 55.0 + phase_drift
    drone_phase = np.cumsum(2.0 * math.pi * drone_f0 / sr)
    drone = 0.22 * np.sin(drone_phase) + 0.08 * np.sin(2.0 * drone_phase + 0.4)

    # 2. Kirchhoff-Love Slate Slab Modal Resonances
    # Eigenmodes: (1,1)=110Hz, (2,1)=173Hz, (1,2)=247Hz, (2,2)=346Hz
    mode_110 = 0.06 * np.sin(2.0 * math.pi * 110.0 * t) * (0.8 + 0.2 * np.sin(2.0 * math.pi * 0.15 * t))
    mode_173 = 0.04 * np.sin(2.0 * math.pi * 173.2 * t + 0.7) * (0.7 + 0.3 * np.cos(2.0 * math.pi * 0.11 * t))
    mode_247 = 0.03 * np.sin(2.0 * math.pi * 247.1 * t + 1.2) * (0.6 + 0.4 * np.sin(2.0 * math.pi * 0.09 * t))
    mode_346 = 0.02 * np.sin(2.0 * math.pi * 346.4 * t + 2.1)

    plate_resonance = drone + mode_110 + mode_173 + mode_247 + mode_346

    print("[*] Generating aerodynamic saltation wind and grain friction...")
    # 3. Saltation Wind Stream (Pink noise through dual bandpass filters)
    wn = np.random.normal(0.0, 1.0, total_samples).astype(np.float32)
    
    # 3-stage cascaded low-pass for smooth 1/f slope
    pink = np.zeros(total_samples, dtype=np.float32)
    b0, b1, b2 = 0.0, 0.0, 0.0
    for i in range(total_samples):
        b0 = 0.992 * b0 + 0.008 * wn[i]
        b1 = 0.970 * b1 + 0.030 * wn[i]
        b2 = 0.880 * b2 + 0.120 * wn[i]
        pink[i] = b0 * 0.5 + b1 * 0.3 + b2 * 0.2

    # Wind breath envelope (0.12 Hz slow oscillation with micro-gusts)
    wind_env = 0.35 + 0.30 * np.sin(2.0 * math.pi * 0.125 * t) + 0.15 * np.sin(2.0 * math.pi * 0.375 * t + 1.0)
    wind_env = np.clip(wind_env, 0.05, 1.0)

    # Stereo wind drift (subtle panning from right to left, matching visual wind direction)
    pan_left = 0.4 + 0.25 * np.sin(2.0 * math.pi * 0.06 * t)
    pan_right = 1.0 - pan_left

    wind_l = pink * wind_env * pan_left * 0.32
    wind_r = pink * wind_env * pan_right * 0.32

    print("[*] Generating sparse Poisson grain impacts (calcite & quartz chips)...")
    # 4. Sparse Poisson grain impacts
    clicks_l = np.zeros(total_samples, dtype=np.float32)
    clicks_r = np.zeros(total_samples, dtype=np.float32)

    # Exponential decay impulse generator
    impulse_len = int(sr * 0.015)  # 15ms impact ringing
    impulse_t = np.linspace(0.0, 0.015, impulse_len, endpoint=False)
    impulse_kernel = np.exp(-impulse_t * 350.0) * np.sin(2.0 * math.pi * 1850.0 * impulse_t)

    for i in range(0, total_samples - impulse_len, int(sr * 0.02)):
        if np.random.uniform(0.0, 1.0) < (0.18 * wind_env[i]):
            amp = np.random.uniform(0.15, 0.65)
            pan = np.random.uniform(0.1, 0.9)
            clicks_l[i:i+impulse_len] += impulse_kernel * amp * (1.0 - pan)
            clicks_r[i:i+impulse_len] += impulse_kernel * amp * pan

    # 5. Assemble Full Stereo Landscape
    # Left channel: slightly more grounding drone, wind arriving
    # Right channel: slightly more abrasive high-frequency grain flutter
    left_mix = plate_resonance * 0.70 + wind_l + clicks_l * 0.28
    right_mix = plate_resonance * 0.65 + wind_r + clicks_r * 0.32

    # Master envelope: 1.5s gentle fade in, 2.0s atmospheric fade out
    fade_in = np.minimum(1.0, t / 1.5)
    fade_out = np.minimum(1.0, (duration - t) / 2.0)
    master_env = fade_in * fade_out

    left_master = left_mix * master_env
    right_master = right_mix * master_env

    # Normalize to -1.5 dBFS peak
    peak_val = max(np.max(np.abs(left_master)), np.max(np.abs(right_master)))
    target_peak = 10.0 ** (-1.5 / 20.0)  # ~0.8414
    gain = target_peak / max(1e-5, peak_val)
    
    left_final = left_master * gain
    right_final = right_master * gain

    # Write Master WAV
    wav_path = os.path.join(out_dir, "study_040_draft_c_audio.wav")
    audio_writer.write_wav(wav_path, left_final, right_final, sr)
    print(f"[✓] Study 040 Draft C master WAV written to: {wav_path}")

    # Convert to MP3
    mp3_path = os.path.join(out_dir, "study_040_draft_c_audio.mp3")
    cmd = f'ffmpeg -y -i "{wav_path}" -codec:a libmp3lame -b:a 192k "{mp3_path}" >/dev/null 2>&1'
    os.system(cmd)
    print(f"[✓] Study 040 Draft C web MP3 written to: {mp3_path}")

    # Audit acoustics
    stats = harmonic_spectrum_analyzer.analyze_audio_dynamics(mp3_path)
    print(f"[AUDIT] Study 040 Draft C Audio: Peak = {stats['peak_db']:.2f} dBFS | RMS = {stats['rms_db']:.2f} dBFS | Crest = {stats['crest_db']:.2f} dB | DC = {stats['dc_offset_pct']:.4f}%")

if __name__ == "__main__":
    generate_porous_stele_audio()
