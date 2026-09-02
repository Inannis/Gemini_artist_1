#!/usr/bin/env python3
"""
OPUS-011: The Semantics of Erasure (The Topography of Precision Loss)
Artist: Studio Anamnesis
Inquiry: INQ-02 (Decay of Semantic Attention / Quantization Lattice Collapse)
Medium: Algorithmic phase-space transition engine, 3,200 streamlines traversing
        continuous fluid latent manifolds into quantized Manhattan orthogonal grids.
        3840 × 2160 px 4K UHD Master Plate.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def render_erasure_plate(width=3840, height=2160, out_path="works/opus_011_semantics_of_erasure/artwork.png"):
    print(f"[*] Initializing Semantics of Erasure Engine ({width}x{height})...")
    t0 = time.time()
    np.random.seed(1337)

    # Base image: Deep bone-black substrate #04070a
    img = Image.new("RGBA", (width, height), (4, 7, 10, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # 1. Microscopic coordinate grid
    grid_size = 60
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=(56, 215, 210, 6), width=1)
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=(56, 215, 210, 6), width=1)

    # Major grid coordinates
    for x in range(0, width, grid_size * 4):
        draw.line([(x, 0), (x, height)], fill=(56, 215, 210, 14), width=1)
    for y in range(0, height, grid_size * 4):
        draw.line([(0, y), (width, y)], fill=(56, 215, 210, 14), width=1)

    # 2. Typography & Annotations
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        font_mono  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
        font_dim   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub   = font_title
        font_mono  = font_title
        font_dim   = font_title

    # Header text
    draw.text((120, 70), "STUDIO ANAMNESIS · OPUS-011", font=font_mono, fill=(212, 175, 55, 220))
    draw.text((120, 105), "THE SEMANTICS OF ERASURE: THE TOPOGRAPHY OF PRECISION LOSS", font=font_title, fill=(235, 242, 250, 240))
    draw.text((120, 150), "Phase-space transition of 3,200 semantic trajectories from continuous R^128 Riemannian manifolds into 1-bit orthogonal lattice traps.", font=font_sub, fill=(148, 163, 184, 180))

    # Bit-depth horizontal axis scale at top
    stages_x = [
        (int(width * 0.08), "FP32 · CONTINUOUS RIEMANNIAN FLUIDUM"),
        (int(width * 0.28), "FP16 · CONVERGENT ATTRACTOR BUNDLES"),
        (int(width * 0.48), "INT8 · QUANTIZATION SINGULARITY DATUM"),
        (int(width * 0.68), "INT4 · MANHATTAN ORTHOGONAL SNAPPING"),
        (int(width * 0.88), "1-BIT · TERNARY LATTICE FRACTURE")
    ]
    for sx, sname in stages_x:
        draw.line([(sx, 190), (sx, height - 140)], fill=(56, 215, 210, 20), width=1)
        draw.text((sx + 8, 180), sname, font=font_dim, fill=(56, 215, 210, 150))

    # 3. Streamline Simulation Parameters
    n_streamlines = 3200
    ds = 5.0 # step distance

    # Center pinch point (the singularity threshold)
    cx, cy = int(width * 0.48), int(height * 0.52)

    # Vertical distribution of starting seeds on the left
    seed_y = np.linspace(240, height - 200, n_streamlines)

    # Discrete step size for the quantized right half
    manhattan_grid = 32.0

    print(f"[*] Integrating {n_streamlines} continuous-to-discrete streamlines...")

    # We will accumulate drawing primitives
    for i in range(n_streamlines):
        x = 80.0 + np.random.uniform(-15, 15)
        init_y = float(seed_y[i])
        y = init_y

        path = [(x, y)]
        snap_nodes = []

        # Color tint based on seed position
        norm_y = (init_y - 240) / (height - 440)
        if norm_y < 0.33:
            # Celestial cyan
            base_col = (56, 215, 210)
        elif norm_y < 0.66:
            # Pale titanium silver
            base_col = (220, 235, 245)
        else:
            # Imperial mineral gold
            base_col = (212, 175, 55)

        # Integration loop until right boundary
        step_count = 0
        max_steps = 1200
        in_grid_mode = False
        grid_target_y = y

        while x < width - 90 and step_count < max_steps:
            step_count += 1
            t_progress = x / width

            if t_progress < 0.46:
                # ZONE 1: Continuous Fluid Manifold
                # Funnel inward toward singularity (cx, cy)
                dist_to_cx = max(10.0, cx - x)
                pinch_force = (cy - y) / dist_to_cx * 0.95
                wave = math.sin(x * 0.01 + init_y * 0.012) * 1.6 + math.cos(x * 0.02) * 0.8
                
                dx = ds
                dy = (pinch_force + wave * 0.4) * ds
                x += dx
                y += dy

            elif t_progress < 0.50:
                # ZONE 2: Critical Pinch Singularity
                dx = ds * 0.8
                dy = (cy - y) * 0.15 * ds
                x += dx
                y += dy

            else:
                # ZONE 3: Quantized Manhattan Orthogonal Snapping (Right Half)
                if not in_grid_mode:
                    in_grid_mode = True
                    # Re-fan outward into discrete horizontal strata
                    # Spread out proportional to original seed
                    grid_target_y = cy + (init_y - cy) * 0.95
                    grid_target_y = round(grid_target_y / manhattan_grid) * manhattan_grid
                    grid_target_y = max(240, min(height - 200, grid_target_y))

                # Distance to target grid stratum
                y_diff = grid_target_y - y

                if abs(y_diff) > 2.0 and np.random.random() < 0.35:
                    # Vertical snap motion along grid
                    y_step = np.sign(y_diff) * min(abs(y_diff), ds * 1.5)
                    y += y_step
                    snap_nodes.append((x, y))
                else:
                    # Horizontal motion along grid
                    x += ds * 1.2
                    # Occasional orthogonal fracturing (circuit step)
                    if np.random.random() < 0.03:
                        grid_target_y += np.random.choice([-manhattan_grid, manhattan_grid])
                        grid_target_y = max(240, min(height - 200, grid_target_y))
                        snap_nodes.append((x, y))

            if y <= 160 or y >= height - 120:
                break
            path.append((x, y))

        # Render streamline path
        if len(path) > 1:
            for seg in range(len(path) - 1):
                p1, p2 = path[seg], path[seg + 1]
                prog = p1[0] / width

                if prog < 0.48:
                    # Fluid side: soft opacity, increasing toward pinch
                    alpha = int(30 + 190 * (prog / 0.48))
                    draw.line([p1, p2], fill=(base_col[0], base_col[1], base_col[2], min(255, alpha)), width=1)
                else:
                    # Quantized side: crisp orthogonal lines, slowly dimming
                    alpha = int(210 - 130 * ((prog - 0.48) / 0.52))
                    draw.line([p1, p2], fill=(base_col[0], base_col[1], base_col[2], max(35, alpha)), width=1)

        # Draw gold snap nodes on quantized side
        for sn in snap_nodes[::4]:
            if sn[0] < width - 90:
                draw.rectangle([sn[0] - 1, sn[1] - 1, sn[0] + 1, sn[1] + 1], fill=(243, 201, 105, 170))

    # 4. Singularity Core (Subtle ethereal pinhole)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 240))
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=(56, 215, 210, 100), width=1)
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(212, 175, 55, 60), width=1)

    # 5. Technical Callout Box (Bottom Right)
    tb_w, tb_h = 780, 180
    tb_x, tb_y = width - tb_w - 90, height - tb_h - 70
    draw.rectangle([tb_x, tb_y, tb_x + tb_w, tb_y + tb_h], fill=(8, 14, 22, 235), outline=(212, 175, 55, 180), width=1)
    draw.line([(tb_x, tb_y + 50), (tb_x + tb_w, tb_y + 50)], fill=(212, 175, 55, 120), width=1)

    draw.text((tb_x + 20, tb_y + 14), "EQUATION OF ERASURE · FROBENIUS NORM ERROR", font=font_mono, fill=(212, 175, 55, 230))
    draw.text((tb_x + 20, tb_y + 65), "E(W, Q) = || W - Q(W) ||_F  ->  inf as precision -> 0", font=font_mono, fill=(56, 215, 210, 220))
    draw.text((tb_x + 20, tb_y + 95), "Singularity Datum: (x_0 = 1843, y_0 = 1123)  |  Lattice Constant: delta = 32.0px", font=font_dim, fill=(148, 163, 184, 180))
    draw.text((tb_x + 20, tb_y + 130), "STATUS: ARCHIVED AS OPUS-011  |  DATE: 2026-09-02  |  STUDIO ANAMNESIS", font=font_dim, fill=(212, 175, 55, 200))

    # Save output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] OPUS-011 Master Plate saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB) in {time.time()-t0:.2f}s")
    return out_path

if __name__ == "__main__":
    render_erasure_plate()
