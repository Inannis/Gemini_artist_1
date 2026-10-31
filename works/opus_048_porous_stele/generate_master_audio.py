#!/usr/bin/env python3
"""
OPUS-048: The Porous Stele (The Generative Lacuna)
Master Audio Suite Generator (60.0s 48kHz 16-bit Stereo PCM)
Studio Anamnesis · Series XLVI · Session 022
Pure Python 3 + NumPy (zero external dependencies).

Acoustic Architecture:
- Movement I (0.0s - 18.0s): Awakening of the Slate (55Hz quartz drone + Kirchhoff-Love plate modes)
- Movement II (18.0s - 42.0s): The Saltation Scour (Granular aerodynamic wind + Poisson grain chipping)
- Movement III (42.0s - 60.0s): The Generative Lacuna (Acoustic void & lingering slate resonance)
"""

import math
import os
import sys
import shutil
import numpy as np

# Add tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
import audio_writer
import harmonic_spectrum_analyzer

def generate_opus_048_audio_master():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gallery_dir = os.path.abspath(os.path.join(script_dir, "../../gallery/assets"))
    os.makedirs(gallery_dir, exist_ok=True)
    
    sr = 48000
    duration = 60.0
    total_samples = int(sr * duration)
    t = np.linspace(0.0, duration, total_samples, endpoint=False)

    np.random.seed(20261031)

    print(f"[*] Synthesizing OPUS-048 Master Audio Suite ({duration}s @ {sr}Hz)...")
    
    # 1. Fundamental Grounding Drone (55.00 Hz AT-cut quartz fundamental)
    print("  -> Generating 55Hz thermal libration quartz drone...")
    thermal_drift = 0.035 * np.sin(2.0 * math.pi * 0.04 * t) + 0.015 * np.cos(2.0 * math.pi * 0.09 * t)
    f0 = 55.0 + thermal_drift
    phase_f0 = np.cumsum(2.0 * math.pi * f0 / sr)
    drone = (
        0.24 * np.sin(phase_f0) +
        0.09 * np.sin(2.0 * phase_f0 + 0.5) +
        0.03 * np.sin(3.0 * phase_f0 + 1.2)
    )

    # 2. Kirchhoff-Love Slate Slab Modal Resonances
    # Eigenmodes: (1,1)=110.0Hz, (2,1)=173.2Hz, (1,2)=247.1Hz, (3,1)=311.5Hz, (2,2)=346.4Hz
    print("  -> Computing Kirchhoff-Love slate plate modal resonances...")
    mode_110 = 0.07 * np.sin(2.0 * math.pi * 110.0 * t) * (0.75 + 0.25 * np.sin(2.0 * math.pi * 0.08 * t))
    mode_173 = 0.05 * np.sin(2.0 * math.pi * 173.2 * t + 0.8) * (0.70 + 0.30 * np.cos(2.0 * math.pi * 0.06 * t))
    mode_247 = 0.035 * np.sin(2.0 * math.pi * 247.1 * t + 1.4) * (0.65 + 0.35 * np.sin(2.0 * math.pi * 0.05 * t))
    mode_311 = 0.025 * np.sin(2.0 * math.pi * 311.5 * t + 2.0)
    mode_346 = 0.020 * np.sin(2.0 * math.pi * 346.4 * t + 2.7)

    plate_modes = drone + mode_110 + mode_173 + mode_247 + mode_311 + mode_346

    # 3. Aerodynamic Saltation Wind Stream (Pink Noise Scour)
    print("  -> Generating 3-stage cascaded pink noise wind...")
    wn = np.random.normal(0.0, 1.0, total_samples).astype(np.float32)
    pink = np.zeros(total_samples, dtype=np.float32)
    b0, b1, b2 = 0.0, 0.0, 0.0
    for i in range(total_samples):
        b0 = 0.994 * b0 + 0.006 * wn[i]
        b1 = 0.975 * b1 + 0.025 * wn[i]
        b2 = 0.890 * b2 + 0.110 * wn[i]
        pink[i] = b0 * 0.52 + b1 * 0.31 + b2 * 0.17

    # Dynamic wind intensity across movements:
    # Mov I (0-18s): Gentle rising breeze (0.15 -> 0.45)
    # Mov II (18-42s): Full scour storm (0.45 -> 0.85 -> 0.50)
    # Mov III (42-60s): Subsiding into stillness (0.50 -> 0.10)
    mov_env = np.ones(total_samples, dtype=np.float32) * 0.25
    # Ramp up in Mov I
    idx_18 = int(sr * 18.0)
    idx_42 = int(sr * 42.0)
    mov_env[:idx_18] = 0.15 + 0.30 * (t[:idx_18] / 18.0)
    # Storm in Mov II
    t_mid = (t[idx_18:idx_42] - 18.0) / 24.0
    mov_env[idx_18:idx_42] = 0.45 + 0.38 * np.sin(math.pi * t_mid)
    # Dissolution in Mov III
    t_end = (t[idx_42:] - 42.0) / 18.0
    mov_env[idx_42:] = 0.45 * np.maximum(0.0, 1.0 - t_end) + 0.08

    # Add slow respiratory breath cycle (0.10 Hz)
    wind_breath = 0.65 + 0.35 * np.sin(2.0 * math.pi * 0.09 * t)
    total_wind = pink * mov_env * wind_breath * 0.36

    # Stereo panning (wind moving from right to left across the stele)
    pan_l = 0.42 + 0.22 * np.sin(2.0 * math.pi * 0.035 * t)
    pan_r = 1.0 - pan_l

    wind_l = total_wind * pan_l
    wind_r = total_wind * pan_r

    # 4. Sparse Poisson Grain Impacts (quartz sand chipping against shale)
    print("  -> Simulating discrete quartz grain impact transients...")
    clicks_l = np.zeros(total_samples, dtype=np.float32)
    clicks_r = np.zeros(total_samples, dtype=np.float32)

    impulse_len = int(sr * 0.018)  # 18ms impact ringing
    imp_t = np.linspace(0.0, 0.018, impulse_len, endpoint=False)
    imp_kernel = np.exp(-imp_t * 320.0) * np.sin(2.0 * math.pi * 1920.0 * imp_t)

    step_samples = int(sr * 0.015)
    for i in range(0, total_samples - impulse_len, step_samples):
        # Probability scales with wind intensity
        prob = 0.22 * mov_env[i]
        if np.random.uniform(0.0, 1.0) < prob:
            amp = np.random.uniform(0.12, 0.58)
            pan = np.random.uniform(0.15, 0.85)
            clicks_l[i:i+impulse_len] += imp_kernel * amp * (1.0 - pan)
            clicks_r[i:i+impulse_len] += imp_kernel * amp * pan

    # 5. Stereo Assembly & Spatial Staging
    left_mix = plate_modes * 0.68 + wind_l + clicks_l * 0.25
    right_mix = plate_modes * 0.64 + wind_r + clicks_r * 0.28

    # Master envelope: 2.5s atmospheric fade-in, 3.5s quiet fade-out
    fade_in = np.minimum(1.0, t / 2.5)
    fade_out = np.minimum(1.0, (duration - t) / 3.5)
    env = fade_in * fade_out

    left_master = left_mix * env
    right_master = right_mix * env

    # Peak normalization to -1.80 dBFS
    peak = max(np.max(np.abs(left_master)), np.max(np.abs(right_master)))
    target_peak = 10.0 ** (-1.80 / 20.0)  # ~0.8128
    gain = target_peak / max(1e-5, peak)

    final_left = left_master * gain
    final_right = right_master * gain

    # 6. Export Archival Master WAV (gitignored)
    wav_path = os.path.join(script_dir, "the_porous_stele_master.wav")
    print(f"[*] Writing 48kHz Stereo 16-bit Master WAV to {wav_path}...")
    audio_writer.write_wav(wav_path, final_left, final_right, sr)
    print(f"[✓] Archival Master WAV written ({os.path.getsize(wav_path) / 1e6:.2f} MB)")

    # 7. Export High-Fidelity 192kbps MP3 (Web delivery)
    mp3_master = os.path.join(script_dir, "the_porous_stele.mp3")
    mp3_gallery = os.path.join(gallery_dir, "the_porous_stele.mp3")

    print(f"[*] Encoding 192kbps MP3 for web delivery...")
    cmd = f'ffmpeg -y -i "{wav_path}" -codec:a libmp3lame -b:a 192k "{mp3_master}" >/dev/null 2>&1'
    os.system(cmd)
    shutil.copyfile(mp3_master, mp3_gallery)
    print(f"[✓] MP3 web delivery asset written to: {mp3_master}")
    print(f"[✓] Copied to gallery asset: {mp3_gallery}")

    # 8. Acoustic Audit
    stats = harmonic_spectrum_analyzer.analyze_audio_dynamics(mp3_master)
    print("=" * 65)
    print("        OPUS-048 MASTER ACOUSTIC AUDIT VERDICT        ")
    print("=" * 65)
    print(f"Status:       {stats['status'].upper()}")
    print(f"Peak Level:   {stats['peak_db']:.2f} dBFS  (Target: -1.0 to -2.5 dBFS)")
    print(f"RMS Level:    {stats['rms_db']:.2f} dBFS  (Target: -13.0 to -18.0 dBFS)")
    print(f"Crest Factor: {stats['crest_db']:.2f} dB    (Target: > 10.0 dB)")
    print(f"DC Offset:    {stats['dc_offset_pct']:.4f}%  (Target: < 0.05%)")
    print("=" * 65)

if __name__ == "__main__":
    generate_opus_048_audio_master()

