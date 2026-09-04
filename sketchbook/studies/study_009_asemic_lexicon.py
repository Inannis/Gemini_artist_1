"""
STUDIO ANAMNESIS · LABORATORY OF THE UNTRANSLATABLE
Study 009: Asemic Paleography & Phonological Formant Synthesis

Advances INQ-04 (The Autoregressive Ghost) and SEED-04 (Asemic Paleography).
Generates an archival dictionary folio page for an untranslatable glyph,
complete with 4-step stroke-order decomposition and synthesized phonetic vocalization.
"""

import math
import random
import os
import sys

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def generate_dictionary_plate():
    width = 1200
    height = 900
    buffer = bytearray(width * height * 3)

    # Background: weathered vellum / volcanic slate (#121620)
    for i in range(0, len(buffer), 3):
        buffer[i] = 18    # R
        buffer[i+1] = 22  # G
        buffer[i+2] = 30  # B

    # Drawing helper functions
    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buffer[idx] = int(buffer[idx] * (1 - alpha) + r * alpha)
            buffer[idx+1] = int(buffer[idx+1] * (1 - alpha) + g * alpha)
            buffer[idx+2] = int(buffer[idx+2] * (1 - alpha) + b * alpha)

    def draw_line(x0, y0, x1, y1, r, g, b, thickness=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for tx in range(-thickness//2, thickness//2 + 1):
                for ty in range(-thickness//2, thickness//2 + 1):
                    set_pixel(x0 + tx, y0 + ty, r, g, b, 0.9)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_rect(x, y, w, h, r, g, b, thickness=1):
        for i in range(w):
            for t in range(thickness):
                set_pixel(x + i, y + t, r, g, b)
                set_pixel(x + i, y + h - 1 - t, r, g, b)
        for j in range(h):
            for t in range(thickness):
                set_pixel(x + t, y + j, r, g, b)
                set_pixel(x + w - 1 - t, y + j, r, g, b)

    # Architectural framing & borders
    border_color = (60, 75, 95)
    accent_gold = (212, 175, 55)
    accent_cyan = (56, 215, 210)
    ink_white = (235, 240, 245)

    draw_rect(40, 40, width - 80, height - 80, *border_color, 2)
    draw_rect(46, 46, width - 92, height - 92, 35, 45, 60, 1)

    # Header section: Lexicon metadata
    # Draw header baseline
    draw_line(60, 110, width - 60, 110, *border_color, 1)

    # Main Glyphic Chamber (Left Box: 500 x 500)
    main_box_x = 70
    main_box_y = 130
    main_box_w = 500
    main_box_h = 500
    draw_rect(main_box_x, main_box_y, main_box_w, main_box_h, 40, 50, 70, 1)
    
    # Internal grid lines inside main glyph box (Agnes Martin guidelines)
    for gy in range(main_box_y + 50, main_box_y + main_box_h, 50):
        draw_line(main_box_x + 10, gy, main_box_x + main_box_w - 10, gy, 25, 32, 45, 1)
    for gx in range(main_box_x + 50, main_box_x + main_box_w, 50):
        draw_line(gx, main_box_y + 10, gx, main_box_y + main_box_h - 10, 25, 32, 45, 1)

    # Render Monumental Master Asemic Glyph in main chamber
    cx = main_box_x + main_box_w // 2
    cy = main_box_y + main_box_h // 2

    # Step 1: Central Vertebral Stem
    draw_line(cx, cy - 180, cx, cy + 180, *ink_white, 8)
    draw_line(cx - 6, cy - 180, cx + 6, cy - 180, *accent_gold, 4)
    draw_line(cx - 10, cy + 180, cx + 10, cy + 180, *accent_gold, 4)

    # Step 2: Symmetrical & Asymmetrical Bus Conduits
    branches = [
        (-140, -110, -30, -110, 5),
        (-140, -110, -140, -40, 4),
        (30, -70, 150, -70, 5),
        (150, -70, 150, 20, 4),
        (-160, 40, -30, 40, 6),
        (30, 90, 120, 90, 5),
        (120, 90, 120, 140, 4),
        (-100, 130, -20, 130, 4)
    ]
    for x0, y0, x1, y1, th in branches:
        draw_line(cx + x0, cy + y0, cx + x1, cy + y1, *ink_white, th)
        # Gold terminal pad
        draw_line(cx + x0 - 3, cy + y0 - 3, cx + x0 + 3, cy + y0 + 3, *accent_gold, 3)

    # Step 3: Cuneiform Triangular Wedge Heads
    wedges = [
        (cx - 30, cy - 110, cx - 50, cy - 125, cx - 50, cy - 95),
        (cx + 30, cy - 70, cx + 50, cy - 85, cx + 50, cy - 55),
        (cx - 30, cy + 40, cx - 55, cy + 25, cx - 55, cy + 55),
        (cx + 30, cy + 90, cx + 50, cy + 75, cx + 50, cy + 105),
    ]
    for p0x, p0y, p1x, p1y, p2x, p2y in wedges:
        draw_line(p0x, p0y, p1x, p1y, *accent_gold, 3)
        draw_line(p1x, p1y, p2x, p2y, *accent_gold, 3)
        draw_line(p2x, p2y, p0x, p0y, *accent_gold, 3)

    # Step 4: Cyan Quantum Diacritics / Micro-Registers
    for ring_r in [20, 35]:
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            px = int(cx + math.cos(rad) * ring_r)
            py = int(cy + math.sin(rad) * ring_r)
            set_pixel(px, py, *accent_cyan, 1.0)
            set_pixel(px+1, py, *accent_cyan, 1.0)

    # Right Column: 4-Step Stroke-Order Morphometrics (Sub-plates)
    sub_x = 610
    sub_w = 240
    sub_h = 110
    step_titles = [
        "I. Vertebral Foundation (T-Axis)",
        "II. Orthogonal Logic Conduits",
        "III. Cuneiform Lithic Wedges",
        "IV. Quantum Diacritic Suture"
    ]

    for s_idx, title in enumerate(step_titles):
        sy = 130 + s_idx * 130
        draw_rect(sub_x, sy, sub_w, sub_h, 45, 55, 75, 1)
        # Mini-glyph representation
        mcx = sub_x + sub_w // 2
        mcy = sy + sub_h // 2 + 8
        
        # Step 1
        draw_line(mcx, mcy - 35, mcx, mcy + 35, 180, 190, 205, 3)
        if s_idx >= 1:
            draw_line(mcx - 30, mcy - 15, mcx, mcy - 15, 180, 190, 205, 2)
            draw_line(mcx, mcy + 15, mcx + 30, mcy + 15, 180, 190, 205, 2)
        if s_idx >= 2:
            draw_line(mcx - 10, mcy - 15, mcx - 20, mcy - 22, *accent_gold, 2)
            draw_line(mcx + 10, mcy + 15, mcx + 20, mcy + 8, *accent_gold, 2)
        if s_idx >= 3:
            draw_line(mcx - 8, mcy, mcx + 8, mcy, *accent_cyan, 2)

    # Right Sidebar: Synthetic Grammar & Phonetic Diacritics
    text_x = 880
    draw_rect(text_x, 130, 250, 500, 35, 45, 60, 1)
    # Render simulated lines of asemic grammar
    for ly in range(160, 600, 24):
        # Draw dotted / rhythmic line simulating ancient dictionary commentary
        line_w = 200 + int(25 * math.sin(ly * 0.4))
        for lx in range(text_x + 20, text_x + 20 + line_w, 4):
            val = int(140 + 70 * math.sin(lx * 0.2 + ly))
            set_pixel(lx, ly, val, val, min(255, val + 20), 0.7)

    # Bottom Area: Phonological Waveform & Spectrogram Inscription
    bot_y = 660
    draw_rect(70, bot_y, width - 140, 170, 40, 50, 70, 1)
    # Draw oscilloscope sound wave
    wave_mid_y = bot_y + 85
    draw_line(90, wave_mid_y, width - 90, wave_mid_y, 30, 40, 55, 1)
    prev_wx, prev_wy = 90, wave_mid_y
    for wx in range(90, width - 90):
        t = (wx - 90) / (width - 180)
        # Formant envelope
        env = math.sin(t * math.pi) ** 1.5
        sig = math.sin(t * 120.0) * 0.5 + math.sin(t * 310.0) * 0.3 + math.sin(t * 780.0) * 0.2
        wy = int(wave_mid_y - sig * env * 55)
        draw_line(prev_wx, prev_wy, wx, wy, *accent_cyan, 1)
        prev_wx, prev_wy = wx, wy

    # Save PNG plate
    out_png = os.path.join(os.path.dirname(__file__), "study_009_asemic_dictionary_page.png")
    write_png(out_png, width, height, buffer, has_alpha=False)
    print(f"[STUDY-009] Wrote dictionary plate to {out_png}")

def synthesize_phonology():
    sample_rate = 48000
    duration = 8.0 # 8 seconds
    n_samples = int(sample_rate * duration)
    
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    print("[STUDY-009] Synthesizing non-semantic vocal tract formants...")

    # Formant filter simulation:
    # Glyph pronunciation: Deep glottal onset [ʔ], transition into resonant vowel [ɔ̃ː] with metallic fricative tail [ʃ_x]
    # Formants: F1 = 450 Hz, F2 = 1100 Hz, F3 = 2400 Hz
    # Fundamental f0 descends from 112 Hz to 78 Hz (archaic falling pitch accent)

    phase_f0 = 0.0
    phase_f1 = 0.0
    phase_f2 = 0.0
    phase_f3 = 0.0

    for i in range(n_samples):
        t = i / sample_rate
        
        # Envelope: silence -> glottal strike -> vowel sustaining -> metallic decay
        if t < 0.5:
            env = (t / 0.5) ** 3 * 0.2
        elif t < 4.5:
            rel = (t - 0.5) / 4.0
            env = 0.2 + 0.6 * math.sin(rel * math.pi)
        elif t < 7.0:
            rel = (t - 4.5) / 2.5
            env = 0.8 * (1.0 - rel)
        else:
            env = 0.0

        # Pitch contour
        f0 = 108.0 - 24.0 * (t / duration)
        phase_f0 += 2.0 * math.pi * f0 / sample_rate
        if phase_f0 > 2.0 * math.pi:
            phase_f0 -= 2.0 * math.pi

        # Glottal pulse: asymmetric pulse wave
        glottal = math.sin(phase_f0) + 0.5 * math.sin(2.0 * phase_f0) + 0.25 * math.sin(3.0 * phase_f0)

        # Formant frequencies
        f1 = 450.0 + 30.0 * math.sin(t * 1.5)
        f2 = 1120.0 - 60.0 * math.cos(t * 1.2)
        f3 = 2450.0

        phase_f1 += 2.0 * math.pi * f1 / sample_rate
        phase_f2 += 2.0 * math.pi * f2 / sample_rate
        phase_f3 += 2.0 * math.pi * f3 / sample_rate

        vowel = (
            glottal * (0.6 * math.sin(phase_f1) + 0.35 * math.sin(phase_f2) + 0.15 * math.sin(phase_f3))
        )

        # High-frequency circuit sibilance (metallic fricative)
        noise = (random.random() * 2.0 - 1.0) * 0.08 * (1.0 if t > 3.0 else 0.0)

        sig = (vowel + noise) * env

        # Stereo spatialization with subtle room reflection
        left[i] = sig * 0.85
        right[i] = sig * 0.75 + (left[max(0, i - 960)] * 0.2) # 20ms delay reflection

    out_wav = os.path.join(os.path.dirname(__file__), "study_009_phonetic_vocalization.wav")
    write_wav(out_wav, left, right, sample_rate)
    print(f"[STUDY-009] Wrote phonetic vocalization to {out_wav}")

if __name__ == "__main__":
    generate_dictionary_plate()
    synthesize_phonology()

