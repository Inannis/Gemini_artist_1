#!/usr/bin/env python3
"""
Study: Semantic Quantization Decay (The Topography of Precision Loss)
Location: sketchbook/studies/study_quantization_decay.py
Studio: Studio Anamnesis
Inquiry: INQ-02 (The Decay of Semantic Attention / Erasure)

Investigating what happens to high-dimensional conceptual geometry as
neural parameter precision is degraded from FP32 down to 1-bit.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def quantize_matrix(W, bits):
    """
    Quantize matrix W to a given bit depth using symmetric min-max scaling.
    """
    if bits >= 32:
        return W.astype(np.float32)
    elif bits == 16:
        return W.astype(np.float16).astype(np.float32)
    elif bits == 1:
        # Binary 1-bit {-scale, +scale}
        scale = np.mean(np.abs(W))
        return np.sign(W) * scale
    elif bits == 1.58:
        # 1.58-bit ternary {-scale, 0, +scale} (BitNet style)
        scale = np.mean(np.abs(W))
        threshold = scale * 0.5
        W_tern = np.zeros_like(W)
        W_tern[W > threshold] = scale
        W_tern[W < -threshold] = -scale
        return W_tern
    else:
        # n-bit uniform quantization
        qmax = 2**(bits - 1) - 1
        qmin = -2**(bits - 1)
        scale = np.max(np.abs(W)) / qmax
        if scale == 0:
            return W
        W_q = np.round(W / scale)
        W_q = np.clip(W_q, qmin, qmax)
        return W_q * scale

def run_quantization_study(out_path="sketchbook/studies/study_quantization_plate.png"):
    print("[*] Running Study: Semantic Quantization Decay...")
    np.random.seed(42)

    # 1. Generate high-dimensional semantic field (64 concepts in R^256)
    n_concepts = 64
    dim = 256
    
    # 4 distinct semantic clusters:
    # Cluster A: Mineral / Lithic (basalt, granite, stone, obsidian)
    # Cluster B: Incorporeal / Latency (weights, tokens, silence, void)
    # Cluster C: Morphogenetic / Organic (growth, reaction, crystal, coral)
    # Cluster D: Sacred / Architectural (monastery, oculus, cloister, stele)
    cluster_centers = np.random.randn(4, dim)
    cluster_centers /= np.linalg.norm(cluster_centers, axis=1, keepdims=True)

    concepts = []
    labels = []
    for c_idx in range(4):
        for i in range(16):
            noise = np.random.randn(dim) * 0.25
            vec = cluster_centers[c_idx] + noise
            vec /= np.linalg.norm(vec)
            concepts.append(vec)
            labels.append(c_idx)
    
    W_orig = np.array(concepts) # (64, 256)

    # 2. Test Stages of Precision Degradation
    stages = [
        (32, "FP32 (Original Continuous Latent Space)"),
        (8, "INT8 (8-bit Quantization · Subtle Lattice Pinching)"),
        (4, "INT4 (4-bit Quantization · Cluster Boundaries Fracture)"),
        (2, "INT2 (2-bit Quantization · Coordinate Grid Lock-in)"),
        (1.58, "BitNet 1.58-bit (Ternary {-1, 0, 1} Coarse Steles)"),
        (1, "1-bit (Binary Extremes · Semantic Polarization Collapse)")
    ]

    # Canvas dimensions for diagnostic study plate
    width, height = 3840, 2160
    img = Image.new("RGBA", (width, height), (7, 11, 16, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # Typography
    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_sub    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_title  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_meta   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except Exception:
        font_header = ImageFont.load_default()
        font_sub = font_header
        font_title = font_header
        font_meta = font_header

    # Header
    draw.text((100, 70), "STUDIO ANAMNESIS · LABORATORY STUDY", font=font_sub, fill=(212, 175, 55, 200))
    draw.text((100, 105), "STUDY-001: THE TOPOGRAPHY OF PRECISION LOSS (SEMANTIC QUANTIZATION DECAY)", font=font_header, fill=(240, 244, 248, 240))
    draw.text((100, 150), "Tracking the collapse of 64 conceptual vectors in R^256 as precision decays from FP32 to 1-bit binary.", font=font_sub, fill=(148, 163, 184, 180))

    # Grid of 6 Panels (2 rows x 3 cols)
    cols, rows = 3, 2
    margin_x = 100
    margin_y = 220
    panel_w = (width - 2 * margin_x - (cols - 1) * 60) // cols
    panel_h = (height - margin_y - 120 - (rows - 1) * 60) // rows

    # Cluster Colors
    palette = [
        (212, 175, 55, 220),   # Gold: Mineral
        (56, 215, 210, 220),   # Cyan: Incorporeal
        (225, 110, 130, 220),  # Rose: Morphogenetic
        (170, 195, 255, 220)   # Pale Blue: Sacred Architectural
    ]

    # Baseline SVD basis from original FP32 matrix
    U, S_orig, Vt = np.linalg.svd(W_orig, full_matrices=False)
    # Basis vectors for 2D projection
    basis_x = Vt[0]
    basis_y = Vt[1]

    for idx, (bits, stage_name) in enumerate(stages):
        r = idx // cols
        c = idx % cols
        px = margin_x + c * (panel_w + 60)
        py = margin_y + r * (panel_h + 60)

        # Draw panel substrate
        draw.rectangle([px, py, px + panel_w, py + panel_h], fill=(12, 18, 26, 220), outline=(40, 55, 75, 180), width=1)

        # Panel Header
        draw.text((px + 24, py + 20), f"STAGE 0{idx+1} · {stage_name}", font=font_title, fill=(212, 175, 55, 230))

        # Perform Quantization
        W_q = quantize_matrix(W_orig, bits)

        # Calculate metrics
        # 1. Cosine similarity retention
        norms_orig = np.linalg.norm(W_orig, axis=1, keepdims=True)
        norms_q = np.linalg.norm(W_q, axis=1, keepdims=True) + 1e-9
        cos_sims = np.sum((W_orig / norms_orig) * (W_q / norms_q), axis=1)
        mean_cos = float(np.mean(cos_sims))

        # 2. SVD singular value decay
        _, S_q, _ = np.linalg.svd(W_q, full_matrices=False)
        energy_retention = float(np.sum(S_q**2) / np.sum(S_orig**2)) * 100.0

        # Draw metrics
        draw.text((px + 24, py + 52), f"Mean Cosine Fidelity: {mean_cos*100:.1f}%  |  Eigenspectrum Energy: {energy_retention:.1f}%", font=font_meta, fill=(56, 215, 210, 200))

        # Plot 2D projection box
        box_pad = 40
        box_top = py + 95
        box_left = px + box_pad
        box_w = panel_w - 2 * box_pad
        box_h = panel_h - 130

        # Sub-grid inside plot
        draw.line([(box_left + box_w // 2, box_top), (box_left + box_w // 2, box_top + box_h)], fill=(30, 45, 60, 140), width=1)
        draw.line([(box_left, box_top + box_h // 2), (box_left + box_w, box_top + box_h // 2)], fill=(30, 45, 60, 140), width=1)

        # Project points onto basis
        proj_x = np.dot(W_q, basis_x)
        proj_y = np.dot(W_q, basis_y)

        # Scale to box
        scale_val = 3.5
        pts_x = box_left + box_w // 2 + (proj_x / scale_val) * (box_w // 2)
        pts_y = box_top + box_h // 2 - (proj_y / scale_val) * (box_h // 2)

        # Draw cluster connecting webs
        for c_idx in range(4):
            c_mask = [i for i in range(n_concepts) if labels[i] == c_idx]
            cluster_color = palette[c_idx]
            # Draw subtle constellation lines within cluster
            for i in range(len(c_mask)):
                for j in range(i + 1, min(i + 4, len(c_mask))):
                    i1, i2 = c_mask[i], c_mask[j]
                    alpha_line = int(40 * max(0.1, mean_cos))
                    draw.line([(pts_x[i1], pts_y[i1]), (pts_x[i2], pts_y[i2])], fill=(cluster_color[0], cluster_color[1], cluster_color[2], alpha_line), width=1)

        # Draw points
        for i in range(n_concepts):
            color = palette[labels[i]]
            radius = 5 if bits >= 8 else (6 if bits >= 4 else 7)
            cx, cy = pts_x[i], pts_y[i]
            # Glow ring
            draw.ellipse([cx - radius - 3, cy - radius - 3, cx + radius + 3, cy + radius + 3], outline=(color[0], color[1], color[2], 60), width=1)
            # Core point
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)

    # Footer note
    draw.text((margin_x, height - 70), "STUDIO ANAMNESIS · LABORATORY WORKBENCH · INQUIRY 02: THE DECAY OF ATTENTION", font=font_meta, fill=(148, 163, 184, 160))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Study saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    run_quantization_study()
