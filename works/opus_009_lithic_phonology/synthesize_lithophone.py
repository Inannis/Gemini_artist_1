#!/usr/bin/env python3
"""
OPUS-009: Lithic Phonology (Modal Acoustic Synthesis of Resonant Stone)
Artist: Studio Anamnesis
Medium: Euler-Bernoulli modal synthesis of volcanic obsidian & basalt slabs, 48kHz stereo master.
"""

import math
import os
import struct
import subprocess
import time
import wave
import numpy as np

def synthesize_modal_strike(fundamental_freq, duration, sample_rate, pan=0.5):
    """Synthesizes an inharmonic strike on a suspended stone slab with Euler-Bernoulli modal ratios."""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False, dtype=np.float32)

    # Inharmonic modal ratios for free-free elastic bar/plate: [1.0, 2.756, 5.404, 8.933, 13.34]
    mode_ratios = [1.0, 2.756, 5.404, 8.933, 13.34]
    mode_amps   = [0.65, 0.40,  0.25,  0.15,  0.08]
    # Higher modes decay much faster in stone
    decay_rates = [1.8,  3.5,   6.2,   11.0,  18.0]

    strike_signal = np.zeros(num_samples, dtype=np.float32)
    for freq_ratio, amp, decay in zip(mode_ratios, mode_amps, decay_rates):
        freq = fundamental_freq * freq_ratio
        if freq < sample_rate * 0.48:  # Nyquist safety
            envelope = amp * np.exp(-decay * t)
            strike_signal += envelope * np.sin(2.0 * np.pi * freq * t)

    # Initial transient mallet impact click (filtered noise pulse)
    transient_len = int(0.008 * sample_rate)
    noise_click = np.random.normal(0, 0.35, transient_len).astype(np.float32) * np.linspace(1, 0, transient_len)
    strike_signal[:transient_len] += noise_click

    # Stereo pan
    left_gain = math.cos(pan * math.pi * 0.5)
    right_gain = math.sin(pan * math.pi * 0.5)

    return strike_signal * left_gain, strike_signal * right_gain

def synthesize_lithophone_suite(output_wav="lithic_resonance.wav", output_mp3="lithic_resonance.mp3", total_duration=120.0, sample_rate=48000):
    print(f"[*] Synthesizing Lithic Phonology Suite ({total_duration}s @ {sample_rate}Hz stereo)...")
    t0 = time.time()
    np.random.seed(999)

    num_samples = int(total_duration * sample_rate)
    master_l = np.zeros(num_samples, dtype=np.float32)
    master_r = np.zeros(num_samples, dtype=np.float32)

    # Mineral slab fundamentals (Obsidian and Basalt modal scales)
    # Pentatonic stone tuning in A minor / Hirajoshi: [A2, C3, D3, E3, G3, A3, C4, E4, A4]
    stone_frequencies = [110.0, 130.8, 146.8, 164.8, 196.0, 220.0, 261.6, 329.6, 440.0, 523.2, 659.2]

    # Score of strikes: contemplative, rhythmic, space-filled
    cur_time = 2.5
    strike_count = 0

    while cur_time < total_duration - 12.0:
        freq = float(np.random.choice(stone_frequencies))
        strike_dur = 8.5
        pan = float(np.random.uniform(0.15, 0.85))

        sig_l, sig_r = synthesize_modal_strike(freq, strike_dur, sample_rate, pan)

        start_idx = int(cur_time * sample_rate)
        end_idx = min(num_samples, start_idx + len(sig_l))
        seg_len = end_idx - start_idx

        master_l[start_idx:end_idx] += sig_l[:seg_len]
        master_r[start_idx:end_idx] += sig_r[:seg_len]

        strike_count += 1
        # Irregular meditative intervals (2.5s to 6.5s between strikes)
        interval = float(np.random.choice([2.8, 3.6, 4.5, 5.8, 7.2]))
        cur_time += interval

    print(f"    Rendered {strike_count} obsidian strikes. Adding subterranean cloister acoustic reverberation...")

    # Subtle convolution/feedback delay to simulate stone cloister reflections
    delay_samples = int(0.38 * sample_rate)
    decay = 0.38
    for i in range(delay_samples, num_samples):
        master_l[i] += master_r[i - delay_samples] * decay * 0.5
        master_r[i] += master_l[i - delay_samples] * decay * 0.5

    # Master envelope and normalization
    fade = int(4.0 * sample_rate)
    master_l[:fade] *= np.linspace(0, 1, fade)
    master_r[:fade] *= np.linspace(0, 1, fade)
    master_l[-fade:] *= np.linspace(1, 0, fade)
    master_r[-fade:] *= np.linspace(1, 0, fade)

    peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r))) + 1e-6
    master_l = (master_l / peak) * 0.88
    master_r = (master_r / peak) * 0.88

    # Write WAV
    int16_l = (master_l * 32767.0).astype(np.int16)
    int16_r = (master_r * 32767.0).astype(np.int16)
    interleaved = np.empty((num_samples * 2,), dtype=np.int16)
    interleaved[0::2] = int16_l
    interleaved[1::2] = int16_r

    out_dir = os.path.dirname(os.path.abspath(__file__))
    wav_path = os.path.join(out_dir, output_wav)
    mp3_path = os.path.join(out_dir, output_mp3)

    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(interleaved.tobytes())

    print(f"[✓] Saved Lithic Master WAV: {wav_path} ({os.path.getsize(wav_path) / (1024*1024):.2f} MB)")

    # Encode to MP3 via ffmpeg
    cmd = ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "320k", mp3_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Saved Lithic MP3: {mp3_path} ({os.path.getsize(mp3_path) / (1024*1024):.2f} MB)")
    return wav_path, mp3_path

if __name__ == "__main__":
    synthesize_lithophone_suite()
