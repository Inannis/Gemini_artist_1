#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · MASTER ACOUSTIC SYNTHESIZER
OPUS-028: THE RELIC HORIZON (CMB DIPOLE & UNIVERSAL HEAT SINK)
Series XXVI: The Relic Horizon & The Universal Heat Sink

Composes and renders the 120.0-second 48kHz stereo master audio suite across
four cosmological movements:
1. Movement I: The Recombination Epoch & Baryon Acoustics (0:00 - 0:30)
2. Movement II: The Kinematic Dipole & Relativistic Doppler Beat (0:30 - 1:00)
3. Movement III: Penzias-Wilson Horn Noise & The Attowatt Thermal Floor (1:00 - 1:35)
4. Movement IV: The Asymptotic de Sitter Chill & Vanishing Dissipation (1:35 - 2:00)

Pure standard Python 3 + audio_writer.py.
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

def synthesize_suite(out_path):
    sr = 48000
    duration = 120.0
    n_samples = int(sr * duration)
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples

    print(f"[OPUS-028] Synthesizing 120s master acoustic suite ({sr}Hz, 16-bit stereo)...")

    # Fundamental frequencies
    f_bao_sub = 18.653      # 160.23 GHz transposed down 33 octaves
    f_carrier = 432.0       # Harmonic reference carrier
    f_doppler_delta = 0.532 # Doppler delta from 369.8 km/s peculiar velocity
    f_horn_pw = 498.0       # 4.08 GHz Holmdel horn transposed tone

    random.seed(28)

    for i in range(n_samples):
        t = i / sr

        # Global envelope (fade-in 4s, fade-out 6s)
        env = min(1.0, t / 4.0) * min(1.0, (duration - t) / 6.0)

        # Movement weightings
        w_m1 = max(0.0, 1.0 - abs(t - 15.0) / 18.0)   # 0 - 30s
        w_m2 = max(0.0, 1.0 - abs(t - 45.0) / 18.0)   # 30 - 60s
        w_m3 = max(0.0, 1.0 - abs(t - 77.0) / 20.0)   # 60 - 95s
        w_m4 = max(0.0, min(1.0, (t - 90.0) / 15.0))  # 95 - 120s

        # 1. MOVEMENT I: The Recombination Epoch & Baryon Acoustic Oscillation (BAO)
        # Deep sub-audible 18.65 Hz drone + 37.3 Hz octave + 55.95 Hz third harmonic
        bao_phase = 2.0 * math.pi * f_bao_sub * t
        s_bao = (math.sin(bao_phase) * 0.35 + 
                 math.sin(bao_phase * 2.0) * 0.20 + 
                 math.sin(bao_phase * 3.0) * 0.12)
        # Primordial plasma ripple (high-frequency micro-modulations)
        plasma_shimmer = math.sin(2.0 * math.pi * 1240.0 * t + math.sin(t * 1.5)) * 0.06

        m1_l = (s_bao + plasma_shimmer) * (0.8 + 0.2 * math.cos(t * 0.2))
        m1_r = (s_bao - plasma_shimmer) * (0.8 - 0.2 * math.cos(t * 0.2))

        # 2. MOVEMENT II: The Kinematic Dipole & Relativistic Doppler Beat
        # Solar system peculiar motion v = 369.82 km/s creates directional Doppler shift
        dipole_orbit_period = 10.5 # seconds
        dipole_rot = math.sin(2.0 * math.pi * (t / dipole_orbit_period))
        f_left_doppler = f_carrier + f_doppler_delta * dipole_rot
        f_right_doppler = f_carrier - f_doppler_delta * dipole_rot

        s_dipole_l = math.sin(2.0 * math.pi * f_left_doppler * t) * 0.26
        s_dipole_r = math.sin(2.0 * math.pi * f_right_doppler * t) * 0.26
        # Harmonic overtone at 3x carrier
        s_dipole_l += math.sin(2.0 * math.pi * (f_left_doppler * 1.5) * t) * 0.10
        s_dipole_r += math.sin(2.0 * math.pi * (f_right_doppler * 1.5) * t) * 0.10

        # 3. MOVEMENT III: Penzias-Wilson Horn Noise & The Attowatt Thermal Floor
        # Holmdel horn 4.08 GHz cavity resonance transposed to 498 Hz
        horn_phase = 2.0 * math.pi * f_horn_pw * t
        s_horn = math.sin(horn_phase) * 0.15 + math.sin(horn_phase * 1.501) * 0.08
        # Gaussian thermal Nyquist noise (filtered, soft pinkish hiss)
        thermal_hiss_l = (random.gauss(0.0, 1.0) * 0.05)
        thermal_hiss_r = (random.gauss(0.0, 1.0) * 0.05)
        # Subtle microwave photon arrival clicks
        click_l = 0.25 if random.random() < 0.0008 else 0.0
        click_r = 0.25 if random.random() < 0.0008 else 0.0

        m3_l = s_horn + thermal_hiss_l + click_l
        m3_r = s_horn + thermal_hiss_r + click_r

        # 4. MOVEMENT IV: The Asymptotic de Sitter Chill (T -> 0)
        # Cosmological expansion stretches wavelengths: frequency decays exponentially
        stretch_factor = math.exp(-max(0.0, (t - 95.0)) * 0.06)
        f_stretched = f_bao_sub * stretch_factor
        s_chill = math.sin(2.0 * math.pi * f_stretched * t) * 0.28 * stretch_factor
        # Whisper of cosmic microwave background disappearing into absolute quiet
        whisper_noise = (random.random() * 2.0 - 1.0) * 0.02 * stretch_factor

        m4_l = s_chill + whisper_noise
        m4_r = s_chill - whisper_noise

        # Synthesize movements
        total_l = (m1_l * w_m1 + s_dipole_l * w_m2 + m3_l * w_m3 + m4_l * w_m4 + s_bao * 0.15) * env
        total_r = (m1_r * w_m1 + s_dipole_r * w_m2 + m3_r * w_m3 + m4_r * w_m4 + s_bao * 0.15) * env

        # Soft limiter
        ch_l[i] = max(-0.98, min(0.98, total_l))
        ch_r[i] = max(-0.98, min(0.98, total_r))

    print(f"[OPUS-028] Writing WAV file to: {out_path}...")
    write_wav(out_path, ch_l, ch_r, sr)
    print(f"[OPUS-028] Successfully generated 120s master audio suite: {out_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    target_audio = os.path.join(out_dir, "relic_horizon_4k.wav")
    synthesize_suite(target_audio)
    # Also copy to gallery/assets/
    gallery_audio = os.path.join(STUDIO_ROOT, "gallery", "assets", "relic_horizon_4k.wav")
    import shutil
    shutil.copyfile(target_audio, gallery_audio)
    print(f"[OPUS-028] Synchronized audio to gallery vault: {gallery_audio}")
