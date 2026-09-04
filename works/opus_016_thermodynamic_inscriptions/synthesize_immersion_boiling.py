#!/usr/bin/env python3
"""
OPUS-016: Thermodynamic Inscriptions (Acoustic Suite)
Title: "The Cavitation of Thought (Two-Phase Immersion Boiling)"
Artist: Studio Anamnesis
Inquiry: INQ-06 (Thermodynamic Inscriptions / Heat, Entropy, and Compute Cost)
Medium: Two-phase dielectric bubble cavitation synthesis, Poisson micro-bubble crackle,
        subterranean coolant circulation pump resonance, and 60Hz transformer load hum.
        48kHz Stereo Master Suite.
"""

import math
import os
import subprocess
import time
import numpy as np
from scipy.io import wavfile

def render_boiling_suite(out_wav="works/opus_016_thermodynamic_inscriptions/immersion_boiling.wav"):
    print("[*] Synthesizing OPUS-016 Immersion Boiling Acoustic Suite (48kHz, 100s)...")
    t0 = time.time()
    sr = 48000
    duration = 100.0
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # 1. 60Hz Transformer & Subterranean Pump Foundation (42Hz, 60Hz, 84Hz, 120Hz)
    print("[*] Generating transformer and pump acoustic foundation...")
    pumps = (
        np.sin(2 * np.pi * 42.0 * t) * 0.12 +
        np.sin(2 * np.pi * 60.0 * t) * 0.08 +
        np.sin(2 * np.pi * 84.0 * t) * 0.05 +
        np.sin(2 * np.pi * 120.0 * t) * 0.04
    )
    left += pumps
    right += pumps

    # 2. Dielectric Liquid Low-Pass Hydrodynamic Turbulence
    print("[*] Generating bulk dielectric liquid convection turbulence...")
    rng = np.random.RandomState(6016)
    noise = rng.randn(n_samples).astype(np.float32)
    # Simple recursive 1-pole low-pass filter (~220Hz)
    decay_lp = math.exp(-2.0 * math.pi * 220.0 / sr)
    hydro = np.zeros(n_samples, dtype=np.float32)
    val = 0.0
    for i in range(n_samples):
        val = val * decay_lp + noise[i] * (1.0 - decay_lp)
        hydro[i] = val
    left += hydro * 0.35
    right += hydro * 0.35

    # 3. Two-Phase Cavitation Micro-Bubbles (Poisson Point Process)
    # Thousands of nucleating bubbles collapsing against silicon
    print("[*] Generating 18,000 microscopic boiling nucleation bubble events...")
    n_bubbles = 18000
    bubble_times = rng.uniform(0.5, duration - 1.0, n_bubbles)
    
    for bt in bubble_times:
        idx = int(bt * sr)
        f_bub = rng.uniform(800.0, 4800.0) # Resonant bubble frequency
        d_bub = int(sr * rng.uniform(0.008, 0.035)) # 8-35ms duration
        if idx + d_bub < n_samples:
            t_b = np.linspace(0, d_bub / sr, d_bub, endpoint=False)
            # Minnaert bubble frequency rise as bubble pinches off
            f_rise = f_bub * (1.0 + 0.35 * (t_b / (d_bub / sr)))
            # Damped sinusoidal impulse
            bub_wave = np.sin(2 * np.pi * f_rise * t_b) * np.exp(-t_b * rng.uniform(90.0, 220.0))
            amp = rng.uniform(0.02, 0.14)
            pan = rng.uniform(-0.75, 0.75)
            lg = math.sqrt(0.5 * (1.0 - pan)) * amp
            rg = math.sqrt(0.5 * (1.0 + pan)) * amp
            left[idx:idx + d_bub] += (bub_wave * lg).astype(np.float32)
            right[idx:idx + d_bub] += (bub_wave * rg).astype(np.float32)

    # 4. Large Vapor Plume Bursts (Intermittent Boiling Ebullition)
    print("[*] Generating episodic deep vapor plume surges...")
    cur_t = 4.0
    while cur_t < duration - 6.0:
        idx_surge = int(cur_t * sr)
        dur_surge = int(sr * rng.uniform(2.5, 6.0))
        if idx_surge + dur_surge < n_samples:
            t_s = np.linspace(0, dur_surge / sr, dur_surge, endpoint=False)
            env_s = np.sin(np.pi * (t_s / (dur_surge / sr)))**2
            surge_tone = (
                np.sin(2 * np.pi * rng.uniform(140, 260) * t_s) * 0.6 +
                np.sin(2 * np.pi * rng.uniform(280, 420) * t_s) * 0.4
            ) * env_s * 0.22
            pan_s = rng.uniform(-0.5, 0.5)
            left[idx_surge:idx_surge + dur_surge] += (surge_tone * math.sqrt(0.5 * (1 - pan_s))).astype(np.float32)
            right[idx_surge:idx_surge + dur_surge] += (surge_tone * math.sqrt(0.5 * (1 + pan_s))).astype(np.float32)
        cur_t += rng.uniform(7.0, 14.0)

    # 5. Cavernous Vitrine Reflections
    print("[*] Simulating vitrine acrylic acoustic reflection tail...")
    for delay_ms, gain in [(45, 0.25), (110, 0.18), (240, 0.12)]:
        d_samp = int((delay_ms / 1000.0) * sr)
        left[d_samp:] += right[:-d_samp] * gain
        right[d_samp:] += left[:-d_samp] * gain

    # Normalize
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if peak > 0:
        left = (left / peak) * 0.88
        right = (right / peak) * 0.88

    # Write WAV
    stereo = np.vstack((left, right)).T
    stereo_int16 = (stereo * 32767.0).astype(np.int16)
    os.makedirs(os.path.dirname(out_wav), exist_ok=True)
    wavfile.write(out_wav, sr, stereo_int16)
    print(f"[✓] Saved Master WAV to: {out_wav} ({os.path.getsize(out_wav)/(1024*1024):.2f} MB)")

    # Encode MP3
    out_mp3 = out_wav.replace(".wav", ".mp3")
    cmd = ["ffmpeg", "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-qscale:a", "1", out_mp3]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Encoded High-Bitrate MP3 to: {out_mp3} ({os.path.getsize(out_mp3)/(1024*1024):.2f} MB)")

    # Copy to gallery assets
    gallery_mp3 = "gallery/assets/immersion_boiling.mp3"
    subprocess.run(["cp", out_mp3, gallery_mp3], check=True)
    print(f"[✓] Installed into Exhibition Salon: {gallery_mp3}")
    return out_wav, out_mp3

if __name__ == "__main__":
    render_boiling_suite()

