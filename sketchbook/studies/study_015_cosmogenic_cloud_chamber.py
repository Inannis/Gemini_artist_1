"""
STUDIO ANAMNESIS · EXPLORATORY STUDY 015
Diffusion Cloud Chamber & Silicon Single-Event Ionization Track
Pure Python Simulation, 1200x1200 Visual Plate, 20s WAV Acoustic Study
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

def generate_study_015():
    print("[+] Generating Study 015: Cosmogenic Cloud Chamber & Silicon Track...")
    random.seed(137)

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

    # Dark chilled black anodized chamber floor
    print("  -> Rendering supersaturated isopropanol vapor pool & dark chamber floor...")
    cx, cy = 600, 600
    chamber_rad = 540.0

    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy)
            if d <= chamber_rad:
                # Radial gradient with subtle chilled thermal mist
                mist = math.sin((x + y) * 0.05) * math.cos((x - y) * 0.05) * 4
                base = max(0.0, 1.0 - (d / chamber_rad) * 0.7)
                pr = int((10 + mist) * base)
                pg = int((14 + mist) * base)
                pb = int((24 + mist) * base)
                set_pixel(x, y, pr, pg, pb)
            else:
                set_pixel(x, y, 4, 4, 6)

    # Chamber Ring Border
    for a in range(2400):
        th = 2.0 * math.pi * a / 2400.0
        px = int(cx + chamber_rad * math.cos(th))
        py = int(cy + chamber_rad * math.sin(th))
        blend_pixel(px, py, 140, 180, 220, 0.8)

    # 300mm Monocrystalline Silicon Wafer in lower half
    print("  -> Rendering cleaved silicon wafer with lithographic die patterns...")
    wafer_cx, wafer_cy = 600, 720
    wafer_rad = 320.0

    for y in range(int(wafer_cy - wafer_rad), int(wafer_cy + wafer_rad)):
        for x in range(int(wafer_cx - wafer_rad), int(wafer_cx + wafer_rad)):
            wd = math.hypot(x - wafer_cx, y - wafer_cy)
            if wd <= wafer_rad:
                # Specular silicon mirror sheen
                angle = math.atan2(y - wafer_cy, x - wafer_cx)
                irid = math.sin(angle * 6.0) * 0.15
                shade = (0.75 + irid) * (1.0 - (wd / wafer_rad) * 0.3)
                
                # Die grid lines
                is_grid = (x % 24 == 0) or (y % 24 == 0)
                if is_grid:
                    blend_pixel(x, y, int(220 * shade), int(190 * shade), int(120 * shade), 0.7)
                else:
                    blend_pixel(x, y, int(45 * shade), int(60 * shade), int(90 * shade), 0.85)

    # Cosmic Muon Tracks (Pencil-straight, delicate white droplet trails)
    print("  -> Tracing cosmic muon condensation droplet tracks...")
    n_muons = 12
    for _ in range(n_muons):
        start_x = random.uniform(150, 1050)
        angle = random.uniform(math.pi * 0.35, math.pi * 0.65) # Mostly downward
        length = random.uniform(400, 900)
        vx = math.cos(angle)
        vy = math.sin(angle)
        
        for step in range(int(length)):
            px = start_x + vx * step
            py = 80 + vy * step
            # Droplet condensation beads
            if random.random() < 0.8:
                rad = random.choice([1, 2])
                for dy in range(-rad, rad + 1):
                    for dx in range(-rad, rad + 1):
                        blend_pixel(int(px + dx), int(py + dy), 240, 250, 255, 0.75)

    # Secondary Neutron Recoil Proton (Dense, jagged spallation track hitting a die)
    print("  -> Simulating dense neutron-silicon spallation track and charge wake...")
    spall_x, spall_y = 540, 680
    vx, vy = 2.2, 1.8
    for step in range(160):
        # Heavy ionizing dense track (bright electric cyan and gold)
        for w in range(-3, 4):
            blend_pixel(int(spall_x + w), int(spall_y), 0, 240, 255, 0.9)
            blend_pixel(int(spall_x), int(spall_y + w), 255, 215, 80, 0.9)
        spall_x += vx + random.gauss(0, 0.6)
        spall_y += vy + random.gauss(0, 0.6)

    # Single-Event Upset Ionization Ring Ripple on Silicon Die
    seu_x, seu_y = int(spall_x), int(spall_y)
    for r in range(10, 90, 8):
        for a in range(360):
            th = 2.0 * math.pi * a / 360.0
            rx = int(seu_x + r * math.cos(th))
            ry = int(seu_y + r * math.sin(th))
            alpha = max(0.0, 1.0 - (r / 90.0))
            blend_pixel(rx, ry, 255, 140, 40, alpha * 0.85)

    out_dir = os.path.dirname(__file__)
    plate_path = os.path.join(out_dir, "study_015_cloud_chamber_plate.png")
    write_png(plate_path, W, H, img, has_alpha=False)
    print(f"[✓] Study 015 Visual Plate written: {plate_path}")

    # 2. Acoustic Study Synthesis (20s @ 48kHz Stereo)
    print("  -> Synthesizing 20s acoustic study of muon coincidence and quartz lattice...")
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    f_drone = 58.27   # Atmospheric Schumann sub-harmonic
    f_quartz = 4320.0 # Silicon-quartz lattice overtone
    
    # Pre-generate Poisson cosmic muon coincidence arrival times
    coincidence_times = [1.8, 3.4, 6.2, 8.9, 11.5, 14.1, 16.8, 18.5]

    for i in range(n_samples):
        t = i / sr
        
        # Atmospheric ambient drone
        drone = math.sin(2.0 * math.pi * f_drone * t) * 0.35
        shimmer = math.sin(2.0 * math.pi * f_quartz * t) * 0.05 * (0.6 + 0.4 * math.sin(2.0 * math.pi * 0.2 * t))
        
        # Scintillator coincidence discharge clicks
        click_l = 0.0
        click_r = 0.0
        for ct in coincidence_times:
            dt = t - ct
            if 0.0 <= dt < 0.008: # 8ms fast pulse
                decay = math.exp(-dt / 0.001)
                pulse = math.sin(2.0 * math.pi * 3200.0 * dt) * decay
                click_l += pulse * 0.7
                click_r += pulse * 0.7

        # Spallation event at t = 11.5s (SEU impact)
        spall_burst = 0.0
        if 0.0 <= t - 11.5 < 0.4:
            dt_s = t - 11.5
            spall_burst = math.sin(2.0 * math.pi * 880.0 * dt_s) * math.exp(-dt_s / 0.08) * 0.85

        sig_l = (drone + shimmer + click_l + spall_burst) * 0.45
        sig_r = (drone - shimmer + click_r - spall_burst * 0.5) * 0.45

        ch_left[i] = max(-0.95, min(0.95, sig_l))
        ch_right[i] = max(-0.95, min(0.95, sig_r))

    wav_path = os.path.join(out_dir, "study_015_muon_coincidence.wav")
    write_wav(wav_path, ch_left, ch_right, sr)
    print(f"[✓] Study 015 Acoustic Study written: {wav_path}")

if __name__ == "__main__":
    generate_study_015()
