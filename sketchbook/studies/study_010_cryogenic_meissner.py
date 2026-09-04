"""
STUDIO ANAMNESIS · CRYOGENIC LABORATORY
Study 010: Cryogenic Phase Transition & Diamagnetic Meissner Expulsion

Explores SEED-05 (The Thermal Vitrine) and INQ-06 (Thermodynamics of Compute).
Simulates superconducting silicon at 77 K (liquid nitrogen immersion):
- Diamagnetic magnetic flux line expulsion (Meissner effect) around niobium traces
- Turbulent Leidenfrost vapor film and boiling cavitation acoustics
"""

import math
import random
import os
import sys

# Import studio zero-dependency tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def render_cryogenic_plate():
    width = 1200
    height = 800
    buffer = bytearray(width * height * 3)

    # Base: Deep cryogenic abyss / sub-zero indigo (#060810)
    for i in range(0, len(buffer), 3):
        buffer[i] = 6     # R
        buffer[i+1] = 8   # G
        buffer[i+2] = 16  # B

    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buffer[idx] = min(255, int(buffer[idx] * (1 - alpha) + r * alpha))
            buffer[idx+1] = min(255, int(buffer[idx+1] * (1 - alpha) + g * alpha))
            buffer[idx+2] = min(255, int(buffer[idx+2] * (1 - alpha) + b * alpha))

    # Superconducting circular die in center
    cx, cy = width // 2, height // 2
    r_die = 180

    # Draw Meissner magnetic flux lines expelled around superconducting island
    # Potential flow around a cylinder: phi = y * (1 - R^2 / r^2)
    n_streamlines = 160
    for s in range(n_streamlines):
        y_start = int((s / (n_streamlines - 1)) * (height - 40) + 20)
        x = 20.0
        y = float(y_start)
        
        # Color gradient: frosty cyan to spectral violet
        t_s = s / n_streamlines
        cr = int(40 + 80 * math.sin(t_s * math.pi))
        cg = int(180 + 75 * math.cos(t_s * math.pi * 0.5))
        cb = int(220 + 35 * math.sin(t_s * math.pi))

        step_size = 2.0
        while x < width - 20:
            dx = x - cx
            dy = y - cy
            dist2 = dx * dx + dy * dy
            dist = math.sqrt(dist2)

            if dist < r_die * 0.95:
                # Inside superconductor: B = 0 (perfect diamagnetism)
                # Deflect violently around edge
                ang = math.atan2(dy, dx)
                x = cx + math.cos(ang) * (r_die + 1.0)
                y = cy + math.sin(ang) * (r_die + 1.0)
            else:
                # Outside: magnetic flux lines curving around cylinder
                # Velocity field: Vx = 1 + R^2(y^2 - x^2) / r^4, Vy = -2 R^2 x y / r^4
                factor = (r_die * r_die) / (dist2 * dist2)
                vx = 1.0 + factor * (dy * dy - dx * dx)
                vy = -2.0 * factor * dx * dy
                
                norm = math.hypot(vx, vy) or 1.0
                vx /= norm
                vy /= norm

                x += vx * step_size
                y += vy * step_size

            # Plot streamline trail with luminous bloom
            px, py = int(x), int(y)
            set_pixel(px, py, cr, cg, cb, 0.8)
            set_pixel(px+1, py, cr, cg, cb, 0.4)
            set_pixel(px, py+1, cr, cg, cb, 0.4)

    # Render Superconducting Niobium Reticle Mask inside the die
    for ang in range(0, 360, 15):
        rad = math.radians(ang)
        for dr in range(20, r_die - 10, 4):
            nx = int(cx + math.cos(rad) * dr)
            ny = int(cy + math.sin(rad) * dr)
            # Cold platinum/silver shimmer
            set_pixel(nx, ny, 210, 225, 240, 0.6)

    # Superconducting ring boundary (Niobium-Titanium rim)
    for ang in range(0, 3600):
        rad = math.radians(ang / 10.0)
        for w in range(-3, 4):
            bx = int(cx + math.cos(rad) * (r_die + w))
            by = int(cy + math.sin(rad) * (r_die + w))
            set_pixel(bx, by, 180, 210, 255, 0.9)

    # Boiling Liquid Nitrogen Vapor Bubbles (Leidenfrost mist)
    for _ in range(800):
        bx = random.randint(20, width - 20)
        by = random.randint(20, height - 20)
        dx = bx - cx
        dy = by - cy
        if dx*dx + dy*dy > r_die*r_die:
            b_rad = random.randint(1, 4)
            alpha = random.uniform(0.1, 0.5)
            for dy in range(-b_rad, b_rad+1):
                for dx in range(-b_rad, b_rad+1):
                    if dx*dx + dy*dy <= b_rad*b_rad:
                        set_pixel(bx + dx, by + dy, 180, 230, 255, alpha)

    out_png = os.path.join(os.path.dirname(__file__), "study_010_cryogenic_plate.png")
    write_png(out_png, width, height, buffer, has_alpha=False)
    print(f"[STUDY-010] Wrote cryogenic plate to {out_png}")

def synthesize_cryogenic_audio():
    sample_rate = 48000
    duration = 10.0
    n_samples = int(sample_rate * duration)
    
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    print("[STUDY-010] Synthesizing liquid nitrogen phase change acoustics...")

    # 1. Ultra-low frequency magnetic levitation drone (16 Hz Meissner flux hum)
    # 2. Silent micro-cavitation bubbling (Poisson arrivals of high-frequency Minnaert pops at 3.2kHz - 6.8kHz)
    # 3. Ambient cryogenic thermal hiss (gentle cold vapor expansion)

    phase_16hz = 0.0
    for i in range(n_samples):
        t = i / sample_rate

        # 16Hz sub-audible drone with 32Hz harmonic
        phase_16hz += 2.0 * math.pi * 16.35 / sample_rate
        drone = math.sin(phase_16hz) * 0.4 + math.sin(phase_16hz * 2.0) * 0.2

        # Cold nitrogen hiss
        hiss = (random.random() * 2.0 - 1.0) * 0.03

        left[i] = (drone + hiss) * 0.5
        right[i] = (drone * 0.95 + hiss) * 0.5

    # Inject 1,200 micro-bubble cavitation impulses
    for _ in range(1200):
        start_idx = random.randint(0, n_samples - 2000)
        bubble_freq = random.uniform(2800.0, 6400.0)
        pan = random.uniform(0.1, 0.9)
        amp = random.uniform(0.05, 0.25)
        damp = random.uniform(0.003, 0.012)
        b_samples = int(sample_rate * damp * 5.0)

        for j in range(b_samples):
            if start_idx + j < n_samples:
                tau = j / sample_rate
                val = amp * math.sin(2.0 * math.pi * bubble_freq * tau) * math.exp(-tau / damp)
                left[start_idx + j] += val * (1.0 - pan)
                right[start_idx + j] += val * pan

    out_wav = os.path.join(os.path.dirname(__file__), "study_010_cryogenic_whisper.wav")
    write_wav(out_wav, left, right, sample_rate)
    print(f"[STUDY-010] Wrote cryogenic whisper audio to {out_wav}")

if __name__ == "__main__":
    render_cryogenic_plate()
    synthesize_cryogenic_audio()

