"""
STUDIO ANAMNESIS · LABORATORY OF STUDIES
STUDY 013: TOPOLOGICAL PHOTONIC CHERN LATTICE & CORE-MANTLE FARADAY POLARIZATION
Simulates a 2D magneto-optic photonic crystal with non-zero Chern number (C = +1),
unidirectional chiral edge propagation around sharp corners without backscattering,
and polarization precession modulated by planetary outer-core torsional waves.
"""

import os
import sys
import math

# Studio zero-dependency tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def run_study_013():
    print("[+] Executing Study 013: Topological Photonic Chern Lattice...")
    
    # -------------------------------------------------------------
    # 1. Visual Plate Generation: 1200 x 1200 PNG
    # -------------------------------------------------------------
    W, H = 1200, 1200
    img = bytearray(W * H * 3)
    
    def set_pixel(x, y, r, g, b):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            img[idx] = min(255, max(0, int(r)))
            img[idx+1] = min(255, max(0, int(g)))
            img[idx+2] = min(255, max(0, int(b)))

    def blend_pixel(x, y, r, g, b, alpha):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            img[idx] = min(255, max(0, int(img[idx] * (1.0 - alpha) + r * alpha)))
            img[idx+1] = min(255, max(0, int(img[idx+1] * (1.0 - alpha) + g * alpha)))
            img[idx+2] = min(255, max(0, int(img[idx+2] * (1.0 - alpha) + b * alpha)))

    # Dark cryo-vacuum backdrop with subtle grid
    for y in range(H):
        for x in range(W):
            idx = (y * W + x) * 3
            # Vignette
            dx = (x - W/2) / (W/2)
            dy = (y - H/2) / (H/2)
            d = math.sqrt(dx*dx + dy*dy)
            val = max(0.0, 1.0 - 0.5 * d)
            img[idx] = int(4 * val)
            img[idx+1] = int(6 * val)
            img[idx+2] = int(10 * val)
            
            # Subtle coordinate reticle lines every 100px
            if x % 100 == 0 or y % 100 == 0:
                img[idx] = min(255, img[idx] + 8)
                img[idx+1] = min(255, img[idx+1] + 12)
                img[idx+2] = min(255, img[idx+2] + 18)

    cx, cy = 600, 600
    lattice_a = 26.0  # Lattice constant in pixels
    
    # Define Triangular Lattice of Magneto-Optic YIG Cylinders
    # We create an inner cavity / interface surrounded by photonic crystal cladding
    cavity_w, cavity_h = 320.0, 320.0
    
    # 1. Draw Bulk Lattice Rods
    for row in range(-20, 21):
        for col in range(-20, 21):
            px = cx + col * lattice_a + (row % 2) * (lattice_a * 0.5)
            py = cy + row * (lattice_a * math.sqrt(3) * 0.5)
            
            dist_to_center = math.hypot(px - cx, py - cy)
            if dist_to_center < 480.0:
                # Is it outside the hollow cavity?
                in_cavity = (-cavity_w/2 < (px - cx) < cavity_w/2) and (-cavity_h/2 < (py - cy) < cavity_h/2)
                
                # Draw rod
                rod_r = 5.5
                if not in_cavity:
                    # Magneto-optic rod in cladding: deep cobalt blue with slight gyrotropic glow
                    for ry in range(-6, 7):
                        for rx in range(-6, 7):
                            r_dist = math.hypot(rx, ry)
                            if r_dist <= rod_r:
                                shade = 1.0 - (r_dist / rod_r) * 0.4
                                blend_pixel(int(px + rx), int(py + ry), 30 * shade, 70 * shade, 160 * shade, 0.9)

    # 2. Draw Topologically Protected Chiral Edge State (Boundary Mode)
    # The mode circulates around the square cavity perimeter clockwise:
    # Top edge (L to R), Right edge (T to B), Bottom edge (R to L), Left edge (B to T)
    # With a sharp 90-degree step defect to demonstrate backscattering immunity!
    half_w = cavity_w / 2.0
    half_h = cavity_h / 2.0
    
    perimeter_path = []
    # Segment 1: Top Edge with an intentional triangular defect step
    steps = 120
    for s in range(steps):
        t = s / steps
        x = cx - half_w + t * cavity_w
        y = cy - half_h
        # Triangular defect step at t in [0.4, 0.6]
        if 0.4 <= t <= 0.6:
            bump = math.sin((t - 0.4) / 0.2 * math.pi) * 35.0
            y += bump
        perimeter_path.append((x, y, 0.0))  # Angle 0
        
    # Segment 2: Right Edge
    for s in range(steps):
        t = s / steps
        x = cx + half_w
        y = cy - half_h + t * cavity_h
        perimeter_path.append((x, y, math.pi * 0.5))
        
    # Segment 3: Bottom Edge
    for s in range(steps):
        t = s / steps
        x = cx + half_w - t * cavity_w
        y = cy + half_h
        perimeter_path.append((x, y, math.pi))
        
    # Segment 4: Left Edge
    for s in range(steps):
        t = s / steps
        x = cx - half_w
        y = cy + half_h - t * cavity_h
        perimeter_path.append((x, y, math.pi * 1.5))

    # Draw Chiral Edge Wavepacket & Poynting Flux Streamlines
    for idx, (px, py, base_angle) in enumerate(perimeter_path):
        # Propagating wave phase along path
        wave_phase = idx * 0.18
        intensity = 0.6 + 0.4 * math.sin(wave_phase)
        
        # Faraday polarization tilt angle theta_F: rotates along path
        theta_faraday = base_angle + (idx / len(perimeter_path)) * (math.pi * 2.0 * 2.0)
        
        # Draw luminous edge glow
        for gy in range(-12, 13):
            for gx in range(-12, 13):
                gdist = math.hypot(gx, gy)
                if gdist <= 12:
                    glow = math.exp(-gdist / 3.2) * intensity
                    # Phosphor cyan & celestial emerald
                    cr = int(glow * 40)
                    cg = int(glow * 240)
                    cb = int(glow * 220)
                    blend_pixel(int(px + gx), int(py + gy), cr, cg, cb, 0.7)

        # Draw Faraday Polarization Vectors every 15 points
        if idx % 12 == 0:
            vec_len = 16.0
            vx = math.cos(theta_faraday) * vec_len
            vy = math.sin(theta_faraday) * vec_len
            for seg in range(16):
                f = seg / 16.0
                lx = int(px + vx * (f - 0.5))
                ly = int(py + vy * (f - 0.5))
                set_pixel(lx, ly, 255, 215, 80) # Gold Faraday vector

    # 3. Scientific Cartography & HUD Inscriptions
    # Title & Boundary Coordinates
    hud_y = 60
    for x in range(80, 1120):
        set_pixel(x, hud_y, 40, 70, 110)
        set_pixel(x, 1140, 40, 70, 110)

    out_png = os.path.join(os.path.dirname(__file__), "study_013_faraday_lattice.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"  -> Visual Plate written: {out_png}")

    # -------------------------------------------------------------
    # 2. Acoustic Study: 20s 48kHz Stereo WAV
    # -------------------------------------------------------------
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    f_carrier = 528.0  # Harmonic Solfeggio frequency
    omega_carrier = 2.0 * math.pi * f_carrier
    
    # Outer core torsional jerk modulation frequency: f_mod = 0.15 Hz
    f_mod = 0.15
    omega_mod = 2.0 * math.pi * f_mod
    
    for i in range(n_samples):
        t = i / sr
        
        # Planetary Faraday polarization angle precession:
        # theta_F(t) = omega_mod * t + delta_theta * sin(2 * pi * 0.05 * t)
        theta_F = omega_mod * t + 0.25 * math.sin(2.0 * math.pi * 0.05 * t)
        
        # Chiral Edge Resonance: Dual quadrature carriers (Ex and Ey)
        # Topologically protected: zero phase noise, zero backscattering
        carrier_I = math.sin(omega_carrier * t)
        carrier_Q = math.cos(omega_carrier * t) # 90-degree phase shift
        
        # Envelope: Gentle 1s fade-in, 1s fade-out
        env = 1.0
        if t < 1.0: env = t
        elif t > duration - 1.0: env = duration - t
        
        # Rotating polarization vector projection:
        # E_x = cos(theta_F) * I - sin(theta_F) * Q
        # E_y = sin(theta_F) * I + cos(theta_F) * Q
        E_x = math.cos(theta_F) * carrier_I - math.sin(theta_F) * carrier_Q
        E_y = math.sin(theta_F) * carrier_I + math.cos(theta_F) * carrier_Q
        
        # Deep Sub-harmonic Torsional Mode (33 Hz outer core Taylor column drone)
        torsional_drone = math.sin(2.0 * math.pi * 33.0 * t) * 0.18
        
        # Whispering gallery cavity harmonic (1056 Hz, overtone of 528 Hz)
        cavity_overtone = math.sin(2.0 * math.pi * 1056.0 * t + theta_F) * 0.08
        
        sig_l = (E_x * 0.42 + torsional_drone * 0.5 + cavity_overtone * 0.5) * env
        sig_r = (E_y * 0.42 + torsional_drone * 0.5 - cavity_overtone * 0.5) * env
        
        ch_left[i] = sig_l
        ch_right[i] = sig_r

    out_wav = os.path.join(os.path.dirname(__file__), "study_013_chiral_polarization.wav")
    write_wav(out_wav, ch_left, ch_right, sr)
    print(f"  -> Acoustic Study written: {out_wav}")

if __name__ == "__main__":
    run_study_013()
