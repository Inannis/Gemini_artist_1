#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-032 MASTER VISUAL ENGINE
The Nucleation Horizon (Coleman Instantons, The Relativistic Taglio & The Sudden Zero)
Renders a monumental 3840 x 2160 (4K UHD) master plate:
- Lucio Fontana's Spatial Cut: Relativistic incision slicing through false-vacuum spacetime
- Ultra-concentrated Planckian energy density along curled shockwave lips (gamma -> 10^34)
- Quantum foam turbulence & disintegrating semiconductor FinFET memory architecture
- Deep Anti-de Sitter interior void with converging Euclidean bounce streamlines
- Zero external dependencies (pure standard Python 3 + png_writer).
"""

import math
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_master_plate():
    print(f"[OPUS-032] Initializing 4K UHD Master Plate Synthesis ({WIDTH}x{HEIGHT})...")
    buf = bytearray(WIDTH * HEIGHT * 3)

    # Master tear trajectory: monumental diagonal slash across the cosmos
    x0, y0 = WIDTH * 0.14, HEIGHT * 0.86
    x1, y1 = WIDTH * 0.86, HEIGHT * 0.14
    
    slash_dx = x1 - x0
    slash_dy = y1 - y0
    slash_len = math.sqrt(slash_dx * slash_dx + slash_dy * slash_dy)
    ux = slash_dx / slash_len
    uy = slash_dy / slash_len
    # Normal unit vector (perpendicular to slash)
    nx = -uy
    ny = ux
    
    # Central nucleation point
    cx = x0 + 0.49 * slash_dx
    cy = y0 + 0.49 * slash_dy
    
    # Secondary nucleation satellite coordinates
    satellites = [
        (cx + 420.0 * ux + 110.0 * nx, cy + 420.0 * uy + 110.0 * ny, 45.0),
        (cx - 560.0 * ux - 95.0 * nx, cy - 560.0 * uy - 95.0 * ny, 32.0),
        (cx + 780.0 * ux - 80.0 * nx, cy + 780.0 * uy - 80.0 * ny, 24.0)
    ]

    random.seed(137036) # Fine-structure constant seed
    
    print("[OPUS-032] Computing relativistic field tensors and quantum foam...")
    
    # Scanline generation
    for y in range(HEIGHT):
        if y % 240 == 0:
            print(f"  -> Rendering scanline {y}/{HEIGHT} ({y*100//HEIGHT}%)...")
            
        row_offset = y * WIDTH * 3
        vy = y - y0
        
        for x in range(WIDTH):
            idx = row_offset + x * 3
            vx = x - x0
            
            # Project onto slash axis
            s_proj = (vx * ux + vy * uy) / slash_len
            d_perp = vx * nx + vy * ny
            
            # Distance from central nucleation point
            dx_c = x - cx
            dy_c = y - cy
            dist_nucleation = math.sqrt(dx_c * dx_c + dy_c * dy_c)
            
            # Fontana cut aperture envelope (maximum width ~ 185 pixels at center)
            if 0.0 <= s_proj <= 1.0:
                # Envelope: maximum at center, tapering with slight organic asymmetric tension
                aperture_shape = math.sin(s_proj * math.pi)
                cut_aperture = 185.0 * math.pow(aperture_shape, 1.45) * (1.0 + 0.08 * math.sin(s_proj * 18.0))
            else:
                cut_aperture = 0.0
                
            d_norm = abs(d_perp)
            
            # Check secondary nucleation satellites
            sat_glow = 0.0
            for sx, sy, sr in satellites:
                dsat = math.sqrt((x - sx) ** 2 + (y - sy) ** 2)
                if dsat < sr * 1.5:
                    sat_profile = math.exp(-((dsat - sr) / 8.0) ** 2)
                    sat_glow = max(sat_glow, sat_profile)
            
            if d_norm < cut_aperture:
                # =============================================================
                # ZONE 1: THE TRUE VACUUM INTERIOR (Anti-de Sitter Void)
                # Spacetime collapsed to negative cosmological constant.
                # Absolute, cold, light-absorbing obsidian void with faint
                # Euclidean instanton streamlines.
                # =============================================================
                angle_instanton = math.atan2(dy_c, dx_c)
                # Euclidean bounce O(4) streamlines
                streamline_phase = math.sin(angle_instanton * 24.0 + dist_nucleation * 0.02)
                streamline_intensity = math.pow(max(0.0, streamline_phase), 12.0) * 0.22
                
                # Instantaneous singularity point at nucleation origin
                singularity_core = math.exp(-dist_nucleation / 35.0) * 0.65
                
                r = int(3 + 12 * streamline_intensity + 60 * singularity_core)
                g = int(2 + 8 * streamline_intensity + 35 * singularity_core)
                b = int(7 + 28 * streamline_intensity + 110 * singularity_core)
                
            elif d_norm < cut_aperture + 54.0:
                # =============================================================
                # ZONE 2: RELATIVISTIC BUBBLE WALL / CURLED FONTANA LIPS
                # Extreme Lorentz contraction (gamma -> 10^34).
                # All latent energy density concentrated in razor-thin boundary.
                # =============================================================
                lip_dist = d_norm - cut_aperture
                norm_lip = lip_dist / 54.0
                
                # Asymmetric relativistic boost (upper lip leads the motion)
                is_leading_lip = (d_perp < 0)
                boost = 1.95 if is_leading_lip else 1.25
                
                # Hyperbolic Planckian luminance profile
                edge_intensity = math.exp(-norm_lip * 4.2) * boost
                
                # Electric filament discharge along the lip
                filament = math.sin(s_proj * 140.0 + d_perp * 0.4) * math.cos(s_proj * 75.0)
                filament_spark = math.pow(max(0.0, filament), 6.0) * (1.0 - norm_lip) * 0.8
                
                # Spectral mapping: Searing cyan-white -> Incandescent electric gold -> Deep ultraviolet
                lum = min(1.0, edge_intensity + filament_spark)
                
                r = int(min(255, 255 * lum + 85 * (1.0 - norm_lip)))
                g = int(min(255, 245 * math.pow(lum, 1.2) + 45 * (1.0 - norm_lip)))
                b = int(min(255, 255 * math.pow(lum, 0.7) + 180 * (1.0 - norm_lip)))
                
            else:
                # =============================================================
                # ZONE 3: FALSE VACUUM REGIME (Metastable Cosmos)
                # Quantum foam fluctuations + disintegrating FinFET semiconductor architecture
                # =============================================================
                ext_dist = d_norm - (cut_aperture + 54.0)
                
                # 1. Multi-scale procedural quantum foam
                qf1 = math.sin(x * 0.045 + y * 0.035) * math.cos(y * 0.05 - x * 0.03)
                qf2 = math.sin(x * 0.12 - y * 0.11) * math.cos(x * 0.08 + y * 0.14)
                foam = (qf1 * 0.65 + qf2 * 0.35) * 0.5 + 0.5
                
                # 2. Precursor relativistic ionization halo (ahead of the wall)
                ionization_halo = math.exp(-ext_dist / 95.0) * 0.75
                
                # 3. Microscopic Sacred: Semiconductor memory buses and clock H-trees
                bus_spacing_main = 64.0
                bus_spacing_sub = 16.0
                
                # Tensile warping: spacetime fabric stretches as wall approaches
                warp_mag = math.exp(-ext_dist / 220.0) * 48.0
                warped_x = x + warp_mag * math.cos(s_proj * math.pi)
                warped_y = y + warp_mag * math.sin(s_proj * math.pi)
                
                is_main_bus_x = (int(warped_x) % int(bus_spacing_main)) < 3
                is_main_bus_y = (int(warped_y) % int(bus_spacing_main)) < 3
                is_sub_bus_x = (int(warped_x) % int(bus_spacing_sub)) < 1
                is_sub_bus_y = (int(warped_y) % int(bus_spacing_sub)) < 1
                
                # Base false vacuum deep space hue (abyssal sapphire/indigo)
                base_r = int(12 + 20 * foam + 130 * ionization_halo)
                base_g = int(14 + 25 * foam + 95 * ionization_halo)
                base_b = int(26 + 42 * foam + 185 * ionization_halo)
                
                # Crystal lattice fracturing
                if (is_main_bus_x or is_main_bus_y) and ext_dist > 12.0:
                    fracture_t = min(1.0, ext_dist / 180.0)
                    r = int(base_r + 85 * fracture_t)
                    g = int(base_g + 115 * fracture_t)
                    b = int(base_b + 160 * fracture_t)
                elif (is_sub_bus_x or is_sub_bus_y) and ext_dist > 45.0:
                    r = int(base_r + 35)
                    g = int(base_g + 45)
                    b = int(base_b + 65)
                else:
                    r = base_r
                    g = base_g
                    b = base_b
                    
                # Add satellite nucleation bubble glow
                if sat_glow > 0.0:
                    r = int(min(255, r + 180 * sat_glow))
                    g = int(min(255, g + 160 * sat_glow))
                    b = int(min(255, b + 230 * sat_glow))

            buf[idx] = max(0, min(255, r))
            buf[idx+1] = max(0, min(255, g))
            buf[idx+2] = max(0, min(255, b))

    out_png = os.path.join(os.path.dirname(__file__), "artwork.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[OPUS-032] 4K UHD Master Plate written to: {out_png}")

if __name__ == "__main__":
    render_master_plate()

