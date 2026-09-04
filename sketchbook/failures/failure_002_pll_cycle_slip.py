#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
Experiment 002: Phase-Locked Loop (PLL) Cycle Slip Catastrophe

Premise:
A Phase-Locked Loop (PLL) attempts to synchronize a local voltage-controlled oscillator (VCO)
to an external reference frequency. 
When thermal drift or sudden phase shock exceeds the pull-in range, the phase detector
exceeds +/- pi, triggering a violent "cycle slip."

The Failure:
An instantaneous phase discontinuity causes instantaneous frequency (d_theta/dt)
to spike toward infinity, generating a harsh transient click and chaotic frequency hunting
before re-acquisition.

Visualizes the phase error trajectory and synthesizes the acoustic rupture.
"""

import math
import os
import random
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from png_writer import write_png
from audio_writer import write_wav

def simulate_pll_cycle_slip():
    print("[FAILURE-002] Simulating Phase-Locked Loop cycle slip...")
    sr = 48000
    duration = 5.0 # 5-second acoustic experiment
    n_samples = int(duration * sr)

    f_ref = 320.0 # Reference frequency (Hz)
    w_ref = 2 * math.pi * f_ref

    # Second-order PLL parameters
    zeta = 0.5 # Damping ratio (under-damped to reveal oscillation)
    wn = 2 * math.pi * 45.0 # Natural loop bandwidth (45 Hz)
    kp = 2 * zeta * wn
    ki = wn * wn

    theta_ref = 0.0
    theta_vco = 0.0
    vco_freq = f_ref # Initial VCO frequency
    integrator = 0.0

    audio = [0.0] * n_samples
    phase_errors = []
    vco_frequencies = []
    slip_events = []

    dt = 1.0 / sr

    for i in range(n_samples):
        t = i / sr

        # Reference phase advance
        # Inject massive phase disturbance at t = 1.5s and t = 3.2s
        if 1.5 <= t < 1.502:
            theta_ref += 0.15 # Massive sudden step shock
        elif 3.2 <= t < 3.204:
            theta_ref -= 0.18 # Shock in opposite direction

        theta_ref += w_ref * dt

        # VCO phase advance
        theta_vco += 2 * math.pi * vco_freq * dt

        # Phase error wrapped to [-pi, pi]
        raw_error = (theta_ref - theta_vco)
        wrapped_error = math.atan2(math.sin(raw_error), math.cos(raw_error))

        # Detect cycle slip (when unwrapped error jumps across 2*pi boundary)
        if abs(raw_error) > math.pi:
            if not slip_events or (i - slip_events[-1]) > 500:
                slip_events.append(i)
                print(f"[FAILURE-002] CYCLE SLIP detected at t={t:.4f}s! Phase error: {raw_error:.2f} rad")
            # Force phase wrap
            theta_vco = theta_ref - wrapped_error

        # Loop filter (PI controller)
        integrator += ki * wrapped_error * dt
        control_voltage = kp * wrapped_error + integrator

        # VCO frequency modulation
        vco_freq = f_ref + control_voltage / (2 * math.pi)

        # Output audio: raw VCO sinusoid
        # When slip occurs, the phase jump creates an acoustic pop
        sig = math.sin(theta_vco)
        audio[i] = sig

        if i % 16 == 0:
            phase_errors.append(wrapped_error)
            vco_frequencies.append(vco_freq)

    # Master audio
    out_wav = os.path.join(SCRIPT_DIR, "failure_002_cycle_slip.wav")
    write_wav(out_wav, audio, audio, sr)
    print(f"[FAILURE-002] Saved acoustic rupture: {out_wav}")

    return phase_errors, vco_frequencies, slip_events

def render_slip_plate(phase_errors, vco_freqs, slip_events, out_png):
    print(f"[FAILURE-002] Rendering phase error and frequency hunting plate to {out_png}...")
    width = 1280
    height = 720
    buf = bytearray([8, 10, 15] * (width * height))

    def set_pixel(x, y, r, g, b):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b

    def draw_line(x0, y0, x1, y1, r, g, b):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            set_pixel(x0, y0, r, g, b)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    # Top panel: Phase Error Trajectory [-pi, pi]
    # Bottom panel: VCO Frequency Hunting (Hz)
    panel_h = 280
    margin_l = 80
    margin_r = 40
    plot_w = width - margin_l - margin_r

    # Background cards
    for y in range(40, 40 + panel_h):
        for x in range(margin_l, margin_l + plot_w):
            idx = (y * width + x) * 3
            buf[idx] = 14; buf[idx+1] = 18; buf[idx+2] = 27

    for y in range(380, 380 + panel_h):
        for x in range(margin_l, margin_l + plot_w):
            idx = (y * width + x) * 3
            buf[idx] = 14; buf[idx+1] = 18; buf[idx+2] = 27

    # Center reference lines
    mid1 = 40 + panel_h // 2
    mid2 = 380 + panel_h // 2
    for x in range(margin_l, margin_l + plot_w):
        set_pixel(x, mid1, 35, 45, 60)
        set_pixel(x, mid2, 35, 45, 60)

    # Plot Phase Error
    n_pts = len(phase_errors)
    step_x = plot_w / max(1, n_pts - 1)
    for i in range(n_pts - 1):
        e0 = phase_errors[i] / math.pi # [-1, 1]
        e1 = phase_errors[i + 1] / math.pi
        x0 = int(margin_l + i * step_x)
        y0 = int(mid1 - e0 * (panel_h // 2 - 20))
        x1 = int(margin_l + (i + 1) * step_x)
        y1 = int(mid1 - e1 * (panel_h // 2 - 20))
        # Draw green/cyan line, red if slip discontinuity
        if abs(e1 - e0) > 0.8:
            draw_line(x0, y0, x1, y1, 255, 60, 60) # Vertical slip tear
        else:
            draw_line(x0, y0, x1, y1, 56, 215, 210)

    # Plot VCO Frequency Hunting
    f_ref = 320.0
    f_range = 140.0
    for i in range(n_pts - 1):
        df0 = (vco_freqs[i] - f_ref) / f_range
        df1 = (vco_freqs[i + 1] - f_ref) / f_range
        x0 = int(margin_l + i * step_x)
        y0 = int(mid2 - df0 * (panel_h // 2 - 20))
        x1 = int(margin_l + (i + 1) * step_x)
        y1 = int(mid2 - df1 * (panel_h // 2 - 20))
        draw_line(x0, y0, x1, y1, 212, 175, 55)

    write_png(out_png, width, height, buf)
    print(f"[FAILURE-002] Saved diagnostic plate to {out_png}")

if __name__ == "__main__":
    pe, vf, slips = simulate_pll_cycle_slip()
    png_path = os.path.join(SCRIPT_DIR, "failure_002_cycle_slip.png")
    render_slip_plate(pe, vf, slips, png_path)
    print("[FAILURE-002] Complete.")

