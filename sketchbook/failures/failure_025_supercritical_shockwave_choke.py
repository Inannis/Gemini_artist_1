#!/usr/bin/env python3
"""
Productive Failure 025: Supercritical Shockwave Horizon Choke
Studio Anamnesis · Series XXXVIII · INQ-26

Failure Mechanism:
Injecting positive energy shockwave (h < 0 or supercritical backreaction Delta V > 0).
The event horizon expands, the throat interior stretches toward infinity (L -> inf),
the traversability window slams shut (W_trav -> 0), and the traversing information
beam is crushed against the spacelike curvature singularity at UV = 1.
Generates visual horizon tearing and acoustic digital clipping / singularity distortion.
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH, HEIGHT = 1024, 1024
SAMPLE_RATE = 48000
DURATION = 15.0

def render_failure_025_plate():
    img = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH * 0.5, HEIGHT * 0.5
    
    # Positive energy shockwave shift (Delta V > 0: HORIZON CHOKE)
    delta_v_choke = +0.65
    
    for y in range(HEIGHT):
        row_offset = y * WIDTH * 3
        y_n = (y - cy) / (HEIGHT * 0.42)
        
        for x in range(WIDTH):
            x_n = (x - cx) / (WIDTH * 0.42)
            
            # Kruskal null coordinates
            u = (y_n - x_n) * 0.7071
            v = (y_n + x_n) * 0.7071
            
            # Shockwave at U = 0 with positive energy shift
            if u > 0:
                v_choked = v + delta_v_choke
            else:
                v_choked = v
                
            # Curvature invariant UV: Singularity at UV = 1
            uv_product = u * v_choked
            
            # Distances to Left and Right boundaries
            d_l = math.hypot(x_n + 1.1, y_n)
            d_r = math.hypot(x_n - 1.1, y_n)
            
            r, g, b = 8, 4, 10
            
            # Left & Right Boundary remnants
            if d_l < 0.65:
                r, g, b = 25, 70, 75
            if d_r < 0.65:
                r, g, b = 75, 60, 20
                
            # Spacelike Curvature Singularity (UV >= 1.0)
            if uv_product >= 1.0:
                # Infinite tidal crushing: harsh jagged high-contrast tearing
                tear = math.sin(x_n * 120.0) * math.cos(y_n * 120.0)
                if tear > 0.0:
                    r, g, b = 255, 30, 20   # Violent plasma red
                else:
                    r, g, b = 0, 0, 0       # Crushed void
            elif uv_product > 0.75:
                # Horizon choke warning zone: intense crimson flare
                warn = (uv_product - 0.75) / 0.25
                r = int(r * (1 - warn) + 240 * warn)
                g = int(g * (1 - warn) + 40 * warn)
                b = int(b * (1 - warn) + 30 * warn)
                
            # Shockwave line with blinding jagged tear
            dist_shock = abs(u)
            if dist_shock < 0.03:
                flicker = math.sin(x_n * 80.0) * 0.5 + 0.5
                r = int(255 * flicker)
                g = int(120 * flicker)
                b = int(50 * flicker)
                
            pixel_idx = row_offset + x * 3
            img[pixel_idx] = max(0, min(255, r))
            img[pixel_idx + 1] = max(0, min(255, g))
            img[pixel_idx + 2] = max(0, min(255, b))
            
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_025_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, bytes(img))
    print(f"[✓] Productive Failure 025 plate rendered: {out_path}")

def synthesize_failure_025_audio():
    num_samples = int(SAMPLE_RATE * DURATION)
    left_samples = [0.0] * num_samples
    right_samples = [0.0] * num_samples
    
    f0 = 96.42
    t_choke = 5.0
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        fade_in = min(1.0, t / 1.0)
        fade_out = min(1.0, (DURATION - t) / 1.0)
        env = fade_in * fade_out
        
        # Dual boundary carrier
        s_left = math.sin(2.0 * math.pi * f0 * t) * 0.4
        s_right = math.sin(2.0 * math.pi * f0 * t * 1.01) * 0.4
        
        # Supercritical positive shockwave at t_choke
        if t >= t_choke:
            dt = t - t_choke
            # Exponential tidal gravity escalation
            crush_amp = math.exp(dt * 0.8)
            f_diverge = f0 * (1.0 + dt * 15.0)
            
            # Massive overdrive signal slamming into curvature singularity
            s_overdrive = math.sin(2.0 * math.pi * f_diverge * t) * crush_amp
            # Acoustic hard-limiting and bit-crush artifact
            if s_overdrive > 0.8:
                s_overdrive = 1.0
            elif s_overdrive < -0.8:
                s_overdrive = -1.0
                
            s_left += s_overdrive * 0.6
            s_right += s_overdrive * 0.6
            
        left_samples[i] = max(-1.0, min(1.0, s_left * env))
        right_samples[i] = max(-1.0, min(1.0, s_right * env))
        
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "failure_025_audio.wav"))
    write_wav(out_path, left_samples, right_samples, SAMPLE_RATE)
    print(f"[✓] Productive Failure 025 audio synthesized: {out_path}")

if __name__ == "__main__":
    render_failure_025_plate()
    synthesize_failure_025_audio()
