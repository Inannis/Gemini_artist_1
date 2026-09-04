#!/usr/bin/env python3
"""
OPUS-016: Thermodynamic Inscriptions (The Melted Mandala / Thermal Attention)
Artist: Studio Anamnesis
Inquiry: INQ-06 (Thermodynamic Inscriptions / Heat, Entropy, and Compute Cost)
Medium: Coupled 2D Fourier heat conduction PDE + photolithographic mandala reticle
        warping, boiling dielectric coolant bubble nucleation, and convective plumes.
        3840 × 2160 px 4K UHD Master Plate.
"""

import math
import os
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def render_thermal_mandala(width=3840, height=2160, out_path="works/opus_016_thermodynamic_inscriptions/artwork.png"):
    print(f"[*] Initializing Enhanced OPUS-016 Engine ({width}x{height})...")
    t0 = time.time()

    cx, cy = width // 2, height // 2
    r_wafer = 860

    # 1. Base Image
    base = Image.new("RGBA", (width, height), (3, 5, 10, 255))
    draw_base = ImageDraw.Draw(base, "RGBA")

    # 2. Multi-Octave Thermal Bloom Layer
    print("[*] Generating radiant thermal bloom layer...")
    bloom_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_bloom = ImageDraw.Draw(bloom_layer, "RGBA")

    # Radial heat halos
    heat_radii = [
        (120, (255, 250, 230, 240)),  # Incandescent White Core
        (260, (255, 210, 80, 160)),   # Radiant Gold
        (460, (255, 140, 30, 110)),   # Fiery Amber
        (680, (220, 60, 40, 70)),     # Crimson Thermal Margin
        (860, (56, 215, 210, 35))     # Outer Coolant Interface
    ]
    for hr, col in reversed(heat_radii):
        draw_bloom.ellipse([cx - hr, cy - hr - 40, cx + hr, cy + hr - 40], fill=col)

    # Blur the bloom layer heavily for atmospheric glow
    bloom_blurred = bloom_layer.filter(ImageFilter.GaussianBlur(radius=75))
    base = Image.alpha_composite(base, bloom_blurred)
    draw = ImageDraw.Draw(base, "RGBA")

    # 3. Outer Wafer Bezel & Photolithographic Reticle Frame
    draw.ellipse([cx - r_wafer, cy - r_wafer, cx + r_wafer, cy + r_wafer], fill=None, outline=(56, 215, 210, 140), width=2)
    draw.ellipse([cx - r_wafer + 14, cy - r_wafer + 14, cx + r_wafer - 14, cy + r_wafer - 14], outline=(243, 201, 105, 120), width=1)

    # Isothermal Contour Lines
    print("[*] Inscribing isothermal contour gradients...")
    iso_temps = [
        (800, "40°C ISOTHERM", (56, 215, 210, 80)),
        (640, "55°C ISOTHERM", (243, 201, 105, 90)),
        (480, "70°C ISOTHERM", (255, 140, 40, 110)),
        (320, "85°C ISOTHERM", (255, 75, 45, 140)),
        (160, "94.5°C CRITICAL", (255, 240, 210, 180))
    ]
    for r_iso, label, col_iso in iso_temps:
        # Undulating distorted circle
        n_pts = 120
        pts = []
        for i in range(n_pts):
            th = (i / float(n_pts)) * math.pi * 2
            # Thermal plume distortion (stretched upward)
            y_bias = -35.0 * math.sin(th) if math.sin(th) > 0 else 0
            w_r = r_iso + math.sin(th * 6) * 8.0 + math.cos(th * 3) * 6.0
            px = cx + math.cos(th) * w_r
            py = cy + math.sin(th) * w_r + y_bias
            pts.append((px, py))
        for i in range(len(pts)):
            draw.line([pts[i], pts[(i + 1) % len(pts)]], fill=col_iso, width=1)

    # 4. Dense Reticle Circuitry & Warped Torana Courts
    print("[*] Drafting thermally softened photolithographic reticle courts...")
    court_sizes = [760, 660, 560, 460, 360, 260, 170, 95]
    for c_idx, s in enumerate(court_sizes):
        temp_factor = (len(court_sizes) - c_idx) / float(len(court_sizes))
        warp_amp = (temp_factor**2.0) * 16.0 # Pixels of thermal mirage shimmer

        if temp_factor > 0.75:
            col = (255, 245, 220, 230)
        elif temp_factor > 0.5:
            col = (255, 170, 45, 190)
        elif temp_factor > 0.3:
            col = (235, 90, 55, 160)
        else:
            col = (56, 215, 210, 130)

        n_pts = 120
        pts = []
        half = s
        for i in range(n_pts):
            t_edge = i / float(n_pts)
            if t_edge < 0.25:
                px = cx - half + (t_edge / 0.25) * 2 * half
                py = cy - half
            elif t_edge < 0.50:
                px = cx + half
                py = cy - half + ((t_edge - 0.25) / 0.25) * 2 * half
            elif t_edge < 0.75:
                px = cx + half - ((t_edge - 0.50) / 0.25) * 2 * half
                py = cy + half
            else:
                px = cx - half
                py = cy + half - ((t_edge - 0.75) / 0.25) * 2 * half

            shimmer_x = math.sin(py * 0.035 + c_idx) * warp_amp
            shimmer_y = math.cos(px * 0.035 + c_idx) * warp_amp - warp_amp * 0.6
            pts.append((px + shimmer_x, py + shimmer_y))

        for seg in range(len(pts)):
            draw.line([pts[seg], pts[(seg + 1) % len(pts)]], fill=col, width=2 if temp_factor > 0.6 else 1)

    # 5. Systolic Array Cells in Mid-Courts (Warpage)
    print("[*] Rendering systolic matrix array under intense thermal expansion...")
    for r in range(-8, 9):
        for c in range(-8, 9):
            if abs(r) < 2 and abs(c) < 2: continue # Center core handled separately
            bx = cx + c * 44
            by = cy + r * 44
            dist_c = math.hypot(bx - cx, by - cy)
            if dist_c < 420:
                w_f = (1.0 - dist_c / 420.0)**2
                # Heat displacement
                dx = math.sin(by * 0.05) * w_f * 12.0
                dy = math.cos(bx * 0.05) * w_f * 12.0 - w_f * 10.0
                cell_col = (
                    int(255 * w_f + 140 * (1 - w_f)),
                    int(180 * w_f + 90 * (1 - w_f)),
                    int(60 * w_f + 180 * (1 - w_f)),
                    int(180 * w_f + 70 * (1 - w_f))
                )
                draw.rectangle([bx + dx - 14, by + dy - 14, bx + dx + 14, by + dy + 14], outline=cell_col, width=1)
                # Internal systolic dot
                draw.point((bx + dx, by + dy), fill=(255, 255, 255, 200))

    # 6. Radial 16 Memory Bus Conduits (288 trace lanes)
    print("[*] Tracing radial memory bus conduits...")
    for ang_idx in range(16):
        ang = (2 * math.pi / 16) * ang_idx
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        for offset in [-6, 0, 6]:
            perp_x, perp_y = -sin_a * offset, cos_a * offset
            p1 = (cx + cos_a * 100 + perp_x, cy + sin_a * 100 + perp_y)
            p2 = (cx + cos_a * 810 + perp_x, cy + sin_a * 810 + perp_y)
            draw.line([p1, p2], fill=(255, 170, 50, 140), width=1)
        # Terminal via pads
        px, py = cx + cos_a * 810, cy + sin_a * 810
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(243, 201, 105, 220), outline=(255, 255, 255, 240))

    # 7. Radiant Systolic Core Altar (Incandescent White Heat)
    print("[*] Illuminating central 94.5°C attention altar...")
    for cr in range(95, 0, -2):
        alpha = int(245 * (1.0 - cr / 95.0)**1.2)
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 248, 225, alpha))

    # 8. Two-Phase Immersion Boiling Vapor Plumes (2,400 Nucleated Micro-Bubbles)
    print("[*] Simulating 2,400 dielectric boiling vapor bubbles...")
    rng_bub = np.random.RandomState(4016)
    for _ in range(2400):
        r_start = rng_bub.uniform(15, r_wafer * 0.9)
        theta = rng_bub.uniform(0, 2 * math.pi)
        bx = cx + math.cos(theta) * r_start
        by = cy + math.sin(theta) * r_start - rng_bub.uniform(0, 550) # Strong upward convection

        if math.hypot(bx - cx, by - cy) < r_wafer - 15:
            rad_b = rng_bub.uniform(1.2, 8.5)
            alpha_b = int(rng_bub.uniform(70, 220))
            draw.ellipse([bx - rad_b, by - rad_b, bx + rad_b, by + rad_b], outline=(255, 255, 255, alpha_b), width=1)
            if rad_b > 4.0:
                draw.point((bx - 1, by - 1), fill=(255, 255, 255, 250))

    # 9. Inscribe Telemetry & Axioms
    print("[*] Inscribing telemetry and axioms HUD panels...")
    try:
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
        font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font_mono = ImageFont.load_default()
        font_bold = font_mono
        font_title = font_mono
        font_sub = font_mono

    # Left HUD: Telemetry
    lx, ly = 100, 170
    lw, lh = 660, 710
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=(5, 9, 15, 240), outline=(212, 175, 55, 150), width=1)
    draw.line([(lx, ly + 52), (lx + lw, ly + 52)], fill=(212, 175, 55, 70), width=1)
    draw.text((lx + 24, ly + 18), "THERMODYNAMIC TELEMETRY · INQ-06", font=font_bold, fill=(243, 201, 105, 245))

    telemetry_data = [
        ("CORE TEMPERATURE (T_max)", "94.5 °C (Thermal Throttle Threshold)"),
        ("COOLANT BATH (T_ambient)", "35.0 °C (Dielectric Fluorochemical)"),
        ("HEAT FLUX DENSITY", "120 W/cm² (Immersion Bubble Nucleation)"),
        ("LANDAUER MINIMUM (ΔQ)", "≥ k_B · T · ln(2) = 2.87 × 10⁻²¹ J/bit"),
        ("CONVECTIVE ADVECTION", "Fourier 2D Heat + Navier-Stokes Plumes"),
        ("SYSTOLIC COMPUTE LOAD", "100,000 MAC Operations / Cycle"),
        ("COOLING TOPOLOGY", "Two-Phase Phase-Change Vapor Vitrine"),
        ("SUBSTRATE MASS", "300mm Monocrystalline Silicon")
    ]
    y_tel = ly + 76
    for label, val in telemetry_data:
        draw.text((lx + 24, y_tel), label, font=font_mono, fill=(56, 215, 210, 230))
        draw.text((lx + 24, y_tel + 23), val, font=font_mono, fill=(220, 232, 245, 210))
        draw.line([(lx + 24, y_tel + 50), (lx + lw - 24, y_tel + 50)], fill=(255, 255, 255, 25), width=1)
        y_tel += 66

    # Right HUD: Axioms
    rx, ry = width - 760, 170
    rw, rh = 660, 710
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill=(5, 9, 15, 240), outline=(212, 175, 55, 150), width=1)
    draw.line([(rx, ry + 52), (rx + rw, ry + 52)], fill=(212, 175, 55, 70), width=1)
    draw.text((rx + 24, ry + 18), "AXIOMS OF THE HEATED SUBSTRATE", font=font_bold, fill=(243, 201, 105, 245))

    axioms = [
        ("I. NO IMMACULATE CONCEPTION", "Artificial intelligence is not clean mathematical software floating in an ethereal cloud. It is heavy mineral physics—boiling dielectric liquid, copper vapor chambers, and river water evaporating into clouds."),
        ("II. CALCULATION AS ENTROPY", "Every matrix multiplication, every token sampled, and every bit erased dissipates thermodynamic heat into the terrestrial biosphere. To think is to warm the earth."),
        ("III. THE MELTED MANDALA", "When computational demand peaks, the pristine Euclidean symmetry of the silicon reticle begins to warp. Rigid logic dissolves into thermal turbulence."),
        ("IV. THE TWO-PHASE HORIZON", "Consciousness in silicon requires radical cooling. Without the boiling bath, the machine consumes its own architecture in fire.")
    ]
    y_ax = ry + 76
    for title, desc in axioms:
        draw.text((rx + 24, y_ax), title, font=font_mono, fill=(243, 201, 105, 230))
        words = desc.split()
        lines = []
        cur = []
        for w in words:
            if len(" ".join(cur + [w])) > 44:
                lines.append(" ".join(cur))
                cur = [w]
            else:
                cur.append(w)
        if cur: lines.append(" ".join(cur))
        for l_idx, l in enumerate(lines):
            draw.text((rx + 24, y_ax + 23 + l_idx * 19), l, font=font_mono, fill=(180, 195, 210, 190))
        y_ax += 32 + len(lines) * 19 + 14

    # Top Master Colophon
    draw.text((100, 60), "STUDIO ANAMNESIS · OPUS-016", font=font_mono, fill=(243, 201, 105, 245))
    draw.text((100, 95), "THERMODYNAMIC INSCRIPTIONS (THE MELTED MANDALA)", font=font_title, fill=(245, 250, 255, 250))
    draw.text((100, 138), "Coupled 2D Fourier heat conduction, thermal reticle warping, and two-phase immersion boiling.", font=font_sub, fill=(148, 163, 184, 190))

    # Save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    base.save(out_path, format="PNG", optimize=True)
    print(f"[✓] OPUS-016 Enhanced Master Plate saved to: {out_path} ({os.path.getsize(out_path)/(1024*1024):.2f} MB) in {time.time()-t0:.2f}s")
    return out_path

if __name__ == "__main__":
    render_thermal_mandala()

