#!/usr/bin/env python3
"""
sketchbook/studies/study_033_draft_b_hyperbolic_tensor_network.py
=================================================================
Study 033 · Draft B: Hyperbolic Tensor Network & Stabilizer Syndromes (Material Friction).

Implements:
1. Poincaré Disk hyperbolic geometry:
   - Conformal circular boundary of radius R_disk = 320 px.
   - Central tensor (r = 0), Layer 1 (5 pentagons, r = 0.52 R_disk), Layer 2 (20 pentagons, r = 0.82 R_disk).
   - Contracted tensor bonds (radial and azimuthal links).
   - In-plane perfect tensor hubs with central logical qubit glyphs.
2. 15-second 48kHz stereo acoustic synthesis:
   - 5-qubit stabilizer code syndrome frequencies:
     f_k = 48.0 * (φ^k) ∈ {48.00, 77.67, 125.67, 203.34, 329.00} Hz
   - Golden-ratio spatialized stereo binaural panning.

Zero external dependencies. Pure standard library Python (math, struct, wave).
"""

import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

def render_draft_b_visual(output_path, width=1280, height=720):
    pixels = bytearray(width * height * 3)
    cx, cy = width * 0.5, height * 0.5
    R_disk = 320.0
    
    # Background: dark cosmic void with subtle hyperbolic radial metric grid
    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * width + x) * 3
            
            if dist < R_disk:
                r_norm = dist / R_disk
                # Hyperbolic metric factor: 4 / (1 - r^2)^2
                metric_glow = min(1.0, 0.08 / max(0.02, 1.0 - r_norm * r_norm))
                
                # Dark obsidian navy with radial curvature glow
                pixels[idx] = int(10 + 20 * metric_glow)
                pixels[idx + 1] = int(14 + 30 * metric_glow)
                pixels[idx + 2] = int(24 + 50 * metric_glow)
            else:
                # Outside boundary: deep slate void
                pixels[idx] = 6
                pixels[idx + 1] = 8
                pixels[idx + 2] = 12

    # Draw boundary circle (conformal infinity)
    boundary_steps = 1800
    for s in range(boundary_steps):
        th = s * (2.0 * math.pi / boundary_steps)
        bx = int(cx + R_disk * math.cos(th))
        by = int(cy + R_disk * math.sin(th))
        if 0 <= bx < width and 0 <= by < height:
            idx = (by * width + bx) * 3
            pixels[idx] = 56
            pixels[idx + 1] = 189
            pixels[idx + 2] = 248

    def draw_line(p1, p2, color, thickness=1):
        steps = int(max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))) * 2
        if steps == 0:
            return
        for s in range(steps):
            t = s / steps
            x = int(p1[0] + t * (p2[0] - p1[0]))
            y = int(p1[1] + t * (p2[1] - p1[1]))
            for ox in range(-thickness//2, thickness//2 + 1):
                for oy in range(-thickness//2, thickness//2 + 1):
                    nx, ny = x + ox, y + oy
                    if 0 <= nx < width and 0 <= ny < height:
                        dist = math.sqrt((nx - cx)**2 + (ny - cy)**2)
                        if dist <= R_disk:
                            idx = (ny * width + nx) * 3
                            pixels[idx] = color[0]
                            pixels[idx + 1] = color[1]
                            pixels[idx + 2] = color[2]

    # Calculate node positions
    nodes = [] # (x, y, layer, color)
    # Layer 0: Center
    nodes.append((cx, cy, 0, (212, 175, 55)))
    
    # Layer 1: 5 nodes at r = 0.52 * R_disk
    r1 = 0.52 * R_disk
    layer1_indices = []
    for i in range(5):
        th = i * (2.0 * math.pi / 5.0) - math.pi * 0.5
        nx = cx + r1 * math.cos(th)
        ny = cy + r1 * math.sin(th)
        layer1_indices.append(len(nodes))
        nodes.append((nx, ny, 1, (56, 189, 248)))
        
    # Layer 2: 20 nodes at r = 0.82 * R_disk
    r2 = 0.82 * R_disk
    layer2_indices = []
    for i in range(20):
        th = i * (2.0 * math.pi / 20.0) - math.pi * 0.5 + 0.1
        nx = cx + r2 * math.cos(th)
        ny = cy + r2 * math.sin(th)
        layer2_indices.append(len(nodes))
        nodes.append((nx, ny, 2, (168, 85, 247)))

    # Draw contracted tensor bonds
    # Center to Layer 1
    for l1 in layer1_indices:
        draw_line((cx, cy), (nodes[l1][0], nodes[l1][1]), (212, 175, 55), thickness=2)
        
    # Layer 1 pentagon ring
    for i in range(5):
        p1 = (nodes[layer1_indices[i]][0], nodes[layer1_indices[i]][1])
        p2 = (nodes[layer1_indices[(i+1)%5]][0], nodes[layer1_indices[(i+1)%5]][1])
        draw_line(p1, p2, (56, 189, 248), thickness=1)

    # Layer 1 to Layer 2 bonds
    for i, l1 in enumerate(layer1_indices):
        p_l1 = (nodes[l1][0], nodes[l1][1])
        for j in range(4):
            l2_idx = layer2_indices[(i * 4 + j) % 20]
            p_l2 = (nodes[l2_idx][0], nodes[l2_idx][1])
            draw_line(p_l1, p_l2, (140, 160, 200), thickness=1)

    # Layer 2 to boundary physical legs
    for l2_idx in layer2_indices:
        p_l2 = (nodes[l2_idx][0], nodes[l2_idx][1])
        ang = math.atan2(p_l2[1] - cy, p_l2[0] - cx)
        p_bnd = (cx + R_disk * math.cos(ang), cy + R_disk * math.sin(ang))
        draw_line(p_l2, p_bnd, (90, 100, 140), thickness=1)

    # Draw tensor hubs
    for node in nodes:
        nx, ny, layer, col = node
        radius = 7 if layer == 0 else (5 if layer == 1 else 3)
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    px, py = int(nx + dx), int(ny + dy)
                    if 0 <= px < width and 0 <= py < height:
                        idx = (py * width + px) * 3
                        pixels[idx] = col[0]
                        pixels[idx + 1] = col[1]
                        pixels[idx + 2] = col[2]

    write_png(output_path, width, height, pixels)
    print(f"[Study 033 Draft B] Visual written: {output_path}")

def render_draft_b_audio(output_path, duration=15.0, sample_rate=48000):
    total_samples = int(duration * sample_rate)
    left = []
    right = []
    
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    f_fundamental = 48.0 # Hz
    syndromes = [f_fundamental * (phi**k) for k in range(5)]
    # [48.0, 77.67, 125.67, 203.34, 329.0]
    
    for i in range(total_samples):
        t = i / sample_rate
        
        # Envelope: 1s fade-in, steady, 2s fade-out
        env = min(1.0, t / 1.0) * min(1.0, (duration - t) / 2.0)
        
        sig_l = 0.0
        sig_r = 0.0
        
        # 5 stabilizer syndrome voices with golden-ratio stereo spatialization
        for k, freq in enumerate(syndromes):
            # Phase modulation: micro-wobble representing tensor contractions
            mod = 0.03 * math.sin(2.0 * math.pi * 0.382 * t + k)
            osc = math.sin(2.0 * math.pi * freq * t + mod)
            
            # Pan: from -0.8 (left) to +0.8 (right)
            pan = -0.8 + 1.6 * (k / 4.0)
            gain_l = math.cos((pan + 1.0) * 0.25 * math.pi)
            gain_r = math.sin((pan + 1.0) * 0.25 * math.pi)
            amp = (0.28 / (1.0 + 0.3 * k))
            
            sig_l += osc * gain_l * amp
            sig_r += osc * gain_r * amp
            
        sig_l *= env * 0.8
        sig_r *= env * 0.8
        
        left.append(sig_l)
        right.append(sig_r)
        
    write_wav(output_path, left, right, sample_rate)
    print(f"[Study 033 Draft B] Audio written: {output_path}")

if __name__ == "__main__":
    v_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_033_draft_b_plate.png"))
    a_out = os.path.abspath(os.path.join(os.path.dirname(__file__), "study_033_draft_b_audio.wav"))
    render_draft_b_visual(v_out)
    render_draft_b_audio(a_out)

