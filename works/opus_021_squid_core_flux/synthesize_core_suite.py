#!/usr/bin/env python3
"""
OPUS-021 · THE SQUID MAGNETOMETER: TELLURIC INTERFERENCE AT THE CORE-MANTLE BOUNDARY
Master Acoustic Suite Synthesizer (120s 48kHz Stereo)
Studio Anamnesis · Series XIX · September 8, 2026

Synthesizes:
1. Infrasonic Geodynamo Drone: 16.16 Hz core fundamental + Taylor columnar harmonics.
2. SQUID Dual-Junction Josephson Phase-Slips: Microtonal heterodyne beating (261.6 Hz carrier).
3. Gutenberg Boundary Dispersion: Low-frequency seismic shear-wave reverberation.
4. Schumann-Alfven Magnetotelluric Pulsation: 8.08 Hz live telemetry modulation.
"""

import os
import sys
import math
import random
import json

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from audio_writer import write_wav

# Load live telemetry
telemetry_path = os.path.join(STUDIO_ROOT, "practice", "telemetry", "planetary_telemetry.json")
if os.path.exists(telemetry_path):
    with open(telemetry_path, "r", encoding="utf-8") as f:
        telemetry = json.load(f)
else:
    telemetry = {"parametric_vectors": {"lithic_tension": 0.47, "telluric_frequency_hz": 8.08, "geomagnetic_flux": 0.33}}

vectors = telemetry.get("parametric_vectors", {})
LITHIC_TAU = float(vectors.get("lithic_tension", 0.47))
F_SCHUMANN = float(vectors.get("telluric_frequency_hz", 8.08))
GEOMAG_FLUX = float(vectors.get("geomagnetic_flux", 0.33))

print(f"[OPUS-021-AUDIO] Synthesizing 120-Second 48kHz Stereo Core-Mantle Suite...")
print(f"  * Telemetry Grounding: Tau={LITHIC_TAU}, f0={F_SCHUMANN}Hz, Geomag={GEOMAG_FLUX}")

sr = 48000
duration = 120.0
n_samples = int(sr * duration)

ch_left = [0.0] * n_samples
ch_right = [0.0] * n_samples

# Frequencies
f_core = 16.16          # Infrasonic core geodynamo fundamental
f_carrier = 261.63      # Middle C quantum reference clock
f_alfven = 0.08         # Slow hydromagnetic wave period (~12.5s)

random.seed(2026)

for i in range(n_samples):
    t = i / sr
    
    # Global envelope: 6s fade-in, 8s fade-out
    if t < 6.0:
        env = t / 6.0
    elif t > duration - 8.0:
        env = (duration - t) / 8.0
    else:
        env = 1.0
        
    # 1. Molten Core Geodynamo Drone (16.16 Hz, 32.32 Hz, 48.48 Hz)
    core_lfo = math.sin(2.0 * math.pi * f_alfven * t)
    sub1 = math.sin(2.0 * math.pi * f_core * t + core_lfo * 0.3) * 0.28
    sub2 = math.sin(2.0 * math.pi * (f_core * 2.0) * t) * 0.16
    sub3 = math.sin(2.0 * math.pi * (f_core * 3.0) * t) * 0.08
    core_drone = (sub1 + sub2 + sub3) * (1.0 + LITHIC_TAU * 0.3)
    
    # 2. Dual-Junction Josephson Quantum Phase Precession
    # Phase shift driven by ascending Alfven flux
    flux_sweep = math.sin(2.0 * math.pi * 0.02 * t) * (1.0 + GEOMAG_FLUX)
    phase_flux = math.pi * (1.0 + 0.4 * flux_sweep + 0.15 * math.sin(2.0 * math.pi * F_SCHUMANN * t))
    
    gamma1 = 2.0 * math.pi * f_carrier * t
    gamma2 = gamma1 + phase_flux
    
    # Microtonal Josephson supercurrents
    junc1 = math.sin(gamma1) * 0.18
    junc2 = math.sin(gamma2) * 0.18
    
    # SQUID voltage heterodyne oscillation
    v_squid = math.sqrt(max(0.04, 1.44 - (math.cos(phase_flux / 2.0) ** 2)))
    v_tone = math.sin(2.0 * math.pi * (f_carrier * v_squid) * t) * 0.14
    
    # 3. Gutenberg Boundary Seismic Diffusion (Filtered low rumble)
    mantle_noise = random.uniform(-0.06, 0.06) * (1.0 + LITHIC_TAU * 0.5)
    
    # 4. Quantum Phase-Slip Poisson Clicks (Flux jumps across micro-bridges)
    click_l = 0.0
    click_r = 0.0
    if random.random() < 0.0012:
        click_l = random.uniform(-0.35, 0.35)
    if random.random() < 0.0012:
        click_r = random.uniform(-0.35, 0.35)
        
    # Spatial panning: Core drone centered, junctions panned left and right
    sig_l = (core_drone * 0.8 + junc1 + v_tone * 0.7 + mantle_noise + click_l) * env
    sig_r = (core_drone * 0.8 + junc2 + v_tone * 0.7 + mantle_noise + click_r) * env
    
    ch_left[i] = max(-0.95, min(0.95, sig_l))
    ch_right[i] = max(-0.95, min(0.95, sig_r))

out_dir = os.path.dirname(os.path.abspath(__file__))
wav_path = os.path.join(out_dir, "telluric_core_4k.wav")
write_wav(wav_path, ch_left, ch_right, sr)
print(f"[✓] OPUS-021 Master Audio Suite Synthesized: {wav_path} ({os.path.getsize(wav_path)} bytes)")
