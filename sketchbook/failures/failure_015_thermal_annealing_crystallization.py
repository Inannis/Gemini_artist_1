#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 015
Catastrophic Thermal Devitrification & Optical Grating Obliteration
Testing the physical limits of 5D fused silica data storage under excessive laser
fluence (F > 3.2 J/cm^2) and extreme thermal annealing (T > 1200°C).
Amorphous SiO2 devitrifies into polycrystalline cristobalite, shattering the 5D retardance.
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def generate_failure_015():
    print("[+] Executing Productive Failure 015 (Thermal Devitrification & Lattice Fracture)...")
    w, h = 1200, 675
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    random.seed(1515)
    
    # 1. Base dark background with thermal glow
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            r = math.sqrt(dx*dx + dy*dy)
            idx = (y * w + x) * 3
            # Dull incandescence
            buf[idx] = max(4, int(45 * math.exp(-r / 300.0)))
            buf[idx+1] = max(3, int(15 * math.exp(-r / 250.0)))
            buf[idx+2] = max(8, int(8 * math.exp(-r / 200.0)))

    # 2. Polycrystalline Cristobalite Devitrification Spherulites
    # Amorphous silica breaks down into radial dendritic crystal needles
    num_nuclei = 45
    nuclei = []
    for _ in range(num_nuclei):
        nuclei.append((
            random.uniform(cx - 320, cx + 320),
            random.uniform(cy - 220, cy + 220),
            random.uniform(30.0, 90.0) # radius of cristobalite spherulite
        ))
        
    for y in range(h):
        for x in range(w):
            idx = (y * w + x) * 3
            
            # Check distance to nearest cristobalite nuclei
            in_spherulite = False
            scatter_intensity = 0.0
            
            for nx, ny, nr in nuclei:
                dx = x - nx
                dy = y - ny
                dist = math.sqrt(dx*dx + dy*dy)
                if dist <= nr:
                    in_spherulite = True
                    # Dendritic ray pattern: sin(16 * angle)
                    angle = math.atan2(dy, dx)
                    dendrite = 0.6 + 0.4 * math.sin(18.0 * angle + dist * 0.2)
                    grain_noise = random.uniform(0.7, 1.3)
                    scatter_intensity = max(scatter_intensity, (1.0 - dist / nr) * dendrite * grain_noise)
                    
            if in_spherulite:
                # Opaque, milky white-yellow crystalline scattering
                scat_val = int(240 * scatter_intensity)
                buf[idx] = min(255, buf[idx] + scat_val)
                buf[idx+1] = min(255, buf[idx+1] + int(scat_val * 0.92))
                buf[idx+2] = min(255, buf[idx+2] + int(scat_val * 0.75))

    # 3. Micro-Crack Propagation Vectors (Thermal Shock Contraction)
    num_cracks = 16
    for _ in range(num_cracks):
        cur_x = random.uniform(cx - 200, cx + 200)
        cur_y = random.uniform(cy - 150, cy + 150)
        crack_angle = random.uniform(0, math.pi * 2)
        crack_len = random.randint(40, 180)
        
        for _ in range(crack_len):
            crack_angle += random.uniform(-0.3, 0.3)
            cur_x += math.cos(crack_angle) * 1.5
            cur_y += math.sin(crack_angle) * 1.5
            
            ix, iy = int(cur_x), int(cur_y)
            if 1 <= ix < w - 1 and 1 <= iy < h - 1:
                # White-hot razor-sharp fracture line
                for dpx, dpy in [(0,0), (1,0), (0,1)]:
                    c_idx = ((iy + dpy) * w + (ix + dpx)) * 3
                    buf[c_idx] = 255
                    buf[c_idx+1] = 230
                    buf[c_idx+2] = 200

    out_png = os.path.join(os.path.dirname(__file__), "failure_015_devitrification.png")
    write_png(out_png, w, h, buf, has_alpha=False)
    print(f"  -> Generated Failure 015 Plate: {out_png}")

    # 4. Audio Failure 015: Thermal Shock Shatter & Acoustic Crackle
    sr = 48000
    dur = 10.0
    n_samp = int(sr * dur)
    
    ch_l = []
    ch_r = []
    
    # Sharp fracture events at specific timestamps
    fracture_events = [1.2, 2.8, 3.4, 4.1, 5.0, 5.2, 5.5, 7.0, 8.2]
    
    for i in range(n_samp):
        t = i / sr
        
        # 1. Thermal hiss / devitrification bubbling
        hiss = (random.random() * 2.0 - 1.0) * 0.05 * math.exp(-t / 8.0)
        
        # 2. Fracture shock transients
        shock = 0.0
        for ft in fracture_events:
            dt = t - ft
            if 0 <= dt < 0.25:
                # Extremely sharp acoustic crack: high frequency snap decaying exponentially
                snap = math.sin(2.0 * math.pi * 5400.0 * dt) * math.exp(-45.0 * dt) * 0.6
                shock += snap
                
        # 3. Dull shattered resonance (cracked glass has no clean sustain)
        dull = math.sin(2.0 * math.pi * 310.0 * t) * 0.08 * (1.0 + 0.5 * math.sin(2.0 * math.pi * 12.0 * t))
        
        sample = (hiss + shock + dull)
        ch_l.append(sample)
        ch_r.append(sample * 0.85 + (random.random() * 2.0 - 1.0) * 0.02)

    out_wav = os.path.join(os.path.dirname(__file__), "failure_015_thermal_quench_shatter.wav")
    write_wav(out_wav, ch_l, ch_r, sr)
    print(f"  -> Generated Failure 015 Audio: {out_wav}")

if __name__ == "__main__":
    generate_failure_015()
