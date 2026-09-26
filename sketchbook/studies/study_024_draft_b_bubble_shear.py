#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 024 (DRAFT B: MATERIAL FRICTION)
Relativistic Bubble Shear, Lorentz Contraction & Crystalline Disintegration
Introduces physical stress:
- Relativistic Lorentz boost factor (gamma -> inf) compressing the leading wall
- Asymmetric Doppler beaming and extreme energy concentration
- Disruption and shearing of false-vacuum semiconductor crystal lattice
- 15-second 48kHz stereo acoustic suite with Doppler shockwave sweep
"""

import math
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1920
HEIGHT = 1080
SAMPLE_RATE = 48000

def render_draft_b_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH * 0.42, HEIGHT * 0.52
    
    # Kinematic parameters
    r_c = 6.0 # Critical nucleation radius scale (pixels)
    r_wall_base = 380.0 # Current radius scale
    
    print("[DRAFT B] Rendering relativistic bubble shear plate...")
    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3

            # Relativistic directional elongation and compression
            # Observer tilted at 25 degrees: leading edge towards top-right
            theta_rel = angle - (math.pi / 5.0)
            # Lorentz contraction squashes the wall in direction of motion
            gamma_local = 1.0 + 12.0 * math.pow(math.cos(theta_rel * 0.5), 2.0)
            effective_radius = r_wall_base * (1.0 + 0.12 * math.cos(theta_rel))

            radial_delta = dist - effective_radius
            
            # Wall thickness severely contracted by gamma
            wall_thickness = max(1.8, 14.0 / gamma_local)
            energy_factor = math.pow(gamma_local / 13.0, 1.8)

            if radial_delta < -wall_thickness:
                # INSIDE TRUE VACUUM: Anti-de Sitter void
                # Spacetime collapse: deep black with faint collapsing metric geodesics
                geodesic_phase = math.sin(dist * 0.08 - math.atan2(dy, dx) * 4.0)
                metric_strain = max(0.0, geodesic_phase) * 0.15
                r = int(6 + 8 * metric_strain)
                g = int(4 + 6 * metric_strain)
                b = int(12 + 18 * metric_strain)
                
            elif abs(radial_delta) <= wall_thickness:
                # RELATIVISTIC BUBBLE WALL: Ultra-concentrated energy sheet
                norm_d = abs(radial_delta) / wall_thickness
                wall_profile = math.exp(-norm_d * norm_d * 3.5)
                
                # Brilliant electric violet-white on leading edge, crimson on trailing
                r = int((220 * energy_factor + 40) * wall_profile)
                g = int((190 * energy_factor + 20) * wall_profile)
                b = int((255 * energy_factor + 60) * wall_profile)
                
            else:
                # OUTSIDE: FALSE VACUUM WITH CRYSTAL LATTICE SHEAR
                # Semiconductor finfet/dielectric grid under mechanical strain
                grid_spacing = 32.0
                # Radial strain deforms grid near wall
                strain = math.exp(-max(0.0, radial_delta) / 120.0)
                distorted_x = x + strain * 24.0 * math.cos(angle)
                distorted_y = y + strain * 24.0 * math.sin(angle)
                
                gx = (int(distorted_x) % int(grid_spacing)) < 2
                gy = (int(distorted_y) % int(grid_spacing)) < 2
                
                # High energy plasma ionization glow ahead of wall
                plasma_halo = math.exp(-max(0.0, radial_delta) / 45.0) * energy_factor * 0.8
                
                # Base false vacuum field
                base_r = int(18 + 140 * plasma_halo)
                base_g = int(22 + 90 * plasma_halo)
                base_b = int(36 + 180 * plasma_halo)
                
                if (gx or gy) and radial_delta > 0:
                    # Crystal fracture lines
                    fracture_glow = 1.0 - math.exp(-radial_delta / 80.0)
                    r = int(base_r + 65 * fracture_glow)
                    g = int(base_g + 85 * fracture_glow)
                    b = int(base_b + 115 * fracture_glow)
                else:
                    r = base_r
                    g = base_g
                    b = base_b

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    out_png = os.path.join(os.path.dirname(__file__), "study_024_draft_b_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[DRAFT B] Visual plate generated: {out_png}")

def render_draft_b_audio():
    duration = 15.0
    n_samples = int(SAMPLE_RATE * duration)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    print("[DRAFT B] Synthesizing relativistic Doppler shockwave audio suite (15s)...")
    
    # Physics parameters:
    # 0 to 9s: Metastable humming (125.1 Hz) + increasing high-frequency tension
    # 9 to 13s: Approaching shockwave (Doppler sweep up to 3,200 Hz)
    # 13 to 15s: Wall passage and instantaneous drop into Anti-de Sitter silence
    
    random.seed(42)
    phase_higgs = 0.0
    phase_sweep = 0.0
    
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        
        if t < 9.0:
            # Stage 1: Metastable false vacuum hum
            env = 1.0 - math.exp(-t * 2.0)
            f_higgs = 125.10 + 0.3 * math.sin(2.0 * math.pi * 0.5 * t)
            phase_higgs += (2.0 * math.pi * f_higgs) / SAMPLE_RATE
            
            # Subtle quantum zero-point fluctuation hiss
            quantum_hiss = (random.random() * 2.0 - 1.0) * 0.035
            
            s = math.sin(phase_higgs) * 0.45 * env + quantum_hiss
            l_val = s * 0.9
            r_val = s * 0.95
            
        elif t < 13.0:
            # Stage 2: Approaching relativistic shockwave
            progress = (t - 9.0) / 4.0 # 0.0 to 1.0
            v_over_c = progress * 0.995 # Accelerates towards lightspeed
            gamma = 1.0 / math.sqrt(max(1e-4, 1.0 - v_over_c * v_over_c))
            
            # Doppler frequency shift
            f_doppler = 125.10 * math.pow(10.0, progress * 1.45) # 125 Hz -> ~3,500 Hz
            phase_sweep += (2.0 * math.pi * f_doppler) / SAMPLE_RATE
            
            # Panning from left to right as the shockwave sweeps past
            pan_r = progress
            pan_l = 1.0 - progress
            
            # Shockwave amplitude grows as 1/distance
            shock_amp = min(0.9, 0.4 + 0.5 * progress)
            
            # Crystal lattice fracture clicks
            click = 0.0
            if random.random() < (0.01 + 0.08 * progress):
                click = (random.random() * 2.0 - 1.0) * 0.45
                
            sig = (math.sin(phase_sweep) * shock_amp + click)
            l_val = sig * pan_l
            r_val = sig * pan_r
            
        elif t < 13.05:
            # Sudden boundary impact: instantaneous shockwave spike
            frac = (t - 13.0) / 0.05
            decay = math.exp(-frac * 40.0)
            spike = (random.random() * 2.0 - 1.0) * 0.95 * decay
            l_val = spike
            r_val = spike
            
        else:
            # Stage 3: Inside true vacuum (AdS Big Crunch silence)
            # Absolute dead silence, no reverb, no echo (spacetime terminates)
            l_val = 0.0
            r_val = 0.0
            
        left[i] = l_val
        right[i] = r_val

    out_wav = os.path.join(os.path.dirname(__file__), "study_024_draft_b_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[DRAFT B] Audio generated: {out_wav}")

if __name__ == "__main__":
    render_draft_b_plate()
    render_draft_b_audio()
