#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 024: THE WHEELER PINCH-OFF CATASTROPHE & TOPOLOGICAL RUPTURE
Studio Anamnesis · Series XXXVII (Topological Geometrodynamics)
Anti-One-Shot Discipline: Boundary Overdrive & Singular Metric Collapse

Physics of Failure:
When trapped electric flux exceeds critical threshold (Phi_E >> Phi_crit),
the self-gravitation of the electromagnetic field energy (u_EM ~ Phi_E^2 / r^4)
crushes the Morris-Thorne-Wheeler throat flaring condition.
The throat radius collapses toward zero (b_0 -> 0), triggering:
1. Kretschmann invariant divergence: K = R^abcd R_abcd -> infinity
2. Manifold topological rupture (disconnection of upper and lower spatial sheets)
3. Naked singularity blowout: chaotic metric shear spikes, jagged visual fissures
4. Acoustic shockwave blowout: severe non-linear clipping and sub-harmonic shrieking
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 800
HEIGHT = 450

def render_failure_024():
    buf = bytearray(WIDTH * HEIGHT * 3)
    
    # 1. Background: Blood-amber and void fracture
    for y in range(HEIGHT):
        ny = (y - HEIGHT / 2.0) / (HEIGHT / 2.0)
        grad = abs(ny)
        r_bg = int(22 + 45 * grad)
        g_bg = int(8 + 12 * grad)
        b_bg = int(12 + 10 * grad)
        for x in range(WIDTH):
            idx = (y * WIDTH + x) * 3
            buf[idx] = r_bg
            buf[idx+1] = g_bg
            buf[idx+2] = b_bg

    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # 2. Render Pinched-Off Ruptured Throat (b_0 -> 0)
    # The throat has necked down to a zero-dimensional singularity
    # Producing jagged radial metric tearing rays
    num_tear_rays = 120
    for ray in range(num_tear_rays):
        angle = 2.0 * math.pi * ray / num_tear_rays
        # Overdriven chaotic length due to Kretschmann divergence
        max_dist = 60.0 + 260.0 * abs(math.sin(angle * 7.5 + math.cos(angle * 13.0)))
        
        step_len = 2.0
        cur_dist = 2.0
        while cur_dist < max_dist:
            # Metric shear deflection
            shear = math.sin(cur_dist * 0.15) * 14.0
            px = int(cx + cur_dist * math.cos(angle) + shear * math.sin(angle))
            py = int(cy + (cur_dist * math.sin(angle) - shear * math.cos(angle)) * 0.48)
            
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                idx = (py * WIDTH + px) * 3
                # Searing white and crimson singularity blowout
                intensity = max(0.0, 1.0 - (cur_dist / max_dist))
                buf[idx] = min(255, buf[idx] + int(255 * intensity))
                buf[idx+1] = min(255, buf[idx+1] + int(110 * intensity))
                buf[idx+2] = min(255, buf[idx+2] + int(60 * intensity))
                
            cur_dist += step_len

    # 3. Disconnected Severed Hyperboloid Sheets (Upper & Lower drifting apart)
    for sheet_sign in (+1, -1):
        # The sheets have ruptured vertically apart by 70 pixels
        sheet_offset_y = sheet_sign * 65.0
        num_rings = 35
        for r_step in range(num_rings):
            # Broken jagged radius
            r = 15.0 + (r_step ** 1.4) * 5.0
            if r > 340.0:
                continue
                
            num_pts = 300
            for p in range(num_pts):
                phi = 2.0 * math.pi * p / num_pts
                
                # Topological fracture perturbation
                fracture = math.sin(phi * 11.0 + r_step * 0.8) * 8.0
                proj_x = cx + (r + fracture) * math.cos(phi)
                proj_y = cy + sheet_offset_y + ((r + fracture) * math.sin(phi)) * 0.42
                
                px, py = int(proj_x), int(proj_y)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    idx = (py * WIDTH + px) * 3
                    # Rupture edge glows in volatile electric amber
                    buf[idx] = min(255, buf[idx] + 200)
                    buf[idx+1] = min(255, buf[idx+1] + 60)
                    buf[idx+2] = min(255, buf[idx+2] + 40)

    # 4. Central Naked Singularity Void Spark (Pinch-off point)
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            d = math.sqrt(dx*dx + dy*dy)
            if d <= 8.0:
                px = int(cx + dx)
                py = int(cy + dy)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    idx = (py * WIDTH + px) * 3
                    buf[idx] = 255
                    buf[idx+1] = 255
                    buf[idx+2] = 255

    output_png = os.path.join(os.path.dirname(__file__), "failure_024_plate.png")
    write_png(output_png, WIDTH, HEIGHT, buf, has_alpha=False)
    print(f"[+] Failure 024 Plate written to: {output_png}")

def synthesize_failure_024_audio():
    sr = 48000
    duration_s = 15.0
    n_samples = int(sr * duration_s)
    
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples
    
    # Overdriven frequency soaring from 77.92 Hz up into screaming singularity whistle (1400 Hz)
    for i in range(n_samples):
        t = i / float(sr)
        progress = t / duration_s
        
        # Accelerating exponential frequency rise (gravitational collapse)
        inst_f = 77.92 * math.exp(progress * 2.8) # 77 Hz -> 1280 Hz
        
        # Hard clipping non-linear saturation
        raw_osc = math.sin(2.0 * math.pi * inst_f * t) * (1.0 + progress * 3.5)
        # Squeeze through tanh distortion
        distorted = math.tanh(raw_osc * 3.0)
        
        # Singular rupture pops
        pop = 0.0
        if math.sin(t * 88.0) > 0.98:
            pop = (math.sin(t * 4500.0) * math.exp(-(t % 0.05) * 80.0)) * 0.7
            
        sig = distorted * 0.65 + pop * 0.35
        # Controlled brickwall limiter
        sig_clamped = max(-0.95, min(0.95, sig))
        
        ch_l[i] = sig_clamped
        ch_r[i] = sig_clamped * (0.8 + 0.2 * math.cos(2.0 * math.pi * 3.0 * t))
        
    output_wav = os.path.join(os.path.dirname(__file__), "failure_024_audio.wav")
    write_wav(output_wav, ch_l, ch_r, sr)
    print(f"[+] Failure 024 Audio written to: {output_wav}")

if __name__ == "__main__":
    render_failure_024()
    synthesize_failure_024_audio()
