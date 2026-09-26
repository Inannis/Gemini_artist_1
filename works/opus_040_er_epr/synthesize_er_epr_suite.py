#!/usr/bin/env python3
"""
OPUS-040: ER = EPR & The Traversable Wormhole (120-Second 48kHz Master Suite)
Studio Anamnesis · Series XXXVIII · Cornerstone #18

Four Movements:
1. Movement I: The Thermofield Double & Dual Boundary Bath (0 - 30s)
2. Movement II: Linear Complexity & Interior Throat Growth (30 - 60s)
3. Movement III: The Gao-Jafferis-Wall Negative Energy Pulse (60 - 90s)
4. Movement IV: Holographic Teleportation & Quantum Un-Scrambling (90 - 120s)

Pure Python standard library + audio_writer (Zero external dependencies).
"""

import math
import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0

def synthesize_suite():
    print(f"[+] Synthesizing 120s 48kHz stereo master suite ({int(SAMPLE_RATE * DURATION)} samples)...")
    num_samples = int(SAMPLE_RATE * DURATION)
    left_channel = [0.0] * num_samples
    right_channel = [0.0] * num_samples
    
    f0 = 96.42
    f_sub = f0 * 0.5
    f_high = f0 * 8.0
    beta = 5.0265
    
    for i in range(num_samples):
        if i % (SAMPLE_RATE * 15) == 0:
            print(f"    Synthesis progress: {i / num_samples * 100:.1f}% ({i / SAMPLE_RATE:.0f}s)...")
        t = i / SAMPLE_RATE
        
        # Global studio fade-in and fade-out
        fade_in = min(1.0, t / 4.0)
        fade_out = min(1.0, (DURATION - t) / 4.0)
        env = fade_in * fade_out
        
        # --- MOVEMENT I: The Thermofield Double (0 - 30s) ---
        m1_weight = max(0.0, min(1.0, (30.0 - t) / 10.0)) if t < 30.0 else 0.0
        if t < 35.0:
            # Independent thermal Hawking fluctuations
            drift = 0.7 * math.sin(t * (2.0 * math.pi / beta))
            s_l_m1 = math.sin(2.0 * math.pi * f0 * t) * 0.4 + math.sin(2.0 * math.pi * f0 * 2.0 * t) * 0.15
            s_r_m1 = math.sin(2.0 * math.pi * f0 * t + drift) * 0.4 + math.sin(2.0 * math.pi * f0 * 2.0 * t + drift) * 0.15
            # Sub-harmonic breathing
            s_sub_m1 = math.sin(2.0 * math.pi * f_sub * t) * 0.25
            l1 = (s_l_m1 + s_sub_m1) * m1_weight
            r1 = (s_r_m1 + s_sub_m1) * m1_weight
        else:
            l1, r1 = 0.0, 0.0
            
        # --- MOVEMENT II: Interior Throat Growth (30 - 60s) ---
        if 25.0 <= t <= 65.0:
            m2_weight = math.sin(max(0.0, min(math.pi, (t - 25.0) / 40.0 * math.pi)))
            # Throat stretches linearly: frequency descends
            progress = (t - 30.0) / 30.0
            progress = max(0.0, min(1.0, progress))
            f_stretch = f0 * (1.0 - 0.33 * progress)  # 96.42 -> 64.28 Hz
            
            # Non-traversable singularity sub-bass rumble
            singularity_rumble = math.sin(2.0 * math.pi * 32.14 * t) * (0.3 + 0.2 * math.sin(t * 1.3))
            s_l_m2 = math.sin(2.0 * math.pi * f_stretch * t) * 0.45 + singularity_rumble
            s_r_m2 = math.sin(2.0 * math.pi * f_stretch * t * 1.01) * 0.45 + singularity_rumble
            l2 = s_l_m2 * m2_weight
            r2 = s_r_m2 * m2_weight
        else:
            l2, r2 = 0.0, 0.0
            
        # --- MOVEMENT III: The Negative Energy Pulse (60 - 90s) ---
        if 55.0 <= t <= 95.0:
            m3_weight = math.sin(max(0.0, min(math.pi, (t - 55.0) / 40.0 * math.pi)))
            # Bilateral coupling pulse at t = 72.0s
            t_pulse = 72.0
            pulse_dist = abs(t - t_pulse)
            pulse_anec = math.exp(-(pulse_dist ** 2) / 1.5)
            
            # Inverted negative-energy gravitational bass wave
            s_anec = math.sin(2.0 * math.pi * f_sub * t) * (0.3 + 0.6 * pulse_anec)
            # Throat acoustic opening resonance
            f_open = f0 * (1.0 + 0.25 * pulse_anec)
            s_throat = math.sin(2.0 * math.pi * f_open * t) * 0.4
            
            l3 = (s_throat + s_anec) * m3_weight
            r3 = (s_throat + s_anec) * m3_weight
        else:
            l3, r3 = 0.0, 0.0
            
        # --- MOVEMENT IV: Holographic Teleportation & Un-Scrambling (90 - 120s) ---
        if t >= 85.0:
            m4_weight = max(0.0, min(1.0, (t - 85.0) / 10.0))
            # Qubit teleports from Left to Right through the open traversable window
            t_transit = t - 90.0
            
            # Scrambling high-frequency chord focusing into coherence
            scramble_decay = math.exp(-max(0.0, t_transit - 8.0) / 6.0)
            f_scramble = f_high * (1.0 + 0.05 * math.sin(t * 8.0))
            s_scramble_l = math.sin(2.0 * math.pi * f_scramble * t) * 0.15 * scramble_decay
            
            # Emergent coherent harmonic chord on Right boundary
            coherence_growth = min(1.0, max(0.0, t_transit / 12.0))
            chord_1 = math.sin(2.0 * math.pi * f0 * t) * 0.4
            chord_2 = math.sin(2.0 * math.pi * f0 * 1.5 * t) * 0.25 * coherence_growth
            chord_3 = math.sin(2.0 * math.pi * f0 * 2.0 * t) * 0.2 * coherence_growth
            chord_4 = math.sin(2.0 * math.pi * f_sub * t) * 0.3
            
            s_teleported_chord = chord_1 + chord_2 + chord_3 + chord_4
            
            l4 = (s_teleported_chord + s_scramble_l) * m4_weight
            r4 = (s_teleported_chord + s_scramble_l * 0.5) * m4_weight
        else:
            l4, r4 = 0.0, 0.0
            
        # Master mix
        l_mix = (l1 + l2 + l3 + l4) * env * 0.82
        r_mix = (r1 + r2 + r3 + r4) * env * 0.82
        
        left_channel[i] = max(-1.0, min(1.0, l_mix))
        right_channel[i] = max(-1.0, min(1.0, r_mix))
        
    out_dir = os.path.dirname(__file__)
    opus_path = os.path.join(out_dir, "the_traversable_wormhole_4k.wav")
    gallery_path = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/opus_040_audio.wav"))
    
    print(f"[+] Writing 120s master WAV to {opus_path}...")
    write_wav(opus_path, left_channel, right_channel, SAMPLE_RATE)
    print(f"[+] Mirroring master audio to {gallery_path}...")
    shutil.copyfile(opus_path, gallery_path)
    print("[✓] OPUS-040 120s Master Suite successfully synthesized and vaulted.")

if __name__ == "__main__":
    synthesize_suite()
