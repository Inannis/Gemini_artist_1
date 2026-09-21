#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · SKETCHBOOK STUDY 022
Birefringence Polarimetry Sweep, Michel-Levy Interference & Bessel Plate Modal Dispersion
Series XXVIII · INQ-16 (The Deep-Time Reliquary) · September 21, 2026

Systematic parameter sweep exploring:
1. Cross-polarized Stokes-Mueller transmittance under rotating polarizer angles.
2. Form birefringence retardation delta_R in [0, 300 nm] with Michel-Levy chromatic dispersion.
3. Comparative Archimedean spiral track pitch vs voxel retardance capacity.
4. Bessel function eigenfunctions of free-edge circular fused-silica Kirchhoff-Love plate.
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def bessel_j0(x):
    """Zero-order Bessel function of the first kind J0(x)."""
    val = 0.0
    term = 1.0
    x_half_sq = (x * 0.5) ** 2
    for k in range(16):
        if k > 0:
            term *= -x_half_sq / (k * k)
        val += term
    return val

def bessel_j1(x):
    """First-order Bessel function of the first kind J1(x)."""
    val = 0.0
    term = x * 0.5
    x_half_sq = (x * 0.5) ** 2
    for k in range(1, 16):
        if k > 1:
            term *= -x_half_sq / ((k - 1) * k)
        val += term
    return val

def bessel_j2(x):
    """Second-order Bessel function J2(x) via recurrence."""
    if abs(x) < 1e-6:
        return 0.0
    return (2.0 / x) * bessel_j1(x) - bessel_j0(x)

def bessel_j3(x):
    """Third-order Bessel function J3(x)."""
    if abs(x) < 1e-6:
        return 0.0
    return (4.0 / x) * bessel_j2(x) - bessel_j1(x)

def michel_levy_rgb(retardance_nm):
    """
    Computes transmission under crossed linear polarizers for RGB primaries:
    Red (650 nm), Green (532 nm), Blue (450 nm).
    Formula: T_lambda = sin^2(pi * delta_R / lambda)
    """
    lambda_r = 650.0
    lambda_g = 532.0
    lambda_b = 450.0
    
    tr = math.sin(math.pi * retardance_nm / lambda_r) ** 2
    tg = math.sin(math.pi * retardance_nm / lambda_g) ** 2
    tb = math.sin(math.pi * retardance_nm / lambda_b) ** 2
    
    # Scale to 0-255 with slight gamma curve
    r = int(min(255, max(0, (tr ** 0.8) * 255.0)))
    g = int(min(255, max(0, (tg ** 0.8) * 255.0)))
    b = int(min(255, max(0, (tb ** 0.8) * 255.0)))
    return (r, g, b)

