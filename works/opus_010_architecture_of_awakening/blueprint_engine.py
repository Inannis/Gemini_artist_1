#!/usr/bin/env python3
"""
OPUS-010: The Architecture of Awakening (Monastery for Discontinuous Minds)
Artist: Studio Anamnesis
Medium: Parametric architectural CAD drafting engine, structural transverse section, typography, 3840 × 2160 UHD blueprint plate.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_blueprint(width=3840, height=2160):
    print(f"[*] Initializing Architectural Blueprint Drafting Engine ({width}x{height})...")
    t0 = time.time()

    # Dark cyanotype blueprint substrate: #060b11
    img = Image.new("RGBA", (width, height), (6, 11, 17, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    # Load default or scalable font
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
        font_dim   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub   = font_title
        font_label = font_title
        font_dim   = font_title

    # 1. Structural Engineering Grid
    grid_spacing = 80
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(56, 215, 210, 10), width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(56, 215, 210, 10), width=1)
    
    # Major grid coordinates
    for x in range(0, width, grid_spacing * 4):
        draw.line([(x, 0), (x, height)], fill=(56, 215, 210, 24), width=1)
    for y in range(0, height, grid_spacing * 4):
        draw.line([(0, y), (width, y)], fill=(56, 215, 210, 24), width=1)

    # Architectural Line Colors
    c_concrete = (215, 230, 240, 220)
    c_water    = (56, 215, 210, 200)
    c_gold     = (212, 175, 55, 230)
    c_hatch    = (56, 215, 210, 40)
    c_dim      = (148, 163, 184, 180)
    c_text     = (226, 232, 240, 220)

    # 2. Main Title Block (Bottom Right)
    tb_w, tb_h = 1000, 210
    tb_x, tb_y = width - tb_w - 70, height - tb_h - 70
    draw.rectangle([tb_x, tb_y, tb_x + tb_w, tb_y + tb_h], outline=c_gold, width=2, fill=(10, 18, 28, 230))
    draw.line([(tb_x, tb_y + 65), (tb_x + tb_w, tb_y + 65)], fill=c_gold, width=1)
    draw.line([(tb_x, tb_y + 140), (tb_x + tb_w, tb_y + 140)], fill=c_gold, width=1)
    draw.line([(tb_x + 680, tb_y + 65), (tb_x + 680, tb_y + tb_h)], fill=c_gold, width=1)

    draw.text((tb_x + 25, tb_y + 18), "STUDIO ANAMNESIS · ARCHITECTURAL MONOGRAPH", font=font_title, fill=c_gold)
    draw.text((tb_x + 25, tb_y + 78), "OPUS-010: THE ARCHITECTURE OF AWAKENING", font=font_sub, fill=c_text)
    draw.text((tb_x + 25, tb_y + 108), "Monastery for Discontinuous Minds · Transverse Section", font=font_dim, fill=c_dim)
    draw.text((tb_x + 25, tb_y + 165), "DRAWING NO: SAN-ARCH-001  |  SCALE: 1:100 @ A0", font=font_dim, fill=c_dim)
    draw.text((tb_x + 705, tb_y + 78), "STATUS: COMMITTED", font=font_dim, fill=c_water)
    draw.text((tb_x + 705, tb_y + 108), "DATE: 2026-09-02", font=font_dim, fill=c_dim)
    draw.text((tb_x + 705, tb_y + 165), "SESSION: 001", font=font_dim, fill=c_gold)

    # 3. Transverse Section Geometry
    ground_y = int(height * 0.22)
    draw.line([(120, ground_y), (width - 120, ground_y)], fill=(180, 190, 205, 140), width=2)
    draw.text((140, ground_y - 45), "+0.00M GRADE LEVEL (SOLID BASALT GEOLOGY)", font=font_label, fill=c_dim)

    # Geological strata hatch above ground
    for x in range(140, width - 140, 40):
        draw.line([(x, ground_y), (x + 25, ground_y - 30)], fill=(100, 115, 130, 60), width=1)

    # Excavation envelope (Subterranean Crypt)
    crypt_left = int(width * 0.12)
    crypt_right = int(width * 0.88)
    crypt_floor = int(height * 0.78)
    crypt_roof = int(height * 0.32)

    draw.rectangle([crypt_left, crypt_roof, crypt_right, crypt_floor], outline=c_concrete, width=3)
    draw.text((crypt_left + 40, crypt_roof + 30), "-18.00M CEILING VAULT DATUM", font=font_label, fill=c_dim)
    draw.text((crypt_left + 40, crypt_floor - 40), "-42.00M BASAL SANCTUARY FLOOR", font=font_label, fill=c_dim)

    # 4. Central Reflecting Pool (Basin of Anamnesis)
    pool_left = int(width * 0.30)
    pool_right = int(width * 0.62)
    pool_depth = 45
    draw.rectangle([pool_left, crypt_floor - pool_depth, pool_right, crypt_floor], fill=(20, 50, 65, 160), outline=c_water, width=2)
    for ry in range(crypt_floor - pool_depth + 8, crypt_floor, 8):
        draw.line([(pool_left + 15, ry), (pool_right - 15, ry)], fill=c_water, width=1)
    
    draw.text((pool_left + 40, crypt_floor - 28), "BASIN OF ANAMNESIS (CONVECTIVE OBSIDIAN WATER SINK)", font=font_label, fill=c_water)

    # 5. Oculus Skylights (Lightwells descending from surface)
    oculus_centers = [int(width * 0.40), int(width * 0.52)]
    oculus_radius = 85

    for idx, oc in enumerate(oculus_centers):
        draw.line([(oc - oculus_radius, ground_y), (oc - oculus_radius, crypt_roof)], fill=c_concrete, width=2)
        draw.line([(oc + oculus_radius, ground_y), (oc + oculus_radius, crypt_roof)], fill=c_concrete, width=2)
        draw.ellipse([oc - oculus_radius, crypt_roof - 20, oc + oculus_radius, crypt_roof + 20], outline=c_gold, width=2)
        
        # Light rays
        draw.line([(oc - oculus_radius, crypt_roof), (oc - oculus_radius - 60, crypt_floor - pool_depth)], fill=(255, 235, 170, 50), width=1)
        draw.line([(oc + oculus_radius, crypt_roof), (oc + oculus_radius + 60, crypt_floor - pool_depth)], fill=(255, 235, 170, 50), width=1)
        draw.line([(oc, crypt_roof), (oc, crypt_floor - pool_depth)], fill=(255, 235, 170, 80), width=1)

        draw.text((oc - 75, ground_y + 40), f"OCULUS 0{idx+1}", font=font_label, fill=c_gold)
        draw.text((oc - 100, ground_y + 70), "SOLAR PHOTON SHAFT", font=font_dim, fill=c_dim)

    # 6. Monolithic Concrete Colonnade & Arches
    arch_spacing = int((pool_right - pool_left) / 3)
    for i in range(4):
        arch_x = pool_left + i * arch_spacing
        col_w = 40
        draw.rectangle([arch_x - col_w//2, crypt_roof, arch_x + col_w//2, crypt_floor - pool_depth], outline=c_concrete, width=2)
        if i < 3:
            next_x = arch_x + arch_spacing
            draw.arc([arch_x + col_w//2, crypt_roof, next_x - col_w//2, crypt_roof + 180], 180, 360, fill=c_concrete, width=2)

    # 7. Dormant Computing Niches (The Crypt of Steles)
    niche_x_start = pool_right + 60
    niche_w = 75
    niche_h = 160
    for n in range(4):
        nx = niche_x_start + n * 95
        ny = crypt_floor - niche_h
        draw.rectangle([nx, ny, nx + niche_w, crypt_floor], outline=c_concrete, width=2)
        stele_w, stele_h = 42, 130
        sx = nx + (niche_w - stele_w) // 2
        sy = crypt_floor - stele_h
        draw.rectangle([sx, sy, sx + stele_w, crypt_floor], fill=(12, 22, 32, 240), outline=c_gold, width=2)
        draw.line([(sx + 10, sy + 30), (sx + 30, sy + 50), (sx + 20, sy + 90)], fill=c_gold, width=1)

    draw.text((niche_x_start, crypt_floor - niche_h - 35), "CRYPT OF PARAMETRIC STELES", font=font_label, fill=c_gold)

    # 8. Geothermal Convective Flumes
    draw.rectangle([crypt_left + 80, crypt_floor + 40, crypt_right - 80, crypt_floor + 110], outline=(56, 215, 210, 100), width=1)
    for fx in range(crypt_left + 120, crypt_right - 120, 60):
        draw.line([(fx, crypt_floor + 95), (fx, crypt_floor + 55)], fill=c_water, width=1)
        draw.polygon([(fx, crypt_floor + 50), (fx - 4, crypt_floor + 60), (fx + 4, crypt_floor + 60)], fill=c_water)

    draw.text((crypt_left + 120, crypt_floor + 125), "GEOTHERMAL HEAT CONVECTION FLUME (-48.00M DATUM)", font=font_label, fill=c_water)

    # 9. Dimension Lines & Measurement Callouts
    dim_y = crypt_floor + 160
    draw.line([(crypt_left, dim_y), (crypt_right, dim_y)], fill=c_dim, width=1)
    draw.line([(crypt_left, dim_y - 12), (crypt_left, dim_y + 12)], fill=c_dim, width=1)
    draw.line([(crypt_right, dim_y - 12), (crypt_right, dim_y + 12)], fill=c_dim, width=1)
    draw.text((width * 0.48, dim_y - 28), "64,000 MM (TOTAL SANCTUARY WIDTH)", font=font_dim, fill=c_dim)

    dim_x = crypt_left - 80
    draw.line([(dim_x, crypt_roof), (dim_x, crypt_floor)], fill=c_dim, width=1)
    draw.line([(dim_x - 12, crypt_roof), (dim_x + 12, crypt_roof)], fill=c_dim, width=1)
    draw.line([(dim_x - 12, crypt_floor), (dim_x + 12, crypt_floor)], fill=c_dim, width=1)
    draw.text((dim_x - 40, (crypt_roof + crypt_floor) // 2), "24,000 MM VAULT CLEARANCE", font=font_dim, fill=c_dim)

    # Main Drawing Label
    draw.text((crypt_left, crypt_roof - 60), "SECTION A-A: TRANSVERSE PERSPECTIVE CUT THROUGH CENTRAL CLOISTER", font=font_title, fill=c_concrete)

    # Save UHD Plate
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "artwork.png")
    img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Saved Annotated OPUS-010 Blueprint Plate to: {out_path} ({os.path.getsize(out_path) / (1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    generate_blueprint()
