#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
Experiment 001: Non-Linear Resonance Divergence & IEEE-754 Collapse

Hypothesis:
We attempted to model an acoustic waveguide resonator with high-order cubic-quintic
non-linear stiffness to simulate physical distortion in mineral plates:
f(u) = alpha * u^3 - beta * u^5

The Intended Outcome:
Rich harmonic saturation and microtonal distortion similar to overdriven volcanic slate.

The Reality / The Failure:
Beyond an excitation threshold (|u| > 1.25), the quintic softening term (-beta * u^5)
overwhelms the restoring stiffness and turns negative, accelerating outward.
The Courant-Friedrichs-Lewy stability criterion shatters.
Numerical values explode exponentially (10^3 -> 10^12 -> 10^150 -> inf -> NaN).

This script records this collapse visually (phase space portrait & waveform)
and acoustically using pure Python without external library dependencies.
"""

import math
import os
import random
import sys

# Import studio tools
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from png_writer import write_png
from audio_writer import write_wav

def run_simulation():
    print("[FAILURE-001] Running non-linear waveguide simulation...")
    n_steps = 3000
    nx = 120
    dt = 0.0004
    dx = 0.01
    c = 1.0
    gamma = 0.015
    alpha = 5.0  # Cubic stiffening
    beta = 3.2   # Quintic softening (instability trigger)

    # State vectors
    x = [i / (nx - 1) for i in range(nx)]
    # Sharp initial pluck
    u_curr = [math.exp(-((xi - 0.45) ** 2) / (2 * (0.04 ** 2))) for xi in x]
    u_prev = list(u_curr)
    u_next = [0.0] * nx

    center_history = []
    energy_history = []
    collapse_step = None
    spatial_snapshots = []

    for step in range(n_steps):
        # Record center node
        center_val = u_curr[nx // 2]
        center_history.append(center_val)

        if step % 250 == 0:
            spatial_snapshots.append((step, list(u_curr)))

        # Check for numeric runaway
        if math.isnan(center_val) or math.isinf(center_val) or abs(center_val) > 1e6:
            if collapse_step is None:
                collapse_step = step
                print(f"[FAILURE-001] !!! NUMERICAL DIVERGENCE at step {step}! Value: {center_val}")
            # Stop simulation once entered NaN/overflow
            break

        # Spatial finite difference & time update
        kin_e = 0.0
        pot_e = 0.0
        for i in range(1, nx - 1):
            d2u = (u_curr[i + 1] - 2 * u_curr[i] + u_curr[i - 1]) / (dx * dx)
            v = (u_curr[i] - u_prev[i]) / dt
            u = u_curr[i]
            
            # Non-linear restoring force
            f_nl = alpha * (u ** 3) - beta * (u ** 5)

            u_next_val = 2 * u - u_prev[i] + (dt * dt) * (c * c * d2u + f_nl) - gamma * dt * v
            u_next[i] = u_next_val

            kin_e += 0.5 * (v ** 2)
            pot_e += 0.5 * (c ** 2) * (((u_curr[i + 1] - u_curr[i]) / dx) ** 2)

        u_next[0] = 0.0
        u_next[-1] = 0.0

        total_e = (kin_e + pot_e) * dx
        energy_history.append(total_e)

        u_prev = list(u_curr)
        u_curr = list(u_next)

    return center_history, energy_history, collapse_step, spatial_snapshots

def render_failure_plate(history, energy, collapse_step, out_png):
    print(f"[FAILURE-001] Rendering diagnostic analysis plate to {out_png}...")
    width = 1280
    height = 720
    buffer = bytearray([8, 10, 15] * (width * height)) # Dark background #080a0f

    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < width and 0 <= py < height:
            idx = (py * width + px) * 3
            if alpha >= 1.0:
                buffer[idx] = r
                buffer[idx + 1] = g
                buffer[idx + 2] = b
            else:
                buffer[idx] = int(buffer[idx] * (1 - alpha) + r * alpha)
                buffer[idx + 1] = int(buffer[idx + 1] * (1 - alpha) + g * alpha)
                buffer[idx + 2] = int(buffer[idx + 2] * (1 - alpha) + b * alpha)

    def draw_line(x0, y0, x1, y1, r, g, b, alpha=1.0):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            set_pixel(x0, y0, r, g, b, alpha)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # Draw border card rectangles
    panels = [
        (40, 40, 580, 310, "WAVEFORM DIVERGENCE"),
        (660, 40, 580, 310, "PHASE SPACE COLLAPSE (u vs v)"),
        (40, 380, 580, 300, "LOGARITHMIC ENERGY BLOWUP"),
        (660, 380, 580, 300, "INSCRIPTION OF RUIN")
    ]

    for (px, py, pw, ph, title) in panels:
        # Background fill
        for y in range(py, py + ph):
            for x in range(px, px + pw):
                idx = (y * width + x) * 3
                buffer[idx] = 16
                buffer[idx + 1] = 20
                buffer[idx + 2] = 30
        # Border
        for x in range(px, px + pw):
            set_pixel(x, py, 45, 55, 75)
            set_pixel(x, py + ph - 1, 45, 55, 75)
        for y in range(py, py + ph):
            set_pixel(px, y, 45, 55, 75)
            set_pixel(px + pw - 1, y, 45, 55, 75)

    # 1. Plot Waveform
    px, py, pw, ph = panels[0][0], panels[0][1], panels[0][2], panels[0][3]
    mid_y = py + ph // 2
    for x in range(px + 10, px + pw - 10):
        set_pixel(x, mid_y, 30, 40, 55) # Zero line

    valid_pts = len(history)
    scale_x = (pw - 40) / max(1, valid_pts - 1)
    # Find max amplitude before blowout
    max_amp = max(0.001, max(abs(v) for v in history if not (math.isnan(v) or math.isinf(v))))
    max_amp = min(max_amp, 10.0) # Clamp for view

    for i in range(valid_pts - 1):
        v0 = history[i]
        v1 = history[i + 1]
        if math.isnan(v0) or math.isnan(v1) or math.isinf(v0) or math.isinf(v1):
            continue
        x0 = int(px + 20 + i * scale_x)
        y0 = int(mid_y - (v0 / max_amp) * (ph // 2 - 30))
        x1 = int(px + 20 + (i + 1) * scale_x)
        y1 = int(mid_y - (v1 / max_amp) * (ph // 2 - 30))
        # Fade from cyan to red near collapse
        t_ratio = i / max(1, valid_pts - 1)
        r = int(56 + t_ratio * 199)
        g = int(215 * (1 - t_ratio))
        b = int(210 * (1 - t_ratio))
        draw_line(x0, y0, x1, y1, r, g, b, 0.9)

    # 2. Phase Space Portrait: u vs du/dt
    px, py, pw, ph = panels[1][0], panels[1][1], panels[1][2], panels[1][3]
    cx = px + pw // 2
    cy = py + ph // 2
    for x in range(px + 10, px + pw - 10):
        set_pixel(x, cy, 30, 40, 55)
    for y in range(py + 10, py + ph - 10):
        set_pixel(cx, y, 30, 40, 55)

    velocities = []
    for i in range(len(history) - 1):
        velocities.append((history[i + 1] - history[i]))

    phase_scale = (ph // 2 - 40) / max(0.1, max_amp)
    for i in range(len(velocities) - 1):
        u0, v0 = history[i], velocities[i] * 50.0
        u1, v1 = history[i + 1], velocities[i + 1] * 50.0
        if math.isnan(u0) or math.isnan(u1) or math.isinf(u0) or math.isinf(u1):
            continue
        x0 = int(cx + u0 * phase_scale)
        y0 = int(cy - v0 * phase_scale)
        x1 = int(cx + u1 * phase_scale)
        y1 = int(cy - v1 * phase_scale)
        draw_line(x0, y0, x1, y1, 168, 85, 247, 0.7)

    # 3. Energy Log Plot
    px, py, pw, ph = panels[2][0], panels[2][1], panels[2][2], panels[2][3]
    for i in range(len(energy) - 1):
        e0 = energy[i]
        e1 = energy[i + 1]
        if e0 <= 0 or e1 <= 0 or math.isnan(e0) or math.isnan(e1) or math.isinf(e0) or math.isinf(e1):
            continue
        log_e0 = math.log10(max(1e-6, e0))
        log_e1 = math.log10(max(1e-6, e1))
        x0 = int(px + 20 + i * scale_x)
        y0 = int(py + ph - 30 - (log_e0 + 6) * 18)
        x1 = int(px + 20 + (i + 1) * scale_x)
        y1 = int(py + ph - 30 - (log_e1 + 6) * 18)
        draw_line(x0, y0, x1, y1, 212, 175, 55, 0.85)

    # Write PNG output
    write_png(out_png, width, height, buffer)

def render_failure_audio(history, out_wav):
    print(f"[FAILURE-001] Synthesizing acoustic ruin to {out_wav}...")
    sr = 48000
    duration = 4.0
    n_samples = int(duration * sr)
    
    # Sound structure:
    # 0.0 - 1.8s: Pure mineral chime (180 Hz) building harmonic overtones
    # 1.8 - 2.4s: Chaotic violent distortion, buzz, sub-octave rumble
    # 2.4 - 2.5s: 1-bit hard square-wave clip blast (+32767 / -32767)
    # 2.5 - 4.0s: Total digital silence (the NaN void)
    
    left = []
    right = []
    
    for i in range(n_samples):
        t = i / sr
        if t < 1.8:
            # Building resonance
            amp = (t / 1.8) ** 1.5 * 0.4
            f0 = 180.0
            # Higher harmonics creeping in
            sig = math.sin(2 * math.pi * f0 * t) * 0.6
            sig += math.sin(2 * math.pi * f0 * 2.76 * t) * 0.3 * (t / 1.8)
            sig += math.sin(2 * math.pi * f0 * 5.4 * t) * 0.2 * ((t / 1.8) ** 2)
            val_l = sig * amp
            val_r = sig * amp
        elif t < 2.4:
            # Chaotic instability
            dt_inst = (t - 1.8) / 0.6
            f_warped = 180.0 * (1.0 + math.sin(t * 80.0) * dt_inst * 2.0)
            sig = math.sin(2 * math.pi * f_warped * t) * (0.4 + dt_inst * 0.8)
            # Add harsh non-linear foldback
            sig = math.sin(sig * (1.0 + dt_inst * 8.0))
            val_l = max(-1.0, min(1.0, sig))
            val_r = max(-1.0, min(1.0, sig * 1.1))
        elif t < 2.48:
            # 1-bit square wave clip blast
            val_l = 1.0 if (i % 32 < 16) else -1.0
            val_r = 1.0 if (i % 30 < 15) else -1.0
        else:
            # The NaN void: pure digital zero
            val_l = 0.0
            val_r = 0.0
            
        left.append(val_l)
        right.append(val_r)
        
    write_wav(out_wav, left, right, sr)

if __name__ == "__main__":
    hist, energy, collapse, snaps = run_simulation()
    png_path = os.path.join(SCRIPT_DIR, "failure_001_numerical_explosion.png")
    wav_path = os.path.join(SCRIPT_DIR, "failure_001_acoustic_singularity.wav")
    render_failure_plate(hist, energy, collapse, png_path)
    render_failure_audio(hist, wav_path)
    print("[FAILURE-001] Simulation, visual plate, and audio ruin generated successfully.")

