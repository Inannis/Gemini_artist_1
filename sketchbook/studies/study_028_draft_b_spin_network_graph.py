#!/usr/bin/env python3
"""
STUDY 028 · DRAFT B (MATERIAL FRICTION: SU(2) SPIN NETWORKS)
Series XXXIV: Quantum Gravity Foam & Spin Networks
Background-independent 3D spin network graph with discrete area-colored edges,
volume intertwiner nodes, and 15s 48kHz discrete area spectrum audio study.
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "telemetry"))
from png_writer import write_png
from audio_writer import write_wav
from spin_network import SpinNetworkGraph, area_eigenvalue

WIDTH = 1200
HEIGHT = 1200

def render_draft_b_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    scale = 420.0
    
    # 1. Generate Spin Network Graph (64 nodes, deterministic seed)
    net = SpinNetworkGraph(num_nodes=72, seed=137)
    
    # 3D rotation angles for aesthetic perspective
    rot_x = 0.45
    rot_y = 0.65
    cos_rx, sin_rx = math.cos(rot_x), math.sin(rot_x)
    cos_ry, sin_ry = math.cos(rot_y), math.sin(rot_y)
    
    # Project 3D nodes to 2D screen coordinates
    proj_nodes = []
    for n in net.nodes:
        x, y, z = n["x"], n["y"], n["z"]
        # Rotate around Y then X
        x1 = x * cos_ry + z * sin_ry
        y1 = y
        z1 = -x * sin_ry + z * cos_ry
        
        x2 = x1
        y2 = y1 * cos_rx - z1 * sin_rx
        z2 = y1 * sin_rx + z1 * cos_rx
        
        # Perspective projection
        dist_cam = 2.4 - z2
        px = cx + (x2 / dist_cam) * scale
        py = cy + (y2 / dist_cam) * scale
        proj_nodes.append((px, py, z2, n["volume_planck"], n["valence"]))
        
    # Render background: deep quantum vacuum void with subtle radial vignette
    for y in range(HEIGHT):
        dy = (y - cy) / cy
        for x in range(WIDTH):
            dx = (x - cx) / cx
            r_sq = dx * dx + dy * dy
            vignette = max(0.0, 1.0 - r_sq * 0.75)
            idx = (y * WIDTH + x) * 3
            buf[idx] = int(4 * vignette)
            buf[idx + 1] = int(5 * vignette)
            buf[idx + 2] = int(10 * vignette)
            
    # Color map for SU(2) spin representations j
    # j = 0.5 (cyan), 1.0 (emerald), 1.5 (amber), 2.0 (violet), 2.5 (rose), 3.0 (opal white)
    spin_colors = {
        0.5: (0, 240, 220),
        1.0: (40, 220, 120),
        1.5: (240, 180, 40),
        2.0: (180, 100, 255),
        2.5: (255, 110, 160),
        3.0: (230, 240, 255)
    }
    
    # Draw edges (Wilson lines / Area quanta) sorted by depth z
    edges_sorted = sorted(net.edges, key=lambda e: (proj_nodes[e["node1"]][2] + proj_nodes[e["node2"]][2]) * 0.5)
    
    for edge in edges_sorted:
        p1 = proj_nodes[edge["node1"]]
        p2 = proj_nodes[edge["node2"]]
        spin = edge["spin"]
        col = spin_colors.get(spin, (200, 200, 200))
        
        # Depth fog
        avg_z = (p1[2] + p2[2]) * 0.5
        depth_bright = max(0.2, min(1.0, 0.6 + avg_z * 0.45))
        r_c = int(col[0] * depth_bright)
        g_c = int(col[1] * depth_bright)
        b_c = int(col[2] * depth_bright)
        
        # Line rasterization with Bresenham / stepped DDA
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        vx = x2 - x1
        vy = y2 - y1
        length = math.hypot(vx, vy)
        steps = max(1, int(length * 2.0))
        
        line_w = 1.0 if spin <= 1.0 else 1.8
        for s in range(steps):
            t = s / steps
            lx = x1 + t * vx
            ly = y1 + t * vy
            ilx, ily = int(lx), int(ly)
            if 1 <= ilx < WIDTH - 1 and 1 <= ily < HEIGHT - 1:
                pix_idx = (ily * WIDTH + ilx) * 3
                buf[pix_idx] = min(255, buf[pix_idx] + r_c // 2)
                buf[pix_idx + 1] = min(255, buf[pix_idx + 1] + g_c // 2)
                buf[pix_idx + 2] = min(255, buf[pix_idx + 2] + b_c // 2)
                
    # Draw intertwiner nodes (quanta of 3-volume)
    nodes_sorted = sorted(proj_nodes, key=lambda n: n[2])
    for px, py, z2, vol, val in nodes_sorted:
        ix, iy = int(px), int(py)
        # Node radius proportional to volume
        radius = max(2.5, min(9.0, 2.0 + (vol ** 0.33) * 2.5))
        r_int = int(radius + 1.5)
        
        depth_b = max(0.3, min(1.0, 0.65 + z2 * 0.4))
        
        for dy in range(-r_int, r_int + 1):
            for dx in range(-r_int, r_int + 1):
                d_sq = dx * dx + dy * dy
                if d_sq <= radius * radius:
                    intense = math.exp(-0.5 * (math.sqrt(d_sq) / (radius * 0.45)) ** 2)
                    tx = ix + dx
                    ty = iy + dy
                    if 0 <= tx < WIDTH and 0 <= ty < HEIGHT:
                        pidx = (ty * WIDTH + tx) * 3
                        buf[pidx] = min(255, buf[pidx] + int(220 * intense * depth_b))
                        buf[pidx + 1] = min(255, buf[pidx + 1] + int(240 * intense * depth_b))
                        buf[pidx + 2] = min(255, buf[pidx + 2] + int(255 * intense * depth_b))
                        
    out_path = os.path.join(os.path.dirname(__file__), "study_028_draft_b_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT B] Generated Spin Network plate: {out_path}")

def render_draft_b_audio():
    sample_rate = 48000
    duration = 15.0
    num_samples = int(sample_rate * duration)
    left = []
    right = []
    
    # Area operator spectrum base frequency
    f_base = 72.0
    spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    freqs = [f_base * math.sqrt(j * (j + 1.0)) for j in spins]
    
    for i in range(num_samples):
        t = i / sample_rate
        env = min(1.0, t / 1.5) * min(1.0, (duration - t) / 2.0)
        
        # Left channel: discrete area spectrum drone ladder
        sig_l = 0.0
        for idx, f in enumerate(freqs):
            # Dynamic weighting across ladder
            breath = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.15 * t + idx * 0.8)
            amp = (0.28 / (idx + 1.0)) * breath
            sig_l += amp * math.sin(2.0 * math.pi * f * t)
            
        # Right channel: Intertwiner volume micro-pulses
        # Granular quantum area punctures (sparse high-frequency Poisson clicks)
        sig_r = 0.0
        # Pseudo-random pulse generator
        pulse_phase = (t * 8.0) % 1.0
        if pulse_phase < 0.04:
            click = math.sin(2.0 * math.pi * 2880.0 * (t % 0.02)) * math.exp(-pulse_phase * 60.0)
            sig_r += 0.22 * click
            
        # Background fundamental volume mode (36.0 Hz sub-bass)
        sig_r += 0.25 * math.sin(2.0 * math.pi * 36.0 * t)
        
        # Cross coupling
        s_left = env * (sig_l * 0.85 + sig_r * 0.15)
        s_right = env * (sig_r * 0.85 + sig_l * 0.15)
        
        left.append(s_left)
        right.append(s_right)
        
    out_audio = os.path.join(os.path.dirname(__file__), "study_028_draft_b_audio.wav")
    write_wav(out_audio, left, right, sample_rate)
    print(f"[DRAFT B] Generated Spin Network Acoustic study: {out_audio}")

if __name__ == "__main__":
    render_draft_b_plate()
    render_draft_b_audio()

