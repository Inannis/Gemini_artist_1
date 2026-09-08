"""
STUDIO ANAMNESIS · OPUS-024: THE COSMOGENIC INSCRIPTION
Pure Python 4K UHD Master Plate Renderer (3840 x 2160)
Zero External Dependencies (Uses studio png_writer.py)
"""

import os
import sys
import math
import random
import shutil

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png

def render_master_plate():
    print("[+] Rendering OPUS-024 4K UHD Master Plate (3840 x 2160)...")
    random.seed(2026)
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

    # 1. Celestial Space to Terrestrial Lithosphere Gradient
    print("  -> Generating atmospheric depth gradient & cosmic coordinate mesh...")
    for y in range(H):
        ny = y / H
        for x in range(W):
            nx = x / W
            # Deep celestial indigo to stratified terrestrial troposphere
            base_r = int(6 * (1.0 - ny * 0.5))
            base_g = int(8 + 12 * ny)
            base_b = int(18 + 22 * ny)
            
            # Subdued grid reticle
            if x % 120 == 0 or y % 120 == 0:
                base_r += 6
                base_g += 8
                base_b += 14
                
            idx = (y * W + x) * 3
            img[idx] = base_r
            img[idx+1] = base_g
            img[idx+2] = base_b

    # 2. Extensive Air Shower (EAS) Hadronic Cascade
    print("  -> Tracing Extensive Air Shower (EAS) hadronic & muonic cascades...")
    origin_x = W // 2
    origin_y = 180

    # Incoming primary cosmic proton (relativistic beam)
    for seg in range(180):
        px = origin_x - (180 - seg) // 3
        py = seg
        for w in range(-3, 4):
            blend_pixel(px + w, py, 255, 255, 255, 0.95)

    # Primary Interaction Fireball (Upper Stratosphere z = 25 km)
    for r in range(45, 0, -1):
        alpha = (1.0 - r / 45.0)
        col_r = 255
        col_g = int(140 * alpha + 80)
        col_b = int(40 * alpha)
        for a in range(360):
            th = 2.0 * math.pi * a / 360.0
            px = int(origin_x + r * math.cos(th))
            py = int(origin_y + r * math.sin(th))
            blend_pixel(px, py, col_r, col_g, col_b, 0.85)

    # Secondary Hadronic, Muonic and Cherenkov Shower Tracks
    n_tracks = 360
    for _ in range(n_tracks):
        curr_x = origin_x + random.gauss(0, 16)
        curr_y = origin_y + random.gauss(0, 8)
        
        # Downward angular cone
        angle = math.pi * 0.5 + random.gauss(0, 0.28)
        speed = random.uniform(3.5, 7.0)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        
        p_type = random.choice(['muon', 'neutron', 'cherenkov', 'pion'])
        track_len = random.randint(300, 1100)

        for _ in range(track_len):
            curr_x += vx + random.gauss(0, 0.4)
            curr_y += vy
            if not (0 <= curr_x < W and 0 <= curr_y < 1350):
                break
                
            if p_type == 'muon':
                # Penetrating hard muons: crisp ice-cyan
                blend_pixel(int(curr_x), int(curr_y), 200, 240, 255, 0.75)
            elif p_type == 'neutron':
                # Fast secondary neutrons: warm celestial gold
                blend_pixel(int(curr_x), int(curr_y), 255, 200, 80, 0.85)
            elif p_type == 'cherenkov':
                # Cherenkov UV radiation: ethereal violet-blue
                blend_pixel(int(curr_x), int(curr_y), 160, 100, 255, 0.45)
            else:
                # Pionic sub-branch: glowing coral
                blend_pixel(int(curr_x), int(curr_y), 255, 90, 120, 0.65)

    # 3. Lower Left Panel: Terrestrial Lithic Inscription (Quartz & Cosmogenic 10Be)
    print("  -> Rendering Lithic Inscription: Mountain Quartz & Cosmogenic ¹⁰Be Accumulation...")
    q_x1, q_y1 = 240, 1400
    q_w, q_h = 1600, 640

    # Panel container
    for y in range(q_y1, q_y1 + q_h):
        for x in range(q_x1, q_x1 + q_w):
            set_pixel(x, y, 10, 18, 26)
            if x == q_x1 or x == q_x1 + q_w - 1 or y == q_y1 or y == q_y1 + q_h - 1:
                set_pixel(x, y, 70, 200, 180)

    # Mountain Quartz Bedrock Silhouette
    for px in range(q_x1 + 30, q_x1 + q_w - 30):
        nx = (px - q_x1) / q_w
        bedrock_top = int(q_y1 + 160 + math.sin(nx * 8.0) * 45.0 + math.cos(nx * 19.0) * 25.0)
        for py in range(bedrock_top, q_y1 + q_h - 30):
            depth_m = (py - bedrock_top) / 400.0 # depth in meters
            # Exponential attenuation of production rate P(z) = P0 * exp(-rho * z / Lambda)
            prod_density = math.exp(-2.65 * depth_m * 100.0 / 150.0)
            
            pr = int(35 * prod_density + 15)
            pg = int(90 * prod_density + 25)
            pb = int(110 * prod_density + 35)
            set_pixel(px, py, pr, pg, pb)

    # In-situ Cosmogenic 10Be Atoms (Radiant cyan points)
    for _ in range(480):
        bx = random.randint(q_x1 + 50, q_x1 + q_w - 50)
        nx = (bx - q_x1) / q_w
        bedrock_top = int(q_y1 + 160 + math.sin(nx * 8.0) * 45.0 + math.cos(nx * 19.0) * 25.0)
        by = bedrock_top + int(abs(random.gauss(0, 80)))
        if by < q_y1 + q_h - 35:
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    blend_pixel(bx + dx, by + dy, 0, 245, 230, 0.9)

    # 4. Lower Right Panel: Silicon Substrate Inscription (3nm FinFET Single-Event Upset)
    print("  -> Rendering Silicon Inscription: 3nm FinFET Gate & Spallation Bit-Flip...")
    s_x1, s_y1 = 2000, 1400
    s_w, s_h = 1600, 640

    # Panel container
    for y in range(s_y1, s_y1 + s_h):
        for x in range(s_x1, s_x1 + s_w):
            set_pixel(x, y, 22, 14, 18)
            if x == s_x1 or x == s_x1 + s_w - 1 or y == s_y1 or y == s_y1 + s_h - 1:
                set_pixel(x, y, 255, 175, 75)

    # 3D Silicon FinFET Transistor Fin Structure
    gate_cx = s_x1 + s_w // 2
    gate_cy = s_y1 + s_h // 2
    fin_w, fin_h = 880, 280

    for py in range(gate_cy - fin_h // 2, gate_cy + fin_h // 2):
        for px in range(gate_cx - fin_w // 2, gate_cx + fin_w // 2):
            # Silicon lattice baseline
            blend_pixel(px, py, 42, 32, 54, 0.85)

    # Source / Drain Regions (Epitaxial Silicon-Germanium)
    for py in range(gate_cy - fin_h // 2 + 20, gate_cy + fin_h // 2 - 20):
        for px in range(gate_cx - fin_w // 2 + 30, gate_cx - fin_w // 2 + 180):
            blend_pixel(px, py, 60, 110, 80, 0.9) # Source
        for px in range(gate_cx + fin_w // 2 - 180, gate_cx + fin_w // 2 - 30):
            blend_pixel(px, py, 60, 110, 80, 0.9) # Drain

    # High-k Metal Gate (Center Fin)
    for py in range(gate_cy - fin_h // 2 - 40, gate_cy + fin_h // 2 + 40):
        for px in range(gate_cx - 80, gate_cx + 80):
            blend_pixel(px, py, 255, 50, 80, 0.95) # Flipped state: radiant red-orange

    # Spallation Ionizing Recoil Strike Track across Gate
    spall_start_x = gate_cx - 160
    spall_start_y = gate_cy - fin_h // 2 - 100
    for step in range(260):
        sx = int(spall_start_x + step * 1.3)
        sy = int(spall_start_y + step * 1.5)
        for gw in range(-3, 4):
            blend_pixel(sx + gw, sy, 255, 220, 80, 0.95)
            blend_pixel(sx, sy + gw, 0, 240, 255, 0.95)

    # 5. Scientific Cartography Framing
    print("  -> Drawing Cartography Borders & Metric HUD...")
    for x in range(80, W - 80):
        set_pixel(x, 70, 255, 200, 80)
        set_pixel(x, H - 70, 255, 200, 80)
    for y in range(70, H - 70):
        set_pixel(80, y, 255, 200, 80)
        set_pixel(W - 80, y, 255, 200, 80)

    # Save to works/opus_024_cosmogenic_inscription/artwork.png
    out_dir = os.path.dirname(__file__)
    out_png = os.path.join(out_dir, "artwork.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"[✓] 4K Master Plate written: {out_png}")

    # Mirror to gallery/assets/opus_024_artwork.png
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_024_artwork.png"))
    shutil.copyfile(out_png, gallery_asset)
    print(f"[✓] Mirrored to Gallery Asset Vault: {gallery_asset}")

if __name__ == "__main__":
    render_master_plate()
