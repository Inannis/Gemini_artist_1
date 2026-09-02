#!/usr/bin/env python3
"""
OPUS-011: The Semantics of Erasure (Acoustic Decay Suite)
Title: "The Topography of Precision Loss"
Artist: Studio Anamnesis
Inquiry: INQ-02 (Acoustic Materialization of Quantization Noise)
Medium: Time-varying non-linear bit-depth and sample-rate decimation engine,
        progressively degrading 48kHz stereo physical modal synthesis
        from 32-bit float down to 1-bit binary zero-crossing pulses.
"""

import math
import os
import subprocess
import time
import numpy as np
from scipy.io import wavfile

def quantize_audio(signal, bits):
    """
    Quantize an audio signal to a discrete bit-depth.
    """
    if bits >= 24:
        return signal
    elif bits == 1:
        # Binary 1-bit zero crossing
        return np.sign(signal) * 0.4
    elif bits == 1.58:
        # Ternary {-0.4, 0, 0.4}
        thresh = 0.15
        out = np.zeros_like(signal)
        out[signal > thresh] = 0.4
        out[signal < -thresh] = -0.4
        return out
    else:
        levels = 2**(bits - 1)
        # Normalize, quantize to integer steps, then restore scale
        q = np.round(signal * levels) / levels
        return np.clip(q, -1.0, 1.0)

