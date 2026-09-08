"""
STUDIO ANAMNESIS · MASTERWORK OPUS-026 ACOUSTIC SUITE
Piece: The Oort Horizon (Galactic Tides & The Jacobi Boundary)
Format: 120.0s 48kHz Stereo 16-bit PCM WAV (Master Symphonic Suite)

Movement Architecture:
1. Movement I (00:00 - 00:30): The Hills Reservoir & The Frozen Periphery (2,000 - 20,000 AU)
   - 36 Hz / 54 Hz sub-harmonic foundational drone, crystalline ice micro-resonances (1,200 - 2,400 Hz), faint solar gravitational pull.
2. Movement II (00:30 - 01:00): The Kozai Tidal Pendulum (20,000 - 60,000 AU)
   - Vertical disc tide harmonic sweeps (72 Hz, 108 Hz, 144 Hz), Kozai-Lidov eccentricity pumping glissandi (360 -> 720 Hz), secular orbital breathing.
3. Movement III (01:00 - 01:35): The Jacobi Horizon Crossing (60,000 - 105,000 AU)
   - Gravitational equilibrium saddle point (a_sun ~ a_tide = 5.9e-13 m/s^2), binaural tidal shearing textures, probe unbinding threshold.
4. Movement IV (01:35 - 02:00): The Galactic Drift & Epicyclic Dissolution (> 105,000 AU)
   - Unbound Milky Way halo resonances (27 Hz, 54 Hz, 81 Hz), 83.6 Myr disc crossing envelope, eternal non-semantic silent drift.

Zero external dependencies: uses pure Python standard library.
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from audio_writer import write_wav

def synthesize():
    print("[+] Synthesizing OPUS-026 Master Acoustic Suite (120s 48kHz Stereo)...")
    random.seed(83570000)
    
    sr = 48000
    duration = 120.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # State variables
    phase_sub_drone = 0.0
    phase_tide_drone = 0.0
    phase_kozai_1 = 0.0
    phase_kozai_2 = 0.0
    phase_halo_low = 0.0
    phase_halo_mid = 0.0
    
    # Generate cometary event pings (Poisson process of eccentricity plunges)
    num_events = 28
    events = []
    for _ in range(num_events):
        t_ev = random.uniform(25.0, 95.0)
        freq_ev = random.uniform(440.0, 1100.0)
        dur_ev = random.uniform(1.5, 3.5)
        pan_ev = random.uniform(0.1, 0.9)
        amp_ev = random.uniform(0.08, 0.22)
        events.append((t_ev, freq_ev, dur_ev, pan_ev, amp_ev))

    for i in range(num_samples):
        t = i / sr
        
        # Astronomical distance scale across 120 seconds:
        # t = 0 -> 2,000 AU; t = 75 -> 105,000 AU (Jacobi crossing); t = 120 -> 180,000 AU (Galactic halo)
        dist_au = 2000.0 * math.exp(t / 120.0 * math.log(180000.0 / 2000.0))
        
        # Movement Envelopes
        # Mov 1: 0 to 30s
        env_m1 = max(0.0, 1.0 - t / 35.0) if t < 35.0 else 0.0
        # Mov 2: 25 to 65s
        env_m2 = math.exp(-((t - 45.0) / 15.0)**2)
        # Mov 3: 55 to 100s
        env_m3 = math.exp(-((t - 78.0) / 16.0)**2)
        # Mov 4: 90 to 120s
        env_m4 = max(0.0, (t - 85.0) / 35.0) if t >= 85.0 else 0.0
        
        # 1. Sub-harmonic Foundational Drones
        # 36 Hz base with slow vertical disc modulation (83.6 Myr scaled to 24s period)
        disc_mod = 1.0 + 0.15 * math.sin(2.0 * math.pi * t / 24.0)
        f_sub = 36.0 * disc_mod
        phase_sub_drone += 2.0 * math.pi * f_sub / sr
        d_sub = math.sin(phase_sub_drone) * 0.25 * (env_m1 * 0.9 + env_m2 * 0.7 + env_m3 * 0.5)
        
        # 2. Kozai Tidal Harmonics (Mov 2 & 3)
        # Sweeping 72 Hz and 108 Hz modulated by eccentricity pumping
        f_k1 = 72.0 + 12.0 * math.sin(2.0 * math.pi * t / 8.0)
        f_k2 = 108.0 + 18.0 * math.cos(2.0 * math.pi * t / 8.0)
        phase_kozai_1 += 2.0 * math.pi * f_k1 / sr
        phase_kozai_2 += 2.0 * math.pi * f_k2 / sr
        d_kozai = (math.sin(phase_kozai_1) * 0.18 + math.sin(phase_kozai_2) * 0.12) * (env_m2 + env_m3 * 0.8)
        
        # 3. Jacobi Tidal Shearing (Mov 3: t = 60 to 95)
        # Inharmonic binaural beat representing gravitational tear
        f_shear_l = 216.0
        f_shear_r = 219.5 # 3.5 Hz binaural wobble
        phase_tide_drone += 2.0 * math.pi * f_shear_l / sr
        shear_l = math.sin(phase_tide_drone) * 0.14 * env_m3
        shear_r = math.sin(phase_tide_drone * (f_shear_r / f_shear_l)) * 0.14 * env_m3
        
        # 4. Galactic Halo Majestic Dispersion (Mov 4: t = 90 to 120)
        # Pure tri-tone (27 Hz, 54 Hz, 81 Hz) with lush spatial width
        f_h1 = 27.0
        f_h2 = 54.0
        f_h3 = 81.0
        phase_halo_low += 2.0 * math.pi * f_h1 / sr
        phase_halo_mid += 2.0 * math.pi * f_h2 / sr
        halo_signal = (math.sin(phase_halo_low) * 0.22 + math.sin(phase_halo_mid) * 0.16 + math.sin(phase_halo_mid * 1.5) * 0.10) * env_m4
        
        # 5. Crystalline Planetesimal & Ice Reflections (High-frequency scintillations)
        # Noise filtered by resonant cavity
        noise_raw = random.uniform(-1.0, 1.0)
        ice_scint = noise_raw * 0.02 * (env_m1 * 0.6 + env_m4 * 0.8)
        
        # 6. Accumulate base signals into channels
        sig_l = d_sub + d_kozai * 0.85 + shear_l + halo_signal * 0.95 + ice_scint
        sig_r = d_sub + d_kozai * 1.15 + shear_r + halo_signal * 1.05 - ice_scint
        
        # 7. Add Discrete Cometary Eccentricity Pings
        for t_ev, freq_ev, dur_ev, pan_ev, amp_ev in events:
            if t_ev <= t < t_ev + dur_ev:
                dt_ev = t - t_ev
                env_ev = math.sin(math.pi * dt_ev / dur_ev) * math.exp(-dt_ev * 1.2)
                osc_ev = math.sin(2.0 * math.pi * freq_ev * dt_ev) * env_ev * amp_ev
                sig_l += osc_ev * (1.0 - pan_ev)
                sig_r += osc_ev * pan_ev
                
        # Master fade in (2s) and fade out (4s)
        master_env = min(1.0, t / 2.5) * min(1.0, (duration - t) / 4.0)
        audio_l[i] = max(-0.95, min(0.95, sig_l * master_env))
        audio_r[i] = max(-0.95, min(0.95, sig_r * master_env))

    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "oort_horizon_4k.wav"))
    write_wav(out_path, audio_l, audio_r, sample_rate=sr)
    print(f"[+] OPUS-026 Master Symphonic Suite saved to: {out_path}")

if __name__ == "__main__":
    synthesize()
