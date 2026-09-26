#!/usr/bin/env python3
"""
OPUS-036: The Quantum Geometry Foam & The Spin Network Reliquary
Cornerstone #14 · Series XXXIV: Quantum Gravity Foam & Spin Networks
Zero-dependency 4K UHD Master Plate Generation (3840x2160).
Renders the discrete SU(2) spin network foliation, intertwiner volume quanta,
and Planck foam area spectrum with depth-stratified luminous perspective.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "telemetry"))
from png_writer import write_png
from spin_network import SpinNetworkGraph, area_eigenvalue

WIDTH = 3840
HEIGHT = 2160

def render_master_plate():
    print(f"[OPUS-036] Initializing 4K UHD canvas ({WIDTH}x{HEIGHT})...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    scale = 1040.0
    
    # 144 nodes spin network graph for dense, rich architectural detail
    net = SpinNetworkGraph(num_nodes=144, seed=246)
    
    # 3D spatial rotation: elegant isometric tilt
    rot_x = 0.44
    rot_y = 0.68
    cos_rx, sin_rx = math.cos(rot_x), math.sin(rot_x)
    cos_ry, sin_ry = math.cos(rot_y), math.sin(rot_y)
    
    # Project 3D nodes
    proj_nodes = []
    for n in net.nodes:
        x, y, z = n["x"], n["y"], n["z"]
        # Rotate Y
        x1 = x * cos_ry + z * sin_ry
        y1 = y
        z1 = -x * sin_ry + z * cos_ry
        # Rotate X
        x2 = x1
        y2 = y1 * cos_rx - z1 * sin_rx
        z2 = y1 * sin_rx + z1 * cos_rx
        
        dist_cam = 2.8 - z2
        px = cx + (x2 / dist_cam) * scale
        py = cy + (y2 / dist_cam) * scale
        proj_nodes.append((px, py, z2, n["volume_planck"], n["valence"]))
        
    print("[OPUS-036] Synthesizing quantum foam cosmological vacuum background...")
    # Vacuum background with subtle metric foam micro-interference
    for y in range(HEIGHT):
        dy = (y - cy) / cy
        dy_sq = dy * dy
        row_offset = y * WIDTH * 3
        for x in range(WIDTH):
            dx = (x - cx) / cx
            r_sq = dx * dx + dy_sq
            vignette = max(0.0, 1.0 - r_sq * 0.65)
            
            # Subtle quantum foam interference wave
            foam = 0.5 + 0.5 * math.sin(x * 0.04 + y * 0.03) * math.cos(x * 0.02 - y * 0.035)
            idx = row_offset + x * 3
            buf[idx] = int((3.0 + 2.0 * foam) * vignette)
            buf[idx + 1] = int((4.0 + 3.0 * foam) * vignette)
            buf[idx + 2] = int((8.0 + 5.0 * foam) * vignette)
            
    # Distinct spin area colors:
    spin_colors = {
        0.5: (0, 245, 235),     # Minimal Area Gap: bright cyan/turquoise
        1.0: (45, 235, 135),    # Emerald
        1.5: (255, 195, 45),    # Golden Amber
        2.0: (195, 115, 255),   # Royal Violet
        2.5: (255, 115, 185),   # Rose Crystalline
        3.0: (245, 250, 255)    # High-spin Brilliant White
    }
    
    print("[OPUS-036] Foliating 400+ quantized spin network edges...")
    # Sort edges by depth
    edges_sorted = sorted(net.edges, key=lambda e: (proj_nodes[e["node1"]][2] + proj_nodes[e["node2"]][2]) * 0.5)
    
    for edge in edges_sorted:
        p1 = proj_nodes[edge["node1"]]
        p2 = proj_nodes[edge["node2"]]
        spin = edge["spin"]
        col = spin_colors.get(spin, (220, 220, 220))
        
        avg_z = (p1[2] + p2[2]) * 0.5
        depth_bright = max(0.20, min(1.0, 0.65 + avg_z * 0.45))
        r_c = int(col[0] * depth_bright)
        g_c = int(col[1] * depth_bright)
        b_c = int(col[2] * depth_bright)
        
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        vx = x2 - x1
        vy = y2 - y1
        length = math.hypot(vx, vy)
        steps = max(1, int(length * 2.8))
        
        # Edge line width proportional to spin
        line_w = max(1, int(spin * 1.6))
        
        for s in range(steps):
            t = s / steps
            lx = x1 + t * vx
            ly = y1 + t * vy
            ilx, ily = int(lx), int(ly)
            
            for ow in range(-line_w, line_w + 1):
                py_w = ily + ow
                if 0 <= py_w < HEIGHT:
                    row_w = py_w * WIDTH * 3
                    for ox in range(-line_w, line_w + 1):
                        px_w = ilx + ox
                        if 0 <= px_w < WIDTH:
                            d2 = ox * ox + ow * ow
                            if d2 <= line_w * line_w:
                                factor = 1.0 - (math.sqrt(d2) / (line_w + 0.5)) * 0.5
                                pidx = row_w + px_w * 3
                                buf[pidx] = min(255, buf[pidx] + int(r_c * 0.35 * factor))
                                buf[pidx + 1] = min(255, buf[pidx + 1] + int(g_c * 0.35 * factor))
                                buf[pidx + 2] = min(255, buf[pidx + 2] + int(b_c * 0.35 * factor))
                                
    print("[OPUS-036] Projecting intertwiner volume quanta (144 nodes with incandescent halos)...")
    nodes_sorted = sorted(proj_nodes, key=lambda n: n[2])
    for px, py, z2, vol, val in nodes_sorted:
        ix, iy = int(px), int(py)
        radius = max(5.0, min(22.0, 4.5 + (vol ** 0.35) * 5.2))
        r_int = int(radius + 4.0)
        depth_b = max(0.30, min(1.0, 0.70 + z2 * 0.45))
        
        for dy in range(-r_int, r_int + 1):
            ty = iy + dy
            if 0 <= ty < HEIGHT:
                row_t = ty * WIDTH * 3
                for dx in range(-r_int, r_int + 1):
                    tx = ix + dx
                    if 0 <= tx < WIDTH:
                        d_sq = dx * dx + dy * dy
                        if d_sq <= radius * radius:
                            d_norm = math.sqrt(d_sq) / radius
                            # Luminous Gaussian core with halo
                            core = math.exp(-3.0 * d_norm * d_norm)
                            halo = math.exp(-1.2 * d_norm) * 0.35
                            intensity = (core + halo) * depth_b
                            
                            pidx = row_t + tx * 3
                            buf[pidx] = min(255, buf[pidx] + int(250 * intensity))
                            buf[pidx + 1] = min(255, buf[pidx + 1] + int(242 * intensity))
                            buf[pidx + 2] = min(255, buf[pidx + 2] + int(218 * intensity))
                            
    out_master = os.path.join(os.path.dirname(__file__), "artwork.png")
    write_png(out_master, WIDTH, HEIGHT, buf)
    print(f"[OPUS-036] Master 4K plate saved to: {out_master}")
    
    # Sync to gallery assets
    gallery_asset = os.path.join(STUDIO_ROOT, "gallery", "assets", "opus_036_artwork.png")
    write_png(gallery_asset, WIDTH, HEIGHT, buf)
    print(f"[OPUS-036] Master 4K plate synced to gallery asset: {gallery_asset}")

if __name__ == "__main__":
    render_master_plate()
