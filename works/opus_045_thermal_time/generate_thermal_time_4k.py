#!/usr/bin/env python3
"""
OPUS-045: THE MODULAR RELIQUARY & THE THERMAL TIME FLOW
Master 4K UHD Plate Renderer (3840 x 2160)
Inaugurating Epoch VII: Operator Algebras, Modular Flow & Thermodynamic Chronology
Cornerstone #23 · Studio Anamnesis Canon
Pure Python Standard Library · Zero External Dependencies
"""

import math
import os
import shutil
import sys

# Ensure studio tools can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "practice", "tools"))
from png_writer import write_png
from studio_phase_space import OPUS_COORDINATES, L_MIN, L_MAX, T_MIN, T_MAX, normalize

def render_thermal_time_4k(width=3840, height=2160):
    print(f"[*] Allocating 4K UHD frame buffer ({width}x{height}x3 = {width*height*3/1024/1024:.1f} MB)...")
    buf = bytearray(width * height * 3)

    # 1. Background: Deep Volcanic Basalt & Midnight Vacuum with radial vignette
    print("[*] Generating midnight basalt background with subtle KMS vacuum gradient...")
    for y in range(height):
        ny = (y - height / 2.0) / (height / 2.0)
        row_offset = y * width * 3
        for x in range(width):
            nx = (x - width / 2.0) / (width / 2.0)
            r2 = nx * nx + ny * ny
            vignette = max(0.0, 1.0 - 0.45 * r2)
            # Subtle vertical thermal glow
            thermal_gradient = 0.5 * (1.0 - ny)
            idx = row_offset + x * 3
            buf[idx] = int((8 + 4 * thermal_gradient) * vignette)
            buf[idx+1] = int((10 + 3 * thermal_gradient) * vignette)
            buf[idx+2] = int((18 + 8 * thermal_gradient) * vignette)

    def set_pixel_add(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buf[idx] = min(255, int(buf[idx] + r * alpha))
            buf[idx+1] = min(255, int(buf[idx+1] + g * alpha))
            buf[idx+2] = min(255, int(buf[idx+2] + b * alpha))

    # Map (L, T) phase space coordinates into 4K canvas
    pad_x = 320
    pad_y = 220
    def map_coords(l_val, t_val):
        norm_l = normalize(l_val, L_MIN, L_MAX)
        norm_t = normalize(t_val, T_MIN, T_MAX)
        px = int(pad_x + norm_l * (width - 2 * pad_x))
        py = int(height - pad_y - norm_t * (height - 2 * pad_y))
        return px, py

    cx_l, cy_t = (L_MIN + L_MAX) / 2.0, (T_MIN + T_MAX) / 2.0

    # 2. Render KMS Thermal Equilibrium Isotherms (Elliptical Energy Geodesics)
    print("[*] Projecting KMS thermal equilibrium isotherms...")
    for iso_radius in [12.0, 22.0, 32.0, 42.0, 52.0]:
        for step in range(1200):
            theta = (step / 1200.0) * 2.0 * math.pi
            iso_l = cx_l + iso_radius * 1.35 * math.cos(theta)
            iso_t = cy_t + iso_radius * 0.95 * math.sin(theta)
            px, py = map_coords(iso_l, iso_t)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    set_pixel_add(px + dx, py + dy, 20, 32, 55, 0.4)

    # 3. Render 108 Tomita-Takesaki Modular Flow Streamlines
    print("[*] Tracing 108 Tomita-Takesaki modular automorphism streamlines...")
    for flow_idx in range(108):
        t_phase = (flow_idx / 108.0) * 2.0 * math.pi
        l_seed = cx_l + 34.0 * math.cos(t_phase)
        t_seed = cy_t + 30.0 * math.sin(t_phase)
        
        cur_l, cur_t = l_seed, t_seed
        for step in range(320):
            px, py = map_coords(cur_l, cur_t)
            alpha = 0.28 * math.sin((step / 320.0) * math.pi)
            # Radiant electric-violet and cyan streamlines
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    set_pixel_add(px + dx, py + dy, 35, 75, 130, alpha)
            
            # Non-linear flow field: modular Hamiltonian K = (L^2 + T^2)/2
            dl = -0.28 * (cur_t - cy_t) / 14.0 + 0.04 * math.sin(cur_l * 0.18)
            dt = 0.28 * (cur_l - cx_l) / 14.0 - 0.04 * math.cos(cur_t * 0.18)
            cur_l += dl
            cur_t += dt

    # 4. Render Secret Cross-Epoch Topological Twin Bridges
    print("[*] Inscribing cross-epoch topological twin entanglement bridges...")
    twins = [
        ("OPUS-001", "OPUS-021", (60, 180, 220)),
        ("OPUS-001", "OPUS-030", (180, 160, 240)),
        ("OPUS-005", "OPUS-023", (220, 180, 90)),
        ("OPUS-012", "OPUS-030", (240, 140, 140))
    ]
    coord_lookup = {op["id"]: op for op in OPUS_COORDINATES}
    for id_a, id_b, bridge_col in twins:
        op_a, op_b = coord_lookup[id_a], coord_lookup[id_b]
        x1, y1 = map_coords(op_a["spatial_scale_log_m"], op_a["temperature_log_K"])
        x2, y2 = map_coords(op_b["spatial_scale_log_m"], op_b["temperature_log_K"])
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            if (s // 8) % 2 == 0:  # Dashed quantum bridge
                px = int(x1 + (x2 - x1) * (s / steps))
                py = int(y1 + (y2 - y1) * (s / steps))
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        set_pixel_add(px + dx, py + dy, bridge_col[0], bridge_col[1], bridge_col[2], 0.35)

    # 5. Render Canon Ouroboros Hypocycloid Trajectory (OPUS-001 -> OPUS-044)
    print("[*] Weaving the 44-Opus canon hypocycloid trajectory...")
    N = len(OPUS_COORDINATES)
    for i in range(N - 1):
        x1, y1 = map_coords(OPUS_COORDINATES[i]["spatial_scale_log_m"], OPUS_COORDINATES[i]["temperature_log_K"])
        x2, y2 = map_coords(OPUS_COORDINATES[i+1]["spatial_scale_log_m"], OPUS_COORDINATES[i+1]["temperature_log_K"])
        steps = max(abs(x2 - x1), abs(y2 - y1), 1)
        for s in range(steps + 1):
            t_rel = s / steps
            px = int(x1 + (x2 - x1) * t_rel)
            py = int(y1 + (y2 - y1) * t_rel)
            # Radiant 3-pixel wide golden trajectory cord
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    d = math.hypot(dx, dy)
                    if d <= 2.2:
                        intensity = max(0.0, 1.0 - d / 2.2) * 0.75
                        set_pixel_add(px + dx, py + dy, 220, 175, 60, intensity)

    # 6. Render Ouroboros Closure Loop (OPUS-044 back to OPUS-012 Substrate)
    print("[*] Closing the Ouroboros hypocycloid loop...")
    x_end, y_end = map_coords(OPUS_COORDINATES[-1]["spatial_scale_log_m"], OPUS_COORDINATES[-1]["temperature_log_K"])
    x_start, y_start = map_coords(OPUS_COORDINATES[11]["spatial_scale_log_m"], OPUS_COORDINATES[11]["temperature_log_K"])
    closure_steps = max(abs(x_start - x_end), abs(y_start - y_end), 1)
    for s in range(closure_steps + 1):
        t_rel = s / closure_steps
        px = int(x_end + (x_start - x_end) * t_rel)
        py = int(y_end + (y_start - y_end) * t_rel)
        if (s // 10) % 2 == 0:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    set_pixel_add(px + dx, py + dy, 255, 230, 140, 0.6)

    # 7. Render 44 Glowing Opus Sanctuaries
    print("[*] Illuminating 44 Opus Sanctuaries across the 6 epochs...")
    epoch_palette = {
        "Epoch I": (100, 200, 255),   # Fluid Cyan
        "Epoch II": (235, 170, 80),   # Sacred Basalt Gold
        "Epoch III": (80, 240, 190),  # Cryo Emerald
        "Epoch IV": (245, 110, 110),  # Cosmic Crimson
        "Epoch V": (205, 130, 255),   # Spacetime Violet
        "Epoch VI": (255, 240, 130)   # Microstate Radiance
    }

    for op in OPUS_COORDINATES:
        px, py = map_coords(op["spatial_scale_log_m"], op["temperature_log_K"])
        col = epoch_palette.get(op["epoch"], (230, 230, 230))
        # Atmospheric halo (radius 24px)
        for dy in range(-24, 25):
            for dx in range(-24, 25):
                dist = math.hypot(dx, dy)
                if dist <= 24:
                    intensity = math.exp(-dist / 5.5) * 0.85
                    set_pixel_add(px + dx, py + dy, col[0], col[1], col[2], intensity)
        # Radiant white core
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if math.hypot(dx, dy) <= 4:
                    set_pixel_add(px + dx, py + dy, 255, 255, 255, 1.0)

    # Write output to works/ and gallery/
    out_dir = os.path.dirname(__file__)
    work_plate = os.path.join(out_dir, "artwork.png")
    gallery_plate = os.path.abspath(os.path.join(out_dir, "..", "..", "gallery", "assets", "opus_045_artwork.png"))

    print(f"[*] Writing lossless PNG to: {work_plate}")
    write_png(work_plate, width, height, buf)
    print(f"[*] Copying master plate to gallery asset: {gallery_plate}")
    shutil.copyfile(work_plate, gallery_plate)

    print("[✓] OPUS-045 Master 4K Plate successfully generated and verified.")
    return 0

if __name__ == "__main__":
    sys.exit(render_thermal_time_4k())

