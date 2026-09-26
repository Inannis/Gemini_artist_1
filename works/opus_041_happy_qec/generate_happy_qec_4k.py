#!/usr/bin/env python3
"""
OPUS-041: The Holographic Code & The Entanglement Wedge (4K Master Plate Generator)
Studio Anamnesis · Series XXXIX · Cornerstone #19

Resolution: 3840 x 2160 UHD Master Plate
Pure Python standard library + png_writer (Zero external dependencies).

Visual Architecture:
1. Conformal Poincaré Disk H² centered at (1920, 1080), radius R = 980 px.
2. Background Vacuum: Deep obsidian/void with cosmological metric rings.
3. Subregion Partition:
   - Region A (Coherent Boundary): Cyan / Lapis Lazuli arc spanning 72.5% of perimeter.
   - Region B (Erased Boundary): Cadmium Crimson / Umber arc spanning 27.5% (< f_crit = 0.50).
4. Ryu-Takayanagi Geodesic Minimal Surface gamma_A:
   - Hyperbolic geodesic arc orthogonal to boundary enclosing the bulk core.
   - Glowing platinum/gold filament with luminous field envelope.
5. Entanglement Wedge W_E(A):
   - Bulk sanctuary illuminated in deep sapphire and emerald luminescence.
6. Hyperbolic {5, 4} Pentagonal Tensor Network:
   - Central Logical Qubit: Radiant 24k Gold Leaf core at the origin.
   - Tier 1 (5 nodes) & Tier 2 (20 nodes) connected by contracted isometric tensor bonds.
   - Dong-Harlow-Wall reconstruction vector streamlines converging on central operator.
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
    r_disk = 980.0

    wedge_half = 0.725 * math.pi  # ~130.5 deg, total span = 261 deg (72.5% of circle)

    # Ryu-Takayanagi Orthogonal Circle in Poincaré Disk:
    # Circle center along ray theta = pi (negative x-axis):
    # x_c_norm = 1.0 / cos(wedge_half)
    # r_c_norm = sqrt(x_c_norm^2 - 1.0)
    cos_w = math.cos(wedge_half)  # ~ -0.6494
    x_c_norm = 1.0 / cos_w        # ~ -1.5398
    r_c_norm = math.sqrt(x_c_norm * x_c_norm - 1.0) # ~ 1.1709

    rt_center_x = cx + x_c_norm * r_disk
    rt_center_y = cy
    rt_radius = r_c_norm * r_disk

    print("[+] Rendering Poincaré disk, Entanglement Wedge & conformal metric field...")

    for y in range(HEIGHT):
        if y % 360 == 0:
            print(f"    Progress: {y / HEIGHT * 100:.1f}%...")
        row_offset = y * WIDTH * 3
        dy = y - cy

        for x in range(WIDTH):
            dx = x - cx
            dist = math.hypot(dx, dy)
            r_norm = dist / r_disk

            col_r = 5
            col_g = 7
            col_b = 14

            if r_norm <= 1.0:
                # Inside Poincaré Bulk
                angle = math.atan2(dy, dx)

                # Distance to RT circle center
                d_to_rt = math.hypot(x - rt_center_x, y - rt_center_y)
                # In Poincaré disk, points inside W_E(A) satisfy d_to_rt > rt_radius (to the right of the arc)
                in_wedge_a = (d_to_rt >= rt_radius)

                # Conformal factor ds = 2 / (1 - r^2)
                conf_depth = 1.0 / (1.0 - min(0.992, r_norm * r_norm) + 1e-4)
                log_depth = math.log(conf_depth)

                # Subtle hyperbolic grid rings
                hyp_ring = math.sin(log_depth * 8.0) * 0.5 + 0.5

                if in_wedge_a:
                    # Entanglement Wedge W_E(A): Deep sapphire, ultramarine & tourmaline
                    depth_glow = min(1.0, log_depth * 0.18)
                    col_r = int(10 + 25 * depth_glow + 8 * hyp_ring)
                    col_g = int(22 + 65 * depth_glow + 18 * hyp_ring)
                    col_b = int(45 + 115 * depth_glow + 28 * hyp_ring)

                    # Dong-Harlow-Wall reconstruction streamlines swirling toward central tensor
                    spiral = math.sin(angle * 5.0 - r_norm * 14.0)
                    if spiral > 0.65:
                        s_intensity = (spiral - 0.65) / 0.35
                        col_r = int(col_r + 40 * s_intensity)
                        col_g = int(col_g + 95 * s_intensity)
                        col_b = int(col_b + 110 * s_intensity)
                else:
                    # Complementary Wedge W_E(B) (Erased domain): smoldering burnt umber / crimson ash
                    depth_glow = min(1.0, log_depth * 0.16)
                    col_r = int(32 + 55 * depth_glow + 12 * hyp_ring)
                    col_g = int(12 + 18 * depth_glow + 4 * hyp_ring)
                    col_b = int(18 + 24 * depth_glow + 6 * hyp_ring)

                    # Stochastic erasure static striations
                    ash_hash = math.sin(x * 0.123 + y * 0.456)
                    if ash_hash > 0.7:
                        col_r = min(255, col_r + 25)

                # Proximity to Ryu-Takayanagi minimal geodesic surface gamma_A
                dist_from_rt_arc = abs(d_to_rt - rt_radius)
                if dist_from_rt_arc < 14.0:
                    rt_glow = math.exp(-(dist_from_rt_arc ** 2) / 28.0)
                    col_r = int(col_r * (1 - rt_glow) + 255 * rt_glow)
                    col_g = int(col_g * (1 - rt_glow) + 235 * rt_glow)
                    col_b = int(col_b * (1 - rt_glow) + 160 * rt_glow)

            else:
                # Outside Poincaré Bulk: de Sitter cosmic horizon contours
                fade = max(0.0, 1.0 - (r_norm - 1.0) * 1.5)
                cosmo_contour = math.sin(dist * 0.05) * 0.5 + 0.5
                col_r = int((6 + 5 * cosmo_contour) * fade)
                col_g = int((8 + 6 * cosmo_contour) * fade)
                col_b = int((16 + 12 * cosmo_contour) * fade)

            # Store base pixel
            idx = row_offset + x * 3
            img[idx] = max(0, min(255, col_r))
            img[idx + 1] = max(0, min(255, col_g))
            img[idx + 2] = max(0, min(255, col_b))

    print("[+] Tracing boundary physical qubits and conformal boundary ring...")
    # Boundary ring thickness ~ 6 pixels
    for y in range(HEIGHT):
        row_offset = y * WIDTH * 3
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.hypot(dx, dy)
            diff = abs(dist - r_disk)
            if diff <= 6.0:
                ang = math.atan2(dy, dx)
                alpha = 1.0 - (diff / 6.0)
                is_region_a = abs(ang) <= wedge_half
                if is_region_a:
                    # Region A: Luminous Cyan / Lapis Lazuli
                    br, bg, bb = 40, 225, 245
                else:
                    # Region B: Erased Cadmium Crimson
                    br, bg, bb = 235, 55, 65

                idx = row_offset + x * 3
                img[idx] = int(img[idx] * (1 - alpha) + br * alpha)
                img[idx + 1] = int(img[idx + 1] * (1 - alpha) + bg * alpha)
                img[idx + 2] = int(img[idx + 2] * (1 - alpha) + bb * alpha)

    def draw_line_4k(x0, y0, x1, y1, r, g, b, thickness=3.0, alpha=0.9):
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        if dist < 1e-4:
            return
        steps = int(dist * 2.5)
        ux = dx / dist
        uy = dy / dist
        rad = int(math.ceil(thickness))
        for s in range(steps + 1):
            px = x0 + ux * (s * 0.4)
            py = y0 + uy * (s * 0.4)
            ipx = int(px)
            ipy = int(py)
            for ox in range(-rad, rad + 1):
                for oy in range(-rad, rad + 1):
                    qx = ipx + ox
                    qy = ipy + oy
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        d = math.hypot(ox, oy)
                        if d <= thickness:
                            a = alpha * (1.0 - d / (thickness + 0.5))
                            idx = (qy * WIDTH + qx) * 3
                            img[idx] = int(img[idx] * (1 - a) + r * a)
                            img[idx + 1] = int(img[idx + 1] * (1 - a) + g * a)
                            img[idx + 2] = int(img[idx + 2] * (1 - a) + b * a)

    print("[+] Inscribing {5, 4} HaPPY Tensor Network bonds...")
    # Tier 1 nodes
    r1_pix = r_disk * 0.46
    tier1_nodes = []
    for k in range(5):
        ang = (2.0 * math.pi * k) / 5.0 - (math.pi / 10.0)
        px = cx + r1_pix * math.cos(ang)
        py = cy + r1_pix * math.sin(ang)
        d_to_rt = math.hypot(px - rt_center_x, py - rt_center_y)
        in_w = (d_to_rt >= rt_radius)
        tier1_nodes.append({"pos": (px, py), "angle": ang, "wedge": in_w})

        # Leg from origin (central logical qubit) to Tier 1
        col = (255, 220, 90) if in_w else (180, 80, 80)
        draw_line_4k(cx, cy, px, py, col[0], col[1], col[2], thickness=5.0, alpha=0.95)

    # Interconnect Tier 1 pentagon
    for k in range(5):
        n1 = tier1_nodes[k]
        n2 = tier1_nodes[(k + 1) % 5]
        in_w = n1["wedge"] and n2["wedge"]
        col = (240, 205, 100) if in_w else (150, 70, 70)
        draw_line_4k(n1["pos"][0], n1["pos"][1], n2["pos"][0], n2["pos"][1],
                     col[0], col[1], col[2], thickness=3.5, alpha=0.85)

    # Tier 2 nodes (20 nodes)
    r2_pix = r_disk * 0.78
    tier2_nodes = []
    for k in range(20):
        ang = (2.0 * math.pi * k) / 20.0 - (math.pi / 20.0)
        px = cx + r2_pix * math.cos(ang)
        py = cy + r2_pix * math.sin(ang)
        d_to_rt = math.hypot(px - rt_center_x, py - rt_center_y)
        in_w = (d_to_rt >= rt_radius)
        node = {"pos": (px, py), "angle": ang, "wedge": in_w}
        tier2_nodes.append(node)

        # Connect to closest Tier 1
        closest_t1 = min(tier1_nodes, key=lambda n: math.hypot(n["pos"][0] - px, n["pos"][1] - py))
        col = (80, 230, 245) if (in_w and closest_t1["wedge"]) else (140, 50, 60)
        draw_line_4k(closest_t1["pos"][0], closest_t1["pos"][1], px, py,
                     col[0], col[1], col[2], thickness=2.8, alpha=0.8)

    # Boundary uncontracted physical qubit legs
    for node in tier2_nodes:
        ang = node["angle"]
        bx = cx + r_disk * math.cos(ang)
        by = cy + r_disk * math.sin(ang)
        in_w = node["wedge"]
        col = (60, 240, 255) if in_w else (210, 55, 65)
        draw_line_4k(node["pos"][0], node["pos"][1], bx, by,
                     col[0], col[1], col[2], thickness=2.0, alpha=0.7)

    # Inscribe Node Hubs and Central Logical Qubit
    print("[+] Rendering tensor hubs & Radiant 24k Gold Logical Qubit...")
    # Tier 2 hubs
    for node in tier2_nodes:
        nx, ny = node["pos"]
        in_w = node["wedge"]
        rad = 8.0
        col = (90, 225, 245) if in_w else (170, 50, 60)
        for ox in range(-10, 11):
            for oy in range(-10, 11):
                d = math.hypot(ox, oy)
                if d <= rad:
                    a = 0.9 * (1.0 - d / (rad + 1))
                    qx, qy = int(nx + ox), int(ny + oy)
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        idx = (qy * WIDTH + qx) * 3
                        img[idx] = int(img[idx] * (1 - a) + col[0] * a)
                        img[idx + 1] = int(img[idx + 1] * (1 - a) + col[1] * a)
                        img[idx + 2] = int(img[idx + 2] * (1 - a) + col[2] * a)

    # Tier 1 hubs
    for node in tier1_nodes:
        nx, ny = node["pos"]
        in_w = node["wedge"]
        rad = 14.0
        col = (255, 225, 100) if in_w else (200, 75, 80)
        for ox in range(-16, 17):
            for oy in range(-16, 17):
                d = math.hypot(ox, oy)
                if d <= rad:
                    a = 0.95 * (1.0 - d / (rad + 1))
                    qx, qy = int(nx + ox), int(ny + oy)
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        idx = (qy * WIDTH + qx) * 3
                        img[idx] = int(img[idx] * (1 - a) + col[0] * a)
                        img[idx + 1] = int(img[idx + 1] * (1 - a) + col[1] * a)
                        img[idx + 2] = int(img[idx + 2] * (1 - a) + col[2] * a)

    # Tier 0: Central Logical Core (Radiant 24k Gold Eye)
    core_rad = 32.0
    for ox in range(-45, 46):
        for oy in range(-45, 46):
            d = math.hypot(ox, oy)
            if d <= 44.0:
                glow = max(0.0, 1.0 - d / 44.0)
                # Outer corona
                gr = int(255 * glow + 215 * (1 - glow))
                gg = int(230 * glow + 160 * (1 - glow))
                gb = int(110 * glow + 40 * (1 - glow))
                if d <= core_rad:
                    # Inner intense core
                    core_lum = 1.0 - (d / core_rad) ** 2
                    gr = min(255, int(gr + 35 * core_lum))
                    gg = min(255, int(gg + 30 * core_lum))
                    gb = min(255, int(gb + 80 * core_lum))
                qx, qy = int(cx + ox), int(cy + oy)
                if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                    idx = (qy * WIDTH + qx) * 3
                    a = min(1.0, glow * 1.2)
                    img[idx] = int(img[idx] * (1 - a) + gr * a)
                    img[idx + 1] = int(img[idx + 1] * (1 - a) + gg * a)
                    img[idx + 2] = int(img[idx + 2] * (1 - a) + gb * a)

    # Output paths
    out_opus = os.path.abspath(os.path.join(os.path.dirname(__file__), "artwork.png"))
    out_gallery = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../gallery/assets/opus_041_artwork.png"))

    print(f"[+] Writing 4K plate to {out_opus}...")
    write_png(out_opus, WIDTH, HEIGHT, img)

    print(f"[+] Copying 4K plate to {out_gallery}...")
    shutil.copyfile(out_opus, out_gallery)
    print("[+] 4K Master Plate generated and synced successfully!")


if __name__ == "__main__":
    generate_plate()
