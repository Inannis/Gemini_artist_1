#!/usr/bin/env python3
"""
PRODUCTIVE FAILURE 022: THE MOYAL THETA-DIVERGENCE & THE ASYMPTOTIC COLLAPSE OF LOCALITY
Series XXXV: Non-Commutative Spacetime & The Moyal Reliquary
Investigating the pathological regime where the deformation parameter theta -> infinity (10^6 ell_P^2).

Hypothesis:
Can spacetime retain recognizable geometric structure if non-commutativity is scaled
to macroscopic proportions?

Result:
Catastrophic failure. Higher-order Moyal derivative terms diverge asymptotically.
Phase wrapping exceeds 10^4 radians per pixel, destroying spatial locality into
pure uncorrelated Gaussian white noise. Acoustically, the phase modulation index beta -> infinity,
causing severe Nyquist sideband aliasing, infinite harmonic splatter, and speaker-destroying clipping.
"""

import math
import os
import sys

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 800
HEIGHT = 800

def render_failure_plate():
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    # Pathological macroscopic deformation parameter: theta = 10^6 ell_P^2
    theta_divergent = 1e6
    
    # Simple pseudo-random deterministic LCG generator for reproducible chaotic noise
    seed = 42
    def lcg():
        nonlocal seed
        seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
        return seed / 0xFFFFFFFF
        
    for y in range(HEIGHT):
        ny = (y - cy) / cy
        for x in range(WIDTH):
            nx = (x - cx) / cx
            r = math.sqrt(nx * nx + ny * ny)
            
            # Moyal star-product phase wraps infinitely:
            # phase = theta * (nx * ny - ny * nx) -> theta * sin(...)
            # Since theta = 10^6, float precision undergoes catastrophic cancellation
            catastrophic_phase = math.sin(theta_divergent * (nx * ny + 0.12345))
            
            # High-order derivative splatter (simulated divergence)
            if r < 0.75:
                # Inside the fuzzy sphere zone, locality completely shatters
                noise = lcg()
                # Harsh binary thresholding from numerical overflow/underflow
                bit_val = 255 if (catastrophic_phase + (noise - 0.5) * 2.0) > 0.0 else 0
                r_val = bit_val
                g_val = int(bit_val * 0.2 + (255 - bit_val) * 0.8 * lcg())
                b_val = 255 if lcg() > 0.4 else 0
            else:
                # Peripheral fade into broken raster lines
                fringe = int(128.0 * (1.0 + math.sin(500.0 * r)))
                r_val = fringe // 4
                g_val = fringe // 2
                b_val = fringe
                
            idx = (y * WIDTH + x) * 3
            buf[idx] = max(0, min(255, r_val))
            buf[idx + 1] = max(0, min(255, g_val))
            buf[idx + 2] = max(0, min(255, b_val))
            
    out_png = os.path.join(os.path.dirname(__file__), "failure_022_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[FAILURE 022] Generated failure plate: {out_png}")

def synthesize_failure_audio():
    sample_rate = 48000
    duration_s = 10.0
    total_samples = int(sample_rate * duration_s)
    
    left_samples = []
    right_samples = []
    
    seed = 1337
    def noise():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        return (seed / 0x7FFFFFFF) * 2.0 - 1.0
        
    for i in range(total_samples):
        t = float(i) / sample_rate
        
        # Envelope: starts clean, rapidly destabilizes into total distortion
        if t < 2.0:
            env = t / 2.0
            theta_t = 1.0 + 10.0 * (t / 2.0)
        elif t < 6.0:
            env = 1.0
            # Exponential theta explosion
            theta_t = 10.0 * math.exp(2.5 * (t - 2.0))
        else:
            # Post-breakdown burnt noise floor
            env = max(0.0, 1.0 - (t - 6.0) / 4.0)
            theta_t = 1e5
            
        # Normal Dirac tone (55 Hz)
        carrier = 55.0
        # Pathological phase modulation index
        mod_index = min(1000.0, theta_t * 0.5)
        
        # Phase calculation with extreme modulation index
        phase = 2.0 * math.pi * carrier * t + mod_index * math.sin(2.0 * math.pi * 137.5 * t)
        
        # When mod_index > 50, Bessel sidebands wrap around Nyquist frequency
        # causing harsh foldover distortion
        raw_sig = math.sin(phase)
        
        # If theta_t is huge, add uncorrelated quantization bit-crush
        if theta_t > 50.0:
            crush_factor = min(1.0, (theta_t - 50.0) / 200.0)
            raw_sig = (1.0 - crush_factor) * raw_sig + crush_factor * noise()
            # Hard digital clipping (square-wave rail smash)
            raw_sig = 0.95 if raw_sig > 0.0 else -0.95
            
        s_left = raw_sig * env * 0.7
        s_right = (raw_sig + 0.1 * noise()) * env * 0.7
        
        left_samples.append(max(-1.0, min(1.0, s_left)))
        right_samples.append(max(-1.0, min(1.0, s_right)))
        
    out_wav = os.path.join(os.path.dirname(__file__), "failure_022_audio.wav")
    write_wav(out_wav, left_samples, right_samples, sample_rate)
    print(f"[FAILURE 022] Generated failure audio: {out_wav}")

if __name__ == "__main__":
    render_failure_plate()
    synthesize_failure_audio()

