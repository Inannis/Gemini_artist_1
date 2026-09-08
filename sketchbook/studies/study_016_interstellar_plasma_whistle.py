"""
STUDIO ANAMNESIS · EXPLORATORY STUDY 016
Study: The Interstellar Plasma Whistle (Langmuir Wave Excitation at the Heliopause)
Series XXIII: The Heliopause & Interstellar Radio Quietude

Models the shock-excited Langmuir electron plasma oscillations in the Very Local Interstellar Medium (VLISM):
- Plasma density n_e ~ 0.085 -> 0.11 cm^-3
- Langmuir resonance frequency drifting upward: f_p(t) = 2600 + 520 * (1 - exp(-t / 6.0)) Hz
- Suprathermal electron bump-on-tail instability and non-linear wave packet modulation
- Voyager Plasma Wave Science (PWS) 10-meter dipole antenna reception

Outputs:
1. study_016_plasma_whistle_plate.png (1200 x 1200 spectrogram and phase-space plate)
2. study_016_interstellar_whistle.wav (20.0s 48kHz stereo acoustic study)
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
    print("[+] Executing Study 016: Interstellar Plasma Whistle Synthesis...")
    random.seed(20120825) # Voyager 1 heliopause crossing seed
    
    sr = 48000
    duration = 20.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # State for plasma oscillator
    phase_plasma_l = 0.0
    phase_plasma_r = 0.0
    phase_rumble = 0.0
    
    # For spectrogram visualization: 1000 time steps x 500 frequency bins
    spec_w, spec_h = 1000, 500
    spec_grid = [[0.0] * spec_h for _ in range(spec_w)]
    
    # Waveform trace for lower panel
    trace_samples = []
    
    # Telemetry carrier parameters
    telemetry_freq = 110.0 # 10 Hz telemetry modulation on low-frequency subcarrier
    
    for i in range(num_samples):
        t = i / sr
        
        # 1. Shock arrival and plasma frequency drift
        # CME shock arrives around t = 4.0s
        shock_env = 0.0
        if t >= 3.5:
            shock_env = 1.0 - math.exp(-(t - 3.5) / 4.0)
            
        # Frequency rises from 2580 Hz to 3120 Hz
        fp = 2580.0 + 540.0 * shock_env
        
        # Micro-turbulence frequency jitter (interstellar density fluctuations delta_n / n ~ 0.02)
        turb = math.sin(2.0 * math.pi * 3.7 * t) * 12.0 + math.sin(2.0 * math.pi * 14.3 * t) * 6.0
        inst_fp = fp + turb * shock_env
        
        # Phase advancement
        d_phase = 2.0 * math.pi * inst_fp / sr
        phase_plasma_l += d_phase
        # 10-meter dipole stereo phase separation (interstellar wave propagation vector theta ~ 45 deg)
        phase_plasma_r += d_phase + 0.18 * math.sin(2.0 * math.pi * 0.5 * t)
        
        # Langmuir wave envelope: wave packets from bump-on-tail non-linear saturation
        packet_env = (math.sin(2.0 * math.pi * 2.1 * t) ** 2) * (math.sin(2.0 * math.pi * 0.4 * t) ** 2)
        plasma_amp = shock_env * (0.35 + 0.25 * packet_env)
        
        plasma_sig_l = math.sin(phase_plasma_l) * plasma_amp
        plasma_sig_r = math.sin(phase_plasma_r) * plasma_amp
        
        # 2. Deep heliosheath turbulent magnetic rumble (32 Hz + harmonics)
        phase_rumble += 2.0 * math.pi * (32.0 + 4.0 * math.sin(2.0 * math.pi * 0.2 * t)) / sr
        rumble = (math.sin(phase_rumble) * 0.25 + math.sin(phase_rumble * 1.5) * 0.12) * (1.0 - 0.5 * shock_env)
        
        # 3. Attowatt telemetry carrier ticks (10 Hz BPSK clock)
        bit_clock = 1.0 if (int(t * 10.0) % 2 == 0) else -1.0
        carrier_tick = math.sin(2.0 * math.pi * telemetry_freq * t) * bit_clock * 0.035
        
        # 4. Interstellar cosmic microwave background hiss (filtered white noise)
        noise_l = (random.random() - 0.5) * 0.08
        noise_r = (random.random() - 0.5) * 0.08
        
        # Combine into audio
        val_l = plasma_sig_l + rumble + carrier_tick + noise_l
        val_r = plasma_sig_r + rumble + carrier_tick + noise_r
        
        audio_l[i] = val_l
        audio_r[i] = val_r
        
        # Accumulate spectrogram intensity
        step_idx = int((t / duration) * spec_w)
        if 0 <= step_idx < spec_w:
            # Map frequency inst_fp [2000 Hz, 3500 Hz] into spec_h [0, 500]
            if shock_env > 0.01:
                f_bin = int(((inst_fp - 2000.0) / 1500.0) * spec_h)
                if 0 <= f_bin < spec_h:
                    spec_grid[step_idx][f_bin] += plasma_amp * 0.08
                    # Add bandwidth spread
                    if f_bin > 0: spec_grid[step_idx][f_bin-1] += plasma_amp * 0.04
                    if f_bin < spec_h - 1: spec_grid[step_idx][f_bin+1] += plasma_amp * 0.04
                    
        # Trace for lower panel (sample around shock arrival t in [7.0, 7.05])
        if 7.0 <= t < 7.05 and (i % 2 == 0):
            trace_samples.append((t - 7.0, val_l))

    # Normalize audio
    max_amp = max(max(abs(x) for x in audio_l), max(abs(x) for x in audio_r))
    if max_amp > 0:
        audio_l = [x / max_amp * 0.85 for x in audio_l]
        audio_r = [x / max_amp * 0.85 for x in audio_r]
        
    wav_path = os.path.join(os.path.dirname(__file__), "study_016_interstellar_whistle.wav")
    write_wav(wav_path, audio_l, audio_r, sr)
    print(f"  -> Generated Acoustic Study: {wav_path}")

    # Render Visual Plate (1200 x 1200 PNG)
    w, h = 1200, 1200
    pixels = bytearray([8, 12, 18] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    # Grid background
    for x in range(0, w, 80):
        for y in range(h):
            if y % 4 == 0: set_pixel(x, y, 30, 45, 65, 0.3)
    for y in range(0, h, 80):
        for x in range(w):
            if x % 4 == 0: set_pixel(x, y, 30, 45, 65, 0.3)

    # Upper Panel: Spectrogram (x: 100 to 1100, y: 100 to 600)
    spec_x1, spec_x2 = 100, 1100
    spec_y1, spec_y2 = 100, 600
    
    # Draw frame
    for x in range(spec_x1, spec_x2 + 1):
        set_pixel(x, spec_y1, 80, 110, 150, 0.8)
        set_pixel(x, spec_y2, 80, 110, 150, 0.8)
    for y in range(spec_y1, spec_y2 + 1):
        set_pixel(spec_x1, y, 80, 110, 150, 0.8)
        set_pixel(spec_x2, y, 80, 110, 150, 0.8)

    # Plot spectrogram
    for sx in range(min(spec_w, spec_x2 - spec_x1)):
        px = spec_x1 + sx
        for sy in range(min(spec_h, spec_y2 - spec_y1)):
            py = spec_y2 - sy # invert frequency axis
            intensity = min(1.0, spec_grid[sx][sy])
            if intensity > 0.01:
                # Color map: deep blue -> cyan -> electric gold -> white
                cr = int(30 + 225 * (intensity ** 1.5))
                cg = int(100 + 155 * intensity)
                cb = int(240 * (1.0 - intensity * 0.3))
                set_pixel(px, py, cr, cg, cb, min(1.0, intensity * 2.0))

    # Lower Panel Left: Dipole Antenna Waveform V_PWS(t) (x: 100 to 600, y: 700 to 1100)
    wav_x1, wav_x2 = 100, 600
    wav_y1, wav_y2 = 700, 1100
    wav_cy = (wav_y1 + wav_y2) // 2

    for x in range(wav_x1, wav_x2 + 1):
        set_pixel(x, wav_y1, 80, 110, 150, 0.8)
        set_pixel(x, wav_y2, 80, 110, 150, 0.8)
        set_pixel(x, wav_cy, 60, 80, 110, 0.4)
    for y in range(wav_y1, wav_y2 + 1):
        set_pixel(wav_x1, y, 80, 110, 150, 0.8)
        set_pixel(wav_x2, y, 80, 110, 150, 0.8)

    if trace_samples:
        t_max = trace_samples[-1][0]
        prev_pt = None
        for dt_val, val in trace_samples:
            px = int(wav_x1 + (dt_val / max(0.001, t_max)) * (wav_x2 - wav_x1))
            py = int(wav_cy - val * 160.0)
            if prev_pt is not None:
                x0, y0 = prev_pt
                steps = max(abs(px - x0), abs(py - y0), 1)
                for s in range(steps + 1):
                    lx = int(x0 + (px - x0) * (s / steps))
                    ly = int(y0 + (py - y0) * (s / steps))
                    set_pixel(lx, ly, 80, 230, 255, 0.8)
            prev_pt = (px, py)

    # Lower Panel Right: Electron Beam Phase Space Vortex (x, vx) (x: 650 to 1100, y: 700 to 1100)
    vortex_cx = (650 + 1100) // 2
    vortex_cy = (700 + 1100) // 2
    for rad in [50, 100, 150, 180]:
        for a_deg in range(0, 360, 3):
            rad_ang = math.radians(a_deg)
            gx = int(vortex_cx + rad * math.cos(rad_ang))
            gy = int(vortex_cy + rad * math.sin(rad_ang))
            set_pixel(gx, gy, 45, 65, 90, 0.4)
    for dx in range(-200, 201):
        set_pixel(vortex_cx + dx, vortex_cy, 60, 85, 115, 0.5)
    for dy in range(-200, 201):
        set_pixel(vortex_cx, vortex_cy + dy, 60, 85, 115, 0.5)

    # Draw phase space spiral / vortex
    for theta_step in range(1200):
        theta = theta_step * 0.05
        r_spiral = 15.0 + 0.14 * theta_step
        # Add non-linear vortex deformation
        deform = math.sin(3.0 * theta) * 18.0
        vx = int(vortex_cx + (r_spiral + deform) * math.cos(theta))
        vy = int(vortex_cy + (r_spiral + deform) * math.sin(theta))
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                set_pixel(vx + ox, vy + oy, 255, 190, 60, 0.75)

    png_path = os.path.join(os.path.dirname(__file__), "study_016_plasma_whistle_plate.png")
    write_png(png_path, w, h, pixels, has_alpha=False)
    print(f"  -> Generated Visual Plate: {png_path}")

if __name__ == "__main__":
    run_study()
