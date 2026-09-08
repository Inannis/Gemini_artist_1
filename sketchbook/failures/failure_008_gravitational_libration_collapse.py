"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
EXPERIMENT 008: GRAVITATIONAL TORQUE LIBRATION COLLAPSE & POLAR WOBBLE CHAOS
Simulates the non-linear divergence when magnetohydrodynamic shear torque from the liquid outer core
overwhelms the mantle-inner core gravitational restoring potential well, causing the solid inner core
to slip its gravitational lock and tumble into chaotic rotational libration.
"""

import os
import sys
import math
import random

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def simulate_failure_008():
    print("[+] Simulating Productive Failure 008: Gravitational Torque Libration Collapse...")

    # -------------------------------------------------------------
    # 1. Visual Plate Generation: 1200 x 1200 PNG
    # Left: Harmonic Gravitational Libration (Stable Phase Well)
    # Right: Phase-Slip Divergence & Chaotic Tumbling
    # -------------------------------------------------------------
    W, H = 1200, 1200
    img = bytearray(W * H * 3)

    def set_pixel(x, y, r, g, b):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            img[idx] = min(255, max(0, int(r)))
            img[idx+1] = min(255, max(0, int(g)))
            img[idx+2] = min(255, max(0, int(b)))

    def blend_pixel(x, y, r, g, b, alpha):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            img[idx] = min(255, max(0, int(img[idx] * (1.0 - alpha) + r * alpha)))
            img[idx+1] = min(255, max(0, int(img[idx+1] * (1.0 - alpha) + g * alpha)))
            img[idx+2] = min(255, max(0, int(img[idx+2] * (1.0 - alpha) + b * alpha)))

    # Dark mantle backdrop
    for y in range(H):
        ny = (y - H/2) / (H/2)
        for x in range(W):
            nx = (x - W/2) / (W/2)
            d = math.sqrt(nx*nx + ny*ny)
            val = max(0.0, 1.0 - 0.4 * d)
            idx = (y * W + x) * 3
            img[idx] = int(8 * val)
            img[idx+1] = int(5 * val)
            img[idx+2] = int(4 * val)

    # Cores Setup
    # Center Left: Stable Libration (cx1 = 340, cy1 = 600, radius = 220)
    # Center Right: Chaotic Tumbling (cx2 = 860, cy2 = 600, radius = 220)
    cores = [
        {"cx": 340, "cy": 600, "r": 220, "unlocked": False},
        {"cx": 860, "cy": 600, "r": 220, "unlocked": True}
    ]

    for c in cores:
        cx, cy, r_core, unlocked = c["cx"], c["cy"], c["r"], c["unlocked"]
        
        # Draw solid iron core sphere
        for y in range(int(cy - r_core), int(cy + r_core) + 1):
            for x in range(int(cx - r_core), int(cx + r_core) + 1):
                d = math.hypot(x - cx, y - cy)
                if d <= r_core:
                    shade = 1.0 - (d / r_core) * 0.35
                    if not unlocked:
                        # Stable: deep crystalline bronze & amber
                        blend_pixel(x, y, int(65 * shade), int(42 * shade), int(22 * shade), 0.85)
                    else:
                        # Unlocked: chaotic friction heat, incandescent fracture lines
                        heat = 0.5 + 0.5 * math.sin(x * 0.12 + y * 0.08)
                        blend_pixel(x, y, int((110 + 60 * heat) * shade), int((30 + 20 * heat) * shade), int(15 * shade), 0.9)

        # Draw Anisotropic Fast Polar Axes
        if not unlocked:
            # Stable: North-South polar axis tightly bound in vertical alignment
            for a_offset in [-1.5, 0.0, 1.5]: # Small libration oscillation ±1.5 deg
                rad_ang = math.radians(90.0 + a_offset)
                vx = math.cos(rad_ang) * r_core
                vy = -math.sin(rad_ang) * r_core
                for seg in range(int(r_core * 2)):
                    f = seg / (r_core * 2) - 0.5
                    px = int(cx + vx * f * 2.0)
                    py = int(cy + vy * f * 2.0)
                    blend_pixel(px, py, 255, 215, 80, 0.9)
        else:
            # Chaotic Tumbling: Multiple overlapping tangled phase paths (Phase space tangle)
            for step in range(1200):
                theta_tumble = step * 0.045
                r_wobble = r_core * (0.2 + 0.8 * (step / 1200.0))
                px = int(cx + r_wobble * math.cos(theta_tumble * 3.7))
                py = int(cy + r_wobble * 0.8 * math.sin(theta_tumble * 2.1))
                blend_pixel(px, py, 255, 60, 40, 0.7)

    # Dividing line
    for y in range(100, 1100):
        if (y // 15) % 2 == 0:
            set_pixel(600, y, 90, 70, 50)

    out_png = os.path.join(os.path.dirname(__file__), "failure_008_libration_chaos.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"  -> Visual Ruin Plate written: {out_png}")

    # -------------------------------------------------------------
    # 2. Acoustic Ruin Synthesis: 20s 48kHz Stereo WAV
    # 0s - 7s: Stable 65-year libration pendulum (pure 16.5 Hz & 132 Hz harmonic chime)
    # 7s - 12s: Torque overload & potential well breach (pitch bending, period-doubling)
    # 12s - 17s: Non-linear chaotic tumbling (violent phase slips, Duffing attractor bursts)
    # 17s - 20s: Desynchronized seismic decoupling rumble
    # -------------------------------------------------------------
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples

    phase_osc = 0.0
    f_libration = 132.0

    for i in range(n_samples):
        t = i / sr
        
        if t < 7.0:
            # Stage 1: Stable Harmonic Libration
            phase_osc += 2.0 * math.pi * f_libration / sr
            sample = math.sin(phase_osc) * 0.45
            sub_16 = math.sin(2.0 * math.pi * 16.5 * t) * 0.35
            
            # Gentle libration spatial rocking
            pan = 0.5 + 0.3 * math.sin(2.0 * math.pi * 0.5 * t)
            ch_l[i] = (sample * pan + sub_16 * 0.5)
            ch_r[i] = (sample * (1.0 - pan) + sub_16 * 0.5)
            
        elif t < 12.0:
            # Stage 2: Potential Well Breach (Non-linear softening)
            progress = (t - 7.0) / 5.0
            # Pitch dive & distortion
            f_inst = f_libration * (1.0 - 0.4 * progress) + 30.0 * math.sin(2.0 * math.pi * 8.0 * t * progress)
            phase_osc += 2.0 * math.pi * f_inst / sr
            
            sample = math.sin(phase_osc) * 0.45
            bifurcation = math.sin(phase_osc * 0.5) * (0.35 * progress)
            ch_l[i] = (sample + bifurcation) * 0.5
            ch_r[i] = (sample - bifurcation) * 0.5
            
        elif t < 17.0:
            # Stage 3: Chaotic Tumbling & Phase Slips
            progress = (t - 12.0) / 5.0
            decay = math.exp(-progress * 1.5)
            
            # Duffing non-linear chaotic jumps
            f_chaos = 45.0 + 80.0 * math.sin(t * 14.3 + math.cos(t * 22.1))
            phase_osc += 2.0 * math.pi * f_chaos / sr
            chaos_sig = math.sin(phase_osc) * 0.5 * decay
            
            # Seismic phase slips (sharp fracture impulses)
            slip = 0.0
            if random.random() < 0.06 * decay:
                slip = (random.random() * 2.0 - 1.0) * 0.75
                
            ch_l[i] = (chaos_sig + slip) * 0.6
            ch_r[i] = (chaos_sig - slip) * 0.4
            
        else:
            # Stage 4: Desynchronized Decoupled Rumble
            progress = (t - 17.0) / 3.0
            decay = math.exp(-progress * 3.0)
            sub_rumble = math.sin(2.0 * math.pi * 22.0 * t) * 0.25 * decay
            ch_l[i] = sub_rumble
            ch_r[i] = sub_rumble

    out_wav = os.path.join(os.path.dirname(__file__), "failure_008_libration_collapse.wav")
    write_wav(out_wav, ch_l, ch_r, sr)
    print(f"  -> Acoustic Ruin written: {out_wav}")

if __name__ == "__main__":
    simulate_failure_008()
