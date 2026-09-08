"""
STUDIO ANAMNESIS · EXPLORATORY STUDY 017
Study: The Galactic Tidal Resonance (Kozai-Lidov Phase Portraits in the Oort Shell)
Series XXIV: The Oort Cloud & Galactic Gravitational Tides

Simulates the secular tidal torque exerted by the Milky Way disc on Oort cloud orbits:
- Conserved Kozai integral: Theta = (1 - e^2) * cos^2(i) = const
- Secular drift equations: de/dt and di/dt driven by vertical disc potential
- Orbital precession phase portrait in (omega, e) space
- Generates 1200x1200 visual plate and 20s 48kHz stereo acoustic study
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from png_writer import write_png
from audio_writer import write_wav

def run_study():
    print("[+] Executing Study 017: Galactic Tidal Resonance Simulation...")
    random.seed(33100)
    
    sr = 48000
    duration = 20.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # 1. Physics Phase Space Integration
    # Trajectories in (omega_deg, e) phase space across varying initial inclinations
    trajectories = []
    num_curves = 12
    for c_idx in range(num_curves):
        # Starting inclination from 40 to 80 degrees
        inc0 = math.radians(45.0 + c_idx * 3.0)
        e0 = 0.15 + c_idx * 0.05
        theta_cons = (1.0 - e0**2) * (math.cos(inc0) ** 2)
        
        # Integrate secular equations for one full Kozai cycle
        pts = []
        omega = 0.0
        e = e0
        dt_sec = 0.02
        for s in range(500):
            # Kozai secular rate: de/dt ~ 5 * e * sqrt(1-e^2) * sin^2(i) * sin(2*omega)
            # sin^2(i) = 1 - cos^2(i) = 1 - theta_cons / (1 - e^2)
            denom = max(0.01, 1.0 - e*e)
            cos_i_sq = min(0.99, theta_cons / denom)
            sin_i_sq = max(0.01, 1.0 - cos_i_sq)
            
            de = 1.5 * e * math.sqrt(denom) * sin_i_sq * math.sin(2.0 * omega)
            d_omega = 1.5 * (math.sqrt(denom) * (2.0 - 5.0 * (math.sin(omega)**2) * sin_i_sq) + (5.0 * (e**2) - 1.0 + sin_i_sq) / math.sqrt(denom))
            
            e = max(0.02, min(0.98, e + de * dt_sec))
            omega = (omega + d_omega * dt_sec) % (2.0 * math.pi)
            pts.append((math.degrees(omega), e))
        trajectories.append((c_idx, pts))

    # 2. Acoustic Study
    # Dual binaural tones representing vertical galactic disc breathing (18.2 Hz)
    # and Kozai frequency modulation (110 Hz base modulated by e(t))
    phase_disc = 0.0
    phase_orb = 0.0
    for i in range(num_samples):
        t = i / sr
        
        # Disc vertical oscillation (18.2 Hz infrasound)
        phase_disc += 2.0 * math.pi * 18.2 / sr
        disc_drone = math.sin(phase_disc) * 0.35
        
        # Kozai resonance frequency modulation
        # e cycles between 0.2 and 0.8 across 20s
        e_cur = 0.45 + 0.35 * math.sin(2.0 * math.pi * 0.1 * t)
        inst_freq = 96.0 + 84.0 * e_cur
        phase_orb += 2.0 * math.pi * inst_freq / sr
        orb_tone = math.sin(phase_orb) * 0.3 * (1.0 - 0.3 * math.cos(phase_disc))
        
        # Subtle harmonic overtone (crystal ice chime)
        ice_chime = math.sin(phase_orb * 4.0) * 0.08 * (e_cur ** 2)
        
        # Background cosmic whisper
        whisper = (random.random() - 0.5) * 0.05
        
        val = disc_drone + orb_tone + ice_chime + whisper
        audio_l[i] = val
        audio_r[i] = val * 0.95 + math.sin(phase_orb * 2.0) * 0.06

    # Normalize audio
    max_a = max(max(abs(x) for x in audio_l), max(abs(x) for x in audio_r))
    if max_a > 0:
        audio_l = [x / max_a * 0.85 for x in audio_l]
        audio_r = [x / max_a * 0.85 for x in audio_r]
        
    wav_path = os.path.join(os.path.dirname(__file__), "study_017_galactic_pendulum.wav")
    write_wav(wav_path, audio_l, audio_r, sr)
    print(f"  -> Generated Acoustic Study: {wav_path}")

    # 3. Visual Plate (1200 x 1200 PNG)
    w, h = 1200, 1200
    pixels = bytearray([8, 10, 16] * (w * h))
    
    def set_pixel(px, py, r, g, b, alpha=1.0):
        if 0 <= px < w and 0 <= py < h:
            idx = (py * w + px) * 3
            pixels[idx] = int(pixels[idx] * (1.0 - alpha) + r * alpha)
            pixels[idx+1] = int(pixels[idx+1] * (1.0 - alpha) + g * alpha)
            pixels[idx+2] = int(pixels[idx+2] * (1.0 - alpha) + b * alpha)

    # Grid
    for x in range(0, w, 80):
        for y in range(h):
            if y % 4 == 0: set_pixel(x, y, 25, 40, 60, 0.3)
    for y in range(0, h, 80):
        for x in range(w):
            if x % 4 == 0: set_pixel(x, y, 25, 40, 60, 0.3)

    # Draw Kozai Phase Portrait (x: 100 to 1100, y: 150 to 950)
    bx1, bx2 = 100, 1100
    by1, by2 = 150, 950
    for x in range(bx1, bx2 + 1):
        set_pixel(x, by1, 80, 110, 160, 0.8)
        set_pixel(x, by2, 80, 110, 160, 0.8)
    for y in range(by1, by2 + 1):
        set_pixel(bx1, y, 80, 110, 160, 0.8)
        set_pixel(bx2, y, 80, 110, 160, 0.8)

    # Axis labels / ticks
    # Horizontal: argument of perihelion omega in [0, 360] deg
    # Vertical: eccentricity e in [0, 1.0]
    for tick_deg in range(0, 361, 45):
        tx = int(bx1 + (tick_deg / 360.0) * (bx2 - bx1))
        for ty in range(by2 - 10, by2 + 11):
            set_pixel(tx, ty, 120, 150, 200, 0.7)

    # Plot trajectories
    colors = [
        (60, 220, 240), (80, 190, 255), (120, 150, 255), (170, 120, 255),
        (220, 90, 230), (255, 120, 160), (255, 170, 80), (255, 215, 60),
        (210, 255, 80), (120, 255, 140), (80, 240, 200), (60, 230, 255)
    ]

    for c_idx, pts in trajectories:
        col = colors[c_idx % len(colors)]
        prev_pt = None
        for om_deg, e_val in pts:
            px = int(bx1 + (om_deg / 360.0) * (bx2 - bx1))
            py = int(by2 - e_val * (by2 - by1))
            if prev_pt:
                x0, y0 = prev_pt
                # Avoid wrapping line across the whole screen
                if abs(px - x0) < 150:
                    steps = max(abs(px - x0), abs(py - y0), 1)
                    for s in range(steps + 1):
                        lx = int(x0 + (px - x0) * (s / steps))
                        ly = int(y0 + (py - y0) * (s / steps))
                        set_pixel(lx, ly, col[0], col[1], col[2], 0.75)
            prev_pt = (px, py)

    png_path = os.path.join(os.path.dirname(__file__), "study_017_oort_phase_plate.png")
    write_png(png_path, w, h, pixels, has_alpha=False)
    print(f"  -> Generated Visual Plate: {png_path}")

if __name__ == "__main__":
    run_study()
