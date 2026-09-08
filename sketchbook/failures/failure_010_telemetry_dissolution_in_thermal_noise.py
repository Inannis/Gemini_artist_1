"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 010
Experiment: Telemetry Dissolution in Cosmic Thermal Noise & PLL Cycle-Slipping Collapse
Series XXIII: The Heliopause & Interstellar Radio Quietude

Simulates a coherent Costas Loop phase-locked receiver demodulating an 8.42 GHz carrier
attenuated across 250 AU into the interstellar thermal noise floor (-10.5 dB SNR).
Demonstrates catastrophic phase slip, constellation dispersion, and Bit Error Rate (BER) -> 0.50.

Zero external dependencies: uses pure Python standard library (math, struct, zlib, random).
Generates:
1. failure_010_pll_collapse.png (1200 x 1200 diagnostic visual plate)
2. failure_010_carrier_dissolution.wav (20.0s 48kHz stereo acoustic ruin)
"""

import os
import sys
import math
import random
import struct
import zlib

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png
from audio_writer import write_wav

def run_experiment():
    print("[+] Executing Productive Failure 010: Interstellar Telemetry Dissolution...")
    random.seed(19770820) # Voyager 2 launch date seed
    
    # 1. Physics & Simulation Parameters
    sample_rate = 48000
    duration = 20.0
    num_samples = int(sample_rate * duration)
    
    # Carrier and modulation
    carrier_freq = 880.0     # Baseband audio representation of carrier
    bit_rate = 10.0          # 10 bits per second deep space telemetry
    samples_per_bit = int(sample_rate / bit_rate)
    num_bits = int(num_samples / samples_per_bit) + 1
    
    # Generate true bitstream
    bits = [1 if random.random() > 0.5 else -1 for _ in range(num_bits)]
    
    # Loop filter parameters (2nd-order Costas Loop)
    loop_bw = 15.0 # Hz
    damping = 0.707
    wn = 2.0 * math.pi * loop_bw
    kp = 2.0 * damping * wn / sample_rate
    ki = (wn ** 2) / (sample_rate ** 2)
    
    # Simulation state
    nco_phase = 0.0
    loop_integ = 0.0
    true_phase = 0.25 # slight initial offset
    
    # Records for plotting plate
    # We will sample 2000 constellation points across time
    constellation_clean = []   # t in [0, 4] s (SNR = +20 dB)
    constellation_critical = []# t in [8, 12] s (SNR = +3 dB)
    constellation_collapsed = []# t in [15, 20] s (SNR = -10 dB)
    
    phase_error_history = []
    
    # Audio buffers
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # Progressively degrade SNR across 20 seconds (simulating traversal 100 AU -> 280 AU)
    for i in range(num_samples):
        t = i / sample_rate
        bit_idx = int(t * bit_rate)
        cur_bit = bits[bit_idx] if bit_idx < len(bits) else 1
        
        # Traversal from 100 AU (t=0) to 280 AU (t=20)
        # SNR decreases from +20 dB to -12 dB
        snr_db = 20.0 - 32.0 * (t / duration)
        linear_snr = 10.0 ** (snr_db / 10.0)
        sig_amp = math.sqrt(linear_snr)
        noise_amp = 1.0
        
        # Transmitted BPSK signal
        carrier_theta = 2.0 * math.pi * carrier_freq * t + true_phase
        tx_sig = sig_amp * cur_bit * math.sin(carrier_theta)
        
        # Additive White Gaussian Noise (Box-Muller)
        u1 = max(1e-12, random.random())
        u2 = random.random()
        noise = noise_amp * math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        rx_sig = tx_sig + noise
        
        # Costas Loop Demodulation
        # In-phase (I) and Quadrature (Q) mixing with local NCO
        mix_i = rx_sig * 2.0 * math.sin(nco_phase)
        mix_q = rx_sig * 2.0 * math.cos(nco_phase)
        
        # Phase detector error: e = I * Q
        phase_err = mix_i * mix_q
        # Limit error for numerical stability
        phase_err = max(-5.0, min(5.0, phase_err))
        
        # Update Loop filter
        loop_integ += ki * phase_err
        freq_offset = kp * phase_err + loop_integ
        nco_phase += 2.0 * math.pi * carrier_freq / sample_rate + freq_offset
        
        # Wrap phase
        if nco_phase > math.pi:
            nco_phase -= 2.0 * math.pi
        elif nco_phase < -math.pi:
            nco_phase += 2.0 * math.pi
            
        # Record phase tracking error
        instant_err = carrier_theta - nco_phase
        # Normalize to [-pi, pi]
        norm_err = (instant_err + math.pi) % (2.0 * math.pi) - math.pi
        if i % 240 == 0:
            phase_error_history.append((t, norm_err))
            
        # Sample constellation at bit center
        if (i % samples_per_bit) == (samples_per_bit // 2):
            point = (mix_i / (sig_amp + 0.1), mix_q / (sig_amp + 0.1))
            if t < 5.0:
                constellation_clean.append(point)
            elif 8.0 <= t < 13.0:
                constellation_critical.append(point)
            elif t >= 15.0:
                constellation_collapsed.append(point)
                
        # Audio generation:
        # Left channel: Raw received RF baseband (Carrier + Noise)
        # Right channel: Demodulated In-Phase bitstream + PLL cycle-slip clicks
        slip_click = 0.0
        if abs(freq_offset * sample_rate) > 200.0: # cycle slip transient
            slip_click = (random.random() - 0.5) * 0.8
            
        audio_l[i] = max(-1.0, min(1.0, (rx_sig / (sig_amp + 1.0)) * 0.4))
        audio_r[i] = max(-1.0, min(1.0, (mix_i / (sig_amp + 1.0)) * 0.35 + slip_click))

    # Normalize audio
    max_amp = max(max(abs(x) for x in audio_l), max(abs(x) for x in audio_r))
    if max_amp > 0:
        audio_l = [x / max_amp * 0.85 for x in audio_l]
        audio_r = [x / max_amp * 0.85 for x in audio_r]
        
    wav_path = os.path.join(os.path.dirname(__file__), "failure_010_carrier_dissolution.wav")
    write_wav(wav_path, audio_l, audio_r, sample_rate)
    print(f"  -> Generated Acoustic Ruin: {wav_path}")

    # 2. Render Diagnostic Plate (1200 x 1200 PNG)
    w, h = 1200, 1200
    pixels = bytearray([8, 10, 16] * (w * h)) # deep void background
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    def draw_grid():
        for x in range(0, w, 100):
            for y in range(h):
                if y % 4 == 0:
                    set_pixel(x, y, 25, 35, 50, 0.4)
        for y in range(0, h, 100):
            for x in range(w):
                if x % 4 == 0:
                    set_pixel(x, y, 25, 35, 50, 0.4)

    draw_grid()

    # Draw 3 Constellation Panes:
    # Pane 1: Clean (t < 5s, 100 AU) - Centered at (250, 400)
    # Pane 2: Critical (8s <= t < 13s, 180 AU) - Centered at (600, 400)
    # Pane 3: Collapsed (t >= 15s, 260 AU) - Centered at (950, 400)
    panes = [
        ("CLEAN LOCK (100 AU / +20 dB SNR)", 250, 400, constellation_clean, (60, 220, 160)),
        ("CYCLE SLIPPING (180 AU / +3 dB SNR)", 600, 400, constellation_critical, (240, 180, 50)),
        ("GAUSSIAN RUIN (260 AU / -10 dB SNR)", 950, 400, constellation_collapsed, (240, 70, 70))
    ]

    for title, cx, cy, pts, col in panes:
        # Draw circle target
        for rad in [40, 80, 120]:
            for a_deg in range(0, 360, 4):
                rad_ang = math.radians(a_deg)
                gx = int(cx + rad * math.cos(rad_ang))
                gy = int(cy + rad * math.sin(rad_ang))
                set_pixel(gx, gy, 40, 55, 75, 0.5)
        # Axis lines
        for dx in range(-140, 141):
            set_pixel(cx + dx, cy, 50, 70, 95, 0.6)
        for dy in range(-140, 141):
            set_pixel(cx, cy + dy, 50, 70, 95, 0.6)
            
        # Plot points
        for px, py in pts:
            sx = int(cx + px * 45.0)
            sy = int(cy - py * 45.0)
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    set_pixel(sx + ox, sy + oy, col[0], col[1], col[2], 0.7)

    # Lower Panel: Phase Error & Cycle Slip Trajectory (t vs phase error)
    # Box from x=100 to 1100, y=700 to 1100 (cy = 900)
    box_x1, box_x2 = 100, 1100
    box_y1, box_y2 = 700, 1100
    box_cy = (box_y1 + box_y2) // 2

    for x in range(box_x1, box_x2 + 1):
        set_pixel(x, box_y1, 70, 90, 120, 0.8)
        set_pixel(x, box_y2, 70, 90, 120, 0.8)
        set_pixel(x, box_cy, 60, 80, 110, 0.4) # 0-phase line
        # +/- pi lines
        set_pixel(x, box_cy - 150, 120, 60, 60, 0.3)
        set_pixel(x, box_cy + 150, 120, 60, 60, 0.3)
    for y in range(box_y1, box_y2 + 1):
        set_pixel(box_x1, y, 70, 90, 120, 0.8)
        set_pixel(box_x2, y, 70, 90, 120, 0.8)

    # Plot phase error history
    prev_pt = None
    for t_val, err in phase_error_history:
        px = int(box_x1 + (t_val / duration) * (box_x2 - box_x1))
        py = int(box_cy - (err / math.pi) * 150)
        if prev_pt is not None:
            # Draw connecting line segment
            x0, y0 = prev_pt
            steps = max(abs(px - x0), abs(py - y0), 1)
            for s in range(steps + 1):
                lx = int(x0 + (px - x0) * (s / steps))
                ly = int(y0 + (py - y0) * (s / steps))
                # Color shifts from cyan (stable) to orange (slip) to crimson (chaotic)
                progress = t_val / duration
                cr = int(50 + 200 * progress)
                cg = int(220 * (1.0 - progress * 0.7))
                cb = int(240 * (1.0 - progress))
                set_pixel(lx, ly, cr, cg, cb, 0.85)
        prev_pt = (px, py)

    png_path = os.path.join(os.path.dirname(__file__), "failure_010_pll_collapse.png")
    write_png(png_path, w, h, pixels, has_alpha=False)
    print(f"  -> Generated Visual Diagnostic Plate: {png_path}")

if __name__ == "__main__":
    run_experiment()
