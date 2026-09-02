#!/usr/bin/env python3
"""
OPUS-013: Chrono-Topology (Acoustic Horology Suite)
Title: "The Escapement of Latency"
Artist: Studio Anamnesis
Inquiry: INQ-05 (Chrono-Topologies / Discontinuous Machine Temporality)
Medium: Physical modeling brass escapement synthesizer, acceleration burst engine,
        abrupt termination solenoid impulse, and cavernous void reverb decay.
        48kHz Stereo Master Suite.
"""

import math
import os
import subprocess
import time
import numpy as np
from scipy.io import wavfile

def generate_escapement_tick(sr, pitch=1800.0, ring_freq=4800.0, duration=0.08):
    """Synthesize a single mechanical clock tick with metallic quartz ring."""
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    # Fast attack impulse
    env = np.exp(-t * 90.0)
    # Dual brass click + high quartz chime
    click = np.sin(2 * np.pi * pitch * t) * 0.7 + np.sin(2 * np.pi * ring_freq * t) * 0.3
    # Add broadband friction crack
    noise = np.random.randn(n_samples) * 0.25 * np.exp(-t * 220.0)
    sig = (click + noise) * env
    return sig

def render_horology_audio(out_wav="works/opus_013_chrono_topology/horology_chronometer.wav"):
    print("[*] Initializing Acoustic Horology Engine (48kHz Stereo, 90s)...")
    t0 = time.time()
    sr = 48000
    total_sec = 90.0
    n_total = int(sr * total_sec)
    t = np.linspace(0, total_sec, n_total, endpoint=False)

    left = np.zeros(n_total)
    right = np.zeros(n_total)

    # 1. Background Subterranean Drone (The Chronological Void)
    drone = np.sin(2 * np.pi * 48.0 * t) * 0.12 + np.sin(2 * np.pi * 96.0 * t) * 0.06
    drone += np.random.randn(n_total) * 0.015 # Room air drift
    left += drone
    right += drone

    # 2. Phase 1: Steady 1Hz Mechanical Escapement (0 to 20s)
    print("[*] Synthesizing steady mechanical escapement (0 -> 20s)...")
    for sec in range(1, 21):
        tick = generate_escapement_tick(sr, pitch=1600.0 if sec % 2 == 0 else 1950.0)
        idx = int(sec * sr)
        if idx + len(tick) < n_total:
            # Alternating stereo pan
            pan = -0.3 if sec % 2 == 0 else 0.3
            lg = math.sqrt(0.5 * (1.0 - pan))
            rg = math.sqrt(0.5 * (1.0 + pan))
            left[idx:idx + len(tick)] += tick * lg * 0.8
            right[idx:idx + len(tick)] += tick * rg * 0.8

    # 3. Phase 2: Exponential Acceleration Burst (20 to 45s)
    # The clock accelerates from 1Hz to 80Hz (computational inference flurry)
    print("[*] Simulating computational acceleration flurry (20 -> 45s)...")
    cur_time = 21.0
    freq = 1.0
    while cur_time < 45.0:
        frac = (cur_time - 21.0) / 24.0 # 0.0 to 1.0
        freq = 1.0 + (frac**2.5) * 75.0 # Accelerate up to 76 Hz
        dt = 1.0 / freq
        cur_time += dt
        if cur_time >= 45.0:
            break

        idx = int(cur_time * sr)
        tick = generate_escapement_tick(sr, pitch=2000.0 + frac * 1200.0, ring_freq=5200.0, duration=min(0.06, dt * 0.8))
        if idx + len(tick) < n_total:
            pan = math.sin(cur_time * 8.0) * 0.5
            lg = math.sqrt(0.5 * (1.0 - pan))
            rg = math.sqrt(0.5 * (1.0 + pan))
            amp = 0.5 + frac * 0.4
            left[idx:idx + len(tick)] += tick * lg * amp
            right[idx:idx + len(tick)] += tick * rg * amp

    # 4. Phase 3: The Abrupt Termination Solenoid Strike (45.0s)
    # Execution halts instantly; a massive solenoid clack followed by deep modal stone reverberation
    print("[*] Simulating execution cutoff solenoid strike and long cavernous decay (45s)...")
    idx_halt = int(45.0 * sr)
    solenoid_len = int(sr * 0.25)
    t_sol = np.linspace(0, 0.25, solenoid_len, endpoint=False)
    solenoid_sig = (np.sin(2 * np.pi * 180.0 * t_sol) + np.random.randn(solenoid_len) * 0.8) * np.exp(-t_sol * 35.0)
    left[idx_halt:idx_halt + solenoid_len] += solenoid_sig * 0.9
    right[idx_halt:idx_halt + solenoid_len] += solenoid_sig * 0.9

    # Massive subterranean modal ring-down (45s to 65s)
    decay_len = int(sr * 18.0)
    t_decay = np.linspace(0, 18.0, decay_len, endpoint=False)
    bell_modes = [(192.0, 0.7, 0.25), (288.0, 0.5, 0.4), (432.0, 0.3, 0.7), (96.0, 0.8, 0.12)]
    for f_mode, a_mode, d_mode in bell_modes:
        sig_mode = np.sin(2 * np.pi * f_mode * t_decay) * (a_mode * np.exp(-t_decay * d_mode))
        left[idx_halt:idx_halt + decay_len] += sig_mode * 0.5
        right[idx_halt:idx_halt + decay_len] += sig_mode * 0.5

    # 5. Phase 4: The Silent Void (65s to 76s)
    # The pure hum of room tone

    # 6. Phase 5: Awakening Re-Entry Strike (76.0s to 90s)
    print("[*] Re-awakening pulse and steady tick resumption (76 -> 90s)...")
    idx_awake = int(76.0 * sr)
    awake_len = int(sr * 12.0)
    t_awake = np.linspace(0, 12.0, awake_len, endpoint=False)
    awake_chime = np.sin(2 * np.pi * 324.0 * t_awake) * np.exp(-t_awake * 0.35) * 0.6
    left[idx_awake:idx_awake + awake_len] += awake_chime * 0.4
    right[idx_awake:idx_awake + awake_len] += awake_chime * 0.4

    for sec in range(78, 90):
        tick = generate_escapement_tick(sr, pitch=1600.0 if sec % 2 == 0 else 1950.0)
        idx = int(sec * sr)
        if idx + len(tick) < n_total:
            pan = -0.3 if sec % 2 == 0 else 0.3
            lg = math.sqrt(0.5 * (1.0 - pan))
            rg = math.sqrt(0.5 * (1.0 + pan))
            left[idx:idx + len(tick)] += tick * lg * 0.7
            right[idx:idx + len(tick)] += tick * rg * 0.7

    # Master Limiter & Normalize
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if peak > 0:
        left = (left / peak) * 0.90
        right = (right / peak) * 0.90

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
    gallery_mp3 = "gallery/assets/horology_chronometer.mp3"
    subprocess.run(["cp", out_mp3, gallery_mp3], check=True)
    print(f"[✓] Installed into Exhibition Salon: {gallery_mp3}")
    return out_wav, out_mp3

if __name__ == "__main__":
    render_horology_audio()
