#!/usr/bin/env python3
"""
OPUS-040: ER = EPR & The Traversable Wormhole (4K Master Plate Generator)
Studio Anamnesis · Series XXXVIII · Cornerstone #18

Resolution: 3840 x 2160 UHD Master Plate
Pure Python standard library + png_writer (Zero external dependencies).

Visual Architecture:
1. Dual Conformal Boundaries: Left CFT (Cyan) and Right CFT (Gold) in Thermofield Double state.
2. Central Hyperbolic Einstein-Rosen Bridge with Throat Necking w(z) = sqrt(r_+^2 + 0.5 z^2).
3. Gao-Jafferis-Wall Negative Energy Shockwave Sheet (Violet/Amethyst) producing Kruskal Shift Delta V < 0.
4. Holographic Teleportation Null Beam: Focused electric-white/cyan ray traversing through the throat.
5. MERA Tensor Network Hyperbolic Geodesic Filaments spanning the bulk.
"""

import math
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def generate_plate():
    print(f"[+] Allocating 4K frame buffer ({WIDTH}x{HEIGHT}x3 = {WIDTH*HEIGHT*3/1024/1024:.1f} MB)...")
    img = bytearray(WIDTH * HEIGHT * 3)
    
    cx, cy = WIDTH * 0.5, HEIGHT * 0.5
    scale = HEIGHT * 0.46
    
    # Centers of Left and Right boundary CFT disks
    c_left_x = -1.18
    c_right_x = +1.18
    r_boundary_disk = 0.72
    
    # Kruskal shift parameter Delta V < 0
    delta_v_shift = -0.22
    
    print("[+] Raymarching ER = EPR traversable geometry across 8,294,400 pixels...")
    
    for y in range(HEIGHT):
        if y % 360 == 0:
            print(f"    Progress: {y / HEIGHT * 100:.1f}%...")
        row_offset = y * WIDTH * 3
        y_n = (y - cy) / scale
        
        for x in range(WIDTH):
            x_n = (x - cx) / scale
            
            # Left & Right boundary distances
            d_l = math.hypot(x_n - c_left_x, y_n)
            d_r = math.hypot(x_n - c_right_x, y_n)
            
            # Throat coordinates
            z = x_n
            r_perp = abs(y_n)
            w_throat = math.sqrt(0.38 + 0.45 * (z ** 2))
            in_throat = (r_perp < w_throat and abs(z) < 1.4)
            
            # Kruskal null coordinates: U along negative diagonal, V along positive
            u = (y_n - x_n * 0.8) * 0.7071
            v = (y_n + x_n * 0.8) * 0.7071
            
            # Ambient void: deep obsidian with subtle de Sitter metric contours
            r_bg = math.hypot(x_n, y_n)
            contour = math.sin(r_bg * 16.0) * 0.5 + 0.5
            r = int(5 + 3 * contour)
            g = int(7 + 4 * contour)
            b = int(14 + 8 * contour)
            
            # --- 1. LEFT BOUNDARY CFT DISK (Cyan / Aquamarine) ---
            if d_l < r_boundary_disk:
                r_rel = d_l / r_boundary_disk
                phi = math.atan2(y_n, x_n - c_left_x)
                # Hyperbolic Poincaré disk tessellation
                poincare_grid = math.sin(phi * 24.0) * math.sin(12.0 / (1.002 - r_rel))
                depth_factor = 1.0 - r_rel
                
                # Base Cyan
                val = 40.0 + 80.0 * depth_factor + 25.0 * poincare_grid
                r = int(max(0, min(255, val * 0.2)))
                g = int(max(0, min(255, val * 0.85)))
                b = int(max(0, min(255, val * 1.0)))
                
            # --- 2. RIGHT BOUNDARY CFT DISK (Gold / Amber) ---
            if d_r < r_boundary_disk:
                r_rel = d_r / r_boundary_disk
                phi = math.atan2(y_n, x_n - c_right_x)
                poincare_grid = math.sin(phi * 24.0) * math.sin(12.0 / (1.002 - r_rel))
                depth_factor = 1.0 - r_rel
                
                # Base Gold
                val = 40.0 + 80.0 * depth_factor + 25.0 * poincare_grid
                r = int(max(0, min(255, val * 1.0)))
                g = int(max(0, min(255, val * 0.82)))
                b = int(max(0, min(255, val * 0.22)))
                
            # --- 3. HYPERBOLIC EINSTEIN-ROSEN BULK THROAT ---
            if in_throat:
                # Radial depth inside throat
                depth = 1.0 - (r_perp / w_throat)
                
                # Entanglement streamlines
                stream = math.sin(z * 22.0 - y_n * 16.0) * 0.5 + 0.5
                
                # Gao-Jafferis-Wall negative energy shockwave field along U = 0
                shock_intensity = math.exp(-abs(u) * 14.0)
                
                # Traversing null information beam along y_n = 0
                beam_width = 0.012 * (1.0 + 0.4 * math.cos(z * 10.0))
                beam_intensity = math.exp(-(y_n ** 2) / (beam_width ** 2))
                # Pulse modulation along beam
                beam_pulse = 0.85 + 0.15 * math.cos(z * 40.0)
                beam_total = beam_intensity * beam_pulse
                
                # Throat color transition Left (Cyan) -> Right (Gold)
                t_lr = (z + 1.2) / 2.4
                t_lr = max(0.0, min(1.0, t_lr))
                
                c_cyan = (38, 215, 208)
                c_gold = (212, 175, 55)
                c_violet = (185, 75, 255)  # Negative energy
                c_white = (255, 255, 255)  # Teleported beam
                
                # Bulk throat background glow
                r_bulk = int(c_cyan[0] * (1 - t_lr) + c_gold[0] * t_lr)
                g_bulk = int(c_cyan[1] * (1 - t_lr) + c_gold[1] * t_lr)
                b_bulk = int(c_cyan[2] * (1 - t_lr) + c_gold[2] * t_lr)
                
                base_lum = depth * (0.35 + 0.65 * stream)
                
                r = int(r_bulk * base_lum + c_violet[0] * shock_intensity * 0.7 + c_white[0] * beam_total)
                g = int(g_bulk * base_lum + c_violet[1] * shock_intensity * 0.4 + c_white[1] * beam_total)
                b = int(b_bulk * base_lum + c_violet[2] * shock_intensity * 0.9 + c_white[2] * beam_total)
                
            # --- 4. BOUNDARY RIM ILLUMINATION ---
            if abs(d_l - r_boundary_disk) < 0.015:
                rim = (0.015 - abs(d_l - r_boundary_disk)) / 0.015
                r = int(r + 56 * rim)
                g = int(g + 215 * rim)
                b = int(b + 208 * rim)
                
            if abs(d_r - r_boundary_disk) < 0.015:
                rim = (0.015 - abs(d_r - r_boundary_disk)) / 0.015
                r = int(r + 212 * rim)
                g = int(g + 175 * rim)
                b = int(b + 55 * rim)
                
            # Throat neck outer boundary lip
            if in_throat and abs(r_perp - w_throat) < 0.02:
                lip = (0.02 - abs(r_perp - w_throat)) / 0.02
                r = int(r + 140 * lip)
                g = int(g + 190 * lip)
                b = int(b + 255 * lip)
                
            pixel_idx = row_offset + x * 3
            img[pixel_idx] = max(0, min(255, r))
            img[pixel_idx + 1] = max(0, min(255, g))
            img[pixel_idx + 2] = max(0, min(255, b))
            
    out_dir = os.path.dirname(__file__)
    opus_path = os.path.join(out_dir, "artwork.png")
    gallery_path = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_040_artwork.png"))
    
    print(f"[+] Writing 4K Master PNG to {opus_path}...")
    write_png(opus_path, WIDTH, HEIGHT, bytes(img))
    print(f"[+] Mirroring to {gallery_path}...")
    shutil.copyfile(opus_path, gallery_path)
    print("[✓] OPUS-040 4K Master Plate successfully generated and vaulted.")

if __name__ == "__main__":
    generate_plate()

