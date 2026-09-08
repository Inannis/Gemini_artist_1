"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 009
Atmospheric Hadronic Shower Cascades & Irreversible Parity Checksum Collapse
Pure Python Simulation, 1200x1200 Visual Plate, 20s WAV Acoustic Ruin
Zero External Dependencies
"""

import os
import sys
import math
import random

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def simulate_failure_009():
    print("[+] Simulating Productive Failure 009: Hadronic Shower & Parity Collapse...")
    random.seed(42)

    # 1. Visual Plate (1200 x 1200)
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

    # Dark atmospheric void background
    for y in range(H):
        ny = y / H
        for x in range(W):
            nx = x / W
            d = math.hypot(nx - 0.5, ny - 0.5)
            val = max(0.0, 1.0 - 0.6 * d)
            set_pixel(x, y, int(8 * val), int(4 * val), int(12 * val))

    # Grid of memory array (64x64 word blocks)
    grid_start_x, grid_start_y = 150, 150
    grid_size = 900
    cell_size = grid_size // 64

    # Simulate hadronic shower core impact at center
    impact_x, impact_y = 600, 600
    shower_energy = 1.4e16 # eV

    # Render Memory Cells
    print("  -> Simulating 4,096 memory cells and hadronic ionization wakes...")
    for row in range(64):
        for col in range(64):
            cx = grid_start_x + col * cell_size + cell_size // 2
            cy = grid_start_y + row * cell_size + cell_size // 2
            
            dist_to_impact = math.hypot(cx - impact_x, cy - impact_y)
            # Ionization density decreases as 1/r^1.8
            ion_density = 12000.0 / ((dist_to_impact + 20.0) ** 1.8)
            
            # Bit flip probability based on charge collection
            q_collected = ion_density * (0.8 + 0.4 * random.random())
            is_flipped = q_collected > 1.25 # Critical charge threshold
            is_multi_upset = q_collected > 3.5 # MCU threshold: breaks SEC-DED ECC

            for py in range(cy - cell_size//2 + 1, cy + cell_size//2):
                for px in range(cx - cell_size//2 + 1, cx + cell_size//2):
                    if is_multi_upset:
                        # Catastrophic corrupted cell (vivid neon crimson / magenta)
                        blend_pixel(px, py, 255, 30, 90, 0.95)
                    elif is_flipped:
                        # Single-bit flip (amber error)
                        blend_pixel(px, py, 255, 170, 40, 0.85)
                    else:
                        # Stable bit (subtle indigo-slate)
                        blend_pixel(px, py, 25, 35, 60, 0.6)

    # Render Hadronic Shower Cascade Tracks (Extensive Air Shower branching)
    print("  -> Tracing branching hadronic cascade tracks...")
    n_tracks = 140
    for _ in range(n_tracks):
        # Ray starts from top atmosphere toward impact
        curr_x = impact_x + random.gauss(0, 12)
        curr_y = 0
        vx = (impact_x - curr_x) / 600.0 + random.gauss(0, 0.15)
        vy = random.uniform(2.5, 4.5)
        
        while curr_y < impact_y + random.gauss(80, 50):
            blend_pixel(int(curr_x), int(curr_y), 160, 220, 255, 0.7)
            curr_x += vx + random.gauss(0, 0.8)
            curr_y += vy
            if random.random() < 0.04: # Hadronic branching sub-cascade
                b_vx = vx + random.choice([-1.5, 1.5]) * random.uniform(0.5, 2.0)
                bx, by = curr_x, curr_y
                for _ in range(35):
                    bx += b_vx
                    by += vy * 0.8
                    blend_pixel(int(bx), int(by), 255, 90, 140, 0.5)

    # Frame and reticle
    for x in range(80, W - 80):
        set_pixel(x, 80, 255, 60, 100)
        set_pixel(x, H - 80, 255, 60, 100)
    for y in range(80, H - 80):
        set_pixel(80, y, 255, 60, 100)
        set_pixel(W - 80, y, 255, 60, 100)

    out_dir = os.path.dirname(__file__)
    plate_path = os.path.join(out_dir, "failure_009_shower_cascade.png")
    write_png(plate_path, W, H, img, has_alpha=False)
    print(f"[✓] Failure 009 Visual Plate written: {plate_path}")

    # 2. Acoustic Ruin Synthesis (20s @ 48kHz Stereo)
    print("  -> Synthesizing 20s acoustic ruin of parity collapse & ionizing spallation...")
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    for i in range(n_samples):
        t = i / sr
        
        # Envelope: calm before impact (0-4s), violent shower impact at t=5s, chaotic collapse (5-20s)
        if t < 5.0:
            env = 0.2
            drone = math.sin(2.0 * math.pi * 128.0 * t) * 0.3
            noise = (random.random() - 0.5) * 0.05
            sig_l = drone + noise
            sig_r = drone - noise
        elif t < 5.5:
            # Impact burst
            burst_env = math.exp(-(t - 5.0) / 0.1)
            sig_l = (random.random() - 0.5) * 1.8 * burst_env
            sig_r = (random.random() - 0.5) * 1.8 * burst_env
        else:
            # Post-cascade parity collapse: bit-flip clicking, dissonant hash collision tones
            decay = math.exp(-(t - 5.5) / 6.0)
            f_err1 = 880.0 * (1.0 + 0.4 * math.sin(2.0 * math.pi * 7.3 * t))
            f_err2 = 941.0 * (1.0 + 0.3 * math.cos(2.0 * math.pi * 11.1 * t))
            
            # Stochastic Poisson bit-flip impulse clicks
            click = 0.8 if random.random() < 0.003 else 0.0
            
            tone_l = math.sin(2.0 * math.pi * f_err1 * t) * 0.25
            tone_r = math.cos(2.0 * math.pi * f_err2 * t) * 0.25
            sub_drone = math.sin(2.0 * math.pi * 37.0 * t) * 0.4
            
            sig_l = (tone_l + sub_drone + click) * (0.3 + 0.7 * decay)
            sig_r = (tone_r + sub_drone - click) * (0.3 + 0.7 * decay)

        ch_left[i] = max(-0.95, min(0.95, sig_l * 0.5))
        ch_right[i] = max(-0.95, min(0.95, sig_r * 0.5))

    wav_path = os.path.join(out_dir, "failure_009_hadronic_spallation.wav")
    write_wav(wav_path, ch_left, ch_right, sr)
    print(f"[✓] Failure 009 Acoustic Ruin written: {wav_path}")

if __name__ == "__main__":
    simulate_failure_009()
