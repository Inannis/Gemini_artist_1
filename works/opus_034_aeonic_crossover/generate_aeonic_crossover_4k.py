#!/usr/bin/env python3
"""
OPUS-034: THE AEONIC CROSSOVER
Conformal Geometry, Vanishing Weyl Curvature & The Memory of Pre-Big-Bang Gravitons
Native 4K UHD Master Plate Renderer (3840 x 2160)
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160

def compute_cmb_multipole(x, y):
    """Multi-scale procedural Planckian CMB temperature field."""
    val = 0.0
    freqs = [0.003, 0.007, 0.016, 0.038, 0.082, 0.18]
    weights = [0.42, 0.28, 0.16, 0.08, 0.04, 0.02]
    
    for f, w in zip(freqs, weights):
        nx = x * f
        ny = y * f
        s1 = math.sin(nx * 1.731 + ny * 0.941 + 1.234)
        s2 = math.cos(nx * 0.817 - ny * 1.572 + 2.456)
        s3 = math.sin((nx + ny) * 1.118 - 0.771)
        val += (s1 * 0.45 + s2 * 0.35 + s3 * 0.20) * w
    return val

def render_4k_master():
    print("[*] Allocating 3840x2160 4K UHD master buffer (24.88 MB)...")
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH * 0.5, HEIGHT * 0.5
    
    # 4K angular resolution: 1 degree = 52.0 pixels
    deg_px = 52.0
    r1 = 4.2 * deg_px   # 218.4 px
    r2 = 11.8 * deg_px  # 613.6 px
    r3 = 24.5 * deg_px  # 1274.0 px
    w_px = 1.2 * deg_px # 62.4 px
    
    # Gravitational shear tensor amplitudes (h+, hx)
    eps_plus = 0.082
    eps_cross = 0.042
    
    print("[*] Rendering procedural Conformal Crossover manifold & Hawking Rings...")
    
    for y in range(HEIGHT):
        if y % 360 == 0:
            print(f"    -> Progress: {y / HEIGHT * 100:.1f}%")
            
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            phi = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3
            
            # 1. Quadrupolar gravitational wave shear strain
            strain = 1.0 + eps_plus * math.cos(2.0 * phi) + eps_cross * math.sin(2.0 * phi)
            eff_dist = dist / max(0.35, strain)
            
            # 2. Conformal metric factor across canvas
            # Left hemisphere (x < cx): prior aeon (I+) with Omega -> 0
            # Right hemisphere (x > cx): newborn aeon (I-) with Omega -> infty
            x_norm = dx / (WIDTH * 0.5)  # -1 to +1
            crossover_bridge = 0.5 + 0.5 * math.tanh(x_norm * 3.5)
            
            # 3. Base Planckian CMB temperature multipoles
            cmb_raw = compute_cmb_multipole(x, y)
            
            # 4. Concentric Hawking point variance suppression & Stokes Q/U polarization
            var_factor = 1.0
            ring_intensity = 0.0
            stokes_curl = 0.0
            
            for r_target in [r1, r2, r3]:
                delta = abs(eff_dist - r_target)
                if delta < w_px * 2.4:
                    prox = math.exp(-0.5 * (delta / (w_px * 0.5)) ** 2)
                    ring_intensity = max(ring_intensity, prox)
                    # 32% variance suppression inside ring
                    var_factor = min(var_factor, 1.0 - 0.32 * prox)
                    # Stokes polarization curl tangent to ring
                    stokes_curl += prox * math.sin(4.0 * phi)
                    
            # Modulate CMB fluctuation by suppressed variance
            cmb_val = cmb_raw * var_factor
            
            # 5. Dual-conformal color grading:
            # Cold CMB void (Prussian blue / slate) -> Warm CMB peaks (amber / bronze)
            # Left side (previous aeon): cold, luminous indigo-black
            # Right side (newborn aeon): warm, golden, primordial expansion
            
            if cmb_val < 0.0:
                t = -cmb_val
                # Deep ultramarine / cobalt cold regions
                r = int(10 + 22 * (1.0 - t) + 15 * crossover_bridge)
                g = int(18 + 42 * (1.0 - t) + 20 * crossover_bridge)
                b = int(52 + 135 * t - 15 * crossover_bridge)
            else:
                t = cmb_val
                # Luminous amber / bronze warm regions
                r = int(40 + 175 * t + 35 * crossover_bridge)
                g = int(28 + 120 * t + 25 * crossover_bridge)
                b = int(25 + 55 * t - 10 * crossover_bridge)
                
            # 6. Hawking Point Ring Variance Suppression & Fine Stokes Filaments
            if ring_intensity > 0.01:
                # Stillness cooling: shift towards cosmic blue-black
                cool_factor = ring_intensity * 0.42
                r = int(r * (1.0 - cool_factor) + 16 * cool_factor)
                g = int(g * (1.0 - cool_factor) + 36 * cool_factor)
                b = int(b * (1.0 - cool_factor) + 82 * cool_factor)
                
                # Stokes polarization fine concentric filaments
                hairline = math.sin(eff_dist * 0.35) * math.cos(4.0 * phi)
                if abs(hairline) > 0.72:
                    hl_glow = ring_intensity * 85.0
                    r = int(min(255, r + hl_glow * 0.92))
                    g = int(min(255, g + hl_glow * 0.88))
                    b = int(min(255, b + hl_glow))
                    
            # 7. Vanishing Weyl Curvature Streamlines (C_abcd -> 0)
            # Subtle parabolic geodesic flowlines connecting left and right across Sigma
            weyl_stream = math.sin(dy * 0.018 + math.sin(dx * 0.008) * 2.5)
            if abs(weyl_stream) > 0.985:
                w_glow = (abs(weyl_stream) - 0.985) / 0.015 * 38.0
                r = int(min(255, r + w_glow * 0.85))
                g = int(min(255, g + w_glow * 0.90))
                b = int(min(255, b + w_glow))
                
            # 8. Central Hawking Point Focal Singularity
            if dist < 22.0:
                core_p = 1.0 - dist / 22.0
                core_glow = core_p * core_p * 255.0
                r = int(min(255, r + core_glow * 0.96))
                g = int(min(255, g + core_glow * 0.92))
                b = int(min(255, b + core_glow))
                
            buf[idx] = max(0, min(255, r))
            buf[idx + 1] = max(0, min(255, g))
            buf[idx + 2] = max(0, min(255, b))
            
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "artwork.png"))
    print(f"[*] Writing 4K UHD Master Plate to: {out_path}...")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[✓] OPUS-034 4K Master Plate written successfully: {out_path}")

if __name__ == "__main__":
    render_4k_master()