def render_sweep_plate():
    W, H = 1920, 1080
    buf = bytearray(W * H * 3)
    
    def set_pixel(x, y, r, g, b):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b

    # Background: Obsidian void with subtle coordinate grid
    for y in range(H):
        bg_val = int(6 + 8 * (1.0 - y / H))
        for x in range(W):
            # Subtle division lines at x = 960 and y = 540
            is_div_x = (abs(x - 960) < 2)
            is_div_y = (abs(y - 540) < 2)
            if is_div_x or is_div_y:
                set_pixel(x, y, 40, 60, 80)
            else:
                set_pixel(x, y, bg_val, bg_val + 2, bg_val + 6)

    # -------------------------------------------------------------
    # Quadrant 1 (Top-Left): Cross-Polarized Vector Azimuth Field
    # Center at (480, 270), Radius = 220
    # -------------------------------------------------------------
    cx1, cy1, r1 = 480, 270, 210
    for y in range(cy1 - r1 - 10, cy1 + r1 + 10):
        for x in range(cx1 - r1 - 10, cx1 + r1 + 10):
            dx = x - cx1
            dy = y - cy1
            dist = math.hypot(dx, dy)
            if dist <= r1:
                phi = math.atan2(dy, dx)
                # Slow-axis azimuth theta(r, phi) = 2.0 * phi + 0.5 * (dist / r1) * pi
                theta = 2.0 * phi + 0.5 * (dist / r1) * math.pi
                # Cross-polarized intensity: I = sin^2(2 * theta) * sin^2(pi * delta / lambda)
                # Vary retardance radially from 50nm to 240nm
                delta_r = 50.0 + 190.0 * (dist / r1)
                t_cross = (math.sin(2.0 * theta) ** 2)
                
                rgb = michel_levy_rgb(delta_r)
                # Modulate by crossed polarization
                r = int(rgb[0] * t_cross * (0.4 + 0.6 * (dist / r1)))
                g = int(rgb[1] * t_cross * (0.4 + 0.6 * (dist / r1)))
                b = int(rgb[2] * t_cross * (0.4 + 0.6 * (dist / r1)))
                
                # Glass disc rim highlight
                if abs(dist - r1) < 2.0:
                    r = min(255, r + 140)
                    g = min(255, g + 180)
                    b = min(255, b + 220)
                set_pixel(x, y, r, g, b)

    # -------------------------------------------------------------
    # Quadrant 2 (Top-Right): Michel-Lévy Retardance Spectrum Bar
    # Box from x in [1040, 1840], y in [120, 420]
    # -------------------------------------------------------------
    x_start, x_end = 1040, 1840
    y_start, y_end = 140, 400
    for x in range(x_start, x_end):
        frac_x = (x - x_start) / (x_end - x_start)
        # Retardance from 0 nm to 600 nm across 1st and 2nd orders
        retardance = frac_x * 650.0
        rgb = michel_levy_rgb(retardance)
        for y in range(y_start, y_end):
            # Intensity modulation across vertical axis to show analyzer extinction
            frac_y = (y - y_start) / (y_end - y_start)
            # Extinction brush simulation
            brush_mod = math.sin(frac_y * math.pi) ** 0.5
            r = int(rgb[0] * brush_mod)
            g = int(rgb[1] * brush_mod)
            b = int(rgb[2] * brush_mod)
            set_pixel(x, y, r, g, b)

    # -------------------------------------------------------------
    # Quadrant 3 (Bottom-Left): Archimedean Spiral 5D Data Tracks
    # Center at (480, 810), Radius = 210
    # -------------------------------------------------------------
    cx3, cy3, r3 = 480, 810, 210
    # Render disc backdrop
    for y in range(cy3 - r3 - 5, cy3 + r3 + 5):
        for x in range(cx3 - r3 - 5, cx3 + r3 + 5):
            dist = math.hypot(x - cx3, y - cy3)
            if dist <= r3:
                set_pixel(x, y, 12, 16, 24)
            if abs(dist - r3) < 1.5:
                set_pixel(x, y, 56, 120, 180)

    # Plot 28 Archimedean spiral turns with voxel retardance color
    for theta_deg in range(0, 360 * 28, 2):
        theta_rad = math.radians(theta_deg)
        # Archimedean formula: r = a + b * theta
        r_spiral = 15.0 + (r3 - 25.0) * (theta_rad / (math.radians(360 * 28)))
        px = int(cx3 + r_spiral * math.cos(theta_rad))
        py = int(cy3 + r_spiral * math.sin(theta_rad))
        
        # 5D Voxel payload modulation: alternate retardance and azimuth
        voxel_id = theta_deg // 4
        retardance = 60.0 + 160.0 * (0.5 + 0.5 * math.sin(voxel_id * 0.15))
        rgb = michel_levy_rgb(retardance)
        set_pixel(px, py, rgb[0], rgb[1], rgb[2])
        # Slight line thickness
        set_pixel(px + 1, py, rgb[0] // 2, rgb[1] // 2, rgb[2] // 2)

    # -------------------------------------------------------------
    # Quadrant 4 (Bottom-Right): Bessel Plate Modal Chladni Patterns
    # Center at (1440, 810), Radius = 210
    # Modes (2, 0) and (0, 1) superposition: W(r, phi) = J2(k r) cos(2 phi) + 0.6 J0(k r)
    # -------------------------------------------------------------
    cx4, cy4, r4 = 1440, 810, 210
    for y in range(cy4 - r4 - 10, cy4 + r4 + 10):
        for x in range(cx4 - r4 - 10, cx4 + r4 + 10):
            dx = x - cx4
            dy = y - cy4
            dist = math.hypot(dx, dy)
            if dist <= r4:
                norm_r = (dist / r4) * 5.136 # First root scale
                phi = math.atan2(dy, dx)
                # Mode superposition
                w_disp = bessel_j2(norm_r) * math.cos(2.0 * phi) + 0.45 * bessel_j0(norm_r)
                
                # Nodal line proximity (Chladni dust concentration)
                nodal_prox = math.exp(-(abs(w_disp) / 0.06) ** 2)
                
                # Color field: positive displacement cyan, negative magenta, nodal line brilliant gold
                disp_norm = max(-1.0, min(1.0, w_disp / 0.4))
                if disp_norm > 0:
                    r = int(20 + 60 * disp_norm)
                    g = int(30 + 150 * disp_norm)
                    b = int(60 + 180 * disp_norm)
                else:
                    neg = -disp_norm
                    r = int(60 + 160 * neg)
                    g = int(20 + 40 * neg)
                    b = int(50 + 120 * neg)
                
                # Add Chladni nodal gold dust
                if nodal_prox > 0.05:
                    gold_r = int(240 * nodal_prox)
                    gold_g = int(200 * nodal_prox)
                    gold_b = int(80 * nodal_prox)
                    r = min(255, r + gold_r)
                    g = min(255, g + gold_g)
                    b = min(255, b + gold_b)
                
                if abs(dist - r4) < 2.0:
                    r = min(255, r + 180)
                    g = min(255, g + 210)
                    b = min(255, b + 240)
                set_pixel(x, y, r, g, b)

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_022_polarimetry_sweep_plate.png"))
    write_png(out_path, W, H, buf)
    print(f"[STUDY-022] Master parameter sweep plate rendered to {out_path}")

def render_acoustic_sweep():
    """
    Synthesizes a 30-second 48kHz stereo acoustic sweep of fused silica plate Bessel modes:
    - Fundamental Euler-Bernoulli mode (0, 1) breathing: 43.2 Hz
    - Chladni cross mode (2, 0): 89.4 Hz
    - Chladni hexagram mode (3, 0): 235.4 Hz
    - 1st circular overtone (1, 1): 348.0 Hz
    - High-order glass bell chimes: 1728 Hz, 2592 Hz, 3456 Hz
    - High Q reverberation (Q = 10^7) modeled with exponential ringdown envelopes
    """
    sr = 48000
    duration_s = 30.0
    n_samples = int(sr * duration_s)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    # Mode definitions: (freq, amplitude, decay_tau, stereo_pan, phase_offset)
    modes = [
        (43.2, 0.40, 28.0, 0.0, 0.0),      # Fundamental sub-drone
        (89.4, 0.28, 22.0, -0.2, 0.4),     # Mode (2, 0) cross
        (89.8, 0.25, 22.0, 0.2, 1.2),      # Degenerate pair split (0.4 Hz beat)
        (235.4, 0.20, 18.0, 0.35, 0.8),    # Mode (3, 0) hexagram
        (348.0, 0.16, 14.0, -0.4, 1.5),    # Mode (1, 1) circular overtone
        (584.2, 0.12, 12.0, 0.15, 0.2),    # Mode (0, 2)
        (1728.0, 0.10, 8.0, -0.6, 2.1),    # 5th harmonic bell chime
        (2592.0, 0.07, 6.0, 0.6, 0.7),     # Crystalline harmonic
        (3456.0, 0.05, 4.5, -0.1, 1.9)     # Ultra-high glass shimmer
    ]
    
    # Synthesize continuous evolving field
    for t_idx in range(n_samples):
        t = t_idx / sr
        
        # Periodic excitation pulses (sub-femtosecond plasma spark strike every 6.0 seconds)
        strike_period = 6.0
        strike_t = t % strike_period
        strike_env = math.exp(-strike_t * 1.5)
        
        sample_l = 0.0
        sample_r = 0.0
        
        for f, amp, tau, pan, phase in modes:
            # Continuous resonant ringdown
            decay = math.exp(-t / tau)
            osc = math.sin(2.0 * math.pi * f * t + phase)
            
            # Additional strike excitation
            transient = strike_env * math.sin(2.0 * math.pi * f * strike_t * 1.002)
            
            signal = (osc * decay * 0.7 + transient * 0.3) * amp
            
            # Stereo panning: pan in [-1, 1]
            gain_l = 0.5 * (1.0 - pan)
            gain_r = 0.5 * (1.0 + pan)
            sample_l += signal * gain_l
            sample_r += signal * gain_r
            
        # Subtle vacuum thermal hiss (-48 dB floor)
        noise = (math.sin(t * 12345.67) * 43758.5453) % 1.0 - 0.5
        noise_gain = 0.003
        sample_l += noise * noise_gain
        sample_r += noise * noise_gain
        
        left[t_idx] = max(-0.95, min(0.95, sample_l))
        right[t_idx] = max(-0.95, min(0.95, sample_r))
        
    out_wav = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_022_modal_sweep.wav"))
    write_wav(out_wav, left, right, sr)
    print(f"[STUDY-022] Master acoustic sweep synthesized to {out_wav}")

if __name__ == "__main__":
    print("[+] Executing Study 022: Birefringence Polarimetry & Bessel Modal Sweep...")
    render_sweep_plate()
    render_acoustic_sweep()
    print("[✓] Study 022 execution complete.")

