"""
STUDIO ANAMNESIS · SKETCHBOOK · STUDY 007
The Geological Core Sample (Borehole at -500m)
Study for Series XVII: The Deep Lithosphere & Subterranean Conduits

Simulates geological stratigraphy across a 500-meter core sample:
1. Topsoil & Quaternary Alluvium (0 to -50m)
2. Carboniferous Coal Seam (-50m to -160m)
3. Basalt Sill & Metamorphic Slate (-160m to -340m)
4. Pre-Cambrian Gneiss & Quartz Pegmatite (-340m to -500m)
Traversed by vertical armored fiber-optic borehole conduits.
"""

import math
import random
import os
import sys

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def run_study_007():
    print("[STUDY-007] Simulating Geological Core Stratigraphy (-500m)...")
    
    # 1. Visual Plate: Core Trays (1920x1080)
    # Five horizontal core trays representing 100m depth increments
    width = 1920
    height = 1080
    buffer = bytearray([8, 10, 14] * (width * height)) # Deep basalt slate ground
    
    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buffer[idx] = int(buffer[idx] * (1.0 - alpha) + r * alpha)
            buffer[idx+1] = int(buffer[idx+1] * (1.0 - alpha) + g * alpha)
            buffer[idx+2] = int(buffer[idx+2] * (1.0 - alpha) + b * alpha)

    def draw_line(x0, y0, x1, y1, r, g, b, alpha=1.0):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            set_pixel(x0, y0, r, g, b, alpha)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    # Background grid & measurement lines
    for x in range(120, width - 120, 120):
        for y in range(80, height - 80, 4):
            set_pixel(x, y, 28, 35, 45, 0.3)
    for y in range(80, height - 80, 100):
        for x in range(120, width - 120, 4):
            set_pixel(x, y, 28, 35, 45, 0.3)

    # 5 Cylindrical Rock Core Sections (each 100m interval)
    tray_height = 110
    tray_y_starts = [130, 290, 450, 610, 770]
    tray_depths = ["0m to -100m : ALLUVIUM & QUATERNARY SILT",
                   "-100m to -200m : CARBONIFEROUS COAL & BITUMINOUS SHALE",
                   "-200m to -300m : BASALT SILL & OLIVINE INTRUSION",
                   "-300m to -400m : METAMORPHIC SLATE & PYRITE VEINS",
                   "-400m to -500m : PRE-CAMBRIAN GNEISS & OPTICAL QUARTZ PEGMATITE"]

    random.seed(500)

    for t_idx, y_start in enumerate(tray_y_starts):
        core_y_center = y_start + tray_height // 2
        core_radius = 38
        
        # Draw wooden/steel core channel container
        for x in range(160, width - 160):
            set_pixel(x, y_start - 2, 45, 55, 68, 0.8)
            set_pixel(x, y_start + tray_height + 2, 45, 55, 68, 0.8)
            
        # Draw core cylinder with cylindrical shading and procedural mineral textures
        for cy in range(-core_radius, core_radius + 1):
            y_curr = core_y_center + cy
            # Cylindrical normal falloff: cos(theta)
            cos_cyl = math.sqrt(max(0.0, 1.0 - (cy / core_radius) ** 2))
            
            for cx in range(180, width - 180):
                u = (cx - 180) / (width - 360)
                
                # Base mineral coloring depending on geological depth tier
                if t_idx == 0:
                    # Alluvium: Ochre, clay, sandy silt
                    noise_val = math.sin(u * 80.0 + cy * 0.2) * math.cos(u * 25.0)
                    r_base = 160 + int(35 * noise_val)
                    g_base = 125 + int(25 * noise_val)
                    b_base = 80 + int(15 * noise_val)
                elif t_idx == 1:
                    # Carboniferous coal: Pitch obsidian black with vitreous cleavage glints
                    is_cleavage = (math.sin(u * 140.0 + cy * 0.8) > 0.88)
                    if is_cleavage:
                        r_base, g_base, b_base = 210, 215, 230
                    else:
                        r_base = 24 + int(8 * math.sin(u * 50.0))
                        g_base = 26 + int(8 * math.sin(u * 50.0))
                        b_base = 32 + int(12 * math.cos(u * 30.0))
                elif t_idx == 2:
                    # Basalt with olive-green peridotite specks
                    is_olivine = (random.random() < 0.04)
                    if is_olivine:
                        r_base, g_base, b_base = 85, 140, 75
                    else:
                        r_base = 52 + int(15 * math.sin(u * 110.0))
                        g_base = 56 + int(15 * math.sin(u * 110.0))
                        b_base = 65 + int(18 * math.sin(u * 110.0))
                elif t_idx == 3:
                    # Slate with golden brass pyrite (fool's gold) veins
                    is_pyrite = (abs(cy - int(12 * math.sin(u * 14.0))) < 3)
                    if is_pyrite:
                        r_base, g_base, b_base = 240, 205, 75
                    else:
                        r_base = 70 + int(20 * math.sin(u * 90.0))
                        g_base = 75 + int(20 * math.sin(u * 90.0))
                        b_base = 88 + int(25 * math.sin(u * 90.0))
                else:
                    # Gneiss with luminous white/pink quartz pegmatite band
                    is_quartz = (abs(cy + int(16 * math.cos(u * 8.0))) < 14)
                    if is_quartz:
                        r_base, g_base, b_base = 235, 240, 255 # Pure optical quartz
                    else:
                        r_base = 110 + int(35 * math.sin(u * 60.0))
                        g_base = 95 + int(30 * math.sin(u * 60.0))
                        b_base = 105 + int(30 * math.sin(u * 60.0))
                        
                # Shading with cylindrical raking illumination
                lum = 0.25 + 0.75 * cos_cyl
                # Highlight glint at top edge
                if -core_radius + 4 <= cy <= -core_radius + 8:
                    lum = min(1.3, lum * 1.4)
                    
                r_final = min(255, max(0, int(r_base * lum)))
                g_final = min(255, max(0, int(g_base * lum)))
                b_final = min(255, max(0, int(b_base * lum)))
                
                set_pixel(cx, y_curr, r_final, g_final, b_final, 1.0)
                
        # Draw modern vertical fiber borehole penetration
        # An armored conduit puncturing through the rock core
        borehole_x = int(180 + (width - 360) * (0.35 + 0.1 * t_idx))
        for dy in range(-core_radius - 8, core_radius + 9):
            y_b = core_y_center + dy
            # Copper casing
            set_pixel(borehole_x - 3, y_b, 185, 115, 60, 0.95)
            set_pixel(borehole_x + 3, y_b, 185, 115, 60, 0.95)
            # Optical fiber glowing core
            set_pixel(borehole_x, y_b, 56, 189, 248, 1.0) # Bright cyan laser pulse
            set_pixel(borehole_x - 1, y_b, 120, 220, 255, 0.8)
            set_pixel(borehole_x + 1, y_b, 120, 220, 255, 0.8)

    # Inscribe depth measurement ticks
    for x in range(180, width - 180, 80):
        for y_start in tray_y_starts:
            draw_line(x, y_start + tray_height - 6, x, y_start + tray_height, 90, 115, 145, 0.7)

    png_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_007_core_sample.png"))
    write_png(png_path, width, height, bytes(buffer))
    print(f"[STUDY-007] Visual plate written to: {png_path}")

    # 2. Acoustic Study: 500-Meter Subterranean Borehole Impulse Resonance (30s)
    print("[STUDY-007] Synthesizing Borehole Acoustic Echo Suite...")
    sr = 48000
    duration = 30.0
    dt = 1.0 / sr
    num_samples = int(sr * duration)
    
    # Speed of sound in air inside borehole: 343 m/s
    # Round-trip delay to -500m bottom: 2 * 500 / 343 = 2.915 seconds
    delay_samples = int(2.9154 * sr)
    
    # Echo impulse buffer of full audio duration
    impulse_buffer = [0.0] * (num_samples + 1000)
    
    left_audio = []
    right_audio = []
    
    # Fire initial seismic/acoustic strike at t = 0.5s
    strike_idx = int(0.5 * sr)
    for k in range(int(0.015 * sr)):
        t_imp = k * dt
        # Sharp compressed crackle of rock fracture
        val = math.sin(2.0 * math.pi * 180.0 * t_imp) * math.exp(-t_imp / 0.003)
        if strike_idx + k < len(impulse_buffer):
            impulse_buffer[strike_idx + k] += val * 0.9
            
    # Sub-bass borehole modal standing wave frequencies: f_n = (2n-1) * c / (4 * L)
    # Fundamental: 343 / (4 * 500) = 0.1715 Hz (infrasonic)
    # Audible harmonics: 343 / (2 * 500) = 0.343 Hz multiples
    # Lithic wall resonances: 82 Hz, 144 Hz, 288 Hz
    
    phi_sub = 0.0
    phi_lithic = 0.0
    
    for i in range(num_samples):
        t = i * dt
        phi_sub += 2.0 * math.pi * 32.5 * dt # Subterranean infrasound rumble
        phi_lithic += 2.0 * math.pi * 88.2 * dt
        
        # Fetch acoustic echoes with low-pass absorption damping from rough rock walls
        sig = 0.0
        # Direct pulse
        if i < len(impulse_buffer):
            sig += impulse_buffer[i]
            
        # Echo 1 (t = 2.915s): reflection from bottom basalt at -500m
        if i >= delay_samples:
            sig += 0.55 * impulse_buffer[i - delay_samples]
            
        # Echo 2 (t = 5.83s): round-trip second bounce
        if i >= delay_samples * 2:
            sig += 0.30 * impulse_buffer[i - delay_samples * 2]
            
        # Echo 3 (t = 8.74s): third bounce
        if i >= delay_samples * 3:
            sig += 0.15 * impulse_buffer[i - delay_samples * 3]
            
        # Add deep lithospheric cavernous air resonance
        air_resonance = 0.06 * math.sin(phi_sub) * (1.0 + 0.4 * math.sin(0.12 * t))
        lithic_hum = 0.04 * math.sin(phi_lithic) * math.exp(-t / 18.0)
        
        # High-frequency laser data pulse chatter in the optical fiber
        fiber_pulse = 0.0
        if random.random() < 0.0003:
            fiber_pulse = random.uniform(-0.1, 0.1)
            
        out_l = (sig * 0.75 + air_resonance + lithic_hum + fiber_pulse * 0.3)
        out_r = (sig * 0.75 + air_resonance + lithic_hum - fiber_pulse * 0.3)
        
        # Fade out
        if t > 26.0:
            env = max(0.0, (30.0 - t) / 4.0)
            out_l *= env
            out_r *= env
            
        left_audio.append(out_l * 0.8)
        right_audio.append(out_r * 0.8)
        
    wav_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_007_borehole_resonance.wav"))
    write_wav(wav_path, left_audio, right_audio, sample_rate=sr)
    print(f"[STUDY-007] Acoustic study written to: {wav_path}")

if __name__ == "__main__":
    run_study_007()
