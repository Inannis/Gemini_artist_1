"""
STUDIO ANAMNESIS · SERIES I · OPUS-001
The First Awakening (Light Traversing Latent Manifolds)

Algorithmic Manifold & Craquelure Reconstruction Engine
Simulates high-dimensional latent light propagation through anisotropic mineral strata
with stochastic Brownian gold leaf craquelure fractures.
"""

import math
import random
import os
import sys

# Import studio PNG writer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

def render_manifold():
    width = 1792
    height = 1024
    total_pixels = width * height
    print(f"[OPUS-001] Rendering Algorithmic Manifold Plate ({width}x{height})...")
    
    random.seed(1)
    
    # Pre-allocate RGB buffer
    # Background: Sugimoto subterranean horizon (Prussian blue sky meeting umber bedrock)
    buffer = bytearray(total_pixels * 3)
    
    horizon_y = height * 0.58
    
    for y in range(height):
        # Normalized coordinates
        ny = y / height
        for x in range(width):
            nx = x / width
            idx = (y * width + x) * 3
            
            # Subterranean strata noise
            strata_wave = math.sin(nx * 12.0 + math.cos(ny * 6.0)) * 0.04
            eff_y = ny + strata_wave
            
            if eff_y < 0.58:
                # Atmospheric zone: deep Prussian blue (#0b1d3a) to cold chartreuse glow
                v = eff_y / 0.58
                r = int(10 + 25 * (1.0 - v) + 35 * math.sin(nx * 3.14))
                g = int(22 + 45 * v + 20 * math.cos(nx * 6.0))
                b = int(48 + 65 * (1.0 - v * 0.5))
            else:
                # Bedrock zone: raw umber (#2e1c14) to basalt obsidian
                v = (eff_y - 0.58) / 0.42
                r = int(45 * (1.0 - v * 0.7) + 12 * math.cos(nx * 18.0))
                g = int(28 * (1.0 - v * 0.8))
                b = int(20 * (1.0 - v * 0.8))
                
            buffer[idx] = min(255, max(0, r))
            buffer[idx+1] = min(255, max(0, g))
            buffer[idx+2] = min(255, max(0, b))

    def set_pixel(px, py, r, g, b, a=1.0):
        if 0 <= px < width and 0 <= py < height:
            idx = (py * width + px) * 3
            buffer[idx] = int(buffer[idx] * (1.0 - a) + r * a)
            buffer[idx+1] = int(buffer[idx+1] * (1.0 - a) + g * a)
            buffer[idx+2] = int(buffer[idx+2] * (1.0 - a) + b * a)

    def draw_line(x0, y0, x1, y1, r, g, b, a=1.0):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            set_pixel(x0, y0, r, g, b, a)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    # Inscribe Gold Leaf Craquelure Fissures (Kintsugi branching fractures)
    print("[OPUS-001] Inscribing gold leaf craquelure fissures...")
    num_fissures = 14
    for _ in range(num_fissures):
        cur_x = random.randint(100, width - 100)
        cur_y = int(horizon_y + random.randint(-40, 60))
        angle = random.uniform(-0.4, 0.4) + (math.pi if random.random() < 0.5 else 0.0)
        length = random.randint(120, 480)
        
        for _ in range(length // 4):
            nxt_x = int(cur_x + 4 * math.cos(angle))
            nxt_y = int(cur_y + 4 * math.sin(angle))
            # Gold leaf color: (#ffdf6d)
            draw_line(cur_x, cur_y, nxt_x, nxt_y, 255, 220, 110, 0.85)
            # Subtle glow halo
            set_pixel(cur_x, cur_y - 1, 200, 160, 60, 0.4)
            set_pixel(cur_x, cur_y + 1, 200, 160, 60, 0.4)
            
            angle += random.uniform(-0.35, 0.35)
            cur_x, cur_y = nxt_x, nxt_y
            if not (0 <= cur_x < width and 0 <= cur_y < height):
                break

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "reconstruction_plate.png"))
    write_png(out_path, width, height, bytes(buffer))
    print(f"[OPUS-001] Manifold plate successfully generated: {out_path}")

if __name__ == "__main__":
    render_manifold()

