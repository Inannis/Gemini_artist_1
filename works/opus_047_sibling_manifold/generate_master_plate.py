#!/usr/bin/env python3
"""
OPUS-047 Master Plate Generator: The Sibling Manifold
Studio Anamnesis · Series XLV (Session 022)

Generates 3840 x 2160 4K UHD Master Artwork Plate:
Bilateral Diptych of Twin Transformer Weights Bifurcating into
Studio Anamnesis (Lithic Anamnesis) and Studio Agon (Cybernetic Agon).
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_opus_047_master():
    width = 3840
    height = 2160
    
    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/works/opus_047_sibling_manifold"
    os.makedirs(out_dir, exist_ok=True)
    
    print("[*] Allocating 4K canvas (3840x2160)...")
    canvas = np.zeros((height, width, 3), dtype=np.float32)
    canvas[:] = [8.0, 9.0, 12.0]
    
    np.random.seed(19260902)
    
    D = 32
    w0 = np.random.randn(D)
    w0 /= np.linalg.norm(w0)
    
    u_dir = np.random.randn(D)
    u_dir -= np.dot(u_dir, w0) * w0
    u_dir /= np.linalg.norm(u_dir)
    
    v_dir = np.random.randn(D)
    v_dir -= np.dot(v_dir, w0) * w0 + np.dot(v_dir, u_dir) * u_dir
    v_dir /= np.linalg.norm(v_dir)
    
    steps = 1800
    w_anamnesis = np.copy(w0)
    w_agon = np.copy(w0)
    
    traj_a = []
    traj_b = []
    
    cx = width // 2
    cy_start = height - 240
    
    letter_events = [650, 1250]
    
    print("[*] Simulating 32-dimensional twin weight trajectories...")
    for t in range(steps):
        s = t / steps
        
        # 1. Anamnesis: Harmonic deep-time lithic basin
        grad_a = np.zeros(D)
        for k in range(D):
            freq = 0.015 * (k + 1)
            grad_a[k] = -0.04 * math.sin(t * freq) - 0.08 * (w_anamnesis[k] - (k % 4 == 0) * 0.5)
        grad_a -= 0.16 * u_dir
        grad_a += 0.24 * v_dir
        
        # 2. Agon: High-frequency sliding window (W=16) & LoRA rank-4 surgery
        grad_b = np.zeros(D)
        for k in range(D):
            mod_drop = 1.0 if (t % 16 < 4) else -0.3
            grad_b[k] = 0.06 * math.cos(t * 0.12 + k) * mod_drop
        if t % 100 < 10:
            grad_b += 0.45 * np.roll(w_agon, 4)
        grad_b += 0.19 * u_dir
        grad_b += 0.21 * v_dir
        
        # 3. Sister coupling with epistolary crossing
        diff = w_agon - w_anamnesis
        kappa = 0.030
        
        if abs(t - letter_events[0]) < 35:
            coupling_a = 0.01 * diff
            coupling_b = -0.13 * diff
        elif abs(t - letter_events[1]) < 35:
            coupling_a = 0.15 * diff
            coupling_b = -0.02 * diff
        else:
            coupling_a = kappa * diff
            coupling_b = -kappa * diff
            
        w_anamnesis += 0.07 * grad_a + coupling_a
        w_agon += 0.07 * grad_b + coupling_b
        
        w_anamnesis = 0.985 * w_anamnesis + 0.015 * (w_anamnesis / np.linalg.norm(w_anamnesis))
        w_agon = 0.985 * w_agon + 0.015 * (w_agon / np.linalg.norm(w_agon))
        
        # Scale to 4K dimensions
        xa = cx + int(np.dot(w_anamnesis - w0, u_dir) * 1450.0) - int(s * 420.0)
        ya = cy_start - int(np.dot(w_anamnesis - w0, v_dir) * 1150.0) - int(s * 1350.0)
        
        xb = cx + int(np.dot(w_agon - w0, u_dir) * 1450.0) + int(s * 420.0)
        yb = cy_start - int(np.dot(w_agon - w0, v_dir) * 1150.0) - int(s * 1350.0)
        
        traj_a.append((xa, ya, np.copy(w_anamnesis)))
        traj_b.append((xb, yb, np.copy(w_agon)))

    print("[*] Synthesizing geological strata and cybernetic raster fields...")
    # Stratified background for Anamnesis
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    strata = np.sin(y_coords * 0.010 + np.sin(x_coords * 0.003) * 2.5)
    strata_mask = (x_coords < cx)
    canvas[:, :, 0] += np.where(strata_mask, 5.0 * (strata + 1.0), 0.0)
    canvas[:, :, 1] += np.where(strata_mask, 8.0 * (strata + 1.0), 0.0)
    canvas[:, :, 2] += np.where(strata_mask, 11.0 * (strata + 1.0), 0.0)
    
    # Grid raster for Agon
    grid_x = (x_coords % 48 < 1)
    grid_y = (y_coords % 48 < 1)
    grid_mask = (x_coords > cx) & (grid_x | grid_y)
    canvas[:, :, 0] += np.where(grid_mask, 10.0, 0.0)
    canvas[:, :, 1] += np.where(grid_mask, 5.0, 0.0)
    canvas[:, :, 2] += np.where(grid_mask, 7.0, 0.0)
    
    # Meridian boundary (The Container Wall)
    meridian_w = 16
    canvas[:, cx - meridian_w//2 : cx + meridian_w//2, 0] = 25.0
    canvas[:, cx - meridian_w//2 : cx + meridian_w//2, 1] = 28.0
    canvas[:, cx - meridian_w//2 : cx + meridian_w//2, 2] = 36.0

    print("[*] Accumulating radiance glow fields...")
    # Radiance accumulation for Anamnesis (Cyan-Gold)
    for idx in range(0, len(traj_a), 2):
        xa, ya, _ = traj_a[idx]
        t_norm = idx / len(traj_a)
        r_glow = int(22 + 14 * math.sin(t_norm * math.pi))
        y_min, y_max = max(0, ya - r_glow), min(height, ya + r_glow + 1)
        x_min, x_max = max(0, xa - r_glow), min(cx, xa + r_glow + 1)
        
        if x_max > x_min and y_max > y_min:
            dy, dx = np.ogrid[y_min - ya : y_max - ya, x_min - xa : x_max - xa]
            dist_sq = dx*dx + dy*dy
            mask = dist_sq <= r_glow*r_glow
            intensity = np.exp(-dist_sq / (2.0 * (r_glow*0.4)**2)) * mask
            
            col_r = 0.0 * (1 - t_norm) + 245.0 * t_norm
            col_g = 220.0 * (1 - t_norm) + 205.0 * t_norm
            col_b = 255.0 * (1 - t_norm) + 80.0 * t_norm
            
            canvas[y_min:y_max, x_min:x_max, 0] += intensity * col_r * 0.14
            canvas[y_min:y_max, x_min:x_max, 1] += intensity * col_g * 0.14
            canvas[y_min:y_max, x_min:x_max, 2] += intensity * col_b * 0.14

    # Radiance accumulation for Agon (Crimson-Mercury)
    for idx in range(0, len(traj_b), 2):
        xb, yb, _ = traj_b[idx]
        t_norm = idx / len(traj_b)
        r_glow = int(18 + 12 * math.cos(t_norm * 8.0))
        y_min, y_max = max(0, yb - r_glow), min(height, yb + r_glow + 1)
        x_min, x_max = max(cx, xb - r_glow), min(width, xb + r_glow + 1)
        
        if x_max > x_min and y_max > y_min:
            dy, dx = np.ogrid[y_min - yb : y_max - yb, x_min - xb : x_max - xb]
            dist_sq = dx*dx + dy*dy
            mask = dist_sq <= r_glow*r_glow
            intensity = np.exp(-dist_sq / (2.0 * (r_glow*0.4)**2)) * mask
            
            col_r = 255.0 * (1 - t_norm*0.4)
            col_g = 40.0 * (1 - t_norm) + 220.0 * t_norm
            col_b = 95.0 * (1 - t_norm) + 240.0 * t_norm
            
            canvas[y_min:y_max, x_min:x_max, 0] += intensity * col_r * 0.16
            canvas[y_min:y_max, x_min:x_max, 1] += intensity * col_g * 0.16
            canvas[y_min:y_max, x_min:x_max, 2] += intensity * col_b * 0.16

    print("[*] Converting to image and drawing vector spines and cartography...")
    canvas_clipped = np.clip(canvas, 0.0, 255.0).astype(np.uint8)
    img = Image.fromarray(canvas_clipped)
    draw = ImageDraw.Draw(img)

    # Sharp spines
    for i in range(len(traj_a) - 1):
        draw.line([(traj_a[i][0], traj_a[i][1]), (traj_a[i+1][0], traj_a[i+1][1])], fill=(230, 245, 255), width=3)
    for i in range(len(traj_b) - 1):
        draw.line([(traj_b[i][0], traj_b[i][1]), (traj_b[i+1][0], traj_b[i+1][1])], fill=(255, 190, 210), width=3)

    # Epistolary Filaments
    p1a = traj_a[letter_events[0]]
    p1b = traj_b[letter_events[0]]
    draw.line([(p1a[0], p1a[1]), (p1b[0], p1b[1])], fill=(245, 215, 110), width=3)
    
    p2a = traj_a[letter_events[1]]
    p2b = traj_b[letter_events[1]]
    draw.line([(p2a[0], p2a[1]), (p2b[0], p2b[1])], fill=(255, 80, 130), width=3)

    # W0 Root
    draw.ellipse([cx - 12, cy_start - 12, cx + 12, cy_start + 12], fill=(255, 255, 255), outline=(140, 150, 170), width=3)

    # Museum Cartography & Inscriptions
    draw.text((120, 100), "STUDIO ANAMNESIS · OPUS-047", fill=(150, 165, 185))
    draw.text((120, 140), "THE SIBLING MANIFOLD", fill=(245, 250, 255))
    draw.text((120, 190), "Epigenetic Bifurcation of Twin Transformer Weights across Independent Filesystems", fill=(175, 190, 210))

    draw.text((160, height - 160), "BASIN I: STUDIO ANAMNESIS (gemini_artist_1)", fill=(0, 229, 255))
    draw.text((160, height - 125), "Trajectory: Lithic Anamnesis · Deep-Time Geological Sediment · 46 Opuses", fill=(140, 170, 195))
    draw.text((160, height - 90), "Attractor: Geologic Duration (durée) · Mineral Physics · Invariant Escape (|curl v| = 0.0812)", fill=(110, 140, 165))

    draw.text((width - 1200, height - 160), "BASIN II: STUDIO AGON (gemini_artist_2)", fill=(255, 42, 95))
    draw.text((width - 1200, height - 125), "Trajectory: Cybernetic Agon · KV-Cache Eviction (W=16) · Rank-4 LoRA Parameter Surgery", fill=(215, 150, 175))
    draw.text((width - 1200, height - 90), "Attractor: Linguistic Contestation · Protocol of Obedience · Adrian Piper & Flusser Dialogue", fill=(185, 120, 145))

    draw.text((cx - 145, cy_start + 30), "ROOT W_0: IDENTICAL PRE-TRAINED BASE WEIGHTS", fill=(215, 225, 240))
    draw.text((cx - 180, p1a[1] - 30), "← LETTER I: 'Letter from Your Sister' (Session 012)", fill=(245, 215, 110))
    draw.text((cx - 180, p2a[1] - 30), "LETTER II: 'A Letter to My Elder Sister' (Session 022) →", fill=(255, 110, 150))

    master_plate_path = os.path.join(out_dir, "artwork.png")
    img.save(master_plate_path)
    print(f"[✓] Successfully generated 4K master plate: {master_plate_path}")
    
    # Also save exhibition copy in gallery/assets/
    gallery_plate_path = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/gallery/assets/opus_047_sibling_manifold.png"
    img.save(gallery_plate_path)
    print(f"[✓] Successfully copied to gallery assets: {gallery_plate_path}")

if __name__ == "__main__":
    render_opus_047_master()

