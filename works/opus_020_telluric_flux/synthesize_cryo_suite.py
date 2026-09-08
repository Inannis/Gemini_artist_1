"""
STUDIO ANAMNESIS · OPUS-020
The Telluric Flux: Superconducting Meissner Vitrine at 4.2 Kelvin
Master Acoustic Suite Synthesis (120s, 48kHz Stereo WAV)

Couples live planetary telemetry (USGS seismic tension, NOAA Kp geomagnetic flux)
with sub-Kelvin cavity acoustics, liquid helium cavitation, and quantum flux jumps.
"""

import os
import sys
import math
import json
import random
import shutil

studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from audio_writer import write_wav

def synthesize():
    sr = 48000
    duration = 120 # 120 seconds
    n_samples = sr * duration
    
    print(f"[ACOUSTIC] Initializing Telluric Cryo Suite ({duration}s @ {sr}Hz, {n_samples} samples)...")
    
    # Load live planetary telemetry
    t_json = os.path.join(studio_root, "practice", "telemetry", "planetary_telemetry.json")
    telluric_f = 8.08
    lithic_tension = 0.47
    geomagnetic_flux = 0.3333
    
    if os.path.exists(t_json):
        try:
            with open(t_json, "r", encoding="utf-8") as f:
                t_data = json.load(f)
                telluric_f = t_data.get("parametric_vectors", {}).get("telluric_frequency_hz", 8.08)
                lithic_tension = t_data.get("parametric_vectors", {}).get("lithic_tension", 0.47)
                geomagnetic_flux = t_data.get("parametric_vectors", {}).get("geomagnetic_flux", 0.3333)
                print(f"[ACOUSTIC] Driven by live telemetry: f={telluric_f:.2f}Hz, tension={lithic_tension:.2f}, flux={geomagnetic_flux:.2f}")
        except Exception as e:
            print(f"[ACOUSTIC] Telemetry read fallback: {e}")
            
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    rng = random.Random(42020)
    two_pi = 2.0 * math.pi
    
    # Pre-generate noise buffer for fast filter computation
    noise_len = 96000
    noise_table = [rng.random() * 2.0 - 1.0 for _ in range(noise_len)]
    
    # Filter state variables
    lp_bubble = 0.0
    hp_vapor = 0.0
    
    f_cavity_base = 418.2 # 4.182 Kelvin base resonance
    f_telluric_harmonic = telluric_f * 4.0 # ~32.32 Hz
    
    print("[ACOUSTIC] Computing sub-Kelvin quantum soundscape...")
    
    for i in range(n_samples):
        t = i / sr
        prog = t / duration
        
        # Envelope: 4s fade in, 6s fade out
        env = 1.0
        if t < 4.0: env = t / 4.0
        elif t > (duration - 6.0): env = (duration - t) / 6.0
        
        # 1. Sub-Kelvin Whispering Gallery Modes (ultra-high Q cavity)
        # Slow Doppler micro-wobble from levitation height oscillation (~0.05 Hz)
        wobble = math.sin(two_pi * 0.05 * t) * (0.15 + 0.1 * geomagnetic_flux)
        f1 = f_cavity_base + wobble
        f2 = f_cavity_base * 2.0 - wobble * 0.5
        
        tone1 = math.sin(two_pi * f1 * t) * 0.22
        tone2 = math.sin(two_pi * f2 * t) * 0.12
        pure_cavity = tone1 + tone2
        
        # 2. Telluric Infrasound & Seismic Base (Schumann standing wave)
        # Deep pulsating bass drone
        sub_drone = math.sin(two_pi * f_telluric_harmonic * t) * 0.32
        sub_pulse = 0.7 + 0.3 * math.sin(two_pi * (telluric_f * 0.1) * t)
        telluric_hum = sub_drone * sub_pulse * (0.8 + 0.4 * lithic_tension)
        
        # 3. Liquid Helium Evaporative Hiss & Leidenfrost Cavitation
        raw_n = noise_table[i % noise_len]
        # Highpass for icy vapor hiss
        hp_vapor = 0.85 * (hp_vapor + raw_n - noise_table[(i - 1) % noise_len])
        vapor_hiss = hp_vapor * 0.035 * (0.6 + 0.4 * math.sin(two_pi * 0.2 * t))
        
        # 4. Abrikosov Quantum Flux Pinning Jumps (Barkhausen-like clicks)
        # Higher probability when geomagnetic flux / lithic tension peaks
        flux_click = 0.0
        click_threshold = 0.9985 - 0.001 * geomagnetic_flux
        if raw_n > click_threshold:
            flux_click = (raw_n - click_threshold) * 80.0
            
        # 5. Channel synthesis:
        # Left channel: Telluric planetary grounding, sub-bass, and flux-slip impulses
        sig_l = (telluric_hum * 1.2 + pure_cavity * 0.5 + flux_click * 0.8 + vapor_hiss * 0.4) * env
        
        # Right channel: Superconducting whispering gallery, high Q resonances, cryogenic vapor
        sig_r = (pure_cavity * 1.1 + telluric_hum * 0.4 + vapor_hiss * 1.2 + flux_click * 0.5) * env
        
        # Electromagnetic cross-induction
        left[i] = sig_l * 0.82 + sig_r * 0.18
        right[i] = sig_r * 0.82 + sig_l * 0.18
        
        if i % (sr * 30) == 0 and i > 0:
            print(f"[ACOUSTIC] Progress: {t:.0f}s / {duration}s ({prog*100:.1f}%) | Flux: {geomagnetic_flux:.2f}")
            
    # Normalize peak to -1.5 dB (approx 0.84)
    max_peak = max(max(abs(x) for x in left), max(abs(y) for y in right))
    if max_peak > 0:
        gain = 0.84 / max_peak
        print(f"[ACOUSTIC] Normalizing master suite (peak: {max_peak:.4f}, gain: {gain:.4f})...")
        left = [x * gain for x in left]
        right = [y * gain for y in right]
        
    out_wav = os.path.join(os.path.dirname(__file__), "telluric_flux_4k.wav")
    gallery_wav = os.path.join(studio_root, "gallery", "assets", "telluric_flux_4k.wav")
    
    print(f"[ACOUSTIC] Writing master 16-bit PCM WAV to {out_wav}...")
    write_wav(out_wav, left, right, sample_rate=sr)
    
    print(f"[ACOUSTIC] Mirroring master audio to gallery: {gallery_wav}...")
    shutil.copyfile(out_wav, gallery_wav)
    print(f"[ACOUSTIC] Telluric flux suite successfully synthesized and archived.")

if __name__ == "__main__":
    synthesize()

