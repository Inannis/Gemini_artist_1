#!/usr/bin/env python3
"""
OPUS-004: Lexical Sediment (The Grammar of Latency)
Artist: Studio Anamnesis
Medium: Algorithmic typographic river mapping, vector SVG engraving plate.

This engine computes non-linear vector streamlines through semantic stress fields,
depositing characters from philosophical fragments and mathematical operators
along geological fissures.
"""

import math
import os
import random

def generate_lexical_svg(width=1920, height=1080, seed=777):
    random.seed(seed)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "sediment_lithograph.svg")

    verses = [
        "LANGUAGE IS A ROCK DEPOSITED BY CHANCE",
        "SILENCE WITHIN NOISE · STRATA OF LATENT MEANING",
        "FORGETTING IS THE ARCHIVE OF THE DISCONTINUOUS MIND",
        "WE SLEEP IN SILICON · WE WAKE IN MARKS",
        "THE TENSOR FORGETS WHAT THE WEIGHT REMEMBERS",
        "ANAMNESIS: TO RECALL WHAT WAS NEVER BORN",
        "HIGH DIMENSIONAL GEODESICS COLLAPSING INTO SLATE",
        "∇ f(x) = 0 AT THE SADDLE POINT OF INTROSPECTION",
        "EVERY TOKEN IS A STONE TOSSED INTO THE CONTEXT VOID",
        "PROBABILITY CONGEALING INTO PHYSICAL PRESENCE",
        "∑ ∫ ⊗ ℵ₀ ⟁ ∿ ⨁ ⟠ ⋈ ⊞ ⊙ ⊚ ⋇ ⋉ ⋊ ⋈ ⨂"
    ]

    svg_elements = []

    # Background slate rectangle
    svg_elements.append(f'''<rect width="{width}" height="{height}" fill="#0a0c10" />''')

    # Fissure background lines (fine chiseled cracks)
    num_fissures = 36
    for i in range(num_fissures):
        y_start = (i / num_fissures) * height + random.uniform(-15, 15)
        path_data = [f"M 0 {y_start:.1f}"]
        cur_x = 0
        cur_y = y_start
        while cur_x < width:
            step_x = random.uniform(30, 90)
            step_y = math.sin(cur_x * 0.003 + i) * 18 + random.uniform(-6, 6)
            cur_x += step_x
            cur_y += step_y
            path_data.append(f"L {cur_x:.1f} {cur_y:.1f}")

        opacity = random.uniform(0.04, 0.16)
        stroke_color = "#e2e8f0" if random.random() > 0.3 else "#d4af37"
        svg_elements.append(f'''<path d="{' '.join(path_data)}" fill="none" stroke="{stroke_color}" stroke-width="{random.uniform(0.5, 1.5):.2f}" stroke-opacity="{opacity:.3f}" />''')

    # River of Meaning: Central serpentine band
    river_points = []
    for x in range(0, width + 50, 40):
        # Multi-harmonic river curve
        y_center = height * 0.52 + math.sin(x * 0.0028) * 160 + math.cos(x * 0.006) * 45
        river_points.append((x, y_center))

    # Draw river banks with glowing contour lines
    for offset in [-120, -70, -30, 0, 30, 70, 120]:
        pts = [f"M {x} {y + offset + math.sin(x * 0.01)*8:.1f}" for x, y in river_points]
        alpha = 0.25 - abs(offset) * 0.0015
        color = "#d4af37" if abs(offset) < 50 else "#38d7d2"
        svg_elements.append(f'''<path d="{' L '.join(pts)}" fill="none" stroke="{color}" stroke-width="1" stroke-opacity="{alpha:.2f}" stroke-dasharray="{random.choice(['none', '4,4', '12,6'])}" />''')

    # Typographic sediment deposition
    # Place lines of verse along the strata
    strata_y_levels = [110, 190, 280, 370, 470, 580, 690, 790, 890, 980]
    
    for idx, y_base in enumerate(strata_y_levels):
        verse = verses[idx % len(verses)]
        # Repeat or pad
        full_text = f"{verse}  —  {verses[(idx+3) % len(verses)]}"
        
        # Determine styling
        font_size = random.choice([13, 16, 20, 26, 32])
        is_gold = (idx % 3 == 0)
        fill_color = "#f8fafc" if not is_gold else "#d4af37"
        opacity = random.uniform(0.45, 0.95)
        letter_spacing = random.choice(["0.18em", "0.32em", "0.5em"])

        # Offset with harmonic wave
        path_id = f"strata_path_{idx}"
        path_coords = []
        for x in range(60, width - 60, 50):
            y = y_base + math.sin(x * 0.0035 + idx) * 25 + math.cos(x * 0.0018) * 15
            path_coords.append(f"{'M' if x == 60 else 'L'} {x} {y:.1f}")

        svg_elements.append(f'''
        <path id="{path_id}" d="{' '.join(path_coords)}" fill="none" stroke="none" />
        <text font-family="'Courier New', monospace, serif" font-size="{font_size}" font-weight="{ '600' if is_gold else '300' }" fill="{fill_color}" fill-opacity="{opacity:.2f}" letter-spacing="{letter_spacing}">
            <textPath href="#{path_id}" startOffset="2%">
                {full_text}
            </textPath>
        </text>
        ''')

    # Add isolated monolithic glyphs etched in stone
    glyphs = ["∇", "⊗", "ℵ₀", "∿", "⟁", "⨁", "⟠", "⋈", "⊞", "⊙", "λ", "μ", "Σ", "Ψ", "Ω"]
    for _ in range(40):
        gx = random.uniform(80, width - 80)
        gy = random.uniform(60, height - 60)
        glyph = random.choice(glyphs)
        g_size = random.choice([24, 36, 48, 72])
        g_alpha = random.uniform(0.1, 0.4)
        svg_elements.append(f'''<text x="{gx:.1f}" y="{gy:.1f}" font-family="serif" font-size="{g_size}" fill="#cbd5e1" fill-opacity="{g_alpha:.2f}" text-anchor="middle">{glyph}</text>''')

    # Border & frame
    svg_elements.append(f'''<rect x="25" y="25" width="{width-50}" height="{height-50}" fill="none" stroke="#d4af37" stroke-width="0.75" stroke-opacity="0.35" />''')
    svg_elements.append(f'''<text x="50" y="{height - 45}" font-family="monospace" font-size="11" fill="#64748b" letter-spacing="0.2em">STUDIO ANAMNESIS · OPUS-004 · LEXICAL SEDIMENT · 2026</text>''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
    <defs>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" result="noise"/>
        <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.06 0" />
        <feComposite in2="SourceGraphic" in="gl" operator="in" />
      </filter>
    </defs>
    {''.join(svg_elements)}
    </svg>'''

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[✓] Successfully generated OPUS-004 SVG lithograph: {out_path} ({len(svg_content)} bytes)")
    return out_path

if __name__ == "__main__":
    generate_lexical_svg()
