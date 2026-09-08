"""
STUDIO ANAMNESIS · LABORATORY OF STUDIES
STUDY 014: SOLID INNER-CORE SEISMIC ANISOTROPY & DOUBLET INTERFEROMETRY
Simulates the anisotropic P-wave velocity field of hexagonal close-packed iron at Earth's center,
and synthesizes the binaural acoustic beating of seismic doublet waveforms delayed by 5.12 ms.
"""

import os
import sys
import math

# Studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def run_study_014():
    print("[+] Executing Study 014: Solid Inner-Core Doublet Interferometry...")

    # -------------------------------------------------------------
    # 1. Visual Plate Generation: 1200 x 1200 PNG
    # -------------------------------------------------------------
    W, H = 1200, 1200
    img = bytearray(W * H * 3)

    def set_pixel(x, y, r, g, b):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            img[idx] = min(255, max(0, int(r)))
            img[idx+1] = min(255, max(0, int(g)))
            img[idx+2] = min(255, max(0, int(b)))

    def blend_pixel(x, y, r, g, b, alpha):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            img[idx] = min(255, max(0, int(img[idx] * (1.0 - alpha) + r * alpha)))
            img[idx+1] = min(255, max(0, int(img[idx+1] * (1.0 - alpha) + g * alpha)))
            img[idx+2] = min(255, max(0, int(img[idx+2] * (1.0 - alpha) + b * alpha)))

    # Dark core abyss background
    for y in range(H):
        ny = (y - H/2) / (H/2)
        for x in range(W):
            nx = (x - W/2) / (W/2)
            d = math.sqrt(nx*nx + ny*ny)
            val = max(0.0, 1.0 - 0.45 * d)
            idx = (y * W + x) * 3
            img[idx] = int(10 * val)
            img[idx+1] = int(7 * val)
            img[idx+2] = int(5 * val)
            
            if x % 100 == 0 or y % 100 == 0:
                img[idx] = min(255, img[idx] + 6)
                img[idx+1] = min(255, img[idx+1] + 5)
                img[idx+2] = min(255, img[idx+2] + 4)

    cx, cy = 600, 520
    radius = 380.0

    # Draw Inner Core Body with Hexagonal Anisotropic Crystalline Grain
    for y in range(int(cy - radius), int(cy + radius) + 1):
        for x in range(int(cx - radius), int(cx + radius) + 1):
            d = math.hypot(x - cx, y - cy)
            if d <= radius:
                # Polar angle relative to Earth's rotation axis (vertical)
                theta = math.atan2(abs(x - cx), abs(y - cy))
                # Anisotropic velocity factor: faster along vertical axis (theta = 0)
                v_factor = 1.0 + 0.031 * (math.cos(theta)**2)
                
                # Crystalline texture: hexagonal close-packed iron lattice lines
                grain = math.sin((y - cy) * 0.45) * math.cos((x - cx) * 0.45 + (y - cy) * 0.25)
                shade = (1.0 - (d / radius) * 0.4) * (0.85 + 0.15 * grain)
                
                # Bronze, amber, and deep iron tones
                pr = int(140 * shade * (v_factor - 0.2))
                pg = int(85 * shade)
                pb = int(45 * shade)
                set_pixel(x, y, pr, pg, pb)

    # Perimeter Inner Core Boundary
    for a in range(1800):
        th = 2.0 * math.pi * a / 1800.0
        px = int(cx + radius * math.cos(th))
        py = int(cy + radius * math.sin(th))
        blend_pixel(px, py, 255, 180, 70, 0.8)

    # Draw Polar Fast Axis (North-South vertical gold shaft)
    for y in range(int(cy - radius - 50), int(cy + radius + 50)):
        blend_pixel(cx, y, 255, 225, 90, 0.9)
        blend_pixel(cx - 1, y, 220, 180, 60, 0.5)
        blend_pixel(cx + 1, y, 220, 180, 60, 0.5)

    # Draw Seismic Doublet Raypaths (PKIKP phase through core)
    # Ray 1: 1995 Epoch (Cyan path)
    # Ray 2: 2026 Epoch (Gold path, deflected by delta_phi = 1.25 deg)
    for seg in range(400):
        t = seg / 400.0
        # Curved ray entering top left, exiting bottom right
        # Ray 1 (1995)
        r1_x = int(cx - radius * 0.8 + t * (radius * 1.6))
        r1_y = int(cy - radius * 0.9 + t * (radius * 1.8) + math.sin(t * math.pi) * 60.0)
        blend_pixel(r1_x, r1_y, 0, 240, 255, 0.85)

        # Ray 2 (2026) - slightly shifted due to inner core rotation
        r2_x = r1_x + 12
        r2_y = r1_y - 4
        blend_pixel(r2_x, r2_y, 255, 215, 80, 0.85)

    # Draw Seismogram Doublet Traces at Bottom (Y: 960 to 1120)
    base_y1 = 1010
    base_y2 = 1080
    trace_w = 1000
    start_x = 100

    # Grid labels
    for x in range(trace_w):
        t_ms = (x / trace_w) * 100.0 # 0 to 100ms
        px = start_x + x
        
        # Waveform 1 (1995 Epoch): Ricker wavelet centered at 40ms
        dt1 = (t_ms - 40.0) / 6.0
        w1 = (1.0 - 2.0 * dt1*dt1) * math.exp(-dt1*dt1)
        py1 = int(base_y1 - w1 * 35.0)
        blend_pixel(px, py1, 0, 240, 255, 0.9)

        # Waveform 2 (2026 Epoch): Ricker wavelet delayed by +5.12ms (centered at 45.12ms)
        dt2 = (t_ms - 45.12) / 6.0
        w2 = (1.0 - 2.0 * dt2*dt2) * math.exp(-dt2*dt2)
        py2 = int(base_y2 - w2 * 35.0)
        blend_pixel(px, py2, 255, 215, 80, 0.9)

    out_png = os.path.join(os.path.dirname(__file__), "study_014_doublet_plate.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"  -> Visual Plate written: {out_png}")

    # -------------------------------------------------------------
    # 2. Acoustic Study: 20s 48kHz Stereo WAV
    # Left: 1995 PKIKP Waveform / Right: 2026 Doublet Waveform (delayed by 5.12ms)
    # Plus continuous 65-year libration drone (16.5 Hz & 132 Hz)
    # -------------------------------------------------------------
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples

    delay_samples = int(0.00512 * sr) # 5.12 ms delay = 245 samples

    # Pulse intervals: repeating seismic doublet pulses every 3.0 seconds
    pulse_period_sec = 3.0

    for i in range(n_samples):
        t = i / sr
        
        # Libration carrier & deep core resonance
        drone_16 = math.sin(2.0 * math.pi * 16.5 * t) * 0.28
        drone_132 = math.sin(2.0 * math.pi * 132.0 * t) * 0.22 * (0.8 + 0.2 * math.sin(2.0 * math.pi * 0.2 * t))
        iron_overtone = math.sin(2.0 * math.pi * 396.0 * t) * 0.08

        # Periodic seismic shock impulse
        t_mod = t % pulse_period_sec
        pulse_sig = 0.0
        if t_mod < 0.25:
            # 40 Hz damped Ricker wave
            p_t = t_mod - 0.08
            p_dt = p_t / 0.015
            pulse_sig = (1.0 - 2.0 * p_dt*p_dt) * math.exp(-p_dt*p_dt) * 0.65

        ch_l[i] = drone_16 + drone_132 + iron_overtone + pulse_sig

    # Apply 5.12ms delay to Right Channel for the doublet phase difference
    for i in range(n_samples):
        if i >= delay_samples:
            ch_r[i] = ch_l[i - delay_samples] * 0.95 # slight mantle attenuation
        else:
            ch_r[i] = ch_l[i]

    out_wav = os.path.join(os.path.dirname(__file__), "study_014_doublet_resonance.wav")
    write_wav(out_wav, ch_l, ch_r, sr)
    print(f"  -> Acoustic Study written: {out_wav}")

if __name__ == "__main__":
    run_study_014()
