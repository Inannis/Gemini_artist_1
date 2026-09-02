#!/usr/bin/env python3
"""
OPUS-008: Heliotropic Cybernetics (The Autonomous Homeostat) - Enhanced Engine
Artist: Studio Anamnesis
Medium: Dense amber glass polygon rasterization, homeostatic solar tracking, radiant volumetric shaft.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw

def generate_heliotrope(width=3840, height=2160, num_petals=120, seed=512):
    print(f"[*] Initializing Enhanced Heliotrope Engine ({width}x{height}, {num_petals} petals)...")
    np.random.seed(seed)
    t0 = time.time()

    # PIL drawing image for clean antialiased polygons + numpy buffer for volumetric optics
    base_img = Image.new("RGBA", (width, height), (10, 14, 20, 255))
    draw = ImageDraw.Draw(base_img, "RGBA")

    # Sun skylight origin (top center-left)
    sun_x = width * 0.48
    sun_y = height * 0.08

    # Organism center
    cx = width * 0.58
    cy = height * 0.54

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    golden_angle = 2.0 * math.pi * (1.0 - 1.0 / phi)

    # 1. Background board-formed concrete lines
    for y in range(0, height, 110):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 6), width=2)
        # Form tie holes
        for x in range(160, width, 420):
            draw.ellipse([x-4, y+55-4, x+4, y+55+4], fill=(5, 7, 10, 220), outline=(255, 255, 255, 12))

    # 2. Draw wall shadow of the sculpture (cast behind)
    shadow_offset_x = -180
    shadow_offset_y = 120
    scx = cx + shadow_offset_x
    scy = cy + shadow_offset_y

    for n in range(num_petals):
        th = n * golden_angle
        r = math.sqrt(n / float(num_petals)) * (height * 0.38)
        px = scx + r * math.cos(th)
        py = scy + r * math.sin(th) * 0.85
        
        # Shadow petal
        angle_to_sun = math.atan2(sun_y - py, sun_x - px)
        orient = th * 0.5 + angle_to_sun * 0.5
        plen = (height * 0.16) * (0.5 + 0.5 * math.sqrt(n / num_petals))
        pw = (height * 0.045)
        
        # Draw shadow ellipse
        s_tip_x = px + plen * math.cos(orient)
        s_tip_y = py + plen * math.sin(orient)
        s_left_x = px + pw * math.cos(orient + math.pi/2) * 0.5
        s_left_y = py + pw * math.sin(orient + math.pi/2) * 0.5
        s_right_x = px + pw * math.cos(orient - math.pi/2) * 0.5
        s_right_y = py + pw * math.sin(orient - math.pi/2) * 0.5

        draw.polygon([(px, py), (s_left_x, s_left_y), (s_tip_x, s_tip_y), (s_right_x, s_right_y)],
                     fill=(4, 6, 9, 75))

    # 3. Bronze Mechanical Central Core (gears, rings, armature)
    for ring_r in [180, 140, 100, 70, 40, 20]:
        alpha = int(120 + ring_r * 0.4)
        draw.ellipse([cx-ring_r, cy-ring_r, cx+ring_r, cy+ring_r],
                     outline=(180, 130, 50, alpha), width=max(2, int(ring_r * 0.04)))
    
    # Gear teeth
    num_teeth = 36
    for i in range(num_teeth):
        ang = (i / num_teeth) * 2 * math.pi
        t_x1 = cx + 90 * math.cos(ang)
        t_y1 = cy + 90 * math.sin(ang)
        t_x2 = cx + 115 * math.cos(ang)
        t_y2 = cy + 115 * math.sin(ang)
        draw.line([(t_x1, t_y1), (t_x2, t_y2)], fill=(210, 155, 65, 200), width=3)

    # 4. Draw Primary Translucent Amber Glass Petals
    for n in range(num_petals):
        th = n * golden_angle
        r = math.sqrt(n / float(num_petals)) * (height * 0.40)
        px = cx + r * math.cos(th)
        py = cy + r * math.sin(th)

        angle_to_sun = math.atan2(sun_y - py, sun_x - px)
        bias = 0.25 + 0.45 * (r / (height * 0.40))
        orient = th * (1.0 - bias) + angle_to_sun * bias

        plen = (height * 0.20) * (0.4 + 0.6 * math.sqrt((n + 10) / num_petals))
        pw = (height * 0.055) * (0.5 + 0.5 * math.sin((n / num_petals) * math.pi))

        # Bezier-like petal outline points
        cos_o = math.cos(orient)
        sin_o = math.sin(orient)
        cos_p = math.cos(orient + math.pi / 2)
        sin_p = math.sin(orient + math.pi / 2)

        tip_x = px + plen * cos_o
        tip_y = py + plen * sin_o
        
        # Flank points
        flank1_x = px + plen * 0.45 * cos_o + pw * cos_p
        flank1_y = py + plen * 0.45 * sin_o + pw * sin_p

        flank2_x = px + plen * 0.45 * cos_o - pw * cos_p
        flank2_y = py + plen * 0.45 * sin_o - pw * sin_p

        # Petal color: radiant honey amber body with luminous golden edge
        depth_factor = n / float(num_petals)
        red_val = int(235 + 20 * depth_factor)
        green_val = int(145 + 50 * depth_factor)
        blue_val = int(35 + 30 * depth_factor)
        alpha_val = int(110 + 60 * math.sin(depth_factor * math.pi))

        draw.polygon([(px, py), (flank1_x, flank1_y), (tip_x, tip_y), (flank2_x, flank2_y)],
                     fill=(red_val, green_val, blue_val, alpha_val),
                     outline=(255, 235, 160, 220))
        
        # Central rib line
        draw.line([(px, py), (tip_x, tip_y)], fill=(255, 245, 200, 180), width=2)

    # 5. Bioluminescent Turquoise Fiber Tendrils
    for i in range(72):
        t_ang = math.pi + np.random.uniform(-0.55, 0.55)
        cur_x = cx + np.random.uniform(-50, 50)
        cur_y = cy + np.random.uniform(-50, 50)
        t_len = np.random.uniform(height * 0.45, height * 0.95)
        
        pts = [(cur_x, cur_y)]
        for s in range(60):
            cur_x += math.cos(t_ang) * (t_len / 60) + math.sin(s * 0.2 + i) * 3.5
            cur_y += math.sin(t_ang) * (t_len / 60) * 0.4 + math.cos(s * 0.15 + i) * 3.0 + 1.2
            pts.append((cur_x, cur_y))
        
        draw.line(pts, fill=(56, 215, 210, 160), width=2)

    # 6. Convert to numpy for Volumetric Light Shaft & Optical Tonemapping
    np_img = np.array(base_img, dtype=np.float32) / 255.0
    rgb = np_img[:, :, :3]

    print("[*] Compositing volumetric sunlight beam...")
    y_grid, x_grid = np.mgrid[0:height, 0:width]
    beam_dx = x_grid - sun_x
    beam_dy = y_grid - sun_y
    beam_angle = np.arctan2(beam_dy, beam_dx)
    target_beam_angle = math.atan2(cy - sun_y, cx - sun_x)

    angle_diff = np.abs(beam_angle - target_beam_angle)
    beam_dist = np.sqrt(beam_dx**2 + beam_dy**2)

    beam_cone = np.exp(-((angle_diff / 0.22) ** 2)) * np.exp(-beam_dist / (height * 1.8))
    beam_light = np.clip(beam_cone * 0.35, 0.0, 1.0)[:, :, None]

    # Add sunbeam to RGB
    sun_color = np.array([1.0, 0.94, 0.80], dtype=np.float32)
    rgb += beam_light * sun_color

    # Optical dust grain & filmic tonemap
    rgb = np.clip(rgb, 0.0, 1.0)
    grain = np.random.normal(0, 0.012, (height, width, 1)).astype(np.float32)
    rgb = np.clip(rgb + grain, 0.0, 1.0)

    final_img = Image.fromarray((rgb * 255.0).astype(np.uint8), mode="RGB")
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "artwork.png")
    final_img.save(out_path, format="PNG", optimize=True)
    print(f"[✓] Saved enhanced OPUS-008 artwork to: {out_path} ({os.path.getsize(out_path) / (1024*1024):.2f} MB)")
    return out_path

if __name__ == "__main__":
    generate_heliotrope()
