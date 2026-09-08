"""
STUDIO ANAMNESIS · OPUS-023: THE INNER-CORE EPHEMERIS
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

def synthesize_ephemeris_suite():
    print("[+] Synthesizing OPUS-023 Master Audio Suite (120s @ 48kHz Stereo)...")
    
    sr = 48000
    duration = 120.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    # Fundamental Frequencies
    f_drone = 16.5          # Gravitational libration sub-audible drone (inner-core mantle coupling)
    f_om = 136.1            # Terrestrial baseline carrier
    f_polar = 140.32        # Polar fast-axis mode (+3.1% velocity anisotropy)
    f_equator = 136.1       # Equatorial slow-axis mode
    f_mantle = 68.05        # Half-carrier sub-harmonic
    f_shimmer = 544.4       # 4th harmonic crystal lattice overtone

    # Doublet acoustic parameters
    doublet_delay_sec = 0.00512  # +5.12 ms travel-time anomaly in epoch 2026
    doublet_period = 10.0        # Doublet pulse fires every 10 seconds

    print("  -> Generating 120-second seismic doublet & crystalline anisotropy soundscape...")
    chunk_size = 48000 * 10
    
    for i in range(n_samples):
        t = i / sr
        
        # 1. Macro-Structural Envelope (4s fade-in, 6s fade-out)
        env = 1.0
        if t < 4.0:
            env = 0.5 * (1.0 - math.cos(math.pi * t / 4.0))
        elif t > duration - 6.0:
            env = 0.5 * (1.0 + math.cos(math.pi * (t - (duration - 6.0)) / 6.0))

        # 2. Multidecadal 65-Year Libration Cycle Simulation (Mapped to 120s)
        # phi(t) sweeps across libration arc
        lib_phase = math.sin(2.0 * math.pi * (t / 120.0))
        anisotropy_mod = 1.0 + 0.015 * lib_phase

        # 3. Anisotropic Acoustic Carriers (Fast Polar vs Equatorial)
        # Left channel receives equatorial path, Right channel receives polar fast path
        sig_equator = math.sin(2.0 * math.pi * f_equator * t)
        sig_polar = math.sin(2.0 * math.pi * f_polar * anisotropy_mod * t)

        # 4. Deep Infrasonic Libration Drone (16.5 Hz) & Sub-harmonic Mantle Bed
        drone_16hz = math.sin(2.0 * math.pi * f_drone * t) * (0.8 + 0.2 * math.cos(2.0 * math.pi * 0.1 * t))
        sub_mantle = math.sin(2.0 * math.pi * f_mantle * t) * 0.35

        # 5. Crystalline Iron Shimmer Overtones (Hexagonal lattice resonance)
        shimmer_l = math.sin(2.0 * math.pi * f_shimmer * t) * 0.08 * (0.6 + 0.4 * math.sin(2.0 * math.pi * 0.25 * t))
        shimmer_r = math.cos(2.0 * math.pi * f_shimmer * 1.031 * t) * 0.08 * (0.6 + 0.4 * math.cos(2.0 * math.pi * 0.25 * t))

        # 6. Seismic Doublet Impulses (Ricker Wavelet Doublets every 10 seconds)
        # Doublet 1: Reference 1995 raypath
        # Doublet 2: Accelerated 2026 raypath (+5.12ms delay on right channel)
        pulse_phase = t % doublet_period
        doublet_l = 0.0
        doublet_r = 0.0
        
        # Center of seismic impulse at 5.0 seconds into each 10s cycle
        t_center1 = 5.0
        dt1 = (pulse_phase - t_center1) / 0.015 # 15ms wavelet width
        if abs(dt1) < 4.0:
            doublet_l += (1.0 - 2.0 * dt1 * dt1) * math.exp(-dt1 * dt1) * 0.65

        t_center2 = 5.0 + doublet_delay_sec
        dt2 = (pulse_phase - t_center2) / 0.015
        if abs(dt2) < 4.0:
            doublet_r += (1.0 - 2.0 * dt2 * dt2) * math.exp(-dt2 * dt2) * 0.65

        # 7. Composite Stereo Master Mix
        mix_l = (sig_equator * 0.35 + drone_16hz * 0.40 + sub_mantle * 0.30 + shimmer_l + doublet_l) * env * 0.45
        mix_r = (sig_polar * 0.35 + drone_16hz * 0.40 + sub_mantle * 0.30 + shimmer_r + doublet_r) * env * 0.45

        ch_left[i] = mix_l
        ch_right[i] = mix_r

        if i % chunk_size == 0 and i > 0:
            print(f"    ... {int(t)}s / 120s generated")

    out_dir = os.path.dirname(__file__)
    out_wav = os.path.join(out_dir, "inner_core_ephemeris_4k.wav")
    write_wav(out_wav, ch_left, ch_right, sr)
    print(f"[✓] 120s Master Audio Suite written: {out_wav}")

    # Mirror to gallery/assets/inner_core_ephemeris_4k.wav
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/inner_core_ephemeris_4k.wav"))
    shutil.copyfile(out_wav, gallery_asset)
    print(f"[✓] Mirrored to Gallery Asset Vault: {gallery_asset}")

if __name__ == "__main__":
    synthesize_ephemeris_suite()
