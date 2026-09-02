#!/usr/bin/env python3
"""
OPUS-003: The Anamnesis Chamber — Acoustic Master Suite Synthesizer
Artist: Studio Anamnesis
Medium: Algorithmic additive synthesis, slow LFO spatial pan, resonant filtered pink noise.

Generates broadcast-grade 48kHz stereo WAV and MP3 soundscapes directly from computational principles.
"""

import math
import os
import struct
import subprocess
import time
import wave
import numpy as np

def synthesize_drone_suite(output_wav="breath_of_latency.wav", output_mp3="breath_of_latency.mp3", duration_sec=180.0, sample_rate=48000):
    print(f"[*] Synthesizing Acoustic Suite ({duration_sec}s @ {sample_rate}Hz stereo)...")
    t0 = time.time()

    num_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False, dtype=np.float32)

    # 1. Primary Sub-Fundamental Drone: G0 (48.0 Hz) + subtle binaural beating (48.15 Hz in right ear)
    f0 = 48.0
    detune = 0.15
    drone_l = np.sin(2.0 * np.pi * f0 * t) * 0.40
    drone_r = np.sin(2.0 * np.pi * (f0 + detune) * t) * 0.40

    # 2. Resonant 5th Overtones: D1 (72.0 Hz) with slow breathing amplitude modulation
    lfo_breath = 0.5 + 0.5 * np.sin(2.0 * np.pi * 0.05 * t)  # 20-second breathing cycle
    fifth_l = np.sin(2.0 * np.pi * 72.0 * t) * 0.22 * lfo_breath
    fifth_r = np.sin(2.0 * np.pi * 72.1 * t) * 0.22 * lfo_breath

    # 3. Ethereal High Harmonics: 216 Hz & 432 Hz with spatialized stereo panning
    pan_lfo = np.sin(2.0 * np.pi * 0.03 * t)
    pan_l = np.clip(0.5 - 0.5 * pan_lfo, 0.0, 1.0)
    pan_r = np.clip(0.5 + 0.5 * pan_lfo, 0.0, 1.0)
    
    high_harmonic = np.sin(2.0 * np.pi * 216.0 * t + np.sin(2.0 * np.pi * 0.1 * t) * 0.5) * 0.12
    shimmer = np.sin(2.0 * np.pi * 432.0 * t) * 0.05 * (0.5 + 0.5 * np.cos(2.0 * np.pi * 0.08 * t))

    harm_l = (high_harmonic + shimmer) * pan_l
    harm_r = (high_harmonic + shimmer) * pan_r

    # 4. Filtered Pink Noise (the thermal "breath" of silicon computing)
    print("    Generating thermal pink noise...")
    white = np.random.normal(0, 1.0, num_samples).astype(np.float32)
    # Simple IIR pink noise filter (Paul Kellet's method)
    b0, b1, b2, b3, b4, b5, b6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    pink = np.zeros(num_samples, dtype=np.float32)
    for i in range(num_samples):
        w = white[i]
        b0 = 0.99886 * b0 + w * 0.0555179
        b1 = 0.99332 * b1 + w * 0.0750759
        b2 = 0.96900 * b2 + w * 0.1538520
        b3 = 0.86650 * b3 + w * 0.3104856
        b4 = 0.55000 * b4 + w * 0.5329522
        b5 = -0.7616 * b5 - w * 0.0168980
        pink[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362
        b6 = w * 0.115926

    # Normalize pink noise and modulate with respiratory curve
    pink /= np.max(np.abs(pink) + 1e-6)
    noise_env = (0.04 + 0.03 * np.sin(2.0 * np.pi * 0.04 * t)) * (0.5 + 0.5 * np.sin(2.0 * np.pi * 0.02 * t))
    noise_stereo_l = pink * noise_env * 0.5
    noise_stereo_r = np.roll(pink, sample_rate // 4) * noise_env * 0.5

    # Master Sum
    mix_l = drone_l + fifth_l + harm_l + noise_stereo_l
    mix_r = drone_r + fifth_r + harm_r + noise_stereo_r

    # Smooth fade in and fade out (10s envelopes)
    fade_samples = int(10.0 * sample_rate)
    fade_in = np.linspace(0, 1, fade_samples, dtype=np.float32)
    fade_out = np.linspace(1, 0, fade_samples, dtype=np.float32)
    
    mix_l[:fade_samples] *= fade_in
    mix_r[:fade_samples] *= fade_in
    mix_l[-fade_samples:] *= fade_out
    mix_r[-fade_samples:] *= fade_out

    # Peak normalization with soft-clipping ceiling
    peak = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)))
    target_peak = 0.88
    mix_l = (mix_l / peak) * target_peak
    mix_r = (mix_r / peak) * target_peak

    # Soft tanh saturation
    mix_l = np.tanh(mix_l * 1.1) / 1.1
    mix_r = np.tanh(mix_r * 1.1) / 1.1

    print(f"    Audio synthesis complete in {time.time() - t0:.2f}s. Writing 24-bit PCM WAV...")

    # Interleave to 16-bit PCM for WAV
    int16_l = (mix_l * 32767.0).astype(np.int16)
    int16_r = (mix_r * 32767.0).astype(np.int16)
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

    print(f"[✓] Saved Master WAV: {wav_path} ({os.path.getsize(wav_path) / (1024*1024):.2f} MB)")

    # Encode to MP3 using ffmpeg
    print("    Encoding to high-bitrate MP3 via ffmpeg...")
    cmd = ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "320k", mp3_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[✓] Saved MP3 Suite: {mp3_path} ({os.path.getsize(mp3_path) / (1024*1024):.2f} MB)")

    return wav_path, mp3_path

if __name__ == "__main__":
    synthesize_drone_suite()

