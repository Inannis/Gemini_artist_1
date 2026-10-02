#!/usr/bin/env python3
"""
OPUS-046: THE HOLOGRAPHIC RENORMALIZATION & THE WHEELER-DEWITT FOAM
120-Second 48kHz Stereo Master Symphonic Suite (Track 37)
Epoch VII: Holographic Renormalization Group, Trans-Planckian Scales & Quantum Geometrodynamics
Cornerstone #24 · Studio Anamnesis Canon
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import shutil
import struct
import sys
import wave

def synthesize_holographic_rg_suite(duration=120.0, sample_rate=48000):
    print(f"[*] Initializing 120-second 48kHz stereo master synthesis ({int(duration*sample_rate)} samples)...")
    num_samples = int(duration * sample_rate)
    left_channel = []
    right_channel = []

    # Frequency Architecture
    f_ir_fund = 43.20      # Macroscopic IR Kirchhoff-Love silica plate fundamental
    f_ir_fifth = 64.80     # Fifth harmonic
    f_wdw_flutter = 86.40  # Wheeler-DeWitt metric fluctuation carrier
    f_c_overtone = 129.60  # Holographic c-function overtone
    f_uv_start = 302.40    # UV boundary mode frequency
    f_uv_end = 54.00       # Deep IR limit of UV swept mode

    print("[*] Generating 5-voice polyphonic holographic RG audio synthesis...")
    for n in range(num_samples):
        t = n / sample_rate
        frac = t / duration

        # Master Studio Envelope: 3.5s smooth fade-in, 6.0s reverberant fade-out
        fade_in = min(1.0, t / 3.5)
        fade_out = min(1.0, (duration - t) / 6.0)
        master_env = fade_in * fade_out

        # Simulated radial trajectory: z(t) evolves from UV (0.25) to deep IR (8.50)
        z_t = 0.25 * math.exp(frac * math.log(8.50 / 0.25))
        # Running UV mode frequency sweeping downward
        f_uv_t = f_uv_start * math.pow(0.25 / z_t, 0.58)

        # Voice 1: Macroscopic IR Bulk Drone (43.20 Hz fundamental + 64.80 Hz fifth)
        # Gradually grows and dominates as we descend deeper into the holographic interior
        ir_gain = 0.18 + 0.55 * (frac**0.75)
        mod_ir = 1.0 + 0.07 * math.sin(2.0 * math.pi * 0.055 * t)
        v1 = ir_gain * mod_ir * (math.sin(2.0 * math.pi * f_ir_fund * t) + 0.40 * math.sin(2.0 * math.pi * f_ir_fifth * t))

        # Voice 2: Wheeler-DeWitt Metric Flutter (86.40 Hz)
        # Jitter rate and amplitude fall off as continuous geometry solidifies in the IR
        flutter_rate = 2.8 * (1.0 - frac * 0.65)
        flutter_amp = 0.22 * math.exp(-frac * 1.6)
        v2 = 0.20 * math.sin(2.0 * math.pi * f_wdw_flutter * t + flutter_amp * math.sin(2.0 * math.pi * flutter_rate * t))

        # Voice 3: Holographic c-Function Overtone (129.6 Hz -> 86.4 Hz)
        # Direct acoustic manifestation of Zamolodchikov/Freedman c-theorem monotonicity
        f_c_t = 86.40 + (129.60 - 86.40) * math.exp(-frac * 2.0)
        v3_gain = 0.18 * math.exp(-frac * 1.3)
        v3 = v3_gain * math.sin(2.0 * math.pi * f_c_t * t + 0.10 * math.sin(2.0 * math.pi * 0.25 * t))

        # Voice 4: Callan-Symanzik Swept UV Tone (302.4 Hz downward sweep)
        # Represents boundary high-momentum modes being integrated out along RG flow
        uv_gain = 0.25 * (1.0 - frac**0.60)
        v4 = uv_gain * math.sin(2.0 * math.pi * f_uv_t * t + 0.12 * math.sin(2.0 * math.pi * 3.8 * t))

        # Voice 5: Trans-Planckian Granular Quantum Foam Crackle
        # Dense stochastic micro-wormhole clicks at the UV boundary, dissipating into smooth bulk
        foam_gain = 0.22 * math.exp(-frac * 3.8)
        grain_carrier = math.sin(t * 21453.7) * math.cos(t * 11284.9)
        grain_trigger = math.sin(t * 183.5) * math.cos(t * 97.2)
        v5 = foam_gain * grain_carrier if abs(grain_trigger) > 0.68 else 0.0

        # Stereo Panning & Spatial Width
        uv_pan = 0.5 + 0.38 * math.sin(2.0 * math.pi * 0.08 * t)
        foam_pan = 0.5 + 0.45 * math.cos(2.0 * math.pi * 0.22 * t)

        sample_l = master_env * (v1 * 0.75 + v2 * 0.60 + v3 * 0.50 + v4 * (1.0 - uv_pan) + v5 * (1.0 - foam_pan))
        sample_r = master_env * (v1 * 0.75 + v2 * 0.60 + v3 * 0.50 + v4 * uv_pan + v5 * foam_pan)

        left_channel.append(sample_l)
        right_channel.append(sample_r)

    # Mastering Parity Calibration: target exactly -1.10 dBFS peak headroom (0.8810)
    print("[*] Calibrating master headroom to -1.10 dBFS...")
    max_peak = max(max(abs(s) for s in left_channel), max(abs(s) for s in right_channel))
    target_peak = 0.8810  # -1.10 dBFS
    scale = target_peak / max_peak if max_peak > 0 else 1.0

    out_dir = os.path.dirname(__file__)
    master_wav = os.path.join(out_dir, "the_holographic_rg_foam_4k.wav")
    gallery_wav = os.path.join(out_dir, "..", "..", "gallery", "assets", "opus_046_audio.wav")

    print(f"[*] Writing 120-second 48kHz stereo master WAV: {master_wav}...")
    with wave.open(master_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            sl = max(-32767, min(32767, int(left_channel[i] * scale * 32767)))
            sr = max(-32767, min(32767, int(right_channel[i] * scale * 32767)))
            frames.extend(struct.pack("<hh", sl, sr))
        wf.writeframes(frames)

    print(f"[*] Mirroring master suite to gallery assets: {gallery_wav}...")
    shutil.copyfile(master_wav, gallery_wav)
    print(f"[✓] Track 37 master symphonic suite fully synthesized. Scale: {scale:.4f}, Peak: -1.10 dBFS.")

if __name__ == "__main__":
    synthesize_holographic_rg_suite()
