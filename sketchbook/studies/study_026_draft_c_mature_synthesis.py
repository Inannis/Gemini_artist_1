#!/usr/bin/env python3
"""
STUDY 026 · DRAFT C (MATURE SYNTHESIS)
Series XXXII: Conformal Cyclic Cosmology & The Penrose Crossover
Mature synthesis uniting dual-conformal metric projection, Planckian CMB
temperature multipoles, quadrupolar gravitational wave shear, Stokes Q/U
polarization streamlines, and a 30-second multi-movement acoustic suite.
Zero external dependencies.
"""

import math
import random
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1920
HEIGHT = 1080

def compute_cmb_fluctuation(x, y):
    """Multi-scale procedural Planckian CMB temperature field."""
    val = 0.0
    freqs = [0.006, 0.014, 0.032, 0.075, 0.16]
    weights = [0.45, 0.28, 0.16, 0.08, 0.03]
    
    for f, w in zip(freqs, weights):
        nx = x * f
        ny = y * f
        # Pseudo-random isotropic Fourier phase harmonics
        s1 = math.sin(nx * 1.73 + ny * 0.94 + 1.23)
        s2 = math.cos(nx * 0.81 - ny * 1.57 + 2.45)
        s3 = math.sin((nx + ny) * 1.11 - 0.77)
        val += (s1 * 0.4 + s2 * 0.4 + s3 * 0.2) * w
    return val

def render_draft_c_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH * 0.5, HEIGHT * 0.5
    
    # Angular scale: 1 deg = 26 pixels at 1080p
    deg_px = 26.0
    r1 = 4.2 * deg_px   # 109.2 px
    r2 = 11.8 * deg_px  # 306.8 px
    r3 = 24.5 * deg_px  # 637.0 px
    w_px = 1.2 * deg_px # 31.2 px
    
    # Gravitational shear tensor amplitudes (h+, hx)
    eps_plus = 0.085
    eps_cross = 0.045
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            phi = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3
            
            # 1. Quadrupolar gravitational shear metric deformation
            strain = 1.0 + eps_plus * math.cos(2.0 * phi) + eps_cross * math.sin(2.0 * phi)
            eff_dist = dist / max(0.4, strain)
            
            # 2. Conformal factor Omega: smooth vanishing towards exterior
            # Omega passes through zero at the horizon boundary
            omega = max(0.0, 1.0 - (dist / (WIDTH * 0.55)) ** 1.6)
            
            # 3. Base Planckian CMB field
            cmb_raw = compute_cmb_fluctuation(x, y)
            
            # 4. Concentric variance suppression & Stokes Q/U polarization
            var_factor = 1.0
            ring_intensity = 0.0
            stokes_shear = 0.0
            
            for r_target in [r1, r2, r3]:
                delta = abs(eff_dist - r_target)
                if delta < w_px * 2.5:
                    prox = math.exp(-0.5 * (delta / (w_px * 0.5)) ** 2)
                    ring_intensity = max(ring_intensity, prox)
                    # Variance suppressed by 32% inside ring
                    var_factor = min(var_factor, 1.0 - 0.32 * prox)
                    # Stokes polarization curl tangent to rings
                    stokes_shear += prox * math.sin(4.0 * phi)
                    
            # Modulate CMB fluctuation by suppressed variance
            cmb_val = cmb_raw * var_factor
            
            # 5. Dual-conformal color grading:
            # Cold CMB void (Prussian blue / slate) -> Warm CMB peaks (amber / bronze)
            # Rings: eerie luminescent lapis lazuli with platinum polarization filaments
            
            norm_t = 0.5 + 0.5 * cmb_val
            norm_t = max(0.0, min(1.0, norm_t))
            
            if cmb_val < 0:
                t = -cmb_val
                # Deep ultramarine / cobalt cold regions
                r = int(12 + 25 * (1.0 - t))
                g = int(22 + 45 * (1.0 - t))
                b = int(55 + 130 * t)
            else:
                t = cmb_val
                # Luminous amber / bronze warm regions
                r = int(45 + 180 * t)
                g = int(32 + 125 * t)
                b = int(28 + 60 * t)
                
            # Imprint ring stillness & polarization hairline structure
            if ring_intensity > 0.01:
                # Stillness cooling: shift towards pure cosmic blue-black
                cool_factor = ring_intensity * 0.45
                r = int(r * (1.0 - cool_factor) + 18 * cool_factor)
                g = int(g * (1.0 - cool_factor) + 38 * cool_factor)
                b = int(b * (1.0 - cool_factor) + 85 * cool_factor)
                
                # Stokes polarization fine concentric filaments
                hairline = math.sin(eff_dist * 0.45) * math.cos(4.0 * phi)
                if abs(hairline) > 0.75:
                    hl_glow = ring_intensity * 75.0
                    r = int(min(255, r + hl_glow * 0.9))
                    g = int(min(255, g + hl_glow * 0.85))
                    b = int(min(255, b + hl_glow))
                    
            # 6. Central Hawking point focal aperture
            if dist < 12.0:
                core_p = 1.0 - dist / 12.0
                core_glow = core_p * core_p * 255.0
                r = int(min(255, r + core_glow * 0.95))
                g = int(min(255, g + core_glow * 0.92))
                b = int(min(255, b + core_glow))
                
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b
            
    out_path = os.path.join(os.path.dirname(__file__), "study_026_draft_c_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT C] Generated Mature Synthesis plate: {out_path}")

