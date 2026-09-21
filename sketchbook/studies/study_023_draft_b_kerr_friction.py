#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 023 (DRAFT B: KERR FRICTION & RELATIVISTIC BEAMING)
Material Friction Draft 2: Introducing Kerr metric spin (a = 0.94), relativistic Doppler beaming,
gravitational lensing arcs (bent disk rear), and Teukolsky quasinormal acoustic ringdown.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def generate_draft_b():
    print("[+] Executing Study 023 (Draft B: Kerr Friction & Relativistic Beaming)...")
    w, h = 1920, 1080
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    M = 45.0
    a = 0.94 # High-spin Kerr parameter
    
    # Kerr Event Horizon and Ergosphere radii (equatorial)
    r_plus = M * (1.0 + math.sqrt(1.0 - a * a)) # ~63.9 pixels
    r_isco = M * (3.0 + 3.0 - math.sqrt((3.0 - 1.0)*(3.0 + 1.0))) # Co-rotating ISCO ~ 2.04 M = 91.8 px
    
    # Observer inclination angle (e.g. 75 degrees - looking near edge-on)
    inc = math.radians(72.0)
    sin_inc = math.sin(inc)
    cos_inc = math.cos(inc)
    
    for y in range(h):
        for x in range(w):
            dx = (x - cx)
            dy = (y - cy)
            idx = (y * w + x) * 3
            
            # Apparent impact parameter in screen coordinates
            # Apply inclination projection to map to accretion disk plane
            y_disk = dy / max(0.08, cos_inc)
            r_plane = math.sqrt(dx * dx + y_disk * y_disk)
            phi = math.atan2(y_disk, dx)
            
            # Gravitational lensing distortion: light near the shadow is deflected
            # Impact parameter b
            b = math.sqrt(dx * dx + dy * dy)
            
            # Shadow radius for Kerr observer at inclination: asymmetric D-shape
            # Left side (prograde) pushes closer to horizon, right side expands
            r_shadow_eff = 2.6 * M * (1.0 + 0.15 * a * math.sin(phi))
            
            # 1. Inside the shadow
            if b <= r_shadow_eff:
                # Photon ring caustic glow right at the boundary
                edge_dist = (r_shadow_eff - b)
                if edge_dist < 4.0:
                    glow = (1.0 - edge_dist / 4.0) * 0.8
                    buf[idx] = int(glow * 255)
                    buf[idx+1] = int(glow * 220)
                    buf[idx+2] = int(glow * 240)
                else:
                    buf[idx] = 0
                    buf[idx+1] = 0
                    buf[idx+2] = 0
                continue
                
            # 2. Accretion Disk & Lensing Arcs
            # Check direct disk (lower half / front) and lensed disk (upper arc bent over black hole)
            in_direct_disk = (r_plane >= r_isco and r_plane <= 520.0 and abs(dy) <= r_plane * cos_inc * 1.4)
            # Secondary lensed ring: bent rear of the disk appearing above and below the shadow
            is_lensed_arc = (b >= r_shadow_eff and b <= r_shadow_eff * 1.45 and abs(dy) > 10.0)
            
            if in_direct_disk or is_lensed_arc:
                # Determine effective emission radius
                r_emit = r_plane if in_direct_disk else (r_isco + (b - r_shadow_eff) * 3.0)
                
                # Relativistic Keplerian orbital velocity v/c
                v_c = min(0.65, math.sqrt(M / max(r_emit, r_isco)))
                
                # Line of sight velocity component: prograde rotation (left side approaching)
                v_parallel = -v_c * math.sin(phi) * sin_inc
                
                # Relativistic Lorentz factor
                gamma = 1.0 / math.sqrt(max(0.05, 1.0 - v_c * v_c))
                
                # Gravitational redshift factor: sqrt(1 - 2M/r)
                redshift_grav = math.sqrt(max(0.05, 1.0 - 2.0 * M / max(r_emit, r_plus * 1.05)))
                
                # Relativistic Doppler factor delta
                delta = 1.0 / (gamma * max(0.1, 1.0 - v_parallel))
                
                # Total frequency shift g = delta * redshift_grav
                g_shift = delta * redshift_grav
                
                # Intensity beamed by g^4
                beaming = math.pow(g_shift, 4.0)
                
                # Base radial temperature: T(r) ~ r^(-3/4)
                t_rad = math.pow(r_isco / max(r_emit, r_isco), 0.75)
                intensity = t_rad * beaming * 0.4
                
                # Turbulent spiral filament modulation
                turb = 0.8 + 0.2 * math.sin(phi * 4.0 + math.log(r_emit + 1.0) * 8.0)
                intensity *= turb
                
                # Color temperature shifts:
                # Blueshifted approaching side (left): shifts to piercing icy-blue/white
                # Redshifted receding side (right): shifts to deep dim crimson/umber
                if g_shift > 1.0:
                    # Blue-beamed
                    r_col = min(255, int(intensity * 230))
                    g_col = min(255, int(intensity * 240))
                    b_col = min(255, int(intensity * 255))
                else:
                    # Red-shifted
                    r_col = min(255, int(intensity * 240 * g_shift))
                    g_col = min(255, int(intensity * 110 * g_shift * g_shift))
                    b_col = min(255, int(intensity * 40 * g_shift * g_shift))
                
                buf[idx] = max(buf[idx], r_col)
                buf[idx+1] = max(buf[idx+1], g_col)
                buf[idx+2] = max(buf[idx+2], b_col)
            else:
                # Space background with gravitational deflection
                # Weak lensing creates Einstein shear ring
                shear = math.exp(-b / 300.0) * 0.2
                seed = (int(x + shear * 50.0) * 1234567 + int(y + shear * 50.0) * 7654321) % 10000
                if seed > 9980:
                    v = min(255, int((seed - 9980) * 12))
                    buf[idx] = v
                    buf[idx+1] = v
                    buf[idx+2] = min(255, int(v * 1.2))
                else:
                    buf[idx] = 3
                    buf[idx+1] = 3
                    buf[idx+2] = 6

    out_png = os.path.join(os.path.dirname(__file__), "study_023_draft_b_plate.png")
    write_png(out_png, w, h, bytes(buf))
    print(f"[✓] Draft B plate written to: {out_png}")
    
    # Synthesize Draft B Audio: Quasinormal Mode Ringdown
    synthesize_draft_b_audio()