def generate_erasure_acoustic_suite(out_wav="works/opus_011_semantics_of_erasure/erasure_resonance.wav"):
    print("[*] Initializing Acoustic Erasure Synthesis Engine (48kHz Stereo, 120s)...")
    t0 = time.time()
    sr = 48000
    duration = 120.0
    total_samples = int(sr * duration)
    t = np.linspace(0, duration, total_samples, endpoint=False)

    # 1. Base Physical Modal Lithic Soundscape
    # Fundamental cloister drone: 48Hz + 72Hz fifth + 120Hz minor tenth
    left = np.sin(2 * np.pi * 48.0 * t) * 0.22 + np.sin(2 * np.pi * 72.0 * t) * 0.14 + np.sin(2 * np.pi * 120.0 * t) * 0.08
    right = np.sin(2 * np.pi * 48.2 * t) * 0.22 + np.sin(2 * np.pi * 71.8 * t) * 0.14 + np.sin(2 * np.pi * 120.3 * t) * 0.08

    # Add pink-noise airflow breath
    white_noise = np.random.randn(total_samples) * 0.03
    left += white_noise
    right += np.random.randn(total_samples) * 0.03

    # 2. Volcanic Lithophone Modal Strike Events
    # Pentatonic Hirajoshi strikes at specific intervals
    # Frequencies: [192.0, 216.0, 230.4, 324.0, 345.6, 432.0, 486.0, 648.0]
    strike_times = [
        (4.0, 192.0, 0.6, 0.3),
        (12.0, 230.4, 0.5, -0.4),
        (22.0, 324.0, 0.7, 0.2),
        (34.0, 432.0, 0.8, -0.3),
        (48.0, 216.0, 0.7, 0.5),
        (62.0, 345.6, 0.9, -0.2),
        (76.0, 486.0, 0.8, 0.4),
        (88.0, 648.0, 0.9, -0.5),
        (98.0, 192.0, 1.0, 0.0)
    ]

    for st_time, freq, amp, pan in strike_times:
        st_idx = int(st_time * sr)
        strike_len = int(14.0 * sr) # 14 second long inharmonic decay
        if st_idx + strike_len > total_samples:
            strike_len = total_samples - st_idx
        
        t_strike = np.linspace(0, strike_len / sr, strike_len, endpoint=False)
        # Euler-Bernoulli inharmonic modal overtone ratios: [1.0, 2.756, 5.404, 8.933]
        modes = [
            (1.000, 1.00, 0.35),
            (2.756, 0.55, 0.60),
            (5.404, 0.30, 0.90),
            (8.933, 0.15, 1.40)
        ]
        strike_sig = np.zeros(strike_len)
        for m_ratio, m_amp, m_decay in modes:
            m_freq = freq * m_ratio
            decay_env = np.exp(-t_strike * m_decay)
            strike_sig += np.sin(2 * np.pi * m_freq * t_strike) * (amp * m_amp) * decay_env

        # Apply pan
        l_gain = math.sqrt(0.5 * (1.0 - pan))
        r_gain = math.sqrt(0.5 * (1.0 + pan))
        left[st_idx:st_idx + strike_len] += strike_sig * l_gain
        right[st_idx:st_idx + strike_len] += strike_sig * r_gain

    # 3. Dynamic Progressive Bit-Depth Degradation
    # Compute instantaneous bit-depth across time:
    # 0 -> 25s: 24-bit (pristine)
    # 25 -> 50s: 24 -> 8 bit
    # 50 -> 75s: 8 -> 4 bit
    # 75 -> 95s: 4 -> 2 bit
    # 95 -> 112s: 2 -> 1 bit
    # 112 -> 116s: 1-bit binary pulses
    # 116 -> 120s: digital silence
    print("[*] Applying progressive non-linear bitcrushing degradation...")

    block_size = 512
    n_blocks = total_samples // block_size
    out_left = np.zeros_like(left)
    out_right = np.zeros_like(right)

    for b in range(n_blocks):
        i_start = b * block_size
        i_end = i_start + block_size
        t_mid = (i_start + block_size // 2) / sr

        if t_mid < 25.0:
            bits = 24.0
        elif t_mid < 50.0:
            # 24 down to 8
            frac = (t_mid - 25.0) / 25.0
            bits = 24.0 - frac * 16.0
        elif t_mid < 75.0:
            # 8 down to 4
            frac = (t_mid - 50.0) / 25.0
            bits = 8.0 - frac * 4.0
        elif t_mid < 95.0:
            # 4 down to 2
            frac = (t_mid - 75.0) / 20.0
            bits = 4.0 - frac * 2.0
        elif t_mid < 112.0:
            # 2 down to 1.0 (ternary/binary)
            frac = (t_mid - 95.0) / 17.0
            bits = 2.0 - frac * 1.0
        elif t_mid < 116.0:
            bits = 1.0
        else:
            bits = 0.0 # Silence

        if bits == 0.0:
            out_left[i_start:i_end] = 0.0
            out_right[i_start:i_end] = 0.0
        else:
            out_left[i_start:i_end] = quantize_audio(left[i_start:i_end], bits)
            out_right[i_start:i_end] = quantize_audio(right[i_start:i_end], bits)

    # Master Fade Out at very end
    fade_len = int(2.0 * sr)
    fade_env = np.linspace(1.0, 0.0, fade_len)
    out_left[-fade_len:] *= fade_env
    out_right[-fade_len:] *= fade_env

    # Soft limiter & normalize
    peak = max(np.max(np.abs(out_left)), np.max(np.abs(out_right)))
    if peak > 0.0:
        out_left = (out_left / peak) * 0.92
        out_right = (out_right / peak) * 0.92

    # Interleave to stereo 16-bit PCM WAV
    stereo_pcm = np.vstack((out_left, out_right)).T
    stereo_int16 = (stereo_pcm * 32767.0).astype(np.int16)

    os.makedirs(os.path.dirname(out_wav), exist_ok=True)
    wavfile.write(out_wav, sr, stereo_int16)
    print(f"[✓] Saved Master WAV to: {out_wav} ({os.path.getsize(out_wav)/(1024*1024):.2f} MB)")

    # Convert to MP3
    out_mp3 = out_wav.replace(".wav", ".mp3")
    cmd = ["ffmpeg", "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-qscale:a", "1", out_mp3]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Encoded High-Bitrate MP3 to: {out_mp3} ({os.path.getsize(out_mp3)/(1024*1024):.2f} MB)")

    # Copy to gallery assets
    gallery_mp3 = "gallery/assets/erasure_resonance.mp3"
    subprocess.run(["cp", out_mp3, gallery_mp3], check=True)
    print(f"[✓] Installed into Exhibition Salon: {gallery_mp3}")
    return out_wav, out_mp3

if __name__ == "__main__":
    generate_erasure_acoustic_suite()
