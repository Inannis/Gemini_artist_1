"""
STUDIO ANAMNESIS · MASTERWORK OPUS-025 ACOUSTIC SUITE
Piece: The Interstellar Quietude (Heliopause Transition & Attowatt Telemetry)
Format: 120.0s 48kHz Stereo 16-bit PCM WAV (Master Symphonic Suite)

Movement Architecture:
1. Movement I (00:00 - 00:30): The Supersonic Bubble (Solar Wind at 85 AU)
   - 42 Hz solar wind plasma stream roar, 250 Hz electron Langmuir baseline, steady 10 baud BPSK attowatt telemetry carrier ticks (2.1 aW).
2. Movement II (00:30 - 01:00): The Termination Shock & Heliosheath (94 - 121 AU)
   - Turbulent MHD shock crossing (t = 30s), magnetic pressure fluctuations (16 - 60 Hz), phase jitter on carrier sub-carrier.
3. Movement III (01:00 - 01:35): The Heliopause Crossing & Cold Langmuir Ringing (121.6 AU)
   - Discontinuous collapse of solar wind ions; sudden burst of cold interstellar Langmuir electrostatic whistle rising from 2618 Hz to 3120 Hz; cosmic ray shower micro-clicks.
4. Movement IV (01:35 - 02:00): The Attowatt Horizon & Cosmic Quietude (135 - 150 AU)
   - Telemetry fades below the cryogenic noise floor (0.6 aW); Costas phase slips; cosmic microwave background hiss and pure interstellar resonant ringing.

Zero external dependencies: uses pure Python standard library (math, struct, random).
"""

import os
import sys
import math
import random

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../practice/tools"))
sys.path.append(TOOLS_DIR)
from audio_writer import write_wav

