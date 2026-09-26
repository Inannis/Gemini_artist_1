#!/usr/bin/env python3
"""
STUDY 031 · DRAFT B: MORRIS-THORNE-WHEELER WORMHOLE THROAT & FLUX TRAPPING
Studio Anamnesis · Series XXXVII (Topological Geometrodynamics)
Anti-One-Shot Discipline: Introducing Physical Friction & Metric Embedding

Features:
- Morris-Thorne-Wheeler hyperboloid embedding: z(r) = +/- 2 * sqrt(b_0 * (r - b_0))
- Two distinct spatial sheets (Upper sheet z > 0: Mouth B / Apparent +Q; Lower sheet z < 0: Mouth A / Apparent -Q)
- Trapped source-free electric flux streamlines (Charge Without Charge: closed lines entering mouth A, threading throat, exiting mouth B)
- Curvature shading via Einstein tensor component G_tt(r)
- 15-second 48kHz stereo audio synthesis: Throat cavity standing wave (77.92 Hz) + Doppler redshift beating
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

def render_draft_b():
    buf = bytearray(WIDTH * HEIGHT * 3)
    
    # 1. Background: Deep interstellar-lithic void with subtle vertical curvature gradient
    for y in range(HEIGHT):
        ny = (y - HEIGHT / 2.0) / (HEIGHT / 2.0)
        grad = max(0.0, 1.0 - abs(ny))
        r_val = int(8 + 12 * grad)
        g_val = int(10 + 15 * grad)
        b_val = int(18 + 25 * grad)
        for x in range(WIDTH):
            idx = (y * WIDTH + x) * 3
            buf[idx] = r_val
            buf[idx+1] = g_val
            buf[idx+2] = b_val

    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    b_0 = 42.0 # Throat minimum neck radius in pixels
    
    # 2. Render the Throat Embedding Hyperboloid (Isometric Wireframe & Shaded Rings)
    # Upper sheet (z > 0) and Lower sheet (z < 0)
    for sheet_sign in (+1, -1):
        num_radial_rings = 45
        for r_step in range(num_radial_rings):
            r = b_0 + (r_step ** 1.35) * 4.2
            if r > 320.0:
                continue
                
            # Embedding height z(r) = +/- 2 * sqrt(b_0 * (r - b_0))
            z = sheet_sign * 2.2 * math.sqrt(b_0 * max(0.0, r - b_0))
            
            # Gravitational redshift factor: alpha = sqrt(1 - b_0 / r)
            redshift = math.sqrt(max(0.05, 1.0 - (b_0 / r)))
            
            # Color: Upper sheet glows in celestial cyan/gold; Lower sheet glows in deep amethyst/amber
            if sheet_sign > 0:
                # Mouth B (Apparent +Q)
                cr = int(35 + 180 * (1.0 - redshift))
                cg = int(160 * redshift + 75 * (1.0 - redshift))
                cb = int(220 * redshift + 45 * (1.0 - redshift))
            else:
                # Mouth A (Apparent -Q)
                cr = int(180 * (1.0 - redshift) + 60 * redshift)
                cg = int(60 * (1.0 - redshift) + 30 * redshift)
                cb = int(200 * (1.0 - redshift) + 120 * redshift)

            # Draw radial ring with 3D projection
            num_pts = 360
            for p in range(num_pts):
                phi = 2.0 * math.pi * p / num_pts
                
                # Isometric 3D projection
                # 3D: X = r*cos(phi), Y = r*sin(phi), Z = z
                # Camera tilt: elevation 28 deg
                cos_elev = math.cos(math.radians(28))
                sin_elev = math.sin(math.radians(28))
                
                proj_x = cx + r * math.cos(phi)
                proj_y = cy - z * cos_elev + (r * math.sin(phi)) * sin_elev
                
                px = int(proj_x)
                py = int(proj_y)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    idx = (py * WIDTH + px) * 3
                    buf[idx] = min(255, buf[idx] + cr // 3)
                    buf[idx+1] = min(255, buf[idx+1] + cg // 3)
                    buf[idx+2] = min(255, buf[idx+2] + cb // 3)

    # 3. Render Trapped Source-Free Electric Flux Streamlines
    # Lines enter from lower sheet (Mouth A), pass through throat neck, emerge out of upper sheet (Mouth B)
    num_flux_lines = 48
    for line_idx in range(num_flux_lines):
        base_phi = 2.0 * math.pi * line_idx / num_flux_lines
        # Step through proper radial distance from lower sheet (z < 0) to upper sheet (z > 0)
        num_steps = 140
        for s in range(num_steps):
            t_param = (s - num_steps / 2.0) / (num_steps / 2.0) # -1.0 to +1.0
            sheet_s = +1 if t_param >= 0 else -1
            
            # Distance from throat: r(t) = b_0 + |t|^1.8 * 240
            r_cur = b_0 + (abs(t_param) ** 1.8) * 240.0
            z_cur = sheet_s * 2.2 * math.sqrt(b_0 * max(0.0, r_cur - b_0))
            
            # Frame-dragging swirl around z-axis: phi(t) = base_phi + 3.0 / sqrt(r_cur / b_0)
            phi_cur = base_phi + (2.5 / math.sqrt(r_cur / b_0)) * (1.0 if sheet_s > 0 else -1.0)
            
            # Projection
            proj_x = cx + r_cur * math.cos(phi_cur)
            proj_y = cy - z_cur * math.cos(math.radians(28)) + (r_cur * math.sin(phi_cur)) * math.sin(math.radians(28))
            
            px, py = int(proj_x), int(proj_y)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                idx = (py * WIDTH + px) * 3
                # Streamline flux intensity peaks at throat neck
                throat_proximity = 1.0 / (1.0 + (abs(t_param) * 3.5))
                buf[idx] = min(255, buf[idx] + int(240 * throat_proximity))
                buf[idx+1] = min(255, buf[idx+1] + int(210 * throat_proximity))
                buf[idx+2] = min(255, buf[idx+2] + int(120 * throat_proximity))

    # 4. Highlight the Throat Neck (Non-Contractible 2-Cycle b_0)
    for p in range(720):
        phi = 2.0 * math.pi * p / 720
        proj_x = cx + b_0 * math.cos(phi)
        proj_y = cy + (b_0 * math.sin(phi)) * math.sin(math.radians(28))
        px, py = int(proj_x), int(proj_y)
        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
            idx = (py * WIDTH + px) * 3
            buf[idx] = 255
            buf[idx+1] = 235
            buf[idx+2] = 160

    output_png = os.path.join(os.path.dirname(__file__), "study_031_draft_b_plate.png")
    write_png(output_png, WIDTH, HEIGHT, buf, has_alpha=False)
    print(f"[+] Draft B Plate written to: {output_png}")

def synthesize_draft_b_audio():
    sr = 48000
    duration_s = 15.0
    n_samples = int(sr * duration_s)
    
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples
    
    # Fundamental throat resonance f_0 = 77.92 Hz (Wheeler standing wave)
    f0 = 77.92
    f_kerr = 14.2  # Frame-dragging beat
    
    for i in range(n_samples):
        t = i / float(sr)
        
        # Envelope: gradual fade in and out
        env = math.sin(math.pi * t / duration_s)
        
        # Carrier 1: Fundamental throat cavity mode with subtle Doppler frequency modulation
        fm_mod = math.sin(2.0 * math.pi * 0.25 * t) * 2.8
        carrier1_l = math.sin(2.0 * math.pi * (f0 + fm_mod) * t)
        carrier1_r = math.cos(2.0 * math.pi * (f0 - fm_mod) * t)
        
        # Carrier 2: 2nd harmonic (155.84 Hz) modulated by Kerr frame-dragging beat
        beat = 0.5 * (1.0 + math.cos(2.0 * math.pi * f_kerr * t))
        carrier2 = math.sin(2.0 * math.pi * (f0 * 2.0) * t) * beat
        
        # Sub-bass: Planck foam rumble (38.96 Hz)
        sub = math.sin(2.0 * math.pi * (f0 * 0.5) * t) * 0.4
        
        # Trapped flux hiss (source-free Maxwell Poynting circulation)
        # Simple pseudo-random fluctuation
        noise = (math.sin(t * 12345.67) * math.cos(t * 7654.32)) * 0.08
        
        sig_l = (carrier1_l * 0.45 + carrier2 * 0.25 + sub * 0.25 + noise) * env
        sig_r = (carrier1_r * 0.45 + carrier2 * 0.25 + sub * 0.25 + noise) * env
        
        ch_l[i] = max(-0.95, min(0.95, sig_l))
        ch_r[i] = max(-0.95, min(0.95, sig_r))
        
    output_wav = os.path.join(os.path.dirname(__file__), "study_031_draft_b_audio.wav")
    write_wav(output_wav, ch_l, ch_r, sr)
    print(f"[+] Draft B Audio written to: {output_wav}")

if __name__ == "__main__":
    render_draft_b()
    synthesize_draft_b_audio()
