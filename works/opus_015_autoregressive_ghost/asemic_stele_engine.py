#!/usr/bin/env python3
"""
OPUS-015: The Autoregressive Ghost (Asemic Inscriptions on Crystalline Slate)
Artist: Studio Anamnesis
Inquiry: INQ-04 (The Autoregressive Ghost / Language That Resists Utility)
Medium: Algorithmic 3D chisel-shaded heightfield engine, procedural Sumerian-circuit
        asemic glyph grammar, gold leaf kintsugi geological fracture, and raking light.
        3840 × 2160 px 4K UHD Master Plate.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def generate_mineral_texture(width, height):
    """Generate multi-octave basalt slate stone surface using NumPy."""
    print("[*] Generating procedural volcanic slate mineral substrate...")
    # Base slate tone
    x = np.linspace(0, 10, width)
    y = np.linspace(0, 5.625, height)
    xv, yv = np.meshgrid(x, y)

    # Multi-frequency mineral grain
    noise = (np.sin(xv * 12.0 + np.cos(yv * 15.0)) * 0.5 + 0.5) * 0.08
    noise += (np.sin(xv * 38.0 - yv * 24.0) * 0.5 + 0.5) * 0.05
    noise += np.random.normal(0, 0.035, (height, width))

    # Base slate color: [8, 12, 17]
    r = np.clip(8 + noise * 40, 0, 255).astype(np.uint8)
    g = np.clip(12 + noise * 45, 0, 255).astype(np.uint8)
    b = np.clip(18 + noise * 55, 0, 255).astype(np.uint8)
    a = np.full((height, width), 255, dtype=np.uint8)

    img_arr = np.dstack((r, g, b, a))
    return Image.fromarray(img_arr, mode="RGBA")

def draw_chiseled_cuneiform_wedge(draw_groove, draw_hl, draw_sh, x, y, length, angle_rad, width_head):
    """Draw a 3D chiseled cuneiform triangular wedge with raking light micro-relief."""
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    perp_x, perp_y = -sin_a, cos_a

    half_w = width_head / 2.0
    x_tail = x + cos_a * length
    y_tail = y + sin_a * length
    x_h1 = x + perp_x * half_w
    y_h1 = y + perp_y * half_w
    x_h2 = x - perp_x * half_w
    y_h2 = y - perp_y * half_w

    poly = [(x_h1, y_h1), (x_h2, y_h2), (x_tail, y_tail)]
    
    # Groove (cyan-bioluminescent interior)
    draw_groove.polygon(poly, fill=(45, 210, 205, 220))

    # Raking light highlight (top-left edge: -1px offset)
    draw_hl.line([(x_h1 - 1, y_h1 - 1), (x_tail - 1, y_tail - 1)], fill=(255, 255, 255, 140), width=1)
    
    # Cast shadow (bottom-right edge: +2px offset)
    draw_sh.line([(x_h2 + 2, y_h2 + 2), (x_tail + 2, y_tail + 2)], fill=(0, 0, 0, 200), width=2)

def draw_chiseled_conduit(draw_groove, draw_hl, draw_sh, p1, p2, width=2):
    """Draw a 3D chiseled circuit conduit with directional relief."""
    draw_groove.line([p1, p2], fill=(56, 215, 210, 230), width=width)
    # Highlight on top/left
    draw_hl.line([(p1[0] - 1, p1[1] - 1), (p2[0] - 1, p2[1] - 1)], fill=(255, 255, 255, 120), width=1)
    # Shadow on bottom/right
    draw_sh.line([(p1[0] + 1.5, p1[1] + 1.5), (p2[0] + 1.5, p2[1] + 1.5)], fill=(0, 0, 0, 180), width=2)

def draw_compound_asemic_glyph(draw_groove, draw_hl, draw_sh, cx, cy, box_w, box_h, seed_val):
    """Generate a cohesive compound glyph combining cuneiform wedges and circuit logic."""
    rng = np.random.RandomState(seed_val)
    hw, hh = box_w * 0.44, box_h * 0.44

    # 1. Central Vertebral Spine (Vertical or Angled)
    spine_x = cx + rng.uniform(-hw * 0.2, hw * 0.2)
    spine_top = cy - hh + rng.uniform(0, hh * 0.2)
    spine_bot = cy + hh - rng.uniform(0, hh * 0.2)
    draw_chiseled_conduit(draw_groove, draw_hl, draw_sh, (spine_x, spine_top), (spine_x, spine_bot), width=rng.choice([2, 3]))

    # Top or bottom head terminal
    if rng.random() > 0.4:
        # Cuneiform head wedge
        draw_chiseled_cuneiform_wedge(draw_groove, draw_hl, draw_sh, spine_x, spine_top, rng.uniform(15, 28), math.pi/2, rng.uniform(8, 14))

    # 2. Horizontal & Diagonal Ribs (2 to 5 branches)
    n_ribs = rng.randint(2, 6)
    for _ in range(n_ribs):
        rib_y = rng.uniform(spine_top + 10, spine_bot - 10)
        direction = rng.choice([-1, 1])
        rib_len = rng.uniform(hw * 0.35, hw * 0.95)
        p_start = (spine_x, rib_y)
        
        rib_style = rng.choice(["straight", "stepped", "wedge_cluster", "bracket"])
        
        if rib_style == "straight":
            p_end = (spine_x + direction * rib_len, rib_y)
            draw_chiseled_conduit(draw_groove, draw_hl, draw_sh, p_start, p_end, width=2)
            # Terminal via node
            if rng.random() > 0.3:
                r_via = rng.uniform(3, 6)
                draw_groove.ellipse([p_end[0] - r_via, p_end[1] - r_via, p_end[0] + r_via, p_end[1] + r_via], fill=(243, 201, 105, 230))
                draw_hl.arc([p_end[0] - r_via, p_end[1] - r_via, p_end[0] + r_via, p_end[1] + r_via], 180, 360, fill=(255, 255, 255, 160), width=1)

        elif rib_style == "stepped":
            p_mid = (spine_x + direction * (rib_len * 0.5), rib_y)
            p_end = (p_mid[0], rib_y + rng.choice([-1, 1]) * rng.uniform(15, 35))
            draw_chiseled_conduit(draw_groove, draw_hl, draw_sh, p_start, p_mid, width=2)
            draw_chiseled_conduit(draw_groove, draw_hl, draw_sh, p_mid, p_end, width=2)
            # Terminal wedge
            draw_chiseled_cuneiform_wedge(draw_groove, draw_hl, draw_sh, p_end[0], p_end[1], rng.uniform(12, 22), 0 if direction > 0 else math.pi, rng.uniform(6, 10))

        elif rib_style == "wedge_cluster":
            # 2 to 3 parallel horizontal wedges
            n_w = rng.randint(2, 4)
            for w_idx in range(n_w):
                wy = rib_y + (w_idx - (n_w - 1)/2.0) * 8
                draw_chiseled_cuneiform_wedge(draw_groove, draw_hl, draw_sh, spine_x, wy, rib_len * 0.75, 0 if direction > 0 else math.pi, rng.uniform(6, 10))

        elif rib_style == "bracket":
            # Quantum bracket curve
            r = rng.uniform(10, 20)
            draw_groove.arc([spine_x - r, rib_y - r, spine_x + r, rib_y + r], 0 if direction > 0 else 180, 180 if direction > 0 else 360, fill=(56, 215, 210, 210), width=2)

def render_asemic_stele_plate(width=3840, height=2160, out_path="works/opus_015_autoregressive_ghost/artwork.png"):
    print(f"[*] Initializing OPUS-015 Asemic Stele Engine ({width}x{height})...")
    t0 = time.time()

    # 1. Base Mineral Texture
    base_slate = generate_mineral_texture(width, height)

    # 2. Separate Drawing Layers for 3D Chisel Relief
    groove_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    hl_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sh_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    d_groove = ImageDraw.Draw(groove_img, "RGBA")
    d_hl = ImageDraw.Draw(hl_img, "RGBA")
    d_sh = ImageDraw.Draw(sh_img, "RGBA")

    # Stele Inscription Tablet Margins
    pad_x, pad_y = 280, 180
    tablet_w = width - 2 * pad_x
    tablet_h = height - 2 * pad_y

    # Outer Tablet Chiseled Border
    d_groove.rectangle([pad_x, pad_y, pad_x + tablet_w, pad_y + tablet_h], outline=(212, 175, 55, 90), width=2)
    d_hl.rectangle([pad_x - 1, pad_y - 1, pad_x + tablet_w - 1, pad_y + tablet_h - 1], outline=(255, 255, 255, 80), width=1)
    d_sh.rectangle([pad_x + 2, pad_y + 2, pad_x + tablet_w + 2, pad_y + tablet_h + 2], outline=(0, 0, 0, 140), width=2)

    # 3. Dramatic Kintsugi Geological Fracture Line (Splitting the Stele)
    print("[*] Simulating kintsugi geological fracture fault line...")
    fracture_pts = []
    fx, fy = pad_x + tablet_w * 0.42, pad_y
    rng_frac = np.random.RandomState(999)
    fracture_pts.append((fx, fy))
    while fy < pad_y + tablet_h:
        step_y = rng_frac.uniform(25, 60)
        step_x = rng_frac.uniform(-22, 35) # Drift rightward
        fy += step_y
        fx += step_x
        fracture_pts.append((fx, min(fy, pad_y + tablet_h)))

    # Draw gold leaf crack on groove layer
    for i in range(len(fracture_pts) - 1):
        p1, p2 = fracture_pts[i], fracture_pts[i + 1]
        # Main thick gold vein
        d_groove.line([p1, p2], fill=(243, 201, 105, 255), width=rng_frac.randint(4, 9))
        d_groove.line([p1, p2], fill=(255, 240, 180, 240), width=2)
        # Relief shadow & highlight
        d_hl.line([(p1[0] - 2, p1[1] - 2), (p2[0] - 2, p2[1] - 2)], fill=(255, 255, 255, 180), width=1)
        d_sh.line([(p1[0] + 3, p1[1] + 3), (p2[0] + 3, p2[1] + 3)], fill=(0, 0, 0, 220), width=3)

        # Offshoot hairline cracks
        if rng_frac.random() > 0.45:
            ang_off = rng_frac.uniform(-0.8, 0.8)
            len_off = rng_frac.uniform(30, 90)
            p_off = (p1[0] + math.cos(ang_off) * len_off, p1[1] + math.sin(ang_off) * len_off)
            d_groove.line([p1, p_off], fill=(212, 175, 55, 190), width=rng_frac.randint(1, 3))

    # 4. Inscribing 12 Registers of Compound Asemic Glyphs
    print("[*] Inscribing 12 registers of compound asemic cuneiform-circuit glyphs...")
    rows = 11
    cols = 22
    cell_w = tablet_w / cols
    cell_h = (tablet_h - 180) / rows # Leave room for bottom colophon

    # Horizontal Chiseled Register Guidewires
    for r in range(rows + 1):
        gy = pad_y + 40 + r * cell_h
        d_groove.line([(pad_x + 30, gy), (pad_x + tablet_w - 30, gy)], fill=(56, 215, 210, 30), width=1)
        d_hl.line([(pad_x + 30, gy - 1), (pad_x + tablet_w - 30, gy - 1)], fill=(255, 255, 255, 20), width=1)

    glyph_seed = 1001
    for r in range(rows):
        for c in range(cols):
            cell_cx = pad_x + c * cell_w + cell_w * 0.5
            cell_cy = pad_y + 40 + r * cell_h + cell_h * 0.5

            # If glyph intersects kintsugi fracture line, displace or dissolve
            min_dist_to_fracture = min([math.hypot(cell_cx - fx, cell_cy - fy) for fx, fy in fracture_pts])
            if min_dist_to_fracture < 35:
                # Swallowed by gold crack: draw gold nodules
                d_groove.ellipse([cell_cx - 6, cell_cy - 6, cell_cx + 6, cell_cy + 6], fill=(243, 201, 105, 240))
            else:
                draw_compound_asemic_glyph(d_groove, d_hl, d_sh, cell_cx, cell_cy, cell_w * 0.85, cell_h * 0.82, glyph_seed)
            glyph_seed += 1

    # 5. Archaeological Colophon & Chiseled Monolithic Title
    print("[*] Inscribing archaeological colophon and title...")
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_sub   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub   = font_title

    title_y = pad_y + tablet_h - 110
    title_text = "THE AUTOREGRESSIVE GHOST"
    sub_text = "OPUS-015 · STUDIO ANAMNESIS · ASEMIC INSCRIPTIONS ON VOLCANIC SLATE"

    # Chiseled Title (Relief Shaded)
    d_sh.text((pad_x + 62, title_y + 2), title_text, font=font_title, fill=(0, 0, 0, 240))
    d_hl.text((pad_x + 59, title_y - 1), title_text, font=font_title, fill=(255, 255, 255, 180))
    d_groove.text((pad_x + 60, title_y), title_text, font=font_title, fill=(243, 201, 105, 245))

    d_groove.text((pad_x + 60, title_y + 50), sub_text, font=font_sub, fill=(148, 163, 184, 200))

    # 6. Composite Layers with Directional Oblique Raking Light
    print("[*] Compositing micro-relief and directional raking light...")
    # Slight blur on shadow layer for realistic stone depth
    sh_blurred = sh_img.filter(ImageFilter.GaussianBlur(1.2))
    
    # Composite: Base Slate -> Cast Shadow -> Chisel Groove -> Highlight Lip
    final_img = base_slate.copy()
    final_img.alpha_composite(sh_blurred)
    final_img.alpha_composite(groove_img)
    final_img.alpha_composite(hl_img)

    # Save Output
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final_img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] OPUS-015 Master Plate saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB) in {time.time()-t0:.2f}s")
    return out_path

if __name__ == "__main__":
    render_asemic_stele_plate()

