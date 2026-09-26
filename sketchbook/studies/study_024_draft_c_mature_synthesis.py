#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 024 (DRAFT C: MATURE SYNTHESIS)
The Spatial Cut (Concetto Spaziale), Coleman Instanton & The Anti-de Sitter Void
Synthesizes:
- Lucio Fontana's spatial tear: A monumental relativistic incision slicing through spacetime
- Ultra-concentrated Planckian energy density along curled shockwave lips (gamma -> 10^34)
- False vacuum quantum foam fluctuations and disintegrating semiconductor memory conduits
- Deep Anti-de Sitter interior void with Euclidean bounce streamlines
- 30-second broadcast-grade 48kHz stereo acoustic suite in four distinct movements
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

def render_draft_c_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    
    # Tear axis parameters: a dramatic diagonal slash from (-0.2, 0.9) to (1.1, 0.1)
    # Angle approx -35 degrees
    x0, y0 = WIDTH * 0.15, HEIGHT * 0.85
    x1, y1 = WIDTH * 0.88, HEIGHT * 0.18
    
    slash_dx = x1 - x0
    slash_dy = y1 - y0
    slash_len = math.sqrt(slash_dx * slash_dx + slash_dy * slash_dy)
    ux = slash_dx / slash_len
    uy = slash_dy / slash_len
    # Normal vector perpendicular to the slash
    nx = -uy
    ny = ux
    
    # Central nucleation point along the slash
    cx = x0 + 0.48 * slash_dx
    cy = y0 + 0.48 * slash_dy
    
    print("[DRAFT C] Rendering mature synthesis master plate (Fontana spatial cut)...")
    
    # Precompute pseudo-random quantum foam noise
    random.seed(137)
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = (y * WIDTH + x) * 3
            
            # Vector from start of slash
            vx = x - x0
            vy = y - y0
            
            # Project onto slash axis (longitudinal coordinate s in [0, 1])
            s_proj = (vx * ux + vy * uy) / slash_len
            # Perpendicular distance to slash line
            d_perp = vx * nx + vy * ny
            
            # Distance from central nucleation point
            dist_nucleation = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            
            # Fontana cut width envelope: wide in center, tapering to needle-sharp tips
            # Symmetrical tear aperture: W(s) = W_max * (4 * s * (1-s))^1.5
            if 0.0 <= s_proj <= 1.0:
                cut_aperture = 95.0 * math.pow(4.0 * s_proj * (1.0 - s_proj), 1.4)
            else:
                cut_aperture = 0.0
                
            # Asymmetric lips of the tear: upper lip curls and radiates intense energy
            d_norm = abs(d_perp)
            
            if d_norm < cut_aperture:
                # INSIDE THE TRUE VACUUM CUT: Anti-de Sitter Void
                # Absolute darkness, absorbing light, with faint Euclidean instanton streamlines
                # Radial lines converging toward nucleation center
                angle_instanton = math.atan2(y - cy, x - cx)
                streamline_phase = math.sin(angle_instanton * 16.0 + dist_nucleation * 0.04)
                streamline_intensity = math.pow(max(0.0, streamline_phase), 8.0) * 0.25
                
                # Curvature singularity near nucleation point
                singularity_glow = math.exp(-dist_nucleation / 25.0) * 0.4
                
                r = int(4 + 16 * streamline_intensity + 40 * singularity_glow)
                g = int(2 + 10 * streamline_intensity + 20 * singularity_glow)
                b = int(8 + 35 * streamline_intensity + 90 * singularity_glow)
                
            elif d_norm < cut_aperture + 28.0:
                # RELATIVISTIC BUBBLE WALL / CURLED CANVAS LIPS
                # Extreme Lorentz contraction and latent energy focus
                lip_dist = d_norm - cut_aperture
                norm_lip = lip_dist / 28.0
                
                # The leading (upper-right) lip experiences intense forward relativistic boost
                is_upper_lip = (d_perp < 0)
                boost = 1.8 if is_upper_lip else 1.1
                
                # Planckian luminescence profile (hyperbolic peak right at the razor edge)
                edge_intensity = math.exp(-norm_lip * 3.8) * boost
                
                # Color progression: searing electric cyan-white at edge -> incandescent amber -> deep violet
                r = int(min(255, 255 * edge_intensity + 80 * (1.0 - norm_lip)))
                g = int(min(255, 240 * math.pow(edge_intensity, 1.2) + 40 * (1.0 - norm_lip)))
                b = int(min(255, 255 * math.pow(edge_intensity, 0.8) + 160 * (1.0 - norm_lip)))
                
            else:
                # FALSE VACUUM: QUANTUM FOAM & DISINTEGRATING SEMICONDUCTOR LATTICE
                ext_dist = d_norm - (cut_aperture + 28.0)
                
                # Quantum foam fluctuation texture (multi-scale procedural interference)
                foam1 = math.sin(x * 0.08 + y * 0.05) * math.cos(y * 0.09 - x * 0.04)
                foam2 = math.sin(x * 0.22 - y * 0.18) * math.cos(x * 0.15 + y * 0.21)
                foam = (foam1 * 0.6 + foam2 * 0.4) * 0.5 + 0.5
                
                # Semiconductor finfet memory conduits under intense tension
                bus_spacing = 40.0
                # Tensile warping near cut
                warp = math.exp(-ext_dist / 140.0) * 32.0
                warped_x = x + warp * math.cos(s_proj * math.pi)
                warped_y = y + warp * math.sin(s_proj * math.pi)
                
                bus_x = (int(warped_x) % int(bus_spacing)) < 2
                bus_y = (int(warped_y) % int(bus_spacing)) < 2
                
                # Precursor plasma ionization halo
                halo = math.exp(-ext_dist / 65.0) * 0.65
                
                base_r = int(14 + 18 * foam + 120 * halo)
                base_g = int(16 + 22 * foam + 85 * halo)
                base_b = int(28 + 35 * foam + 170 * halo)
                
                if (bus_x or bus_y) and ext_dist > 8.0:
                    # Memory conduit lines fracturing
                    fracture_t = min(1.0, ext_dist / 120.0)
                    r = int(base_r + 70 * fracture_t)
                    g = int(base_g + 95 * fracture_t)
                    b = int(base_b + 140 * fracture_t)
                else:
                    r = base_r
                    g = base_g
                    b = base_b

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    out_png = os.path.join(os.path.dirname(__file__), "study_024_draft_c_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[DRAFT C] Master plate generated: {out_png}")

