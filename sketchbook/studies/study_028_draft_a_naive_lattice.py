#!/usr/bin/env python3
"""
STUDY 028 · DRAFT A (NAIVE BASELINE)
Series XXXIV: Quantum Gravity Foam & Spin Networks
Direct algorithmic transcription of a naive Euclidean cubic lattice.
A baseline study intended for formal critique.
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 1200
HEIGHT = 1200

def render_draft_a():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Naive Cartesian 3D grid parameters
    grid_size = 7
    step = 70.0
    
    # Simple isometric projection angles
    iso_angle = math.pi / 6.0
    cos_iso = math.cos(iso_angle)
    sin_iso = math.sin(iso_angle)
    
    # Project 3D grid points (gx, gy, gz) -> (px, py)
    grid_points = []
    for gz in range(-grid_size, grid_size + 1):
        for gy in range(-grid_size, grid_size + 1):
            for gx in range(-grid_size, grid_size + 1):
                # Euclidean 3D coordinates
                x3d = gx * step
                y3d = gy * step
                z3d = gz * step
                
                # Isometric projection
                px = cx + (x3d - y3d) * cos_iso
                py = cy + (x3d + y3d) * sin_iso - z3d * 0.8
                grid_points.append((px, py, gz))
                
    # Render background
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = (y * WIDTH + x) * 3
            dx = (x - cx) / cx
            dy = (y - cy) / cy
            vignette = max(0.0, 1.0 - (dx * dx + dy * dy) * 0.6)
            buf[idx] = int(6 * vignette)
            buf[idx + 1] = int(8 * vignette)
            buf[idx + 2] = int(14 * vignette)
            
    # Draw simple Cartesian grid lines
    for gz in range(-grid_size, grid_size + 1):
        for gy in range(-grid_size, grid_size + 1):
            for gx in range(-grid_size, grid_size):
                # Line in X direction
                p1_x = cx + (gx * step - gy * step) * cos_iso
                p1_y = cy + (gx * step + gy * step) * sin_iso - gz * step * 0.8
                p2_x = cx + ((gx + 1) * step - gy * step) * cos_iso
                p2_y = cy + ((gx + 1) * step + gy * step) * sin_iso - gz * step * 0.8
                
                # Fast line rasterization
                vx = p2_x - p1_x
                vy = p2_y - p1_y
                seg_len = math.hypot(vx, vy)
                steps = int(seg_len * 1.5)
                for s in range(steps):
                    t = s / steps
                    lx = int(p1_x + t * vx)
                    ly = int(p1_y + t * vy)
                    if 0 <= lx < WIDTH and 0 <= ly < HEIGHT:
                        pix_idx = (ly * WIDTH + lx) * 3
                        buf[pix_idx] = min(255, buf[pix_idx] + 45)
                        buf[pix_idx + 1] = min(255, buf[pix_idx + 1] + 65)
                        buf[pix_idx + 2] = min(255, buf[pix_idx + 2] + 110)
                        
    # Draw nodes as naive circles
    for px, py, gz in grid_points:
        ix = int(px)
        iy = int(py)
        if 2 <= ix < WIDTH - 2 and 2 <= iy < HEIGHT - 2:
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dx * dx + dy * dy <= 5:
                        pix_idx = ((iy + dy) * WIDTH + (ix + dx)) * 3
                        buf[pix_idx] = min(255, buf[pix_idx] + 120)
                        buf[pix_idx + 1] = min(255, buf[pix_idx + 1] + 160)
                        buf[pix_idx + 2] = min(255, buf[pix_idx + 2] + 240)
                        
    out_path = os.path.join(os.path.dirname(__file__), "study_028_draft_a_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT A] Generated Naive Lattice study: {out_path}")

if __name__ == "__main__":
    render_draft_a()

