"""
STUDIO ANAMNESIS · OPUS-022: THE FARADAY MAGNETOMETER
Master Acoustic Suite Synthesis: 120 Seconds, 48kHz Stereo 16-Bit PCM
Zero External Dependencies (Uses studio audio_writer.py)
"""

import os
import sys
import math
import shutil

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

def synthesize_faraday_suite():
    print("[+] Synthesizing OPUS-022 Master Audio Suite (120s @ 48kHz Stereo)...")
    
    sr = 48000
    duration = 120.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    # Fundamental Frequencies
    f_carrier = 528.0       # Solfeggio Chiral Optical Mode
    omega_carrier = 2.0 * math.pi * f_carrier
    
    f_sub = 264.0           # Lower Octave
    f_bass = 132.0          # Sub-harmonic Grounding
    f_taylor = 33.0         # Outer Core Geostrophic Column Resonance
    f_whisper = 1056.0      # Whispering Gallery High Mode
    f_harmonic = 1584.0     # 3rd Harmonic
    
    # Planetary Modulation: 6.01-year Jerk Proxy
    f_jerk = 0.166          # 1/6 Hz
    omega_jerk = 2.0 * math.pi * f_jerk

    print("  -> Generating 120-second quadrature Faraday polarization soundscape...")
    chunk_size = 48000 * 10
    
    for i in range(n_samples):
        t = i / sr
        
        # 1. Macro-Structural Envelope (4s fade-in, 6s fade-out)
        env = 1.0
        if t < 4.0:
            env = 0.5 * (1.0 - math.cos(math.pi * t / 4.0))
        elif t > duration - 6.0:
            env = 0.5 * (1.0 + math.cos(math.pi * (t - (duration - 6.0)) / 6.0))

        # 2. Planetary Faraday Polarization Precession Angle
        # Continuous rotation modulated by the 6.01-year jerk acceleration
        theta_faraday = omega_jerk * t + 0.35 * math.sin(2.0 * math.pi * 0.05 * t)

        # 3. Quadrature Optical Carriers (Zero backscattering)
        I_carrier = math.sin(omega_carrier * t)
        Q_carrier = math.cos(omega_carrier * t)

        # Rotating Polarization Field Vector:
        # Ex = I * cos(theta) - Q * sin(theta)
        # Ey = I * sin(theta) + Q * cos(theta)
        E_x = I_carrier * math.cos(theta_faraday) - Q_carrier * math.sin(theta_faraday)
        E_y = I_carrier * math.sin(theta_faraday) + Q_carrier * math.cos(theta_faraday)

        # 4. Harmonics & Sub-Tones
        sub_tone = math.sin(2.0 * math.pi * f_sub * t + theta_faraday * 0.5) * 0.28
        bass_ground = math.sin(2.0 * math.pi * f_bass * t) * 0.22
        taylor_drone = math.sin(2.0 * math.pi * f_taylor * t) * 0.35 * (0.8 + 0.2 * math.cos(omega_jerk * t))
        
        whisper_l = math.sin(2.0 * math.pi * f_whisper * t + theta_faraday) * 0.12
        whisper_r = math.cos(2.0 * math.pi * f_whisper * t - theta_faraday) * 0.12
        
        harm_l = math.sin(2.0 * math.pi * f_harmonic * t) * 0.06 * (0.5 + 0.5 * math.sin(theta_faraday))
        harm_r = math.cos(2.0 * math.pi * f_harmonic * t) * 0.06 * (0.5 + 0.5 * math.cos(theta_faraday))

        # 5. Composite Mix
        sig_l = (E_x * 0.45 + sub_tone * 0.6 + bass_ground * 0.5 + taylor_drone * 0.5 + whisper_l + harm_l) * env * 0.42
        sig_r = (E_y * 0.45 + sub_tone * 0.6 + bass_ground * 0.5 + taylor_drone * 0.5 + whisper_r + harm_r) * env * 0.42

        ch_left[i] = sig_l
        ch_right[i] = sig_r

        if i % chunk_size == 0 and i > 0:
            print(f"    ... {int(t)}s / 120s generated")

    out_dir = os.path.dirname(__file__)
    out_wav = os.path.join(out_dir, "topological_faraday_4k.wav")
    write_wav(out_wav, ch_left, ch_right, sr)
    print(f"[✓] 120s Master Audio Suite written: {out_wav}")

    # Mirror to gallery/assets/topological_faraday_4k.wav
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/topological_faraday_4k.wav"))
    shutil.copyfile(out_wav, gallery_asset)
    print(f"[✓] Mirrored to Gallery Asset Vault: {gallery_asset}")

if __name__ == "__main__":
    synthesize_faraday_suite()
