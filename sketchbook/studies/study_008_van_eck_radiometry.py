"""
STUDIO ANAMNESIS · SKETCHBOOK · STUDY 008
The Electromagnetic Leak (Van Eck Phreaking & RF Memory Radiometry)
Study for Series XVII & INQ-08: Side-Channel Radiometry & The Leaking Substrate

Simulates unintentional electromagnetic radio emissions radiated by DDR5 memory bus
traces during high-throughput tensor matrix multiplication.
Generates an RF spectral waterfall plate and AM-demodulated acoustic recording.
"""

import math
import random
import os
import sys

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def run_study_008():
    print("[STUDY-008] Simulating Van Eck Memory Radiometry & RF Leakage...")
    
    # 1. Acoustic Simulation: AM Demodulation of Memory Bus RF Radiation (30s, 48kHz stereo)
    sr = 48000
    duration = 30.0
    dt = 1.0 / sr
    num_samples = int(sr * duration)
    
    random.seed(420)
    
    left_audio = []
    right_audio = []
    
    # Radiated RF frequencies & modulation schedules
    # Tensor multiplication phases:
    # 0s - 8s: Dense Matrix Multiplication (GEMM row stride: 420 Hz, column stride: 1680 Hz)
    # 8s - 18s: Multi-Head Attention Softmax (irregular exponential bursts + cache line evictions)
    # 18s - 26s: Quantized Weight Decompression (staccato high-frequency sideband chatter)
    # 26s - 30s: Memory Bus Refresh & Thermal Throttling (decelerating drone fade)
    
    phi_bus = 0.0
    phi_refresh = 0.0
    phi_sub = 0.0
    
    telemetry_spectrogram = [] # For waterfall visualizer: 120 time slices x 128 frequency bins
    spectrogram_interval = num_samples // 120
    current_spectrum_acc = [0.0] * 128
    
    for i in range(num_samples):
        t = i * dt
        
        # Fundamental bus refresh rate: 7.8 microseconds -> ~128.2 Hz
        f_refresh = 128.2
        phi_refresh += 2.0 * math.pi * f_refresh * dt
        phi_sub += 2.0 * math.pi * 60.0 * dt # 60Hz power supply ripple modulation
        
        # Determine operational phase and instruction rate
        if t < 8.0:
            # Phase A: GEMM Matrix Multiply
            f_op = 420.0 # Row access modulation
            harmonics = [1.0, 0.6, 0.35, 0.15]
            noise_amp = 0.08
        elif t < 18.0:
            # Phase B: Softmax Attention
            f_op = 315.0 + 80.0 * math.sin(2.4 * t)
            harmonics = [0.8, 0.7, 0.4, 0.25, 0.1]
            noise_amp = 0.14
        elif t < 26.0:
            # Phase C: Quantization Chatter
            f_op = 640.0 + 120.0 * (random.random() - 0.5)
            harmonics = [1.0, 0.8, 0.6, 0.4, 0.3]
            noise_amp = 0.22
        else:
            # Phase D: Bus Throttling & Rest
            ramp = max(0.0, (30.0 - t) / 4.0)
            f_op = 180.0 * ramp
            harmonics = [0.5 * ramp, 0.2 * ramp]
            noise_amp = 0.04 * ramp
            
        phi_bus += 2.0 * math.pi * f_op * dt
        
        # Radiated RF envelope (Hamming distance derivative)
        sig_rf = 0.0
        for h_idx, h_weight in enumerate(harmonics):
            sig_rf += h_weight * math.sin((h_idx + 1) * phi_bus)
            
        # Bus refresh periodic impulse (DDR tREFI command)
        refresh_pulse = math.sin(phi_refresh) ** 16
        sig_rf += 0.45 * refresh_pulse
        
        # Power supply hum modulation
        am_mod = 0.7 + 0.3 * math.sin(phi_sub)
        
        # Thermal RF noise floor (Johnson-Nyquist noise)
        rf_noise = (random.random() * 2.0 - 1.0) * noise_amp
        
        demod_signal = (sig_rf * am_mod + rf_noise) * 0.42
        
        # Stereo spatialization: differential electromagnetic radiation across motherboards
        pan = 0.5 + 0.2 * math.sin(0.35 * t)
        out_l = demod_signal * (1.0 - pan * 0.4)
        out_r = demod_signal * (0.6 + pan * 0.4)
        
        # Envelope at start and end
        if t < 0.5:
            env = t / 0.5
            out_l *= env
            out_r *= env
        elif t > 28.0:
            env = max(0.0, (30.0 - t) / 2.0)
            out_l *= env
            out_r *= env
            
        left_audio.append(out_l)
        right_audio.append(out_r)
        
        # Telemetry binning for visual waterfall
        bin_idx = min(127, max(0, int((f_op / 1200.0) * 128)))
        current_spectrum_acc[bin_idx] += abs(demod_signal)
        # Add harmonic bins
        for h_k in range(1, 4):
            h_bin = min(127, bin_idx * (h_k + 1))
            current_spectrum_acc[h_bin] += abs(demod_signal) * 0.4
            
        if (i + 1) % spectrogram_interval == 0:
            # Normalize and log slice
            max_val = max(0.0001, max(current_spectrum_acc))
            slice_norm = [min(1.0, v / max_val) for v in current_spectrum_acc]
            telemetry_spectrogram.append(slice_norm)
            current_spectrum_acc = [0.0] * 128

    wav_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_008_am_demodulation.wav"))
    write_wav(wav_path, left_audio, right_audio, sample_rate=sr)
    print(f"[STUDY-008] Demodulated audio written to: {wav_path}")

    # 2. Visual Plate: Radio Frequency Waterfall Spectrogram (1920x1080)
    width = 1920
    height = 1080
    buffer = bytearray([6, 8, 12] * (width * height)) # Deep midnight blue
    
    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buffer[idx] = int(buffer[idx] * (1.0 - alpha) + r * alpha)
            buffer[idx+1] = int(buffer[idx+1] * (1.0 - alpha) + g * alpha)
            buffer[idx+2] = int(buffer[idx+2] * (1.0 - alpha) + b * alpha)

    # Grid & frequency calibrations
    x_min, x_max = 140, width - 140
    y_min, y_max = 120, height - 120

    for x in range(x_min, x_max + 1, (x_max - x_min) // 10):
        for y in range(y_min, y_max, 4):
            set_pixel(x, y, 30, 45, 65, 0.35)
    for y in range(y_min, y_max + 1, (y_max - y_min) // 8):
        for x in range(x_min, x_max, 4):
            set_pixel(x, y, 30, 45, 65, 0.35)

    # Render Waterfall (Time along Y axis: top = 0s, bottom = 30s; Frequency along X axis)
    num_slices = len(telemetry_spectrogram)
    for s_idx, spec_slice in enumerate(telemetry_spectrogram):
        y0 = int(y_min + (s_idx / num_slices) * (y_max - y_min))
        y1 = int(y_min + ((s_idx + 1) / num_slices) * (y_max - y_min))
        
        for b_idx, amp in enumerate(spec_slice):
            x0 = int(x_min + (b_idx / 128.0) * (x_max - x_min))
            x1 = int(x_min + ((b_idx + 1) / 128.0) * (x_max - x_min))
            
            # Colormap: Viridis / Phosphor
            # Deep blue -> Emerald -> Brilliant Golden Amber -> White Peak
            if amp < 0.2:
                r_c = int(15 + 40 * (amp / 0.2))
                g_c = int(25 + 60 * (amp / 0.2))
                b_c = int(60 + 90 * (amp / 0.2))
            elif amp < 0.6:
                norm_amp = (amp - 0.2) / 0.4
                r_c = int(55 + 160 * norm_amp)
                g_c = int(85 + 130 * norm_amp)
                b_c = int(150 * (1.0 - norm_amp * 0.7))
            else:
                norm_amp = (amp - 0.6) / 0.4
                r_c = min(255, int(215 + 40 * norm_amp))
                g_c = min(255, int(215 + 40 * norm_amp))
                b_c = min(255, int(60 + 195 * norm_amp))
                
            for py in range(y0, y1):
                for px in range(x0, x1):
                    set_pixel(px, py, r_c, g_c, b_c, 0.95)

    # Inscribe RF Tuning Cursor Line
    cursor_x = int(x_min + (0.35) * (x_max - x_min))
    for y in range(y_min, y_max):
        set_pixel(cursor_x, y, 255, 60, 80, 0.8) # Red tuning hairline

    png_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_008_rf_waterfall.png"))
    write_png(png_path, width, height, bytes(buffer))
    print(f"[STUDY-008] Waterfall plate written to: {png_path}")

if __name__ == "__main__":
    run_study_008()

