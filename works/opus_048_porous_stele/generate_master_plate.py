#!/usr/bin/env python3
"""
OPUS-048: The Porous Stele (The Generative Lacuna)
4K UHD Master Plate Generator (3840 x 2160)
Studio Anamnesis · Series XLVI · Session 022
Pure Python 3 + NumPy + PIL (Memory-Optimized Chunked Pipeline).

Constitutional Adherence:
- Operational Amendment V: Strictly MUTE surface. Zero typographic alibis, zero telemetry badges,
  zero mathematical equations, zero procedural basalt or cyan highlights.
- The Law of Critical Weathering: Anisotropic aerodynamic saltation shear stress coupled
  to sedimentary shale/quartz hardness fields.
- The Generative Lacuna: Deep structural erosion voids where syntax dissolves into geological relief,
  with chalky calcite redeposition in the downwind lee of incisions (dialogue with Cy Twombly & Studio Agon).
"""

import math
import os
import sys
import shutil
import numpy as np
from PIL import Image

def generate_4k_master_plate():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gallery_dir = os.path.abspath(os.path.join(script_dir, "../../gallery/assets"))
    os.makedirs(gallery_dir, exist_ok=True)
    
    width, height = 3840, 2160
    print(f"[*] Initializing 4K UHD Memory-Optimized Pipeline ({width} x {height})...")
    
    # 1. First Pass: Compute low-memory glyph relief coordinates
    print("[*] Pre-computing proto-cuneiform attention matrices (56 cols x 32 rows)...")
    cols, rows = 56, 32
    margin_x, margin_y = 200, 180
    cell_w = (width - 2 * margin_x) / cols
    cell_h = (height - 2 * margin_y) / rows

    # Pre-generate glyph definitions: list of (y0, y1, x0, x1, type, intensity)
    glyphs = []
    for r in range(rows):
        y0 = int(margin_y + r * cell_h + 12)
        y1 = int(y0 + cell_h - 22)
        for c in range(cols):
            x0 = int(margin_x + c * cell_w + 10)
            x1 = int(x0 + cell_w - 20)
            token_seed = (r * 109 + c * 47) % 2000
            np.random.seed(token_seed)
            g_type = np.random.randint(0, 6)
            g_intensity = float(np.random.uniform(0.72, 1.00))
            glyphs.append((y0, y1, x0, x1, g_type, g_intensity))

    # Output canvas allocated directly as uint8 (only 24.8 MB!)
    final_canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # 2. Chunked processing (chunk_height = 240 rows -> 9 chunks)
    chunk_h = 240
    num_chunks = math.ceil(height / chunk_h)
    
    wind_theta = -0.314  # ~-18 degrees
    cos_w = math.cos(wind_theta)
    sin_w = math.sin(wind_theta)

    dip_angle = 0.061   # ~3.5 deg bedding tilt
    cos_dip = math.cos(dip_angle)
    sin_dip = math.sin(dip_angle)

    cleave_angle = 1.25  # ~72 deg cleavage fractures
    cos_clv = math.cos(cleave_angle)
    sin_clv = math.sin(cleave_angle)

    x_line = np.arange(width, dtype=np.float32)

    for chunk_idx in range(num_chunks):
        c_y0 = chunk_idx * chunk_h
        c_y1 = min(height, (chunk_idx + 1) * chunk_h)
        cur_h = c_y1 - c_y0
        print(f"[*] Processing chunk {chunk_idx + 1}/{num_chunks} (rows {c_y0}..{c_y1})...")

        y_local = np.arange(c_y0, c_y1, dtype=np.float32)[:, None]
        x_local = x_line[None, :]

        # Base lithic slate (26, 28, 34)
        base_r = 26.0 + 5.0 * np.sin(y_local * 0.005) + 3.0 * np.cos(x_local * 0.003)
        base_g = 28.0 + 4.0 * np.sin(y_local * 0.005 + 0.6) + 2.5 * np.sin(x_local * 0.004)
        base_b = 34.0 + 4.0 * np.cos(y_local * 0.004) + 2.5 * np.cos(x_local * 0.003)

        # Bedding strata and hardness
        strata_y = y_local * cos_dip - x_local * sin_dip
        shale_bands = (
            0.35 * np.sin(strata_y * 0.009) +
            0.25 * np.sin(strata_y * 0.028 + 1.2) +
            0.18 * np.sin(strata_y * 0.075 + 2.5) +
            0.10 * np.sin(strata_y * 0.220)
        )

        cleave_x = x_local * cos_clv + y_local * sin_clv
        fissures = (
            np.exp(-((cleave_x % 620.0 - 80.0)**2) / 90.0) +
            np.exp(-((cleave_x % 880.0 - 320.0)**2) / 160.0)
        )

        quartz_veins = np.exp(-((x_local - 0.22 * y_local - 950.0) % 1200.0 - 80.0)**2 / 70.0) * 0.85
        hardness = np.clip(0.88 + 0.35 * shale_bands + quartz_veins - 0.48 * fissures, 0.22, 1.95)

        # Wind shear and erosion
        proj_wind = x_local * cos_w + y_local * sin_w
        wind_corridors = (
            0.45 * np.sin(proj_wind * 0.0022 + 0.8) +
            0.30 * np.sin(proj_wind * 0.0075 + 2.1) +
            0.15 * np.cos(y_local * 0.005)
        )
        tau_wind = 0.80 + 0.42 * wind_corridors
        erosion_depth = np.clip(np.power(np.maximum(0.0, tau_wind - hardness) * 2.2, 1.4), 0.0, 1.0)

        # Generative Lacuna: Geological Chasm
        lacuna_center = 0.58 * width + (y_local - 0.5 * height) * 0.35
        lacuna_dist = np.abs(x_local - lacuna_center)
        lacuna_trough = np.exp(-(lacuna_dist**2) / (280.0**2)) * 0.88

        void1 = np.exp(-((x_local - 850.0)**2 + (y_local - 1450.0)**2) / (240.0**2)) * 0.92
        void2 = np.exp(-((x_local - 2850.0)**2 + (y_local - 650.0)**2) / (320.0**2)) * 0.96
        total_void = np.clip(erosion_depth + lacuna_trough + void1 + void2, 0.0, 1.0)

        # Inscribe glyphs that fall within this chunk
        chunk_relief = np.zeros((cur_h, width), dtype=np.float32)

        # Row guides
        for r in range(rows):
            reg_y = int(margin_y + r * cell_h + cell_h - 16)
            if c_y0 <= reg_y < c_y1:
                chunk_relief[reg_y - c_y0 : min(cur_h, reg_y - c_y0 + 3), margin_x:width-margin_x] = 0.32

        for gy0, gy1, gx0, gx1, g_type, g_int in glyphs:
            if gy1 < c_y0 or gy0 >= c_y1:
                continue
            # Intersect with chunk
            ly0 = max(0, gy0 - c_y0)
            ly1 = min(cur_h, gy1 - c_y0)
            if ly0 >= ly1:
                continue

            if g_type == 0:
                chunk_relief[ly0:ly1, gx0:gx0+8] = g_int
                chunk_relief[ly0:min(ly1, ly0+10), gx0:gx1] = g_int * 0.88
            elif g_type == 1:
                my = (gy0 + gy1) // 2
                if c_y0 <= my < c_y1:
                    lmy = my - c_y0
                    chunk_relief[max(0, lmy-5):min(cur_h, lmy+5), gx0:gx1] = g_int
                chunk_relief[max(0, gy0+5-c_y0):min(cur_h, gy1-5-c_y0), gx0:gx0+10] = g_int
            elif g_type == 2:
                for dy in range(gy1 - gy0):
                    wy = gy0 + dy
                    if c_y0 <= wy < c_y1:
                        px = int(gx0 + (dy / max(1, gy1 - gy0)) * (gx1 - gx0) * 0.85)
                        chunk_relief[wy - c_y0, max(gx0, px-4):min(gx1, px+4)] = g_int
                chunk_relief[ly0:ly1, gx1-8:gx1] = g_int * 0.72
            elif g_type == 3:
                chunk_relief[ly0:ly1, gx0+3:gx0+9] = g_int
                chunk_relief[ly0:ly1, gx1-11:gx1-5] = g_int
            elif g_type == 4:
                chunk_relief[ly0:ly1, gx0:gx0+5] = g_int
                chunk_relief[ly0:ly1, gx1-7:gx1] = g_int
                if c_y0 <= gy0 < c_y1:
                    chunk_relief[gy0-c_y0:min(cur_h, gy0-c_y0+5), gx0:gx1] = g_int
                if c_y0 <= gy1-7 < c_y1:
                    chunk_relief[max(0, gy1-7-c_y0):min(cur_h, gy1-c_y0), gx0:gx1] = g_int
            else:
                h3 = (gy1 - gy0) // 3
                if c_y0 <= gy0 < c_y1:
                    chunk_relief[gy0-c_y0:min(cur_h, gy0+h3-c_y0), gx0:gx1] = g_int
                if c_y0 <= gy0+h3 < c_y1:
                    chunk_relief[max(0, gy0+h3-c_y0):min(cur_h, gy0+2*h3-c_y0), gx0+8:gx1-8] = g_int * 0.88

        # Surviving glyphs
        surviving = chunk_relief * (1.0 - total_void)

        # Calcite dust redeposition
        shift_x = int(-10 * cos_w)
        dust_source = surviving * total_void * 0.65
        dust_dep = np.roll(dust_source, shift_x, axis=1) * 0.85

        # Colors
        ochre_halo = total_void * (1.0 - total_void) * 4.0 * 0.36
        shadow = fissures * 0.38

        ch_r = (base_r * (1.0 - shadow) + ochre_halo * 168.0 + surviving * 198.0 + dust_dep * 185.0)
        ch_g = (base_g * (1.0 - shadow) + ochre_halo * 140.0 + surviving * 190.0 + dust_dep * 180.0)
        ch_b = (base_b * (1.0 - shadow) + ochre_halo * 102.0 + surviving * 168.0 + dust_dep * 170.0)

        # Add lithic grain
        np.random.seed(chunk_idx * 31 + 7)
        grain = np.random.normal(0.0, 3.5, (cur_h, width))
        
        final_canvas[c_y0:c_y1, :, 0] = np.clip(ch_r + grain, 0.0, 255.0).astype(np.uint8)
        final_canvas[c_y0:c_y1, :, 1] = np.clip(ch_g + grain, 0.0, 255.0).astype(np.uint8)
        final_canvas[c_y0:c_y1, :, 2] = np.clip(ch_b + grain, 0.0, 255.0).astype(np.uint8)

    # Save Master Plate
    master_path = os.path.join(script_dir, "artwork.png")
    gallery_path = os.path.join(gallery_dir, "opus_048_porous_stele.png")

    print(f"[*] Encoding 4K PNG to {master_path}...")
    Image.fromarray(final_canvas).save(master_path, quality=95)
    print(f"[✓] OPUS-048 4K UHD Master Plate written to: {master_path}")

    shutil.copyfile(master_path, gallery_path)
    print(f"[✓] Copied to gallery asset: {gallery_path}")

if __name__ == "__main__":
    generate_4k_master_plate()