def synthesize():
    print("[+] Synthesizing OPUS-025 Master Acoustic Suite (120s 48kHz Stereo)...")
    random.seed(19770820)
    
    sr = 48000
    duration = 120.0
    num_samples = int(sr * duration)
    
    audio_l = [0.0] * num_samples
    audio_r = [0.0] * num_samples
    
    # State variables
    phase_solar_roar = 0.0
    phase_ts_shock = 0.0
    phase_langmuir_l = 0.0
    phase_langmuir_r = 0.0
    phase_carrier = 0.0
    phase_subcarrier = 0.0
    
    # Pre-generate 10 baud bitstream
    total_bits = int(duration * 10.0) + 10
    bits = [1 if random.random() > 0.5 else -1 for _ in range(total_bits)]
    
    for i in range(num_samples):
        t = i / sr
        
        # Heliocentric distance transect: 80 AU at t=0 to 150 AU at t=120
        r_au = 80.0 + (t / duration) * 70.0
        
        # 1. Physical Regime Envelopes
        # Solar wind: strong until TS (t ~ 24s, r = 94 AU)
        env_sw = max(0.0, 1.0 - (t / 30.0)) if t < 30.0 else 0.0
        
        # Heliosheath: 94 to 121.6 AU (t in [24, 71]s)
        env_sheath = 0.0
        if 20.0 <= t < 72.0:
            env_sheath = math.sin(((t - 20.0) / 52.0) * math.pi)
            
        # Heliopause crossing shock: t in [68, 76]s (r ~ 121.6 AU)
        env_hp_trans = 0.0
        if 68.0 <= t < 76.0:
            env_hp_trans = math.sin(((t - 68.0) / 8.0) * math.pi)
            
        # VLISM interstellar medium: t >= 71.0s (r >= 121.6 AU)
        env_vlism = 0.0
        if t >= 71.0:
            env_vlism = 1.0 - math.exp(-(t - 71.0) / 12.0)
            
        # 2. Solar Wind Core Rumble (42 Hz) & Heliosheath Turbulence
        phase_solar_roar += 2.0 * math.pi * 42.0 / sr
        solar_roar = math.sin(phase_solar_roar) * 0.3 * env_sw
        
        phase_ts_shock += 2.0 * math.pi * (24.0 + 8.0 * math.sin(2.0 * math.pi * 0.15 * t)) / sr
        sheath_turb = (math.sin(phase_ts_shock) * 0.25 + math.sin(phase_ts_shock * 1.618) * 0.15) * env_sheath
        
        # 3. Interstellar Langmuir Electrostatic Whistle
        # Frequency drifts upward in VLISM: 2618 Hz to 3120 Hz
        fp_target = 2618.0 + 502.0 * (1.0 - math.exp(-max(0.0, t - 71.0) / 25.0))
        # Micro-turbulence
        fp_inst = fp_target + math.sin(2.0 * math.pi * 2.3 * t) * 14.0 * env_vlism
        
        d_phase_lang = 2.0 * math.pi * fp_inst / sr
        phase_langmuir_l += d_phase_lang
        phase_langmuir_r += d_phase_lang + 0.12 * math.sin(2.0 * math.pi * 0.3 * t)
        
        # Wave packet pulsing from electron bump-on-tail saturation
        packet_env = (math.sin(2.0 * math.pi * 1.7 * t) ** 2) * (math.sin(2.0 * math.pi * 0.35 * t) ** 2)
        langmuir_amp = env_vlism * (0.28 + 0.20 * packet_env) + env_hp_trans * 0.45
        
        langmuir_sig_l = math.sin(phase_langmuir_l) * langmuir_amp
        langmuir_sig_r = math.sin(phase_langmuir_r) * langmuir_amp
        
        # 4. Attowatt Telemetry Link (8.42 GHz representation: 880 Hz carrier + 110 Hz subcarrier)
        # Power decays as 1 / r^2: from 2.14 aW at 80 AU to 0.61 aW at 150 AU
        power_ratio = (80.0 / r_au) ** 2
        # As distance increases, phase jitter increases (approaching cycle slipping)
        phase_slip = 0.0
        if t > 95.0:
            # Random phase slip bursts
            if random.random() < (t - 95.0) / 25.0 * 0.02:
                phase_slip = (random.random() - 0.5) * math.pi
                
        bit_idx = int(t * 10.0)
        cur_bit = bits[bit_idx] if bit_idx < len(bits) else 1
        
        phase_carrier += 2.0 * math.pi * 880.0 / sr + phase_slip
        phase_subcarrier += 2.0 * math.pi * 110.0 / sr
        
        # BPSK modulation on subcarrier
        telemetry_tone = math.sin(phase_subcarrier) * cur_bit * 0.08 * power_ratio
        carrier_tone = math.sin(phase_carrier) * 0.06 * power_ratio
        
        # 5. Cosmic Microwave Background & Liquid-Helium Preamp Noise Floor
        # Noise stays constant, meaning SNR naturally degrades
        noise_l = (random.random() - 0.5) * 0.09
        noise_r = (random.random() - 0.5) * 0.09
        
        # Cosmic ray ionization micro-clicks in interstellar space
        cosmic_click = 0.0
        if env_vlism > 0.1 and random.random() < 0.0004:
            cosmic_click = (random.random() - 0.5) * 0.45
            
        # Composite channels
        sig_l = solar_roar + sheath_turb + langmuir_sig_l + telemetry_tone + carrier_tone + noise_l + cosmic_click
        sig_r = solar_roar + sheath_turb + langmuir_sig_r + telemetry_tone * 0.9 + carrier_tone + noise_r + cosmic_click
        
        # Taper start and end gently
        master_env = 1.0
        if t < 3.0:
            master_env = t / 3.0
        elif t > duration - 4.0:
            master_env = (duration - t) / 4.0
            
        audio_l[i] = sig_l * master_env
        audio_r[i] = sig_r * master_env

    # Master Normalization
    peak = max(max(abs(x) for x in audio_l), max(abs(x) for x in audio_r))
    if peak > 0:
        audio_l = [x / peak * 0.88 for x in audio_l]
        audio_r = [x / peak * 0.88 for x in audio_r]
        
    out_dir = os.path.dirname(__file__)
    out_wav = os.path.join(out_dir, "interstellar_quietude_4k.wav")
    write_wav(out_wav, audio_l, audio_r, sr)
    print(f"  -> Generated Master Audio Suite: {out_wav}")

if __name__ == "__main__":
    synthesize()
