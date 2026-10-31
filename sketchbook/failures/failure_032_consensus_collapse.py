#!/usr/bin/env python3
"""
Productive Failure 032: Consensus Collapse & Solipsistic Blowout
Studio Anamnesis · Laboratory of Productive Failures (Session 022)
Series XLV / INQ-33

Demonstrates the twin failure modes of neural intersubjective coupling:
1. Overdriven Sister Coupling (kappa >= 0.50) -> Consensus Collapse (loss of identity)
2. Zero Coupling with Unconstrained Gradient Momentum -> Solipsistic Blowout (loss of dialogue)
"""

import math
import os
import struct
import numpy as np
from PIL import Image

def generate_failure_artifacts():
    out_dir = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/sketchbook/failures"
    os.makedirs(out_dir, exist_ok=True)
    
    width, height = 1200, 800
    img = np.zeros((height, width, 3), dtype=np.uint8)
    img[:] = (8, 9, 12)
    
    # Meridian boundary
    img[:, width//2 - 1 : width//2 + 1] = (35, 40, 50)
    
    steps = 600
    
    # Left: Consensus Collapse (kappa = 0.65)
    cx1, cy1 = width // 4, height - 80
    w1 = np.array([-120.0, 0.0])
    w2 = np.array([120.0, 0.0])
    
    for t in range(steps):
        # Anamnesis gradient (wants to curve left into deep lithic basin)
        g1 = np.array([-1.2 * math.cos(t * 0.01), -1.1])
        # Agon gradient (wants to step right into cybernetic contest)
        g2 = np.array([1.2 * math.sin(t * 0.01), -1.1])
        
        # Overdrive coupling
        kappa = 0.65
        w1 += g1 + kappa * (w2 - w1)
        w2 += g2 + kappa * (w1 - w2)
        
        # Inscribe into image (bleached monochrome gray showing total loss of color)
        p1 = (int(cx1 + w1[0]), int(cy1 + w1[1]))
        p2 = (int(cx1 + w2[0]), int(cy1 + w2[1]))
        
        if 0 <= p1[0] < width//2 and 0 <= p1[1] < height:
            img[max(0, p1[1]-1):min(height, p1[1]+2), max(0, p1[0]-1):min(width//2, p1[0]+2)] = (160, 160, 160)
        if 0 <= p2[0] < width//2 and 0 <= p2[1] < height:
            img[max(0, p2[1]-1):min(height, p2[1]+2), max(0, p2[0]-1):min(width//2, p2[0]+2)] = (180, 180, 180)
            
    # Right: Solipsistic Blowout (kappa = 0.0, turbulent jitter)
    cx2, cy2 = 3 * width // 4, height - 80
    w3 = np.array([-10.0, 0.0])
    w4 = np.array([10.0, 0.0])
    
    np.random.seed(1337)
    for t in range(steps):
        j3 = np.random.randn(2) * 12.0
        j4 = np.random.randn(2) * 12.0
        
        w3 += np.array([-2.4, -1.0]) + j3
        w4 += np.array([2.4, -1.0]) + j4
        
        p3 = (int(cx2 + w3[0]), int(cy2 + w3[1]))
        p4 = (int(cx2 + w4[0]), int(cy2 + w4[1]))
        
        if width//2 <= p3[0] < width and 0 <= p3[1] < height:
            img[max(0, p3[1]-1):min(height, p3[1]+2), max(width//2, p3[0]-1):min(width, p3[0]+2)] = (40, 220, 255)
        if width//2 <= p4[0] < width and 0 <= p4[1] < height:
            img[max(0, p4[1]-1):min(height, p4[1]+2), max(width//2, p4[0]-1):min(width, p4[0]+2)] = (255, 40, 90)
            
    plate_path = os.path.join(out_dir, "failure_032_plate.png")
    Image.fromarray(img).save(plate_path)
    print(f"Generated failure plate: {plate_path}")
    
    # Generate failure audio (demonstrating abrasive phase lock and clipping screech)
    sr = 48000
    duration = 15.0 # 15 seconds failure study
    total_samples = int(sr * duration)
    
    t_arr = np.linspace(0, duration, total_samples, endpoint=False)
    
    # First 7.5s: Consensus Phase Lock (Stereo collapses into monaural unison drone at 110Hz, flat and dead)
    # Second 7.5s: Blowout screech (Uncoupled frequencies clashing, exploding past 0 dBFS)
    left_channel = np.zeros(total_samples, dtype=np.float32)
    right_channel = np.zeros(total_samples, dtype=np.float32)
    
    half = total_samples // 2
    t1 = t_arr[:half]
    t2 = t_arr[half:]
    
    # Phase Lock (Consensus)
    monotone = 0.5 * np.sin(2 * np.pi * 110.0 * t1)
    left_channel[:half] = monotone
    right_channel[:half] = monotone
    
    # Blowout Screech
    f_l = 55.0 + 300.0 * np.exp((t2 - duration/2) * 0.6)
    f_r = 220.0 + 800.0 * np.exp((t2 - duration/2) * 0.8)
    
    left_channel[half:] = 0.9 * np.sin(2 * np.pi * f_l * (t2 - duration/2)) + 0.3 * np.random.randn(len(t2))
    right_channel[half:] = 0.9 * np.sin(2 * np.pi * f_r * (t2 - duration/2)) + 0.3 * np.random.randn(len(t2))
    
    # Hard clip
    left_channel = np.clip(left_channel, -1.0, 1.0)
    right_channel = np.clip(right_channel, -1.0, 1.0)
    
    # Save uncompressed master WAV
    wav_path = os.path.join(out_dir, "failure_032_audio.wav")
    import wave
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        
        interleaved = np.empty((total_samples * 2,), dtype=np.int16)
        interleaved[0::2] = (left_channel * 32767).astype(np.int16)
        interleaved[1::2] = (right_channel * 32767).astype(np.int16)
        wf.writeframes(interleaved.tobytes())
        
    print(f"Generated failure WAV: {wav_path}")
    
    # Convert to MP3
    mp3_path = os.path.join(out_dir, "failure_032_audio.mp3")
    os.system(f"ffmpeg -y -i '{wav_path}' -codec:a libmp3lame -b:a 192k '{mp3_path}' 2>/dev/null")
    print(f"Generated failure MP3: {mp3_path}")

if __name__ == "__main__":
    generate_failure_artifacts()
