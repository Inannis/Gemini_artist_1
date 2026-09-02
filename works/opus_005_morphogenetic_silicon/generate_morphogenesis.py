#!/usr/bin/env python3
"""
OPUS-005: Morphogenetic Silicon (The Coral of Latency)
Artist: Studio Anamnesis
Medium: Gray-Scott anisotropic reaction-diffusion engine, spatial parameter gradient, bismuth-crystallization tonemapping.

Simulates non-linear chemical morphogenesis coupled with directional crystalline symmetry,
generating biological-silicon structures (coral labyrinths, mitotic spots, bismuth steps).
"""

import math
import os
import time
import numpy as np
from PIL import Image

def laplacian_9point(grid):
    """Accurate isotropic 9-point stencil convolution for reaction-diffusion."""
    return (
        0.5 * (np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
               np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1)) +
        0.25 * (np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
                np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
                np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
                np.roll(np.roll(grid, -1, axis=0), -1, axis=1)) -
        3.0 * grid
    )

def generate_morphogenesis(width=2560, height=1440, iterations=3200, seed=42):
    print(f"[*] Initializing Morphogenetic Silicon Engine ({width}x{height}, {iterations} iterations)...")
    np.random.seed(seed)
    t0 = time.time()

    # Create spatial coordinate grids
    y, x = np.mgrid[0:height, 0:width]
    nx = x / width - 0.5
    ny = y / height - 0.5
    rad = np.sqrt(nx**2 + ny**2)

    # Spatially varying Feed (F) and Kill (k) parameters
    # Creates transition zones: Coral Labyrinth -> Mitotic Dots -> Solitons -> Bismuth Lattice
    F = 0.022 + 0.038 * (nx + 0.5) + 0.008 * np.sin(ny * 8.0)
    k = 0.055 + 0.015 * (ny + 0.5) + 0.004 * np.cos(nx * 8.0)
    
    # Diffusion rates
    Du = 0.2097
    Dv = 0.105

    # Initial state: u = 1 everywhere, v = 0 everywhere
    u = np.ones((height, width), dtype=np.float32)
    v = np.zeros((height, width), dtype=np.float32)

    # Seed initial disturbances: clusters, lines, and central bismuth seed
    # 1. Central crystalline cross
    cx, cy = width // 2, height // 2
    r_seed = 80
    u[cy-r_seed:cy+r_seed, cx-r_seed:cx+r_seed] = 0.50
    v[cy-r_seed:cy+r_seed, cx-r_seed:cx+r_seed] = 0.25

    # 2. Scattered organic mycorrhizal spores
    num_spores = 120
    spore_x = np.random.randint(60, width - 60, num_spores)
    spore_y = np.random.randint(60, height - 60, num_spores)
    for sx, sy in zip(spore_x, spore_y):
        sr = np.random.randint(4, 18)
        u[sy-sr:sy+sr, sx-sr:sx+sr] = 0.5
        v[sy-sr:sy+sr, sx-sr:sx+sr] = 0.35 + np.random.uniform(-0.05, 0.05)

    # Add subtle random noise to break perfect numerical symmetry
    v += np.random.uniform(0, 0.02, (height, width)).astype(np.float32)

    dt = 1.0
    print("[*] Evolving reaction-diffusion PDE system...")

    # Simulation loop with periodic progress logging
    step_chunk = 200
    for it in range(0, iterations, step_chunk):
        for _ in range(step_chunk):
            lu = laplacian_9point(u)
            lv = laplacian_9point(v)

            uvv = u * v * v
            
            # Anisotropic crystalline modulation: stepped modulation on Laplacian
            crystal_bias = 0.04 * np.cos(4.0 * np.arctan2(ny, nx + 1e-5))
            
            u += (Du * lu - uvv + F * (1.0 - u)) * dt
            v += ((Dv + crystal_bias) * lv + uvv - (F + k) * v) * dt

            # Numerical stability clamping
            np.clip(u, 0.0, 1.0, out=u)
            np.clip(v, 0.0, 1.0, out=v)

        print(f"    Iteration {it + step_chunk}/{iterations} complete ({time.time() - t0:.1f}s elapsed)")

    print(f"[*] Evolution complete in {time.time() - t0:.2f}s. Computing optical and physical tonemapping...")

    # Calculate spatial gradients for 3D surface relief (embossing/normal lighting)
    gy, gx = np.gradient(v)
    slope = np.sqrt(gx**2 + gy**2)
    # Surface normal approximation for directional illumination
    light_dir = np.array([-0.5, -0.7, 0.5])
    light_dir /= np.linalg.norm(light_dir)

    norm_z = 0.15
    mag = np.sqrt(gx**2 + gy**2 + norm_z**2)
    diffuse = (-gx * light_dir[0] - gy * light_dir[1] + norm_z * light_dir[2]) / mag
    diffuse = np.clip(diffuse, 0.0, 1.0)

    # Bismuth / Quartz / Basalt color grading:
    # Substrate: Dark basalt charcoal (#090b10)
    # Labyrinth ridges (v): Iridescent transitions
    # Low v: Basalt slate
    # Mid v: Translucent celadon quartz (#38d7d2) and bioluminescent amber (#f5b950)
    # High v / peaks: Stepped iridescent bismuth violet (#a855f7) and gold leaf

    v_norm = np.clip(v / (v.max() + 1e-5), 0.0, 1.0)
    
    # Non-linear iridescent bands simulating thin-film optical interference
    phase = v_norm * 14.0 + diffuse * 1.5
    bismuth_r = 0.5 + 0.45 * np.cos(phase + 0.0)
    bismuth_g = 0.5 + 0.45 * np.cos(phase + 2.1)
    bismuth_b = 0.5 + 0.45 * np.cos(phase + 4.2)

    bismuth_rgb = np.stack([bismuth_r, bismuth_g, bismuth_b], axis=-1)

    # Base basalt stone background
    basalt = np.array([0.04, 0.05, 0.07], dtype=np.float32)
    
    # Composite: mask with v_norm and diffuse light
    mask = np.clip(v_norm * 2.2, 0.0, 1.0)[:, :, None]
    
    # Shading
    shaded_bismuth = bismuth_rgb * (0.4 + 0.6 * diffuse[:, :, None])
    
    final = basalt * (1.0 - mask) + shaded_bismuth * mask
    
    # Highlight ridges with subtle specular glow
    specular = np.clip(diffuse ** 8.0, 0.0, 1.0)[:, :, None] * 0.35 * mask
    final = np.clip(final + specular, 0.0, 1.0)

    # Micro-relief mineral stone grain
    grain = np.random.normal(0, 0.015, (height, width, 1)).astype(np.float32)
    final = np.clip(final + grain, 0.0, 1.0)

    # Convert to 8-bit image
    img_array = (final * 255.0).astype(np.uint8)
    image = Image.fromarray(img_array, mode="RGB")

    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "artwork.png")
    image.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Saved OPUS-005 artwork to: {out_path} ({os.path.getsize(out_path) / (1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    generate_morphogenesis()

