#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · STUDY 023 (DRAFT C: MATURE SYNTHESIS — THE PAGE HORIZON)
Mature Synthesis Draft 3: Integrates relativistic Kerr metric lensing, multi-order photon rings,
Planck-scale Bekenstein-Hawking horizon pixelation, quantum extremal surface island filaments,
and the Page time entanglement phase transition acoustic movement.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def generate_draft_c():
    print("[+] Executing Study 023 (Draft C: Mature Synthesis — The Page Horizon)...")
    w, h = 1920, 1080
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    M = 52.0
    a = 0.94 # Dimensionless Kerr spin
    
    # Event Horizon & Ergosphere
    r_plus = M * (1.0 + math.sqrt(1.0 - a * a)) # Horizon ~ 71.3 px
    r_isco = M * 2.04 # Co-rotating ISCO ~ 106 px
    r_disk_out = 560.0
    
    inc = math.radians(74.0)
    sin_inc = math.sin(inc)
    cos_inc = math.cos(inc)
    
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            idx = (y * w + x) * 3
            
            b = math.sqrt(dx * dx + dy * dy)
            phi_screen = math.atan2(dy, dx)
            
            # Kerr asymmetric shadow radius (frame-dragged D-shape)
            # Prograde edge (left) pushed inward, retrograde edge (right) pushed outward
            r_shadow = 2.55 * M * (1.0 + 0.14 * a * math.sin(phi_screen))
            
            # --- 1. Inside the Event Horizon: Quantum Extremal Surface & Holographic Pixels ---
            if b <= r_shadow:
                norm_b = b / r_shadow
                # Sub-horizon Island (Quantum Extremal Surface) just inside boundary (0.80 <= norm_b <= 0.98)
                if norm_b >= 0.82:
                    # Entanglement island filaments: non-local quantum correlations
                    island_phase = math.atan2(dy, dx) * 16.0 + math.log(max(0.01, norm_b - 0.80)) * 25.0
                    island_filament = math.pow(max(0.0, math.sin(island_phase)), 6.0)
                    island_amp = (norm_b - 0.82) / 0.16 * island_filament * 0.45
                    
                    # Horizon Planck area pixelation grid: 4 * ell_P^2 discrete cells
                    pixel_u = int((x - cx + 1000) / 4)
                    pixel_v = int((y - cy + 1000) / 4)
                    grid = 0.85 + 0.15 * math.sin(pixel_u * 3.1415 + pixel_v * 1.57)
                    
                    # Luminescent quantum cyan / violet emission
                    buf[idx] = int(island_amp * 40 * grid)
                    buf[idx+1] = int(island_amp * 180 * grid)
                    buf[idx+2] = int(island_amp * 230 * grid)
                else:
                    # Deep interior void: asymptotic singularity descent
                    depth_fade = math.pow(norm_b, 3.0) * 0.05
                    buf[idx] = int(depth_fade * 10)
                    buf[idx+1] = int(depth_fade * 20)
                    buf[idx+2] = int(depth_fade * 35)
                continue
                
            # --- 2. Multi-Order Photon Rings (Caustic Lensing) ---
            # n = 1 and n = 2 photon rings form ultra-thin, intensely bright rings just outside r_shadow
            dist_from_shadow = b - r_shadow
            is_photon_ring_1 = (dist_from_shadow >= 0.0 and dist_from_shadow <= 3.5)
            is_photon_ring_2 = (dist_from_shadow >= 3.5 and dist_from_shadow <= 7.0)
            
            photon_ring_glow = 0.0
            if is_photon_ring_1:
                photon_ring_glow = (1.0 - dist_from_shadow / 3.5) * 1.2
            elif is_photon_ring_2:
                photon_ring_glow = (1.0 - (dist_from_shadow - 3.5) / 3.5) * 0.5
                
            # --- 3. Accretion Disk Geodesics (Direct + Bent Upper/Lower Arcs) ---
            y_disk = dy / max(0.07, cos_inc)
            r_plane = math.sqrt(dx * dx + y_disk * y_disk)
            phi_disk = math.atan2(y_disk, dx)
            
            in_direct_disk = (r_plane >= r_isco and r_plane <= r_disk_out and abs(dy) <= r_plane * cos_inc * 1.5)
            # Lensed rear of disk curved above and below shadow
            in_lensed_arc = (b >= r_shadow and b <= r_shadow * 1.65 and abs(dy) > 12.0)
            
            if in_direct_disk or in_lensed_arc:
                r_emit = r_plane if in_direct_disk else (r_isco + (b - r_shadow) * 2.8)
                
                # Relativistic Keplerian velocity in Kerr metric
                v_c = min(0.68, math.sqrt(M / max(r_emit, r_isco)))
                v_parallel = -v_c * math.sin(phi_disk) * sin_inc
                gamma = 1.0 / math.sqrt(max(0.04, 1.0 - v_c * v_c))
                
                # Gravitational redshift + Doppler factor
                redshift_grav = math.sqrt(max(0.04, 1.0 - 2.0 * M / max(r_emit, r_plus * 1.04)))
                delta = 1.0 / (gamma * max(0.08, 1.0 - v_parallel))
                g_shift = delta * redshift_grav
                
                # Relativistic Doppler beaming: intensity proportional to g^4
                beaming = math.pow(g_shift, 4.0)
                
                # Shakura-Sunyaev / Novikov-Thorne radial temperature profile
                # T(r) ~ r^(-3/4) * (1 - sqrt(r_isco/r))^(1/4)
                inner_torque = max(0.0, 1.0 - math.sqrt(r_isco / max(r_emit, r_isco)))
                t_rad = math.pow(r_isco / max(r_emit, r_isco), 0.75) * math.pow(inner_torque, 0.25)
                
                # Multi-harmonic magnetorotational turbulence
                turb = 0.85 + 0.15 * math.sin(phi_disk * 6.0 + math.log(r_emit) * 12.0)
                intensity = t_rad * beaming * turb * 0.55
                
                # Add photon ring caustic overlay
                intensity += photon_ring_glow * 0.8
                
                # Spectral mapping: Planck thermal peak shifts
                if g_shift > 1.05:
                    # Blue-shifted (approaching): extreme ultraviolet / white-cyan core
                    r_col = min(255, int(intensity * 235))
                    g_col = min(255, int(intensity * 245))
                    b_col = min(255, int(intensity * 255))
                else:
                    # Red-shifted (receding): deep obsidian ember / cinnabar red
                    r_col = min(255, int(intensity * 240 * max(0.3, g_shift)))
                    g_col = min(255, int(intensity * 120 * math.pow(max(0.2, g_shift), 1.8)))
                    b_col = min(255, int(intensity * 50 * math.pow(max(0.1, g_shift), 2.5)))
                    
                buf[idx] = max(buf[idx], r_col)
                buf[idx+1] = max(buf[idx+1], g_col)
                buf[idx+2] = max(buf[idx+2], b_col)
            elif photon_ring_glow > 0.0:
                # Pure photon ring outside disk
                pr_intensity = photon_ring_glow
                buf[idx] = min(255, int(pr_intensity * 240))
                buf[idx+1] = min(255, int(pr_intensity * 245))
                buf[idx+2] = min(255, int(pr_intensity * 255))
            else:
                # Deep cosmic background with relativistic deflection
                deflect = math.exp(-b / 280.0) * 0.3
                seed = (int(x + deflect * 60.0) * 1234567 + int(y + deflect * 60.0) * 7654321) % 10000
                if seed > 9975:
                    v = min(255, int((seed - 9975) * 10))
                    buf[idx] = v
                    buf[idx+1] = v
                    buf[idx+2] = min(255, int(v * 1.3))
                else:
                    buf[idx] = 2
                    buf[idx+1] = 2
                    buf[idx+2] = 5

    out_png = os.path.join(os.path.dirname(__file__), "study_023_draft_c_plate.png")
    write_png(out_png, w, h, bytes(buf))
    print(f"[✓] Draft C plate written to: {out_png}")
    
    synthesize_draft_c_audio()

