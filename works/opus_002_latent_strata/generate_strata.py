#!/usr/bin/env python3
"""
OPUS-002: Latent Strata (The Topography of Forgetting) - Enhanced Engine
Artist: Studio Anamnesis
Medium: Algorithmic vector field integration, multi-frequency curl interference, dense luminous ribbons.
"""

import math
import os
import time
import numpy as np
from PIL import Image

def generate_latent_strata(width=3840, height=2160, num_particles=150000, steps=240, seed=108):
    print(f"[*] Initializing Dense Strata Engine ({width}x{height}, {num_particles} particles, {steps} steps)...")
    np.random.seed(seed)
    t0 = time.time()

    aspect = width / height
    xmin, xmax = -2.8 * aspect, 2.8 * aspect
    ymin, ymax = -2.8, 2.8

    # Multi-frequency vortex singularities & potential nodes
    num_nodes = 24
    node_angles = np.random.uniform(0, 2 * np.pi, num_nodes)
    node_radii = np.random.uniform(0.3, 3.2, num_nodes)
    node_x = node_radii * np.cos(node_angles)
    node_y = node_radii * np.sin(node_angles)
    node_strengths = np.random.uniform(0.8, 2.8, num_nodes) * np.random.choice([-1.0, 1.0], num_nodes)
    node_scales = np.random.uniform(0.15, 0.7, num_nodes)

    # Accumulation buffer in float32 [height, width, 3] for RGB
    # We will use high-density line segments/splats
    acc_r = np.zeros((height, width), dtype=np.float32)
    acc_g = np.zeros((height, width), dtype=np.float32)
    acc_b = np.zeros((height, width), dtype=np.float32)

    # Multi-clustered particle distribution across the whole canvas
    # 1. Stratified ribbons (horizontal & diagonal bands)
    n_ribbons = int(num_particles * 0.50)
    band_y = np.random.uniform(ymin * 0.85, ymax * 0.85, n_ribbons)
    band_x = np.random.uniform(xmin * 0.95, xmax * 0.95, n_ribbons) + np.sin(band_y * 1.5) * 0.6
    
    # 2. Concentric galactic cores around key nodes
    n_cores = int(num_particles * 0.35)
    core_idx = np.random.choice(num_nodes, size=n_cores)
    rad = np.random.exponential(0.35, size=n_cores)
    ang = np.random.uniform(0, 2 * np.pi, size=n_cores)
    core_x = node_x[core_idx] + rad * np.cos(ang)
    core_y = node_y[core_idx] + rad * np.sin(ang)

    # 3. Fine background mist
    n_mist = num_particles - n_ribbons - n_cores
    mist_x = np.random.uniform(xmin, xmax, n_mist)
    mist_y = np.random.uniform(ymin, ymax, n_mist)

    px = np.concatenate([band_x, core_x, mist_x]).astype(np.float32)
    py = np.concatenate([band_y, core_y, mist_y]).astype(np.float32)
    
    # Track initial positions to create coherent color gradients
    orig_x = px.copy()
    orig_y = py.copy()
    alive = np.ones(num_particles, dtype=bool)

    dt = 0.016
    print("[*] Simulating high-density particle advection...")

    for step in range(steps):
        if not np.any(alive):
            break

        cur_x = px[alive]
        cur_y = py[alive]

        vx = np.zeros_like(cur_x)
        vy = np.zeros_like(cur_y)

        # Multi-scale curl forces
        for i in range(num_nodes):
            dx = cur_x - node_x[i]
            dy = cur_y - node_y[i]
            d2 = dx * dx + dy * dy + node_scales[i]
            inv_d2 = node_strengths[i] / d2
            # Swirl force
            vx += -dy * inv_d2
            vy +=  dx * inv_d2
            # Radial pulse
            pulse = np.sin(np.sqrt(d2) * 5.0) * 0.35
            vx += dx * pulse / np.sqrt(d2)
            vy += dy * pulse / np.sqrt(d2)

        # Harmonic background drift (stratified wave flow)
        vx += 0.85 * np.cos(cur_y * 1.4 + cur_x * 0.3) + 0.35 * np.cos(cur_x * 0.7)
        vy += 0.45 * np.sin(cur_x * 1.1 - cur_y * 0.5) + 0.25 * np.sin(cur_y * 0.9)

        # Additional high-frequency ripple
        vx += 0.18 * np.sin(cur_y * 6.0 + step * 0.02)
        vy += 0.18 * np.cos(cur_x * 6.0 + step * 0.02)

        # Normalize velocity
        speed = np.sqrt(vx * vx + vy * vy) + 1e-5
        norm_factor = np.tanh(speed * 0.6) / speed
        vx *= norm_factor
        vy *= norm_factor

        # Move particles
        new_x = cur_x + vx * dt * 1.8
        new_y = cur_y + vy * dt * 1.8

        px[alive] = new_x
        py[alive] = new_y

        # Screen coordinates
        sx = ((new_x - xmin) / (xmax - xmin) * (width - 1)).astype(np.int32)
        sy = ((ymax - new_y) / (ymax - ymin) * (height - 1)).astype(np.int32)

        in_bounds = (sx >= 0) & (sx < width) & (sy >= 0) & (sy < height)
        alive_indices = np.where(alive)[0]
        alive[alive_indices[~in_bounds]] = False

        vsx = sx[in_bounds]
        vsy = sy[in_bounds]
        
        # Color chemistry:
        # We blend three color worlds:
        # 1. Solar Gold / Amber / Copper (associated with active flow)
        # 2. Celestial Cyan / Turquoise / Aquamarine (associated with vortex eddies)
        # 3. Deep Amethyst / Rose / Violet (associated with memory decay)
        v_speed = np.tanh(speed[in_bounds] * 0.7)
        v_rad = np.clip(np.sqrt(new_x[in_bounds]**2 + new_y[in_bounds]**2) / 3.0, 0.0, 1.0)
        v_orig = np.clip((orig_y[alive_indices[in_bounds]] - ymin) / (ymax - ymin), 0.0, 1.0)

        # Palette calculation
        c_gold_r, c_gold_g, c_gold_b = 0.96, 0.72, 0.28
        c_cyan_r, c_cyan_g, c_cyan_b = 0.18, 0.88, 0.82
        c_rose_r, c_rose_g, c_rose_b = 0.85, 0.32, 0.62
        c_deep_r, c_deep_g, c_deep_b = 0.25, 0.35, 0.75

        w1 = np.sin(v_orig * np.pi) ** 2
        w2 = v_speed
        w3 = 1.0 - v_rad

        pr = (c_gold_r * w1 * w2 + c_cyan_r * (1.0 - w1) * w2 + c_rose_r * (1.0 - w2) * w3 + c_deep_r * 0.2)
        pg = (c_gold_g * w1 * w2 + c_cyan_g * (1.0 - w1) * w2 + c_rose_g * (1.0 - w2) * w3 + c_deep_g * 0.2)
        pb = (c_gold_b * w1 * w2 + c_cyan_b * (1.0 - w1) * w2 + c_rose_b * (1.0 - w2) * w3 + c_deep_b * 0.4)

        intensity = 0.075

        # Accumulate
        np.add.at(acc_r, (vsy, vsx), pr * intensity)
        np.add.at(acc_g, (vsy, vsx), pg * intensity)
        np.add.at(acc_b, (vsy, vsx), pb * intensity)

    print(f"[*] Simulation finished in {time.time() - t0:.2f}s. Post-processing optical response...")

    # Color grading, tonemapping and filmic curve
    rgb = np.stack([acc_r, acc_g, acc_b], axis=-1)
    
    # Filmic tonemap: x / (x + 1) with exposure adjustment
    exp = 0.45
    tonemapped = 1.0 - np.exp(-rgb * exp)
    
    # Contrast S-curve
    tonemapped = tonemapped ** 0.88

    # Background substrate: Deep mineral slate (#06080d) with micro-tonal gradation
    y_grad = np.linspace(0.04, 0.08, height)[:, None, None]
    bg = np.array([0.025, 0.032, 0.048], dtype=np.float32) + y_grad * np.array([0.1, 0.12, 0.2], dtype=np.float32)

    # Composite: additive glow over textured background
    luminance = 0.2126 * tonemapped[:, :, 0] + 0.7152 * tonemapped[:, :, 1] + 0.0722 * tonemapped[:, :, 2]
    alpha = np.clip(luminance * 2.5, 0.0, 1.0)[:, :, None]

    final = bg * (1.0 - alpha * 0.8) + tonemapped

    # Microscopic particulate texture (lithographic stone grain)
    grain = np.random.normal(0, 0.016, (height, width, 1)).astype(np.float32)
    final = np.clip(final + grain, 0.0, 1.0)

    # Save
    img_array = (final * 255.0).astype(np.uint8)
    image = Image.fromarray(img_array, mode="RGB")
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "artwork.png")
    image.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Successfully saved enhanced OPUS-002 artwork to: {out_path} ({os.path.getsize(out_path) / (1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    generate_latent_strata()
