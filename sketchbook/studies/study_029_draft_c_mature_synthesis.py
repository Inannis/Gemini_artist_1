#!/usr/bin/env python3
"""
STUDY 029 · DRAFT C (MATURE SYNTHESIS)
Series XXXV: Non-Commutative Spacetime & The Moyal Foam
Dual-shell Fuzzy Sphere reliquary, Moyal star-product symplectic field,
UV/IR mixing interference fringes, and 30s 48kHz 5-mode Dirac acoustic suite.
Zero external dependencies (pure Python 3 standard library).
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "telemetry"))
from png_writer import write_png
from audio_writer import write_wav
from noncommutative_metric import NonCommutativeMetric

WIDTH = 1920
HEIGHT = 1080

def render_draft_c_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Telemetry parameters
    nc = NonCommutativeMetric(theta_planck_ratio=1.0, matrix_dim_n=32)
    theta_N = 2.0 / math.sqrt(32 * 32 - 1.0)
    
    # 1. Background: Non-Commutative Moyal Phase Field & Symplectic Waves
    for y in range(HEIGHT):
        ny = (y - cy) / cy # [-1, 1]
        for x in range(WIDTH):
            nx = (x - cx) / cy # aspect ratio preserved
            r = math.sqrt(nx * nx + ny * ny)
            angle = math.atan2(ny, nx)
            
            # Moyal star-product commutator simulation:
            # f * g - g * f = i * theta * (df/dx * dg/dy - df/dy * dg/dx)
            # We evaluate two non-commuting phase waves
            w1 = math.sin(12.0 * nx + 1.5 * math.sin(8.0 * ny))
            w2 = math.cos(12.0 * ny - 1.5 * math.cos(8.0 * nx))
            
            # Symplectic curl interaction
            curl = w1 * w2
            radial_taper = max(0.0, 1.0 - 0.55 * r)
            
            # Paikian electronic beam distortion fringe
            paik_fringe = math.sin(36.0 * r - 4.0 * angle + 2.0 * curl)
            
            lum = max(0.0, 0.045 * radial_taper + 0.02 * paik_fringe * radial_taper)
            
            idx = (y * WIDTH + x) * 3
            buf[idx] = int(255.0 * max(0.0, min(1.0, lum * 0.45 + 0.008 * curl)))       # Deep violet
            buf[idx + 1] = int(255.0 * max(0.0, min(1.0, lum * 0.65 + 0.015 * curl)))   # Cyan edge
            buf[idx + 2] = int(255.0 * max(0.0, min(1.0, lum * 1.10 + 0.025 * curl)))   # Luminous cobalt
            
    # 2. Dual-Shell Fuzzy Sphere Geometry (Outer UV Shell + Inner IR Core)
    shells = [
        {"cells_count": 1024, "radius": 380.0, "yaw": 0.62, "pitch": 0.38, "alpha_mult": 0.85, "core": False},
        {"cells_count": 256,  "radius": 190.0, "yaw": -0.45, "pitch": 0.55, "alpha_mult": 1.00, "core": True}
    ]
    
    all_projected_cells = []
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    
    for sh in shells:
        n_pts = sh["cells_count"]
        rad_px = sh["radius"]
        cos_y, sin_y = math.cos(sh["yaw"]), math.sin(sh["yaw"])
        cos_p, sin_p = math.cos(sh["pitch"]), math.sin(sh["pitch"])
        
        for k in range(n_pts):
            z_k = 1.0 - (2.0 * k + 1.0) / float(n_pts)
            r_xy = math.sqrt(max(0.0, 1.0 - z_k * z_k))
            phi_k = k * golden_angle
            
            x_k = r_xy * math.cos(phi_k)
            y_k = r_xy * math.sin(phi_k)
            
            # Non-commutative matrix perturbation
            dx = theta_N * 0.3 * math.sin(7.0 * phi_k) * z_k
            dy = theta_N * 0.3 * math.cos(7.0 * phi_k) * z_k
            dz = -theta_N * 0.3 * (x_k * math.sin(phi_k) + y_k * math.cos(phi_k))
            
            x_k += dx
            y_k += dy
            z_k += dz
            mag = math.sqrt(x_k * x_k + y_k * y_k + z_k * z_k)
            x_k /= mag
            y_k /= mag
            z_k /= mag
            
            # 3D Rotation
            x1 = x_k * cos_y + z_k * sin_y
            y1 = y_k
            z1 = -x_k * sin_y + z_k * cos_y
            
            x2 = x1
            y2 = y1 * cos_p - z1 * sin_p
            z2 = y1 * sin_p + z1 * cos_p
            
            # Perspective projection
            fov = 1800.0
            dist = fov / (fov + z2 * rad_px * 0.7)
            px = cx + x2 * rad_px * dist
            py = cy - y2 * rad_px * dist
            
            all_projected_cells.append({
                "px": px,
                "py": py,
                "z": z2,
                "dist": dist,
                "core": sh["core"],
                "k": k,
                "rad_px": rad_px
            })
            
    # Sort all cells back to front
    all_projected_cells.sort(key=lambda c: c["z"])
    
    # 3. Draw connecting non-commutative commutator edges between close neighbors
    # For every 8th cell, connect to a neighboring cell to visualize matrix coupling
    for i in range(0, len(all_projected_cells), 12):
        c1 = all_projected_cells[i]
        for j in range(i + 1, min(i + 15, len(all_projected_cells))):
            c2 = all_projected_cells[j]
            if c1["core"] == c2["core"]:
                dx = c1["px"] - c2["px"]
                dy = c1["py"] - c2["py"]
                d_sq = dx * dx + dy * dy
                if d_sq < 2500.0: # within 50px
                    # Draw subtle luminous filament
                    steps = int(math.sqrt(d_sq))
                    if steps > 0:
                        light = max(0.1, (c1["z"] + c2["z"] + 2.0) * 0.25)
                        for s in range(steps):
                            lx = int(c1["px"] + (dx * s) / steps)
                            ly = int(c1["py"] + (dy * s) / steps)
                            if 0 <= lx < WIDTH and 0 <= ly < HEIGHT:
                                idx = (ly * WIDTH + lx) * 3
                                buf[idx] = min(255, buf[idx] + int(20 * light))
                                buf[idx + 1] = min(255, buf[idx + 1] + int(50 * light))
                                buf[idx + 2] = min(255, buf[idx + 2] + int(90 * light))
                                
    # 4. Draw quantum cells
    for cell in all_projected_cells:
        px, py, z2, dist, core, k = cell["px"], cell["py"], cell["z"], cell["dist"], cell["core"], cell["k"]
        
        base_r = 3.5 if core else 2.6
        cell_rad = max(1.5, (base_r + 1.8 * z2) * dist)
        rad_ceil = int(math.ceil(cell_rad + 2.0))
        
        light = max(0.12, (z2 + 1.0) * 0.5)
        
        if core:
            # Golden amber core for IR macroscopic pole
            cr = int(255.0 * min(1.0, light * 0.95))
            cg = int(255.0 * min(1.0, light * 0.75))
            cb = int(255.0 * min(1.0, light * 0.35))
        else:
            # Luminous cyan-azure shell for UV microscopic pole
            cr = int(255.0 * min(1.0, light * 0.35))
            cg = int(255.0 * min(1.0, light * 0.78))
            cb = int(255.0 * min(1.0, light * 0.98))
            
        min_x = max(0, int(px - rad_ceil))
        max_x = min(WIDTH, int(px + rad_ceil + 1))
        min_y = max(0, int(py - rad_ceil))
        max_y = min(HEIGHT, int(py + rad_ceil + 1))
        
        for py_i in range(min_y, max_y):
            dy_p = py_i - py
            for px_i in range(min_x, max_x):
                dx_p = px_i - px
                dist_p = math.sqrt(dx_p * dx_p + dy_p * dy_p)
                if dist_p <= cell_rad:
                    alpha = 1.0 - (dist_p / cell_rad) * 0.7
                    idx = (py_i * WIDTH + px_i) * 3
                    buf[idx] = min(255, int(buf[idx] * (1.0 - alpha) + cr * alpha))
                    buf[idx + 1] = min(255, int(buf[idx + 1] * (1.0 - alpha) + cg * alpha))
                    buf[idx + 2] = min(255, int(buf[idx + 2] * (1.0 - alpha) + cb * alpha))
                    
    out_png = os.path.join(os.path.dirname(__file__), "study_029_draft_c_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[DRAFT C] Generated 1080p plate: {out_png}")

def synthesize_draft_c_audio():
    sample_rate = 48000
    duration_s = 30.0
    total_samples = int(sample_rate * duration_s)
    
    # 5 Dirac operator modes on Fuzzy Sphere:
    # f_n = 55.0 * (n + 0.5)
    modes = [
        {"freq": 27.50, "amp": 0.42, "pan_l": 0.50, "pan_r": 0.50, "phase": 0.0},  # Fundamental A0
        {"freq": 82.50, "amp": 0.30, "pan_l": 0.70, "pan_r": 0.30, "phase": 1.2},  # E2
        {"freq": 137.50, "amp": 0.22, "pan_l": 0.30, "pan_r": 0.70, "phase": 2.4}, # C#3
        {"freq": 192.50, "amp": 0.16, "pan_l": 0.60, "pan_r": 0.40, "phase": 3.6}, # G3
        {"freq": 247.50, "amp": 0.10, "pan_l": 0.40, "pan_r": 0.60, "phase": 4.8}, # B3
    ]
    
    left_samples = []
    right_samples = []
    
    theta_mod_strength = 0.25 # Non-commutative Moyal phase modulation
    
    for i in range(total_samples):
        t = float(i) / sample_rate
        
        # 3-Stage Dynamic Envelope
        if t < 5.0:
            env = 0.5 * (1.0 - math.cos(math.pi * t / 5.0))
        elif t > 23.0:
            env = 0.5 * (1.0 + math.cos(math.pi * (t - 23.0) / 7.0))
        else:
            env = 1.0
            
        # Non-commutative cross-frequency phase modulation (Moyal bracket acoustic transduction)
        cross_phase = math.sin(2.0 * math.pi * 0.2 * t) * math.sin(2.0 * math.pi * 27.5 * t)
        
        s_left = 0.0
        s_right = 0.0
        
        for m in modes:
            # Dynamic pan modulation (slow spatial orbit)
            orbit = 0.15 * math.sin(2.0 * math.pi * 0.08 * t + m["phase"])
            pan_l = max(0.0, min(1.0, m["pan_l"] + orbit))
            pan_r = max(0.0, min(1.0, m["pan_r"] - orbit))
            
            # Non-linear Moyal phase modulation
            phase_t = 2.0 * math.pi * m["freq"] * t + theta_mod_strength * cross_phase + m["phase"]
            sig = math.sin(phase_t) * m["amp"]
            
            s_left += sig * pan_l
            s_right += sig * pan_r
            
        # Soft limiter / saturation
        left_samples.append(math.tanh(s_left * env))
        right_samples.append(math.tanh(s_right * env))
        
    out_wav = os.path.join(os.path.dirname(__file__), "study_029_draft_c_audio.wav")
    write_wav(out_wav, left_samples, right_samples, sample_rate)
    print(f"[DRAFT C] Generated 30s 48kHz audio: {out_wav}")

if __name__ == "__main__":
    render_draft_c_plate()
    synthesize_draft_c_audio()
