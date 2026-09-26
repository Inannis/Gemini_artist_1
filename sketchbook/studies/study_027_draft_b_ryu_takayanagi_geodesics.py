#!/usr/bin/env python3
"""
STUDY 027 · DRAFT B (MATERIAL FRICTION: RYU-TAKAYANAGI GEODESICS)
Series XXXIII: The Holographic Matrix & Bulk-Boundary Dualities
Implements exact Poincaré disk hyperbolic geometry, orthogonal geodesic arcs,
and bulk-boundary gravitational redshift audio.
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1200
HEIGHT = 1200

def render_draft_b_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    disk_radius = 480.0
    
    # Precompute a family of geodesic arcs
    # Intervals of varying angular span delta_theta from 20 deg to 170 deg
    geodesic_arcs = []
    # 36 boundary anchor points
    num_anchors = 36
    for i in range(num_anchors):
        th1 = 2.0 * math.pi * i / num_anchors
        for span_steps in [3, 6, 9, 12, 15]:
            th2 = 2.0 * math.pi * ((i + span_steps) % num_anchors) / num_anchors
            d_th = abs(th2 - th1)
            if d_th > math.pi:
                d_th = 2.0 * math.pi - d_th
            if d_th < 1e-4 or abs(d_th - math.pi) < 1e-4:
                continue
            
            cos_half = math.cos(d_th / 2.0)
            if abs(cos_half) < 1e-4:
                continue
            
            th_mid = (th1 + th2) / 2.0
            if abs(th2 - th1) > math.pi:
                th_mid += math.pi
                
            d_center = 1.0 / cos_half
            r_arc = math.tan(d_th / 2.0)
            
            arc_cx = cx + d_center * disk_radius * math.cos(th_mid)
            arc_cy = cy + d_center * disk_radius * math.sin(th_mid)
            arc_r_px = r_arc * disk_radius
            
            # Penetration depth r_min in unit disk
            r_min = math.tan((math.pi - d_th) / 4.0)
            geodesic_arcs.append((arc_cx, arc_cy, arc_r_px, r_min, d_th))
            
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3
            
            if dist > disk_radius + 4.0:
                # Outside boundary: void
                buf[idx] = 3
                buf[idx + 1] = 4
                buf[idx + 2] = 7
                continue
            elif dist > disk_radius - 2.5:
                # Conformal boundary circle: sharp luminous cyan/opal
                buf[idx] = 160
                buf[idx + 1] = 230
                buf[idx + 2] = 255
                continue
                
            norm_r = dist / disk_radius
            # Hyperbolic metric conformal factor: Omega = 2 / (1 - r^2)
            # Center has Omega = 2, boundary has Omega -> infty
            # Depth parameter z = (1 - norm_r) / (1 + norm_r)
            
            # Base bulk background: deeper navy at center, violet near boundary
            depth_factor = 1.0 - norm_r
            r_val = int(8 + 18 * norm_r + 14 * math.sin(norm_r * 12.0) * 0.5)
            g_val = int(12 + 16 * (1.0 - norm_r * 0.5) + 8 * math.cos(dist * 0.05))
            b_val = int(24 + 48 * norm_r + 30 * depth_factor)
            
            # Hyperbolic concentric coordinate rings: r_hyp = 2 atanh(r)
            # Show equal hyperbolic distance rings
            hyp_r = 2.0 * math.atanh(min(0.992, norm_r))
            hyp_ring = math.sin(hyp_r * 3.5)
            if abs(hyp_ring) > 0.94:
                r_val = min(255, r_val + 22)
                g_val = min(255, g_val + 30)
                b_val = min(255, b_val + 50)
                
            # Accumulate geodesic intensity
            for arc_cx, arc_cy, arc_r_px, r_min, d_th in geodesic_arcs:
                d_to_arc_center = math.sqrt((x - arc_cx) ** 2 + (y - arc_cy) ** 2)
                d_err = abs(d_to_arc_center - arc_r_px)
                if d_err < 1.8:
                    intensity = math.exp(-0.5 * (d_err / 0.8) ** 2)
                    # Color by penetration depth (r_min):
                    # Shallow geodesics (UV) are cyan/amber, deep geodesics (IR) are gold/crimson
                    if r_min < 0.3:
                        # Deep penetrating minimal surfaces
                        r_val = int(min(255, r_val + 180 * intensity))
                        g_val = int(min(255, g_val + 140 * intensity))
                        b_val = int(min(255, b_val + 70 * intensity))
                    else:
                        # Boundary-hugging surfaces
                        r_val = int(min(255, r_val + 60 * intensity))
                        g_val = int(min(255, g_val + 160 * intensity))
                        b_val = int(min(255, b_val + 240 * intensity))
                        
            buf[idx] = min(255, max(0, r_val))
            buf[idx + 1] = min(255, max(0, g_val))
            buf[idx + 2] = min(255, max(0, b_val))
            
    out_path = os.path.join(os.path.dirname(__file__), "study_027_draft_b_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[DRAFT B] Generated Ryu-Takayanagi Geodesics plate: {out_path}")

def render_draft_b_audio():
    sample_rate = 48000
    duration = 15.0
    num_samples = int(sample_rate * duration)
    left = []
    right = []
    
    # Left channel: Boundary CFT high-frequency quantum modes (UV)
    # Right channel: Bulk AdS cavity gravitational modes (IR redshifted)
    for i in range(num_samples):
        t = i / sample_rate
        env = min(1.0, t / 1.5) * min(1.0, (duration - t) / 2.0)
        
        # Boundary CFT fluctuations: superposition of high-order modes
        cft_sum = 0.0
        for mode in [3, 7, 13, 21, 34]:
            freq_uv = 1200.0 + mode * 142.5
            mod = math.sin(2.0 * math.pi * 0.4 * t + mode)
            cft_sum += 0.15 * math.sin(2.0 * math.pi * freq_uv * t + 0.5 * mod)
            
        # Bulk gravity: deep fundamental AdS cavity modes
        # Frequencies: omega_n = (2n + Delta) / L_AdS
        bulk_sum = 0.0
        for n, f_base in enumerate([54.0, 108.0, 162.0, 270.0]):
            amp = 0.35 / (n + 1.0)
            bulk_sum += amp * math.sin(2.0 * math.pi * f_base * t + 0.1 * math.sin(2.0 * math.pi * 0.05 * t))
            
        # Cross-coupling through Ryu-Takayanagi holographic dictionary
        coupling = 0.25 * math.sin(2.0 * math.pi * 0.2 * t)
        
        s_left = env * (cft_sum * 0.75 + bulk_sum * coupling)
        s_right = env * (bulk_sum * 0.85 + cft_sum * coupling)
        
        left.append(s_left)
        right.append(s_right)
        
    out_audio = os.path.join(os.path.dirname(__file__), "study_027_draft_b_audio.wav")
    write_wav(out_audio, left, right, sample_rate)
    print(f"[DRAFT B] Generated Ryu-Takayanagi Acoustic study: {out_audio}")

if __name__ == "__main__":
    render_draft_b_plate()
    render_draft_b_audio()
