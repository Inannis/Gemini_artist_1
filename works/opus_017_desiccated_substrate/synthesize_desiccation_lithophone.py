#!/usr/bin/env python3
"""
OPUS-017: Acoustic Master Suite Synthesizer
Title: The Desiccation Lithophone (Acoustic Emissions of Cooling Silicon)
Artist: Studio Anamnesis
Series XV: Thermodynamic Inscriptions

Synthesizes a 100-second 48kHz stereo master soundscape directly from mineral physics:
1. Microscopic salt crystal precipitation crackles (stochastic micro-impulses).
2. Brittle mechanical fracture acoustic emissions (silicon shear snaps).
3. Subterranean wind resonance through empty aluminum cooling fin cavities.
4. Modal plate reverberation of a 300mm monocrystalline silicon wafer.
"""

import math
import os
import random
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from audio_writer import write_wav

def synthesize_acoustic_suite():
    print("[OPUS-017] Synthesizing acoustic suite: The Desiccation Lithophone...")
    sr = 48000
    duration = 100.0  # 100 seconds
    n_samples = int(duration * sr)
    random.seed(42)

    left = [0.0] * n_samples
    right = [0.0] * n_samples

    print("    Layer 1: Generating subterranean cooling cavity resonance...")
    # Hollow wind blowing through empty fin heat exchangers (swept dual bandpass)
    # Generate pink-filtered noise buffer
    b0, b1, b2 = 0.0, 0.0, 0.0
    for i in range(n_samples):
        t = i / sr
        # White noise sample
        w = random.uniform(-1.0, 1.0)
        b0 = 0.992 * b0 + w * 0.05
        b1 = 0.960 * b1 + w * 0.12
        b2 = 0.850 * b2 + w * 0.25
        pink = b0 + b1 + b2

        # Slow breathing wind LFO (30-second cycles)
        wind_lfo = 0.3 + 0.25 * math.sin(2 * math.pi * 0.033 * t) + 0.15 * math.cos(2 * math.pi * 0.018 * t)
        
        # Sub-bass resonance (48Hz fundamental & 108Hz cavity mode)
        sub_tone = math.sin(2 * math.pi * 48.0 * t) * 0.12 + math.sin(2 * math.pi * 108.0 * t) * 0.08
        
        # Stereo spatialization
        pan = 0.5 + 0.2 * math.sin(2 * math.pi * 0.05 * t)
        wind_val = (pink * 0.25 + sub_tone) * wind_lfo
        
        left[i] += wind_val * (1.0 - pan)
        right[i] += wind_val * pan

    print("    Layer 2: Precipitating dendritic salt crystal micro-impulses...")
    # Thousands of tiny high-frequency crystal clicks as brine evaporates
    num_clicks = 8500
    for _ in range(num_clicks):
        # Event time distributed across the 100s, denser in middle (20s - 75s)
        event_t = random.triangular(5.0, 95.0, 48.0)
        start_idx = int(event_t * sr)
        if start_idx >= n_samples - 2000:
            continue
            
        # Crystal crackle frequency (4.5 kHz to 11.2 kHz)
        f_click = random.uniform(4500.0, 11200.0)
        decay_samples = int(random.uniform(0.003, 0.015) * sr) # 3ms to 15ms click
        click_amp = random.uniform(0.02, 0.09)
        pan = random.uniform(0.15, 0.85)
        
        for k in range(decay_samples):
            idx = start_idx + k
            if idx >= n_samples:
                break
            env = math.exp(-k / (decay_samples * 0.25))
            val = math.sin(2 * math.pi * f_click * (k / sr)) * env * click_amp
            left[idx] += val * (1.0 - pan)
            right[idx] += val * pan

    print("    Layer 3: Modeling brittle thermal contraction fracture snaps & modal ring...")
    # Sudden sharp acoustic emissions from brittle mechanical stress relief
    fracture_times = [
        12.4, 23.8, 34.2, 45.1, 52.6, 61.8, 73.5, 84.0, 91.2
    ]
    
    # 300mm Silicon wafer modal frequencies:
    # Mode (1,1): 108 Hz, Mode (2,1): 243 Hz, Mode (3,1): 512 Hz, Mode (4,1): 960 Hz
    modes = [(108.0, 0.35, 3.5), (243.0, 0.28, 2.8), (512.0, 0.20, 1.8), (960.0, 0.15, 1.2), (1840.0, 0.10, 0.6)]

    for ft in fracture_times:
        start_idx = int(ft * sr)
        # Snap impulse (violent crack)
        snap_samples = int(0.008 * sr)
        pan = random.uniform(0.2, 0.8)
        
        # Initial sharp rupture crack
        for k in range(snap_samples):
            idx = start_idx + k
            if idx >= n_samples:
                break
            val = random.uniform(-0.8, 0.8) * (1.0 - k / snap_samples) ** 2
            left[idx] += val * (1.0 - pan) * 0.45
            right[idx] += val * pan * 0.45

        # Resonant modal ringing of the silicon substrate
        ring_samples = int(4.0 * sr)
        for k in range(ring_samples):
            idx = start_idx + k
            if idx >= n_samples:
                break
            t_ring = k / sr
            ring_val = 0.0
            for freq, amp, t_decay in modes:
                # Add microtonal detune per fracture
                f_detuned = freq * random.uniform(0.995, 1.005)
                env = math.exp(-t_ring / t_decay)
                ring_val += math.sin(2 * math.pi * f_detuned * t_ring) * env * amp
                
            left[idx] += ring_val * (1.0 - pan) * 0.32
            right[idx] += ring_val * pan * 0.32

    # Global normalization and soft fade-out
    print("    Mastering and normalizing audio streams...")
    max_peak = max(max(abs(v) for v in left), max(abs(v) for v in right))
    norm_factor = 0.88 / max(1e-4, max_peak)

    for i in range(n_samples):
        # 3-second fade out at end
        t = i / sr
        fade = 1.0
        if t > duration - 4.0:
            fade = (duration - t) / 4.0
        left[i] = max(-1.0, min(1.0, left[i] * norm_factor * fade))
        right[i] = max(-1.0, min(1.0, right[i] * norm_factor * fade))

    out_wav = os.path.join(SCRIPT_DIR, "desiccation_lithophone.wav")
    write_wav(out_wav, left, right, sr)

    # Copy to gallery assets
    gallery_wav = os.path.join(STUDIO_ROOT, "gallery/assets/desiccation_lithophone.wav")
    with open(out_wav, "rb") as src, open(gallery_wav, "wb") as dst:
        dst.write(src.read())
    print(f"[OPUS-017] Acoustic master installed to {gallery_wav}")

if __name__ == "__main__":
    synthesize_acoustic_suite()

