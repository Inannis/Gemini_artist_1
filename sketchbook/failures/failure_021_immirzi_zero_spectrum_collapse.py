#!/usr/bin/env python3
"""
FAILURE 021: The Immirzi Zero Spectrum Collapse & Metric Disintegration
Series XXXIV: Quantum Gravity Foam & Spin Networks
Simulates the catastrophic failure mode when the Barbero-Immirzi parameter gamma -> 0.
The area quantum Delta_min collapses, causing the volume eigenvalues of intertwiners
to crash to zero and local spatial curvature to violently diverge into numerical blowout.
Zero external dependencies.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "telemetry"))
from png_writer import write_png
from audio_writer import write_wav
from spin_network import SpinNetworkGraph

WIDTH = 1280
HEIGHT = 720

def render_failure_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    net = SpinNetworkGraph(num_nodes=64, seed=244)
    
    # Render catastrophic collapse: as radius expands or edges contract to singularity
    # Background: black void corrupted by metric dislocation streaks
    for y in range(HEIGHT):
        ny = (y - cy) / cy
        for x in range(WIDTH):
            nx = (x - cx) / cx
            r = math.sqrt(nx * nx + ny * ny)
            
            # Metric tearing noise when gamma collapses
            idx = (y * WIDTH + x) * 3
            if abs(ny) < 0.08:
                # Singularity plane blowout
                blowout = int(255 * math.exp(-abs(ny) * 45.0) * (0.8 + 0.2 * math.sin(nx * 120.0)))
                buf[idx] = min(255, blowout)
                buf[idx + 1] = min(255, int(blowout * 0.4))
                buf[idx + 2] = min(255, int(blowout * 0.1))
            else:
                # Disintegrated foam artifact
                h = math.sin(nx * 40.0 / (abs(ny) + 0.05)) * math.cos(ny * 30.0)
                if abs(h) > 0.92:
                    buf[idx] = 180
                    buf[idx + 1] = 40
                    buf[idx + 2] = 70
                else:
                    buf[idx] = 4
                    buf[idx + 1] = 2
                    buf[idx + 2] = 8

    # Collapsed spin network edges violently pulled into central singularity (0, 0)
    for edge in net.edges:
        n1 = net.nodes[edge["node1"]]
        n2 = net.nodes[edge["node2"]]
        
        # Pull toward center with chaotic non-linear pinch
        p1_x = cx + n1["x"] * 380.0 * 0.15
        p1_y = cy + n1["y"] * 80.0 * 0.10
        p2_x = cx + n2["x"] * 380.0 * 0.15
        p2_y = cy + n2["y"] * 80.0 * 0.10
        
        dx = p2_x - p1_x
        dy = p2_y - p1_y
        dist = math.hypot(dx, dy)
        steps = max(1, int(dist * 3.0))
        for s in range(steps):
            t = s / steps
            px = int(p1_x + t * dx)
            py = int(p1_y + t * dy)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                pidx = (py * WIDTH + px) * 3
                buf[pidx] = 255
                buf[pidx + 1] = 220
                buf[pidx + 2] = 200

    out_png = os.path.join(os.path.dirname(__file__), "failure_021_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[FAILURE 021] Rendered plate: {out_png}")

def render_failure_audio():
    sample_rate = 48000
    duration = 12.0
    num_samples = int(sample_rate * duration)
    left = []
    right = []
    
    # Progression:
    # 0s - 4s: Stable spin network chords (gamma = 0.274)
    # 4s - 8s: Rapid collapse of gamma -> 0, frequencies diverge violently (rho -> infty)
    # 8s - 10s: Uncontrolled digital clipping screech & Nyquist foldback
    # 10s - 12s: Total collapse into dead void null
    
    for i in range(num_samples):
        t = i / sample_rate
        
        if t < 4.0:
            # Stable discrete spin network tone
            gamma = 0.274067
            sig_l = 0.25 * math.sin(2.0 * math.pi * 74.8 * t) + 0.18 * math.sin(2.0 * math.pi * 122.2 * t)
            sig_r = 0.25 * math.sin(2.0 * math.pi * 75.1 * t) + 0.18 * math.sin(2.0 * math.pi * 121.8 * t)
        elif t < 8.0:
            # Progressive collapse of gamma
            p = (t - 4.0) / 4.0
            gamma = 0.274067 * (1.0 - p) + 0.0001
            # Curvature density explodes as 1/gamma
            freq_base = 74.8 * (0.274067 / gamma)
            amp = 0.4 + p * 0.5
            # Chaotic phase modulation
            phase_mod = math.sin(2.0 * math.pi * (freq_base * 0.1) * t) * 5.0 * p
            sig_l = amp * math.sin(2.0 * math.pi * freq_base * t + phase_mod)
            sig_r = amp * math.cos(2.0 * math.pi * (freq_base * 1.05) * t - phase_mod)
        elif t < 9.8:
            # Full blow-out clip & foldback screech
            p = (t - 8.0) / 1.8
            screech_freq = 9400.0 + 8500.0 * math.sin(2.0 * math.pi * 32.0 * t)
            raw = 1.8 * math.sin(2.0 * math.pi * screech_freq * t) + 0.8 * (math.sin(t * 12345.67) > 0.0)
            # Hard clip
            sig_l = max(-0.99, min(0.99, raw))
            sig_r = max(-0.99, min(0.99, -raw * 0.9))
        else:
            # Complete spatial extinction (vacuum null)
            sig_l = 0.0
            sig_r = 0.0
            
        left.append(sig_l)
        right.append(sig_r)
        
    out_wav = os.path.join(os.path.dirname(__file__), "failure_021_audio.wav")
    write_wav(out_wav, left, right, sample_rate)
    print(f"[FAILURE 021] Synthesized audio: {out_wav}")

if __name__ == "__main__":
    render_failure_plate()
    render_failure_audio()

