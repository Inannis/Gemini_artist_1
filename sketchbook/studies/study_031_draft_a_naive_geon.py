#!/usr/bin/env python3
"""
STUDY 031 · DRAFT A: NAIVE GEON & TOROIDAL ELECTROMAGNETIC BUNDLE
Studio Anamnesis · Series XXXVII (Topological Geometrodynamics)
Anti-One-Shot Discipline: Baseline Naive Transcription

This script renders a naive geometric approximation of a Wheeler geon:
a flat Euclidean torus with concentric electromagnetic rings and radial field lines.
It deliberately lacks:
- Genuine non-trivial spatial topology (wormhole throat connecting two sheets)
- Source-free flux trapping through a non-contractible 2-cycle
- Metric curvature backreaction (G_mu_nu = 8pi T_mu_nu)
- Planck-scale quantum metric foam fluctuations (Delta g ~ 1)
"""

import math
import os
import sys

# Studio zero-dependency tool imports
STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png

WIDTH = 800
HEIGHT = 450

def render_draft_a():
    buf = bytearray(WIDTH * HEIGHT * 3)
    
    # Background: flat obsidian void
    bg_r, bg_g, bg_b = 6, 8, 14
    for i in range(0, len(buf), 3):
        buf[i] = bg_r
        buf[i+1] = bg_g
        buf[i+2] = bg_b
        
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    r_major = 160.0
    r_minor = 55.0
    
    # 1. Draw flat concentric toroidal rings
    num_rings = 24
    for ring in range(num_rings):
        rad = r_minor * (ring + 1) / float(num_rings)
        alpha = (ring + 1) / float(num_rings)
        
        # Ring color: naive gold-cyan gradient
        cr = int(212 * alpha + 40 * (1 - alpha))
        cg = int(175 * alpha + 180 * (1 - alpha))
        cb = int(55 * alpha + 220 * (1 - alpha))
        
        # Sample circle points around major radius
        num_theta = 720
        for t_idx in range(num_theta):
            theta = 2.0 * math.pi * t_idx / num_theta
            
            # Torus coordinates with isometric tilt
            torus_center_x = cx + r_major * math.cos(theta)
            torus_center_y = cy + (r_major * math.sin(theta)) * 0.45
            
            # Cross section
            num_phi = 32
            for p_idx in range(num_phi):
                phi = 2.0 * math.pi * p_idx / num_phi
                px = int(torus_center_x + rad * math.cos(phi) * 0.8)
                py = int(torus_center_y + rad * math.sin(phi))
                
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    idx = (py * WIDTH + px) * 3
                    # Additive blend
                    buf[idx] = min(255, buf[idx] + (cr // 6))
                    buf[idx+1] = min(255, buf[idx+1] + (cg // 6))
                    buf[idx+2] = min(255, buf[idx+2] + (cb // 6))
                    
    # 2. Draw naive radial field lines
    for angle_deg in range(0, 360, 15):
        rad_angle = math.radians(angle_deg)
        for dist in range(40, 260, 2):
            fx = int(cx + dist * math.cos(rad_angle))
            fy = int(cy + (dist * math.sin(rad_angle)) * 0.45)
            if 0 <= fx < WIDTH and 0 <= fy < HEIGHT:
                idx = (fy * WIDTH + fx) * 3
                buf[idx] = min(255, buf[idx] + 30)
                buf[idx+1] = min(255, buf[idx+1] + 45)
                buf[idx+2] = min(255, buf[idx+2] + 70)
                
    output_path = os.path.join(os.path.dirname(__file__), "study_031_draft_a_plate.png")
    write_png(output_path, WIDTH, HEIGHT, buf, has_alpha=False)
    print(f"[+] Draft A Plate written to: {output_path}")

if __name__ == "__main__":
    render_draft_a()
