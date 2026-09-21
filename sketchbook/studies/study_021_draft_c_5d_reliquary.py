#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 021 (DRAFT C: THE 5D OPTICAL RELIQUARY)
Mature Synthesis Draft 3: Concentric Archimedean 5D optical tracks in fused silica.
Harmonizes slow-axis azimuth modulation, cross-polarized isochromatic stress rings,
and tuned glass plate acoustic flexural resonances.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def generate_draft_c():
    print("[+] Executing Study 021 (Draft C: The 5D Optical Reliquary)...")
    w, h = 1920, 1080
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    disc_r = 440.0
    
    # 1. Background: Deep velvet obsidian space with subtle peripheral vignetting
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            dist_center = math.sqrt(dx*dx + dy*dy)
            
            # Subtle vignetting
            bg_lum = max(0, int(6 - 4 * (dist_center / (w * 0.6))))
            idx = (y * w + x) * 3
            buf[idx] = bg_lum
            buf[idx+1] = bg_lum + 1
            buf[idx+2] = bg_lum + 4

    # 2. Render Fused-Silica Optical Wafer Disc
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            r = math.sqrt(dx*dx + dy*dy)
            
            if r <= disc_r:
                th = math.atan2(dy, dx)
                idx = (y * w + x) * 3
                
                # Internal photoelastic stress isoclines under crossed polarizers
                # I = I_0 * sin^2(2*th) * sin^2(pi * r / delta)
                stress_factor = math.pow(math.sin(2.0 * th), 2.0) * math.pow(math.sin(math.pi * r / 85.0), 2.0)
                
                # Base optical transparency (refractive index n = 1.458)
                base_r = int(14 + 18 * (r / disc_r) + 30 * stress_factor)
                base_g = int(22 + 28 * (r / disc_r) + 40 * stress_factor)
                base_b = int(38 + 50 * (r / disc_r) + 80 * stress_factor)
                
                # Chamfered beveled wafer rim
                if r >= disc_r - 8.0:
                    rim_factor = (disc_r - r) / 8.0
                    base_r = int(base_r * rim_factor + 160 * (1.0 - rim_factor))
                    base_g = int(base_g * rim_factor + 190 * (1.0 - rim_factor))
                    base_b = int(base_b * rim_factor + 220 * (1.0 - rim_factor))
                    
                buf[idx] = min(255, base_r)
                buf[idx+1] = min(255, base_g)
                buf[idx+2] = min(255, base_b)

    # 3. Render Concentric Archimedean 5D Data Tracks
    num_tracks = 36
    for t_idx in range(num_tracks):
        track_r = 75.0 + (t_idx / num_tracks) * (disc_r - 95.0)
        num_voxels = int(track_r * 0.9)
        
        for v in range(num_voxels):
            v_angle = (v / num_voxels) * math.pi * 2.0
            
            # Slow-axis azimuth theta(r, phi)
            azimuth = 2.0 * v_angle + (track_r / 40.0)
            retardance = 0.5 + 0.5 * math.sin(v_angle * 5.0 + track_r * 0.05)
            
            vx = cx + math.cos(v_angle) * track_r
            vy = cy + math.sin(v_angle) * track_r
            
            # Draw oriented elliptical nanograting birefringence voxel
            cos_a = math.cos(azimuth)
            sin_a = math.sin(azimuth)
            
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    u = dx * cos_a + dy * sin_a
                    v_coord = -dx * sin_a + dy * cos_a
                    
                    e_dist = (u * u) / 6.0 + (v_coord * v_coord) / 1.5
                    if e_dist <= 1.0:
                        px = int(vx + dx)
                        py = int(vy + dy)
                        if 0 <= px < w and 0 <= py < h:
                            p_idx = (py * w + px) * 3
                            
                            # 5D Birefringence Color: shifts from gold to cyan based on retardance
                            r_col = int((180 + 75 * math.cos(azimuth)) * (1.0 - e_dist) * retardance)
                            g_col = int((160 + 50 * math.sin(azimuth)) * (1.0 - e_dist) * retardance)
                            b_col = int((220 - 90 * math.cos(azimuth)) * (1.0 - e_dist) * retardance)
                            
                            buf[p_idx] = min(255, buf[p_idx] + r_col)
                            buf[p_idx+1] = min(255, buf[p_idx+1] + g_col)
                            buf[p_idx+2] = min(255, buf[p_idx+2] + b_col)

    # 4. Central Spindle / Laser Aperture Center
    for y in range(int(cy - 40), int(cy + 41)):
        for x in range(int(cx - 40), int(cx + 41)):
            dx = x - cx
            dy = y - cy
            r_center = math.sqrt(dx*dx + dy*dy)
            if r_center <= 35.0:
                p_idx = (y * w + x) * 3
                if r_center <= 18.0:
                    # Clear void center
                    buf[p_idx] = 4
                    buf[p_idx+1] = 6
                    buf[p_idx+2] = 10
                else:
                    # Gold-plated central clamp collar
                    collar_norm = (r_center - 18.0) / 17.0
                    col_int = int(180 * math.sin(collar_norm * math.pi))
                    buf[p_idx] = min(255, buf[p_idx] + col_int)
                    buf[p_idx+1] = min(255, buf[p_idx+1] + int(col_int * 0.8))
                    buf[p_idx+2] = min(255, buf[p_idx+2] + int(col_int * 0.3))

    out_png = os.path.join(os.path.dirname(__file__), "study_021_draft_c_plate.png")
    write_png(out_png, w, h, buf, has_alpha=False)
    print(f"  -> Generated Draft C Plate: {out_png}")

    # 5. Audio Draft C: Deep-Time Fused Silica Acoustic Suite
    # Harmonizes:
    # - 43.2 Hz flexural glass disc sub-drone
    # - 432 Hz dual carrier with 2.5 Hz binaural slow-axis precession
    # - Tuned crystalline glass chime pings (bandpass-filtered resonant strikes)
    sr = 48000
    dur = 20.0
    n_samp = int(sr * dur)
    
    ch_l = []
    ch_r = []
    
    # Pre-calculate chime hit times
    chime_times = [2.5, 6.0, 10.5, 15.0, 18.2]
    
    for i in range(n_samp):
        t = i / sr
        
        # 1. 43.2 Hz Glass Flexural Fundamental (Euler-Bernoulli circular plate mode)
        sub = math.sin(2.0 * math.pi * 43.2 * t) * 0.28
        
        # 2. 432 Hz Binaural Dual Carrier (Slow-axis azimuthal precession)
        car_l = math.sin(2.0 * math.pi * 432.0 * t) * 0.16
        car_r = math.sin(2.0 * math.pi * 434.5 * t) * 0.16
        
        # 3. Crystalline Glass Chime Strikes (femtosecond laser acoustic dispersion)
        chimes_l = 0.0
        chimes_r = 0.0
        for hit_t in chime_times:
            dt = t - hit_t
            if 0 <= dt < 4.0:
                decay = math.exp(-2.2 * dt)
                # Resonant frequencies of fused silica disc: 1728 Hz, 2592 Hz, 3456 Hz
                strike = (math.sin(2.0 * math.pi * 1728.0 * dt) * 0.5 +
                          math.sin(2.0 * math.pi * 2592.0 * dt) * 0.3 +
                          math.sin(2.0 * math.pi * 3456.0 * dt) * 0.15) * decay * 0.18
                chimes_l += strike
                chimes_r += strike * 0.85
                
        # Master mix with smooth 1.5s fade-in and 2.0s fade-out
        fade = min(1.0, t / 1.5) * min(1.0, (dur - t) / 2.0)
        
        ch_l.append((sub + car_l + chimes_l) * fade)
        ch_r.append((sub + car_r + chimes_r) * fade)

    out_wav = os.path.join(os.path.dirname(__file__), "study_021_draft_c_audio.wav")
    write_wav(out_wav, ch_l, ch_r, sr)
    print(f"  -> Generated Draft C Audio: {out_wav}")

if __name__ == "__main__":
    generate_draft_c()
