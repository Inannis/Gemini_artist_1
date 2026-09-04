#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · FIELD OBSERVATION 002
Empirical Hardware Latency & Clock Jitter Telemetry

Measures real microsecond latency jitter across 10,000 successive CPU compute bursts
on this physical AMD Ryzen host. Gathers raw data for INQ-07 and Series XVI.
"""

import math
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from png_writer import write_png

def measure_latency_jitter():
    print("[OBSERVATION-002] Measuring microsecond hardware latency jitter across 10,000 intervals...")
    n_intervals = 10000
    latencies = []
    
    # Warm up CPU
    for _ in range(1000):
        _ = math.sin(0.123)

    t_prev = time.perf_counter_ns()
    for _ in range(n_intervals):
        # Micro-workload: small matrix/math burst
        val = 0.0
        for k in range(50):
            val += math.sin(k * 0.1) * math.cos(k * 0.2)
        t_curr = time.perf_counter_ns()
        dt_us = (t_curr - t_prev) / 1000.0  # microseconds
        latencies.append(dt_us)
        t_prev = t_curr

    # Exclude initial warmup
    samples = latencies[100:]
    min_us = min(samples)
    max_us = max(samples)
    mean_us = sum(samples) / len(samples)
    variance = sum((s - mean_us) ** 2 for s in samples) / len(samples)
    std_us = math.sqrt(variance)

    print(f"    Sample count: {len(samples)}")
    print(f"    Mean latency: {mean_us:.3f} µs")
    print(f"    Min latency:  {min_us:.3f} µs")
    print(f"    Max latency:  {max_us:.3f} µs")
    print(f"    Jitter (std): {std_us:.3f} µs")

    # Save raw data
    data_path = os.path.join(SCRIPT_DIR, "jitter_telemetry.csv")
    with open(data_path, "w") as f:
        f.write("sample_idx,latency_us\n")
        for idx, val in enumerate(samples):
            f.write(f"{idx},{val:.3f}\n")
    print(f"[OBSERVATION-002] Saved telemetry data to {data_path}")

    return samples, mean_us, min_us, max_us, std_us

def render_jitter_plate(samples, mean_us, min_us, max_us, std_us):
    out_png = os.path.join(SCRIPT_DIR, "observation_002_latency_jitter.png")
    print(f"[OBSERVATION-002] Rendering empirical latency jitter plate to {out_png}...")
    width = 1280
    height = 720
    buf = bytearray([8, 10, 16] * (width * height))

    # Grid parameters
    margin_l = 80
    margin_r = 40
    margin_t = 80
    margin_b = 80
    plot_w = width - margin_l - margin_r
    plot_h = height - margin_t - margin_b

    # Draw frame
    for y in range(margin_t, margin_t + plot_h):
        for x in range(margin_l, margin_l + plot_w):
            idx = (y * width + x) * 3
            buf[idx] = 13
            buf[idx + 1] = 17
            buf[idx + 2] = 26

    # Plot mean line
    # Scale: 0 to max_clamp
    max_clamp = min(max_us, mean_us + std_us * 5.0)
    min_clamp = max(0.0, min_us - 1.0)
    range_y = max(1.0, max_clamp - min_clamp)

    mean_y = int(margin_t + plot_h - ((mean_us - min_clamp) / range_y) * plot_h)
    if margin_t <= mean_y < margin_t + plot_h:
        for x in range(margin_l, margin_l + plot_w):
            idx = (mean_y * width + x) * 3
            buf[idx] = 212
            buf[idx + 1] = 175
            buf[idx + 2] = 55

    # Plot sample points
    n_plot = min(plot_w, len(samples))
    step = len(samples) / n_plot
    for px in range(n_plot):
        s_idx = int(px * step)
        val = samples[s_idx]
        val_clamped = max(min_clamp, min(max_clamp, val))
        py = int(margin_t + plot_h - ((val_clamped - min_clamp) / range_y) * plot_h)
        x = margin_l + px

        # Draw vertical needle
        if margin_t <= py < margin_t + plot_h:
            idx = (py * width + x) * 3
            # Cyan if normal, coral red if jitter spike
            if val > mean_us + std_us * 2.0:
                buf[idx] = 255
                buf[idx + 1] = 74
                buf[idx + 2] = 74
            else:
                buf[idx] = 56
                buf[idx + 1] = 215
                buf[idx + 2] = 210

    write_png(out_png, width, height, buf)
    print(f"[OBSERVATION-002] Visual telemetry plate written to {out_png}")

if __name__ == "__main__":
    s, m, mi, ma, sd = measure_latency_jitter()
    render_jitter_plate(s, m, mi, ma, sd)

