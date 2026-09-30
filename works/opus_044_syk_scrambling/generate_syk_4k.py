#!/usr/bin/env python3
"""
OPUS-044: THE SCRAMBLING HORIZON & THE SYK RELIQUARY
Series XLII · Cornerstone #22 · Epoch VI
Studio Anamnesis · Native 3840 x 2160 UHD Master Plate Generator
Pure Python Standard Library · Zero External Dependencies

Renders:
1. N = 32 Majorana fermion nodes along a fluctuating Schwarzian boundary cutoff
2. All-to-all non-local quartic couplings J_ijkl rendered as hyperbolic geodesics in Poincaré disk
3. Out-Of-Time-Order Correlator (OTOC) thermal wavefront expanding at maximal Lyapunov speed lambda_L
4. Holographic emergence of Jackiw-Teitelboim AdS2 dilaton gravity bulk from zero-dimensional chaos
"""

import os
import sys
import math
import random
import shutil

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def render_master_4k():
    buffer = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_disc = 840.0
    N = 32

    random.seed(44000)
    
    print(f"[OPUS-044] Computing 32 Majorana Nodes & Hyperbolic Quartic Network...")
    
    # 1. Compute Majorana boundary nodes with Schwarzian boundary mode fluctuations:
    # Cutoff curve: r(theta) = R_0 + sum_k c_k cos(k theta + phi_k)
    nodes = []
    for i in range(N):
        theta = 2.0 * math.pi * i / N
        fluc = 16.0 * math.cos(2.0 * theta + 0.4) + 9.5 * math.sin(3.0 * theta - 0.7) + 5.2 * math.cos(5.0 * theta + 1.1)
        r_node = r_disc + fluc
        px = cx + r_node * math.cos(theta)
        py = cy + r_node * math.sin(theta)
        nodes.append((px, py, theta))

    # Sample non-local quartic couplings J_ijkl
    # sigma_J = sqrt(6 / N^3) ~= 0.0135
    sigma_J = math.sqrt(6.0 / (N ** 3))
    chords = []
    for i in range(N):
        for j in range(i + 1, N):
            if random.random() < 0.38:
                coupling = random.gauss(0.0, sigma_J * 55.0)
                chords.append((i, j, coupling))

    print(f"[OPUS-044] Rendering 4K Master Plate ({WIDTH}x{HEIGHT}) with {len(chords)} geodesic chords...")

    # 2. Render pixel buffer (Poincaré disk bulk + OTOC operator wave + Schwarzian boundary)
    for y in range(HEIGHT):
        ny = y - cy
        ny2 = ny * ny
        if y % 240 == 0:
            print(f"  -> Scanline {y}/{HEIGHT} ({y * 100 // HEIGHT}%)...")

        for x in range(WIDTH):
            nx = x - cx
            dist2 = nx * nx + ny2
            dist = math.sqrt(dist2)
            angle = math.atan2(ny, nx)

            # Deep obsidian-slate background with subtle cosmic radial falloff
            bg_lum = max(5, int(15 - dist / 180.0))
            r_val = bg_lum
            g_val = bg_lum + 2
            b_val = bg_lum + 7

            if dist < r_disc + 35.0:
                norm_u = min(0.985, dist / r_disc)
                # Poincaré metric factor: ds^2 = 4 (dx^2 + dy^2) / (1 - u^2)^2
                poincare_conf = 1.0 / max(0.03, (1.0 - norm_u * norm_u))

                # OTOC Operator spreading front:
                # Radial wave moving from boundary (norm_u = 1) toward center (norm_u = 0)
                wave1 = math.sin(14.0 * math.log(norm_u + 0.03) - 2.8 * angle)
                wave2 = math.cos(22.0 * (1.0 - norm_u) + angle * 3.5)
                front = (wave1 * 0.65 + wave2 * 0.35)

                # Core holographic condensation & boundary layer
                core_glow = math.exp(-(norm_u * 3.0)**2) * 2.1
                edge_glow = math.exp(-((norm_u - 1.0) / 0.09)**2) * 1.6

                # Color synthesis:
                # Center: deep cobalt & violet AdS interior
                # Spreading front: radiant gold and amber
                # Boundary: electric horizon cyan Schwarzian boundary
                r_val = int(min(255, r_val + core_glow * 50 + edge_glow * 130 + max(0.0, front) * 75 * norm_u))
                g_val = int(min(255, g_val + core_glow * 40 + edge_glow * 160 + max(0.0, front) * 95 * norm_u))
                b_val = int(min(255, b_val + core_glow * 140 + edge_glow * 205 + max(0.0, front) * 45 * (1.0 - norm_u)))
            else:
                # Exterior asymptotic thermal decay
                d_ext = dist - r_disc
                ext_falloff = math.exp(-d_ext / 75.0) * 0.45
                r_val = int(min(255, r_val + ext_falloff * 95))
                g_val = int(min(255, g_val + ext_falloff * 75))
                b_val = int(min(255, b_val + ext_falloff * 125))

            idx = (y * WIDTH + x) * 3
            buffer[idx] = r_val
            buffer[idx + 1] = g_val
            buffer[idx + 2] = b_val

    # 3. Draw Hyperbolic Geodesic Chords
    print(f"[OPUS-044] Inscribing {len(chords)} Hyperbolic Entanglement Chords...")
    for i, j, coupling in chords:
        p1 = nodes[i]
        p2 = nodes[j]
        th1, th2 = p1[2], p2[2]
        d_th = abs(th1 - th2)
        if d_th > math.pi:
            d_th = 2.0 * math.pi - d_th
        pull = math.sin(d_th / 2.0) * 0.88

        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0
        ctrl_x = mid_x * (1.0 - pull) + cx * pull
        ctrl_y = mid_y * (1.0 - pull) + cy * pull

        # Color based on coupling polarity
        if coupling > 0:
            cr, cg, cb = 224, 182, 60   # Radiant Amber Gold (ferromagnetic)
        else:
            cr, cg, cb = 56, 215, 210   # Electric Horizon Cyan (antiferromagnetic)

        alpha = min(0.70, abs(coupling) * 3.0 + 0.18)
        steps = 450
        for s in range(steps):
            t = s / float(steps)
            qx = (1 - t)**2 * p1[0] + 2 * (1 - t) * t * ctrl_x + t**2 * p2[0]
            qy = (1 - t)**2 * p1[1] + 2 * (1 - t) * t * ctrl_y + t**2 * p2[1]
            
            # Anti-aliased 3x3 footprint for 4K plate
            iqx, iqy = int(qx), int(qy)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    px, py = iqx + dx, iqy + dy
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        idx = (py * WIDTH + px) * 3
                        w_sub = alpha * (1.0 if (dx == 0 and dy == 0) else 0.4)
                        buffer[idx] = int(min(255, buffer[idx] * (1.0 - w_sub) + cr * w_sub))
                        buffer[idx + 1] = int(min(255, buffer[idx + 1] * (1.0 - w_sub) + cg * w_sub))
                        buffer[idx + 2] = int(min(255, buffer[idx + 2] * (1.0 - w_sub) + cb * w_sub))

    # 4. Draw Majorana Nodes and Boundary Halo
    print("[OPUS-044] Inscribing 32 Radiant Majorana Nodes...")
    for px, py, theta in nodes:
        ipx, ipy = int(px), int(py)
        node_radius = 16
        for dy in range(-node_radius, node_radius + 1):
            for dx in range(-node_radius, node_radius + 1):
                d_sq = dx*dx + dy*dy
                if d_sq <= node_radius*node_radius:
                    qx, qy = ipx + dx, ipy + dy
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        idx = (qy * WIDTH + qx) * 3
                        fade = 1.0 - (math.sqrt(d_sq) / float(node_radius))
                        buffer[idx] = int(min(255, buffer[idx] + 255 * fade))
                        buffer[idx + 1] = int(min(255, buffer[idx + 1] + 242 * fade))
                        buffer[idx + 2] = int(min(255, buffer[idx + 2] + 210 * fade))

    out_png = os.path.join(os.path.dirname(__file__), "artwork.png")
    write_png(out_png, WIDTH, HEIGHT, buffer)
    print(f"[OPUS-044] Master 4K Plate Written: {out_png}")

    # Copy to gallery assets
    gallery_png = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_044_artwork.png")
    shutil.copyfile(out_png, gallery_png)
    print(f"[OPUS-044] Copied to Gallery Vault: {gallery_png}")

if __name__ == "__main__":
    render_master_4k()

