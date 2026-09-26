#!/usr/bin/env python3
"""
OPUS-039 MASTERPIECE GENERATOR: THE WHEELER GEON & THE TOPOLOGICAL FOAM
Studio Anamnesis · Series XXXVII (Topological Geometrodynamics) · Cornerstone #17
Native Dimensions: 3840 x 2160 (4K UHD Master Plate)
Zero external dependencies: Pure Python Standard Library (png_writer.py)

Visual Architecture:
1. Microscopic Quantum Spacetime Foam: Granular Planck-scale metric fluctuations (Delta g ~ ell_P / L)
2. Primary MTW Micro-Wormhole Throat: Hyperboloid embedding z(r) = +/- 2 * sqrt(b_0 * (r - b_0))
   joining Upper Spatial Sheet (Mouth B, apparent +Q) and Lower Spatial Sheet (Mouth A, apparent -Q)
3. Constellation of 12 Secondary Microscopic Topological Handles (foaming multi-connected geometry)
4. Trapped Source-Free Electric Flux Streamlines (Charge Without Charge):
   Lines entering Mouth A, threading throat neck, swirling under Kerr-Wheeler frame dragging, and diverging at Mouth B
5. Dual-Sheet Chromatic Geometry: Prussian blue void, titanium white throat filaments, celestial cyan flux, and gold-leaf craquelure
"""