def synthesize_draft_b_audio():
    sample_rate = 48000
    duration = 15.0
    num_samples = int(sample_rate * duration)
    left = [0.0] * num_samples
    right = [0.0] * num_samples
    
    # Teukolsky QNM: fundamental l=2, m=2 mode: f_R = 226.4 Hz, tau = 0.055 s
    f_qnm = 226.4
    tau_qnm = 0.055
    
    # Ergosphere superradiant drone: 56.6 Hz (sub-harmonic)
    f_ergo = 56.6
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # 1. Periodic quasinormal ringdown bursts every 3.0 seconds
        period_t = t % 3.0
        ring_amp = math.exp(-period_t / tau_qnm) * 0.45
        qnm_wave = math.sin(2.0 * math.pi * f_qnm * period_t)
        
        # 2. Continuous superradiant low drone
        drone = math.sin(2.0 * math.pi * f_ergo * t) * 0.15
        drone += math.sin(2.0 * math.pi * (f_ergo * 2.0) * t + 0.4) * 0.08
        
        # 3. Hawking thermal noise floor
        noise = (math.sin(t * 12345.67) * 43758.5453) % 1.0 - 0.5
        noise *= 0.02
        
        sig = qnm_wave * ring_amp + drone + noise
        
        # Stereo panning: left-side blueshift acoustic bias
        left[i] = sig * 0.75
        right[i] = sig * 0.45
        
    out_wav = os.path.join(os.path.dirname(__file__), "study_023_draft_b_audio.wav")
    write_wav(out_wav, left, right, sample_rate=sample_rate)
    print(f"[✓] Draft B audio written to: {out_wav}")

if __name__ == "__main__":
    generate_draft_b()
