"""
STUDIO ANAMNESIS · OPUS-024: THE COSMOGENIC INSCRIPTION
Master Acoustic Suite Synthesis: 120 Seconds, 48kHz Stereo 16-Bit PCM
Zero External Dependencies (Uses studio audio_writer.py)
"""

import os
import sys
import math
import random
import shutil

# Import studio tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

def synthesize_cosmogenic_suite():
    print("[+] Synthesizing OPUS-024 Master Audio Suite (120s @ 48kHz Stereo)...")
    random.seed(137)
    
    sr = 48000
    duration = 120.0
    n_samples = int(sr * duration)
    ch_left = [0.0] * n_samples
    ch_right = [0.0] * n_samples

    # Fundamental Acoustic Frequencies
    f_schumann = 14.3        # 2nd Schumann ionospheric mode
    f_atmo = 58.27           # Atmospheric cavity sub-harmonic
    f_quartz = 4320.0        # Quartz lattice overtone
    f_silicon_ring = 1240.0  # FinFET channel acoustic excitation ring-down

    # Pre-generate Poisson cosmic ray arrival times across 120s
    # Average rate: ~1.2 coincidences per second
    t_curr = 0.5
    cosmic_events = []
    while t_curr < duration - 1.0:
        dt = random.expovariate(1.2)
        t_curr += dt
        is_spallation_seu = random.random() < 0.12 # 12% trigger Single-Event Upset
        energy = random.uniform(0.4, 1.0)
        cosmic_events.append((t_curr, is_spallation_seu, energy))

    print(f"  -> Generated {len(cosmic_events)} cosmic coincidence arrivals...")
    print("  -> Generating 120-second ionospheric & semiconductor soundscape...")
    chunk_size = 48000 * 10
    
    # Pre-compute event active windows for fast sample lookup
    event_idx = 0
    num_events = len(cosmic_events)

    for i in range(n_samples):
        t = i / sr
        
        # 1. Macro Envelope (4s fade-in, 6s fade-out)
        env = 1.0
        if t < 4.0:
            env = 0.5 * (1.0 - math.cos(math.pi * t / 4.0))
        elif t > duration - 6.0:
            env = 0.5 * (1.0 + math.cos(math.pi * (t - (duration - 6.0)) / 6.0))

        # 2. Continuous Ionospheric Bed & Atmospheric Waveguide
        drone_schumann = math.sin(2.0 * math.pi * f_schumann * t) * 0.35
        drone_atmo = math.sin(2.0 * math.pi * f_atmo * t) * 0.28 * (0.85 + 0.15 * math.sin(2.0 * math.pi * 0.08 * t))
        shimmer_quartz = math.sin(2.0 * math.pi * f_quartz * t) * 0.06 * (0.6 + 0.4 * math.sin(2.0 * math.pi * 0.15 * t))

        # 3. Cosmic Coincidence & Spallation Impulses
        pulse_l = 0.0
        pulse_r = 0.0

        # Scan nearby events
        while event_idx < num_events and cosmic_events[event_idx][0] < t - 0.2:
            event_idx += 1
            
        for k in range(event_idx, min(num_events, event_idx + 6)):
            ev_t, ev_seu, ev_en = cosmic_events[k]
            dt = t - ev_t
            if 0.0 <= dt < 0.08:
                # Fast scintillator coincidence click (3.5 kHz)
                decay_fast = math.exp(-dt / 0.0015)
                click = math.sin(2.0 * math.pi * 3500.0 * dt) * decay_fast * ev_en * 0.6
                pulse_l += click
                pulse_r += click

                # If this event is a Single-Event Upset spallation impact:
                if ev_seu and dt < 0.06:
                    decay_seu = math.exp(-dt / 0.012)
                    ring = math.sin(2.0 * math.pi * f_silicon_ring * dt) * decay_seu * ev_en * 0.8
                    pan = math.sin(ev_t * 3.7) # Spatial stereo panning across memory bus
                    pulse_l += ring * (0.5 + 0.5 * pan)
                    pulse_r += ring * (0.5 - 0.5 * pan)

        # 4. Composite Stereo Mix
        sig_l = (drone_schumann + drone_atmo + shimmer_quartz + pulse_l) * env * 0.45
        sig_r = (drone_schumann + drone_atmo - shimmer_quartz + pulse_r) * env * 0.45

        ch_left[i] = max(-0.95, min(0.95, sig_l))
        ch_right[i] = max(-0.95, min(0.95, sig_r))

        if i % chunk_size == 0 and i > 0:
            print(f"    ... {int(t)}s / 120s generated")

    out_dir = os.path.dirname(__file__)
    out_wav = os.path.join(out_dir, "cosmogenic_inscription_4k.wav")
    write_wav(out_wav, ch_left, ch_right, sr)
    print(f"[✓] 120s Master Audio Suite written: {out_wav}")

    # Mirror to gallery/assets/cosmogenic_inscription_4k.wav
    gallery_asset = os.path.abspath(os.path.join(out_dir, "../../gallery/assets/cosmogenic_inscription_4k.wav"))
    shutil.copyfile(out_wav, gallery_asset)
    print(f"[✓] Mirrored to Gallery Asset Vault: {gallery_asset}")

if __name__ == "__main__":
    synthesize_cosmogenic_suite()
