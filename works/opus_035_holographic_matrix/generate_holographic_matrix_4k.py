#!/usr/bin/env python3
"""
OPUS-035: THE HOLOGRAPHIC MATRIX & BULK-BOUNDARY DUALITIES
Series XXXIII · Cornerstone #13 · Master Artwork Generator (4K UHD)
Resolution: 3840 × 2160 px
Zero external dependencies (pure Python standard library).
"""

import math
import os
import shutil
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_master_plate():
    print(f"[OPUS-035] Initializing 4K UHD Master Canvas ({WIDTH}x{HEIGHT})...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    disk_radius = 980.0
    
    # Precompute boundary CFT modes
    num_cft_modes = 16
    cft_phases = [math.sin(i * 1.618) for i in range(num_cft_modes)]
    cft_amps = [1.0 / (1.0 + i * 0.4) for i in range(num_cft_modes)]
    
    # Precompute Ryu-Takayanagi geodesic minimal surfaces
    # We generate a structured foliation of 96 boundary intervals
    geodesics = []
    num_intervals = 64
    for i in range(num_intervals):
        th1 = 2.0 * math.pi * i / num_intervals
        for span_step in [3, 7, 12, 18, 26]:
            th2 = 2.0 * math.pi * ((i + span_step) % num_intervals) / num_intervals
            d_th = abs(th2 - th1)
            if d_th > math.pi:
                d_th = 2.0 * math.pi - d_th
            if d_th < 0.04 or abs(d_th - math.pi) < 0.04:
                continue
            
            cos_half = math.cos(d_th / 2.0)
            if abs(cos_half) < 1e-4:
                continue
                
            th_mid = (th1 + th2) / 2.0
            if abs(th2 - th1) > math.pi:
                th_mid += math.pi
                
            d_center = 1.0 / cos_half
            r_arc = math.tan(d_th / 2.0)
            
            arc_cx = cx + d_center * disk_radius * math.cos(th_mid)
            arc_cy = cy + d_center * disk_radius * math.sin(th_mid)
            arc_r_px = r_arc * disk_radius
            r_min = math.tan((math.pi - d_th) / 4.0)
            
            geodesics.append((arc_cx, arc_cy, arc_r_px, r_min, d_th))
            
    print(f"[OPUS-035] Precomputed {len(geodesics)} Ryu-Takayanagi geodesic minimal surfaces.")
    
    # Scanline render
    for y in range(HEIGHT):
        if y % 360 == 0:
            print(f"[OPUS-035] Rendering line {y}/{HEIGHT} ({y*100//HEIGHT}%)...")
        dy = y - cy
        dy_sq = dy * dy
        
        for x in range(WIDTH):
            dx = x - cx
            dist_sq = dx * dx + dy_sq
            dist = math.sqrt(dist_sq)
            idx = (y * WIDTH + x) * 3
            
            # Exterior cosmic void
            if dist > disk_radius + 18.0:
                ang = math.atan2(dy, dx)
                ext_dist = dist - disk_radius
                # Holographic boundary interference fringes
                fringes = 0.5 + 0.5 * math.sin(ang * 32.0 + ext_dist * 0.08)
                falloff = math.exp(-ext_dist / 320.0)
                buf[idx] = int(3 + 8 * fringes * falloff)
                buf[idx + 1] = int(4 + 10 * fringes * falloff)
                buf[idx + 2] = int(8 + 22 * fringes * falloff)
                continue
                
            # Conformal boundary circle (|w| = 1)
            elif dist > disk_radius - 4.5:
                ang = math.atan2(dy, dx)
                # Compute CFT stress-energy tensor fluctuation
                t_cft = 0.0
                for m in range(num_cft_modes):
                    t_cft += cft_amps[m] * math.cos((m + 1) * ang + cft_phases[m])
                t_norm = max(0.0, min(1.0, 0.5 + 0.25 * t_cft))
                
                buf[idx] = int(190 + 65 * t_norm)
                buf[idx + 1] = int(225 + 30 * t_norm)
                buf[idx + 2] = 255
                continue
                
            norm_r = dist / disk_radius
            ang = math.atan2(dy, dx)
            
            # Hyperbolic depth z = (1 - norm_r) / (1 + norm_r)
            depth_ir = 1.0 - norm_r
            
            # Base bulk interior: deep indigo well with negative curvature glow
            r_val = int(5 + 26 * depth_ir + 18 * (depth_ir ** 2) + 12 * math.sin(norm_r * 10.0) ** 2)
            g_val = int(7 + 22 * depth_ir + 15 * norm_r + 8 * math.cos(ang * 6.0) * depth_ir)
            b_val = int(18 + 72 * depth_ir + 50 * norm_r)
            
            # Hyperbolic distance shells: r_hyp = 2 atanh(r)
            hyp_r = 2.0 * math.atanh(min(0.996, norm_r))
            hyp_shell = math.sin(hyp_r * 4.5)
            if abs(hyp_shell) > 0.94:
                r_val = min(255, r_val + 18)
                g_val = min(255, g_val + 24)
                b_val = min(255, b_val + 40)
                
            # MERA Tensor Network hierarchical discretization rays
            level = int(hyp_r * 1.8)
            num_spokes = 12 * (2 ** min(4, level))
            spoke_angle = 2.0 * math.pi / num_spokes
            delta_ang = abs((ang % spoke_angle) - spoke_angle * 0.5)
            if delta_ang < 0.012:
                intense = (0.012 - delta_ang) / 0.012
                r_val = min(255, r_val + int(22 * intense))
                g_val = min(255, g_val + int(36 * intense))
                b_val = min(255, b_val + int(60 * intense))
                
            # Geodesic minimal surfaces
            for arc_cx, arc_cy, arc_r_px, r_min, d_th in geodesics:
                # Fast bounding check
                d_center_dist = math.hypot(x - arc_cx, y - arc_cy)
                d_to_arc = abs(d_center_dist - arc_r_px)
                if d_to_arc < 2.2:
                    intensity = math.exp(-0.5 * (d_to_arc / 0.9) ** 2)
                    if r_min < 0.22:
                        # Deep minimal surfaces: incandescent golden-amber
                        r_val = int(min(255, r_val + 215 * intensity))
                        g_val = int(min(255, g_val + 170 * intensity))
                        b_val = int(min(255, b_val + 75 * intensity))
                    elif r_min < 0.52:
                        # Intermediate surfaces: emerald-cyan
                        r_val = int(min(255, r_val + 85 * intensity))
                        g_val = int(min(255, g_val + 205 * intensity))
                        b_val = int(min(255, b_val + 215 * intensity))
                    else:
                        # UV boundary-hugging: opalescent violet
                        r_val = int(min(255, r_val + 135 * intensity))
                        g_val = int(min(255, g_val + 95 * intensity))
                        b_val = int(min(255, b_val + 245 * intensity))
                        
            buf[idx] = min(255, max(0, r_val))
            buf[idx + 1] = min(255, max(0, g_val))
            buf[idx + 2] = min(255, max(0, b_val))
            
    out_dir = os.path.dirname(__file__)
    master_path = os.path.join(out_dir, "artwork.png")
    write_png(master_path, WIDTH, HEIGHT, buf)
    print(f"[OPUS-035] Successfully generated 4K Master Artwork: {master_path}")
    
    # Sync to gallery assets
    gallery_asset_path = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_035_artwork.png")
    shutil.copyfile(master_path, gallery_asset_path)
    print(f"[OPUS-035] Synced master plate to gallery asset: {gallery_asset_path}")

if __name__ == "__main__":
    render_master_plate()
