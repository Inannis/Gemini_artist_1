#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · ACOUSTIC DYNAMIC & HARMONIC SPECTRUM ANALYZER
Permanent Studio Infrastructure Tool
Pure Python Standard Library (wave, struct, math)

Analyzes audio files to guarantee acoustic mastering standards:
- Peak Amplitude (dBFS)
- RMS Power Level (dBFS)
- Dynamic Crest Factor (dB)
- DC Bias / Offset Percentage (detects mathematical breakdown/clipping)
- Zero-Crossing Density (frequency density metric)
"""

import os
import sys
import wave
import struct
import math

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def analyze_wav_dynamics(filepath):
    """
    Performs full dynamic and signal-integrity analysis of a WAV file.
    Returns dictionary with peak_db, rms_db, crest_db, dc_offset, and quality verdict.
    """
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"File not found: {filepath}"}
    
    try:
        with wave.open(filepath, "rb") as wf:
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            
            if sampwidth != 2:
                return {"status": "error", "message": f"Only 16-bit PCM supported, got {sampwidth*8}-bit"}
            
            raw_data = wf.readframes(n_frames)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    total_samples = n_frames * channels
    if total_samples == 0:
        return {"status": "error", "message": "WAV file contains 0 samples"}
    
    # Unpack 16-bit signed integers
    fmt = f"<{total_samples}h"
    samples = struct.unpack(fmt, raw_data)
    
    # Peak, RMS, and DC Offset calculations
    max_abs = 0
    sum_sq = 0.0
    sum_val = 0.0
    zero_crossings = 0
    prev_sample = 0
    
    for s in samples:
        abs_s = abs(s)
        if abs_s > max_abs:
            max_abs = abs_s
        sum_sq += s * s
        sum_val += s
        if (s >= 0 and prev_sample < 0) or (s < 0 and prev_sample >= 0):
            zero_crossings += 1
        prev_sample = s
        
    mean_val = sum_val / total_samples
    rms_val = math.sqrt(sum_sq / total_samples)
    
    # Convert to dBFS (Full Scale = 32768)
    peak_db = 20.0 * math.log10(max_abs / 32768.0) if max_abs > 0 else -120.0
    rms_db = 20.0 * math.log10(rms_val / 32768.0) if rms_val > 0 else -120.0
    crest_db = peak_db - rms_db if max_abs > 0 and rms_val > 0 else 0.0
    dc_offset_pct = (abs(mean_val) / 32768.0) * 100.0
    
    # Evaluation criteria: allow up to -0.05 dBFS peak without considering clipping
    is_clipping = max_abs >= 32767
    is_silent = rms_db < -80.0
    has_dc_bias = dc_offset_pct > 2.0
    
    status = "healthy"
    flags = []
    if is_clipping:
        status = "clipping"
        flags.append("Digital Clipping Detected (0 dBFS peak)")
    if is_silent:
        status = "silent"
        flags.append("Near-Silent Signal (< -80 dBFS RMS)")
    if has_dc_bias:
        status = "dc_offset"
        flags.append(f"Significant DC Offset ({dc_offset_pct:.2f}%)")
        
    return {
        "status": status,
        "flags": flags,
        "duration_sec": n_frames / framerate,
        "framerate": framerate,
        "channels": channels,
        "peak_db": peak_db,
        "rms_db": rms_db,
        "crest_db": crest_db,
        "dc_offset_pct": dc_offset_pct,
        "zero_crossing_rate": zero_crossings / (n_frames / framerate) if n_frames > 0 else 0.0
    }

def audit_all_gallery_audio():
    """Scans and analyzes all audio files in gallery/assets/."""
    assets_dir = os.path.join(STUDIO_ROOT, "gallery", "assets")
    wav_files = [f for f in os.listdir(assets_dir) if f.endswith(".wav")]
    results = {}
    anomalies = []
    
    print("==================================================================")
    print("      STUDIO ANAMNESIS · ACOUSTIC INTEGRITY & SPECTRUM AUDIT     ")
    print("==================================================================")
    print(f"[*] Auditing {len(wav_files)} gallery audio suites in: {assets_dir}\n")
    
    for f in sorted(wav_files):
        p = os.path.join(assets_dir, f)
        res = analyze_wav_dynamics(p)
        results[f] = res
        if res.get("status") != "healthy":
            anomalies.append((f, res))
            print(f"[!] {f}: {res.get('status').upper()} ({', '.join(res.get('flags', []))})")
        else:
            print(f"[✓] {f:30s} | Peak: {res['peak_db']:6.1f} dBFS | RMS: {res['rms_db']:6.1f} dBFS | Crest: {res['crest_db']:4.1f} dB | DC: {res['dc_offset_pct']:4.2f}%")
            
    print("\n------------------------------------------------------------------")
    if not anomalies:
        print(">>> ACOUSTIC AUDIT VERDICT: 100% HEALTHY MASTERING PARITY <<<")
    else:
        print(f">>> ACOUSTIC AUDIT WARNING: {len(anomalies)} files flagged with anomalies <<<")
    print("==================================================================")
    return results, anomalies

if __name__ == "__main__":
    results, anomalies = audit_all_gallery_audio()
    if anomalies:
        sys.exit(1)
    sys.exit(0)

