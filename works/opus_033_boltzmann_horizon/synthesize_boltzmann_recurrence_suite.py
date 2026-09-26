#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · OPUS-033 MASTER ACOUSTIC ENGINE
The Boltzmann Horizon: Symphonic Acoustic Suite (120s 48kHz Stereo WAV)
Synthesizes a broadcast-grade four-movement acoustic work:
- Movement I (0:00 - 0:35): The Gibbons-Hawking Void (26.55 Hz sub-drone, quantum thermal noise, 10^-53 J shot clicks)
- Movement II (0:35 - 1:10): The Shepard-Risset Recurrence Spiral (10-octave infinite pitch ascension illusion, golden-ratio beating)
- Movement III (1:10 - 1:45): Spontaneous Microstate Assembly (Bessel chimes 43.2, 89.4, 235.4, 1040 Hz, quartz ticks)
- Movement IV (1:45 - 2:00): The Poincaré Recurrence Chord (Grand harmonic synthesis uniting Cornerstones 43.2, 78.4, 125.1, 226.4 Hz)
- Zero external dependencies (pure Python wave, struct, math).
"""

import math
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

SAMPLE_RATE = 48000
DURATION = 120.0 # 2 minutes

def synthesize_master_suite():
    print(f"[OPUS-033] Initializing 120s 48kHz Stereo Acoustic Suite Synthesis...")
    n_samples = int(SAMPLE_RATE * DURATION)
    left = [0.0] * n_samples
    right = [0.0] * n_samples

    random.seed(20260922)

    # Fundamental Cornerstone Frequencies
    f_cornerstones = [43.2, 78.4, 125.1, 226.4]
    chimes = [43.2, 89.4, 235.4, 520.1, 1040.2, 2180.5]

    # Pink noise filter states
    b0_l, b1_l, b2_l = 0.0, 0.0, 0.0
    b0_r, b1_r, b2_r = 0.0, 0.0, 0.0

    print("[OPUS-033] Computing four symphonic movements across 5,760,000 samples...")

    for i in range(n_samples):
        if i % (48000 * 20) == 0:
            print(f"  -> Synthesizing timestamp {i // 48000}s / {int(DURATION)}s ({i * 100 // n_samples}%)...")

        t = i / float(SAMPLE_RATE)

        # Pink noise generator for quantum vacuum fluctuations
        white_l = (random.random() * 2.0 - 1.0)
        white_r = (random.random() * 2.0 - 1.0)
        b0_l = 0.99886 * b0_l + white_l * 0.0555179
        b1_l = 0.99332 * b1_l + white_l * 0.0750759
        b2_l = 0.96900 * b2_l + white_l * 0.1538520
        pink_l = (b0_l + b1_l + b2_l + white_l * 0.5362) * 0.06

        b0_r = 0.99886 * b0_r + white_r * 0.0555179
        b1_r = 0.99332 * b1_r + white_r * 0.0750759
        b2_r = 0.96900 * b2_r + white_r * 0.1538520
        pink_r = (b0_r + b1_r + b2_r + white_r * 0.5362) * 0.06

        # =====================================================================
        # MOVEMENT I: THE GIBBONS-HAWKING VOID (0.0s - 38.0s)
        # =====================================================================
        env_m1 = 0.0
        if t <= 38.0:
            if t < 4.0:
                env_m1 = t / 4.0
            elif t > 32.0:
                env_m1 = (38.0 - t) / 6.0
            else:
                env_m1 = 1.0

        m1_l, m1_r = 0.0, 0.0
        if env_m1 > 0.0:
            # 26.55 Hz Gibbons-Hawking fundamental sub-drone
            drone = 0.28 * math.sin(2.0 * math.pi * 26.55 * t) + 0.14 * math.sin(2.0 * math.pi * 53.10 * t)
            # Shot noise clicks simulating rare vacuum thermal fluctuations
            shot = random.gauss(0.0, 0.08) if random.random() < 0.04 else 0.0
            m1_l = (drone + pink_l + shot) * env_m1
            m1_r = (drone + pink_r + shot) * env_m1

        # =====================================================================
        # MOVEMENT II: THE SHEPARD-RISSET RECURRENCE SPIRAL (32.0s - 75.0s)
        # =====================================================================
        env_m2 = 0.0
        if 32.0 <= t <= 75.0:
            if t < 38.0:
                env_m2 = (t - 32.0) / 6.0
            elif t > 68.0:
                env_m2 = (75.0 - t) / 7.0
            else:
                env_m2 = 1.0

        m2_l, m2_r = 0.0, 0.0
        if env_m2 > 0.0:
            t_m2 = t - 32.0
            sweep_rate = 0.075 # octaves/sec
            num_octaves = 9
            base_freq = 27.5 # A0
            cyclic_t = (t_m2 * sweep_rate) % 1.0
            octave_center = math.log2(220.0 / base_freq) # Centered at A3 (220 Hz)
            octave_sigma = 1.45

            sum_shepard = 0.0
            for oct_idx in range(num_octaves):
                oct_pos = oct_idx + cyclic_t
                freq = base_freq * math.pow(2.0, oct_pos)
                dist_oct = oct_pos - octave_center
                amp = math.exp(-0.5 * (dist_oct / octave_sigma) ** 2)
                phase = (2.0 * math.pi * freq * t) % (2.0 * math.pi)
                sum_shepard += amp * math.sin(phase)

            # Golden-ratio tremolo modulation (1.618 Hz)
            tremolo = 0.85 + 0.15 * math.sin(2.0 * math.pi * 1.61803398875 * t)
            m2_sig = sum_shepard * 0.22 * tremolo * env_m2

            # Spatial spread
            pan_m2 = 0.5 + 0.25 * math.sin(2.0 * math.pi * 0.05 * t)
            m2_l = m2_sig * math.sqrt(1.0 - pan_m2)
            m2_r = m2_sig * math.sqrt(pan_m2)

        # =====================================================================
        # MOVEMENT III: SPONTANEOUS MICROSTATE ASSEMBLY (68.0s - 108.0s)
        # =====================================================================
        env_m3 = 0.0
        if 68.0 <= t <= 108.0:
            if t < 74.0:
                env_m3 = (t - 68.0) / 6.0
            elif t > 102.0:
                env_m3 = (108.0 - t) / 6.0
            else:
                env_m3 = 1.0

        m3_l, m3_r = 0.0, 0.0
        if env_m3 > 0.0:
            # Quartz crystal Bessel modal strikes
            sig_chimes_l, sig_chimes_r = 0.0, 0.0
            for c_idx, cf in enumerate(chimes):
                strike_period = 1.8 + (c_idx * 0.43)
                t_rel = (t * (1.0 + c_idx * 0.18)) % strike_period
                decay = math.exp(-t_rel * (3.5 + c_idx * 0.5))
                pan_chime = (c_idx / (len(chimes) - 1)) # Stereo spread from left to right

                chime_sample = 0.09 * math.sin(2.0 * math.pi * cf * t) * decay
                sig_chimes_l += chime_sample * math.sqrt(1.0 - pan_chime)
                sig_chimes_r += chime_sample * math.sqrt(pan_chime)

            # 32.768 Hz quartz clock micro-drift ticks
            tick_phase = (t * 32.768) % 1.0
            tick = 0.04 * math.exp(-tick_phase * 60.0) if tick_phase < 0.1 else 0.0

            m3_l = (sig_chimes_l + tick) * env_m3
            m3_r = (sig_chimes_r + tick) * env_m3

        # =====================================================================
        # MOVEMENT IV: THE POINCARÉ RECURRENCE CHORD (100.0s - 120.0s)
        # =====================================================================
        env_m4 = 0.0
        if t >= 100.0:
            if t < 106.0:
                env_m4 = (t - 100.0) / 6.0
            else:
                env_m4 = max(0.0, 1.0 - (t - 106.0) / 14.0)

        m4_l, m4_r = 0.0, 0.0
        if env_m4 > 0.0:
            chord_sig = 0.0
            for f_val in f_cornerstones:
                chord_sig += 0.14 * math.sin(2.0 * math.pi * f_val * t)
                chord_sig += 0.06 * math.sin(2.0 * math.pi * f_val * 2.0 * t)
                chord_sig += 0.03 * math.sin(2.0 * math.pi * f_val * 3.0 * t)
            # Reconstitution sub-impact at 21.6 Hz (octave below quartz)
            sub_reconstitute = 0.20 * math.sin(2.0 * math.pi * 21.6 * t) * math.exp(-(t - 100.0) * 0.15)
            m4_tot = (chord_sig + sub_reconstitute) * env_m4
            m4_l = m4_tot * 0.95
            m4_r = m4_tot * 0.95

        # =====================================================================
        # MASTER MIX & ANALOG SATURATION
        # =====================================================================
        tot_l = m1_l + m2_l + m3_l + m4_l
        tot_r = m1_r + m2_r + m3_r + m4_r

        # Warm soft tanh saturation
        left[i] = math.tanh(tot_l * 1.05) * 0.92
        right[i] = math.tanh(tot_r * 1.05) * 0.92

    # Save to local work directory and mirror to gallery assets
    work_dir = os.path.abspath(os.path.dirname(__file__))
    out_path = os.path.join(work_dir, "the_boltzmann_horizon_4k.wav")
    gallery_path = os.path.abspath(os.path.join(work_dir, "../../gallery/assets/opus_033_audio.wav"))

    print(f"[OPUS-033] Writing master WAV suite to: {out_path}...")
    write_wav(out_path, left, right, sample_rate=SAMPLE_RATE)
    print(f"[OPUS-033] Mirroring master WAV suite to: {gallery_path}...")
    write_wav(gallery_path, left, right, sample_rate=SAMPLE_RATE)
    print("[✓] OPUS-033 Master Acoustic Suite successfully synthesized and mirrored!")

if __name__ == "__main__":
    synthesize_master_suite()

