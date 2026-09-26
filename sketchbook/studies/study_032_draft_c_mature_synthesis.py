#!/usr/bin/env python3
"""
Study 032 · Draft C: Mature Synthesis (ER = EPR Traversable Wormhole)
Studio Anamnesis · Series XXXVIII · INQ-26

Resolves the full synthesis:
1. Dual boundary CFTs with SYK Majorana boundary nodes and MERA tensor geodesics.
2. Central hyperbolic throat warped by Gao-Jafferis-Wall negative energy shockwave (Delta V < 0).
3. Traversing null information beam safely navigating between Left and Right.
4. 20-second 4-voice polyphonic SYK chaotic scrambling and teleportation audio study.
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH, HEIGHT = 1024, 1024
SAMPLE_RATE = 48000
DURATION = 20.0

def render_draft_c_plate():
    img = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH * 0.5, HEIGHT * 0.5
    
    # Negative energy shift and traversable window parameters
    delta_v = -0.18
    throat_radius = 120.0
    
    for y in range(HEIGHT):
        row_offset = y * WIDTH * 3
        y_norm = (y - cy) / (HEIGHT * 0.42)
        
        for x in range(WIDTH):
            x_norm = (x - cx) / (WIDTH * 0.42)
            
            # Distance from Left and Right centers
            d_left = math.hypot(x_norm + 1.1, y_norm)
            d_right = math.hypot(x_norm - 1.1, y_norm)
            
            # Throat necking coordinate
            z = x_norm
            w_throat = math.sqrt(0.35 + 0.5 * (z ** 2))
            r_perp = abs(y_norm)
            in_bulk_throat = (r_perp < w_throat and abs(z) < 1.3)
            
            # Kruskal coordinates
            u = (y_norm - x_norm) * 0.7071
            v = (y_norm + x_norm) * 0.7071
            if u > 0:
                v_shifted = v - delta_v
            else:
                v_shifted = v
                
            # Base cosmic void
            r, g, b = 4, 6, 12
            
            # Left CFT boundary disk
            if d_left < 0.65:
                # Hyperbolic Poincaré metric inside Left boundary
                r_disk = d_left / 0.65
                phi = math.atan2(y_norm, x_norm + 1.1)
                grid_cft = math.sin(phi * 16.0) * math.sin(10.0 / (1.001 - r_disk))
                val_l = int(30 + 50 * (1.0 - r_disk) + 20 * grid_cft)
                r, g, b = val_l // 3, val_l, int(val_l * 1.1)
                
            # Right CFT boundary disk
            if d_right < 0.65:
                r_disk = d_right / 0.65
                phi = math.atan2(y_norm, x_norm - 1.1)
                grid_cft = math.sin(phi * 16.0) * math.sin(10.0 / (1.001 - r_disk))
                val_r = int(30 + 50 * (1.0 - r_disk) + 20 * grid_cft)
                r, g, b = int(val_r * 1.1), int(val_r * 0.9), val_r // 3
                
            # Hyperbolic Bulk Einstein-Rosen Bridge
            if in_bulk_throat:
                depth = 1.0 - (r_perp / w_throat)
                # Entanglement geodesics across bridge
                geodesic = math.sin(z * 18.0 - r_perp * 14.0) * 0.5 + 0.5
                
                # Gao-Jafferis-Wall negative energy shockwave field
                shock_u = math.exp(-abs(u) * 12.0)
                
                # Traversing quantum teleportation beam along y_norm = 0
                beam = math.exp(-(y_norm ** 2) / 0.015) * (0.8 + 0.2 * math.cos(z * 30.0))
                
                t_color = (z + 1.2) / 2.4
                t_color = max(0.0, min(1.0, t_color))
                
                # Color blending
                r_bulk = int(38 * (1 - t_color) + 212 * t_color)
                g_bulk = int(185 * (1 - t_color) + 175 * t_color)
                b_bulk = int(208 * (1 - t_color) + 55 * t_color)
                
                # Combine layers
                r = int(r_bulk * depth * 0.7 + 180 * shock_u + 255 * beam)
                g = int(g_bulk * depth * 0.7 + 70 * shock_u + 240 * beam)
                b = int(b_bulk * depth * 0.7 + 255 * shock_u + 255 * beam)
                
            # Boundary rings
            if abs(d_left - 0.65) < 0.02:
                r, g, b = 56, 215, 208
            if abs(d_right - 0.65) < 0.02:
                r, g, b = 212, 175, 55
                
            pixel_idx = row_offset + x * 3
            img[pixel_idx] = max(0, min(255, r))
            img[pixel_idx + 1] = max(0, min(255, g))
            img[pixel_idx + 2] = max(0, min(255, b))
            
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_032_draft_c_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, bytes(img))
    print(f"[✓] Study 032 Draft C plate rendered: {out_path}")

def synthesize_draft_c_audio():
    num_samples = int(SAMPLE_RATE * DURATION)
    left_samples = [0.0] * num_samples
    right_samples = [0.0] * num_samples
    
    f0 = 96.42
    f_sub = f0 * 0.5
    f_transit = f0 * 8.0
    beta = 5.0265
    t_pulse = 6.0
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        fade_in = min(1.0, t / 2.0)
        fade_out = min(1.0, (DURATION - t) / 2.0)
        env = fade_in * fade_out
        
        # 1. Left CFT Carrier
        s_left_cft = math.sin(2.0 * math.pi * f0 * t) * 0.35 + math.sin(2.0 * math.pi * f0 * 2.0 * t) * 0.12
        
        # 2. Right CFT Carrier with SYK Chaotic Phase Drift
        chaos_phase = 0.9 * math.sin(t * (2.0 * math.pi / beta)) + 0.3 * math.sin(t * 1.7)
        s_right_cft = math.sin(2.0 * math.pi * f0 * t + chaos_phase) * 0.35 + math.sin(2.0 * math.pi * f0 * 2.0 * t + chaos_phase) * 0.12
        
        # 3. Gao-Jafferis-Wall Negative Energy Sub-Bass Pulse
        pulse_env = math.exp(-((t - t_pulse) ** 2) / 0.6)
        s_negative_energy = math.sin(2.0 * math.pi * f_sub * t) * pulse_env * 0.5
        
        # 4. Traversing Quantum Transit Chirp (emerging on Right boundary after pulse)
        transit_env_left = math.exp(-((t - (t_pulse - 0.4)) ** 2) / 0.3)
        transit_env_right = math.exp(-((t - (t_pulse + 0.6)) ** 2) / 0.4)
        
        f_chirp_l = f_transit * (1.0 + 0.5 * (t - (t_pulse - 0.4)))
        f_chirp_r = f_transit * (1.0 - 0.3 * (t - (t_pulse + 0.6)))
        
        s_chirp_l = math.sin(2.0 * math.pi * f_chirp_l * t) * transit_env_left * 0.3
        s_chirp_r = math.sin(2.0 * math.pi * f_chirp_r * t) * transit_env_right * 0.35
        
        # Cross-coupling lock after pulse: entanglement teleports information into unison
        if t > t_pulse:
            lock = min(1.0, (t - t_pulse) / 3.0)
            s_right_cft = s_right_cft * (1.0 - 0.6 * lock) + s_left_cft * (0.6 * lock)
            
        l_out = (s_left_cft + s_negative_energy + s_chirp_l) * env * 0.8
        r_out = (s_right_cft + s_negative_energy + s_chirp_r) * env * 0.8
        
        left_samples[i] = l_out
        right_samples[i] = r_out
        
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_032_draft_c_audio.wav"))
    write_wav(out_path, left_samples, right_samples, SAMPLE_RATE)
    print(f"[✓] Study 032 Draft C audio synthesized: {out_path}")

if __name__ == "__main__":
    render_draft_c_plate()
    synthesize_draft_c_audio()

