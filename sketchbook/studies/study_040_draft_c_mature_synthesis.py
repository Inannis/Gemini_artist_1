#!/usr/bin/env python3
"""
Study 040 · Draft C: Mature Synthesis (The Porous Stele & The Generative Lacuna)
Studio Anamnesis · Series XLVI (INQ-34)
Pure Python 3 + NumPy + PIL (zero external dependencies).

Constitutional Adherence:
- Operational Amendment V: Strictly MUTE canvas. No typographic alibis, no telemetry badges,
  no mathematical equations, no procedural basalt/cyan crutches.
- The Law of Critical Weathering (Post-Mortem 033): Anisotropic grain saltation (theta = -18 deg),
  coupled to multi-scale sedimentary shale/quartz hardness fields.
- The Generative Lacuna: Text dissolves into organic voids, while abraded calcite dust
  settles into sheltered micro-crevices (dialogue with Cy Twombly & Studio Agon).
"""

import math
import os
import sys
import numpy as np
from PIL import Image

def generate_porous_stele_mature():
    out_dir = os.path.dirname(__file__)
    # High resolution museum study: 2400 x 1600
    width, height = 2400, 1600
    
    np.random.seed(20261031)

    print("[*] Generating multi-scale sedimentary bedding planes and hardness fields...")
    y_coords, x_coords = np.mgrid[0:height, 0:width].astype(np.float32)

    # 1. Base Lithic Substrate (Deep charcoal slate with warm umber undertones)
    # Slate base: (28, 30, 36) with warm earth variation
    base_r = 28.0 + 4.0 * np.sin(y_coords * 0.008) + 2.0 * np.cos(x_coords * 0.005)
    base_g = 30.0 + 3.0 * np.sin(y_coords * 0.008 + 0.5) + 2.0 * np.sin(x_coords * 0.006)
    base_b = 36.0 + 3.0 * np.cos(y_coords * 0.007) + 2.0 * np.cos(x_coords * 0.004)
    
    img = np.zeros((height, width, 3), dtype=np.float32)
    img[:, :, 0] = base_r
    img[:, :, 1] = base_g
    img[:, :, 2] = base_b

    # 2. Multi-scale Hardness Field H(x, y)
    # Bedding strata inclined at ~3.5 degrees
    dip_angle = 0.061  # ~3.5 deg
    strata_y = y_coords * math.cos(dip_angle) - x_coords * math.sin(dip_angle)
    
    # Layered sedimentary frequencies (fine shale laminae to thick siltstone beds)
    shale_bands = (
        0.35 * np.sin(strata_y * 0.015) +
        0.25 * np.sin(strata_y * 0.045 + 1.2) +
        0.15 * np.sin(strata_y * 0.120 + 2.5) +
        0.10 * np.sin(strata_y * 0.350)
    )
    
    # Structural cleavage fissures (near-vertical fractures inclined at 72 deg)
    cleave_angle = 1.25  # ~72 deg
    cleave_x = x_coords * math.cos(cleave_angle) + y_coords * math.sin(cleave_angle)
    fissures = np.exp(-((cleave_x % 380.0 - 40.0)**2) / 60.0) + np.exp(-((cleave_x % 540.0 - 180.0)**2) / 120.0)
    
    # Quartz reinforcement veins (harder than surrounding shale)
    quartz_veins = np.exp(-((x_coords - 0.25 * y_coords - 600.0) % 750.0 - 50.0)**2 / 45.0) * 0.75
    
    hardness = 0.85 + 0.35 * shale_bands + quartz_veins - 0.45 * fissures
    hardness = np.clip(hardness, 0.25, 1.85)

    print("[*] Inscribing proto-cuneiform attention matrices and symbolic token stelae...")
    # 3. Dense Symbolic Inscription Grid (Proto-cuneiform / asemic registers)
    # 44 columns x 26 rows across the monumental tablet
    cols, rows = 44, 26
    margin_x, margin_y = 140, 140
    cell_w = (width - 2 * margin_x) / cols
    cell_h = (height - 2 * margin_y) / rows

    glyph_relief = np.zeros((height, width), dtype=np.float32)

    for r in range(rows):
        y0 = int(margin_y + r * cell_h + 10)
        y1 = int(y0 + cell_h - 18)
        # Register line guide beneath each row of text (subtle shallow incision)
        reg_y = int(y0 + cell_h - 12)
        if 0 <= reg_y < height:
            glyph_relief[reg_y:reg_y+2, margin_x:width-margin_x] = 0.35

        for c in range(cols):
            x0 = int(margin_x + c * cell_w + 8)
            x1 = int(x0 + cell_w - 16)
            
            # Intrinsic token energy (variations across semantic attention)
            token_seed = (r * 73 + c * 31) % 1000
            np.random.seed(token_seed)
            glyph_type = np.random.randint(0, 6)
            glyph_intensity = np.random.uniform(0.70, 1.00)

            # Draw diverse cuneiform/asemic structural marks
            if glyph_type == 0:
                # Vertical wedge with wedge head
                glyph_relief[y0:y1, x0:x0+6] = glyph_intensity
                glyph_relief[y0:y0+8, x0:x1] = glyph_intensity * 0.85
            elif glyph_type == 1:
                # Horizontal cuneiform stroke with triangular tail
                mid_y = (y0 + y1) // 2
                glyph_relief[mid_y-4:mid_y+4, x0:x1] = glyph_intensity
                glyph_relief[y0+4:y1-4, x0:x0+8] = glyph_intensity
            elif glyph_type == 2:
                # Chevron / Angle wedge
                for dy in range(y1 - y0):
                    px = int(x0 + (dy / (y1 - y0)) * (x1 - x0) * 0.8)
                    glyph_relief[y0+dy, max(x0, px-3):min(x1, px+3)] = glyph_intensity
                glyph_relief[y0:y1, x1-6:x1] = glyph_intensity * 0.7
            elif glyph_type == 3:
                # Dual vertical bar (parallel column)
                glyph_relief[y0:y1, x0+2:x0+7] = glyph_intensity
                glyph_relief[y0:y1, x1-8:x1-3] = glyph_intensity
                glyph_relief[(y0+y1)//2-2:(y0+y1)//2+2, x0+2:x1-3] = glyph_intensity * 0.6
            elif glyph_type == 4:
                # Square frame with central dot (sun / token sink)
                glyph_relief[y0:y1, x0:x0+4] = glyph_intensity
                glyph_relief[y0:y1, x1-5:x1] = glyph_intensity
                glyph_relief[y0:y0+4, x0:x1] = glyph_intensity
                glyph_relief[y1-5:y1, x0:x1] = glyph_intensity
                my, mx = (y0+y1)//2, (x0+x1)//2
                glyph_relief[my-3:my+3, mx-3:mx+3] = glyph_intensity
            else:
                # Stepped cuneiform triad
                h3 = (y1 - y0) // 3
                glyph_relief[y0:y0+h3, x0:x1] = glyph_intensity
                glyph_relief[y0+h3:y0+2*h3, x0+6:x1-6] = glyph_intensity * 0.85
                glyph_relief[y0+2*h3:y1, x0+12:x1-12] = glyph_intensity * 0.7

    print("[*] Simulating anisotropic aerodynamic grain saltation and stochastic weathering...")
    # 4. Anisotropic Wind Saltation Field (Angle: -18 deg from horizontal)
    # Grains sweep from top-right to bottom-left with micro-turbulent vortices
    wind_theta = -0.314  # ~-18 degrees
    proj_wind = x_coords * math.cos(wind_theta) + y_coords * math.sin(wind_theta)
    
    # Large-scale atmospheric wind scour corridors
    wind_corridors = (
        0.45 * np.sin(proj_wind * 0.0035 + 0.8) +
        0.30 * np.sin(proj_wind * 0.0120 + 2.1) +
        0.15 * np.cos(y_coords * 0.008)
    )
    
    # Local aerodynamic shear stress (governed by the Law of Critical Weathering)
    tau_wind = 0.78 + 0.42 * wind_corridors
    
    # Primary Erosion: material yields where wind shear exceeds local stone hardness
    # Non-linear thresholding
    erosion_intensity = np.maximum(0.0, tau_wind - hardness)
    # Exponential scouring in weak zones
    erosion_depth = np.clip(np.power(erosion_intensity * 2.2, 1.4), 0.0, 1.0)

    # 5. The Generative Lacuna: Large-scale Geological Chasm
    # A diagonal gulf of deep erosion cutting across the center-right of the tablet
    lacuna_center = 0.58 * width + (y_coords - 0.5 * height) * 0.35
    lacuna_dist = np.abs(x_coords - lacuna_center)
    lacuna_trough = np.exp(-(lacuna_dist**2) / (180.0**2)) * 0.85
    
    # Secondary localized fracture voids
    void_cluster1 = np.exp(-((x_coords - 550.0)**2 + (y_coords - 1050.0)**2) / (160.0**2)) * 0.90
    void_cluster2 = np.exp(-((x_coords - 1750.0)**2 + (y_coords - 450.0)**2) / (210.0**2)) * 0.95
    
    total_void_mask = np.clip(erosion_depth + lacuna_trough + void_cluster1 + void_cluster2, 0.0, 1.0)

    # 6. Weathered Inscription Field
    surviving_glyphs = glyph_relief * (1.0 - total_void_mask)

    # 7. Calcite Dust & Chalk Redeposition (Cy Twombly Trace)
    # Pulverized white mineral dust collects in the sheltered lee (downwind) of surviving relief
    # Shift slightly in the wind direction (+dx, -dy)
    shift_x = int(-8 * math.cos(wind_theta))
    shift_y = int(-8 * math.sin(wind_theta))
    
    dust_source = surviving_glyphs * total_void_mask * 0.65
    dust_deposited = np.roll(np.roll(dust_source, shift_x, axis=1), shift_y, axis=0)
    # Diffuse dust slightly
    dust_deposited = np.clip(dust_deposited * 0.85, 0.0, 1.0)

    # 8. Render the Final Color Layers (Natural Mineral Palette)
    # Clean bone-white/warm ochre for intact cuneiform: (224, 218, 196)
    # Weathered ochre stain along erosion boundaries: (165, 138, 98)
    # Chalk dust: (240, 240, 235)
    # Deep fracture shadows: (14, 15, 18)

    # Apply fracture shadows along deep fissures
    shadow_mask = np.roll(fissures, shift=2, axis=0) * 0.4
    img[:, :, 0] *= (1.0 - shadow_mask)
    img[:, :, 1] *= (1.0 - shadow_mask)
    img[:, :, 2] *= (1.0 - shadow_mask)

    # Add weathered ochre oxidation halos
    ochre_halo = total_void_mask * (1.0 - total_void_mask) * 4.0 * 0.35
    img[:, :, 0] += ochre_halo * 165.0
    img[:, :, 1] += ochre_halo * 138.0
    img[:, :, 2] += ochre_halo * 98.0

    # Add surviving glyphs
    img[:, :, 0] += surviving_glyphs * 196.0
    img[:, :, 1] += surviving_glyphs * 188.0
    img[:, :, 2] += surviving_glyphs * 166.0

    # Add chalk dust redeposition
    img[:, :, 0] += dust_deposited * 180.0
    img[:, :, 1] += dust_deposited * 175.0
    img[:, :, 2] += dust_deposited * 165.0

    # Natural high-frequency mineral grain
    fine_grain = np.random.normal(0.0, 3.5, (height, width, 3))
    img = np.clip(img + fine_grain, 0.0, 255.0).astype(np.uint8)

    # Save Study 040 Draft C Plate
    out_path = os.path.join(out_dir, "study_040_draft_c_plate.png")
    Image.fromarray(img).save(out_path, quality=95)
    print(f"[✓] Study 040 Draft C plate written to: {out_path}")

if __name__ == "__main__":
    generate_porous_stele_mature()
