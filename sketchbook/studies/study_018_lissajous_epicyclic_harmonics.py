"""
STUDIO ANAMNESIS · EXPLORATORY STUDY 018
Study: The Lissajous Epicyclic Harmonics (Incommensurate Frequencies & Sputtering Clicks)
Series XXV: The Galactic Epicycle & The Lissajous Reliquary

Mathematical Investigation:
1. Incommensurate Frequency Pairing:
   - Radial Epicycle: f_kappa = 36.0 Hz
   - Vertical Epicycle: f_nu = 36.0 * 2.1131 = 76.0716 Hz
   - Azimuthal Orbital Carrier: f_omega = 26.55 Hz
   - Interference produces an aperiodic, non-repeating phase beat envelope.
2. Interstellar Dust Micro-Acoustics:
   - Poisson process of micro-grain impacts (grain mass 10^-15 to 10^-12 kg at 25 km/s)
   - Resonant piezo-acoustic shock pulses (2,200 - 4,800 Hz) simulating lattice erosion.
3. Generates 1200x1200 visual plate and 20s 48kHz stereo acoustic study.
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png
from audio_writer import write_wav

def run_study():
    print("[+] Executing Study 018: Lissajous Epicyclic Harmonics Simulation...")
    random.seed(20260908)
    
    sr = 48000
    duration = 20.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # 1. Synthesize Incommensurate Epicyclic Soundscape
    f_kappa = 36.0
    f_nu = 36.0 * 2.113116 # 76.072 Hz
    f_omega = 26.55
    
    phase_k = 0.0
    phase_nu = 0.0
    phase_om = 0.0
    
    # Pre-generate dust grain micro-impacts
    num_impacts = 45
    impacts = []
    for _ in range(num_impacts):
        t_imp = random.uniform(0.5, 19.5)
        f_imp = random.uniform(2200.0, 4800.0)
        amp_imp = random.uniform(0.04, 0.18)
        dur_imp = random.uniform(0.015, 0.05)
        pan_imp = random.uniform(0.1, 0.9)
        impacts.append((t_imp, f_imp, amp_imp, dur_imp, pan_imp))

    for i in range(num_samples):
        t = i / sr
        
        phase_k += 2.0 * math.pi * f_kappa / sr
        phase_nu += 2.0 * math.pi * f_nu / sr
        phase_om += 2.0 * math.pi * f_omega / sr
        
        # Incommensurate Lissajous interference
        sig_k = math.sin(phase_k) * 0.35
        sig_nu = math.sin(phase_nu) * 0.28
        sig_om = math.sin(phase_om) * 0.20
        
        # Slow spatial panning based on irrational phase drift
        pan_mod = 0.5 + 0.4 * math.sin(phase_nu - 2.0 * phase_k)
        
        sig_base_l = (sig_k + sig_nu * 0.9 + sig_om) * (1.0 - pan_mod * 0.5)
        sig_base_r = (sig_k + sig_nu * 1.1 + sig_om) * (0.5 + pan_mod * 0.5)
        
        audio_l[i] = sig_base_l
        audio_r[i] = sig_base_r

    # Add dust impact transients
    for t_imp, f_imp, amp_imp, dur_imp, pan_imp in impacts:
        start_idx = int(t_imp * sr)
        n_imp_samp = int(dur_imp * sr)
        for s in range(n_imp_samp):
            idx = start_idx + s
            if idx < num_samples:
                dt = s / sr
                decay = math.exp(-dt * 90.0)
                osc = math.sin(2.0 * math.pi * f_imp * dt) * decay * amp_imp
                audio_l[idx] += osc * (1.0 - pan_imp)
                audio_r[idx] += osc * pan_imp

    # Apply master envelope
    for i in range(num_samples):
        t = i / sr
        env = min(1.0, t / 1.5) * min(1.0, (duration - t) / 2.5)
        audio_l[i] = max(-0.95, min(0.95, audio_l[i] * env))
        audio_r[i] = max(-0.95, min(0.95, audio_r[i] * env))

    out_wav = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_018_lissajous_harmonics.wav"))
    write_wav(out_wav, audio_l, audio_r, sample_rate=sr)
    print(f"  -> Generated Acoustic Study: {out_wav}")

    # 2. Render Diagnostic Visual Plate (1200 x 1200)
    w, h = 1200, 1200
    pixels = bytearray([5, 8, 14] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    # Plot incommensurate Lissajous figure in (Delta R, z) space
    # Delta R = X * cos(kappa * t), z = Z * cos(nu_z * t)
    cx, cy = 600, 600
    X_amp = 480.0
    Z_amp = 400.0
    ratio = 2.113116
    
    # Grid lines
    for x in range(0, w, 100):
        for y in range(h):
            if y % 4 == 0: set_pixel(x, y, 25, 35, 50, 0.3)
    for y in range(0, h, 100):
        for x in range(w):
            if x % 4 == 0: set_pixel(x, y, 25, 35, 50, 0.3)

    # Draw 4,000 continuous steps of the non-closing Lissajous path
    prev_px, prev_py = None, None
    for step in range(12000):
        t_val = step * 0.015
        x_val = X_amp * math.cos(t_val)
        y_val = Z_amp * math.sin(ratio * t_val + 0.3)
        
        px = int(cx + x_val)
        py = int(cy - y_val)
        
        # Color cycles slowly along the ergodic path
        hue_phase = (step / 12000.0) * 3.0
        r_c = int(80 + 120 * math.sin(hue_phase))
        g_c = int(140 + 100 * math.cos(hue_phase))
        b_c = int(220 + 35 * math.sin(hue_phase * 2.0))
        
        set_pixel(px, py, r_c, g_c, b_c, 0.6)
        if prev_px is not None:
            # Interpolate segment
            for a in [0.25, 0.5, 0.75]:
                ix = int(prev_px * (1 - a) + px * a)
                iy = int(prev_py * (1 - a) + py * a)
                set_pixel(ix, iy, r_c, g_c, b_c, 0.4)
        prev_px, prev_py = px, py

    # Draw dust impact craters (small points of micro-abrasion)
    for t_imp, _, _, _, _ in impacts:
        # Map to an impact coordinate along the trajectory
        t_val = t_imp * 6.0
        ix = int(cx + X_amp * math.cos(t_val))
        iy = int(cy - Z_amp * math.sin(ratio * t_val + 0.3))
        for cr in range(4):
            for st in range(12):
                th = st * (2.0 * math.pi / 12.0)
                set_pixel(int(ix + cr * math.cos(th)), int(iy + cr * math.sin(th)), 255, 230, 120, 0.8)

    out_png = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_018_lissajous_plate.png"))
    write_png(out_png, w, h, pixels)
    print(f"  -> Generated Visual Plate: {out_png}")

if __name__ == "__main__":
    run_study()
