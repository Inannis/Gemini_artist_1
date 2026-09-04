"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
Experiment 003: The Adler Injection Locking Catastrophe
Acoustic and Visual Study of Coupling Entrainment and Phase Collapse

When two nearby quartz oscillators or high-frequency clock distribution trees
experience parasitic ground-plane coupling or cross-talk (Adler injection locking),
the independent microtonal beating suddenly snaps into rigid synchrony (K > Kc).
The spatial stereo field collapses into monaural stasis, and non-linear delayed
feedback leads to chaotic phase chatter (metastability collapse).
"""

import math
import sys
import os

# Add practice tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def run_experiment():
    print("[EXPERIMENT-003] Simulating Adler Injection Locking Catastrophe...")
    
    sr = 48000
    duration = 15.0 # 15 seconds
    num_samples = int(sr * duration)
    dt = 1.0 / sr
    
    # Oscillator parameters
    f1_base = 256.0 # Hz (C4)
    f2_base = 254.4 # Hz (detuning of 1.6 Hz)
    w1_base = 2.0 * math.pi * f1_base
    w2_base = 2.0 * math.pi * f2_base
    delta_w = w1_base - w2_base # ~ 10.05 rad/s
    Kc = delta_w / 2.0 # Critical Adler coupling threshold (~ 5.026)
    
    theta1 = 0.0
    theta2 = 0.0
    
    left_samples = []
    right_samples = []
    
    # History buffer for delay in chaotic phase (Phase 3)
    delay_samples = int(sr * 0.008) # 8ms delay
    phase_diff_history = [0.0] * (delay_samples + 1)
    
    # Telemetry logging for visual plate
    telemetry_time = []
    telemetry_phi = []
    telemetry_k = []
    telemetry_beat = []
    
    downsample_factor = 48 # log at 1000 Hz
    
    for i in range(num_samples):
        t = i * dt
        
        # Coupling schedule
        if t < 5.0:
            # Phase 1: Sub-critical weak coupling (Asynchronous drift & rich beating)
            K = 0.8
        elif t < 10.0:
            # Phase 2: Super-critical coupling (Injection lock collapse)
            ramp = min(1.0, (t - 5.0) / 0.5)
            K = 0.8 + ramp * (8.5 - 0.8) # K = 8.5 > Kc
        else:
            # Phase 3: Chaotic non-linear delay feedback
            K = 12.0
            
        phi = theta1 - theta2
        
        # Calculate instantaneous derivatives
        if t < 10.0:
            dtheta1 = w1_base - K * math.sin(phi)
            dtheta2 = w2_base + K * math.sin(phi)
        else:
            # Non-linear delayed coupling with cubic distortion
            delayed_phi = phase_diff_history[-delay_samples]
            coupling_term = K * (math.sin(phi) + 0.8 * math.sin(delayed_phi) + 0.3 * (math.sin(phi)**3))
            dtheta1 = w1_base - coupling_term
            dtheta2 = w2_base + coupling_term
            
        theta1 += dtheta1 * dt
        theta2 += dtheta2 * dt
        
        phase_diff_history.append(theta1 - theta2)
        if len(phase_diff_history) > delay_samples + 10:
            phase_diff_history.pop(0)
            
        # Audio sample generation: stereo binaural channels
        s1 = math.sin(theta1)
        s2 = math.sin(theta2)
        
        # Add subtle 2nd harmonic
        s1 += 0.15 * math.sin(2.0 * theta1)
        s2 += 0.15 * math.sin(2.0 * theta2)
        
        # Subtle sub-bass 48Hz transformer presence
        hum = 0.08 * math.sin(2.0 * math.pi * 48.0 * t)
        
        # Soft envelope at start and finish
        env = 1.0
        if t < 0.1:
            env = t / 0.1
        elif t > duration - 0.2:
            env = max(0.0, (duration - t) / 0.2)
            
        left_samples.append((s1 + hum) * 0.7 * env)
        right_samples.append((s2 + hum) * 0.7 * env)
        
        if i % downsample_factor == 0:
            telemetry_time.append(t)
            telemetry_phi.append((phi + math.pi) % (2.0 * math.pi) - math.pi)
            telemetry_k.append(K)
            instantaneous_beat = abs(dtheta1 - dtheta2) / (2.0 * math.pi)
            telemetry_beat.append(instantaneous_beat)
            
    # Write Audio Artifact
    wav_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_003_injection_locking.wav"))
    write_wav(wav_path, left_samples, right_samples, sample_rate=sr)
    
    # Render Visual Analysis Plate (1920x1080)
    width = 1920
    height = 1080
    buffer = bytearray([12, 14, 18] * (width * height)) # Deep slate background
    
    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buffer[idx] = int(buffer[idx] * (1.0 - alpha) + r * alpha)
            buffer[idx+1] = int(buffer[idx+1] * (1.0 - alpha) + g * alpha)
            buffer[idx+2] = int(buffer[idx+2] * (1.0 - alpha) + b * alpha)
            
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

    # Draw grid
    for gx in range(120, width - 120, 160):
        for y in range(120, height - 120, 4):
            set_pixel(gx, y, 35, 42, 52, 0.4)
    for gy in range(160, height - 120, 120):
        for x in range(120, width - 120, 4):
            set_pixel(x, gy, 35, 42, 52, 0.4)

    # Plot 1: Phase Difference phi(t) across time (Top half)
    t_min, t_max = 0.0, 15.0
    x_start = 140
    x_end = width - 140
    
    y_center_phi = 340
    phi_scale = 120.0 / math.pi
    
    # Draw Phase Boundary (+/- pi)
    for x in range(x_start, x_end):
        set_pixel(x, int(y_center_phi - 120), 70, 80, 95, 0.5)
        set_pixel(x, int(y_center_phi + 120), 70, 80, 95, 0.5)
        set_pixel(x, y_center_phi, 45, 55, 68, 0.8)

    # Plot Phase trajectory
    prev_px = None
    prev_py = None
    for t_val, phi_val in zip(telemetry_time, telemetry_phi):
        px = int(x_start + (t_val / t_max) * (x_end - x_start))
        py = int(y_center_phi - phi_val * phi_scale)
        if prev_px is not None and abs(py - prev_py) < 100:
            draw_line(prev_px, prev_py, px, py, 240, 190, 80, 0.85) # Gold trajectory
        prev_px = px
        prev_py = py

    # Plot 2: Instantaneous Beating Frequency (Bottom half)
    y_base_beat = 880
    beat_scale = 35.0 # pixels per Hz
    
    prev_bx = None
    prev_by = None
    for t_val, beat_val in zip(telemetry_time, telemetry_beat):
        bx = int(x_start + (t_val / t_max) * (x_end - x_start))
        by = int(y_base_beat - min(8.0, beat_val) * beat_scale)
        if prev_bx is not None:
            if t_val < 5.0:
                draw_line(prev_bx, prev_by, bx, by, 70, 200, 240, 0.9)
            elif t_val < 10.0:
                draw_line(prev_bx, prev_by, bx, by, 255, 60, 80, 0.95)
            else:
                draw_line(prev_bx, prev_by, bx, by, 210, 110, 255, 0.9)
        prev_bx = bx
        prev_by = by

    # Draw vertical phase boundary demarcation lines
    x_phase2 = int(x_start + (5.0 / t_max) * (x_end - x_start))
    x_phase3 = int(x_start + (10.0 / t_max) * (x_end - x_start))
    for y in range(120, height - 120):
        set_pixel(x_phase2, y, 220, 80, 90, 0.6)
        set_pixel(x_phase3, y, 180, 120, 240, 0.6)

    # Write Image Artifact
    png_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_003_injection_locking.png"))
    write_png(png_path, width, height, bytes(buffer))
    print(f"[EXPERIMENT-003] Generated: {wav_path} and {png_path}")

if __name__ == "__main__":
    run_experiment()

