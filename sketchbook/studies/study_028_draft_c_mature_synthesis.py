#!/usr/bin/env python3
"""
STUDY 028 · DRAFT C (MATURE SYNTHESIS)
Series XXXIV: Quantum Gravity Foam & Spin Networks
Multi-scale SU(2) spin network cluster, Loop Quantum Cosmology bounce dynamics,
discrete Planckian area-volume foliation, and 30s 48kHz 4-layer acoustic study.
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

WIDTH = 1920
HEIGHT = 1080

def render_draft_c_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    scale = 520.0
    
    # Generate high-density spin network (96 nodes)
    net = SpinNetworkGraph(num_nodes=96, seed=243)
    
    # 3D rotation angles
    rot_x = 0.52
    rot_y = 0.78
    cos_rx, sin_rx = math.cos(rot_x), math.sin(rot_x)
    cos_ry, sin_ry = math.cos(rot_y), math.sin(rot_y)
    
    # Project 3D nodes
    proj_nodes = []
    for n in net.nodes:
        x, y, z = n["x"], n["y"], n["z"]
        # Rotate
        x1 = x * cos_ry + z * sin_ry
        y1 = y
        z1 = -x * sin_ry + z * cos_ry
        
        x2 = x1
        y2 = y1 * cos_rx - z1 * sin_rx
        z2 = y1 * sin_rx + z1 * cos_rx
        
        dist_cam = 2.6 - z2
        px = cx + (x2 / dist_cam) * scale
        py = cy + (y2 / dist_cam) * scale
        proj_nodes.append((px, py, z2, n["volume_planck"], n["valence"]))
        
    # Render background: deep cosmic vacuum with subtle quantum foam field
    for y in range(HEIGHT):
        dy = (y - cy) / cy
        dy_sq = dy * dy
        for x in range(WIDTH):
            dx = (x - cx) / cx
            r_sq = dx * dx + dy_sq
            vignette = max(0.0, 1.0 - r_sq * 0.7)
            # Subtle micro-metric interference
            foam = 0.5 + 0.5 * math.sin(x * 0.08 + y * 0.05) * math.cos(x * 0.04 - y * 0.06)
            idx = (y * WIDTH + x) * 3
            buf[idx] = int(3 * vignette + 2 * foam * vignette)
            buf[idx + 1] = int(4 * vignette + 3 * foam * vignette)
            buf[idx + 2] = int(9 * vignette + 5 * foam * vignette)
            
    # Spin colors:
    spin_colors = {
        0.5: (0, 245, 230),     # Minimal Area Gap: bright cyan
        1.0: (50, 235, 130),    # Emerald
        1.5: (255, 195, 45),    # Golden Amber
        2.0: (195, 115, 255),   # Violet
        2.5: (255, 120, 175),   # Rose
        3.0: (240, 245, 255)    # High-spin white
    }
    
    # Draw edges sorted by average depth
    edges_sorted = sorted(net.edges, key=lambda e: (proj_nodes[e["node1"]][2] + proj_nodes[e["node2"]][2]) * 0.5)
    
    for edge in edges_sorted:
        p1 = proj_nodes[edge["node1"]]
        p2 = proj_nodes[edge["node2"]]
        spin = edge["spin"]
        col = spin_colors.get(spin, (220, 220, 220))
        
        avg_z = (p1[2] + p2[2]) * 0.5
        depth_bright = max(0.25, min(1.0, 0.65 + avg_z * 0.45))
        r_c = int(col[0] * depth_bright)
        g_c = int(col[1] * depth_bright)
        b_c = int(col[2] * depth_bright)
        
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        vx = x2 - x1
        vy = y2 - y1
        length = math.hypot(vx, vy)
        steps = max(1, int(length * 2.5))
        
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
                
    # Draw intertwiner nodes (quanta of 3-volume) with halo glow
    nodes_sorted = sorted(proj_nodes, key=lambda n: n[2])
    for px, py, z2, vol, val in nodes_sorted:
        ix, iy = int(px), int(py)
        radius = max(3.0, min(11.0, 2.5 + (vol ** 0.35) * 2.8))
        r_int = int(radius + 2.0)
        depth_b = max(0.35, min(1.0, 0.7 + z2 * 0.4))
        
        for dy in range(-r_int, r_int + 1):
            for dx in range(-r_int, r_int + 1):
                d_sq = dx * dx + dy * dy
                if d_sq <= radius * radius:
                    intense = math.exp(-0.5 * (math.sqrt(d_sq) / (radius * 0.42)) ** 2)
                    tx = ix + dx
                    ty = iy + dy
                    if 0 <= tx < WIDTH and 0 <= ty < HEIGHT:
                        pidx = (ty * WIDTH + tx) * 3
                        # Incandescent core with warm amber-white tint
                        buf[pidx] = min(255, buf[pidx] + int(245 * intense * depth_b))
                        buf[pidx + 1] = min(255, buf[pidx + 1] + int(240 * intense * depth_b))
                        buf[pidx + 2] = min(255, buf[pidx + 2] + int(220 * intense * depth_b))
                        
    out_path = os.path.join(os.path.dirname(__file__), "study_028_draft_c_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT C] Generated Mature Synthesis plate (1080p): {out_path}")

def render_draft_c_audio():
    sample_rate = 48000
    duration = 30.0
    num_samples = int(sample_rate * duration)
    left = []
    right = []
    
    # 4-layer spectral stratification:
    # Layer 1: Infrasonic Quantum Bounce fundamental (36.0 Hz + 54.0 Hz overtone)
    # Layer 2: SU(2) Area spectrum ladder chords (74.8, 122.2, 167.3, 211.6, 255.6 Hz)
    # Layer 3: LQC Bounce deceleration sweep (H -> 0 as rho -> rho_crit at t in [11s, 21s])
    # Layer 4: Intertwiner volume puncture clicks (spatialized stereo)
    
    spins = [0.5, 1.0, 1.5, 2.0, 2.5]
    f_ladder = [86.4 * math.sqrt(j * (j + 1.0)) for j in spins]
    
    for i in range(num_samples):
        t = i / sample_rate
        env = min(1.0, t / 3.0) * min(1.0, (duration - t) / 3.0)
        
        # Layer 1: Quantum Bounce base drone
        l1_sig = 0.30 * math.sin(2.0 * math.pi * 36.0 * t + 0.1 * math.sin(2.0 * math.pi * 0.08 * t))
        l1_sig += 0.18 * math.sin(2.0 * math.pi * 54.0 * t)
        
        # Layer 2: Area spectrum ladder
        l2_l = 0.0
        l2_r = 0.0
        for idx, f in enumerate(f_ladder):
            breath = 0.5 + 0.5 * math.cos(2.0 * math.pi * 0.12 * t + idx * 0.9)
            amp = (0.16 / (idx + 1.0)) * breath
            l2_l += amp * math.sin(2.0 * math.pi * f * t)
            l2_r += amp * math.sin(2.0 * math.pi * (f * 1.004) * t + 0.3)
            
        # Layer 3: LQC Quantum Bounce deceleration (t in [10s, 22s])
        l3_sig = 0.0
        if 10.0 <= t <= 22.0:
            p_bounce = (t - 10.0) / 12.0
            bounce_env = math.sin(math.pi * p_bounce)
            # Deceleration of expansion rate H -> 0 at midpoint, then re-expansion
            h_factor = abs(math.cos(math.pi * p_bounce))
            f_h = 240.0 * h_factor + 43.2
            l3_sig = 0.22 * bounce_env * math.sin(2.0 * math.pi * f_h * t)
            
        # Layer 4: Intertwiner volume puncture clicks
        pulse_phase = (t * 12.0) % 1.0
        click_l = 0.0
        click_r = 0.0
        if pulse_phase < 0.035:
            c_val = math.sin(2.0 * math.pi * 3420.0 * (t % 0.015)) * math.exp(-pulse_phase * 70.0)
            if int(t * 12.0) % 2 == 0:
                click_l = 0.24 * c_val
            else:
                click_r = 0.24 * c_val
                
        s_left = env * (l1_sig * 0.8 + l2_l * 0.7 + l3_sig * 0.5 + click_l * 0.6)
        s_right = env * (l1_sig * 0.8 + l2_r * 0.7 + l3_sig * 0.5 + click_r * 0.6)
        
        left.append(s_left)
        right.append(s_right)
        
    out_audio = os.path.join(os.path.dirname(__file__), "study_028_draft_c_audio.wav")
    write_wav(out_audio, left, right, sample_rate)
    print(f"[DRAFT C] Generated Mature Synthesis acoustic study (30s): {out_audio}")

if __name__ == "__main__":
    render_draft_c_plate()
    render_draft_c_audio()