def render_draft_c_audio():
    sample_rate = 48000
    duration_sec = 30.0
    total_samples = int(sample_rate * duration_sec)
    
    ch_l = []
    ch_r = []
    
    f_sub = 43.2      # CMB baseline fundamental
    f_ring1 = 58.4    # Ring I modal tone
    f_ring2 = 118.0   # Ring II harmonic
    f_ring3 = 245.0   # Ring III outer boundary resonance
    
    noise_filt = 0.0
    
    for i in range(total_samples):
        t = i / sample_rate
        
        # Movement I (0.0 to 10.0s): The Massless Asymptotic Void (Omega -> 0)
        # Movement II (10.0 to 20.0s): The Conformal Crossover (Sigma Hypersurface)
        # Movement III (20.0 to 30.0s): Concentric Hawking Point Inscription
        
        # 1. Background CMB Brownian filtered noise
        raw_noise = random.gauss(0.0, 0.25)
        noise_filt = 0.97 * noise_filt + 0.03 * raw_noise
        
        # 2. Movement I: Sub-harmonic drone with subtle breathing
        m1_amp = max(0.0, min(1.0, 1.0 - (t - 8.0) / 4.0)) if t > 8.0 else min(1.0, t / 2.0)
        drone = m1_amp * 0.3 * math.sin(2.0 * math.pi * f_sub * t)
        
        # 3. Movement II: Crossover sweep (10s to 20s)
        # Glissando sweeping through zero-mass threshold
        crossover_sig_l = 0.0
        crossover_sig_r = 0.0
        if 8.0 < t < 22.0:
            p = (t - 8.0) / 14.0
            amp = 0.38 * math.sin(p * math.pi)
            freq = 43.2 + (287.89 - 43.2) * (p ** 2.2)
            phase = 2.0 * math.pi * freq * t
            # Quadrupole binaural rotation
            crossover_sig_l = amp * math.sin(phase)
            crossover_sig_r = amp * math.sin(phase + math.pi * 0.5)
            
        # 4. Movement III: Concentric Ring Resonances (18s to 30s)
        ring_sig_l = 0.0
        ring_sig_r = 0.0
        if t > 18.0:
            m3_amp = min(1.0, (t - 18.0) / 3.0)
            if t > 27.0:
                m3_amp *= (30.0 - t) / 3.0
                
            # Triad of concentric ring frequencies
            r1_tone = 0.22 * math.sin(2.0 * math.pi * f_ring1 * t)
            r2_tone = 0.16 * math.sin(2.0 * math.pi * f_ring2 * t + 0.7)
            r3_tone = 0.12 * math.sin(2.0 * math.pi * f_ring3 * t + 1.4)
            
            # Subtle amplitude modulation at Hawking angular frequency ratios (4.2 Hz)
            am_mod = 0.8 + 0.2 * math.sin(2.0 * math.pi * 4.2 * t)
            
            ring_sum = (r1_tone + r2_tone + r3_tone) * am_mod * m3_amp
            ring_sig_l = ring_sum * 0.9
            ring_sig_r = ring_sum * 1.1
            
        # Composite audio stream
        left = drone + noise_filt * 0.25 + crossover_sig_l + ring_sig_l
        right = drone + noise_filt * 0.25 + crossover_sig_r + ring_sig_r
        
        # Overall master envelope
        env = 1.0
        if t < 1.0:
            env = t
        elif t > 28.5:
            env = max(0.0, (30.0 - t) / 1.5)
            
        left *= env
        right *= env
        
        ch_l.append(max(-1.0, min(1.0, left)))
        ch_r.append(max(-1.0, min(1.0, right)))
        
    out_path = os.path.join(os.path.dirname(__file__), "study_026_draft_c_audio.wav")
    write_wav(out_path, ch_l, ch_r, sample_rate)
    print(f"[DRAFT C] Generated Mature Synthesis audio: {out_path}")

def main():
    render_draft_c_plate()
    render_draft_c_audio()

if __name__ == "__main__":
    main()

