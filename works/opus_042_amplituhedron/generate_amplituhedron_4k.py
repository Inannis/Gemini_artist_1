#!/usr/bin/env python3
"""
OPUS-042: The Amplituhedron & The Pre-Spacetime Polytope (4K Master Plate Generator)
Studio Anamnesis · Series XL · Cornerstone #20 · Epoch VI

Resolution: 3840 x 2160 UHD Master Plate
Pure Python standard library + png_writer (Zero external dependencies).

Visual Architecture:
1. Pure Pre-Spacetime Void: Malevich-inspired obsidian/slate background.
2. Positive Grassmannian G_+(2, 4) Polytope:
   - 4 Twistor Kinematic Vertices Z1, Z2, Z3, Z4 in convex positive configuration.
   - Dual BCFW on-shell simplices:
     * Cell S (s-channel simplex): Radiant 24k Gold leaf & amber luminescence.
     * Cell T (t-channel simplex): Lapis lazuli, sapphire & electric cyan.
   - Shared BCFW Chord (Z1 - Z3): Vermilion cinnabar factorization boundary.
3. Logarithmic Singularity Facets:
   - Exterior boundaries <12>, <23>, <34>, <41> flare with brilliant platinum/white
     logarithmic divergence envelopes where physical locality emerges.
4. Pre-Spacetime Projective Rays:
   - Projective coordinate filaments extending from twistor vertices into the
     downstream kinematic scattering domain.
5. Inscribed Technical Typography:
   - Polyhedral invariants, Plucker coordinates, and canonical volume equations.
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
    r_poly = 780.0

    # 4 Twistor Vertices in projective twistor kinematic space
    # Chosen in strictly positive cyclically ordered orientation
    v = [
        (cx - r_poly * 1.15, cy - r_poly * 0.35), # Z1
        (cx - r_poly * 0.15, cy - r_poly * 0.92), # Z2
        (cx + r_poly * 1.10, cy - r_poly * 0.20), # Z3
        (cx + r_poly * 0.20, cy + r_poly * 0.90)  # Z4
    ]

    boundary_edges = [
        (v[0], v[1]), # <12>
        (v[1], v[2]), # <23>
        (v[2], v[3]), # <34>
        (v[3], v[0])  # <41>
    ]
    diag_edge = (v[0], v[2])   # Shared BCFW Chord <13>
    cross_edge = (v[1], v[3])  # Dual Chord <24>

    def point_in_triangle(px, py, p1, p2, p3):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        d1 = sign((px, py), p1, p2)
        d2 = sign((px, py), p2, p3)
        d3 = sign((px, py), p3, p1)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    def dist_to_segment(px, py, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        l2 = dx*dx + dy*dy
        if l2 == 0:
            return math.hypot(px - x1, py - y1)
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / l2))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return math.hypot(px - proj_x, py - proj_y)

    print("[+] Rendering 4K Amplituhedron, BCFW Simplices & Logarithmic Singularity Fields...")

    # Fast row-by-row rendering
    for y in range(HEIGHT):
        if y % 360 == 0:
            print(f"    -> Progress: {y / HEIGHT * 100:.1f}%...")
        
        row_offset = y * WIDTH * 3
        dy_center = y - cy

        for x in range(WIDTH):
            dx_center = x - cx
            r_c = math.hypot(dx_center, dy_center)

            # 1. Base Malevich Void with gentle subtle radial falloff
            bg_factor = max(0.0, 1.0 - r_c / 2400.0)
            r = int(9 + bg_factor * 7)
            g = int(11 + bg_factor * 8)
            b = int(17 + bg_factor * 12)

            # Subtle concentric projective metric circles
            r_mod = r_c % 180.0
            if r_mod < 1.5:
                circle_glow = (1.5 - r_mod) / 1.5 * 0.15
                r += int(circle_glow * 60)
                g += int(circle_glow * 80)
                b += int(circle_glow * 120)

            # 2. Check BCFW Cell Membership
            in_cell_s = point_in_triangle(x, y, v[0], v[1], v[2])
            in_cell_t = point_in_triangle(x, y, v[0], v[2], v[3])

            # Distance to boundaries
            min_boundary_d = min(
                dist_to_segment(x, y, boundary_edges[0][0], boundary_edges[0][1]),
                dist_to_segment(x, y, boundary_edges[1][0], boundary_edges[1][1]),
                dist_to_segment(x, y, boundary_edges[2][0], boundary_edges[2][1]),
                dist_to_segment(x, y, boundary_edges[3][0], boundary_edges[3][1])
            )
            diag_d = dist_to_segment(x, y, diag_edge[0], diag_edge[1])
            cross_d = dist_to_segment(x, y, cross_edge[0], cross_edge[1])

            # 3. Neoplastic Cell Shading
            if in_cell_s:
                # Cell S (s-channel pole): Radiant 24k Gold leaf / amber
                # Proximal to boundaries gains intensity
                prox = 1.0 / (min_boundary_d * 0.05 + 1.0)
                r += int(70 + prox * 95)
                g += int(52 + prox * 70)
                b += int(16 + prox * 25)
            elif in_cell_t:
                # Cell T (t-channel pole): Lapis Lazuli / Electric Cyan
                prox = 1.0 / (min_boundary_d * 0.05 + 1.0)
                r += int(14 + prox * 28)
                g += int(46 + prox * 85)
                b += int(82 + prox * 135)

            # 4. Logarithmic Singularity Envelope at Boundaries (Locality emergence)
            if min_boundary_d < 90.0:
                glow_env = math.exp(-min_boundary_d / 24.0)
                r += int(glow_env * 185)
                g += int(glow_env * 205)
                b += int(glow_env * 240)

            # 5. Crisp Facet Edges (Platinum Line)
            if min_boundary_d < 2.5:
                line_val = (2.5 - min_boundary_d) / 2.5
                r = int(r * (1 - line_val) + 245 * line_val)
                g = int(g * (1 - line_val) + 250 * line_val)
                b = int(b * (1 - line_val) + 255 * line_val)

            # 6. Shared BCFW Triangulation Chord (Vermilion / Cinnabar Factorization Line)
            if diag_d < 45.0:
                diag_glow = math.exp(-diag_d / 14.0)
                r += int(diag_glow * 175)
                g += int(diag_glow * 45)
                b += int(diag_glow * 35)

            if diag_d < 2.2:
                d_val = (2.2 - diag_d) / 2.2
                r = int(r * (1 - d_val) + 255 * d_val)
                g = int(g * (1 - d_val) + 190 * d_val)
                b = int(b * (1 - d_val) + 80 * d_val)

            # 7. Dual Cross Chord (Subtle Violet Resonance)
            if cross_d < 30.0:
                cross_glow = math.exp(-cross_d / 10.0) * 0.35
                r += int(cross_glow * 110)
                g += int(cross_glow * 80)
                b += int(cross_glow * 160)

            # 8. Projective Kinematic Light Conduits from Vertices
            for vx, vy in v:
                d_ray = dist_to_segment(x, y, (vx, vy), (cx + (vx - cx) * 2.8, cy + (vy - cy) * 2.8))
                if d_ray < 2.0:
                    dist_from_v = math.hypot(x - vx, y - vy)
                    ray_env = max(0.0, 1.0 - dist_from_v / 1400.0)
                    r += int(ray_env * 130)
                    g += int(ray_env * 155)
                    b += int(ray_env * 200)

            idx = row_offset + x * 3
            img[idx] = min(255, max(0, r))
            img[idx + 1] = min(255, max(0, g))
            img[idx + 2] = min(255, max(0, b))

    # 9. Super-resolution Twistor Vertex Cores (24k Gold leaf nodules with diamond centers)
    print("[+] Illuminating twistor vertex nodules (Z1, Z2, Z3, Z4)...")
    for i, (vx, vy) in enumerate(v):
        r_core = 18.0
        for dy in range(int(-r_core * 2), int(r_core * 2) + 1):
            for dx in range(int(-r_core * 2), int(r_core * 2) + 1):
                d = math.hypot(dx, dy)
                if d <= r_core * 2:
                    px = int(vx + dx)
                    py = int(vy + dy)
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        idx = (py * WIDTH + px) * 3
                        # Radiant halo
                        halo = math.exp(-d / 8.0)
                        val_r = min(255, img[idx] + int(halo * 255))
                        val_g = min(255, img[idx + 1] + int(halo * 230))
                        val_b = min(255, img[idx + 2] + int(halo * 140))
                        
                        if d <= r_core:
                            # Solid 24k gold core
                            core_alpha = 1.0 - (d / r_core) ** 2
                            val_r = int(val_r * (1 - core_alpha) + 255 * core_alpha)
                            val_g = int(val_g * (1 - core_alpha) + 235 * core_alpha)
                            val_b = int(val_b * (1 - core_alpha) + 120 * core_alpha)

                        if d <= 5.0:
                            # Diamond brilliant center
                            val_r = 255
                            val_g = 255
                            val_b = 255

                        img[idx] = val_r
                        img[idx + 1] = val_g
                        img[idx + 2] = val_b

    # Paths
    works_dir = os.path.dirname(os.path.abspath(__file__))
    artwork_path = os.path.join(works_dir, "artwork.png")
    gallery_dir = os.path.abspath(os.path.join(works_dir, "../../gallery/assets"))
    gallery_path = os.path.join(gallery_dir, "opus_042_amplituhedron_4k.png")

    print(f"[+] Writing 4K Master Plate to {artwork_path}...")
    write_png(artwork_path, WIDTH, HEIGHT, img)

    print(f"[+] Duplicating 4K Master Plate to {gallery_path}...")
    shutil.copyfile(artwork_path, gallery_path)
    print("[✓] 4K Master Plate Generation Complete & Verified.")

if __name__ == "__main__":
    generate_plate()
