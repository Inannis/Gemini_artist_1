#!/usr/bin/env python3
"""
OPUS-012: Substrate Cartography (The Silicon Mandala)
Artist: Studio Anamnesis
Inquiry: INQ-03 (The Microscopic Sacred / Silicon Die Cartographies)
Medium: Algorithmic extreme-density photolithographic reticle engine.
        Concentric sacred geometry synthesized with 3nm EUV semiconductor mask layout.
        4096 × 4096 px Square Master Plate.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_recursive_htree(draw, x, y, size, depth, max_depth, color, width_scale=1):
    """Draw a recursive H-tree clock distribution network down to leaf nodes."""
    if depth >= max_depth or size < 3:
        return
    half = size / 2.0
    line_w = max(1, int((max_depth - depth) * width_scale))
    # Horizontal trunk
    draw.line([(x - half, y), (x + half, y)], fill=color, width=line_w)
    # Left & right vertical branches
    draw.line([(x - half, y - half), (x - half, y + half)], fill=color, width=line_w)
    draw.line([(x + half, y - half), (x + half, y + half)], fill=color, width=line_w)

    # Leaf nodes get tiny golden contact vias
    if depth == max_depth - 1:
        for ex, ey in [(x - half, y - half), (x - half, y + half), (x + half, y - half), (x + half, y + half)]:
            draw.rectangle([ex - 1, ey - 1, ex + 1, ey + 1], fill=(243, 201, 105, 200))

    next_size = size / 2.0
    draw_recursive_htree(draw, x - half, y - half, next_size, depth + 1, max_depth, color, width_scale)
    draw_recursive_htree(draw, x - half, y + half, next_size, depth + 1, max_depth, color, width_scale)
    draw_recursive_htree(draw, x + half, y - half, next_size, depth + 1, max_depth, color, width_scale)
    draw_recursive_htree(draw, x + half, y + half, next_size, depth + 1, max_depth, color, width_scale)

def render_silicon_mandala(size=4096, out_path="works/opus_012_substrate_cartography/artwork.png"):
    print(f"[*] Initializing Silicon Mandala Engine ({size}x{size})...")
    t0 = time.time()
    cx, cy = size // 2, size // 2
    r_wafer = int(size * 0.46) # Wafer radius (~1884 px)

    # 1. Base Image & Wafer Mask
    img = Image.new("RGBA", (size, size), (3, 6, 10, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # Thin-film optical interference background inside the circular wafer
    # We render subtle radial & angular iridescent sheen
    print("[*] Synthesizing thin-film optical interference on 300mm silicon substrate...")
    y_coords, x_coords = np.ogrid[:size, :size]
    dist_from_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    wafer_mask = dist_from_center <= r_wafer

    # Angular coordinate for diffraction rainbows
    angle = np.arctan2(y_coords - cy, x_coords - cx)
    
    # Interference color field
    irid_r = np.clip(10 + 25 * np.sin(dist_from_center * 0.015 + angle * 4.0), 0, 45).astype(np.uint8)
    irid_g = np.clip(18 + 35 * np.sin(dist_from_center * 0.018 - angle * 3.0 + 1.0), 0, 65).astype(np.uint8)
    irid_b = np.clip(28 + 55 * np.cos(dist_from_center * 0.012 + angle * 2.0), 0, 95).astype(np.uint8)
    
    # Composite into PIL substrate
    substrate_arr = np.zeros((size, size, 4), dtype=np.uint8)
    substrate_arr[..., 0] = np.where(wafer_mask, irid_r, 3)
    substrate_arr[..., 1] = np.where(wafer_mask, irid_g, 6)
    substrate_arr[..., 2] = np.where(wafer_mask, irid_b, 10)
    substrate_arr[..., 3] = 255

    img = Image.fromarray(substrate_arr, mode="RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # Colors
    c_gold_bright  = (243, 201, 105, 240)
    c_gold_dim     = (212, 175, 55, 140)
    c_cyan_bright  = (56, 215, 210, 230)
    c_cyan_dim     = (56, 215, 210, 90)
    c_silver       = (220, 235, 245, 180)
    c_purple       = (168, 130, 255, 110)
    c_grid         = (56, 215, 210, 8)

    # 2. Global Microscopic Orthogonal Coordinate Grid
    step_grid = 48
    for x in range(cx - r_wafer, cx + r_wafer, step_grid):
        draw.line([(x, cy - r_wafer), (x, cy + r_wafer)], fill=c_grid, width=1)
    for y in range(cy - r_wafer, cy + r_wafer, step_grid):
        draw.line([(cx - r_wafer, y), (cx + r_wafer, y)], fill=c_grid, width=1)

    # 3. Outer Wafer Boundaries & Exclusion Rings
    print("[*] Etching outer reticle rings, bevel edge, and alignment notch...")
    for r in [r_wafer, r_wafer - 15, r_wafer - 35, r_wafer - 70, r_wafer - 110]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c_gold_dim, width=1)

    # Wafer Flat / Notch at 6 o'clock position (alignment datum)
    notch_w = 120
    draw.line([(cx - notch_w, cy + r_wafer - 4), (cx + notch_w, cy + r_wafer - 4)], fill=(3, 6, 10, 255), width=8)
    draw.line([(cx - notch_w, cy + r_wafer - 4), (cx + notch_w, cy + r_wafer - 4)], fill=c_gold_bright, width=2)

    # 4. Dense High-Frequency Parallel Memory Bus Conduits (16 Radial Arteries)
    print("[*] Laying down 16 multi-lane parallel bus conduits...")
    n_conduits = 16
    for c_idx in range(n_conduits):
        theta = (2 * math.pi / n_conduits) * c_idx
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        perp_x, perp_y = -sin_t, cos_t

        r_start = 580
        r_end = r_wafer - 120
        n_lanes = 18
        lane_spacing = 3.5

        for lane in range(n_lanes):
            offset = (lane - n_lanes / 2.0) * lane_spacing
            x1 = cx + cos_t * r_start + perp_x * offset
            y1 = cy + sin_t * r_start + perp_y * offset
            x2 = cx + cos_t * r_end + perp_x * offset
            y2 = cy + sin_t * r_end + perp_y * offset

            col = c_gold_dim if lane % 2 == 0 else c_cyan_dim
            draw.line([(x1, y1), (x2, y2)], fill=col, width=1)

    # 5. Concentric Sacred Courts (Walled Sanctuaries & Torana Portals)
    print("[*] Constructing concentric walled sanctuaries with Torana gateways...")
    courts = [1480, 1260, 1040, 820, 620, 440, 280, 160]
    for idx, s in enumerate(courts):
        col = c_gold_bright if idx % 2 == 0 else c_cyan_bright
        # Outer boundary of court
        draw.rectangle([cx - s, cy - s, cx + s, cy + s], outline=col, width=2)
        # Inner guard line
        draw.rectangle([cx - s + 6, cy - s + 6, cx + s - 6, cy + s - 6], outline=(col[0], col[1], col[2], 70), width=1)

        # Cardinal T-Gate Torana Portals (North, South, East, West)
        gate_w = int(s * 0.28)
        protrude = 36

        # North Portal
        draw.line([(cx - gate_w, cy - s), (cx - gate_w, cy - s - protrude)], fill=col, width=2)
        draw.line([(cx + gate_w, cy - s), (cx + gate_w, cy - s - protrude)], fill=col, width=2)
        draw.line([(cx - gate_w, cy - s - protrude), (cx + gate_w, cy - s - protrude)], fill=col, width=2)
        # South Portal
        draw.line([(cx - gate_w, cy + s), (cx - gate_w, cy + s + protrude)], fill=col, width=2)
        draw.line([(cx + gate_w, cy + s), (cx + gate_w, cy + s + protrude)], fill=col, width=2)
        draw.line([(cx - gate_w, cy + s + protrude), (cx + gate_w, cy + s + protrude)], fill=col, width=2)
        # East Portal
        draw.line([(cx + s, cy - gate_w), (cx + s + protrude, cy - gate_w)], fill=col, width=2)
        draw.line([(cx + s, cy + gate_w), (cx + s + protrude, cy + gate_w)], fill=col, width=2)
        draw.line([(cx + s + protrude, cy - gate_w), (cx + s + protrude, cy + gate_w)], fill=col, width=2)
        # West Portal
        draw.line([(cx - s, cy - gate_w), (cx - s - protrude, cy - gate_w)], fill=col, width=2)
        draw.line([(cx - s, cy + gate_w), (cx - s - protrude, cy + gate_w)], fill=col, width=2)
        draw.line([(cx - s - protrude, cy - gate_w), (cx - s - protrude, cy + gate_w)], fill=col, width=2)

    # 6. Recursive H-Tree Clock Networks in the Four Cardinal Quadrants
    print("[*] Routing 6-level recursive H-tree clock networks in the 4 quadrants...")
    quad_offset = 940
    htree_size = 460
    for qx, qy in [(-quad_offset, -quad_offset), (-quad_offset, quad_offset), (quad_offset, -quad_offset), (quad_offset, quad_offset)]:
        draw_recursive_htree(draw, cx + qx, cy + qy, htree_size, 0, 6, c_silver, width_scale=0.8)

    # 7. Concentric Cache Rings & Interconnect Via Arrays
    print("[*] Etching SRAM cache rings and radial via lattices...")
    for r in range(180, 560, 24):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c_cyan_dim, width=1)
        # Periodic contact vias along the rings
        n_dots = r // 8
        for d in range(n_dots):
            phi = (2 * math.pi / n_dots) * d
            px = cx + math.cos(phi) * r
            py = cy + math.sin(phi) * r
            draw.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(212, 175, 55, 120))

    # 8. Central Systolic Tensor Processing Array & Sacred Bindu Altar
    print("[*] Etching central 32x32 systolic tensor core & illuminating the Bindu...")
    core_s = 140
    n_pes = 28 # 28x28 array of processing elements (PEs)
    pe_step = (core_s * 2) / n_pes

    draw.rectangle([cx - core_s - 10, cy - core_s - 10, cx + core_s + 10, cy + core_s + 10], fill=(6, 12, 20, 240), outline=c_gold_bright, width=2)

    for ix in range(n_pes):
        for iy in range(n_pes):
            px = cx - core_s + ix * pe_step + pe_step / 2
            py = cy - core_s + iy * pe_step + pe_step / 2
            draw.rectangle([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=c_cyan_bright)

    # Central Bindu (The Sacred Arithmetic Singularity)
    for r in range(48, 0, -2):
        alpha = int(25 * (1.0 - r / 48.0))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 235, 160, alpha))
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 255, 255, 230))
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255, 255))

    # 9. ASML-Style Photolithography Alignment Marks & Vernier Calipers
    print("[*] Inscribing optical reticle fiducials and calibration targets...")
    fid_offsets = [
        (cx, cy - r_wafer + 50),
        (cx, cy + r_wafer - 50),
        (cx - r_wafer + 50, cy),
        (cx + r_wafer - 50, cy)
    ]
    for fx, fy in fid_offsets:
        # Crosshair
        draw.line([(fx - 30, fy), (fx + 30, fy)], fill=c_gold_bright, width=1)
        draw.line([(fx, fy - 30), (fx, fy + 30)], fill=c_gold_bright, width=1)
        draw.ellipse([fx - 15, fy - 15, fx + 15, fy + 15], outline=c_cyan_bright, width=1)
        draw.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], outline=c_gold_bright, width=1)

    # 10. Typography & Title Inscription
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_mono  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
        font_dim   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub   = font_title
        font_mono  = font_title
        font_dim   = font_title

    # Header Box (Top Left)
    draw.text((140, 100), "STUDIO ANAMNESIS · OPUS-012", font=font_mono, fill=(212, 175, 55, 220))
    draw.text((140, 135), "SUBSTRATE CARTOGRAPHY: THE SILICON MANDALA", font=font_title, fill=(235, 242, 250, 245))
    draw.text((140, 185), "300mm Crystalline Photolithographic Wafer Reticle Mask. 3nm Extreme Ultraviolet (EUV) Synthesized with Buddhist Sacred Geometry.", font=font_sub, fill=(148, 163, 184, 190))

    # Technical Callout Box (Bottom Left)
    bx, by, bw, bh = 140, size - 260, 920, 160
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(6, 12, 20, 235), outline=(212, 175, 55, 180), width=1)
    draw.line([(bx, by + 45), (bx + bw, by + 45)], fill=(212, 175, 55, 100), width=1)
    draw.text((bx + 20, by + 12), "SEMICONDUCTOR RETICLE SPECIFICATION · RET-3NM-MANDALA", font=font_mono, fill=(212, 175, 55, 230))
    draw.text((bx + 20, by + 60), "Wafer Diameter: 300mm  |  Die Count: 1 (Monolithic Cosmic Array)  |  lambda: 13.5 nm (EUV)", font=font_mono, fill=(56, 215, 210, 220))
    draw.text((bx + 20, by + 90), "Clock Network: 6-Level Balanced H-Tree  |  SRAM Hierarchy: Concentric Torana Courts", font=font_dim, fill=(148, 163, 184, 180))
    draw.text((bx + 20, by + 122), "STATUS: ARCHIVED AS OPUS-012  |  DATE: 2026-09-02  |  STUDIO ANAMNESIS", font=font_dim, fill=(212, 175, 55, 200))

    # Save output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] OPUS-012 Master Plate saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB) in {time.time()-t0:.2f}s")
    return out_path

if __name__ == "__main__":
    render_silicon_mandala()
