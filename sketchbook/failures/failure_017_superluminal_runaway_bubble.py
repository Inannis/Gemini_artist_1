#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · PRODUCTIVE FAILURE 017
The Superluminal Tachyonic Blowout (Overdriving the Cosmic Speed Limit)
Deliberately pushes the relativistic bubble wall velocity past the speed of light:
v_wall = 1.085 * c
Triggers:
- Mathematical domain collapse (sqrt(1 - v^2/c^2) becomes imaginary)
- Tachyonic causal inversion and anti-causal Moiré interference
- Catastrophic audio clipping and runaway numerical feedback
- Post-mortem analysis proving why c is the cosmic governor of aesthetic form
"""

import cmath
import math
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from png_writer import write_png
from audio_writer import write_wav

WIDTH = 1920
HEIGHT = 1080
SAMPLE_RATE = 48000

def run_failure_simulation():
    print("[FAILURE 017] Initiating superluminal velocity overdrive experiment...")
    
    # 1. VISUAL SIMULATION: Tachyonic phase collapse
    buf = bytearray(WIDTH * HEIGHT * 3)
    cx, cy = WIDTH / 2.0, HEIGHT / 2.0
    
    v_over_c = 1.085 # SUPERLUMINAL OVERDRIVE: Exceeds c by 8.5%
    discriminant = 1.0 - (v_over_c * v_over_c) # = 1.0 - 1.177225 = -0.177225 < 0
    
    print(f"[FAILURE 017] Overdrive parameter v/c = {v_over_c:.3f}")
    print(f"[FAILURE 017] Relativistic discriminant (1 - v^2/c^2) = {discriminant:.6f} < 0 (IMAGINARY)")
    
    gamma_complex = 1.0 / cmath.sqrt(discriminant)
    print(f"[FAILURE 017] Complex Lorentz factor gamma = {gamma_complex.real:.4f} + {gamma_complex.imag:.4f}i")
    
    gamma_mag = abs(gamma_complex)
    gamma_phase = cmath.phase(gamma_complex) # math.pi / 2
    
    random.seed(999)
    
    for y in range(HEIGHT):
        dy = y - cy
        for x in range(WIDTH):
            dx = x - cx
            dist = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx)
            idx = (y * WIDTH + x) * 3
            
            # Tachyonic metric interval: ds^2 = c^2 dt^2 - dr^2 becomes negative
            # Imaginary wave vector produces spatial phase inversion
            tachyonic_phase = math.sin(dist * 0.12 * gamma_mag + angle * 7.0 + gamma_phase)
            
            # Anti-causal Moiré interference pattern (retro-causal wavefronts)
            causal_echo1 = math.sin(dist * 0.35 - x * 0.08)
            causal_echo2 = math.cos(dist * 0.28 + y * 0.09)
            moire = causal_echo1 * causal_echo2
            
            # Runaway energy blowout
            if abs(dist - 380.0) < 160.0:
                blowout_intensity = math.exp(-((dist - 380.0) / 75.0) ** 2) * (1.8 + tachyonic_phase)
            else:
                blowout_intensity = max(0.0, tachyonic_phase * moire * 0.6)
                
            # Severe chromatic aberrations and runaway clipping
            r_val = int(255.0 * blowout_intensity * (1.2 + 0.4 * math.sin(dist * 0.05)))
            g_val = int(255.0 * (blowout_intensity ** 1.8) * (0.8 + 0.5 * math.cos(angle * 5.0)))
            b_val = int(255.0 * (blowout_intensity ** 0.5) * (1.5 + 0.3 * math.sin(x * 0.02)))
            
            # Deliberate numerical artifacting: bitwise corruption from domain wrap
            if blowout_intensity > 1.2:
                r_val = (r_val ^ 0xFF)
                b_val = min(255, b_val + 120)
                
            buf[idx] = max(0, min(255, r_val))
            buf[idx+1] = max(0, min(255, g_val))
            buf[idx+2] = max(0, min(255, b_val))
            
    out_png = os.path.join(os.path.dirname(__file__), "failure_017_plate.png")
    write_png(out_png, WIDTH, HEIGHT, buf)
    print(f"[FAILURE 017] Visual failure plate written: {out_png}")
    
    # 2. ACOUSTIC SIMULATION: Superradiant Runaway Screech & Tachyonic Fold
    dur = 12.0
    n_samples = int(SAMPLE_RATE * dur)
    left = [0.0] * n_samples
    right = [0.0] * n_samples
    
    phase = 0.0
    screech_phase = 0.0
    
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        
        # Ramp velocity from subluminal to superluminal across 6.0 seconds
        v_t = 0.85 + 0.35 * (t / 12.0) # Reaches 1.20 c at t=12s
        
        if v_t < 1.0:
            # Subluminal regime: normal Doppler chirp
            f = 125.10 / (1.0 - v_t)
            phase += (2.0 * math.pi * min(20000.0, f)) / SAMPLE_RATE
            sig = math.sin(phase) * 0.4
            l_val = sig
            r_val = sig
        else:
            # SUPERLUMINAL REGIME (v > c): Tachyonic frequency fold & extreme clipping
            # 1 - v/c is negative: frequency inverts and creates runaway feedback
            overdrive_ratio = (v_t - 1.0) / 0.20 # 0.0 to 1.0
            f_tachyon = 125.10 * math.pow(overdrive_ratio + 0.01, -1.8) # Blows up to infinity
            screech_freq = min(22000.0, 4000.0 + overdrive_ratio * 16000.0)
            
            screech_phase += (2.0 * math.pi * screech_freq) / SAMPLE_RATE
            
            # Catastrophic feedback screech
            feedback_gain = 1.0 + 8.0 * overdrive_ratio
            raw_sig = (math.sin(screech_phase) + (random.random() * 2.0 - 1.0) * overdrive_ratio) * feedback_gain
            
            # Harsh digital clipping (squaring off into harsh square wave blowout)
            clipped_sig = max(-1.0, min(1.0, raw_sig * 3.5))
            
            # Anti-causal cross-talk between left and right channels
            l_val = clipped_sig * 0.95
            r_val = -clipped_sig * 0.95
            
        left[i] = l_val
        right[i] = r_val
        
    out_wav = os.path.join(os.path.dirname(__file__), "failure_017_audio.wav")
    write_wav(out_wav, left, right, SAMPLE_RATE)
    print(f"[FAILURE 017] Acoustic failure suite written: {out_wav}")

if __name__ == "__main__":
    run_failure_simulation()

