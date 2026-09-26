#!/usr/bin/env python3
"""
STUDY 026 · DRAFT B (MATERIAL FRICTION)
Series XXXII: Conformal Cyclic Cosmology & The Penrose Crossover
Introduces physical Planckian CMB temperature multipoles, quadrupolar
gravitational wave strain (h+, hx), true variance suppression,
and a 15-second acoustic shear draft.
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

WIDTH = 1280
HEIGHT = 720

def generate_octave_noise(x, y, octaves=4):
    """Zero-dependency pseudo-continuous octave noise."""
    val = 0.0
    freq = 0.015
    amp = 1.0
    total_amp = 0.0
    for o in range(octaves):
        # Lattice hashing
        nx = x * freq + o * 17.31
        ny = y * freq + o * 31.17
        s = math.sin(nx * 1.414 + ny * 2.718) * math.cos(nx * 3.141 - ny * 1.618)
        val += s * amp
        total_amp += amp
        freq *= 2.1
        amp *= 0.52
    return val / total_amp

def render_draft_b_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Ring parameters (Penrose Hawking point radii)
    r1 = 4.2 * 18.0   # 75.6 px
    r2 = 11.8 * 18.0  # 212.4 px
    r3 = 24.5 * 18.0  # 441.0 px
    w = 1.2 * 18.0    # 21.6 px
    
    # Quadrupolar gravitational shear parameters
    eps_plus = 0.12    # h+ strain amplitude
    eps_cross = 0.06   # hx strain amplitude
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            phi = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3
            
            # Quadrupolar strain distortion
            strain = 1.0 + eps_plus * math.cos(2.0 * phi) + eps_cross * math.sin(2.0 * phi)
            eff_dist = dist / max(0.5, strain)
            
            # Conformal factor Omega compression: Omega(r) = 1 / (1 + (r/300)^2)
            omega = 1.0 / (1.0 + (dist / 320.0) ** 1.8)
            
            # Synthetic Planck CMB temperature fluctuation
            cmb_noise = generate_octave_noise(x, y, octaves=5)
            
            # Determine variance suppression inside concentric rings
            var_factor = 1.0
            ring_proximity = 0.0
            for target_r in [r1, r2, r3]:
                d = abs(eff_dist - target_r)
                if d < w * 2.2:
                    prox = math.exp(-0.5 * (d / (w * 0.6)) ** 2)
                    ring_proximity = max(ring_proximity, prox)
                    # Variance suppression: sigma^2 -> 0.68 sigma_0^2
                    var_factor = min(var_factor, 1.0 - 0.32 * prox)
                    
            # Modulate CMB temperature amplitude by variance factor
            temp_fluc = cmb_noise * var_factor
            
            # Palette mapping:
            # Cold CMB fluctuations -> deep Prussian blue & indigo
            # Warm CMB fluctuations -> golden amber & bronze
            # Rings -> calm, luminous lapis lazuli with subtle cyan polarization edges
            base_val = 0.5 + 0.45 * temp_fluc
            base_val = max(0.0, min(1.0, base_val))
            
            # Polarization highlight on ring boundaries
            pol_glow = ring_proximity * 45.0
            
            if temp_fluc < 0.0:
                # Cold spot: deep ultramarine
                t = -temp_fluc
                r = int(max(0, min(255, 12 + t * 40 - pol_glow * 0.2)))
                g = int(max(0, min(255, 20 + t * 70 + pol_glow * 0.5)))
                b = int(max(0, min(255, 60 + t * 140 + pol_glow)))
            else:
                # Warm spot: amber / gold
                t = temp_fluc
                r = int(max(0, min(255, 30 + t * 180 + pol_glow * 0.8)))
                g = int(max(0, min(255, 24 + t * 130 + pol_glow * 0.7)))
                b = int(max(0, min(255, 45 + t * 50 + pol_glow * 0.4)))
                
            # Central Hawking point focal core
            if dist < 8.0:
                core_t = 1.0 - dist / 8.0
                r = int(min(255, r + 220 * core_t))
                g = int(min(255, g + 210 * core_t))
                b = int(min(255, b + 240 * core_t))
                
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b
            
    out_path = os.path.join(os.path.dirname(__file__), "study_026_draft_b_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT B] Generated Material Friction plate: {out_path}")

def render_draft_b_audio():
    sample_rate = 48000
    duration_sec = 15.0
    total_samples = int(sample_rate * duration_sec)
    
    ch_l = []
    ch_r = []
    
    f_sub = 43.2      # CMB sub-drone (OPUS-030 Bessel fundamental)
    f_start = 58.4    # Quadrupole start frequency
    f_end = 287.89    # GW150914 remnant QNM frequency
    
    # Simple recursive noise filter state
    noise_filt = 0.0
    
    for i in range(total_samples):
        t = i / sample_rate
        
        # Movement I (0.0 to 7.0s): CMB Thermal Void & Sub-Drone
        # Movement II (7.0 to 15.0s): Gravitational Wave Shear Sweep
        
        # 1. Thermal CMB background noise (Brownian low-pass)
        raw_noise = random.gauss(0.0, 0.3)
        noise_filt = 0.96 * noise_filt + 0.04 * raw_noise
        
        # 2. Sub-harmonic de Sitter drone
        drone = 0.28 * math.sin(2.0 * math.pi * f_sub * t)
        
        # 3. Quadrupole gravitational shear sweep
        shear_amp = 0.0
        shear_sig_l = 0.0
        shear_sig_r = 0.0
        if t > 6.0:
            sweep_p = (t - 6.0) / 9.0  # 0 to 1
            shear_amp = 0.35 * (0.5 - 0.5 * math.cos(math.pi * sweep_p))
            cur_freq = f_start + (f_end - f_start) * (sweep_p ** 1.8)
            
            # Quadrupole binaural phase offset (pi/2)
            phase_l = 2.0 * math.pi * cur_freq * t
            phase_r = phase_l + math.pi * 0.5
            
            shear_sig_l = shear_amp * math.sin(phase_l)
            shear_sig_r = shear_amp * math.sin(phase_r)
            
        # Combine
        left = drone + noise_filt * 0.35 + shear_sig_l
        right = drone + noise_filt * 0.35 + shear_sig_r
        
        # Fade envelope
        env = 1.0
        if t < 1.0:
            env = t
        elif t > 14.0:
            env = (15.0 - t)
        left *= env
        right *= env
        
        ch_l.append(max(-1.0, min(1.0, left)))
        ch_r.append(max(-1.0, min(1.0, right)))
        
    out_path = os.path.join(os.path.dirname(__file__), "study_026_draft_b_audio.wav")
    write_wav(out_path, ch_l, ch_r, sample_rate)
    print(f"[DRAFT B] Generated Material Friction audio: {out_path}")

def main():
    render_draft_b_plate()
    render_draft_b_audio()

if __name__ == "__main__":
    render_draft_b_plate()
    render_draft_b_audio()
