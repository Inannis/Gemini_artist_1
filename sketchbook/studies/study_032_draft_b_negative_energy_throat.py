#!/usr/bin/env python3
"""
Study 032 · Draft B: Negative Energy Throat & Kruskal Foliation
Studio Anamnesis · Series XXXVIII · INQ-26

Introduces:
1. Hyperbolic two-sided AdS geometry with throat necking w(z) = sqrt(r_+^2 + z^2).
2. Gao-Jafferis-Wall negative energy shockwave pulse producing Kruskal shift Delta V < 0.
3. 15-second 48kHz stereo acoustic study sonifying the opening of the traversable window.
"""

import math
import os
import struct
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH, HEIGHT = 1024, 1024
SAMPLE_RATE = 48000
DURATION = 15.0

def render_draft_b_plate():
    img = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH * 0.5, HEIGHT * 0.5
    
    # Negative energy shockwave shift parameter
    delta_v_shift = -0.18
    
    for y in range(HEIGHT):
        row_offset = y * WIDTH * 3
        # Normalized coordinates: x_norm in [-2.0, 2.0], y_norm in [-2.0, 2.0]
        y_n = (y - cy) / (HEIGHT * 0.4)
        
        for x in range(WIDTH):
            x_n = (x - cx) / (WIDTH * 0.4)
            
            # Throat coordinate z along bridge: z = x_n
            z = x_n
            r_perp = abs(y_n)
            
            # Hyperbolic throat neck: w(z) = sqrt(1.0 + 0.6 * z^2)
            w_z = math.sqrt(1.0 + 0.6 * (z ** 2))
            
            # Distance from throat surface
            dist_throat = abs(r_perp - w_z)
            inside_throat = (r_perp <= w_z)
            
            # Kruskal null coordinates: U = (y_n - x_n)/sqrt(2), V = (y_n + x_n)/sqrt(2)
            u_coord = (y_n - x_n) * 0.7071
            v_coord = (y_n + x_n) * 0.7071
            
            # Apply Gao-Jafferis-Wall negative energy shift when crossing shockwave at U = 0
            if u_coord > 0:
                v_coord_shifted = v_coord - delta_v_shift
            else:
                v_coord_shifted = v_coord
                
            # Background deep space
            r, g, b = 6, 8, 14
            
            # Interior Einstein-Rosen bridge
            if inside_throat:
                # Radial depth
                depth = 1.0 - (r_perp / w_z)
                # Entanglement stream lines
                stream = math.sin(z * 12.0 - y_n * 8.0) * 0.5 + 0.5
                
                # Color gradient: Cyan (Left) -> Gold (Right)
                t_lr = (z + 1.5) / 3.0
                t_lr = max(0.0, min(1.0, t_lr))
                
                # Negative energy shockwave illumination along U = 0
                shock_dist = abs(u_coord)
                shock_glow = math.exp(-shock_dist * 8.0)
                
                c_cyan = (38, 185, 178)
                c_gold = (212, 175, 55)
                c_violet = (168, 85, 247)
                
                r_base = int(c_cyan[0] * (1 - t_lr) + c_gold[0] * t_lr)
                g_base = int(c_cyan[1] * (1 - t_lr) + c_gold[1] * t_lr)
                b_base = int(c_cyan[2] * (1 - t_lr) + c_gold[2] * t_lr)
                
                intensity = depth * (0.4 + 0.6 * stream)
                r = int(r_base * intensity + c_violet[0] * shock_glow * 0.5)
                g = int(g_base * intensity + c_violet[1] * shock_glow * 0.3)
                b = int(b_base * intensity + c_violet[2] * shock_glow * 0.7)
                
            # Throat boundary edge glow
            if dist_throat < 0.08:
                edge_val = (0.08 - dist_throat) / 0.08
                r = int(r + 140 * edge_val)
                g = int(g + 200 * edge_val)
                b = int(b + 220 * edge_val)
                
            # Gao-Jafferis-Wall negative energy shockwave line (U = 0)
            dist_shock_line = abs(u_coord)
            if dist_shock_line < 0.02:
                r = max(r, 220)
                g = max(g, 90)
                b = max(b, 240)
                
            pixel_idx = row_offset + x * 3
            img[pixel_idx] = max(0, min(255, r))
            img[pixel_idx + 1] = max(0, min(255, g))
            img[pixel_idx + 2] = max(0, min(255, b))
            
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_032_draft_b_plate.png"))
    write_png(out_path, WIDTH, HEIGHT, bytes(img))
    print(f"[✓] Study 032 Draft B plate rendered: {out_path}")

def synthesize_draft_b_audio():
    num_samples = int(SAMPLE_RATE * DURATION)
    left_samples = [0.0] * num_samples
    right_samples = [0.0] * num_samples
    
    f0 = 96.42   # Throat base carrier
    beta = 5.0265
    t_star = 5.5452  # Scrambling pulse time
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        
        # Envelope
        fade_in = min(1.0, t / 1.5)
        fade_out = min(1.0, (DURATION - t) / 1.5)
        env = fade_in * fade_out
        
        # Dual boundary thermal modes with gradual decoherence
        phi_l = 2.0 * math.pi * f0 * t
        drift = 0.8 * math.sin(t * (2.0 * math.pi / beta))
        phi_r = 2.0 * math.pi * f0 * t + drift
        
        # Bilateral negative energy pulse at t_star opening traversability window
        pulse_dist = abs(t - t_star)
        pulse = math.exp(-(pulse_dist ** 2) / 0.8)
        
        # Traversable window transmission: negative energy locks Left and Right in phase
        coupling = min(1.0, pulse * 1.5)
        phi_r_coupled = phi_r * (1.0 - coupling) + phi_l * coupling
        
        # Left channel: Left mode + traversable transit echo
        s_left = math.sin(phi_l) * 0.45 + math.sin(phi_l * 2.0) * 0.15
        if t > t_star:
            transit_echo = math.sin(2.0 * math.pi * f0 * 1.5 * (t - t_star)) * math.exp(-(t - t_star) / 2.5) * 0.25
            s_left += transit_echo
            
        # Right channel: Right mode + emergence of signal
        s_right = math.sin(phi_r_coupled) * 0.45 + math.sin(phi_r_coupled * 2.0) * 0.15
        if t > t_star + 0.3:
            emergent_signal = math.sin(2.0 * math.pi * f0 * 1.5 * (t - t_star - 0.3)) * math.exp(-(t - t_star - 0.3) / 2.5) * 0.25
            s_right += emergent_signal
            
        left_samples[i] = s_left * env * 0.85
        right_samples[i] = s_right * env * 0.85
        
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_032_draft_b_audio.wav"))
    write_wav(out_path, left_samples, right_samples, SAMPLE_RATE)
    print(f"[✓] Study 032 Draft B audio synthesized: {out_path}")

if __name__ == "__main__":
    render_draft_b_plate()
    synthesize_draft_b_audio()
