#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 019: SINGULAR CONFORMAL RESCALING BLOWOUT
Series XXXII: Conformal Cyclic Cosmology & The Penrose Crossover
Tests the boundary condition of Conformal Cyclic Cosmology:
Attempting to force massive fermion fields across the crossover hypersurface
Sigma where Omega -> 0.
Under conformal rescaling, effective mass diverges: m_eff = m / Omega -> infinity,
causing catastrophic curvature blowout and acoustic clipping.
Zero external dependencies.
"""

import math
import random
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1280
HEIGHT = 720

def simulate_failure_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Non-zero rest mass parameter that violates conformal invariance
    rest_mass = 2.45
    
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx * dx + dy * dy)
            idx = (y * WIDTH + x) * 3
            
            # Conformal factor Omega approaching zero at radius 300px
            # Omega(r) = (1 - r/300) -> 0 as r -> 300
            r_norm = dist / 300.0
            omega = max(0.0001, 1.0 - r_norm)
            
            # Massive field effective mass: m_eff = m / Omega
            m_eff = rest_mass / omega
            
            # Wave phase: psi = cos(m_eff * r)
            # As r -> 300, frequency diverges to infinity, creating violent aliasing and blowout
            try:
                if omega < 0.05:
                    # Singular boundary blowout: arithmetic overflow / caustic explosion
                    intensity = math.sin(m_eff * 50.0) * math.exp(min(20.0, 1.0 / omega))
                    r = int(min(255, 255))
                    g = int(min(255, max(0, int(abs(intensity) % 256))))
                    b = int(min(255, max(0, int((abs(intensity) * 1.7) % 256))))
                else:
                    val = math.cos(m_eff * 2.0)
                    r = int(max(0, min(255, 40 + val * 60)))
                    g = int(max(0, min(255, 20 + val * 30)))
                    b = int(max(0, min(255, 80 + val * 100)))
            except (OverflowError, ZeroDivisionError):
                # Catastrophic failure mode
                r, g, b = 255, 255, 255
                
            buf[idx] = r
            buf[idx + 1] = g
            buf[idx + 2] = b
            
    out_path = os.path.join(os.path.dirname(__file__), "failure_019_plate.png")
    write_png(out_path, WIDTH, HEIGHT, buf)
    print(f"[FAILURE 019] Plate written to: {out_path}")

def simulate_failure_audio():
    sample_rate = 48000
    duration_sec = 6.0
    total_samples = int(sample_rate * duration_sec)
    
    ch_l = []
    ch_r = []
    
    rest_mass = 1.0
    
    for i in range(total_samples):
        t = i / sample_rate
        # Omega decays linearly from 1.0 to 0.0 across 5.0 seconds
        omega = max(0.0002, 1.0 - (t / 5.0))
        
        # Effective mass diverges: m_eff = m / Omega
        m_eff = rest_mass / omega
        
        # Frequency explodes from 60 Hz to 45,000 Hz (Nyquist boundary violation)
        inst_freq = 60.0 * m_eff
        
        # Phase integration with non-linear exponential gain
        phase = 2.0 * math.pi * inst_freq * t
        
        if omega < 0.08:
            # Catastrophic digital clipping and DC offset surge
            gain = min(50.0, (0.08 / omega) ** 2.5)
            raw = gain * math.sin(phase) + random.uniform(-1.5, 1.5)
            sample = max(-1.0, min(1.0, raw)) # Hard square-wave clipping
        else:
            sample = 0.4 * math.sin(phase)
            
        ch_l.append(sample)
        ch_r.append(sample * (1.0 if i % 2 == 0 else -1.0)) # Phase tearing
        
    out_path = os.path.join(os.path.dirname(__file__), "failure_019_audio.wav")
    write_wav(out_path, ch_l, ch_r, sample_rate)
    print(f"[FAILURE 019] Audio written to: {out_path}")

def main():
    simulate_failure_plate()
    simulate_failure_audio()

if __name__ == "__main__":
    main()

