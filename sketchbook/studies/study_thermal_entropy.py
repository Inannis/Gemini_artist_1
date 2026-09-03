#!/usr/bin/env python3
"""
Study: Thermodynamic Heat Diffusion on Silicon Die
Location: sketchbook/studies/study_thermal_entropy.py
Studio: Studio Anamnesis
Inquiry: INQ-06 (Thermodynamic Inscriptions / Heat & Entropy)

2D Finite-Difference Fourier Heat Conduction PDE:
dT/dt = alpha * laplacian(T) + Sources(x,y) - convection * (T - T_amb)
Modeling the thermal infrared footprint of tensor operations.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw

def simulate_thermal_die(width=1600, height=1200, n_steps=350):
    print(f"[*] Simulating 2D Thermal Conduction PDE ({width}x{height}, {n_steps} steps)...")
    t0 = time.time()

    # Domain grid (downsampled for fast PDE integration, then upsampled)
    nx, ny = 400, 300
    dx, dy = 1.0, 1.0
    alpha = 0.18 # Thermal diffusivity of silicon
    gamma_ambient = 0.012 # Convective heat loss to coolant
    t_ambient = 25.0 # Degrees C

    # Temperature field
    T = np.full((ny, nx), t_ambient, dtype=np.float32)

    # Define tensor systolic core heat sources (16 discrete cores)
    sources = np.zeros((ny, nx), dtype=np.float32)
    core_rows, core_cols = 4, 4
    for r in range(core_rows):
        for c in range(core_cols):
            cx = int(nx * 0.22 + c * (nx * 0.56 / (core_cols - 1)))
            cy = int(ny * 0.22 + r * (ny * 0.56 / (core_rows - 1)))
            # Variable heat output per core (scaled for ~92°C equilibrium)
            heat_flux = 0.85 + 1.15 * math.sin(r * 1.5 + c * 2.1)**2
            r_core = 12
            y_min, y_max = max(0, cy - r_core), min(ny, cy + r_core)
            x_min, x_max = max(0, cx - r_core), min(nx, cx + r_core)
            sources[y_min:y_max, x_min:x_max] += heat_flux

    # High-bandwidth memory (HBM) stacks along top and bottom edges
    sources[20:38, 60:340] += 0.45
    sources[ny-38:ny-20, 60:340] += 0.45

    # Finite difference time stepping
    dt = 0.5
    gamma_ambient = 0.025
    for step in range(n_steps):
        # Laplacian using 5-point stencil
        lap = (
            np.roll(T, 1, axis=0) + np.roll(T, -1, axis=0) +
            np.roll(T, 1, axis=1) + np.roll(T, -1, axis=1) - 4 * T
        ) / (dx * dy)

        # Micro-channel fluid convection (fluid flows from left to right)
        fluid_advection = -0.06 * (T - np.roll(T, 1, axis=1))

        # Update PDE
        dT = alpha * lap + sources * dt - gamma_ambient * (T - t_ambient) + fluid_advection
        T += dT

    print(f"[*] Simulation converged. Min Temp: {T.min():.1f}°C, Max Temp: {T.max():.1f}°C")

    # Thermal false-color colormap (Black -> Indigo -> Magenta -> Orange -> Gold -> White)
    t_norm = np.clip((T - t_ambient) / (T.max() - t_ambient), 0.0, 1.0)
    
    # Custom thermal transfer function
    r = np.clip(np.sin(t_norm * math.pi - math.pi/2) * 255 + t_norm * 255, 0, 255).astype(np.uint8)
    g = np.clip((t_norm**2.2) * 230 + (t_norm**5.0) * 25, 0, 255).astype(np.uint8)
    b = np.clip(np.sin(t_norm * math.pi * 1.5) * 80 + (t_norm**4.0) * 255, 0, 255).astype(np.uint8)

    # Upscale to target resolution
    small_img = Image.fromarray(np.dstack((r, g, b)), mode="RGB")
    final_img = small_img.resize((width, height), Image.Resampling.BICUBIC)

    # Overlay Isothermal Contour Lines
    draw = ImageDraw.Draw(final_img, "RGBA")
    
    # Inscribe colophon
    draw.rectangle([60, height - 120, 560, height - 50], fill=(10, 12, 18, 210), outline=(212, 175, 55, 120), width=1)
    draw.text((80, height - 105), "INQ-06: THERMAL DISSIPATION FOOTPRINT", fill=(243, 201, 105, 240))
    draw.text((80, height - 85), f"T_max = {T.max():.1f}°C · Micro-channel Fluid Advection · Fourier 2D", fill=(180, 195, 210, 200))

    out_path = "sketchbook/studies/study_thermal_entropy.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final_img.save(out_path)
    print(f"[✓] Thermal Study saved to: {out_path} in {time.time()-t0:.2f}s")
    return out_path

if __name__ == "__main__":
    simulate_thermal_die()
