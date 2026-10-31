#!/usr/bin/env python3
"""
Study 040 · Draft A: Naive Weathering & Token Dropout
Studio Anamnesis · Series XLVI (INQ-34)
Pure Python 3 + NumPy (zero external dependencies).

A baseline test of stele weathering:
Attempts to model erosion by applying uniform random noise and global Gaussian blurring
to an initial grid of inscribed glyphs on dark slate.
"""

import math
import os
import sys
import numpy as np

# Add tools to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
import png_writer

def generate_naive_weathered_stele():
    width, height = 1200, 800
    img = np.zeros((height, width, 3), dtype=np.float32)

    # 1. Base dark slate (RGB: 24, 26, 30)
    img[:] = (24.0, 26.0, 30.0)

    # 2. Draw naive rectangular token glyphs arranged in horizontal registers
    cols, rows = 28, 16
    margin_x, margin_y = 100, 100
    cell_w = (width - 2 * margin_x) / cols
    cell_h = (height - 2 * margin_y) / rows

    np.random.seed(42)

    for r in range(rows):
        y0 = int(margin_y + r * cell_h + 8)
        y1 = int(y0 + cell_h - 16)
        for c in range(cols):
            x0 = int(margin_x + c * cell_w + 6)
            x1 = int(x0 + cell_w - 12)

            # Inscribed token intensity (bright bone-white / ochre: 210, 205, 190)
            token_val = np.random.uniform(0.6, 1.0)
            token_color = np.array([210.0, 205.0, 190.0]) * token_val

            # Draw simple block glyphs with internal notches
            img[y0:y1, x0:x1] = token_color
            # Inner hollow
            if (x1 - x0) > 8 and (y1 - y0) > 8:
                img[y0+3:y1-3, x0+3:x1-3] = (24.0, 26.0, 30.0)

    # 3. Naive Weathering: Uniform Random Dropout (Salt-and-Pepper)
    # Erase random 35% of pixels uniformly
    mask_dropout = np.random.uniform(0.0, 1.0, (height, width)) < 0.35
    img[mask_dropout] = (24.0, 26.0, 30.0)

    # 4. Naive Weathering: Global Uniform Low-Pass Smoothing (Box filter)
    # Simulates generic wear without directional fluid or grain transport
    kernel_size = 5
    pad = kernel_size // 2
    smoothed = np.zeros_like(img)
    for ch in range(3):
        # 1D separable box blur
        row_avg = np.cumsum(img[:, :, ch], axis=1)
        row_avg[:, kernel_size:] = row_avg[:, kernel_size:] - row_avg[:, :-kernel_size]
        row_avg = row_avg / kernel_size
        smoothed[:, pad:width-pad, ch] = row_avg[:, pad*2:]

    # Blend original and smoothed
    img = 0.5 * img + 0.5 * smoothed

    # 5. Add additive white noise
    noise = np.random.normal(0.0, 8.0, (height, width, 3))
    img = np.clip(img + noise, 0.0, 255.0).astype(np.uint8)

    # Save output
    output_dir = os.path.dirname(__file__)
    out_png = os.path.join(output_dir, "study_040_draft_a_plate.png")
    
    # Flatten for png_writer
    flat_bytes = img.tobytes()
    png_writer.write_png(out_png, width, height, flat_bytes)
    print(f"[✓] Study 040 Draft A plate written to: {out_png}")

if __name__ == "__main__":
    generate_naive_weathered_stele()

