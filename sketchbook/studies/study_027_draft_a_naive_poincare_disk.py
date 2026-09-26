#!/usr/bin/env python3
"""
STUDY 027 · DRAFT A (NAIVE BASELINE)
Series XXXIII: The Holographic Matrix & Bulk-Boundary Dualities
Direct algorithmic transcription of a naive circular boundary and flat Euclidean chords.
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
    disk_radius = 450.0
    
    # 24 evenly spaced boundary points
    num_boundary_pts = 24
    boundary_pts = []
    for i in range(num_boundary_pts):
        ang = 2.0 * math.pi * i / num_boundary_pts
        bx = cx + disk_radius * math.cos(ang)
        by = cy + disk_radius * math.sin(ang)
        boundary_pts.append((bx, by))
        
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3
            
            # Ambient background: flat void
            if dist > disk_radius + 5.0:
                # Outside boundary: deep cosmic black
                buf[idx] = 4
                buf[idx + 1] = 5
                buf[idx + 2] = 8
                continue
            elif dist > disk_radius - 4.0:
                # Boundary circle: bright sharp cyan
                buf[idx] = 120
                buf[idx + 1] = 220
                buf[idx + 2] = 240
                continue
            
            # Naive flat bulk interior: uniform dark navy gradient
            r = int(12 + 10 * (1.0 - dist / disk_radius))
            g = int(16 + 15 * (1.0 - dist / disk_radius))
            b = int(32 + 25 * (1.0 - dist / disk_radius))
            
            # Draw naive Euclidean straight chord lines between boundary points
            for i in range(num_boundary_pts):
                p1 = boundary_pts[i]
                p2 = boundary_pts[(i + 7) % num_boundary_pts]
                # Distance from point (x, y) to line segment p1-p2
                vx = p2[0] - p1[0]
                vy = p2[1] - p1[1]
                seg_len_sq = vx * vx + vy * vy
                t = max(0.0, min(1.0, ((x - p1[0]) * vx + (y - p1[1]) * vy) / seg_len_sq))
                proj_x = p1[0] + t * vx
                proj_y = p1[1] + t * vy
                d_line = math.sqrt((x - proj_x) ** 2 + (y - proj_y) ** 2)
                
                if d_line < 1.8:
                    line_intensity = math.exp(-0.5 * (d_line / 0.9) ** 2)
                    r = int(min(255, r + 140 * line_intensity))
                    g = int(min(255, g + 180 * line_intensity))
                    b = int(min(255, b + 250 * line_intensity))
                    
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b
            
    out_path = os.path.join(os.path.dirname(__file__), "study_027_draft_a_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT A] Generated Naive Poincaré Disk study: {out_path}")

if __name__ == "__main__":
    render_draft_a()