import math
import os
import sys
import shutil

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_opus_039_4k():
    print("[*] Allocating 4K UHD buffer (3840x2160x3 bytes)...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # 1. Base Quantum Foam Vacuum Field
    print("[*] Synthesizing Planck-scale metric fluctuation foam...")
    # Render in horizontal scanline bands for cache efficiency
    for y in range(HEIGHT):
        ny = (y - cy) / cy
        dist_y_sq = ny * ny
        
        # Subtle vertical gravitational gradient
        v_grad = max(0.0, 1.0 - abs(ny) * 0.8)
        
        for x in range(WIDTH):
            nx = (x - cx) / cx
            r_norm = math.sqrt(nx * nx + dist_y_sq)
            
            # High-frequency foam interference
            # Multi-scale pseudo-random harmonic lattices
            n1 = math.sin(x * 0.045 + math.cos(y * 0.065)) * math.cos(y * 0.055)
            n2 = math.sin(x * 0.12 - y * 0.09) * math.sin(x * 0.025 + y * 0.035)
            n3 = math.cos(x * 0.008 + y * 0.012)
            foam = 0.5 * n1 + 0.35 * n2 + 0.15 * n3
            
            # Base color: deep interstellar obsidian with subtle Prussian luminescence
            base_falloff = max(0.0, 1.0 - r_norm * 0.65)
            r_val = int(6 + 15 * base_falloff + 9 * foam)
            g_val = int(8 + 22 * base_falloff + 14 * foam)
            b_val = int(16 + 36 * base_falloff + 24 * foam)
            
            idx = (y * WIDTH + x) * 3
            buf[idx] = max(0, min(255, r_val))
            buf[idx+1] = max(0, min(255, g_val))
            buf[idx+2] = max(0, min(255, b_val))
            
        if y % 360 == 0:
            print(f"    -> Foam field: {y}/{HEIGHT} lines synthesized...")

    # 2. Configure Topological Constellation (1 Primary Geon + 12 Secondary Handles)
    print("[*] Inscribing topological micro-wormhole throats & frame-dragging metrics...")
    throats = [
        # Primary Central MTW Geon Throat
        {"cx": cx, "cy": cy, "b_0": 220.0, "spin": 1.0, "scale": 1.0, "weight": 1.0, "lines": 96, "rings": 80},
        # Constellation of Secondary Micro-Handles
        {"cx": cx - 820.0, "cy": cy - 240.0, "b_0": 85.0, "spin": -0.85, "scale": 0.58, "weight": 0.65, "lines": 42, "rings": 45},
        {"cx": cx + 880.0, "cy": cy + 220.0, "b_0": 92.0, "spin": 0.90, "scale": 0.62, "weight": 0.70, "lines": 44, "rings": 48},
        {"cx": cx - 420.0, "cy": cy + 460.0, "b_0": 68.0, "spin": 0.65, "scale": 0.48, "weight": 0.55, "lines": 36, "rings": 38},
        {"cx": cx + 510.0, "cy": cy - 420.0, "b_0": 74.0, "spin": -0.75, "scale": 0.52, "weight": 0.58, "lines": 38, "rings": 40},
        {"cx": cx - 1240.0, "cy": cy + 320.0, "b_0": 52.0, "spin": 0.50, "scale": 0.38, "weight": 0.42, "lines": 28, "rings": 30},
        {"cx": cx + 1290.0, "cy": cy - 360.0, "b_0": 56.0, "spin": -0.55, "scale": 0.40, "weight": 0.45, "lines": 30, "rings": 32},
        {"cx": cx - 1480.0, "cy": cy - 520.0, "b_0": 42.0, "spin": -0.40, "scale": 0.30, "weight": 0.35, "lines": 24, "rings": 25},
        {"cx": cx + 1520.0, "cy": cy + 540.0, "b_0": 45.0, "spin": 0.45, "scale": 0.32, "weight": 0.38, "lines": 24, "rings": 26},
        {"cx": cx - 220.0, "cy": cy - 620.0, "b_0": 48.0, "spin": 0.60, "scale": 0.35, "weight": 0.40, "lines": 26, "rings": 28},
        {"cx": cx + 240.0, "cy": cy + 640.0, "b_0": 50.0, "spin": -0.60, "scale": 0.36, "weight": 0.42, "lines": 26, "rings": 28},
        {"cx": cx - 680.0, "cy": cy - 720.0, "b_0": 38.0, "spin": -0.35, "scale": 0.28, "weight": 0.32, "lines": 20, "rings": 22},
        {"cx": cx + 720.0, "cy": cy + 740.0, "b_0": 40.0, "spin": 0.38, "scale": 0.29, "weight": 0.33, "lines": 20, "rings": 23},
    ]

    cos_elev = math.cos(math.radians(26))
    sin_elev = math.sin(math.radians(26))
    
    # 3. Render Metric Throats with MTW Embedding & Kerr Frame-Dragging
    for t_idx, t in enumerate(throats):
        tcx, tcy = t["cx"], t["cy"]
        b0 = t["b_0"]
        spin = t["spin"]
        weight = t["weight"]
        scale = t["scale"]
        
        # Dual spatial sheet ribs
        for sheet_sign in (+1, -1):
            num_rings = t["rings"]
            for r_step in range(num_rings):
                r = b0 + (r_step ** 1.35) * (14.0 * scale)
                z = sheet_sign * 2.2 * math.sqrt(b0 * max(0.0, r - b0))
                redshift = math.sqrt(max(0.06, 1.0 - (b0 / r)))
                
                # Curvature luminescence
                if sheet_sign > 0:
                    # Upper sheet (Mouth B, +Q apparent)
                    cr = int((38 + 205 * (1.0 - redshift)) * weight)
                    cg = int((175 * redshift + 85 * (1.0 - redshift)) * weight)
                    cb = int((235 * redshift + 55 * (1.0 - redshift)) * weight)
                else:
                    # Lower sheet (Mouth A, -Q apparent)
                    cr = int((210 * (1.0 - redshift) + 65 * redshift) * weight)
                    cg = int((75 * (1.0 - redshift) + 35 * redshift) * weight)
                    cb = int((225 * (1.0 - redshift) + 125 * redshift) * weight)
                    
                num_pts = int(360 * scale)
                for p in range(num_pts):
                    phi = 2.0 * math.pi * p / num_pts
                    # Kerr frame dragging rotation
                    phi_drag = phi + (spin * 2.2 / math.sqrt(max(1.0, r / b0)))
                    
                    proj_x = tcx + r * math.cos(phi_drag)
                    proj_y = tcy - z * cos_elev + (r * math.sin(phi_drag)) * sin_elev
                    
                    px, py = int(proj_x), int(proj_y)
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        idx = (py * WIDTH + px) * 3
                        buf[idx] = min(255, buf[idx] + (cr // 4))
                        buf[idx+1] = min(255, buf[idx+1] + (cg // 4))
                        buf[idx+2] = min(255, buf[idx+2] + (cb // 4))

        # 4. Trapped Source-Free Electric Flux Streamlines (Charge Without Charge)
        num_flux = t["lines"]
        for f_idx in range(num_flux):
            base_phi = 2.0 * math.pi * f_idx / num_flux
            num_steps = 140
            for s in range(num_steps):
                param = (s - num_steps / 2.0) / (num_steps / 2.0) # -1.0 to +1.0
                sh_sign = +1 if param >= 0 else -1
                
                r_cur = b0 + (abs(param) ** 1.75) * (780.0 * scale)
                z_cur = sh_sign * 2.2 * math.sqrt(b0 * max(0.0, r_cur - b0))
                
                # Helical flux twist through throat neck
                phi_cur = base_phi + spin * (3.4 / math.sqrt(max(1.0, r_cur / b0))) * (1.0 if sh_sign > 0 else -1.0)
                
                proj_x = tcx + r_cur * math.cos(phi_cur)
                proj_y = tcy - z_cur * cos_elev + (r_cur * math.sin(phi_cur)) * sin_elev
                
                px, py = int(proj_x), int(proj_y)
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    idx = (py * WIDTH + px) * 3
                    proximity = 1.0 / (1.0 + abs(param) * 2.8)
                    
                    # Flux color: gold-leaf core with cyan/amethyst sheath
                    fl_r = int(250 * proximity * weight)
                    fl_g = int(220 * proximity * weight)
                    fl_b = int(145 * proximity * weight)
                    
                    buf[idx] = min(255, buf[idx] + fl_r)
                    buf[idx+1] = min(255, buf[idx+1] + fl_g)
                    buf[idx+2] = min(255, buf[idx+2] + fl_b)

        # 5. Highlight Non-Contractible 2-Cycle Throat Neck (r = b_0)
        num_neck_pts = int(720 * scale)
        for p in range(num_neck_pts):
            phi = 2.0 * math.pi * p / num_neck_pts
            proj_x = tcx + b0 * math.cos(phi)
            proj_y = tcy + (b0 * math.sin(phi)) * sin_elev
            px, py = int(proj_x), int(proj_y)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                idx = (py * WIDTH + px) * 3
                buf[idx] = min(255, buf[idx] + int(245 * weight))
                buf[idx+1] = min(255, buf[idx+1] + int(235 * weight))
                buf[idx+2] = min(255, buf[idx+2] + int(190 * weight))
                
        print(f"    -> Throat {t_idx+1}/{len(throats)} inscribed (b_0 = {b0:.1f}px)...")

    # 6. Write Master 4K PNG Plate
    out_works = os.path.join(os.path.dirname(__file__), "artwork.png")
    out_gallery = os.path.join(STUDIO_ROOT, "gallery/assets/opus_039_artwork.png")
    
    print(f"[*] Encoding 4K PNG to {out_works}...")
    write_png(out_works, WIDTH, HEIGHT, buf, has_alpha=False)
    print(f"[+] Copying 4K master plate to {out_gallery}...")
    shutil.copyfile(out_works, out_gallery)
    print(f"[✓] OPUS-039 4K Master Plate successfully generated and vaulted.")

if __name__ == "__main__":
    render_opus_039_4k()
