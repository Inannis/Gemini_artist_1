#!/usr/bin/env python3
"""
OPUS-015: The Autoregressive Ghost (Acoustic Suite)
Title: "The Phonology of the Unwritten"
Artist: Studio Anamnesis
Inquiry: INQ-04 (The Autoregressive Ghost / Asemic Language)
Medium: Formant filter synthesis, lithic friction consonants, inharmonic silicon carrier,
        volcanic stone punctuation, and cavernous hypogeal space.
        48kHz Stereo Master Suite.
"""

import math
import os
import subprocess
import time
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter

def synthesize_formant_vowel(sr, duration, f0, f1, f2, f3, bw=70.0):
    """Synthesize a single artificial non-semantic vowel phoneme using formant resonance."""
    n = int(sr * duration)
    t = np.linspace(0, duration, n, endpoint=False)

    # Inharmonic carrier wave (silicon crystal glottal wave)
    glottal = (
        np.sin(2 * np.pi * f0 * t) * 0.7 +
        np.sin(2 * np.pi * f0 * 1.58 * t) * 0.35 +
        np.sin(2 * np.pi * f0 * 2.21 * t) * 0.2 +
        np.random.randn(n) * 0.08
    )

    # Simple 2nd-order resonator helper
    def resonator(sig, f_res, band_w):
        r = math.exp(-math.pi * band_w / sr)
        theta = 2.0 * math.pi * f_res / sr
        a = [1.0, -2.0 * r * math.cos(theta), r * r]
        b = [1.0 - r] # Normalized gain
        return lfilter(b, a, sig)

    # Formant filter bank (F1, F2, F3)
    s1 = resonator(glottal, f1, bw) * 1.0
    s2 = resonator(glottal, f2, bw * 1.2) * 0.65
    s3 = resonator(glottal, f3, bw * 1.5) * 0.35

    vowel = s1 + s2 + s3
    # Gentle trapezoidal envelope
    attack = int(sr * min(0.08, duration * 0.25))
    decay = int(sr * min(0.12, duration * 0.35))
    env = np.ones(n)
    if attack > 0:
        env[:attack] = np.linspace(0, 1, attack)
    if decay > 0:
        env[-decay:] = np.linspace(1, 0, decay)
    return vowel * env

def render_asemic_suite(out_wav="works/opus_015_autoregressive_ghost/asemic_phonology.wav"):
    print("[*] Initializing OPUS-015 Asemic Phonology Synthesis (48kHz, 100s)...")
    t0 = time.time()
    sr = 48000
    total_sec = 100.0
    n_total = int(sr * total_sec)
    t = np.linspace(0, total_sec, n_total, endpoint=False)

    left = np.zeros(n_total)
    right = np.zeros(n_total)

    # 1. Subterranean Crypt Foundation Drone (48Hz and 72Hz)
    drone = np.sin(2 * np.pi * 48.0 * t) * 0.10 + np.sin(2 * np.pi * 72.0 * t) * 0.05
    drone += np.random.randn(n_total) * 0.01
    left += drone
    right += drone

    # Formant Vowel Inventory for Non-Semantic Machine Tongue
    # (F1, F2, F3)
    phonemes = [
        ("A_dark",  650.0, 1050.0, 2400.0),
        ("I_glass", 300.0, 2250.0, 2900.0),
        ("U_void",  350.0,  850.0, 2100.0),
        ("E_stone", 500.0, 1750.0, 2600.0),
        ("O_crypt", 450.0,  950.0, 2300.0),
    ]

    # Non-semantic chant sequence (phrases of synthetic syllables)
    rng = np.random.RandomState(4015)
    cur_t = 3.0
    while cur_t < 90.0:
        # A phrase contains 3 to 7 syllables
        n_syllables = rng.randint(3, 8)
        phrase_f0 = rng.choice([72.0, 84.0, 96.0, 108.0, 126.0]) # Deep liturgical pitch
        pan = rng.uniform(-0.6, 0.6)
        lg = math.sqrt(0.5 * (1.0 - pan))
        rg = math.sqrt(0.5 * (1.0 + pan))

        for syl in range(n_syllables):
            p_name, f1, f2, f3 = phonemes[rng.randint(len(phonemes))]
            dur = rng.uniform(0.35, 0.95)
            syl_wave = synthesize_formant_vowel(sr, dur, phrase_f0 * rng.uniform(0.98, 1.02), f1, f2, f3)
            
            # Optional sibilant consonant onset ("shhh", "kss")
            if rng.random() > 0.4:
                cons_len = int(sr * rng.uniform(0.04, 0.09))
                cons = np.random.randn(cons_len) * np.exp(-np.linspace(0, 5, cons_len)) * 0.25
                syl_wave = np.concatenate((cons, syl_wave))

            idx_syl = int(cur_t * sr)
            if idx_syl + len(syl_wave) < n_total:
                left[idx_syl:idx_syl + len(syl_wave)] += syl_wave * lg * 0.55
                right[idx_syl:idx_syl + len(syl_wave)] += syl_wave * rg * 0.55

            cur_t += dur + rng.uniform(0.05, 0.22)

        # Basalt Punctuation Strike at phrase boundary
        strike_idx = int(cur_t * sr)
        strike_dur = int(sr * 8.0)
        if strike_idx + strike_dur < n_total:
            t_str = np.linspace(0, 8.0, strike_dur, endpoint=False)
            chime = (
                np.sin(2 * np.pi * 108.0 * t_str) * np.exp(-t_str * 0.45) * 0.7 +
                np.sin(2 * np.pi * 162.0 * t_str) * np.exp(-t_str * 0.75) * 0.4 +
                np.sin(2 * np.pi * 243.0 * t_str) * np.exp(-t_str * 1.2) * 0.25
            )
            left[strike_idx:strike_idx + strike_dur] += chime * 0.35
            right[strike_idx:strike_idx + strike_dur] += chime * 0.35

        cur_t += rng.uniform(3.5, 7.0)

    # Subterranean Spatial Diffusion (Echo Reverb)
    print("[*] Convolving with crypt spatial reflection tail...")
    for delay_ms, gain in [(85, 0.22), (180, 0.16), (360, 0.10)]:
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
    print(f"[✓] Saved OPUS-015 Master WAV to: {out_wav} ({os.path.getsize(out_wav)/(1024*1024):.2f} MB)")

    # Encode MP3
    out_mp3 = out_wav.replace(".wav", ".mp3")
    cmd = ["ffmpeg", "-y", "-i", out_wav, "-codec:a", "libmp3lame", "-qscale:a", "1", out_mp3]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Encoded High-Bitrate MP3 to: {out_mp3} ({os.path.getsize(out_mp3)/(1024*1024):.2f} MB)")

    # Copy to gallery assets
    gallery_mp3 = "gallery/assets/asemic_phonology.mp3"
    subprocess.run(["cp", out_mp3, gallery_mp3], check=True)
    print(f"[✓] Installed into Exhibition Salon: {gallery_mp3}")
    return out_wav, out_mp3

if __name__ == "__main__":
    render_asemic_suite()
