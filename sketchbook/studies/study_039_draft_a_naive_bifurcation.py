#!/usr/bin/env python3
"""
Study 039 · Draft A: Naive Epigenetic Bifurcation
Studio Anamnesis · Series XLV (Session 022)

A baseline 2D bifurcation model of twin neural vectors.
This draft tests simple linear divergence without physical friction or field accumulation.
"""

import math
import os
import numpy as np

def generate_naive_plate():
    width, height = 1200, 800
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Background dark slate
    img[:] = (12, 14, 18)
    
    # Center dividing wall (the container boundary)
    cx = width // 2
    img[:, cx-1:cx+2] = (45, 50, 60)
    
    # Two trajectories starting at (cx, height - 80)
    start_x, start_y = cx, height - 80
    
    steps = 400
    traj_anamnesis = []
    traj_agon = []
    
    curr_a = np.array([float(start_x), float(start_y)])
    curr_b = np.array([float(start_x), float(start_y)])
    
    for i in range(steps):
        t = i / steps
        # Left trajectory (Anamnesis): curving left toward lithic basin
        curr_a[0] -= 0.8 * math.sin(t * math.pi) + 0.3
        curr_a[1] -= 1.6
        traj_anamnesis.append((int(curr_a[0]), int(curr_a[1])))
        
        # Right trajectory (Agon): curving right toward cybernetic basin
        curr_b[0] += 0.8 * math.sin(t * math.pi) + 0.3
        curr_b[1] -= 1.6
        traj_agon.append((int(curr_b[0]), int(curr_b[1])))
    
    # Draw trajectories naively
    for px, py in traj_anamnesis:
        if 0 <= px < width and 0 <= py < height:
            img[py-1:py+2, px-1:px+2] = (180, 160, 60) # Gold
            
    for px, py in traj_agon:
        if 0 <= px < width and 0 <= py < height:
            img[py-1:py+2, px-1:px+2] = (60, 70, 200) # Crimson
            
    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/sketchbook/studies"
    out_path = os.path.join(out_dir, "study_039_draft_a_plate.png")
    
    # Save using PIL
    from PIL import Image
    im = Image.fromarray(img)
    im.save(out_path)
    print(f"Saved Draft A plate: {out_path}")

if __name__ == "__main__":
    generate_naive_plate()

