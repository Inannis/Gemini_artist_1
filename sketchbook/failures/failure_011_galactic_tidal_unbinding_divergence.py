"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 011
Experiment: Galactic Tidal Unbinding & Symplectic Energy Divergence at the Jacobi Radius
Series XXIV: The Oort Cloud & Galactic Gravitational Tides

Simulates long-term numerical orbital integration (50 Myr) of space debris at the Oort Cloud horizon (110,000 AU).
Demonstrates the catastrophic breakdown of Keplerian two-body symplectic conservation when crossing the Jacobi tidal boundary.

Zero external dependencies: uses pure Python standard library (math, struct, zlib, random).
Outputs:
1. failure_011_jacobi_unbinding.png (1200 x 1200 diagnostic visual plate)
2. failure_011_tidal_dissolution.wav (20.0s 48kHz stereo acoustic ruin)
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png
from audio_writer import write_wav

def run_experiment():
    print("[+] Executing Productive Failure 011: Galactic Tidal Unbinding...")
    random.seed(30076) # Epoch 30,076 CE seed
    
    sr = 48000
    duration = 20.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # Physics parameters (normalized units: 1 unit = 10,000 AU, 1 time unit = 1 Myr)
    # Sun at (0, 0, 0).
    # Jacobi radius r_J ~ 11.0 units (110,000 AU)
    # Vertical tidal frequency omega_z ~ 0.19 Myr^-1
    omega_z_sq = 0.036
    gm_sun = 1.0
    
    # Particle test batch: 24 particles initialized near r_J with varying inclinations
    particles = []
    for p_idx in range(24):
        rad = 7.0 + p_idx * 0.35 # 70,000 AU to 150,000 AU
        theta = (p_idx / 24.0) * math.pi * 2
        inc = math.radians(15.0 + p_idx * 3.0)
        # Circular-like velocity
        v_mag = math.sqrt(gm_sun / rad) * (0.95 + 0.1 * random.random())
        particles.append({
            "id": p_idx,
            "x": rad * math.cos(theta),
            "y": rad * math.sin(theta) * math.cos(inc),
            "z": rad * math.sin(theta) * math.sin(inc),
            "vx": -v_mag * math.sin(theta),
            "vy": v_mag * math.cos(theta) * math.cos(inc),
            "vz": v_mag * math.cos(theta) * math.sin(inc),
            "trail": [],
            "unbound": False,
            "unbound_time": None
        })
        
    dt = 0.005 # 5,000 years per time step
    total_steps = 4000 # 20 Myr integration
    
    energy_divergence_history = []
    
    for step in range(total_steps):
        t_myr = step * dt
        max_e_error = 0.0
        
        for p in particles:
            if p["unbound"]:
                continue
                
            x, y, z = p["x"], p["y"], p["z"]
            r_sq = x*x + y*y + z*z
            r = math.sqrt(r_sq) + 1e-6
            
            # Accelerations:
            # 1. Solar gravity: a_sun = -GM * r_vec / r^3
            inv_r3 = gm_sun / (r * r_sq)
            ax_sun = -inv_r3 * x
            ay_sun = -inv_r3 * y
            az_sun = -inv_r3 * z
            
            # 2. Galactic disc vertical tidal field: a_tide_z = -omega_z^2 * z
            # (Plus weak radial disc shear: a_tide_x = +4*A*(A-B)*x ~ 0.01 * x)
            az_tide = -omega_z_sq * z
            ax_tide = 0.008 * x
            ay_tide = 0.008 * y
            
            ax = ax_sun + ax_tide
            ay = ay_sun + ay_tide
            az = az_sun + az_tide
            
            # Symplectic Leapfrog step
            p["vx"] += ax * dt
            p["vy"] += ay * dt
            p["vz"] += az * dt
            
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["z"] += p["vz"] * dt
            
            # Energy calculation: E = 0.5 * v^2 - GM / r + 0.5 * omega_z^2 * z^2
            v_sq = p["vx"]**2 + p["vy"]**2 + p["vz"]**2
            e_tot = 0.5 * v_sq - (gm_sun / r) + 0.5 * omega_z_sq * (z**2)
            
            if step % 8 == 0:
                p["trail"].append((p["x"], p["y"], p["z"]))
                
            # Tidal unbinding condition: r > 15.0 units (150,000 AU) and E > 0
            if r > 14.5 and e_tot > 0.0:
                p["unbound"] = True
                p["unbound_time"] = t_myr
                
            max_e_error = max(max_e_error, abs(e_tot))
            
        if step % 20 == 0:
            energy_divergence_history.append((t_myr, max_e_error))

    # Audio synthesis:
    # Sonify the orbital frequency collapse into hyperbolic escape hiss
    phase_slow = 0.0
    phase_fast = 0.0
    for i in range(num_samples):
        t = i / sr
        progress = t / duration # 0 to 1
        
        # Fundamental tidal oscillation frequency (22 Hz drone)
        phase_slow += 2.0 * math.pi * 22.0 / sr
        drone = math.sin(phase_slow) * 0.35
        
        # Keplerian orbital frequency decaying as debris unbinds
        orb_freq = 240.0 * (1.0 - progress * 0.85)
        phase_fast += 2.0 * math.pi * max(15.0, orb_freq) / sr
        kepler_tone = math.sin(phase_fast) * 0.25 * (1.0 - progress * 0.7)
        
        # Unbinding transients: stochastic hyperbolic tearing clicks
        click = 0.0
        if progress > 0.35 and random.random() < (progress * 0.008):
            click = (random.random() - 0.5) * 0.7
            
        # Galactic background thermal noise
        noise = (random.random() - 0.5) * (0.05 + 0.18 * progress)
        
        sig = drone + kepler_tone + click + noise
        audio_l[i] = sig
        audio_r[i] = sig * 0.9 + (random.random() - 0.5) * 0.04

    # Normalize audio
    max_a = max(max(abs(x) for x in audio_l), max(abs(x) for x in audio_r))
    if max_a > 0:
        audio_l = [x / max_a * 0.85 for x in audio_l]
        audio_r = [x / max_a * 0.85 for x in audio_r]
        
    wav_path = os.path.join(os.path.dirname(__file__), "failure_011_tidal_dissolution.wav")
    write_wav(wav_path, audio_l, audio_r, sr)
    print(f"  -> Generated Acoustic Ruin: {wav_path}")

    # Render Visual Plate (1200 x 1200 PNG)
    w, h = 1200, 1200
    pixels = bytearray([6, 8, 14] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    # Grid lines
    for x in range(0, w, 80):
        for y in range(h):
            if y % 4 == 0: set_pixel(x, y, 25, 35, 50, 0.3)
    for y in range(0, h, 80):
        for x in range(w):
            if x % 4 == 0: set_pixel(x, y, 25, 35, 50, 0.3)

    # Upper Main Panel: Orbital Trajectory Map (cx = 600, cy = 450)
    cx, cy = 600, 450
    scale = 22.0 # pixels per 10,000 AU
    
    # Draw Jacobi Tidal Horizon Circle (r_J = 11.0 units -> rad = 242 px)
    jacobi_rad = int(11.0 * scale)
    for a_deg in range(0, 360, 2):
        rad_ang = math.radians(a_deg)
        jx = int(cx + jacobi_rad * math.cos(rad_ang))
        jy = int(cy + jacobi_rad * math.sin(rad_ang))
        set_pixel(jx, jy, 240, 70, 70, 0.6) # Red dashed tidal limit

    # Sun dot
    for ox in (-3, -2, -1, 0, 1, 2, 3):
        for oy in (-3, -2, -1, 0, 1, 2, 3):
            set_pixel(cx + ox, cy + oy, 255, 220, 80, 0.95)

    # Plot particle trails
    for p in particles:
        trail = p["trail"]
        if not trail: continue
        prev_pt = None
        for step_idx, (tx, ty, tz) in enumerate(trail):
            px = int(cx + tx * scale)
            py = int(cy + ty * scale)
            if prev_pt is not None:
                x0, y0 = prev_pt
                steps = max(abs(px - x0), abs(py - y0), 1)
                for s in range(steps + 1):
                    lx = int(x0 + (px - x0) * (s / steps))
                    ly = int(y0 + (py - y0) * (s / steps))
                    # Color shifts from cyan (bound) to crimson (unbound hyperbolic)
                    if p["unbound"] and step_idx > len(trail) // 2:
                        set_pixel(lx, ly, 255, 90, 90, 0.75)
                    else:
                        set_pixel(lx, ly, 70, 180, 240, 0.65)
            prev_pt = (px, py)

    # Lower Panel: Energy Divergence Curve (x: 100 to 1100, y: 850 to 1120)
    bx1, bx2 = 100, 1100
    by1, by2 = 850, 1120
    for x in range(bx1, bx2 + 1):
        set_pixel(x, by1, 80, 100, 140, 0.8)
        set_pixel(x, by2, 80, 100, 140, 0.8)
    for y in range(by1, by2 + 1):
        set_pixel(bx1, y, 80, 100, 140, 0.8)
        set_pixel(bx2, y, 80, 100, 140, 0.8)

    # Plot energy error
    if energy_divergence_history:
        prev_e = None
        max_err = max(e for _, e in energy_divergence_history) or 1.0
        for t_val, err_val in energy_divergence_history:
            px = int(bx1 + (t_val / 20.0) * (bx2 - bx1))
            py = int(by2 - (err_val / max_err) * (by2 - by1 - 20))
            if prev_e:
                x0, y0 = prev_e
                steps = max(abs(px - x0), abs(py - y0), 1)
                for s in range(steps + 1):
                    lx = int(x0 + (px - x0) * (s / steps))
                    ly = int(y0 + (py - y0) * (s / steps))
                    set_pixel(lx, ly, 255, 170, 50, 0.9)
            prev_e = (px, py)

    png_path = os.path.join(os.path.dirname(__file__), "failure_011_jacobi_unbinding.png")
    write_png(png_path, w, h, pixels, has_alpha=False)
    print(f"  -> Generated Visual Diagnostic Plate: {png_path}")

if __name__ == "__main__":
    run_experiment()
