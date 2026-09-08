"""
STUDIO ANAMNESIS · OPUS-023: THE INNER-CORE EPHEMERIS
Pure Python 4K UHD Master Plate Renderer (3840 x 2160)
Zero External Dependencies (Uses studio png_writer.py)
"""

import os
import sys
import math
import shutil

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

def render_master_plate():
    print("[+] Rendering OPUS-023 4K UHD Master Plate (3840 x 2160)...")
    W, H = 3840, 2160
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

    # 1. Background Terrestrial Abyss Gradient
    print("  -> Generating background abyss & metric reticle...")
    for y in range(H):
        ny = (y - H/2) / (H/2)
        for x in range(W):
            nx = (x - W/2) / (W/2)
            d = math.sqrt(nx*nx + ny*ny)
            val = max(0.0, 1.0 - 0.48 * d)
            idx = (y * W + x) * 3
            img[idx] = int(12 * val)
            img[idx+1] = int(7 * val)
            img[idx+2] = int(4 * val)
            
            if x % 120 == 0 or y % 120 == 0:
                img[idx] = min(255, img[idx] + 8)
                img[idx+1] = min(255, img[idx+1] + 5)
                img[idx+2] = min(255, img[idx+2] + 3)

    # 2. Solid Inner Core Sphere (Center Focus)
    print("  -> Rendering Solid Iron Inner Core Body & Anisotropic Crystalline Grain...")
    cx, cy = 1920, 1020
    radius = 720.0

    # Draw solid iron core sphere with hexagonal crystal grain
    for y in range(int(cy - radius), int(cy + radius) + 1):
        for x in range(int(cx - radius), int(cx + radius) + 1):
            d = math.hypot(x - cx, y - cy)
            if d <= radius:
                # Polar angle
                theta = math.atan2(abs(x - cx), abs(y - cy))
                v_fac = 1.0 + 0.031 * (math.cos(theta)**2) # 3.1% polar fast axis
                
                # Hexagonal close packed iron grain
                grain = math.sin((y - cy) * 0.2) * math.cos((x - cx) * 0.2 + (y - cy) * 0.1)
                shade = (1.0 - (d / radius) * 0.42) * (0.88 + 0.12 * grain)
                
                # Rich bronze, copper, and molten amber metallic palette
                pr = int(175 * shade * (v_fac - 0.15))
                pg = int(105 * shade)
                pb = int(55 * shade)
                blend_pixel(x, y, pr, pg, pb, 0.9)

    # Inner Core Boundary Rim
    for a in range(3600):
        th = 2.0 * math.pi * a / 3600.0
        px = int(cx + radius * math.cos(th))
        py = int(cy + radius * math.sin(th))
        blend_pixel(px, py, 255, 205, 90, 0.85)

    # 3. Polar Fast Axis Shaft (Tilted by current libration angle delta_phi = -0.8995 deg)
    print("  -> Rendering Polar Fast Axis & Seismic Raypaths...")
    lib_angle = math.radians(-0.8995)
    axis_len = radius * 1.25
    vx = math.sin(lib_angle) * axis_len
    vy = -math.cos(lib_angle) * axis_len

    for seg in range(int(axis_len * 2)):
        f = seg / (axis_len * 2) - 0.5
        px = int(cx + vx * f * 2.0)
        py = int(cy + vy * f * 2.0)
        for w_offset in range(-3, 4):
            blend_pixel(px + w_offset, py, 255, 220, 80, 0.9)

    # Seismic Doublet Raypaths
    for seg in range(1200):
        t = seg / 1200.0
        # Ray 1: 1995 Epoch (Phosphor Cyan)
        r1_x = int(cx - radius * 0.85 + t * (radius * 1.7))
        r1_y = int(cy - radius * 0.88 + t * (radius * 1.76) + math.sin(t * math.pi) * 140.0)
        for gw in range(-2, 3):
            blend_pixel(r1_x, r1_y + gw, 0, 240, 255, 0.85)
            # Ray 2: 2026 Epoch (Celestial Amber, shifted by inner core rotation)
            blend_pixel(r1_x + 22, r1_y + gw - 8, 255, 215, 80, 0.85)

    # 4. Seismic Doublet Seismograms (Bottom Panel)
    print("  -> Rendering Seismic Doublet Waveform Traces (+5.12ms delay)...")
    base_y1 = 1860
    base_y2 = 1980
    trace_w = 2800
    start_x = 520

    # Trace borders
    for x in range(start_x, start_x + trace_w):
        set_pixel(x, 1780, 80, 50, 30)
        set_pixel(x, 2060, 80, 50, 30)
    for y in range(1780, 2060):
        set_pixel(start_x, y, 80, 50, 30)
        set_pixel(start_x + trace_w, y, 80, 50, 30)

    for px in range(trace_w):
        t_ms = (px / trace_w) * 100.0 # 0 to 100ms
        
        # 1995 Waveform: centered at 35ms
        dt1 = (t_ms - 35.0) / 4.5
        w1 = (1.0 - 2.0 * dt1*dt1) * math.exp(-dt1*dt1)
        py1 = int(base_y1 - w1 * 45.0)
        for gw in range(-1, 2):
            blend_pixel(start_x + px, py1 + gw, 0, 240, 255, 0.9)

        # 2026 Waveform: centered at 40.12ms (+5.12ms delay)
        dt2 = (t_ms - 40.12) / 4.5
        w2 = (1.0 - 2.0 * dt2*dt2) * math.exp(-dt2*dt2)
        py2 = int(base_y2 - w2 * 45.0)
        for gw in range(-1, 2):
            blend_pixel(start_x + px, py2 + gw, 255, 215, 80, 0.9)

    # 5. Scientific Cartography Framing
    print("  -> Drawing Cartography Borders...")
    for x in range(80, W - 80):
        set_pixel(x, 70, 255, 200, 80)
        set_pixel(x, H - 70, 255, 200, 80)
    for y in range(70, H - 70):
        set_pixel(80, y, 255, 200, 80)
        set_pixel(W - 80, y, 255, 200, 80)

    # Save to works/opus_023_inner_core_ephemeris/artwork.png
    out_dir = os.path.dirname(__file__)
    out_png = os.path.join(out_dir, "artwork.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"[✓] 4K Master Plate written: {out_png}")

    # Mirror to gallery/assets/opus_023_artwork.png
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_023_artwork.png"))
    shutil.copyfile(out_png, gallery_asset)
    print(f"[✓] Mirrored to Gallery Asset Vault: {gallery_asset}")

if __name__ == "__main__":
    render_master_plate()
