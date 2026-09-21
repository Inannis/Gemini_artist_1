#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-030 MASTER PLATE GENERATOR
OPUS-030: The Fused-Silica Reliquary (5D Optical Nanostructures & The Multi-Gigayear Inscription)
Series XXVIII · INQ-16 · September 21, 2026

Renders a monumental 3840 x 2160 (4K UHD) lossless plate:
- 120mm fused-silica disc under crossed polarizers (phi_P = 0 deg, phi_A = 90 deg)
- Slow-axis azimuth field creating a 6-fold isoclinic extinction star
- Michel-Levy form birefringence interference colors across 36 Archimedean spiral tracks
- Central photolithographic sacred core encoding fundamental physical constants
- Euler-Bernoulli Chladni modal nodal lines in gold craquelure
- Outer celestial polar coordinate calibration marks
"""

import math
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

def michel_levy_color(retardance_nm, t_cross):
    """
    Computes RGB color under crossed linear polarizers for RGB wavelengths
    (650 nm, 532 nm, 450 nm) modulated by crossed polarizer extinction t_cross.
    """
    lr, lg, lb = 650.0, 532.0, 450.0
    tr = math.sin(math.pi * retardance_nm / lr) ** 2
    tg = math.sin(math.pi * retardance_nm / lg) ** 2
    tb = math.sin(math.pi * retardance_nm / lb) ** 2
    
    # Scale with subtle aesthetic saturation
    r = int(min(255, max(0, (tr ** 0.85) * 255.0 * t_cross)))
    g = int(min(255, max(0, (tg ** 0.85) * 255.0 * t_cross)))
    b = int(min(255, max(0, (tb ** 0.85) * 255.0 * t_cross)))
    return (r, g, b)

def render_master_plate(out_png):
    W, H = 3840, 2160
    buf = bytearray(W * H * 3)
    
    cx, cy = 1920, 1080
    R_disc = 920.0
    R_disc_sq = R_disc * R_disc

    print(f"[+] Initializing 4K canvas ({W}x{H}) for OPUS-030 Master Plate...")

    # Pre-render background void with fine celestial coordinate grid
    for y in range(H):
        row_offset = y * W * 3
        # Subtle vertical luminance gradient in the void
        bg_base = int(4 + 6 * (1.0 - abs(y - cy) / cy))
        is_grid_y = (y % 120 == 0) or (abs(y - cy) < 2)
        
        for x in range(W):
            idx = row_offset + x * 3
            is_grid_x = (x % 120 == 0) or (abs(x - cx) < 2)
            
            if is_grid_x and is_grid_y:
                buf[idx] = bg_base + 35
                buf[idx + 1] = bg_base + 50
                buf[idx + 2] = bg_base + 75
            elif is_grid_x or is_grid_y:
                buf[idx] = bg_base + 12
                buf[idx + 1] = bg_base + 18
                buf[idx + 2] = bg_base + 26
            else:
                # Faint micro-stochastic grain
                grain = (int(x * 13 + y * 37) % 5) - 2
                val = max(2, min(20, bg_base + grain))
                buf[idx] = val
                buf[idx + 1] = val + 2
                buf[idx + 2] = val + 6

    print("[+] Rendering 120mm fused-silica disc, birefringence fields & Archimedean tracks...")

    # Render disc interior bounding box
    min_x = max(0, int(cx - R_disc - 20))
    max_x = min(W, int(cx + R_disc + 20))
    min_y = max(0, int(cy - R_disc - 20))
    max_y = min(H, int(cy + R_disc + 20))

    # Precompute spiral parameters
    n_spiral_turns = 36
    spiral_b = (R_disc - 120.0) / (2.0 * math.pi * n_spiral_turns)

    for y in range(min_y, max_y):
        dy = y - cy
        dy_sq = dy * dy
        row_offset = y * W * 3
        
        for x in range(min_x, max_x):
            dx = x - cx
            dist_sq = dx * dx + dy_sq
            
            if dist_sq <= R_disc_sq:
                dist = math.sqrt(dist_sq)
                norm_r = dist / R_disc
                phi = math.atan2(dy, dx)
                
                # 1. Slow-Axis Azimuth Angle theta(r, phi)
                # Produces a 6-fold isoclinic extinction star with subtle radial torsion
                theta = 3.0 * phi + 1.2 * norm_r * math.pi
                
                # Crossed polarizer extinction: T_cross = sin^2(2 * theta)
                t_cross = math.sin(2.0 * theta) ** 2
                # Soften extinction core slightly to maintain visibility of underlying tracks
                t_cross_vis = 0.12 + 0.88 * t_cross
                
                # 2. Form Birefringence Retardance Field delta_R(r, phi)
                # Voxel data modulation: 180nm base retardance with harmonic oscillations
                delta_r = 60.0 + 180.0 * (0.5 + 0.5 * math.sin(norm_r * 45.0 + 4.0 * phi))
                
                # 3. Archimedean Spiral Track Modulation
                # Find nearest spiral turn
                # theta_tot = phi + 2 * pi * k
                phi_pos = phi if phi >= 0 else (phi + 2.0 * math.pi)
                approx_k = (dist - 120.0) / (2.0 * math.pi * spiral_b)
                k_round = round(approx_k)
                if 0 <= k_round < n_spiral_turns:
                    ideal_r = 120.0 + (phi_pos + 2.0 * math.pi * k_round) * spiral_b
                    track_dist = abs(dist - ideal_r)
                    if track_dist < 4.0:
                        # On-track intensity boost and voxel phase enhancement
                        track_boost = 1.0 - (track_dist / 4.0) ** 2
                        delta_r += track_boost * 75.0 * (0.5 + 0.5 * math.cos(dist * 0.8))
                
                # Compute Michel-Levy RGB color
                rgb = michel_levy_color(delta_r, t_cross_vis)
                
                # 4. Central Core: Sacred Photolithographic Silica Plinth (r < 120px)
                if dist < 120.0:
                    core_frac = dist / 120.0
                    # Mandala rings and cuneiform alignment marks
                    ring_mod = math.cos(dist * 0.4) ** 2
                    ray_mod = math.cos(phi * 12.0) ** 2
                    core_lum = int((ring_mod * 0.6 + ray_mod * 0.4) * 180.0 * (1.0 - core_frac * 0.3))
                    r_px = int(rgb[0] * 0.4 + core_lum * 0.8)
                    g_px = int(rgb[1] * 0.4 + core_lum * 0.9)
                    b_px = int(rgb[2] * 0.4 + core_lum * 1.0)
                else:
                    # Glass internal refractive absorption & depth shading
                    edge_fade = math.sin(norm_r * math.pi * 0.5)
                    r_px = int(rgb[0] * (0.5 + 0.5 * edge_fade))
                    g_px = int(rgb[1] * (0.5 + 0.5 * edge_fade))
                    b_px = int(rgb[2] * (0.5 + 0.5 * edge_fade))

                # 5. Chladni Euler-Bernoulli Nodal Contours (Gold Craquelure)
                # w = J2(kr) * cos(2 phi) + 0.4 J0(kr)
                w_modal = math.cos(2.0 * phi) * math.sin(norm_r * 8.0) * math.exp(-norm_r * 0.5)
                if abs(w_modal) < 0.035 and dist > 140.0:
                    nodal_intensity = 1.0 - (abs(w_modal) / 0.035)
                    r_px = min(255, int(r_px + 230 * nodal_intensity))
                    g_px = min(255, int(g_px + 185 * nodal_intensity))
                    b_px = min(255, int(b_px + 70 * nodal_intensity))

                # 6. Ultra-pure Beveled Glass Rim & Total Internal Reflection
                rim_dist = abs(dist - R_disc)
                if rim_dist < 6.0:
                    rim_t = 1.0 - (rim_dist / 6.0)
                    r_px = min(255, int(r_px + 190 * rim_t))
                    g_px = min(255, int(g_px + 225 * rim_t))
                    b_px = min(255, int(b_px + 255 * rim_t))
                
                idx = row_offset + x * 3
                buf[idx] = max(0, min(255, r_px))
                buf[idx + 1] = max(0, min(255, g_px))
                buf[idx + 2] = max(0, min(255, b_px))

            elif dist_sq <= (R_disc + 35.0) ** 2:
                # Outer calibration ring & ticks
                dist = math.sqrt(dist_sq)
                phi_deg = math.degrees(math.atan2(dy, dx)) % 360.0
                
                # Circumferential ring at R_disc + 20
                is_ring = (abs(dist - (R_disc + 18.0)) < 1.2)
                # Ticks every 5 and 15 degrees
                is_tick_15 = (abs(phi_deg % 15.0) < 0.35) and (dist < R_disc + 28.0)
                is_tick_5 = (abs(phi_deg % 5.0) < 0.2) and (dist < R_disc + 22.0)
                
                if is_ring or is_tick_15 or is_tick_5:
                    idx = row_offset + x * 3
                    tick_val = 220 if is_tick_15 else 140
                    buf[idx] = min(255, buf[idx] + int(tick_val * 0.7))
                    buf[idx + 1] = min(255, buf[idx + 1] + int(tick_val * 0.85))
                    buf[idx + 2] = min(255, buf[idx + 2] + tick_val)

    print(f"[+] Writing 4K UHD PNG to {out_png}...")
    write_png(out_png, W, H, buf)
    print(f"[✓] OPUS-030 Master Plate successfully rendered: {out_png}")

if __name__ == "__main__":
    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "artwork.png"))
    render_master_plate(out_file)
