"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
EXPERIMENT 004: Electromagnetic Skin Depth Discretization Divergence
Simulating spatial Nyquist breakdown when grid resolution exceeds physical skin depth:
Delta_x > delta = sqrt(2 / (omega * mu * sigma))
"""

import os
import sys
import math
import struct
import zlib

studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from png_writer import write_png
from audio_writer import write_wav

def run_experiment():
    print("[FAILURE-004] Initiating Skin Depth Discretization Divergence...")
    
    # 1. Visual Plate Generation (1200 x 800)
    width = 1200
    height = 800
    rgb = bytearray(width * height * 3)
    
    # Fill dark slate background
    for i in range(0, len(rgb), 3):
        rgb[i] = 10     # R
        rgb[i+1] = 12   # G
        rgb[i+2] = 15   # B
        
    # Grid lines
    for y in range(0, height, 40):
        for x in range(width):
            idx = (y * width + x) * 3
            rgb[idx] = 18; rgb[idx+1] = 22; rgb[idx+2] = 28
    for x in range(0, width, 50):
        for y in range(height):
            idx = (y * width + x) * 3
            rgb[idx] = 18; rgb[idx+1] = 22; rgb[idx+2] = 28

    # Three temporal regimes:
    # Top: Stable Evanescent Decay (Delta_x << delta)
    # Middle: Marginal Discretization Boundary (Delta_x ~ delta)
    # Bottom: Catastrophic Spatial Divergence (Delta_x >> delta)
    
    regimes = [
        {"y_center": 180, "title": "REGIME I: STABLE EVANESCENT ABSORPTION (delta = 4.2 * Delta_x)", "sigma": 0.2, "diverge": False, "col": (70, 162, 166)},
        {"y_center": 400, "title": "REGIME II: MARGINAL BOUNDARY & PHASE JITTER (delta = 1.05 * Delta_x)", "sigma": 1.0, "diverge": False, "col": (212, 154, 70)},
        {"y_center": 620, "title": "REGIME III: SPATIAL NYQUIST BLOW-UP & CHECKERBOARD CATASTROPHE (Delta_x >> delta)", "sigma": 8.0, "diverge": True, "col": (224, 75, 75)}
    ]
    
    for reg in regimes:
        yc = reg["y_center"]
        col = reg["col"]
        div = reg["diverge"]
        
        # Interface line at x = 300
        for y in range(yc - 80, yc + 80):
            if 0 <= y < height:
                idx = (y * width + 300) * 3
                rgb[idx] = 80; rgb[idx+1] = 80; rgb[idx+2] = 90
                
        # Draw wave curve
        prev_y = None
        for x in range(40, width - 40):
            # Left of interface: incident sinusoidal carrier
            if x < 300:
                phase = (x / 25.0)
                val = math.sin(phase) * 55.0
            else:
                dx = (x - 300)
                if not div:
                    # Physical exponential decay
                    decay = math.exp(-dx / (60.0 / reg["sigma"]))
                    val = math.sin(dx / 15.0) * 55.0 * decay
                else:
                    # Numerical discretization instability: alternating sign flip and explosion
                    grid_step = dx // 8
                    instability = ((-1.0) ** grid_step) * min(75.0, math.exp(dx * 0.035) * 1.5)
                    jitter = math.sin(dx * 1.4) * 20.0
                    val = instability + jitter
                    
            py = int(yc - val)
            py = max(0, min(height - 1, py))
            
            # Plot line
            if prev_y is not None:
                y_min, y_max = min(prev_y, py), max(prev_y, py)
                for line_y in range(y_min, y_max + 1):
                    if 0 <= line_y < height:
                        idx = (line_y * width + x) * 3
                        rgb[idx] = col[0]
                        rgb[idx+1] = col[1]
                        rgb[idx+2] = col[2]
            prev_y = py

    plate_path = os.path.join(os.path.dirname(__file__), "failure_004_skin_depth_divergence.png")
    write_png(plate_path, width, height, bytes(rgb), has_alpha=False)
    print(f"[FAILURE-004] Inscribed diagnostic plate to {plate_path}")

    # 2. Acoustic Ruin Synthesis (12.0s @ 48kHz Stereo WAV)
    sr = 48000
    dur = 12.0
    n_samples = int(sr * dur)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    two_pi = 2.0 * math.pi
    
    # Acoustic progression:
    # 0s to 4s: Clean carrier tone (220 Hz) with soft physical absorption
    # 4s to 7s: Infiltration of spatial discretization grit, rising phase jitter
    # 7s to 12s: Catastrophic numerical checkerboard scream: alternating sample sign flips,
    # non-conservative energy accumulation, high-frequency aliased shrieking.
    
    for i in range(n_samples):
        t = i / sr
        
        # Envelope
        env = 1.0
        if t < 0.2: env = t / 0.2
        elif t > 11.5: env = (12.0 - t) / 0.5
        
        if t < 4.0:
            # Clean regime
            tone = math.sin(two_pi * 220.0 * t) * 0.5
            decay_filt = math.exp(-t * 0.4)
            left[i] = tone * decay_filt * env
            right[i] = math.sin(two_pi * 220.0 * t + 0.3) * decay_filt * env
        elif t < 7.0:
            # Transition regime: rising phase jitter and harmonic grit
            jitter_amt = (t - 4.0) / 3.0
            phase = two_pi * 220.0 * t + math.sin(two_pi * 1800.0 * t) * jitter_amt * 0.8
            tone = math.sin(phase) * 0.45
            grit = (math.sin(two_pi * 4400.0 * t) if (i % 6 < 3) else -math.sin(two_pi * 4400.0 * t)) * jitter_amt * 0.2
            left[i] = (tone + grit) * env
            right[i] = (tone - grit) * env
        else:
            # Divergence regime: spatial Nyquist collapse
            div_t = (t - 7.0) / 5.0
            # Alternating sample sign flip (checkerboard mode at Nyquist frequency: sr/2 = 24kHz)
            nyquist_flip = (1.0 if (i % 2 == 0) else -1.0) * (0.2 + 0.3 * div_t)
            # Aliased subharmonic drone
            screech = math.sin(two_pi * (1200.0 + div_t * 5400.0) * t) * 0.3
            # Blowup flutter
            flutter = math.sin(two_pi * (14.0 + div_t * 60.0) * t)
            left[i] = ((nyquist_flip * 0.6) + screech * flutter) * env * 0.7
            right[i] = ((-nyquist_flip * 0.6) + screech * (-flutter)) * env * 0.7

    wav_path = os.path.join(os.path.dirname(__file__), "failure_004_skin_depth_divergence.wav")
    write_wav(wav_path, left, right, sample_rate=sr)
    print(f"[FAILURE-004] Inscribed acoustic ruin to {wav_path}")

if __name__ == "__main__":
    run_experiment()
