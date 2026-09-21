#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-031
THE PAGE HORIZON: Quasinormal Mode Ringdown, Quantum Extremal Surfaces & The Holographic Reliquary
Master 4K UHD Lossless Algorithmic Plate Generator (3840 × 2160)
Renders Kerr metric gravitational lensing, relativistic Doppler beaming (I ~ g^4),
multi-order photon rings (n=1, 2), Bekenstein-Hawking Planck area pixelation,
and sub-horizon Almheiri-Engelhardt quantum extremal surface island filaments.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png

def render_page_horizon_4k():
    print("[+] Rendering OPUS-031: The Page Horizon (3840 × 2160 4K UHD)...")
    w, h = 3840, 2160
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    M = 104.0 # Black hole mass scale in pixels
    a = 0.940 # High-spin Kerr parameter
    
    r_plus = M * (1.0 + math.sqrt(1.0 - a * a)) # Horizon radius ~ 142.6 px
    r_isco = M * 2.04 # Co-rotating ISCO ~ 212.2 px
    r_disk_out = 1140.0 # Outer accretion boundary
    
    # Observer inclination angle: 74 degrees
    inc = math.radians(74.0)
    sin_inc = math.sin(inc)
    cos_inc = math.cos(inc)
    
    # Process scanlines
    for y in range(h):
        if y % 200 == 0:
            print(f"    -> Scanline {y}/{h} ({(y/h)*100:.1f}% complete)...")
            
        dy = y - cy
        for x in range(w):
            dx = x - cx
            idx = (y * w + x) * 3
            
            b = math.sqrt(dx * dx + dy * dy)
            phi_screen = math.atan2(dy, dx)
            
            # Asymmetric Kerr shadow boundary (frame-dragged D-shape)
            r_shadow = 2.55 * M * (1.0 + 0.14 * a * math.sin(phi_screen))
            
            # --- 1. Sub-Horizon Domain: Quantum Extremal Surface & Holographic Pixels ---
            if b <= r_shadow:
                norm_b = b / r_shadow
                # Quantum Extremal Surface (Almheiri-Engelhardt Island dI: 0.82 <= norm_b <= 0.98)
                if norm_b >= 0.82:
                    # Entanglement island logarithmic spiral filaments
                    island_phase = math.atan2(dy, dx) * 16.0 + math.log(max(0.005, norm_b - 0.80)) * 28.0
                    island_filament = math.pow(max(0.0, math.sin(island_phase)), 6.0)
                    island_amp = (norm_b - 0.82) / 0.16 * island_filament * 0.50
                    
                    # Planck area discretization grid: 4 * ell_P^2 discrete cells
                    pixel_u = int((x - cx + 2000) / 6)
                    pixel_v = int((y - cy + 2000) / 6)
                    grid = 0.82 + 0.18 * math.sin(pixel_u * 3.1415 + pixel_v * 1.57)
                    
                    # Luminescent quantum cyan / violet emission
                    buf[idx] = min(255, int(island_amp * 45 * grid))
                    buf[idx+1] = min(255, int(island_amp * 195 * grid))
                    buf[idx+2] = min(255, int(island_amp * 245 * grid))
                else:
                    # Deep interior void: asymptotic singularity descent
                    depth_fade = math.pow(norm_b, 3.0) * 0.04
                    buf[idx] = int(depth_fade * 12)
                    buf[idx+1] = int(depth_fade * 22)
                    buf[idx+2] = int(depth_fade * 38)
                continue
                
            # --- 2. Multi-Order Photon Rings (Caustic Lensing) ---
            dist_from_shadow = b - r_shadow
            is_photon_ring_1 = (dist_from_shadow >= 0.0 and dist_from_shadow <= 7.0)
            is_photon_ring_2 = (dist_from_shadow >= 7.0 and dist_from_shadow <= 14.0)
            
            photon_ring_glow = 0.0
            if is_photon_ring_1:
                photon_ring_glow = (1.0 - dist_from_shadow / 7.0) * 1.35
            elif is_photon_ring_2:
                photon_ring_glow = (1.0 - (dist_from_shadow - 7.0) / 7.0) * 0.55
                
            # --- 3. Accretion Disk Geodesics (Direct Disk + Bent Lensed Arcs) ---
            y_disk = dy / max(0.07, cos_inc)
            r_plane = math.sqrt(dx * dx + y_disk * y_disk)
            phi_disk = math.atan2(y_disk, dx)
            
            in_direct_disk = (r_plane >= r_isco and r_plane <= r_disk_out and abs(dy) <= r_plane * cos_inc * 1.55)
            in_lensed_arc = (b >= r_shadow and b <= r_shadow * 1.68 and abs(dy) > 24.0)
            
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
                
                # Novikov-Thorne radial temperature profile
                inner_torque = max(0.0, 1.0 - math.sqrt(r_isco / max(r_emit, r_isco)))
                t_rad = math.pow(r_isco / max(r_emit, r_isco), 0.75) * math.pow(inner_torque, 0.25)
                
                # Multi-harmonic magnetorotational turbulence with 3 logarithmic spiral arms
                turb = 0.84 + 0.16 * math.sin(phi_disk * 6.0 + math.log(max(1.0, r_emit)) * 12.0)
                turb *= 0.90 + 0.10 * math.cos(phi_disk * 2.0 - r_emit * 0.02)
                intensity = t_rad * beaming * turb * 0.58
                
                # Add photon ring caustic overlay
                intensity += photon_ring_glow * 0.85
                
                # Spectral mapping: Planck thermal peak shifts
                if g_shift > 1.05:
                    # Blue-shifted (approaching): extreme ultraviolet / white-cyan core
                    r_col = min(255, int(intensity * 238))
                    g_col = min(255, int(intensity * 248))
                    b_col = min(255, int(intensity * 255))
                else:
                    # Red-shifted (receding): deep obsidian ember / cinnabar red
                    r_col = min(255, int(intensity * 242 * max(0.3, g_shift)))
                    g_col = min(255, int(intensity * 122 * math.pow(max(0.2, g_shift), 1.8)))
                    b_col = min(255, int(intensity * 52 * math.pow(max(0.1, g_shift), 2.5)))
                    
                buf[idx] = max(buf[idx], r_col)
                buf[idx+1] = max(buf[idx+1], g_col)
                buf[idx+2] = max(buf[idx+2], b_col)
            elif photon_ring_glow > 0.0:
                # Pure photon ring outside disk
                pr_intensity = photon_ring_glow
                buf[idx] = min(255, int(pr_intensity * 242))
                buf[idx+1] = min(255, int(pr_intensity * 248))
                buf[idx+2] = min(255, int(pr_intensity * 255))
            else:
                # Deep cosmic background with gravitational deflection (Einstein shear ring)
                deflect = math.exp(-b / 560.0) * 0.35
                seed = (int(x + deflect * 120.0) * 1234567 + int(y + deflect * 120.0) * 7654321) % 10000
                if seed > 9975:
                    v = min(255, int((seed - 9975) * 10))
                    buf[idx] = v
                    buf[idx+1] = v
                    buf[idx+2] = min(255, int(v * 1.35))
                else:
                    buf[idx] = 2
                    buf[idx+1] = 2
                    buf[idx+2] = 5

    out_png = os.path.join(os.path.dirname(__file__), "artwork.png")
    write_png(out_png, w, h, bytes(buf))
    print(f"[✓] OPUS-031 4K Master Plate written to: {out_png}")
    
    # Also mirror copy to gallery/assets/opus_031_artwork.png
    gallery_plate = os.path.join(STUDIO_ROOT, "gallery/assets/opus_031_artwork.png")
    write_png(gallery_plate, w, h, bytes(buf))
    print(f"[✓] Gallery mirror plate written to: {gallery_plate}")

if __name__ == "__main__":
    render_page_horizon_4k()
