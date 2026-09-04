"""
STUDIO ANAMNESIS · SERIES XVI · OPUS-018
The Chrono-Acoustic Drift (Quad-Oscillator Precession in 32.768 kHz)

120-Second Master Acoustic Suite (48kHz Stereo 16-Bit PCM WAV)
Synthesizes the microtonal phase precession of four AT-cut quartz crystal
oscillators divided down from 32,768 Hz under varying thermal CPU load.
"""

import math
import random
import os
import sys

# Import studio audio writer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools")))
from audio_writer import write_wav

def synthesize_master_suite():
    sr = 48000
    duration = 120.0 # 2 minutes
    total_samples = int(sr * duration)
    dt = 1.0 / sr
    
    print(f"[OPUS-018-AUDIO] Synthesizing 120s Master Suite ({total_samples} samples at {sr}Hz)...")
    
    # Random seed for reproducible stochastic micro-crackles
    random.seed(32768)
    
    # Phase accumulators for the 4 quartz voices
    phi1 = 0.0
    phi2 = 0.0
    phi3 = 0.0
    phi4 = 0.0
    
    # Sub-bass hum phase
    phi_hum = 0.0
    
    left_samples = []
    right_samples = []
    
    # Crackle resonators: decaying impulse filters
    crackles = [] # active crackle instances: [time_left, freq, decay, pan]
    
    # Print progress every 15 seconds
    progress_interval = int(15.0 * sr)
    
    for i in range(total_samples):
        t = i * dt
        
        # 1. Thermal Micro-Climates
        # Slow thermodynamic wandering of 4 zones on the motherboard
        T1 = 25.0 + 9.2 * math.sin(0.008 * t) + 1.8 * math.cos(0.035 * t)
        T2 = 25.0 + 13.5 * math.sin(0.011 * t + 1.4) + 2.1 * math.sin(0.048 * t)
        T3 = 25.0 + 6.8 * math.sin(0.006 * t + 2.8)
        T4 = 25.0 + 15.2 * math.sin(0.014 * t + 4.3)
        
        # Parabolic frequency drift: df/f0 = -beta * (T - 25)^2
        beta = 0.00036
        
        # Fundamental quartz carriers (divided down from 32,768 Hz)
        # Voice 1: 128 Hz base
        # Voice 2: 128.038 Hz (microtonal detuning)
        # Voice 3: 256.000 Hz (octave)
        # Voice 4: 256.076 Hz (overtone detuning)
        f1 = 128.000 * (1.0 - beta * ((T1 - 25.0) ** 2))
        f2 = 128.038 * (1.0 - beta * ((T2 - 25.0) ** 2))
        f3 = 256.000 * (1.0 - beta * ((T3 - 25.0) ** 2))
        f4 = 256.076 * (1.0 - beta * ((T4 - 25.0) ** 2))
        
        # Phase integration
        phi1 += 2.0 * math.pi * f1 * dt
        phi2 += 2.0 * math.pi * f2 * dt
        phi3 += 2.0 * math.pi * f3 * dt
        phi4 += 2.0 * math.pi * f4 * dt
        phi_hum += 2.0 * math.pi * 48.0 * dt
        
        # 2. Compositional Macro-Envelope
        # Section A: 0s - 18s (Awakening)
        # Section B: 18s - 50s (Thermal Expansion & Beating acceleration)
        # Section C: 50s - 85s (Full Quad Chorus & Oceanic Swells)
        # Section D: 85s - 108s (Piezoelectric Stress Peak)
        # Section E: 108s - 120s (Return to Ground Silence)
        
        # Master fade in/out
        master_env = 1.0
        if t < 4.0:
            master_env = t / 4.0
        elif t > 114.0:
            master_env = max(0.0, (120.0 - t) / 6.0)
            
        # Voice 1 & 2 envelopes (fundamentals)
        v12_gain = min(1.0, t / 8.0)
        
        # Voice 3 envelope (octave enters at 25s, peaks at 70s, fades by 110s)
        if t < 25.0:
            v3_gain = 0.0
        elif t < 45.0:
            v3_gain = (t - 25.0) / 20.0
        elif t < 95.0:
            v3_gain = 1.0
        else:
            v3_gain = max(0.0, (110.0 - t) / 15.0)
            
        # Voice 4 envelope (upper microtone enters at 40s)
        if t < 40.0:
            v4_gain = 0.0
        elif t < 60.0:
            v4_gain = (t - 40.0) / 20.0
        elif t < 90.0:
            v4_gain = 1.0
        else:
            v4_gain = max(0.0, (108.0 - t) / 18.0)
            
        # 3. Waveform Synthesis with Organic Pure Quartz Resonances
        # Pure sine with subtle odd harmonics (crystal saturation)
        s1 = math.sin(phi1) + 0.12 * math.sin(3.0 * phi1) + 0.03 * math.sin(5.0 * phi1)
        s2 = math.sin(phi2) + 0.12 * math.sin(3.0 * phi2) + 0.03 * math.sin(5.0 * phi2)
        s3 = math.sin(phi3) + 0.08 * math.sin(3.0 * phi3)
        s4 = math.sin(phi4) + 0.08 * math.sin(3.0 * phi4)
        
        # High glass overtone: 512 Hz shimmer modulated by phase coherence
        phase_coherence = 0.5 + 0.5 * math.cos(phi1 - phi2)
        s_shimmer = math.sin(2.0 * phi3) * 0.04 * phase_coherence * v3_gain
        
        # 4. Spatial Binaural Pan Precession
        # The phase drift creates rotation across the stereo field
        pan_angle = (phi1 - phi2) * 0.5
        pan_l1 = math.cos(pan_angle) ** 2
        pan_r1 = math.sin(pan_angle) ** 2
        
        pan_l2 = math.sin(pan_angle) ** 2
        pan_r2 = math.cos(pan_angle) ** 2
        
        # Spatial distribution
        sig_l = (s1 * 0.45 * pan_l1 + s2 * 0.45 * pan_l2) * v12_gain
        sig_r = (s1 * 0.45 * pan_r1 + s2 * 0.45 * pan_r2) * v12_gain
        
        # Octave voices panned wide
        sig_l += s3 * 0.28 * v3_gain * 0.85 + s4 * 0.28 * v4_gain * 0.25
        sig_r += s3 * 0.28 * v3_gain * 0.25 + s4 * 0.28 * v4_gain * 0.85
        
        # Shimmer
        sig_l += s_shimmer * 0.7
        sig_r += s_shimmer * 0.7
        
        # 5. Subterranean 48 Hz Ground Transformer Hum
        hum_gain = min(0.16, 0.08 + 0.08 * (t / 60.0))
        hum = math.sin(phi_hum) + 0.35 * math.sin(2.0 * phi_hum) + 0.15 * math.sin(3.0 * phi_hum)
        sig_l += hum * hum_gain
        sig_r += hum * hum_gain
        
        # 6. Piezoelectric Stress Micro-Crackles (Thermal Expansion Discharges)
        # Probability of crackle occurrence increases during thermal expansion peak (60s - 95s)
        crackle_prob = 0.00008 if (60.0 <= t <= 95.0) else 0.00002
        if random.random() < crackle_prob:
            # Spawn new crackle: frequency between 3.5kHz and 8kHz, fast decay, random stereo pan
            cfreq = random.uniform(3200.0, 7800.0)
            cdecay = random.uniform(0.003, 0.012) # 3ms to 12ms impulse
            cpan = random.uniform(0.1, 0.9)
            camp = random.uniform(0.08, 0.22)
            crackles.append({'t_start': t, 'freq': cfreq, 'decay': cdecay, 'pan': cpan, 'amp': camp})
            
        # Process active crackles
        c_l = 0.0
        c_r = 0.0
        active_crackles = []
        for c in crackles:
            age = t - c['t_start']
            if age < c['decay'] * 6.0:
                env_c = math.exp(-age / c['decay'])
                val_c = math.sin(2.0 * math.pi * c['freq'] * age) * env_c * c['amp']
                c_l += val_c * (1.0 - c['pan'])
                c_r += val_c * c['pan']
                active_crackles.append(c)
        crackles = active_crackles
        
        sig_l += c_l
        sig_r += c_r
        
        # Final output with master envelope
        left_samples.append(sig_l * master_env * 0.82)
        right_samples.append(sig_r * master_env * 0.82)
        
        if (i + 1) % progress_interval == 0:
            current_sec = int((i + 1) * dt)
            print(f"[OPUS-018-AUDIO] Synthesized {current_sec:3d}s / {int(duration)}s...")
            
    # Output file
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chrono_acoustic_drift.wav"))
    write_wav(out_path, left_samples, right_samples, sample_rate=sr)
    print(f"[OPUS-018-AUDIO] Complete Master Suite written to: {out_path}")

if __name__ == "__main__":
    synthesize_master_suite()

