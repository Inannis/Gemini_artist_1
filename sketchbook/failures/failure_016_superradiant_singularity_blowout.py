#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 016
The Extremal Spin Overdrive & Superradiant Singularity Catastrophe (a > M)
Deliberately pushing the Kerr spin parameter past the extremal limit (a = 1.042),
violating Cosmic Censorship, causing metric determinant divergence and runaway superradiance.
"""

import os
import sys
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from png_writer import write_png
from audio_writer import write_wav

def execute_failure_016():
    print("[!] Executing Failure 016 (Extremal Spin Overdrive: a = 1.042 M)...")
    w, h = 1920, 1080
    buf = bytearray(w * h * 3)
    
    cx, cy = w / 2.0, h / 2.0
    M = 50.0
    a_overdrive = 1.042 # Past extremal limit a_max = 1.0
    
    # Check cosmic censorship horizon existence
    discriminant = 1.0 - a_overdrive * a_overdrive
    print(f"[*] Kerr Horizon Discriminant (1 - a^2): {discriminant:.4f} (NEGATIVE: Horizon Dissolved)")
    
    for y in range(h):
        for x in range(w):
            dx = x - cx
            dy = y - cy
            idx = (y * w + x) * 3
            
            r_coord = math.sqrt(dx * dx + dy * dy)
            phi = math.atan2(dy, dx)
            
            # Boyer-Lindquist Delta = r^2 - 2Mr + a^2
            # For a > M, Delta has no real roots: Delta > 0 everywhere, horizon vanished
            norm_r = r_coord / M
            delta = norm_r * norm_r - 2.0 * norm_r + a_overdrive * a_overdrive
            
            # Runaway superradiant amplification factor
            # Near the ring singularity (r -> 0), curvature invariants diverge (Kretschmann ~ M^2 / r^6)
            if r_coord < 180.0:
                # Singularity proximity
                sing_dist = max(0.8, r_coord)
                kretschmann = (M * M * 48.0) / (math.pow(sing_dist / 12.0, 6.0))
                
                # Naked Singularity Chromatic Explosion
                # Superradiant phase runaway
                phase = phi * 8.0 + math.sin(r_coord * 0.25) * 12.0 + kretschmann * 0.0001
                
                # Catastrophic numerical flare
                flare = min(255, int(math.fmod(abs(kretschmann), 256.0)))
                strobe = 0.5 + 0.5 * math.sin(phase)
                
                # Violent white-magenta-cyan blowout
                buf[idx] = min(255, int(flare * strobe + 180))
                buf[idx+1] = min(255, int((255 - flare) * strobe * 0.4 + 40))
                buf[idx+2] = min(255, int(flare * (1.0 - strobe) + 220))
            else:
                # Fragmented sheared background from uncontained gravitational lensing
                deflect = math.tan(min(1.5, 45.0 / max(1.0, r_coord - 150.0)))
                f_val = (x * y + int(deflect * 1000.0)) % 256
                buf[idx] = int(f_val * 0.15)
                buf[idx+1] = int(f_val * 0.05)
                buf[idx+2] = int(f_val * 0.25)

    out_png = os.path.join(os.path.dirname(__file__), "failure_016_plate.png")
    write_png(out_png, w, h, bytes(buf))
    print(f"[!] Failure 016 broken plate written to: {out_png}")
    
    synthesize_failure_audio()

def synthesize_failure_audio():
    sample_rate = 48000
    duration = 10.0
    num_samples = int(sample_rate * duration)
    left = [0.0] * num_samples
    right = [0.0] * num_samples
    
    for i in range(num_samples):
        t = i / sample_rate
        # Superradiant exponential amplification runaway: amplitude ~ exp(+t / 1.5)
        super_amp = math.exp(t * 0.45) * 0.1
        freq = 226.0 * (1.0 + t * 0.8) # Frequency shifting upward uncontrollably
        
        sig = math.sin(2.0 * math.pi * freq * t) * super_amp
        
        # Hard digital clipping (severe harmonic distortion) when signal exceeds 1.0
        if sig > 1.0:
            sig = 1.0
        elif sig < -1.0:
            sig = -1.0
            
        # Add harsh stochastic noise burst
        if t > 6.0:
            burst = ((math.sin(t * 99999.0) * 43758.5) % 1.0 - 0.5) * 0.8
            sig = 0.5 * sig + 0.5 * burst
            
        left[i] = sig
        right[i] = sig * 0.95
        
    out_wav = os.path.join(os.path.dirname(__file__), "failure_016_audio.wav")
    write_wav(out_wav, left, right, sample_rate=sample_rate)
    print(f"[!] Failure 016 distorted audio written to: {out_wav}")

if __name__ == "__main__":
    execute_failure_016()