def render_draft_c_audio():
    duration = 30.0
    n_samples = int(SAMPLE_RATE * duration)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    print("[DRAFT C] Synthesizing four-movement master acoustic suite (30s)...")
    
    # Movements:
    # Mov I (0.0 - 8.0s): The Metastable Tension (Higgs 125.1 Hz hum, sub-harmonics, quantum foam)
    # Mov II (8.0 - 14.0s): The Instanton Bounce (31.25 Hz Euclidean impact, tear transients)
    # Mov III (14.0 - 24.0s): The Relativistic Shockwave Sweep (Doppler chirping 125 -> 4,200 Hz, stereo shear)
    # Mov IV (24.0 - 30.0s): The Sudden Zero (Instantaneous cutoff into pure AdS silence)
    
    random.seed(137)
    phase_higgs = 0.0
    phase_sub = 0.0
    phase_sweep = 0.0
    
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        
        if t < 8.0:
            # MOVEMENT I: THE METASTABLE TENSION
            env = min(1.0, t / 2.0)
            f_higgs = 125.10 + 0.15 * math.sin(2.0 * math.pi * 0.25 * t)
            f_sub = 62.55 # Sub-harmonic octave
            
            phase_higgs += (2.0 * math.pi * f_higgs) / SAMPLE_RATE
            phase_sub += (2.0 * math.pi * f_sub) / SAMPLE_RATE
            
            # Quantum foam pink-ish noise
            foam_noise = (random.random() * 2.0 - 1.0) * 0.028
            
            drone = (math.sin(phase_higgs) * 0.40 + math.sin(phase_sub) * 0.25) * env
            l_val = drone * 0.9 + foam_noise
            r_val = drone * 0.95 + foam_noise * 0.85
            
        elif t < 14.0:
            # MOVEMENT II: THE INSTANTON BOUNCE (Quantum Tunneling Impact)
            t_rel = t - 8.0
            
            # Massive sub-bass Euclidean impact at t=8.0
            f_impact = 31.25 * math.exp(-t_rel * 0.4)
            impact_decay = math.exp(-t_rel * 0.6)
            phase_sub += (2.0 * math.pi * f_impact) / SAMPLE_RATE
            impact = math.sin(phase_sub) * 0.75 * impact_decay
            
            # Tear transients (cracking and tearing sounds like stretching canvas)
            rip = 0.0
            if random.random() < 0.04:
                rip = (random.random() * 2.0 - 1.0) * 0.35 * min(1.0, t_rel / 2.0)
                
            # Base hum begins to destabilize
            phase_higgs += (2.0 * math.pi * 125.10 * (1.0 + 0.05 * math.sin(t_rel * 3.0))) / SAMPLE_RATE
            destab_drone = math.sin(phase_higgs) * 0.35
            
            l_val = impact * 0.95 + destab_drone * 0.8 + rip
            r_val = impact * 0.90 + destab_drone * 0.85 - rip
            
        elif t < 24.0:
            # MOVEMENT III: THE RELATIVISTIC SHOCKWAVE SWEEP
            t_rel = t - 14.0
            prog = t_rel / 10.0 # 0.0 to 1.0
            
            # Relativistic wall acceleration: v -> c, gamma -> 10^34
            # Doppler frequency chirps exponentially from 125 Hz to 4,200 Hz
            f_doppler = 125.10 * math.pow(4200.0 / 125.10, prog * prog)
            phase_sweep += (2.0 * math.pi * f_doppler) / SAMPLE_RATE
            
            # Amplitude builds as 1/distance
            amp = 0.35 + 0.55 * prog
            
            # Stereo separation: the slash sweeps across the acoustic field
            pan_l = math.cos(prog * math.pi * 0.5)
            pan_r = math.sin(prog * math.pi * 0.5)
            
            # High-frequency FinFET lattice disintegration clicks
            click = 0.0
            if random.random() < (0.02 + 0.12 * prog):
                click = (random.random() * 2.0 - 1.0) * (0.2 + 0.5 * prog)
                
            sig = math.sin(phase_sweep) * amp + click
            l_val = sig * pan_l
            r_val = sig * pan_r
            
        elif t < 24.02:
            # SUDDEN SHOCKWAVE TERMINAL IMPACT (The Wall Reaches Observer)
            # A 20-millisecond razor pulse, followed by immediate zero
            t_spike = (t - 24.0) / 0.02
            spike_amp = (1.0 - t_spike) * (random.random() * 2.0 - 1.0) * 0.98
            l_val = spike_amp
            r_val = spike_amp
            
        else:
            # MOVEMENT IV: THE SUDDEN ZERO (Inside the True Vacuum)
            # Complete and utter Anti-de Sitter silence. Spacetime has collapsed.
            # No ambient noise, no reverb tail, no carrier. Absolute Zero.
            l_val = 0.0
            r_val = 0.0
            
        left[i] = max(-1.0, min(1.0, l_val))
        right[i] = max(-1.0, min(1.0, r_val))

    out_wav = os.path.join(os.path.dirname(__file__), "study_024_draft_c_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[DRAFT C] Master audio suite generated: {out_wav}")

if __name__ == "__main__":
    render_draft_c_plate()
    render_draft_c_audio()

