#!/usr/bin/env python3
"""
STUDY 027 · DRAFT C (MATURE SYNTHESIS)
Series XXXIII: The Holographic Matrix & Bulk-Boundary Dualities
Poincaré hyperbolic foliation, Ryu-Takayanagi entanglement phase transitions,
MERA tensor network radial RG flow, and 30s 48kHz dual-register acoustic synthesis.
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1920
HEIGHT = 1080

def render_draft_c_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    disk_radius = 480.0
    
    # Precompute two families of geodesics:
    # 1. Connected phase Ryu-Takayanagi minimal surfaces across boundary intervals
    # 2. Radial MERA tensor network filaments connecting boundary UV to bulk IR
    
    # 64 boundary intervals with mutual information phase transition dynamics
    connected_arcs = []
    disconnected_arcs = []
    
    # Define disjoint intervals A and B
    # A = [-pi/3, -pi/12], B = [pi/12, pi/3]
    # Separation is 2 * pi/12 = pi/6 = 30 deg (~ critical angle theta_c)
    num_subdivisions = 48
    for i in range(num_subdivisions):
        # Sweeping intervals around perimeter
        th1 = 2.0 * math.pi * i / num_subdivisions
        for d_step in [2, 5, 8, 14, 20]:
            th2 = 2.0 * math.pi * ((i + d_step) % num_subdivisions) / num_subdivisions
            d_th = abs(th2 - th1)
            if d_th > math.pi:
                d_th = 2.0 * math.pi - d_th
            if d_th < 0.05 or abs(d_th - math.pi) < 0.05:
                continue
            
            cos_half = math.cos(d_th / 2.0)
            if abs(cos_half) < 1e-4:
                continue
            
            th_mid = (th1 + th2) / 2.0
            if abs(th2 - th1) > math.pi:
                th_mid += math.pi
                
            d_center = 1.0 / cos_half
            r_arc = math.tan(d_th / 2.0)
            
            arc_cx = cx + d_center * disk_radius * math.cos(th_mid)
            arc_cy = cy + d_center * disk_radius * math.sin(th_mid)
            arc_r_px = r_arc * disk_radius
            r_min = math.tan((math.pi - d_th) / 4.0)
            
            connected_arcs.append((arc_cx, arc_cy, arc_r_px, r_min, d_th))
            
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3
            
            # Sub-cosmic boundary handling
            if dist > disk_radius + 12.0:
                # Exterior ambient field: subtle holographic interference fringe
                ang = math.atan2(dy, dx)
                fringe = 0.5 + 0.5 * math.cos(ang * 16.0 + dist * 0.04)
                buf[idx] = int(4 + 6 * fringe)
                buf[idx + 1] = int(5 + 8 * fringe)
                buf[idx + 2] = int(10 + 16 * fringe)
                continue
            elif dist > disk_radius - 3.0:
                # Conformal boundary circle: intense iridescent cyan-white
                ang = math.atan2(dy, dx)
                cft_energy = 0.5 + 0.5 * math.sin(ang * 24.0) * math.cos(ang * 6.0)
                buf[idx] = int(180 + 70 * cft_energy)
                buf[idx + 1] = int(220 + 35 * cft_energy)
                buf[idx + 2] = 255
                continue
                
            norm_r = dist / disk_radius
            ang = math.atan2(dy, dx)
            
            # Hyperbolic depth z = (1 - norm_r) / (1 + norm_r)
            # Center is deep IR (z -> 1, norm_r -> 0), boundary is UV (z -> 0, norm_r -> 1)
            depth_ir = 1.0 - norm_r
            
            # Ambient bulk manifold: deep indigo well with radial gravitational gradient
            r_val = 6 + int(24 * depth_ir + 16 * math.sin(norm_r * 8.0) ** 2)
            g_val = 8 + int(20 * norm_r + 14 * math.cos(ang * 4.0) * depth_ir)
            b_val = 22 + int(65 * depth_ir + 45 * norm_r)
            
            # Hyperbolic distance rings: equal proper distance shells
            hyp_r = 2.0 * math.atanh(min(0.994, norm_r))
            hyp_shell = math.sin(hyp_r * 4.0)
            if abs(hyp_shell) > 0.93:
                r_val = min(255, r_val + 20)
                g_val = min(255, g_val + 28)
                b_val = min(255, b_val + 45)
                
            # Radial MERA tensor network discretization rays (hierarchical tree)
            # Branching at hyp_r thresholds
            level = int(hyp_r * 1.5)
            num_spokes = 8 * (2 ** min(4, level))
            spoke_angle = 2.0 * math.pi / num_spokes
            delta_ang = abs((ang % spoke_angle) - spoke_angle * 0.5)
            if delta_ang < 0.015:
                intense = (0.015 - delta_ang) / 0.015
                r_val = min(255, r_val + int(25 * intense))
                g_val = min(255, g_val + int(40 * intense))
                b_val = min(255, b_val + int(70 * intense))
                
            # Geodesic minimal surfaces
            for arc_cx, arc_cy, arc_r_px, r_min, d_th in connected_arcs:
                d_to_arc = abs(math.hypot(x - arc_cx, y - arc_cy) - arc_r_px)
                if d_to_arc < 1.6:
                    intensity = math.exp(-0.5 * (d_to_arc / 0.7) ** 2)
                    if r_min < 0.25:
                        # Deep minimal surfaces: incandescent golden-amber
                        r_val = int(min(255, r_val + 210 * intensity))
                        g_val = int(min(255, g_val + 165 * intensity))
                        b_val = int(min(255, b_val + 75 * intensity))
                    elif r_min < 0.55:
                        # Intermediate surfaces: emerald-cyan
                        r_val = int(min(255, r_val + 80 * intensity))
                        g_val = int(min(255, g_val + 200 * intensity))
                        b_val = int(min(255, b_val + 210 * intensity))
                    else:
                        # UV boundary boundary-hugging: violet-blue
                        r_val = int(min(255, r_val + 130 * intensity))
                        g_val = int(min(255, g_val + 90 * intensity))
                        b_val = int(min(255, b_val + 245 * intensity))
                        
            buf[idx] = min(255, max(0, r_val))
            buf[idx + 1] = min(255, max(0, g_val))
            buf[idx + 2] = min(255, max(0, b_val))
            
    out_path = os.path.join(os.path.dirname(__file__), "study_027_draft_c_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT C] Generated Mature Synthesis plate (1080p): {out_path}")

def render_draft_c_audio():
    sample_rate = 48000
    duration = 30.0
    num_samples = int(sample_rate * duration)
    left = []
    right = []
    
    # 4-layer spectral stratification
    for i in range(num_samples):
        t = i / sample_rate
        env = min(1.0, t / 3.0) * min(1.0, (duration - t) / 3.0)
        
        # Layer 1: AdS bulk cavity fundamental (43.2 Hz) + golden ratio overtone (69.9 Hz)
        bulk_l1 = 0.32 * math.sin(2.0 * math.pi * 43.2 * t + 0.1 * math.sin(2.0 * math.pi * 0.08 * t))
        bulk_l1 += 0.20 * math.sin(2.0 * math.pi * 69.89 * t)
        
        # Layer 2: Ryu-Takayanagi geodesic tension drones (216 Hz, 324 Hz, 432 Hz)
        # Modulating with periodic geodesic breathing
        breath = 0.5 + 0.5 * math.sin(2.0 * math.pi * 0.12 * t)
        drone = 0.18 * math.sin(2.0 * math.pi * 216.0 * t + breath)
        drone += 0.12 * math.sin(2.0 * math.pi * 324.0 * t)
        drone += 0.08 * math.sin(2.0 * math.pi * 432.0 * t - breath)
        
        # Layer 3: Mutual information phase transition sweep (t in [10s, 22s])
        phase_sig = 0.0
        if 10.0 <= t <= 22.0:
            sweep_p = (t - 10.0) / 12.0
            sweep_env = math.sin(math.pi * sweep_p)
            # Bifurcation sweep: 1280 Hz collapsing to 440 Hz
            f_trans = 1280.0 * (1.0 - 0.65 * sweep_p)
            phase_sig = 0.22 * sweep_env * math.sin(2.0 * math.pi * f_trans * t + 0.5 * math.sin(2.0 * math.pi * 7.5 * t))
            
        # Layer 4: Boundary CFT chiral currents (spatialized left-to-right)
        chirp_left = 0.14 * math.sin(2.0 * math.pi * (2400.0 + 350.0 * math.cos(2.0 * math.pi * 0.3 * t)) * t)
        chirp_right = 0.14 * math.sin(2.0 * math.pi * (2400.0 + 350.0 * math.sin(2.0 * math.pi * 0.3 * t)) * t)
        
        s_left = env * (bulk_l1 * 0.8 + drone * 0.5 + phase_sig * 0.4 + chirp_left * 0.7)
        s_right = env * (bulk_l1 * 0.8 + drone * 0.5 + phase_sig * 0.6 + chirp_right * 0.7)
        
        left.append(s_left)
        right.append(s_right)
        
    out_audio = os.path.join(os.path.dirname(__file__), "study_027_draft_c_audio.wav")
    write_wav(out_audio, left, right, sample_rate)
    print(f"[DRAFT C] Generated Mature Synthesis acoustic study (30s): {out_audio}")

if __name__ == "__main__":
    render_draft_c_plate()
    render_draft_c_audio()
