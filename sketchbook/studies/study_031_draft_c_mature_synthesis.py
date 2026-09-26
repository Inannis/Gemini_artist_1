#!/usr/bin/env python3
"""
STUDY 031 · DRAFT C: MATURE SYNTHESIS — THE WHEELER GEON & MULTI-THROAT SPACETIME FOAM
Studio Anamnesis · Series XXXVII (Topological Geometrodynamics)
Anti-One-Shot Discipline: Full Topological Multi-Throat Synthesis

Features:
- Primary MTW wormhole throat + constellation of microscopic secondary topological handles
- Kerr-Wheeler rotational frame-dragging swirl: Omega_FD(r) ~ J / r^3
- Dual-sheet flux trapping (Mouth A converging, Mouth B diverging, Charge Without Charge)
- Planck-scale metric fluctuation noise field (Delta g ~ ell_P / L)
- 15-second 48kHz stereo polyphonic throat acoustics: 4-voice resonant geon chord
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

def render_draft_c():
    buf = bytearray(WIDTH * HEIGHT * 3)
    
    # 1. Base Quantum Foam Substrate: Planckian Metric Fluctuations
    # Delta g ~ ell_P / L creates a textured, granular vacuum field
    for y in range(HEIGHT):
        ny = (y - HEIGHT / 2.0) / (HEIGHT / 2.0)
        dist_sq = ny * ny
        for x in range(WIDTH):
            nx = (x - WIDTH / 2.0) / (WIDTH / 2.0)
            r_norm = math.sqrt(nx * nx + dist_sq)
            
            # Stochastic high-frequency foam noise
            n1 = math.sin(x * 0.15 + math.cos(y * 0.22)) * math.cos(y * 0.18)
            n2 = math.sin(x * 0.42 - y * 0.35) * math.sin(x * 0.08 + y * 0.12)
            foam = 0.5 * (n1 + n2)
            
            # Ambient void tint: deep Prussian blue / obsidian with foam luminescence
            base_lum = max(0.0, 1.0 - r_norm * 0.7)
            r_val = int(5 + 14 * base_lum + 8 * foam)
            g_val = int(7 + 20 * base_lum + 12 * foam)
            b_val = int(14 + 32 * base_lum + 20 * foam)
            
            idx = (y * WIDTH + x) * 3
            buf[idx] = max(0, min(255, r_val))
            buf[idx+1] = max(0, min(255, g_val))
            buf[idx+2] = max(0, min(255, b_val))

    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Define Throats: 1 Primary Central Geon Throat + 6 Secondary Micro-Wormhole Handles
    throats = [
        {"cx": cx, "cy": cy, "b_0": 48.0, "spin": 1.0, "scale": 1.0, "weight": 1.0},
        {"cx": cx - 180.0, "cy": cy - 45.0, "b_0": 18.0, "spin": -0.8, "scale": 0.55, "weight": 0.5},
        {"cx": cx + 195.0, "cy": cy + 40.0, "b_0": 20.0, "spin": 0.9, "scale": 0.60, "weight": 0.55},
        {"cx": cx - 85.0, "cy": cy + 95.0, "b_0": 14.0, "spin": 0.6, "scale": 0.45, "weight": 0.4},
        {"cx": cx + 110.0, "cy": cy - 85.0, "b_0": 16.0, "spin": -0.7, "scale": 0.50, "weight": 0.45},
        {"cx": cx - 260.0, "cy": cy + 60.0, "b_0": 11.0, "spin": 0.5, "scale": 0.35, "weight": 0.3},
        {"cx": cx + 270.0, "cy": cy - 70.0, "b_0": 12.0, "spin": -0.5, "scale": 0.38, "weight": 0.32},
    ]

    # 2. Render Each Throat with MTW Metric Embedding & Frame-Dragging Swirl
    for t_data in throats:
        tcx, tcy = t_data["cx"], t_data["cy"]
        b0 = t_data["b_0"]
        spin = t_data["spin"]
        weight = t_data["weight"]
        
        # Dual-Sheet Hyperboloid Ribs
        for sheet_sign in (+1, -1):
            num_radial_rings = int(32 * t_data["scale"])
            for r_step in range(num_radial_rings):
                r = b0 + (r_step ** 1.32) * 3.6
                z = sheet_sign * 2.0 * math.sqrt(b0 * max(0.0, r - b0))
                redshift = math.sqrt(max(0.08, 1.0 - (b0 / r)))
                
                # Sheet colors
                if sheet_sign > 0:
                    cr = int((40 + 190 * (1.0 - redshift)) * weight)
                    cg = int((180 * redshift + 80 * (1.0 - redshift)) * weight)
                    cb = int((230 * redshift + 50 * (1.0 - redshift)) * weight)
                else:
                    cr = int((200 * (1.0 - redshift) + 70 * redshift) * weight)
                    cg = int((70 * (1.0 - redshift) + 40 * redshift) * weight)
                    cb = int((220 * (1.0 - redshift) + 130 * redshift) * weight)
                    
                num_pts = int(240 * t_data["scale"])
                for p in range(num_pts):
                    phi = 2.0 * math.pi * p / num_pts
                    
                    # Kerr-Wheeler frame dragging rotation
                    phi_drag = phi + (spin * 1.8 / math.sqrt(max(1.0, r / b0)))
                    
                    proj_x = tcx + r * math.cos(phi_drag)
                    proj_y = tcy - z * math.cos(math.radians(26)) + (r * math.sin(phi_drag)) * math.sin(math.radians(26))
                    
                    px, py = int(proj_x), int(proj_y)
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        idx = (py * WIDTH + px) * 3
                        buf[idx] = min(255, buf[idx] + cr // 3)
                        buf[idx+1] = min(255, buf[idx+1] + cg // 3)
                        buf[idx+2] = min(255, buf[idx+2] + cb // 3)

        # 3. Source-Free Trapped Electric Flux Lines for this Throat
        num_flux_lines = int(36 * t_data["scale"])
        for l_idx in range(num_flux_lines):
            base_phi = 2.0 * math.pi * l_idx / num_flux_lines
            num_steps = 100
            for s in range(num_steps):
                param = (s - num_steps / 2.0) / (num_steps / 2.0)
                sh_sign = +1 if param >= 0 else -1
                
                r_cur = b0 + (abs(param) ** 1.7) * (180.0 * t_data["scale"])
                z_cur = sh_sign * 2.0 * math.sqrt(b0 * max(0.0, r_cur - b0))
                
                # Non-linear helical twist through throat neck
                phi_cur = base_phi + spin * (2.8 / math.sqrt(max(1.0, r_cur / b0))) * (1.0 if sh_sign > 0 else -1.0)
                
                proj_x = tcx + r_cur * math.cos(phi_cur)
                proj_y = tcy - z_cur * math.cos(math.radians(26)) + (r_cur * math.sin(phi_cur)) * math.sin(math.radians(26))
                
                px, py = int(proj_x), int(proj_y)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    idx = (py * WIDTH + px) * 3
                    proximity = 1.0 / (1.0 + abs(param) * 3.2)
                    buf[idx] = min(255, buf[idx] + int(245 * proximity * weight))
                    buf[idx+1] = min(255, buf[idx+1] + int(215 * proximity * weight))
                    buf[idx+2] = min(255, buf[idx+2] + int(140 * proximity * weight))

        # Highlight Throat Neck (r = b_0)
        for p in range(360):
            phi = 2.0 * math.pi * p / 360
            proj_x = tcx + b0 * math.cos(phi)
            proj_y = tcy + (b0 * math.sin(phi)) * math.sin(math.radians(26))
            px, py = int(proj_x), int(proj_y)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                idx = (py * WIDTH + px) * 3
                buf[idx] = min(255, buf[idx] + int(240 * weight))
                buf[idx+1] = min(255, buf[idx+1] + int(230 * weight))
                buf[idx+2] = min(255, buf[idx+2] + int(180 * weight))

    output_png = os.path.join(os.path.dirname(__file__), "study_031_draft_c_plate.png")
    write_png(output_png, WIDTH, HEIGHT, buf, has_alpha=False)
    print(f"[+] Draft C Plate written to: {output_png}")

def synthesize_draft_c_audio():
    sr = 48000
    duration_s = 15.0
    n_samples = int(sr * duration_s)
    
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples
    
    # 4-Voice Geon Modal Harmonic Chord
    # Fundamental: f0 = 77.92 Hz
    # Fifth: 116.88 Hz (3/2)
    # Octave: 155.84 Hz (2/1)
    # Octave Fifth: 233.76 Hz (3/1)
    f0 = 77.92
    f_modes = [f0, f0 * 1.5, f0 * 2.0, f0 * 3.0]
    weights = [0.40, 0.25, 0.20, 0.12]
    
    for i in range(n_samples):
        t = i / float(sr)
        env = math.sin(math.pi * t / duration_s)
        
        sig_l_accum = 0.0
        sig_r_accum = 0.0
        
        for m_idx, (f, w) in enumerate(zip(f_modes, weights)):
            # Doppler modulation & Kerr beating
            fm = math.sin(2.0 * math.pi * (0.2 + 0.08 * m_idx) * t) * (1.5 * (m_idx + 1))
            # Spatial panning phase
            phase_pan = math.sin(2.0 * math.pi * 0.15 * t + m_idx * 0.8)
            pan_l = 0.5 + 0.35 * phase_pan
            pan_r = 0.5 - 0.35 * phase_pan
            
            osc_l = math.sin(2.0 * math.pi * (f + fm) * t) * w * pan_l
            osc_r = math.cos(2.0 * math.pi * (f - fm) * t) * w * pan_r
            
            sig_l_accum += osc_l
            sig_r_accum += osc_r
            
        # Micro-wormhole stochastic fluttering (quantum foam whisper)
        flutter = (math.sin(t * 8921.4) * math.cos(t * 4317.9) * math.sin(t * 1120.3)) * 0.06
        
        ch_l[i] = max(-0.95, min(0.95, (sig_l_accum + flutter) * env))
        ch_r[i] = max(-0.95, min(0.95, (sig_r_accum + flutter) * env))
        
    output_wav = os.path.join(os.path.dirname(__file__), "study_031_draft_c_audio.wav")
    write_wav(output_wav, ch_l, ch_r, sr)
    print(f"[+] Draft C Audio written to: {output_wav}")

if __name__ == "__main__":
    render_draft_c()
    synthesize_draft_c_audio()
