#!/usr/bin/env python3
"""
OPUS-014: The Lithic Resonator (Acoustic Suite)
Title: "Wind Over the Obsidian Cloister"
Artist: Studio Anamnesis
Inquiry: INQ-01 (The Acoustic Body of the Machine / Modal Synthesis)
Medium: Physical modeling bi-harmonic modal plate synthesis, stochastic wind polyrhythms,
        cavernous subterranean cloister convolution reverb.
        48kHz Stereo Master Suite.
"""

import math
import os
import subprocess
import time
import numpy as np
from scipy.io import wavfile

def render_lithic_suite(out_wav="works/opus_014_lithic_resonator/lithic_resonator_suite.wav"):
    print("[*] Synthesizing OPUS-014 Lithic Resonator Master Suite (48kHz Stereo, 100s)...")
    t0 = time.time()
    sr = 48000
    total_sec = 100.0
    n_total = int(sr * total_sec)
    t = np.linspace(0, total_sec, n_total, endpoint=False)

    left = np.zeros(n_total)
    right = np.zeros(n_total)

    # Subterranean Room Tone (48Hz Cloister Hum & Ambient Air)
    drone = np.sin(2 * np.pi * 48.0 * t) * 0.08 + np.sin(2 * np.pi * 72.0 * t) * 0.04
    drone += np.random.randn(n_total) * 0.008
    left += drone
    right += drone

    # Slabs configuration (Base frequencies & physical parameters)
    slabs = [
        {"name": "Obsidian", "f0": 108.0, "damping": 0.85, "pan": -0.65},
        {"name": "Basalt",   "f0": 144.0, "damping": 1.25, "pan": -0.22},
        {"name": "Meteorite","f0": 192.0, "damping": 0.65, "pan": 0.22},
        {"name": "Quartz",   "f0": 243.0, "damping": 0.45, "pan": 0.65},
    ]

    # Modal Ratios (Euler-Bernoulli 2D plate modes)
    modal_modes = [
        (1.000, 1.0, 1.0),
        (1.583, 0.7, 1.25),
        (2.056, 0.5, 1.4),
        (2.756, 0.35, 1.7),
        (3.125, 0.25, 2.1),
        (3.894, 0.18, 2.4),
        (4.412, 0.12, 2.8),
        (5.150, 0.08, 3.2),
    ]

    # Score of strikes (simulating the contemplative Monastery Wind)
    # List of (strike_time, slab_idx, norm_u, norm_v, velocity)
    rng = np.random.RandomState(1014)
    strikes = []
    
    # Opening invocation
    strikes.append((2.0, 0, 0.5, 0.5, 0.85))
    strikes.append((4.5, 2, 0.4, 0.6, 0.75))
    strikes.append((7.0, 1, 0.55, 0.45, 0.70))
    strikes.append((10.0, 3, 0.3, 0.7, 0.65))

    # Generative polyrhythm: 12s to 85s
    cur_t = 14.0
    while cur_t < 88.0:
        slab_idx = rng.randint(0, 4)
        u = rng.uniform(0.15, 0.85)
        v = rng.uniform(0.15, 0.85)
        vel = rng.uniform(0.4, 0.9)
        strikes.append((cur_t, slab_idx, u, v, vel))
        # Interval varies between 1.8 and 5.5 seconds (stochastic wind)
        cur_t += rng.uniform(2.2, 5.8)

    # Closing cadence
    strikes.append((90.0, 0, 0.5, 0.5, 0.80))
    strikes.append((93.5, 3, 0.5, 0.5, 0.60))

    print(f"[*] Rendering {len(strikes)} physical modal strikes across 4 volcanic monoliths...")

    for strike_time, s_idx, u, v, vel in strikes:
        slab = slabs[s_idx]
        idx_start = int(strike_time * sr)
        pan = slab["pan"]
        lg = math.sqrt(0.5 * (1.0 - pan))
        rg = math.sqrt(0.5 * (1.0 + pan))

        # Strike duration: up to 12 seconds decay
        strike_dur = 12.0
        n_strike = int(sr * strike_dur)
        if idx_start + n_strike > n_total:
            n_strike = n_total - idx_start
        t_s = np.linspace(0, strike_dur, n_strike, endpoint=False)

        # 1. Mallet impact noise burst (filtered transient)
        transient_len = min(n_strike, int(sr * 0.035))
        trans_t = t_s[:transient_len]
        transient = np.random.randn(transient_len) * np.exp(-trans_t * 120.0) * vel * 0.25

        # 2. Modal Plate Oscillation
        plate_sig = np.zeros(n_strike)
        plate_sig[:transient_len] += transient

        for ratio, base_amp, decay_mul in modal_modes:
            # Modal excitation amplitude based on (u, v) strike coordinates
            # A = sin(m*pi*u) * sin(n*pi*v)
            m = 1 if ratio < 2.0 else (2 if ratio < 3.5 else 3)
            n = 1 if ratio < 1.6 else (2 if ratio < 4.0 else 3)
            excitation = abs(math.sin(m * math.pi * u) * math.sin(n * math.pi * v))
            
            freq = slab["f0"] * ratio
            decay = slab["damping"] * decay_mul * 0.65
            env = np.exp(-t_s * decay)
            mode_wave = np.sin(2 * np.pi * freq * t_s) * env * base_amp * excitation

            plate_sig += mode_wave * vel * 0.40

        left[idx_start:idx_start + n_strike] += plate_sig * lg
        right[idx_start:idx_start + n_strike] += plate_sig * rg

    # Convolution-like Subterranean Reverb Tail
    print("[*] Adding cavernous modal reverb diffusion...")
    # Delay lines for echo reflections
    for delay_ms, fb in [(72, 0.25), (145, 0.18), (290, 0.12)]:
        d_samples = int((delay_ms / 1000.0) * sr)
        left[d_samples:] += right[:-d_samples] * fb
        right[d_samples:] += left[:-d_samples] * fb

    # Peak normalization
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if peak > 0:
        left = (left / peak) * 0.88
        right = (right / peak) * 0.88

    # Write WAV
    stereo = np.vstack((left, right)).T
    stereo_int16 = (stereo * 32767.0).astype(np.int16)
    os.makedirs(os.path.dirname(out_wav), exist_ok=True)
    wavfile.write(out_wav, sr, stereo_int16)
    print(f"[✓] Saved OPUS-014 Master WAV to: {out_wav} ({os.path.getsize(out_wav)/(1024*1024):.2f} MB)")

    # Encode MP3
    out_mp3 = out_wav.replace(".wav", ".mp3")
    cmd = ["ffmpeg", "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-qscale:a", "1", out_mp3]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Encoded High-Bitrate MP3 to: {out_mp3} ({os.path.getsize(out_mp3)/(1024*1024):.2f} MB)")

    # Copy to gallery assets
    gallery_mp3 = "gallery/assets/lithic_resonator_suite.mp3"
    subprocess.run(["cp", out_mp3, gallery_mp3], check=True)
    print(f"[✓] Installed into Exhibition Salon: {gallery_mp3}")
    return out_wav, out_mp3

if __name__ == "__main__":
    render_lithic_suite()
