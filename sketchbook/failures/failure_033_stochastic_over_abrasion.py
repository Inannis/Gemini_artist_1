#!/usr/bin/env python3
"""
Productive Failure 033: Stochastic Over-Abrasion & Information Liquefaction
Studio Anamnesis · Laboratory of Productive Failures (Session 022)
Series XLVI / INQ-34
Pure Python 3 + NumPy (zero external dependencies).

Demonstrates the catastrophe of overdriven erosion:
1. Sub-Critical Regime (Left): Yield stress preserves glyph structure while fluid saltation carves organic lacunae.
2. Super-Critical Regime (Right): Shear stress overwhelms substrate cohesion across all scales, triggering
   total information liquefaction, contrast collapse, and pulverization into uniform grey sediment.
"""

import math
import os
import sys
import struct
import numpy as np
from PIL import Image

# Add tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
import audio_writer

def generate_failure_033_artifacts():
    out_dir = os.path.dirname(__file__)
    width, height = 1200, 800
    
    # 1. Base Slate Texture
    img = np.zeros((height, width, 3), dtype=np.float32)
    # Dark limestone/slate background: (32, 34, 40)
    img[:] = (32.0, 34.0, 40.0)

    # Dividing central guide
    cx = width // 2
    
    np.random.seed(1337)

    # Create synthetic initial glyph field across both halves
    glyph_mask = np.zeros((height, width), dtype=np.float32)
    cols = 24
    rows = 14
    margin_x, margin_y = 60, 60
    cell_w = (width - 2 * margin_x) / cols
    cell_h = (height - 2 * margin_y) / rows

    for r in range(rows):
        y0 = int(margin_y + r * cell_h + 8)
        y1 = int(y0 + cell_h - 14)
        for c in range(cols):
            x0 = int(margin_x + c * cell_w + 6)
            x1 = int(x0 + cell_w - 12)
            
            # Draw glyph box with character-like incisions
            glyph_mask[y0:y1, x0:x1] = 1.0
            # Horizontal cut
            my = (y0 + y1) // 2
            glyph_mask[my-1:my+2, x0:x1] = 0.0
            # Vertical cut in left or right
            if (c + r) % 2 == 0:
                glyph_mask[y0:y1, x0+4:x0+8] = 0.0
            else:
                glyph_mask[y0:y1, x1-8:x1-4] = 0.0

    # Substrate Hardness Field H(x, y): layered sedimentary shale & quartz veins
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    # Bedding planes
    shale_layers = np.sin(y_coords * 0.03 + np.sin(x_coords * 0.01) * 2.0)
    # Quartz veins
    quartz_veins = np.exp(-((x_coords - 0.4 * y_coords - 200.0) % 280.0 - 10.0)**2 / 30.0)
    hardness = 0.5 + 0.3 * shale_layers + 0.6 * quartz_veins
    hardness = np.clip(hardness, 0.2, 1.5)

    # -------------------------------------------------------------
    # LEFT HALF: Sub-Critical Weathering (tau_wind < sigma_yield)
    # -------------------------------------------------------------
    # Saltation shear stress field with directional wind streaks (angle ~ -15 deg)
    wind_angle = -0.26
    proj_x = x_coords[:, :cx] * math.cos(wind_angle) + y_coords[:, :cx] * math.sin(wind_angle)
    wind_streaks = np.sin(proj_x * 0.05) * np.cos(y_coords[:, :cx] * 0.02)
    
    # Moderate shear stress
    tau_left = 0.45 + 0.35 * wind_streaks
    # Weathering mask: erosion occurs where shear stress exceeds local hardness
    erosion_left = np.maximum(0.0, tau_left - hardness[:, :cx])
    erosion_left = np.clip(erosion_left * 1.8, 0.0, 1.0)

    # Calcite redeposition in depressions
    dust_left = np.roll(erosion_left, shift=3, axis=0) * 0.4

    left_glyphs = glyph_mask[:, :cx] * (1.0 - erosion_left)
    
    # Render Left Side:
    # Intact bone-white glyphs (210, 205, 192), abraded depressions, chalk dust
    img[:, :cx, 0] += left_glyphs * 175.0 + dust_left * 80.0
    img[:, :cx, 1] += left_glyphs * 170.0 + dust_left * 78.0
    img[:, :cx, 2] += left_glyphs * 155.0 + dust_left * 70.0

    # -------------------------------------------------------------
    # RIGHT HALF: Super-Critical Over-Abrasion (tau_wind >> sigma_yield)
    # -------------------------------------------------------------
    # Catastrophic kinetic overdrive: shear stress 4.5x greater than maximum hardness
    tau_right = 3.2 + 1.2 * np.random.uniform(-1.0, 1.0, (height, width - cx))
    
    # Total obliteration: every pixel undergoes severe mechanical gouging
    erosion_right = np.clip((tau_right - hardness[:, cx:]) * 1.5, 0.0, 1.0)
    
    # Information Liquefaction: glyphs are 100% destroyed, turned into homogenous grey smear
    right_glyphs = glyph_mask[:, cx:] * (1.0 - erosion_right)
    # Heavy homogenized abrasive pulverization
    pulverized_dust = 0.55 + 0.05 * np.random.normal(0.0, 1.0, (height, width - cx))
    
    img[:, cx:, 0] += right_glyphs * 175.0 + pulverized_dust * 95.0
    img[:, cx:, 1] += right_glyphs * 170.0 + pulverized_dust * 95.0
    img[:, cx:, 2] += right_glyphs * 155.0 + pulverized_dust * 95.0

    # Central boundary line
    img[:, cx-1:cx+2] = (180.0, 80.0, 70.0)

    # Add realistic lithic noise grain
    grain = np.random.normal(0.0, 4.0, (height, width, 3))
    img = np.clip(img + grain, 0.0, 255.0).astype(np.uint8)

    # Save visual plate
    plate_path = os.path.join(out_dir, "failure_033_plate.png")
    Image.fromarray(img).save(plate_path)
    print(f"[✓] Failure 033 plate written to: {plate_path}")

    # -------------------------------------------------------------
    # ACOUSTIC SYNTHESIS: The Sound of Over-Abrasion Catastrophe
    # -------------------------------------------------------------
    # 8.0s stereo audio:
    # 0.0s - 4.0s: Left ear = Sub-critical lithic weathering (wind breathing, discrete grain clicks)
    # 4.0s - 8.0s: Right ear = Super-critical over-abrasion (deafening white noise blowout, loss of crest factor)
    sr = 48000
    duration = 8.0
    total_samples = int(sr * duration)
    
    audio_left = np.zeros(total_samples, dtype=np.float32)
    audio_right = np.zeros(total_samples, dtype=np.float32)
    
    t = np.linspace(0.0, duration, total_samples, endpoint=False)
    
    # Section 1: Sub-critical grain saltation (Filtered resonant pink noise + discrete clicks)
    pink_filter = 0.0
    for i in range(total_samples):
        # White noise input
        wn = np.random.normal(0.0, 1.0)
        # 1-pole low pass for pink-ish spectrum
        pink_filter = 0.96 * pink_filter + 0.04 * wn
        
        # Wind modulation envelope (0.2 Hz slow breath)
        wind_mod = 0.5 + 0.4 * math.sin(2.0 * math.pi * 0.25 * t[i])
        
        # Resonant lithic drone (55 Hz quartz fundamental)
        drone = math.sin(2.0 * math.pi * 55.0 * t[i]) * 0.12
        
        # Random saltation grain impacts (sparse clicks)
        click = 0.0
        if np.random.uniform(0.0, 1.0) < 0.003:
            click = np.random.uniform(-0.8, 0.8)
            
        audio_left[i] = (pink_filter * 0.35 * wind_mod + drone + click * 0.4) * 0.45
        
    # Section 2: Super-critical Over-Abrasion (Catastrophic screeching white noise blowout)
    # Ramps up sharply after t = 3.0s, reaching saturation at t = 5.0s
    for i in range(total_samples):
        overdrive_gain = min(1.0, max(0.0, (t[i] - 3.0) / 2.0))
        # Harsh, abrasive high-frequency hiss
        harsh_noise = np.random.uniform(-1.0, 1.0) * overdrive_gain * 0.85
        # Soft clipping saturation to prevent digital wrapping while demonstrating crest collapse
        audio_right[i] = np.tanh(harsh_noise * 1.5) * 0.65

    # Master audio WAV
    wav_path = os.path.join(out_dir, "failure_033_audio.wav")
    audio_writer.write_wav(wav_path, audio_left, audio_right, sr)
    print(f"[✓] Failure 033 master WAV written to: {wav_path}")

    # Convert to MP3 for gallery delivery
    mp3_path = os.path.join(out_dir, "failure_033_audio.mp3")
    cmd = f'ffmpeg -y -i "{wav_path}" -codec:a libmp3lame -b:a 192k "{mp3_path}" >/dev/null 2>&1'
    os.system(cmd)
    print(f"[✓] Failure 033 web MP3 written to: {mp3_path}")

if __name__ == "__main__":
    generate_failure_033_artifacts()
