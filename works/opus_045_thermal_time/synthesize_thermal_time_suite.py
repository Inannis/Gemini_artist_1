#!/usr/bin/env python3
"""
OPUS-045: THE MODULAR RELIQUARY & THE THERMAL TIME FLOW
Master Symphonic Audio Suite Synthesizer (120s 48kHz Stereo · Track 36)
Inaugurating Epoch VII: Operator Algebras, Modular Flow & Thermodynamic Chronology
Cornerstone #23 · Studio Anamnesis Canon
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import shutil
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from audio_writer import write_wav
from harmonic_spectrum_analyzer import analyze_wav_dynamics

def synthesize_thermal_time_suite(duration=120.0, sample_rate=48000):
    total_samples = int(duration * sample_rate)
    print(f"[*] Synthesizing OPUS-045 Master Symphonic Suite ({duration:.1f}s at {sample_rate}Hz = {total_samples:,} stereo samples)...")

    left_samples = [0.0] * total_samples
    right_samples = [0.0] * total_samples

    # Fundamental physical frequencies
    f0 = 45.83       # KMS sub-bass thermal drone (Hz)
    f_beat = 53.78   # Near-line beating frequency (Hz)
    f_mode = 68.37   # Modular horizon overtone (Hz)
    f_fine = 137.036 # Fine-structure golden carrier (Hz)
    beta_kms = 12.0  # KMS circulation period (s)
    w_flow = 2.0 * math.pi / beta_kms

    # Report synthesis progress at 25% intervals
    progress_step = total_samples // 4

    for i in range(total_samples):
        if i > 0 and i % progress_step == 0:
            pct = (i / total_samples) * 100.0
            print(f"  -> Progress: {pct:.0f}% ({i:,}/{total_samples:,} samples)")

        t = i / sample_rate

        # --- GLOBAL MASTER ENVELOPE (Four-Movement Architecture) ---
        # Overall 4.0s fade-in, 5.0s fade-out
        if t < 4.0:
            master_env = 0.5 * (1.0 - math.cos(math.pi * t / 4.0))
        elif t > duration - 5.0:
            master_env = 0.5 * (1.0 - math.cos(math.pi * (duration - t) / 5.0))
        else:
            master_env = 1.0

        # Modular breathing envelope (12.0s period)
        cycle_phase = (w_flow * t) % (2.0 * math.pi)
        mod_breath = 0.5 * (1.0 - math.cos(cycle_phase))

        # --- MOVEMENT ENVELOPES ---
        # Movement I: The Frozen Constraint [0:00 - 0:30]
        # Movement II: The Modular Awakening [0:30 - 1:00]
        # Movement III: The Ouroboros Hypocycloid [1:00 - 1:35]
        # Movement IV: Sugimoto Equilibrium [1:35 - 2:00]
        m1 = max(0.0, min(1.0, 1.0 - (t - 25.0) / 10.0)) if t > 25.0 else 1.0
        m2 = max(0.0, min(1.0, (t - 25.0) / 10.0)) if t <= 60.0 else max(0.0, min(1.0, 1.0 - (t - 55.0) / 10.0))
        m3 = max(0.0, min(1.0, (t - 55.0) / 10.0)) if t <= 95.0 else max(0.0, min(1.0, 1.0 - (t - 90.0) / 10.0))
        m4 = max(0.0, min(1.0, (t - 90.0) / 10.0))

        # --- VOICE 1: SUB-BASS WHEELER-DEWITT & KMS DRONE (45.83 Hz) ---
        # Present throughout, anchoring the cosmological stillness
        v1 = (math.sin(2.0 * math.pi * f0 * t) + 
              0.25 * math.sin(4.0 * math.pi * f0 * t) + 
              0.10 * math.sin(6.0 * math.pi * f0 * t)) * 0.42

        # --- VOICE 2: NEAR-LINE MODULAR BEATING (53.78 Hz <-> 55.0 Hz) ---
        # Enters in Movement II, generating a 1.22 Hz somatic pulse
        v2 = math.sin(2.0 * math.pi * f_beat * t) * 0.26 * (0.6 + 0.4 * mod_breath) * (m2 + m3 + m4 * 0.5)

        # --- VOICE 3: MODULAR HORIZON MODE (68.37 Hz) WITH ROTATING PAN ---
        # Orbiting stereo field governed by Tomita-Takesaki automorphism
        v3 = math.sin(2.0 * math.pi * f_mode * t) * 0.20 * (m2 * 0.8 + m3 + m4 * 0.7)
        pan_l = 0.5 + 0.38 * math.sin(w_flow * t)
        pan_r = 0.5 - 0.38 * math.sin(w_flow * t)

        # --- VOICE 4: FINE-STRUCTURE GOLDEN CARRIER (137.036 Hz) ---
        # Enters in Movement III with subtle microtonal KMS dispersion
        f_disp = f_fine + 1.8 * math.sin(w_flow * t * 0.5)
        v4 = math.sin(2.0 * math.pi * f_disp * t) * 0.12 * (0.3 + 0.7 * mod_breath) * (m3 + m4)

        # --- VOICE 5: OUROBOROS HYPOCYCLOID EPOCH GLISSANDO ---
        # Traverses the signature frequencies of all 6 epochs during Movement III
        if m3 > 0.0:
            p_sweep = (t - 55.0) / 40.0
            p_sweep = max(0.0, min(1.0, p_sweep))
            # Smooth interpolation: 55.0 -> 86.4 -> 160.2 -> 137.04 -> 43.65 Hz
            f_sweep = 55.0 * (1.0 - p_sweep)**2 + 160.2 * 2.0 * p_sweep * (1.0 - p_sweep) + 43.65 * (p_sweep**2)
            v5 = math.sin(2.0 * math.pi * f_sweep * t) * 0.16 * m3
        else:
            v5 = 0.0

        # --- VOICE 6: SUGIMOTO EQUILIBRIUM CONSONANCE (Movement IV) ---
        # Pure radiant consonant triad (45.83 Hz, 91.66 Hz, 137.49 Hz)
        if m4 > 0.0:
            v6 = (0.5 * math.sin(2.0 * math.pi * f0 * 2.0 * t) +
                  0.3 * math.sin(2.0 * math.pi * f0 * 3.0 * t)) * 0.18 * m4
        else:
            v6 = 0.0

        # Stereo Channel Mixdown
        l_chan = master_env * (v1 * 0.68 + v2 * 0.50 + v3 * pan_l + v4 * 0.40 + v5 * 0.55 + v6 * 0.50)
        r_chan = master_env * (v1 * 0.68 + v2 * 0.50 + v3 * pan_r + v4 * 0.60 + v5 * 0.45 + v6 * 0.50)

        left_samples[i] = l_chan
        right_samples[i] = r_chan

    # --- MASTERING CALIBRATION (-1.10 dBFS True Peak Target) ---
    print("[*] Calibrating dynamic mastering headroom to -1.10 dBFS...")
    max_peak = max(max(abs(x) for x in left_samples), max(abs(x) for x in right_samples), 1e-6)
    target_peak = 10.0 ** (-1.10 / 20.0)  # ~0.88105
    master_gain = target_peak / max_peak

    left_norm = [s * master_gain for s in left_samples]
    right_norm = [s * master_gain for s in right_samples]

    # Save to works/ and gallery/assets/
    out_dir = os.path.dirname(__file__)
    work_wav = os.path.join(out_dir, "the_thermal_time_flow_4k.wav")
    gallery_wav = os.path.abspath(os.path.join(out_dir, "..", "..", "gallery", "assets", "opus_045_audio.wav"))

    print(f"[*] Writing 120s master WAV file to: {work_wav}")
    write_wav(work_wav, left_norm, right_norm, sample_rate=sample_rate)
    print(f"[*] Copying master audio to gallery asset: {gallery_wav}")
    shutil.copyfile(work_wav, gallery_wav)

    # Perform automated acoustic verification
    print("[*] Performing automated acoustic verification on master suite...")
    metrics = analyze_wav_dynamics(work_wav)
    print("=" * 68)
    print("      OPUS-045 ACOUSTIC MASTERING VERIFICATION REPORT        ")
    print("=" * 68)
    print(f"  Duration          : {metrics['duration_sec']:.2f} seconds")
    print(f"  Peak Level        : {metrics['peak_db']:.2f} dBFS (Target: -1.10 dBFS)")
    print(f"  RMS Power Level   : {metrics['rms_db']:.2f} dBFS")
    print(f"  Crest Factor      : {metrics['crest_db']:.2f} dB (Headroom standard >= 8.0 dB)")
    print(f"  DC Offset Bias    : {metrics['dc_offset_pct']:.4f}%")
    print(f"  Mastering Verdict : {metrics['status'].upper()}")
    print("=" * 68)
    return 0

if __name__ == "__main__":
    sys.exit(synthesize_thermal_time_suite())
