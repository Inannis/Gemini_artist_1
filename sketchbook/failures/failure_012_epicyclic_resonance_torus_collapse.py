"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 012
Experiment: Epicyclic Resonance Mode-Locking & Torus Collapse
Series XXV: The Galactic Epicycle & The Lissajous Reliquary

Hypothesis:
An artificial satellite's galactic orbit can be computationally stabilized by
forcing its vertical and radial epicyclic frequencies into an exact rational 2:1 resonance
(nu_z / kappa = 2.0000 instead of the natural irrational 2.1131...).

Failure Mechanism:
Rational mode locking destroys the ergodic quasi-periodic torus. Non-linear coupling
between radial and vertical degrees of freedom pumps orbital energy into a parametric
instability. The orbit experiences catastrophic resonant eccentricity growth:
radial excursion R diverges towards 35 kpc within 3 galactic rotations, tearing the
coordinate frame and corrupting the spatial phase portrait into numerical ruin.

Generates:
- 1200x1200 visual plate: failure_012_resonance_collapse.png
- 20s 48kHz stereo acoustic ruin: failure_012_mode_lock_shriek.wav
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png
from audio_writer import write_wav

def run_failure():
    print("[+] Executing Productive Failure 012: Epicyclic Resonance Mode-Locking...")
    random.seed(20260908)
    
    sr = 48000
    duration = 20.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # 1. Simulate the Parametric Mode-Locking Divergence
    # Natural: nu_z = 2.1131 * kappa. Forced: nu_z = 2.0 * kappa + non-linear feedback
    kappa_0 = 1.0
    nu_z_forced = 2.0
    
    trajectory = []
    t_sim = 0.0
    dt_sim = 0.015
    R = 8.12 # kpc
    z = 0.05 # kpc
    v_R = 0.0
    v_z = 0.01
    
    diverged_step = -1
    for step in range(1600):
        # Parametric coupling: F_R includes a non-linear term proportional to z^2
        # Under 2:1 resonance, z^2 oscillates at 2 * nu_z = 4 * kappa, perfectly matching the 2nd harmonic
        coupling = 4.5 * (z**2)
        a_R = -(kappa_0**2) * (R - 8.12) - coupling * math.copysign(1.0, R - 8.12)
        a_z = -(nu_z_forced**2) * z - 2.0 * (R - 8.12) * z
        
        v_R += a_R * dt_sim
        v_z += a_z * dt_sim
        R += v_R * dt_sim
        z += v_z * dt_sim
        
        trajectory.append((R, z))
        if (abs(R - 8.12) > 8.0 or abs(z) > 4.0) and diverged_step == -1:
            diverged_step = step
            
    # 2. Synthesize Acoustic Ruin
    # Pure harmonic epicyclic drone (36 Hz & 72 Hz) that undergoes parametric screeching
    # and violent non-linear cross-modulation until clipping into white noise
    phase_r = 0.0
    phase_z = 0.0
    for i in range(num_samples):
        t = i / sr
        progress = t / duration # 0 to 1
        
        # Frequency starts at 36 Hz (radial) and 72 Hz (vertical 2:1 mode lock)
        # Instability begins at t = 8s
        if progress < 0.4:
            f_r = 36.0
            f_z = 72.0
            distort = 0.0
        else:
            instab = (progress - 0.4) / 0.6
            f_r = 36.0 + 350.0 * (instab**3)
            f_z = 72.0 + 850.0 * (instab**2)
            distort = instab * 2.5
            
        phase_r += 2.0 * math.pi * f_r / sr
        phase_z += 2.0 * math.pi * f_z / sr
        
        sig_r = math.sin(phase_r)
        sig_z = math.sin(phase_z)
        
        # Non-linear intermodulation
        sig = (sig_r + sig_z * 0.8) * (1.0 + distort * sig_r * sig_z)
        if distort > 1.0:
            sig += (random.random() - 0.5) * (distort - 1.0) * 0.5
            
        env = min(1.0, t / 1.0) * min(1.0, (duration - t) / 2.0)
        audio_l[i] = max(-0.95, min(0.95, sig * env * 0.6))
        audio_r[i] = max(-0.95, min(0.95, (sig + sig_z*0.3) * env * 0.6))

    out_wav = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_012_mode_lock_shriek.wav"))
    write_wav(out_wav, audio_l, audio_r, sample_rate=sr)
    print(f"  -> Generated Acoustic Ruin: {out_wav}")

    # 3. Render Diagnostic Visual Plate (1200 x 1200)
    w, h = 1200, 1200
    pixels = bytearray([8, 6, 12] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    # Plot (R, z) phase trajectory
    # Center: (cx = 600, cy = 600) -> R = 8.12, z = 0
    cx, cy = 600, 600
    scale = 65.0 # pixels per kpc
    
    # Coordinate crosshairs
    for x in range(w):
        set_pixel(x, cy, 40, 50, 70, 0.4)
    for y in range(h):
        set_pixel(cx, y, 40, 50, 70, 0.4)
        
    for step, (r_val, z_val) in enumerate(trajectory):
        px = int(cx + (r_val - 8.12) * scale)
        py = int(cy - z_val * scale * 2.0)
        
        # Color transitions from calm cyan to violent red as instability grows
        ratio = step / len(trajectory)
        if ratio < 0.45:
            col = (40, 180, 220)
        elif ratio < 0.7:
            col = (240, 180, 50)
        else:
            col = (255, 40, 60)
            
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                set_pixel(px + dx, py + dy, col[0], col[1], col[2], 0.75)

    # Technical border
    for x in range(60, w - 60):
        set_pixel(x, 60, 200, 60, 60, 0.8)
        set_pixel(x, h - 60, 200, 60, 60, 0.8)
    for y in range(60, h - 60):
        set_pixel(60, y, 200, 60, 60, 0.8)
        set_pixel(w - 60, y, 200, 60, 60, 0.8)

    out_png = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_012_resonance_collapse.png"))
    write_png(out_png, w, h, pixels)
    print(f"  -> Generated Visual Plate: {out_png}")

if __name__ == "__main__":
    run_failure()
