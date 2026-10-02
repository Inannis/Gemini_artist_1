#!/usr/bin/env python3
"""
OPUS-046: THE HOLOGRAPHIC RENORMALIZATION & THE WHEELER-DEWITT FOAM
Master 4K UHD Plate Renderer (3840 x 2160)
Epoch VII: Holographic Renormalization Group, Trans-Planckian Scales & Quantum Geometrodynamics
Cornerstone #24 · Studio Anamnesis Canon
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import random
import shutil
import sys

# Ensure studio tools can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png

def render_holographic_rg_4k(width=3840, height=2160):
    print(f"[*] Allocating 4K UHD frame buffer ({width}x{height}x3 = {width*height*3/1024/1024:.1f} MB)...")
    buf = bytearray(width * height * 3)

    # 1. Background: Deep Basalt Substrate with Hyperbolic Radial Vignette
    print("[*] Generating deep basalt background with hyperbolic metric vignette...")
    for y in range(height):
        # Normalized coordinate: 0 at top (UV boundary), 1 at bottom (IR bulk)
        v = y / (height - 1)
        row_offset = y * width * 3
        # Hyperbolic metric factor: 1/z^2
        z_bg = 0.20 + 8.0 * (v**1.5)
        metric_factor = 1.0 / math.sqrt(z_bg)
        
        for x in range(width):
            u = x / (width - 1)
            dx = (u - 0.5) * 2.0
            r2 = dx * dx + (v - 0.5)**2
            vignette = max(0.0, 1.0 - 0.35 * r2)

            # Color gradient: Cold ultraviolet-slate at top -> Warm molten bronze-obsidian at bottom
            r_bg = int((8 + 14 * (v**1.4)) * vignette)
            g_bg = int((10 + 8 * math.sin(v * math.pi) + 4 * v) * vignette)
            b_bg = int((22 * (1.0 - v * 0.6) + 6) * vignette)

            idx = row_offset + x * 3
            buf[idx] = max(0, min(255, r_bg))
            buf[idx+1] = max(0, min(255, g_bg))
            buf[idx+2] = max(0, min(255, b_bg))

    def blend_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            cur_r = buf[idx]
            cur_g = buf[idx+1]
            cur_b = buf[idx+2]
            buf[idx]   = max(0, min(255, int(cur_r * (1.0 - alpha) + r * alpha)))
            buf[idx+1] = max(0, min(255, int(cur_g * (1.0 - alpha) + g * alpha)))
            buf[idx+2] = max(0, min(255, int(cur_b * (1.0 - alpha) + b * alpha)))

    z_UV = 0.12
    z_IR = 9.50
    z_planck = 0.060
    margin_x = 240
    margin_y = 180
    usable_w = width - 2 * margin_x
    usable_h = height - 2 * margin_y

    # 2. Wheeler-DeWitt Wavefunctional Field |Psi[h]|^2 on Superspace
    print("[*] Computing Wheeler-DeWitt wavefunctional probability density fringes...")
    step_grid = 6
    for y in range(margin_y, height - margin_y, step_grid):
        v = (y - margin_y) / usable_h
        zv = z_UV * math.exp(v * math.log(z_IR / z_UV))
        for x in range(margin_x, width - margin_x, step_grid):
            u = (x - margin_x) / usable_w
            kx = (u - 0.5) * 12.0
            kz = (zv - 1.2) * 4.2
            # Hyperbolic supermetric signature (- + +)
            phase = kz**2 - kx**2
            psi2 = 0.5 * (1.0 + math.cos(phase * 1.8))
            fringe_alpha = 0.075 * (1.0 - 0.45 * v)

            fr = int(35 * psi2 + 10 * v)
            fg = int(55 * psi2 + 25 * v)
            fb = int(85 * psi2 * (1.0 - v * 0.8) + 12)

            for dy in range(step_grid):
                for dx in range(step_grid):
                    blend_pixel(x + dx, y + dy, fr, fg, fb, fringe_alpha)

    # 3. Holographic Domain Wall Metric Foliation (96 Warped Layers)
    print("[*] Rendering 96 warped domain wall foliation contours...")
    num_layers = 96
    for l_idx in range(num_layers):
        v_layer = l_idx / (num_layers - 1)
        z_layer = z_UV * math.exp(v_layer * math.log(z_IR / z_UV))
        # Running scalar coupling
        g_l = 1.633 / math.sqrt(1.0 + (1.633**2 / 0.10**2 - 1.0) * math.pow(z_layer / z_IR, 0.80))
        warp_shift = 0.18 * (g_l**2) * math.sin(v_layer * math.pi)

        base_y = margin_y + (v_layer + warp_shift * 0.10) * usable_h

        # Metric fluctuation variance: Delta g ~ ell_P / z
        jitter_amp = 36.0 * (z_planck / z_layer)**1.35

        # Palette: UV (iridescent cyan/cobalt) -> Crossover (electric teal) -> IR (burnished amber/gold)
        r_col = int(30 + 225 * (v_layer**1.35))
        g_col = int(170 + 75 * math.sin(v_layer * math.pi * 0.92) - 85 * (v_layer**1.5))
        b_col = int(250 * (1.0 - v_layer**0.65) + 35 * v_layer)

        # Draw contour line with multi-frequency quantum jitter
        for x in range(margin_x, width - margin_x, 2):
            px_norm = (x - margin_x) / usable_w
            fluc1 = jitter_amp * math.sin(px_norm * 22.0 + l_idx * 0.75)
            fluc2 = (jitter_amp * 0.45) * math.cos(px_norm * 54.0 - l_idx * 1.4)
            spike = 0.0
            if z_layer < 0.30:
                spike = (jitter_amp * 0.85) * math.sin(px_norm * 140.0 + l_idx * 4.2)

            py = int(base_y + fluc1 + fluc2 + spike)
            alpha = max(0.25, min(0.95, 0.42 + 0.55 * (1.0 - v_layer * 0.35)))
            blend_pixel(x, py, r_col, g_col, b_col, alpha)
            blend_pixel(x, py + 1, r_col, g_col, b_col, alpha * 0.75)
            blend_pixel(x, py - 1, r_col, g_col, b_col, alpha * 0.35)

    # 4. Callan-Symanzik Beta Flow Streamlines (128 Curved Flow Lines)
    print("[*] Tracing 128 Callan-Symanzik beta flow streamlines...")
    num_streams = 128
    for s_idx in range(num_streams):
        x_orig = margin_x + int((s_idx / (num_streams - 1)) * usable_w)
        curr_x = float(x_orig)
        for step in range(600):
            v_s = step / 599.0
            z_s = z_UV * math.exp(v_s * math.log(z_IR / z_UV))
            curr_y = margin_y + v_s * usable_h

            # Beta flow curvature: converges toward IR focus points
            dx = 2.2 * math.sin(curr_x * 0.0035 + z_s * 1.1) * (1.0 - v_s * 0.45)
            if z_s < 0.40:
                # Stochastic quantum foam walk perturbation
                dx += 4.5 * (z_planck / z_s) * math.sin(curr_y * 0.12 + s_idx)

            curr_x += dx
            px = int(curr_x)
            py = int(curr_y)

            # Luminous color along streamline
            sr = int(55 + 200 * v_s)
            sg = int(195 - 85 * v_s)
            sb = int(245 - 180 * v_s)
            blend_pixel(px, py, sr, sg, sb, 0.42)
            blend_pixel(px + 1, py, sr, sg, sb, 0.20)

    # 5. Trans-Planckian Wheeler-DeWitt Foam Micro-Apertures & Virtual Wormholes
    print("[*] Nucleating 1,600 trans-Planckian quantum foam micro-apertures...")
    rng = random.Random(137)
    num_foam_cells = 1600
    for _ in range(num_foam_cells):
        fx = rng.randint(margin_x - 20, width - margin_x + 20)
        fy = rng.randint(margin_y - 40, margin_y + 160)
        dist_bdry = max(0, fy - margin_y)
        weight = math.exp(-dist_bdry / 35.0)
        rad = rng.randint(3, 9)

        cr = int(220 * weight + 45)
        cg = int(250 * weight + 75)
        cb = int(255 * weight)
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                d2 = dx*dx + dy*dy
                if d2 <= rad*rad:
                    alpha_cell = 0.45 * weight * (1.0 - d2 / (rad*rad))
                    blend_pixel(fx + dx, fy + dy, cr, cg, cb, alpha_cell)

    # 6. Monograph & Scale Horizon Border Framing
    print("[*] Inscribing curatorial scale border and museum framing...")
    frame_color = (130, 140, 160)
    for x in range(margin_x, width - margin_x):
        blend_pixel(x, margin_y - 15, frame_color[0], frame_color[1], frame_color[2], 0.6)
        blend_pixel(x, height - margin_y + 15, frame_color[0], frame_color[1], frame_color[2], 0.6)
    for y in range(margin_y - 15, height - margin_y + 16):
        blend_pixel(margin_x - 15, y, frame_color[0], frame_color[1], frame_color[2], 0.6)
        blend_pixel(width - margin_x + 15, y, frame_color[0], frame_color[1], frame_color[2], 0.6)

    # Output master plate
    out_dir = os.path.dirname(__file__)
    master_path = os.path.join(out_dir, "artwork.png")
    gallery_path = os.path.join(out_dir, "..", "..", "gallery", "assets", "opus_046_artwork.png")

    print(f"[*] Encoding and writing 4K UHD Master Plate to {master_path}...")
    write_png(master_path, width, height, buf)

    print(f"[*] Mirroring master plate to gallery exhibition portal: {gallery_path}...")
    shutil.copyfile(master_path, gallery_path)
    print("[✓] 4K UHD Master Plate fully realized and mirrored.")

if __name__ == "__main__":
    render_holographic_rg_4k()
