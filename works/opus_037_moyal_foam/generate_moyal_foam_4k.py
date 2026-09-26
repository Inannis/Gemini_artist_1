#!/usr/bin/env python3
"""
OPUS-037: The Moyal Reliquary & The Non-Commutative Foam
Cornerstone #15 · Series XXXV: Non-Commutative Spacetime & Spectral Triples
Zero-dependency 4K UHD Master Plate Generation (3840x2160).
Renders the multi-tier Fuzzy Sphere reliquary, non-commutative Moyal star-product
symplectic interference field, and UV/IR mixing duality.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "telemetry"))
from png_writer import write_png
from noncommutative_metric import NonCommutativeMetric

WIDTH = 3840
HEIGHT = 2160

def render_master_plate():
    print(f"[OPUS-037] Initializing 4K UHD canvas ({WIDTH}x{HEIGHT})...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    nc = NonCommutativeMetric(theta_planck_ratio=1.0, matrix_dim_n=32)
    
    print("[OPUS-037] Synthesizing non-commutative Moyal phase field background...")
    # 1. Background: Moyal Symplectic Phase Field & Paikian Lissajous Raster
    for y in range(HEIGHT):
        ny = (y - cy) / cy # [-1, 1]
        row_offset = y * WIDTH * 3
        for x in range(WIDTH):
            nx = (x - cx) / cy # Aspect ratio preserved
            r = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)
            
            # Non-commutative wave packet simulation:
            w1 = math.sin(10.0 * nx + 1.2 * math.sin(7.0 * ny))
            w2 = math.cos(10.0 * ny - 1.2 * math.cos(7.0 * nx))
            curl = w1 * w2
            
            # Radial attenuation
            vignette = max(0.0, 1.0 - 0.52 * r)
            
            # Paikian electromagnetic deflection fringe
            paik = math.sin(28.0 * r - 3.0 * angle + 2.0 * curl)
            lum = max(0.0, 0.040 * vignette + 0.016 * paik * vignette)
            
            idx = row_offset + x * 3
            buf[idx] = int(255.0 * max(0.0, min(1.0, lum * 0.40 + 0.008 * curl)))       # Deep midnight violet
            buf[idx + 1] = int(255.0 * max(0.0, min(1.0, lum * 0.62 + 0.014 * curl)))   # Luminous cyan edge
            buf[idx + 2] = int(255.0 * max(0.0, min(1.0, lum * 1.05 + 0.022 * curl)))   # Pure cobalt deep
            
    print("[OPUS-037] Computing 3-tier Fuzzy Sphere matrix coordinates (UV/IR Mixing)...")
    # 3-tier Nested Fuzzy Spheres:
    # 1. UV Shell: N=48 -> 2304 cells, R = 780 px (Microscopic Planck Foam)
    # 2. Middle Shell: N=32 -> 1024 cells, R = 500 px (Intermediate Geometry)
    # 3. IR Core: N=16 -> 256 cells, R = 240 px (Macroscopic Horizon Core)
    shells = [
        {"cells": 2304, "radius": 780.0, "yaw": 0.58,  "pitch": 0.35, "tier": "UV"},
        {"cells": 1024, "radius": 500.0, "yaw": -0.42, "pitch": 0.52, "tier": "MID"},
        {"cells": 256,  "radius": 240.0, "yaw": 0.85,  "pitch": -0.30, "tier": "IR"}
    ]
    
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    all_cells = []
    
    for sh in shells:
        n_pts = sh["cells"]
        rad_px = sh["radius"]
        tier = sh["tier"]
        theta_N = 2.0 / math.sqrt(n_pts - 1.0)
        
        cos_y, sin_y = math.cos(sh["yaw"]), math.sin(sh["yaw"])
        cos_p, sin_p = math.cos(sh["pitch"]), math.sin(sh["pitch"])
        
        for k in range(n_pts):
            z_k = 1.0 - (2.0 * k + 1.0) / float(n_pts)
            r_xy = math.sqrt(max(0.0, 1.0 - z_k * z_k))
            phi_k = k * golden_angle
            
            x_k = r_xy * math.cos(phi_k)
            y_k = r_xy * math.sin(phi_k)
            
            # Non-commutative matrix perturbation [X_i, X_j] = i*theta_N*eps_ijk*X_k
            dx = theta_N * 0.35 * math.sin(8.0 * phi_k) * z_k
            dy = theta_N * 0.35 * math.cos(8.0 * phi_k) * z_k
            dz = -theta_N * 0.35 * (x_k * math.sin(phi_k) + y_k * math.cos(phi_k))
            
            x_k += dx
            y_k += dy
            z_k += dz
            mag = math.sqrt(x_k * x_k + y_k * y_k + z_k * z_k)
            x_k /= mag
            y_k /= mag
            z_k /= mag
            
            # 3D Rotations
            x1 = x_k * cos_y + z_k * sin_y
            y1 = y_k
            z1 = -x_k * sin_y + z_k * cos_y
            
            x2 = x1
            y2 = y1 * cos_p - z1 * sin_p
            z2 = y1 * sin_p + z1 * cos_p
            
            # Perspective projection
            fov = 3200.0
            dist = fov / (fov + z2 * rad_px * 0.65)
            px = cx + x2 * rad_px * dist
            py = cy - y2 * rad_px * dist
            
            all_cells.append({
                "px": px,
                "py": py,
                "z": z2,
                "dist": dist,
                "tier": tier,
                "k": k,
                "rad_px": rad_px
            })
            
    print(f"[OPUS-037] Total quantized cells generated: {len(all_cells)}. Sorting by depth...")
    all_cells.sort(key=lambda c: c["z"])
    
    print("[OPUS-037] Inscribing non-commutative matrix commutator filaments...")
    # Commutator links between adjacent cells within the same shell
    for i in range(0, len(all_cells), 14):
        c1 = all_cells[i]
        for j in range(i + 1, min(i + 18, len(all_cells))):
            c2 = all_cells[j]
            if c1["tier"] == c2["tier"]:
                dx = c1["px"] - c2["px"]
                dy = c1["py"] - c2["py"]
                d_sq = dx * dx + dy * dy
                if d_sq < 9000.0: # ~95 px
                    steps = int(math.sqrt(d_sq))
                    if steps > 0:
                        light = max(0.12, (c1["z"] + c2["z"] + 2.0) * 0.25)
                        for s in range(steps):
                            lx = int(c1["px"] + (dx * s) / steps)
                            ly = int(c1["py"] + (dy * s) / steps)
                            if 0 <= lx < WIDTH and 0 <= ly < HEIGHT:
                                idx = (ly * WIDTH + lx) * 3
                                if c1["tier"] == "UV":
                                    buf[idx] = min(255, buf[idx] + int(12 * light))
                                    buf[idx + 1] = min(255, buf[idx + 1] + int(38 * light))
                                    buf[idx + 2] = min(255, buf[idx + 2] + int(75 * light))
                                elif c1["tier"] == "MID":
                                    buf[idx] = min(255, buf[idx] + int(35 * light))
                                    buf[idx + 1] = min(255, buf[idx + 1] + int(25 * light))
                                    buf[idx + 2] = min(255, buf[idx + 2] + int(70 * light))
                                else: # IR core
                                    buf[idx] = min(255, buf[idx] + int(75 * light))
                                    buf[idx + 1] = min(255, buf[idx + 1] + int(50 * light))
                                    buf[idx + 2] = min(255, buf[idx + 2] + int(15 * light))
                                    
    print("[OPUS-037] Rasterizing quantized area cells as luminous quantum splats...")
    for cell in all_cells:
        px, py, z2, dist, tier, k = cell["px"], cell["py"], cell["z"], cell["dist"], cell["tier"], cell["k"]
        
        if tier == "UV":
            base_r = 3.2
            light = max(0.10, (z2 + 1.0) * 0.48)
            cr = int(255.0 * min(1.0, light * 0.28))
            cg = int(255.0 * min(1.0, light * 0.75))
            cb = int(255.0 * min(1.0, light * 0.98))
        elif tier == "MID":
            base_r = 4.2
            light = max(0.15, (z2 + 1.0) * 0.52)
            cr = int(255.0 * min(1.0, light * 0.65))
            cg = int(255.0 * min(1.0, light * 0.45))
            cb = int(255.0 * min(1.0, light * 0.95))
        else: # IR Core
            base_r = 5.8
            light = max(0.20, (z2 + 1.0) * 0.58)
            cr = int(255.0 * min(1.0, light * 0.98))
            cg = int(255.0 * min(1.0, light * 0.78))
            cb = int(255.0 * min(1.0, light * 0.32))
            
        cell_rad = max(1.8, (base_r + 2.2 * z2) * dist)
        rad_ceil = int(math.ceil(cell_rad + 2.0))
        
        min_x = max(0, int(px - rad_ceil))
        max_x = min(WIDTH, int(px + rad_ceil + 1))
        min_y = max(0, int(py - rad_ceil))
        max_y = min(HEIGHT, int(py + rad_ceil + 1))
        
        for py_i in range(min_y, max_y):
            dy_p = py_i - py
            for px_i in range(min_x, max_x):
                dx_p = px_i - px
                dist_p = math.sqrt(dx_p * dx_p + dy_p * dy_p)
                if dist_p <= cell_rad:
                    alpha = 1.0 - (dist_p / cell_rad) * 0.65
                    idx = (py_i * WIDTH + px_i) * 3
                    buf[idx] = min(255, int(buf[idx] * (1.0 - alpha) + cr * alpha))
                    buf[idx + 1] = min(255, int(buf[idx + 1] * (1.0 - alpha) + cg * alpha))
                    buf[idx + 2] = min(255, int(buf[idx + 2] * (1.0 - alpha) + cb * alpha))
                    
    out_png = os.path.join(os.path.dirname(__file__), "artwork.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[OPUS-037] Successfully rendered 4K UHD Master Plate: {out_png}")
    
    # Also sync directly to gallery assets
    gallery_dst = os.path.abspath(os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_037_artwork.png"))
    write_png(gallery_dst, WIDTH, HEIGHT, buf)
    print(f"[OPUS-037] Synced 4K master plate to gallery asset: {gallery_dst}")

if __name__ == "__main__":
    render_master_plate()