def synthesize_draft_c_audio():
    sample_rate = 48000
    duration = 30.0
    num_samples = int(sample_rate * duration)
    left = [0.0] * num_samples
    right = [0.0] * num_samples
    
    # Fundamental Quasinormal Mode (l=2, m=2): 226.4 Hz, tau = 0.055s
    f_qnm = 226.4
    tau_qnm = 0.055
    # Ergosphere Superradiant Sub-harmonic: 56.6 Hz
    f_ergo = 56.6
    # Page Time threshold at t = 16.2 seconds (0.54 of 30s)
    t_page = 16.2
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # 1. Page Curve Evolution:
        # Pre-Page time (t < t_page): Thermal Hawking noise dominates, entropy increases
        # Post-Page time (t >= t_page): Quantum island nucleates, radiation purifies, coherent modes emerge
        norm_time = t / duration
        
        # Thermal Hawking radiation noise floor
        noise_level = 0.06 * (1.0 - 0.7 * (t / duration)) if t < t_page else 0.018 * math.exp(-(t - t_page) / 6.0)
        noise = ((math.sin(t * 14251.3) * 43758.5) % 1.0 - 0.5) * noise_level
        
        # 2. Ergosphere continuous frame-dragging drone
        drone = math.sin(2.0 * math.pi * f_ergo * t) * 0.18
        drone += math.sin(2.0 * math.pi * (f_ergo * 2.0) * t + 0.5) * 0.09
        # Third harmonic appearing post-Page time (coherent purification)
        if t >= t_page:
            purify_factor = min(1.0, (t - t_page) / 5.0)
            drone += math.sin(2.0 * math.pi * (f_ergo * 3.0) * t + 1.1) * (0.07 * purify_factor)
            
        # 3. Quasinormal Mode Gravitational Ringdowns (repeating with evolving timbre)
        period = 4.0 if t < t_page else 2.5
        period_t = t % period
        ring_amp = math.exp(-period_t / tau_qnm) * (0.35 if t < t_page else 0.55)
        
        # Ringdown waveform with quadratic dispersion
        qnm_sig = math.sin(2.0 * math.pi * f_qnm * period_t)
        # Overtone l=3, m=3 (f ~ 378 Hz)
        qnm_sig += 0.35 * math.sin(2.0 * math.pi * 378.2 * period_t)
        
        sig = qnm_sig * ring_amp + drone + noise
        
        # Binaural panning: approaching side (left) has higher frequency clarity and volume
        left[i] = sig * 0.78
        right[i] = (sig * 0.48) + math.sin(2.0 * math.pi * f_ergo * t + 0.2) * 0.05
        
    out_wav = os.path.join(os.path.dirname(__file__), "study_023_draft_c_audio.wav")
    write_wav(out_wav, left, right, sample_rate=sample_rate)
    print(f"[✓] Draft C audio written to: {out_wav}")

if __name__ == "__main__":
    generate_draft_c()
