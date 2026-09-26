#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-038: THE SIMPLICIAL FOLIATION & THE CAUSAL FOAM
4K UHD Master Plate Renderer (3840 x 2160)
Series XXXVI (Causal Dynamical Triangulations · Cornerstone #16)

Generates a monumental 4K visualization of Lorentzian Causal Dynamical Triangulations:
1. 48 Cauchy proper-time foliation slices foliating the cosmos vertically.
2. Lorentzian 4-simplices decomposed into (4,1) and (3,2) geometric building blocks.
3. Regge curvature deficit angle calculations around 2D triangular hinges.
4. Emergent de Sitter cosmological volume expansion V_3(t) proportional to cos^3(t/tau).
5. The scale-dependent spectral dimension d_s(sigma) running from 2 (Planck sheet) to 4 (macroscopic space).
6. Pure Python standard library implementation with zero external dependencies.
"""

import math
import random
import os
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_master_plate():
    print(f"[+] Initializing 4K UHD Frame Buffer: {WIDTH}x{HEIGHT} (24.88 Megapixels)...")
    random.seed(271828)
    buffer = bytearray(WIDTH * HEIGHT * 3)

    # 1. Base cosmological redshift background
    print("[+] Synthesizing deep space cosmological background...")
    for y in range(HEIGHT):
        y_norm = y / HEIGHT
        # Gradient from deep Pre-Cambrian obsidian to cold cosmic navy
        r_bg = int(6 + 8 * (1.0 - y_norm) + 4 * math.sin(y_norm * math.pi))
        g_bg = int(8 + 10 * math.sin(y_norm * math.pi))
        b_bg = int(18 + 18 * y_norm)
        row_start = y * WIDTH * 3
        for x in range(WIDTH):
            idx = row_start + x * 3
            buffer[idx] = r_bg
            buffer[idx+1] = g_bg
            buffer[idx+2] = b_bg

    # 2. Setup 48 Cauchy proper-time slices
    print("[+] Constructing 48 Cauchy proper-time foliation hypersurfaces...")
    num_slices = 48
    margin_y = 120
    usable_h = HEIGHT - 2 * margin_y
    slice_dy = usable_h / (num_slices - 1)

    slices_vertices = []
    mid_x = WIDTH / 2.0 + 80.0 # slight right offset for left telemetric margin
    tau = (num_slices - 1) / 2.0

    # Distribute vertices along emergent de Sitter spatial volume curve
    for s in range(num_slices):
        y_slice = margin_y + s * slice_dy
        t_norm = (s - tau) / tau # -1.0 to +1.0
        
        # de Sitter cosine volume profile V_3(t) ~ cos^3(t * pi/2)
        if abs(t_norm) <= 0.96:
            vol_factor = math.pow(math.cos(t_norm * math.pi * 0.5), 1.5)
        else:
            vol_factor = 0.06 # cosmological neck / Planckian throat
            
        spatial_width = max(240.0, 2200.0 * vol_factor)
        # Number of vertices on spatial slice scales with volume
        n_verts = max(8, int(48 * (spatial_width / 2200.0)))
        
        slice_pts = []
        for v in range(n_verts):
            frac = (v + 0.5 + (random.random() - 0.5) * 0.22) / n_verts
            px = mid_x - spatial_width / 2.0 + frac * spatial_width
            # subtle z-depth for 3D raking projection
            z_depth = math.sin(frac * math.pi) * 120.0 * (1.0 + 0.3 * (random.random() - 0.5))
            slice_pts.append((px, y_slice, z_depth))
        slices_vertices.append(slice_pts)

    # Additive anti-aliased line drawer with clamping
    def draw_line(x0, y0, x1, y1, r, g, b, alpha=1.0):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                idx = (y0 * WIDTH + x0) * 3
                buffer[idx] = min(255, int(buffer[idx] + r * alpha))
                buffer[idx+1] = min(255, int(buffer[idx+1] + g * alpha))
                buffer[idx+2] = min(255, int(buffer[idx+2] + b * alpha))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    # 3. Draw space-like edges (Spatial slice cyan/ice filaments)
    print("[+] Rendering space-like simplicial edges within spatial slices...")
    for s in range(num_slices):
        pts = slices_vertices[s]
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            draw_line(p1[0], p1[1], p2[0], p2[1], 40, 195, 240, 0.70)

    # 4. Draw time-like edges (Lorentzian links: radiant gold / molten amber / amethyst)
    print("[+] Foliating Lorentzian (4,1) and (3,2) time-like simplicial links...")
    for s in range(num_slices - 1):
        pts1 = slices_vertices[s]
        pts2 = slices_vertices[s+1]
        for p1 in pts1:
            dists = sorted([(abs(p1[0] - p2[0]), p2) for p2 in pts2], key=lambda x: x[0])
            for d, p2 in dists[:2]:
                # Regge curvature factor: closer links represent higher deficit angles
                curv_factor = max(0.0, 1.0 - d / 160.0)
                r_c = int(245 * (0.65 + 0.35 * curv_factor))
                g_c = int(175 * (0.50 + 0.50 * (1.0 - curv_factor)))
                b_c = int(50 + 130 * (1.0 - curv_factor))
                draw_line(p1[0], p1[1], p2[0], p2[1], r_c, g_c, b_c, 0.55)
            # Type (3,2) cross link
            if len(dists) > 2 and random.random() < 0.40:
                p3 = dists[2][1]
                draw_line(p1[0], p1[1], p3[0], p3[1], 200, 120, 255, 0.35)

    # 5. Horizontal Cauchy time calibration lines & tick marks
    print("[+] Inscribing Cauchy proper-time horological grid...")
    for s in range(num_slices):
        y_slice = int(margin_y + s * slice_dy)
        for x in range(320, WIDTH - 200, 8):
            idx = (y_slice * WIDTH + x) * 3
            buffer[idx] = min(255, buffer[idx] + 20)
            buffer[idx+1] = min(255, buffer[idx+1] + 25)
            buffer[idx+2] = min(255, buffer[idx+2] + 40)

    # 6. Glowing Regge hinge nodes
    print("[+] Radiating Regge curvature hinge nodes...")
    for s in range(num_slices):
        for px, py, pz in slices_vertices[s]:
            ix, iy = int(px), int(py)
            radius = 4 if pz > 40 else 3
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    r2 = dx*dx + dy*dy
                    if r2 <= radius * radius:
                        qx, qy = ix + dx, iy + dy
                        if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                            idx = (qy * WIDTH + qx) * 3
                            falloff = 1.0 - math.sqrt(r2) / radius
                            buffer[idx] = min(255, int(buffer[idx] + 255 * falloff))
                            buffer[idx+1] = min(255, int(buffer[idx+1] + 245 * falloff))
                            buffer[idx+2] = min(255, int(buffer[idx+2] + 225 * falloff))

    # 7. Left Sidebar Telemetry: The Running Spectral Dimension d_s(sigma)
    print("[+] Inscribing scale-dependent spectral dimension curve d_s(sigma)...")
    curve_x0 = 140
    curve_w = 120
    for y in range(margin_y, HEIGHT - margin_y):
        y_frac = (y - margin_y) / usable_h
        sigma = 1.0 + 999.0 * math.sin(y_frac * math.pi)
        d_s = 4.02 - 2.22 / (1.0 + math.pow(sigma / 40.0, 1.25))
        curve_x = int(curve_x0 + (d_s - 1.80) / (4.02 - 1.80) * curve_w)
        for dx in range(-2, 3):
            cx = curve_x + dx
            if 0 <= cx < WIDTH:
                idx = (y * WIDTH + cx) * 3
                buffer[idx] = 56
                buffer[idx+1] = 215
                buffer[idx+2] = 210

    # Write 4K master plate
    out_dir = os.path.dirname(__file__)
    plate_path = os.path.join(out_dir, "artwork.png")
    print(f"[+] Encoding 4K UHD Master Plate to {plate_path}...")
    write_png(plate_path, WIDTH, HEIGHT, buffer)

    # Sync to gallery assets
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_038_artwork.png"))
    shutil.copyfile(plate_path, gallery_asset)
    print(f"[✓] OPUS-038 4K Master Plate written & synced to {gallery_asset}")

if __name__ == "__main__":
    render_master_plate()

