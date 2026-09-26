#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 030 · DRAFT A: NAIVE EUCLIDEAN TRIANGULATION
Series XXXVI (Causal Dynamical Triangulations & Spacetime Emergence)

Draft A: Naive baseline.
Generates an unfoliated, random Euclidean 2D simplicial mesh without
time slices or Lorentzian causal structure. Demonstrates the static,
sterile quality of Euclidean quantum gravity before the introduction of causality.

Zero external dependencies (pure standard Python 3).
"""

import math
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

WIDTH = 1200
HEIGHT = 1200

def generate_draft_a():
    random.seed(42)
    buffer = bytearray(WIDTH * HEIGHT * 3)

    # Dark charcoal background
    for i in range(0, len(buffer), 3):
        buffer[i] = 12
        buffer[i+1] = 14
        buffer[i+2] = 20

    # Generate 150 random vertices in unit square
    num_pts = 160
    points = []
    margin = 80
    for _ in range(num_pts):
        px = margin + random.random() * (WIDTH - 2 * margin)
        py = margin + random.random() * (HEIGHT - 2 * margin)
        points.append((px, py))

    # Connect proximate points (naive Euclidean triangulation approximation)
    edges = set()
    max_dist = 140.0
    for i in range(num_pts):
        p1 = points[i]
        dists = []
        for j in range(num_pts):
            if i == j:
                continue
            p2 = points[j]
            d = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
            if d < max_dist:
                dists.append((d, j))
        dists.sort()
        for d, j in dists[:4]: # connect to 4 nearest
            edge = tuple(sorted((i, j)))
            edges.add(edge)

    # Rasterize lines (Bresenham)
    def draw_line(x0, y0, x1, y1, r, g, b):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                idx = (y0 * WIDTH + x0) * 3
                buffer[idx] = min(255, buffer[idx] + r)
                buffer[idx+1] = min(255, buffer[idx+1] + g)
                buffer[idx+2] = min(255, buffer[idx+2] + b)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    # Draw triangular edges
    for i, j in edges:
        p1, p2 = points[i], points[j]
        draw_line(p1[0], p1[1], p2[0], p2[1], 80, 140, 180)

    # Draw vertices
    for px, py in points:
        ix, iy = int(px), int(py)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx*dx + dy*dy <= 4:
                    qx, qy = ix + dx, iy + dy
                    if 0 <= qx < WIDTH and 0 <= qy < HEIGHT:
                        idx = (qy * WIDTH + qx) * 3
                        buffer[idx] = 220
                        buffer[idx+1] = 230
                        buffer[idx+2] = 240

    out_path = os.path.join(os.path.dirname(__file__), "study_030_draft_a_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buffer)
    print(f"[✓] Study 030 Draft A generated: {out_path} ({len(points)} vertices, {len(edges)} edges)")

if __name__ == "__main__":
    generate_draft_a()

