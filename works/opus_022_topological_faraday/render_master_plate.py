"""
STUDIO ANAMNESIS · OPUS-022: THE FARADAY MAGNETOMETER
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
    print("[+] Rendering OPUS-022 4K UHD Master Plate (3840 x 2160)...")
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

    # 1. Background Cryo-Vacuum Gradient
    print("  -> Generating background vacuum & coordinate reticle...")
    for y in range(H):
        ny = (y - H/2) / (H/2)
        for x in range(W):
            nx = (x - W/2) / (W/2)
            d = math.sqrt(nx*nx + ny*ny)
            val = max(0.0, 1.0 - 0.45 * d)
            idx = (y * W + x) * 3
            img[idx] = int(4 * val)
            img[idx+1] = int(7 * val)
            img[idx+2] = int(14 * val)
            
            # Subtle coordinate reticle grid lines every 120px
            if x % 120 == 0 or y % 120 == 0:
                img[idx] = min(255, img[idx] + 6)
                img[idx+1] = min(255, img[idx+1] + 10)
                img[idx+2] = min(255, img[idx+2] + 16)

    # 2. Outer Core Geostrophic Taylor Columns (Left Focus)
    print("  -> Rendering Geostrophic Taylor Columns in liquid iron core...")
    core_cx, core_cy = 1100, 1080
    core_radius = 820.0
    icb_radius = core_radius * (1221.5 / 3480.0)

    # Core mantle boundary circle
    for a in range(2400):
        theta = 2.0 * math.pi * a / 2400.0
        px = int(core_cx + core_radius * math.cos(theta))
        py = int(core_cy + core_radius * math.sin(theta))
        blend_pixel(px, py, 90, 140, 200, 0.45)

    # Inner Core Boundary disc
    for y in range(int(core_cy - icb_radius), int(core_cy + icb_radius) + 1):
        for x in range(int(core_cx - icb_radius), int(core_cx + icb_radius) + 1):
            d = math.hypot(x - core_cx, y - core_cy)
            if d <= icb_radius:
                shade = 1.0 - (d / icb_radius) * 0.4
                blend_pixel(x, y, int(55 * shade), int(35 * shade), int(18 * shade), 0.75)

    # 16 Coaxial Geostrophic Taylor Column Cylinders
    num_shells = 16
    for i in range(num_shells):
        s = icb_radius + (i / (num_shells - 1)) * (core_radius - icb_radius)
        phase = (math.pi * i) / (num_shells - 1)
        omega = math.sin(phase)
        
        # Elliptical cylinder boundary
        for a in range(1600):
            theta = 2.0 * math.pi * a / 1600.0
            px = int(core_cx + s * math.cos(theta))
            py = int(core_cy + s * 0.88 * math.sin(theta))
            alpha = 0.15 + abs(omega) * 0.3
            blend_pixel(px, py, 60, 150, 220, alpha)
            
        # Helical Alfvén shear lines on alternate shells
        if i % 2 == 0:
            for a in range(1200):
                theta = 2.0 * math.pi * a / 1200.0
                r_mod = s + math.sin(theta * 6.0) * 12.0
                px = int(core_cx + r_mod * math.cos(theta))
                py = int(core_cy + r_mod * 0.88 * math.sin(theta))
                blend_pixel(px, py, 240, 190, 90, 0.4)

    # 3. 2D Photonic Chern Lattice & Chiral Boundary Mode (Right Focus)
    print("  -> Rendering Magneto-Optic Photonic Chern Lattice...")
    lat_cx, lat_cy = 2640, 1080
    lat_radius = 800.0
    lattice_a = 58.0
    cavity_size = 540.0

    # Draw YIG Ferrite Cylinders (Triangular Lattice)
    rows = 16
    cols = 16
    for r in range(-rows, rows + 1):
        for c in range(-cols, cols + 1):
            px = lat_cx + c * lattice_a + (r % 2) * (lattice_a * 0.5)
            py = lat_cy + r * (lattice_a * math.sqrt(3) * 0.5)
            
            d_center = math.hypot(px - lat_cx, py - lat_cy)
            if d_center < lat_radius:
                in_cavity = (abs(px - lat_cx) < cavity_size * 0.5) and (abs(py - lat_cy) < cavity_size * 0.5)
                if not in_cavity:
                    rod_r = 14.0
                    for ry in range(-15, 16):
                        for rx in range(-15, 16):
                            rd = math.hypot(rx, ry)
                            if rd <= rod_r:
                                shade = 1.0 - (rd / rod_r) * 0.5
                                blend_pixel(int(px + rx), int(py + ry), 
                                            int(70 * shade), int(160 * shade), int(255 * shade), 0.85)

    # 4. Topologically Protected Chiral Boundary Mode with Step Defect
    print("  -> Rendering Chiral Edge Wavepacket & Faraday Vectors...")
    hw = cavity_size * 0.5
    hh = cavity_size * 0.5
    perimeter = []
    pts_per_side = 240

    # Top edge with defect step
    for i in range(pts_per_side):
        f = i / pts_per_side
        x = lat_cx - hw + f * cavity_size
        y = lat_cy - hh
        if 0.4 <= f <= 0.6:
            y += math.sin((f - 0.4) / 0.2 * math.pi) * 75.0 # Defect notch
        perimeter.append((x, y, 0.0))

    # Right edge
    for i in range(pts_per_side):
        f = i / pts_per_side
        perimeter.append((lat_cx + hw, lat_cy - hh + f * cavity_size, math.pi * 0.5))

    # Bottom edge
    for i in range(pts_per_side):
        f = i / pts_per_side
        perimeter.append((lat_cx + hw - f * cavity_size, lat_cy + hh, math.pi))

    # Left edge
    for i in range(pts_per_side):
        f = i / pts_per_side
        perimeter.append((lat_cx - hw, lat_cy + hh - f * cavity_size, math.pi * 1.5))

    # Render Chiral Edge Glow
    for idx, (px, py, base_angle) in enumerate(perimeter):
        wave_phase = idx * 0.08
        intensity = 0.7 + 0.3 * math.sin(wave_phase)
        
        for gy in range(-20, 21):
            for gx in range(-20, 21):
                gd = math.hypot(gx, gy)
                if gd <= 20:
                    glow = math.exp(-gd / 5.2) * intensity
                    blend_pixel(int(px + gx), int(py + gy), 
                                int(glow * 50), int(glow * 240), int(glow * 255), 0.75)

    # Draw Gold Leaf Faraday Polarization Vectors
    num_vectors = 72
    for v in range(num_vectors):
        p_idx = int((v / num_vectors) * len(perimeter))
        px, py, base_angle = perimeter[p_idx]
        
        rot_angle = base_angle + (v / num_vectors) * (math.pi * 4.0)
        v_len = 34.0
        vx = math.cos(rot_angle) * v_len
        vy = math.sin(rot_angle) * v_len
        
        for seg in range(36):
            f = seg / 36.0
            lx = int(px + vx * (f - 0.5))
            ly = int(py + vy * (f - 0.5))
            blend_pixel(lx, ly, 255, 220, 90, 0.9)
            
        # Vector gold bead tip
        for by in range(-3, 4):
            for bx in range(-3, 4):
                if bx*bx + by*by <= 9:
                    set_pixel(int(px + vx * 0.5 + bx), int(py + vy * 0.5 + by), 255, 250, 210)

    # 5. Scientific Framing HUD Borders
    print("  -> Drawing Scientific Cartography Frame...")
    # Outer frame
    for x in range(80, W - 80):
        set_pixel(x, 70, 0, 240, 255)
        set_pixel(x, H - 70, 0, 240, 255)
    for y in range(70, H - 70):
        set_pixel(80, y, 0, 240, 255)
        set_pixel(W - 80, y, 0, 240, 255)

    # Central Divider
    for y in range(120, H - 120):
        if (y // 20) % 2 == 0:
            set_pixel(W // 2, y, 50, 90, 130)

    # Save to works/opus_022_topological_faraday/artwork.png
    out_dir = os.path.dirname(__file__)
    out_png = os.path.join(out_dir, "artwork.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"[✓] 4K Master Plate written: {out_png}")

    # Mirror to gallery/assets/opus_022_artwork.png
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_022_artwork.png"))
    shutil.copyfile(out_png, gallery_asset)
    print(f"[✓] Mirrored to Gallery Asset Vault: {gallery_asset}")

if __name__ == "__main__":
    render_master_plate()
