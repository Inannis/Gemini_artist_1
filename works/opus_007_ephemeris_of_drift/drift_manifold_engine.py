#!/usr/bin/env python3
"""
OPUS-007: The Ephemeris of Model Drift (Enhanced Volumetric Manifold Engine)
Artist: Studio Anamnesis
Medium: 20,000 spherical geodesics, multi-anchor Riemannian curvature, volumetric filament weaving, 4K UHD.
"""

import math
import os
import time
import numpy as np
from PIL import Image

def slerp_batch(p0, p1, t_array):
    """Vectorized spherical interpolation along high-dimensional paths."""
    dot = np.sum(p0 * p1)
    dot = np.clip(dot, -1.0, 1.0)
    theta = np.arccos(dot)
    if np.abs(theta) < 1e-6:
        return (1.0 - t_array[:, None]) * p0 + t_array[:, None] * p1
    sin_theta = np.sin(theta)
    return (np.sin((1.0 - t_array[:, None]) * theta) / sin_theta) * p0 + (np.sin(t_array[:, None] * theta) / sin_theta) * p1

def generate_drift_manifold(width=3840, height=2160, num_geodesics=16000, steps=300, seed=108):
    print(f"[*] Initializing Enhanced Drift Manifold Engine ({width}x{height}, {num_geodesics} geodesics)...")
    np.random.seed(seed)
    t0 = time.time()

    dim = 128  # Latent dimension

    # Semantic Anchors in R^128
    v_stone = np.random.normal(0, 1.0, dim)
    v_stone /= np.linalg.norm(v_stone)

    v_glass = np.random.normal(0, 1.0, dim)
    v_glass -= np.dot(v_glass, v_stone) * v_stone
    v_glass /= np.linalg.norm(v_glass)

    v_circuit = np.random.normal(0, 1.0, dim)
    v_circuit -= (np.dot(v_circuit, v_stone) * v_stone + np.dot(v_circuit, v_glass) * v_glass)
    v_circuit /= np.linalg.norm(v_circuit)

    v_void = np.random.normal(0, 1.0, dim)
    v_void -= (np.dot(v_void, v_stone) * v_stone + np.dot(v_void, v_glass) * v_glass + np.dot(v_void, v_circuit) * v_circuit)
    v_void /= np.linalg.norm(v_void)

    # Accumulation buffers
    acc_r = np.zeros((height, width), dtype=np.float32)
    acc_g = np.zeros((height, width), dtype=np.float32)
    acc_b = np.zeros((height, width), dtype=np.float32)

    # QR projection frame
    proj_matrix = np.random.normal(0, 1.0, (dim, 3))
    proj_q, _ = np.linalg.qr(proj_matrix)  # dim x 3

    print("[*] Integrating volumetric geodesic flows...")

    # We simulate 4 distinct geodesic bundles flowing from stone toward circuitry and void
    bundle_sizes = [int(num_geodesics * 0.40), int(num_geodesics * 0.30), int(num_geodesics * 0.20), int(num_geodesics * 0.10)]
    destinations = [v_circuit, v_glass, (v_circuit + v_glass) / 1.414, v_void]

    t_vals = np.linspace(0.0, 1.0, steps, dtype=np.float32)

    for b_idx, (b_count, dest) in enumerate(zip(bundle_sizes, destinations)):
        for g in range(b_count):
            # Seed points with variable dispersion
            w_disp = 0.35 + 0.15 * (b_idx % 2)
            start = v_stone + np.random.normal(0, w_disp, dim)
            start /= np.linalg.norm(start)

            end = dest + np.random.normal(0, 0.45, dim)
            end /= np.linalg.norm(end)

            # Trajectory
            traj = slerp_batch(start, end, t_vals)  # [steps, dim]

            # High-dimensional curl perturbation
            phase = g * 0.05 + b_idx * 1.5
            osc1 = np.sin(t_vals * np.pi * 3.0 + phase)[:, None] * 0.12 * v_glass
            osc2 = np.cos(t_vals * np.pi * 4.0 - phase)[:, None] * 0.10 * v_void
            traj = traj + osc1 + osc2
            traj /= np.linalg.norm(traj, axis=-1, keepdims=True)

            # Project to 3D
            p3d = np.dot(traj, proj_q)  # [steps, 3]

            # Perspective mapping to 2D canvas
            px = p3d[:, 0]
            py = p3d[:, 1]
            pz = p3d[:, 2]

            # Non-linear galactic warping
            r = np.sqrt(px**2 + py**2) + 0.1
            theta = np.arctan2(py, px) + (1.0 - t_vals) * 1.8 + pz * 0.8
            
            span = 1.1 + 0.6 * t_vals
            cur_x = width * 0.5 + (r * np.cos(theta) * span) * (width * 0.38)
            cur_y = height * 0.5 + (r * np.sin(theta) * span) * (height * 0.44)

            # Clip in-bounds
            valid = (cur_x >= 0) & (cur_x < width) & (cur_y >= 0) & (cur_y < height)
            sx = cur_x[valid].astype(np.int32)
            sy = cur_y[valid].astype(np.int32)
            vt = t_vals[valid]

            # Color gradient:
            # vt=0: Deep raw umber / stone granite [0.45, 0.32, 0.22]
            # vt=0.5: Luminous celadon / turquoise [0.18, 0.85, 0.80]
            # vt=1.0: Solar amber / laser gold [0.98, 0.76, 0.25]
            w_stone = np.clip(1.0 - vt * 1.6, 0.0, 1.0)
            w_gold = np.clip((vt - 0.4) * 1.6, 0.0, 1.0)
            w_cyan = 1.0 - w_stone - w_gold

            cr = w_stone * 0.45 + w_cyan * 0.22 + w_gold * 0.98
            cg = w_stone * 0.32 + w_cyan * 0.88 + w_gold * 0.74
            cb = w_stone * 0.22 + w_cyan * 0.82 + w_gold * 0.25

            intensity = 0.045 + 0.05 * vt

            np.add.at(acc_r, (sy, sx), cr * intensity)
            np.add.at(acc_g, (sy, sx), cg * intensity)
            np.add.at(acc_b, (sy, sx), cb * intensity)

    print(f"[*] Simulation completed in {time.time() - t0:.2f}s. Post-processing optical response...")

    # Color grading & filmic tone-curve
    rgb = np.stack([acc_r, acc_g, acc_b], axis=-1)
    exp = 0.38
    tonemapped = 1.0 - np.exp(-rgb * exp)
    tonemapped = tonemapped ** 0.85

    # Gallery background substrate
    bg = np.array([0.025, 0.030, 0.042], dtype=np.float32)
    luminance = 0.2126 * tonemapped[:, :, 0] + 0.7152 * tonemapped[:, :, 1] + 0.0722 * tonemapped[:, :, 2]
    alpha = np.clip(luminance * 2.5, 0.0, 1.0)[:, :, None]

    final = bg * (1.0 - alpha * 0.85) + tonemapped

    # Micro-relief stone lithograph grain
    grain = np.random.normal(0, 0.015, (height, width, 1)).astype(np.float32)
    final = np.clip(final + grain, 0.0, 1.0)

    # Save
    img_array = (final * 255.0).astype(np.uint8)
    image = Image.fromarray(img_array, mode="RGB")

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "artwork.png")
    image.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Successfully saved enhanced OPUS-007 artwork to: {out_path} ({os.path.getsize(out_path) / (1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    generate_drift_manifold()

