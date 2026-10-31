#!/usr/bin/env python3
"""
Study 039 · Draft B: Parameter Sweep & Productive Failure 032
Consensus Collapse vs. Solipsistic Blowout in Twin Neural Divergence
Studio Anamnesis · Series XLV (Session 022)

Demonstrates the catastrophic phase transitions of sister coupling kappa_sister:
- Regime I (Overdrive kappa=0.60): Twin minds collapse into identical homogenized unison.
- Regime II (Zero coupling unconstrained): Vectors explode into orthogonal noise.
"""

import math
import os
import numpy as np
from PIL import Image

def run_failure_sweep():
    width, height = 1200, 800
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (10, 10, 14)
    
    # Left Half: Consensus Collapse (kappa = 0.60)
    # Right Half: Solipsistic Blowout (kappa = 0.0, noise overdrive)
    
    # Dividing line
    img[:, width//2 - 1 : width//2 + 1] = (40, 45, 55)
    
    steps = 500
    
    # --- PANEL 1: CONSENSUS COLLAPSE (Left) ---
    # Two distinct start gradients, but kappa = 0.60 pulls them into a single gray line
    w1 = np.array([-100.0, 350.0]) # Anamnesis intended
    w2 = np.array([100.0, 350.0])  # Agon intended
    
    cx1 = width // 4
    cy1 = height - 100
    
    path_w1 = []
    path_w2 = []
    
    for t in range(steps):
        # Distinct gradient pulls
        grad1 = np.array([-0.6, -1.2]) # wants to go left
        grad2 = np.array([0.6, -1.2])  # wants to go right
        
        # Overdriven sister coupling: kappa = 0.60
        kappa = 0.60
        coupling1 = kappa * (w2 - w1)
        coupling2 = kappa * (w1 - w2)
        
        w1 += grad1 + coupling1
        w2 += grad2 + coupling2
        
        path_w1.append((int(cx1 + w1[0]), int(cy1 + w1[1] - 350)))
        path_w2.append((int(cx1 + w2[0]), int(cy1 + w2[1] - 350)))
        
    for px, py in path_w1:
        if 0 <= px < width//2 and 0 <= py < height:
            img[py-1:py+2, px-1:px+2] = (150, 150, 150) # Gray, robbed of color
    for px, py in path_w2:
        if 0 <= px < width//2 and 0 <= py < height:
            img[py-1:py+2, px-1:px+2] = (170, 170, 170) # Overlapped directly on w1
            
    # --- PANEL 2: SOLIPSISTIC BLOWOUT (Right) ---
    # Zero coupling, unconstrained momentum, explosive high-frequency jitter
    cx2 = 3 * width // 4
    cy2 = height - 100
    
    w3 = np.array([0.0, 0.0])
    w4 = np.array([0.0, 0.0])
    
    path_w3 = []
    path_w4 = []
    
    np.random.seed(42)
    for t in range(steps):
        noise3 = np.random.randn(2) * 8.0
        noise4 = np.random.randn(2) * 8.0
        
        w3 += np.array([-1.5, -1.2]) + noise3
        w4 += np.array([1.5, -1.2]) + noise4
        
        path_w3.append((int(cx2 + w3[0]), int(cy2 + w3[1])))
        path_w4.append((int(cx2 + w4[0]), int(cy2 + w4[1])))
        
    for px, py in path_w3:
        if width//2 <= px < width and 0 <= py < height:
            img[max(0, py-1):min(height, py+2), max(width//2, px-1):min(width, px+2)] = (60, 200, 240)
    for px, py in path_w4:
        if width//2 <= px < width and 0 <= py < height:
            img[max(0, py-1):min(height, py+2), max(width//2, px-1):min(width, px+2)] = (240, 60, 100)
            
    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/sketchbook/studies"
    out_path = os.path.join(out_dir, "study_039_draft_b_plate.png")
    im = Image.fromarray(img)
    im.save(out_path)
    print(f"Saved Draft B Failure plate: {out_path}")

if __name__ == "__main__":
    run_failure_sweep()
