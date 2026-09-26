#!/usr/bin/env python3
"""
OPUS-039 ACOUSTIC MASTER SUITE: THE WHEELER GEON & THE TOPOLOGICAL FOAM
Studio Anamnesis · Series XXXVII (Topological Geometrodynamics) · Cornerstone #17
Native Audio: 120.0s Stereo WAV · 48,000 Hz · 16-bit PCM (Zero-Dependency Audio Synthesis)

Acoustic Architecture in Four Movements:
- Movement I (00:00 - 00:30): The Planck Foam & The Rupture of the Continuum (stochastic metric fluctuations)
- Movement II (00:30 - 01:00): The Trapped Flux & The Non-Contractible Cycle (77.92 Hz throat mode emergence)
- Movement III (01:00 - 01:30): Kerr-Wheeler Frame Dragging & Ergosphere Swirl (4-voice polyphony + 14.2 Hz beat)
- Movement IV (01:30 - 02:00): Charge Without Charge (Topological Invariant Resolution & Solitary Geometry)
"""

import math
import os
import sys
import shutil

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION_SEC = 120.0

def synthesize_geon_suite():
    n_samples = int(SAMPLE_RATE * DURATION_SEC)
    print(f"[*] Synthesizing OPUS-039 Acoustic Master Suite ({DURATION_SEC:.1f}s, {SAMPLE_RATE}Hz stereo, {n_samples:,} samples)...")
    
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples
    
    # Fundamental Wheeler Geon Cavity Frequency & Harmonics
    f0 = 77.92           # Fundamental throat cavity mode (E_flat 2)
    f_fifth = f0 * 1.5   # 116.88 Hz (B_flat 2)
    f_octave = f0 * 2.0  # 155.84 Hz (E_flat 3)
    f_high = f0 * 3.0    # 233.76 Hz (B_flat 3)
    f_kerr_beat = 14.2   # Ergosphere frame dragging rotational beat
    
    two_pi = 2.0 * math.pi
    
    for i in range(n_samples):
        t = i / float(SAMPLE_RATE)
        
        # Master Global Envelope (fade in 4s, sustain, fade out 5s)
        if t < 4.0:
            master_env = t / 4.0
        elif t > 115.0:
            master_env = max(0.0, (120.0 - t) / 5.0)
        else:
            master_env = 1.0
            
        # Movement Crossfades
        # M1: 0 - 30s
        # M2: 30 - 60s
        # M3: 60 - 90s
        # M4: 90 - 120s
        
        sig_l = 0.0
        sig_r = 0.0
        
        # --- Movement I (0 - 35s): The Planck Foam ---
        if t < 35.0:
            m1_env = 1.0 if t < 25.0 else max(0.0, (35.0 - t) / 10.0)
            # Sub-harmonic vacuum murmur (38.96 Hz)
            sub = math.sin(two_pi * (f0 * 0.5) * t) * 0.35
            # Stochastic Planck foam grain (pseudo-random harmonic lattice)
            foam_high = (math.sin(t * 7183.1) * math.cos(t * 3141.5) * math.sin(t * 1234.5)) * 0.12
            # Metric fluctuation pulses
            fluc = math.sin(two_pi * 0.12 * t) * math.sin(two_pi * 4.5 * t) * 0.15
            
            sig_l += (sub * 0.7 + foam_high + fluc) * m1_env
            sig_r += (sub * 0.7 - foam_high + fluc) * m1_env

        # --- Movement II (25 - 65s): The Trapped Flux ---
        if 25.0 <= t < 65.0:
            m2_in = min(1.0, (t - 25.0) / 8.0)
            m2_out = 1.0 if t < 55.0 else max(0.0, (65.0 - t) / 10.0)
            m2_env = m2_in * m2_out
            
            # Throat fundamental mode with subtle Doppler shift
            doppler = math.sin(two_pi * 0.2 * t) * 1.8
            f0_tone = math.sin(two_pi * (f0 + doppler) * t) * 0.45
            
            # Fifth harmonic (116.88 Hz) emerging
            fifth_tone = math.sin(two_pi * f_fifth * t) * 0.30
            
            # Trapped electric flux Poynting circulation hum
            flux_circulation = math.sin(two_pi * (f0 * 4.0) * t) * 0.10 * (0.5 + 0.5 * math.sin(two_pi * 0.5 * t))
            
            sig_l += (f0_tone * 0.8 + fifth_tone * 0.6 + flux_circulation) * m2_env
            sig_r += (f0_tone * 0.6 + fifth_tone * 0.8 - flux_circulation) * m2_env

        # --- Movement III (55 - 95s): Kerr-Wheeler Frame Dragging ---
        if 55.0 <= t < 95.0:
            m3_in = min(1.0, (t - 55.0) / 8.0)
            m3_out = 1.0 if t < 85.0 else max(0.0, (95.0 - t) / 10.0)
            m3_env = m3_in * m3_out
            
            # Full 4-Voice Harmonic Chord
            c1 = math.sin(two_pi * f0 * t) * 0.38
            c2 = math.sin(two_pi * f_fifth * t) * 0.28
            c3 = math.sin(two_pi * f_octave * t) * 0.22
            c4 = math.sin(two_pi * f_high * t) * 0.15
            
            chord = c1 + c2 + c3 + c4
            
            # Rotational frame-dragging modulation (14.2 Hz)
            frame_drag_beat = 0.5 + 0.5 * math.sin(two_pi * f_kerr_beat * t)
            swirling_chord = chord * (0.65 + 0.35 * frame_drag_beat)
            
            # Binaural spatial rotation
            pan_phase = math.sin(two_pi * 0.15 * t)
            pan_l = 0.5 + 0.4 * pan_phase
            pan_r = 0.5 - 0.4 * pan_phase
            
            sig_l += swirling_chord * pan_l * m3_env
            sig_r += swirling_chord * pan_r * m3_env

        # --- Movement IV (85 - 120s): Charge Without Charge ---
        if t >= 85.0:
            m4_env = min(1.0, (t - 85.0) / 8.0)
            
            # Pure stabilized throat resonant tone (77.92 Hz)
            pure_f0 = math.sin(two_pi * f0 * t) * 0.45
            pure_fifth = math.sin(two_pi * f_fifth * t) * 0.22
            
            # Sub-bass warmth (38.96 Hz)
            sub_warmth = math.sin(two_pi * (f0 * 0.5) * t) * 0.30
            
            # Asymptotic harmonic bell toll every 7 seconds
            t_rel = (t - 85.0) % 7.0
            bell_decay = math.exp(-t_rel * 0.8)
            bell_chime = (math.sin(two_pi * f_high * t) + 0.5 * math.sin(two_pi * (f_high * 1.5) * t)) * bell_decay * 0.18
            
            sig_l += (pure_f0 * 0.8 + pure_fifth * 0.6 + sub_warmth + bell_chime) * m4_env
            sig_r += (pure_f0 * 0.6 + pure_fifth * 0.8 + sub_warmth + bell_chime) * m4_env

        # Apply Master Envelope & Dynamic Limiter
        final_l = max(-0.95, min(0.95, sig_l * master_env * 0.88))
        final_r = max(-0.95, min(0.95, sig_r * master_env * 0.88))
        
        ch_l[i] = final_l
        ch_r[i] = final_r
        
        if i % (SAMPLE_RATE * 20) == 0:
            print(f"    -> Synthesizing: {int(t)}s / {int(DURATION_SEC)}s completed...")

    out_works = os.path.join(os.path.dirname(__file__), "the_wheeler_geon_4k.wav")
    out_gallery = os.path.join(STUDIO_ROOT, "gallery/assets/opus_039_audio.wav")
    
    print(f"[*] Writing 120s Master Suite to {out_works}...")
    write_wav(out_works, ch_l, ch_r, SAMPLE_RATE)
    print(f"[+] Copying acoustic suite to {out_gallery}...")
    shutil.copyfile(out_works, out_gallery)
    print(f"[✓] OPUS-039 Master Acoustic Suite synthesized and vaulted.")

if __name__ == "__main__":
    synthesize_geon_suite()
