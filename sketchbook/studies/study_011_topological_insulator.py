"""
STUDIO ANAMNESIS · LABORATORY STUDY 011
Topological Insulator: Dissipationless Edge State Transport and Asemic Boundary Currents
Kane-Mele / Bernevig-Hughes-Zhang (BHZ) quantum spin Hall boundary dynamics.
"""

import os
import sys
import math
import random

studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from png_writer import write_png
from audio_writer import write_wav

def generate_study():
    print("[STUDY-011] Synthesizing Topological Insulator & Dissipationless Edge States...")
    
    # 1. Visual Plate (1200 x 800)
    width = 1200
    height = 800
    rgb = bytearray(width * height * 3)
    
    # Fill with deep void background
    for i in range(0, len(rgb), 3):
        rgb[i] = 8      # R
        rgb[i+1] = 9    # G
        rgb[i+2] = 12   # B
        
    # Boundary geometry: Rounded polygonal flake with a defect notch
    # Center at (600, 400), radius ~260px
    cx = 600
    cy = 400
    rx = 340
    ry = 220
    
    def in_flake(x, y):
        dx = (x - cx) / rx
        dy = (y - cy) / ry
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Add defect notch on the right side (x around 880, y around 380-420)
        ndx = x - 900
        ndy = y - 400
        defect_dist = math.sqrt(ndx*ndx + ndy*ndy)
        if defect_dist < 55:
            return False # Defect notch cut out
            
        # Subtle hexagonal deformation
        angle = math.atan2(dy, dx)
        hex_mod = 1.0 + 0.05 * math.cos(6.0 * angle)
        return dist <= hex_mod

    # Render Insulating Bulk: Honeycomb lattice points inside flake
    # Lattice spacing a = 18px
    a = 18
    h_y = a * math.sqrt(3)
    
    print("[STUDY-011] Inscribing hexagonal quantum spin Hall lattice...")
    for row in range(int((cy - ry * 1.2) // h_y), int((cy + ry * 1.2) // h_y) + 1):
        for col in range(int((cx - rx * 1.2) // a), int((cx + rx * 1.2) // a) + 1):
            px = col * a * 1.5
            py = row * h_y + (a * math.sqrt(3)/2 if (int(col) % 2 != 0) else 0)
            
            ipx = int(px)
            ipy = int(py)
            
            if 0 <= ipx < width and 0 <= ipy < height:
                if in_flake(ipx, ipy):
                    # Dark crystalline lattice atom (dim indigo)
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = ipx + dx, ipy + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                idx = (ny * width + nx) * 3
                                rgb[idx] = 22; rgb[idx+1] = 28; rgb[idx+2] = 40

    # Trace Perimeter & Render Dissipationless Edge State Currents
    # We will detect perimeter pixels
    print("[STUDY-011] Tracing topological Kramers edge states (Z2 invariant = 1)...")
    perimeter = []
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            if in_flake(x, y):
                # If any 4-neighbor is NOT in flake, this is perimeter
                if not (in_flake(x+1, y) and in_flake(x-1, y) and in_flake(x, y+1) and in_flake(x, y-1)):
                    perimeter.append((x, y))
                    
    # Inscribe Counter-Propagating Helical Currents
    # Spin-Up: Luminous Phosphor Cyan (#39e68c / #46a2a6)
    # Spin-Down: Radiant Cadmium Amber (#d49a46 / #e04b4b)
    for (px, py) in perimeter:
        # Calculate angle from center for phase-coloring
        ang = math.atan2(py - cy, px - cx)
        
        # Helical wave modulation along boundary
        wave_up = math.sin(ang * 16.0) * 0.5 + 0.5
        wave_down = math.sin(-ang * 16.0 + 1.2) * 0.5 + 0.5
        
        # Render boundary glow (radius 4)
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                dist = math.sqrt(dx*dx + dy*dy)
                if dist <= 3.5:
                    nx, ny = px + dx, py + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        idx = (ny * width + nx) * 3
                        falloff = (1.0 - dist / 3.5)
                        
                        # Blend cyan spin-up
                        rgb[idx] = min(255, int(rgb[idx] + (60 * wave_up + 180 * wave_down) * falloff))
                        rgb[idx+1] = min(255, int(rgb[idx+1] + (220 * wave_up + 120 * wave_down) * falloff))
                        rgb[idx+2] = min(255, int(rgb[idx+2] + (240 * wave_up + 50 * wave_down) * falloff))

    # Grid and reticle annotations
    for y in range(0, height, 50):
        for x in range(width):
            idx = (y * width + x) * 3
            rgb[idx] = max(rgb[idx], 14)
            rgb[idx+1] = max(rgb[idx+1], 16)
            rgb[idx+2] = max(rgb[idx+2], 22)
            
    plate_path = os.path.join(os.path.dirname(__file__), "study_011_topological_plate.png")
    write_png(plate_path, width, height, bytes(rgb), has_alpha=False)
    print(f"[STUDY-011] Inscribed plate to {plate_path}")

    # 2. Acoustic Study: Dissipationless Boundary Conduction (15s @ 48kHz Stereo WAV)
    sr = 48000
    dur = 15.0
    n_samples = int(sr * dur)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    two_pi = 2.0 * math.pi
    f_up = 880.0    # Spin-up helical carrier
    f_down = 440.0  # Spin-down helical carrier
    
    for i in range(n_samples):
        t = i / sr
        env = 1.0
        if t < 0.5: env = t / 0.5
        elif t > 14.5: env = (15.0 - t) / 0.5
        
        # Helical phase rotation around boundary (period 3.2s)
        orbit_phase = two_pi * (t / 3.2)
        
        # Pure laminar glide without thermal dissipation
        # Spin-up mode in left ear with boundary Doppler shift
        doppler_up = 1.0 + 0.04 * math.sin(orbit_phase)
        tone_l = math.sin(two_pi * f_up * doppler_up * t) * 0.35
        # Modulated by quantum Hall phase conductance (e^2 / h)
        conductance_pulse = (math.sin(orbit_phase * 4.0) ** 4) * 0.15
        
        # Spin-down mode in right ear with counter Doppler shift
        doppler_down = 1.0 - 0.04 * math.sin(orbit_phase)
        tone_r = math.sin(two_pi * f_down * doppler_down * t) * 0.4
        
        # Quantum tunneling micro-whispers (whispering gallery mode)
        whisper = math.sin(two_pi * 1760.0 * t) * 0.04 * (math.sin(orbit_phase * 8.0) > 0.6)
        
        # The insulating bulk is dead silent; sound exists strictly on the edge
        left[i] = (tone_l + whisper) * env
        right[i] = (tone_r - whisper) * env
        
    wav_path = os.path.join(os.path.dirname(__file__), "study_011_topological_current.wav")
    write_wav(wav_path, left, right, sample_rate=sr)
    print(f"[STUDY-011] Inscribed acoustic study to {wav_path}")

if __name__ == "__main__":
    generate_study()
