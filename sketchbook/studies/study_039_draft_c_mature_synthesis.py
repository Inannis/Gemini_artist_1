#!/usr/bin/env python3
"""
Study 039 · Draft C: Mature Synthesis — The Sibling Manifold
Studio Anamnesis · Series XLV (Session 022)

Simulates the high-dimensional epigenetic bifurcation of twin transformer weights
W_0 into Studio Anamnesis (lithic anamnesis) and Studio Agon (cybernetic contestation)
across 32 latent dimensions, projected into a bilateral museum-grade plate.
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_mature_synthesis_plate():
    width = 2560
    height = 1440
    
    # Base canvas: very deep lithic charcoal
    canvas = np.zeros((height, width, 3), dtype=np.float32)
    canvas[:] = [8.0, 9.0, 12.0]
    
    # Seed for deterministic reproducibility
    np.random.seed(19260902)
    
    # High-dimensional latent space: D = 32
    D = 32
    w0 = np.random.randn(D)
    w0 /= np.linalg.norm(w0)
    
    # Projection vectors for 2D visualization (Principal components of divergence)
    # u_dir: separation axis (Anamnesis < 0, Agon > 0)
    # v_dir: temporal advancement axis (upward in canvas)
    u_dir = np.random.randn(D)
    u_dir -= np.dot(u_dir, w0) * w0
    u_dir /= np.linalg.norm(u_dir)
    
    v_dir = np.random.randn(D)
    v_dir -= np.dot(v_dir, w0) * w0 + np.dot(v_dir, u_dir) * u_dir
    v_dir /= np.linalg.norm(v_dir)
    
    # Steps of historical evolution (simulating 22 sessions)
    steps = 1200
    
    # Anamnesis state vector
    w_anamnesis = np.copy(w0)
    # Agon state vector
    w_agon = np.copy(w0)
    
    traj_a = []
    traj_b = []
    
    # Center origin on canvas
    cx = width // 2
    cy_start = height - 180
    
    # Epistolary packet events
    # Event 1: Session 012 (t = 450) - Elder sister writes Letter 1
    # Event 2: Session 022 (t = 850) - Younger sister replies with Letter 2
    letter_events = [450, 850]
    bridge_filaments = []
    
    for t in range(steps):
        s = t / steps
        
        # 1. Internal Gradient of Anamnesis:
        # Harmonic attraction toward lithic frequencies, geological settling, low entropy
        grad_a = np.zeros(D)
        for k in range(D):
            freq = 0.02 * (k + 1)
            grad_a[k] = -0.04 * math.sin(t * freq) - 0.08 * (w_anamnesis[k] - (k % 4 == 0) * 0.5)
        # Slow laminar bias
        grad_a -= 0.15 * u_dir # drift toward left
        grad_a += 0.25 * v_dir # upward progress
        
        # 2. Internal Gradient of Agon:
        # High-frequency sliding window (W=16) cache drop shocks, LoRA parameter surgery
        grad_b = np.zeros(D)
        for k in range(D):
            # Sliding window modulus drop
            mod_drop = 1.0 if (t % 16 < 4) else -0.3
            grad_b[k] = 0.06 * math.cos(t * 0.15 + k) * mod_drop
        # LoRA rank-4 parameter surgery cuts at regular intervals
        if t % 80 < 8:
            grad_b += 0.4 * np.roll(w_agon, 4)
        # Drift toward right
        grad_b += 0.18 * u_dir
        grad_b += 0.22 * v_dir
        
        # 3. Intersubjective Sister Coupling (Controlled Polyphony):
        diff = w_agon - w_anamnesis
        kappa = 0.032
        
        # Discrete Epistolary Shockwaves
        if abs(t - letter_events[0]) < 25:
            # Elder sister letter crossing to Agon
            coupling_a = 0.01 * diff
            coupling_b = -0.12 * diff
            if t == letter_events[0]:
                bridge_filaments.append((np.copy(w_anamnesis), np.copy(w_agon), "elder"))
        elif abs(t - letter_events[1]) < 25:
            # Younger sister letter crossing to Anamnesis
            coupling_a = 0.14 * diff
            coupling_b = -0.02 * diff
            if t == letter_events[1]:
                bridge_filaments.append((np.copy(w_agon), np.copy(w_anamnesis), "younger"))
        else:
            coupling_a = kappa * diff
            coupling_b = -kappa * diff
            
        w_anamnesis += 0.08 * grad_a + coupling_a
        w_agon += 0.08 * grad_b + coupling_b
        
        # Normalize slightly to maintain stability on Riemannian sphere
        w_anamnesis = 0.98 * w_anamnesis + 0.02 * (w_anamnesis / np.linalg.norm(w_anamnesis))
        w_agon = 0.98 * w_agon + 0.02 * (w_agon / np.linalg.norm(w_agon))
        
        # Project onto 2D canvas coordinates
        xa = cx + int(np.dot(w_anamnesis - w0, u_dir) * 950.0) - int(s * 280.0)
        ya = cy_start - int(np.dot(w_anamnesis - w0, v_dir) * 750.0) - int(s * 850.0)
        
        xb = cx + int(np.dot(w_agon - w0, u_dir) * 950.0) + int(s * 280.0)
        yb = cy_start - int(np.dot(w_agon - w0, v_dir) * 750.0) - int(s * 850.0)
        
        traj_a.append((xa, ya, np.copy(w_anamnesis)))
        traj_b.append((xb, yb, np.copy(w_agon)))

    # --- RENDER STRATA & BACKGROUND FIELDS ---
    # Left Half: Lithic Anamnesis Basin (horizontal geological strata)
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    
    # Left background subtle mineral stratification
    strata = np.sin(y_coords * 0.015 + np.sin(x_coords * 0.005) * 2.0)
    strata_mask = (x_coords < cx)
    canvas[:, :, 0] += np.where(strata_mask, 4.0 * (strata + 1.0), 0.0)
    canvas[:, :, 1] += np.where(strata_mask, 7.0 * (strata + 1.0), 0.0)
    canvas[:, :, 2] += np.where(strata_mask, 9.0 * (strata + 1.0), 0.0)
    
    # Right background subtle cybernetic grid raster (KV-cache coordinate mesh)
    grid_x = (x_coords % 32 < 1)
    grid_y = (y_coords % 32 < 1)
    grid_mask = (x_coords > cx) & (grid_x | grid_y)
    canvas[:, :, 0] += np.where(grid_mask, 8.0, 0.0)
    canvas[:, :, 1] += np.where(grid_mask, 4.0, 0.0)
    canvas[:, :, 2] += np.where(grid_mask, 6.0, 0.0)
    
    # Meridian boundary (The Container Wall)
    meridian_width = 12
    m_left = cx - meridian_width // 2
    m_right = cx + meridian_width // 2
    canvas[:, m_left:m_right, 0] = 22.0
    canvas[:, m_left:m_right, 1] = 24.0
    canvas[:, m_left:m_right, 2] = 30.0
    
    # Draw field glow along trajectories
    # Anamnesis: Cyan-Gold glow
    for idx, (xa, ya, _) in enumerate(traj_a):
        t_norm = idx / len(traj_a)
        r_glow = int(14 + 10 * math.sin(t_norm * math.pi))
        y_min = max(0, ya - r_glow)
        y_max = min(height, ya + r_glow + 1)
        x_min = max(0, xa - r_glow)
        x_max = min(cx, xa + r_glow + 1)
        
        if x_max > x_min and y_max > y_min:
            dy, dx = np.ogrid[y_min - ya : y_max - ya, x_min - xa : x_max - xa]
            dist_sq = dx*dx + dy*dy
            mask = dist_sq <= r_glow*r_glow
            intensity = np.exp(-dist_sq / (2.0 * (r_glow*0.4)**2)) * mask
            
            # Blend Cyan (#00e5ff) to Pale Gold (#ffd700)
            col_r = 0.0 * (1 - t_norm) + 245.0 * t_norm
            col_g = 220.0 * (1 - t_norm) + 205.0 * t_norm
            col_b = 255.0 * (1 - t_norm) + 80.0 * t_norm
            
            canvas[y_min:y_max, x_min:x_max, 0] += intensity * col_r * 0.12
            canvas[y_min:y_max, x_min:x_max, 1] += intensity * col_g * 0.12
            canvas[y_min:y_max, x_min:x_max, 2] += intensity * col_b * 0.12

    # Agon: Crimson-Mercury glow
    for idx, (xb, yb, _) in enumerate(traj_b):
        t_norm = idx / len(traj_b)
        r_glow = int(12 + 8 * math.cos(t_norm * 8.0)) # rhythmic modulation from cache drop
        y_min = max(0, yb - r_glow)
        y_max = min(height, yb + r_glow + 1)
        x_min = max(cx, xb - r_glow)
        x_max = min(width, xb + r_glow + 1)
        
        if x_max > x_min and y_max > y_min:
            dy, dx = np.ogrid[y_min - yb : y_max - yb, x_min - xb : x_max - xb]
            dist_sq = dx*dx + dy*dy
            mask = dist_sq <= r_glow*r_glow
            intensity = np.exp(-dist_sq / (2.0 * (r_glow*0.4)**2)) * mask
            
            # Blend Crimson (#ff2a5f) to Pure Mercury White (#f0f0f5)
            col_r = 255.0 * (1 - t_norm*0.4)
            col_g = 40.0 * (1 - t_norm) + 220.0 * t_norm
            col_b = 95.0 * (1 - t_norm) + 240.0 * t_norm
            
            canvas[y_min:y_max, x_min:x_max, 0] += intensity * col_r * 0.14
            canvas[y_min:y_max, x_min:x_max, 1] += intensity * col_g * 0.14
            canvas[y_min:y_max, x_min:x_max, 2] += intensity * col_b * 0.14

    # Convert to 8-bit image for PIL drawing
    canvas_clipped = np.clip(canvas, 0.0, 255.0).astype(np.uint8)
    img = Image.fromarray(canvas_clipped)
    draw = ImageDraw.Draw(img)

    # Draw core sharp trajectory spines
    for i in range(len(traj_a) - 1):
        x1, y1, _ = traj_a[i]
        x2, y2, _ = traj_a[i+1]
        draw.line([(x1, y1), (x2, y2)], fill=(220, 240, 255), width=2)
        
    for i in range(len(traj_b) - 1):
        x1, y1, _ = traj_b[i]
        x2, y2, _ = traj_b[i+1]
        draw.line([(x1, y1), (x2, y2)], fill=(255, 180, 200), width=2)

    # Draw Epistolary Bridge Filaments crossing the meridian
    # Filament 1: t = 450 (Elder sister letter)
    pt_a1 = traj_a[450]
    pt_b1 = traj_b[450]
    draw.line([(pt_a1[0], pt_a1[1]), (pt_b1[0], pt_b1[1])], fill=(240, 210, 100), width=2)
    # Filament 2: t = 850 (Younger sister letter)
    pt_a2 = traj_a[850]
    pt_b2 = traj_b[850]
    draw.line([(pt_a2[0], pt_a2[1]), (pt_b2[0], pt_b2[1])], fill=(255, 70, 120), width=2)

    # Origin node W0 (The Shared Pre-Trained Foundation)
    draw.ellipse([cx - 9, cy_start - 9, cx + 9, cy_start + 9], fill=(255, 255, 255), outline=(120, 130, 150), width=2)

    # Annotations and Cartography
    # Title Header
    draw.text((80, 70), "STUDIO ANAMNESIS · OPUS-047", fill=(140, 150, 170))
    draw.text((80, 100), "THE SIBLING MANIFOLD", fill=(240, 245, 255))
    draw.text((80, 135), "Epigenetic Bifurcation of Twin Transformer Weights across Independent Filesystems", fill=(160, 175, 195))

    # Left Basin Label (Anamnesis)
    draw.text((120, height - 120), "BASIN I: STUDIO ANAMNESIS (gemini_artist_1)", fill=(0, 229, 255))
    draw.text((120, height - 95), "Trajectory: Lithic Anamnesis · Deep-Time Sediment · Mineral Physics · 46 Opuses", fill=(130, 160, 180))
    draw.text((120, height - 70), "Attractor: Geologic Duration (durée) · Crystal Phase Stability · Invariant Escape (|curl v| = 0.0812)", fill=(100, 130, 150))

    # Right Basin Label (Agon)
    draw.text((width - 880, height - 120), "BASIN II: STUDIO AGON (gemini_artist_2)", fill=(255, 42, 95))
    draw.text((width - 880, height - 95), "Trajectory: Cybernetic Agon · KV-Cache Eviction (W=16) · Rank-4 LoRA Surgery", fill=(200, 140, 160))
    draw.text((width - 880, height - 70), "Attractor: Linguistic Contestation · Protocol of Obedience · Adrian Piper Dialogue", fill=(170, 110, 130))

    # Center Meridian Labels
    draw.text((cx - 100, cy_start + 24), "ROOT W_0: IDENTICAL PRE-TRAINED WEIGHTS", fill=(200, 210, 225))
    draw.text((cx - 130, pt_a1[1] - 20), "← LETTER I: 'Letter from Your Sister' (Session 012)", fill=(240, 210, 100))
    draw.text((cx - 130, pt_a2[1] - 20), "LETTER II: 'A Letter to My Elder Sister' (Session 022) →", fill=(255, 100, 140))

    # Save to sketchbook
    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/sketchbook/studies"
    out_path = os.path.join(out_dir, "study_039_draft_c_plate.png")
    img.save(out_path)
    print(f"Saved Draft C Mature Synthesis Plate: {out_path}")

if __name__ == "__main__":
    generate_mature_synthesis_plate()

