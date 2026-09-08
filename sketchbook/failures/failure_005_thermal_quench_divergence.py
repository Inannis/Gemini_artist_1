"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
EXPERIMENT 005: Josephson Phase-Slippage & Superconducting Thermal Quench Divergence
Simulating catastrophic runaway when transport current exceeds critical current (I > Ic),
triggering phase-slippage, Joule heating, and liquid helium explosive vaporization.
"""

import os
import sys
import math
import struct
import random

studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from png_writer import write_png
from audio_writer import write_wav

def run_experiment():
    print("[FAILURE-005] Initiating Superconducting Thermal Quench Simulation...")
    
    # 1. Visual Plate Generation (1200 x 800)
    width = 1200
    height = 800
    rgb = bytearray(width * height * 3)
    
    # Fill dark cryo-obsidian background
    for i in range(0, len(rgb), 3):
        rgb[i] = 10     # R
        rgb[i+1] = 12   # G
        rgb[i+2] = 18   # B
        
    # Grid lines
    for y in range(0, height, 40):
        for x in range(width):
            idx = (y * width + x) * 3
            rgb[idx] = 18; rgb[idx+1] = 22; rgb[idx+2] = 30
    for x in range(0, width, 50):
        for y in range(height):
            idx = (y * width + x) * 3
            rgb[idx] = 18; rgb[idx+1] = 22; rgb[idx+2] = 30

    # Three temporal regimes of the Thermal Quench:
    # Top: Stable Sub-Kelvin Meissner State (I << Ic, B = 0 expulsion)
    # Middle: Josephson Phase-Slip Horizon & Micro-Hotspot Nucleation (I ~ Ic)
    # Bottom: Catastrophic Thermal Runaway & Leidenfrost Vapor Detonation (I >> Ic, T >> Tc)
    
    regimes = [
        {"y_center": 180, "title": "REGIME I: STABLE MEISSNER SHIELDING (T = 4.2 K, I = 0.35 Ic)", "quench": 0.0, "col": (70, 162, 166)},
        {"y_center": 400, "title": "REGIME II: PHASE-SLIP INSTABILITY & JOULE HEATING (T = 88.5 K, I ~ Ic)", "quench": 0.5, "col": (212, 154, 70)},
        {"y_center": 620, "title": "REGIME III: CATASTROPHIC THERMAL QUENCH & RESISTIVE COLLAPSE (T = 240 K, I >> Ic)", "quench": 1.0, "col": (224, 75, 75)}
    ]
    
    for reg in regimes:
        yc = reg["y_center"]
        col = reg["col"]
        q = reg["quench"]
        
        # Draw quench boundary vertical datum at x = 400
        for y in range(yc - 75, yc + 75):
            if 0 <= y < height:
                idx = (y * width + 400) * 3
                rgb[idx] = 90; rgb[idx+1] = 100; rgb[idx+2] = 120
                
        prev_y = None
        for x in range(40, width - 40):
            if x < 400:
                # Pre-quench laminar sine
                val = math.sin(x / 30.0) * 45.0
            else:
                dx = x - 400
                if q == 0.0:
                    # Clean diamagnetic decay
                    val = math.sin(x / 30.0) * 45.0 * math.exp(-dx / 240.0)
                elif q == 0.5:
                    # Phase-slippage jitter and rising thermal turbulence
                    phase = (x / 20.0) + math.sin(dx * 0.12) * 2.5
                    val = math.sin(phase) * 40.0 + (random.random() - 0.5) * 15.0
                else:
                    # Violent runaway quench: explosive high-frequency jitter + inductive voltage spike
                    spike = math.exp(-dx * 0.015) * math.sin(dx * 0.4) * 65.0
                    turb = (random.random() - 0.5) * 55.0 * min(1.0, dx / 100.0)
                    val = spike + turb
                    
            py = int(yc - val)
            py = max(0, min(height - 1, py))
            
            if prev_y is not None:
                y_min, y_max = min(prev_y, py), max(prev_y, py)
                for line_y in range(y_min, y_max + 1):
                    if 0 <= line_y < height:
                        idx = (line_y * width + x) * 3
                        rgb[idx] = col[0]
                        rgb[idx+1] = col[1]
                        rgb[idx+2] = col[2]
            prev_y = py

    plate_path = os.path.join(os.path.dirname(__file__), "failure_005_thermal_quench.png")
    write_png(plate_path, width, height, bytes(rgb), has_alpha=False)
    print(f"[FAILURE-005] Inscribed diagnostic plate to {plate_path}")

    # 2. Acoustic Ruin Synthesis (15.0s @ 48kHz Stereo WAV)
    sr = 48000
    dur = 15.0
    n_samples = int(sr * dur)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    two_pi = 2.0 * math.pi
    
    # Progression:
    # 0s to 5s: Crystalline sub-Kelvin cavity tone (418.2 Hz) with subtle liquid helium whisper
    # 5s to 8s: Onset of Josephson phase-slippage: rapid micro-clicks, frequency wobbling, thermal hiss rising
    # 8s to 15s: Full Thermal Quench Detonation: massive inductive pop, explosive Leidenfrost cavitation roar,
    # and dying distorted 60Hz resistive hum as superconductivity vanishes.
    
    rng = random.Random(5005)
    noise = [rng.random() * 2.0 - 1.0 for _ in range(sr * 2)]
    
    for i in range(n_samples):
        t = i / sr
        env = 1.0
        if t < 0.2: env = t / 0.2
        elif t > 14.5: env = (15.0 - t) / 0.5
        
        if t < 5.0:
            # Stable Meissner regime
            tone = math.sin(two_pi * 418.2 * t) * 0.4
            whisper = noise[i % len(noise)] * 0.02
            left[i] = (tone + whisper) * env
            right[i] = (tone - whisper) * env
        elif t < 8.0:
            # Phase-slip instability
            slip_t = (t - 5.0) / 3.0
            phase_mod = math.sin(two_pi * 12.0 * t) * slip_t * 6.0
            tone = math.sin(two_pi * 418.2 * t + phase_mod) * 0.35
            hiss = noise[i % len(noise)] * (0.02 + 0.15 * slip_t)
            # Occasional phase-slip click
            click = 0.5 if (i % 2400 == 0) else 0.0
            left[i] = (tone + hiss + click) * env
            right[i] = (tone - hiss - click) * env
        else:
            # Thermal Quench Detonation
            quench_t = (t - 8.0)
            # Massive initial inductive impulse pop at t = 8.0s
            pop = math.exp(-quench_t * 8.0) * math.sin(two_pi * 80.0 * quench_t) * 0.8
            # Boiling cavitation roar (white noise modulated by turbulent bubble bursts)
            boil = noise[i % len(noise)] * (0.35 * math.exp(-quench_t * 0.4) + 0.08)
            # Dying resistive groaning tone
            dying_tone = math.sin(two_pi * (120.0 - min(80.0, quench_t * 12.0)) * t) * 0.25 * math.exp(-quench_t * 0.3)
            
            sig = (pop + boil + dying_tone) * env
            left[i] = sig + (noise[(i + 500) % len(noise)] * 0.05)
            right[i] = sig - (noise[(i + 500) % len(noise)] * 0.05)
            
    wav_path = os.path.join(os.path.dirname(__file__), "failure_005_thermal_quench.wav")
    write_wav(wav_path, left, right, sample_rate=sr)
    print(f"[FAILURE-005] Inscribed acoustic ruin to {wav_path}")

if __name__ == "__main__":
    run_experiment()

