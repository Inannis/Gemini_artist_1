#!/usr/bin/env python3
"""
FAILURE 020: ENTANGLEMENT DISCONNECTION SINGULARITY
Series XXXIII: The Holographic Matrix & Bulk-Boundary Dualities
Simulates the catastrophic tearing of bulk spacetime when boundary quantum entanglement
is driven to zero (Van Raamsdonk Disconnection Catastrophe).
Produces severe metric singularities, jagged pixel shears, and +16.8 dBFS digital blowout.
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

def render_failure_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    disk_radius = 480.0
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3
            
            if dist > disk_radius + 4.0:
                buf[idx] = 2
                buf[idx + 1] = 2
                buf[idx + 2] = 4
                continue
                
            norm_r = dist / disk_radius
            ang = math.atan2(dy, dx)
            
            # Distance from vertical throat fault line (x = cx, i.e. dx = 0)
            throat_dist = abs(dx) / disk_radius
            
            # Van Raamsdonk throat contraction:
            # Throat neck width w_neck -> 0 as entanglement S -> 0
            # Around dx = 0, metric pinches off with severe singular tearing
            if throat_dist < 0.12:
                # Singularity zone: curvature blowout
                # Shear displacement
                shear = math.sin(dy * 0.15) * 24.0 + math.cos(dy * 0.08) * 12.0
                displaced_dx = dx + shear
                
                # Extreme high-frequency metric noise & blowout
                noise = math.sin(displaced_dx * 3.7 + dy * 1.9) * math.cos(dy * 4.2)
                blowout = math.exp(-0.5 * (throat_dist / 0.03) ** 2)
                
                # Searing white-hot and corrupted chromatic glitch
                r = int(min(255, 20 + 235 * blowout + 80 * abs(noise)))
                g = int(min(255, 10 + 210 * blowout + 40 * math.sin(dy * 0.3)))
                b = int(min(255, 40 + 255 * blowout + 160 * math.cos(dx * 0.4)))
                
                # Digital bit-crush artifact
                if int(y / 4) % 3 == 0:
                    r = min(255, r ^ 0x9f)
                    b = min(255, b ^ 0xc3)
            else:
                # Disconnecting bulk hemispheres
                # Left hemisphere (dx < 0) vs Right hemisphere (dx > 0)
                # Hyperbolic distortion pulling violently away from center
                repulsion = 1.0 + 0.35 * math.exp(-throat_dist * 4.0)
                curv_factor = norm_r * repulsion
                
                if dx < 0:
                    # Left manifold: cold dying cobalt
                    r = int(min(255, 8 + 30 * curv_factor))
                    g = int(min(255, 14 + 40 * (1.0 - norm_r)))
                    b = int(min(255, 45 + 110 * curv_factor))
                else:
                    # Right manifold: scorched amber-violet
                    r = int(min(255, 45 + 120 * curv_factor))
                    g = int(min(255, 15 + 35 * (1.0 - norm_r)))
                    b = int(min(255, 30 + 80 * curv_factor))
                    
                # Ruptured geodesic fragments
                frag = math.sin(dist * 0.1 + ang * 7.0) * math.cos(dist * 0.05)
                if abs(frag) > 0.88:
                    r = min(255, r + 70)
                    g = min(255, g + 80)
                    b = min(255, b + 110)
                    
            buf[idx] = min(255, max(0, r))
            buf[idx + 1] = min(255, max(0, g))
            buf[idx + 2] = min(255, max(0, b))
            
    out_path = os.path.join(os.path.dirname(__file__), "failure_020_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[FAILURE 020] Generated Disconnection Singularity plate: {out_path}")

def render_failure_audio():
    sample_rate = 48000
    duration = 12.0
    num_samples = int(sample_rate * duration)
    left = []
    right = []
    
    # 0s - 5s: Smooth holographic bulk drone, steadily increasing tension
    # 5s - 8s: Entanglement drops toward zero, throat pinches off, severe distortion starts
    # 8s - 10s: Catastrophic blowout, +16.8 dBFS digital clipping screech, aliasing
    # 10s - 12s: Metric collapse, absolute dead vacuum silence
    
    for i in range(num_samples):
        t = i / sample_rate
        
        if t < 5.0:
            env = min(1.0, t / 1.5)
            # Normal bulk harmonics
            s_l = env * (0.35 * math.sin(2.0 * math.pi * 54.0 * t) + 0.15 * math.sin(2.0 * math.pi * 320.0 * t))
            s_r = env * (0.35 * math.sin(2.0 * math.pi * 54.0 * t + 0.4) + 0.15 * math.sin(2.0 * math.pi * 324.0 * t))
        elif t < 8.0:
            # Throat pinching
            p = (t - 5.0) / 3.0
            throat_width = 1.0 - p
            tension_freq = 54.0 + 800.0 * (p ** 2)
            # Harmonic destabilization
            jitter = math.sin(2.0 * math.pi * 45.0 * t) * (p * 0.4)
            raw_l = math.sin(2.0 * math.pi * tension_freq * t + jitter) * (1.0 + 2.0 * p)
            raw_r = math.sin(2.0 * math.pi * (tension_freq * 1.01) * t - jitter) * (1.0 + 2.0 * p)
            # Begin soft clipping
            s_l = math.tanh(raw_l) * 0.8
            s_r = math.tanh(raw_r) * 0.8
        elif t < 9.8:
            # Catastrophic blowout (+16.8 dBFS digital distortion)
            p_cat = (t - 8.0) / 1.8
            # Hyperbolic singularity
            singularity_amp = 8.0 / max(0.01, 1.0 - p_cat * 0.95)
            raw_sig = (math.sin(2.0 * math.pi * 3840.0 * t) + 
                       math.sin(2.0 * math.pi * 7920.0 * t) + 
                       math.sin(2.0 * math.pi * 14400.0 * t)) * singularity_amp
            # Hard digital clipping with sign foldback
            s_clipped = max(-1.0, min(1.0, raw_sig * 0.2))
            # Phase inversion screech
            s_l = s_clipped * (0.95 if int(t * 120) % 2 == 0 else -0.95)
            s_r = -s_clipped * (0.95 if int(t * 90) % 2 == 0 else -0.95)
        else:
            # Absolute metric erasure: vacuum silence
            s_l = 0.0
            s_r = 0.0
            
        left.append(s_l)
        right.append(s_r)
        
    out_audio = os.path.join(os.path.dirname(__file__), "failure_020_audio.wav")
    write_wav(out_audio, left, right, sample_rate)
    print(f"[FAILURE 020] Generated Disconnection Singularity audio: {out_audio}")

if __name__ == "__main__":
    render_failure_plate()
    render_failure_audio()
