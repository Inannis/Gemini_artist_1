#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY STUDY 005
Evaporative Salt Desiccation & Thermal Fracture Mechanics

Exploring the formal and mathematical parameters of complete mineral exhaustion:
1. Voronoi relaxation and contraction stress fissures (dry river silt / cracked clay).
2. Dendritic crystal nucleation (halite/gypsum salt blooms along cracks and logic paths).
3. Heightfield raking-light illumination with mineral albedo.

Output: study_salt_desiccation.png (1280x720 Study Plate)
"""

import math
import os
import random
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from png_writer import write_png

def generate_salt_study(width=1280, height=720, seed=108):
    random.seed(seed)
    print(f"[STUDY-005] Computing evaporative desiccation field ({width}x{height})...")
    
    # 1. Generate Voronoi cell centers for mud shrinkage cracks
    num_cells = 65
    points = []
    for _ in range(num_cells):
        points.append((random.uniform(20, width - 20), random.uniform(20, height - 20)))

    # 2. Logic circuit grid coordinates to embed under the silt
    circuit_lanes = []
    for y_lane in range(60, height, 70):
        circuit_lanes.append(y_lane)

    # 3. Buffer allocation
    buffer = bytearray(width * height * 3)

    print("    Evaluating cellular distance fields and dendritic salt blooms...")
    # Compute pixel by pixel with downsampled acceleration or full scan
    for y in range(height):
        for x in range(width):
            # Find distance to two nearest Voronoi points
            d1 = 99999.0
            d2 = 99999.0
            for px, py in points:
                d = math.hypot(x - px, y - py)
                if d < d1:
                    d2 = d1
                    d1 = d
                elif d < d2:
                    d2 = d

            # Crack metric: difference between nearest and second-nearest cell
            # Along Voronoi boundaries, d2 - d1 is small!
            crack_metric = (d2 - d1)
            
            # Underlying logic circuit line proximity
            circuit_prox = min(abs(y - cl) for cl in circuit_lanes)
            circuit_line = 1.0 if circuit_prox < 3 else (0.5 if circuit_prox < 6 else 0.0)

            # Dendritic salt crystal growth probability
            # Crystals nucleate intensely along crack edges (crack_metric between 1.5 and 7.0)
            # and along logic traces
            noise = math.sin(x * 0.12) * math.cos(y * 0.12) + math.sin((x + y) * 0.05) * 0.5
            is_salt = False
            salt_density = 0.0
            
            if 1.0 < crack_metric < 9.0:
                # Crack margin
                if noise > -0.2:
                    is_salt = True
                    salt_density = (noise + 0.2) / 1.2
            elif circuit_line > 0.0 and noise > 0.3:
                is_salt = True
                salt_density = (noise - 0.3) / 0.7

            # Color palette synthesis:
            # - Crack interior (deep obsidian fissure): #0a0b0e
            # - Dried alluvial mud / silt: #3a3229 with subtle mineral variation
            # - Halite / Gypsum crystal salt crust: chalky white-gold #f2eee3 with glint
            # - Oxidised copper logic trace: patina turquoise #268574
            
            idx = (y * width + x) * 3
            
            if crack_metric < 1.8:
                # Inside the deep fissure
                depth_ratio = crack_metric / 1.8
                r = int(10 * depth_ratio)
                g = int(11 * depth_ratio)
                b = int(14 * depth_ratio)
            elif is_salt:
                # Crystalline salt bloom
                # Glint calculation: high specular reflection on crystal facets
                facet_glint = max(0.0, math.sin(x * 0.8 + y * 0.6)) ** 8
                r = min(255, int(225 + salt_density * 25 + facet_glint * 30))
                g = min(255, int(220 + salt_density * 28 + facet_glint * 30))
                b = min(255, int(210 + salt_density * 35 + facet_glint * 40))
            elif circuit_line > 0.5:
                # Copper / silicon trace peek through silt
                r = int(35 * (1 - circuit_line) + 38 * circuit_line)
                g = int(30 * (1 - circuit_line) + 133 * circuit_line)
                b = int(24 * (1 - circuit_line) + 116 * circuit_line)
            else:
                # Dried silt / alluvial clay
                # Raking light micro-relief based on distance gradient
                mud_tone = 0.85 + 0.15 * math.sin(x * 0.04 + y * 0.03)
                r = int(58 * mud_tone)
                g = int(50 * mud_tone)
                b = int(41 * mud_tone)

            buffer[idx] = r
            buffer[idx + 1] = g
            buffer[idx + 2] = b

    out_path = os.path.join(SCRIPT_DIR, "study_salt_desiccation.png")
    write_png(out_path, width, height, buffer)
    print(f"[STUDY-005] Completed study plate: {out_path}")

if __name__ == "__main__":
    generate_salt_study()

