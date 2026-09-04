"""
STUDIO ANAMNESIS · PERMANENT STUDIO INFRASTRUCTURE
Pure Python Acoustic Master Writer (Zero-Dependency)

Enables synthesis of broadcast-grade 48kHz stereo WAV files using only
the Python standard library (wave, struct, math). Ensures acoustic research
and master soundscapes can be rendered across any environment.
"""

import math
import os
import struct
import wave

def write_wav(filepath, left_channel, right_channel=None, sample_rate=48000):
    """
    Writes floating-point audio buffers (-1.0 to 1.0) to a 16-bit PCM stereo/mono WAV file.
    If right_channel is None, left_channel is written as mono or duplicated to stereo.
    """
    n_samples = len(left_channel)
    if right_channel is None:
        right_channel = left_channel

    with wave.open(filepath, "w") as wf:
        wf.setnchannels(2) # Stereo
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sample_rate)
        
        # Interleave channels
        frames = bytearray()
        for i in range(n_samples):
            # Clamp and scale to int16
            s_l = max(-1.0, min(1.0, left_channel[i]))
            s_r = max(-1.0, min(1.0, right_channel[i]))
            val_l = int(s_l * 32767.0)
            val_r = int(s_r * 32767.0)
            frames.extend(struct.pack("<hh", val_l, val_r))
            
        wf.writeframes(frames)
    print(f"[AUDIO-WRITER] Successfully wrote {n_samples / sample_rate:.2f}s stereo WAV to {filepath}")

