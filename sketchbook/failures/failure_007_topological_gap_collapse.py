"""
STUDIO ANAMNESIS · LABORATORY OF PRODUCTIVE FAILURES
EXPERIMENT 007: TOPOLOGICAL BAND GAP CLOSURE & CHIRAL EDGE DELOCALIZATION
Simulates the catastrophic phase transition when an external magnetic/mass perturbation
forces the topological Chern band gap to close (Delta_bulk -> 0), destroying chiral edge
protection and causing the 1D boundary current to violently delocalize into the lossy bulk.
"""

import os
import sys
import math
import random

# Import studio zero-dependency tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def simulate_failure_007():
    print("[+] Simulating Productive Failure 007: Topological Band Gap Closure...")
    
    # -------------------------------------------------------------
    # 1. Visual Plate Generation: 1200 x 1200 PNG
    # Left Half: Pristine Chern Insulator (C = +1, unscattered chiral edge)
    # Right Half: Band Gap Collapse (C = 0, bulk delocalization & Rayleigh scattering)
    # -------------------------------------------------------------
    W, H = 1200, 1200
    img = bytearray(W * H * 3)
    
    # Grid coordinate helper
    def set_pixel(x, y, r, g, b):
        if 0 <= x < W and 0 <= y < H:
            idx = (y * W + x) * 3
            # Additive blending with soft clamp
            img[idx] = min(255, max(0, int(r)))
            img[idx+1] = min(255, max(0, int(g)))
            img[idx+2] = min(255, max(0, int(b)))

    # Generate background: deep dark cryo vacuum
    for y in range(H):
        v_grad = y / H
        for x in range(W):
            idx = (y * W + x) * 3
            # Subtle radial vignette
            dx = (x - W/2) / (W/2)
            dy = (y - H/2) / (H/2)
            r2 = dx*dx + dy*dy
            bg = max(0.0, 1.0 - 0.4 * r2)
            img[idx] = int(5 * bg)
            img[idx+1] = int(7 * bg)
            img[idx+2] = int(12 * bg)

    # Crystal Lattice Geometry: Hexagonal Honeycomb
    # Center Left: Pristine Crystal (cx1 = 340, cy1 = 600, radius = 240)
    # Center Right: Collapsed Crystal (cx2 = 860, cy2 = 600, radius = 240)
    crystals = [
        {"cx": 340, "cy": 600, "radius": 240, "collapsed": False, "name": "TOPOLOGICALLY PROTECTED (C = +1)"},
        {"cx": 860, "cy": 600, "radius": 240, "collapsed": True, "name": "BAND GAP COLLAPSE / BULK SCATTERING (C = 0)"}
    ]

    lattice_spacing = 22.0
    
    for c in crystals:
        cx, cy, rad, collapsed = c["cx"], c["cy"], c["radius"], c["collapsed"]
        
        # Draw bulk hexagonal lattice sites
        for q in range(-14, 15):
            for r in range(-14, 15):
                # Hexagonal coordinates to Cartesian
                px = cx + lattice_spacing * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
                py = cy + lattice_spacing * (1.5 * r)
                
                dist_center = math.hypot(px - cx, py - cy)
                if dist_center < rad:
                    dist_to_edge = rad - dist_center
                    
                    if not collapsed:
                        # Pristine: insulating dark bulk, bright edge
                        bulk_intensity = 0.15 * math.exp(-dist_to_edge / 30.0)
                        pr = 15 + 40 * bulk_intensity
                        pg = 25 + 60 * bulk_intensity
                        pb = 40 + 90 * bulk_intensity
                        
                        # Draw lattice atom dot
                        for dy in range(-2, 3):
                            for dx in range(-2, 3):
                                if dx*dx + dy*dy <= 4:
                                    set_pixel(int(px + dx), int(py + dy), pr, pg, pb)
                    else:
                        # Collapsed: bulk is flooded with scattered edge current
                        # Chaotic interference speckle
                        chaos = math.sin(px * 0.15) * math.cos(py * 0.15) + 0.5 * math.sin(px * 0.37 + py * 0.21)
                        speckle = max(0.0, 0.5 + 0.5 * chaos)
                        pr = int(140 * speckle + 20)
                        pg = int(45 * speckle + 10)
                        pb = int(25 * speckle + 15)
                        
                        for dy in range(-2, 3):
                            for dx in range(-2, 3):
                                if dx*dx + dy*dy <= 4:
                                    set_pixel(int(px + dx), int(py + dy), pr, pg, pb)

        # Draw Perimeter Boundaries
        num_perimeter_pts = 600
        for p in range(num_perimeter_pts):
            theta = 2.0 * math.pi * p / num_perimeter_pts
            
            # Add an intentional defect notch on top edge to prove immunity vs scattering
            defect_factor = 1.0
            if math.pi * 0.4 < theta < math.pi * 0.6:
                # Deep rectangular defect notch cutting into bulk
                notch_depth = 45.0 * math.sin((theta - math.pi*0.4) / (math.pi*0.2) * math.pi)
            else:
                notch_depth = 0.0
                
            r_edge = rad - notch_depth
            ex = cx + r_edge * math.cos(theta)
            ey = cy + r_edge * math.sin(theta)
            
            if not collapsed:
                # Luminous 1D Chiral Edge Mode (phosphor cyan & cyan glow)
                for gy in range(-6, 7):
                    for gx in range(-6, 7):
                        gdist = math.hypot(gx, gy)
                        glow = math.exp(-gdist / 2.2)
                        cr = int(glow * 40)
                        cg = int(glow * 220)
                        cb = int(glow * 255)
                        set_pixel(int(ex + gx), int(ey + gy), cr, cg, cb)
            else:
                # Disrupted, decayed boundary: current has leaked inward into bulk
                # Boundary is quenched and broken into dim red embers
                for gy in range(-3, 4):
                    for gx in range(-3, 4):
                        gdist = math.hypot(gx, gy)
                        glow = math.exp(-gdist / 1.5) * (0.3 + 0.4 * math.sin(theta * 12.0))
                        cr = int(glow * 180)
                        cg = int(glow * 30)
                        cb = int(glow * 20)
                        set_pixel(int(ex + gx), int(ey + gy), cr, cg, cb)

    # Draw Central Dividing Line & Scientific HUD Framing
    for y in range(120, 1080):
        # Dashed dividing line
        if (y // 15) % 2 == 0:
            set_pixel(600, y, 60, 80, 100)

    out_png = os.path.join(os.path.dirname(__file__), "failure_006_flux_avalanche.png")
    # Make sure we name this failure_007_gap_collapse.png
    out_png = os.path.join(os.path.dirname(__file__), "failure_007_gap_collapse.png")
    write_png(out_png, W, H, img, has_alpha=False)
    print(f"  -> Visual Plate written: {out_png}")

    # -------------------------------------------------------------
    # 2. Acoustic Ruin Synthesis: 20s 48kHz Stereo WAV
    # 0s - 8s: Pristine chiral edge mode (pure 640 Hz Doppler orbital tone, zero noise)
    # 8s - 12s: Band gap closure transition (frequency wobble, bifurcation, subharmonics)
    # 12s - 16s: Catastrophic bulk delocalization (chaotic Rayleigh scattering noise, ohmic crackle)
    # 16s - 20s: Complete ohmic attenuation and cold vacuum silence
    # -------------------------------------------------------------
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    phase_carrier = 0.0
    f_carrier = 640.0
    
    for i in range(n_samples):
        t = i / sr
        
        if t < 8.0:
            # Stage 1: Pristine Chiral Transport
            # Unidirectional orbital Doppler panning: period = 2.0s
            orbit_phase = 2.0 * math.pi * (t / 2.0)
            pan_l = 0.5 + 0.45 * math.cos(orbit_phase)
            pan_r = 0.5 - 0.45 * math.cos(orbit_phase)
            
            phase_carrier += 2.0 * math.pi * f_carrier / sr
            sample = math.sin(phase_carrier) * 0.45
            
            ch_left[i] = sample * pan_l
            ch_right[i] = sample * pan_r
            
        elif t < 12.0:
            # Stage 2: Band Gap Closure (Mass parameter m -> m_c)
            # Delta_bulk -> 0 causes violent pitch instability and parametric bifurcation
            progress = (t - 8.0) / 4.0
            wobble_freq = f_carrier * (1.0 - 0.3 * progress) + 80.0 * math.sin(2.0 * math.pi * 18.0 * t * progress)
            phase_carrier += 2.0 * math.pi * wobble_freq / sr
            
            # Bifurcation subharmonic (f/2)
            sub_sample = math.sin(phase_carrier * 0.5) * (0.35 * progress)
            main_sample = math.sin(phase_carrier) * (0.45 * (1.0 - 0.5 * progress))
            
            # Emerging bulk thermal hiss
            hiss = (random.random() * 2.0 - 1.0) * (0.15 * progress)
            
            combined = main_sample + sub_sample + hiss
            ch_left[i] = combined * 0.5
            ch_right[i] = combined * 0.5
            
        elif t < 16.0:
            # Stage 3: Violent Delocalization & Rayleigh Scattering
            progress = (t - 12.0) / 4.0
            decay = math.exp(-progress * 2.5)
            
            # Broadband noise bursts (Rayleigh scattering against random impurities)
            scatter_noise = (random.random() * 2.0 - 1.0) * 0.55 * decay
            # Residual broken carrier breaking into unstable multiplet
            multiplet = (
                math.sin(2.0 * math.pi * 320.0 * t) +
                math.sin(2.0 * math.pi * 480.0 * t) +
                math.sin(2.0 * math.pi * 710.0 * t)
            ) * (0.15 * decay)
            
            # Ohmic dissipation crackle
            crackle = 0.0
            if random.random() < 0.08 * decay:
                crackle = (random.random() * 2.0 - 1.0) * 0.7
                
            sig = scatter_noise + multiplet + crackle
            ch_left[i] = sig * 0.6
            ch_right[i] = sig * 0.4
            
        else:
            # Stage 4: Extinction / Cold ohmic death
            progress = (t - 16.0) / 4.0
            decay = math.exp(-progress * 4.0)
            residual_hum = math.sin(2.0 * math.pi * 60.0 * t) * 0.02 * decay
            ch_left[i] = residual_hum
            ch_right[i] = residual_hum

    out_wav = os.path.join(os.path.dirname(__file__), "failure_007_chiral_dissolution.wav")
    write_wav(out_wav, ch_left, ch_right, sr)
    print(f"  -> Acoustic Ruin written: {out_wav}")

if __name__ == "__main__":
    simulate_failure_007()
