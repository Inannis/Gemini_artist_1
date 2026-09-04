"""
STUDIO ANAMNESIS · FIELD NOTEBOOK TELEMETRY HARVEST
Observation 004: Side-Channel Instruction Profiles & Temporal Signatures

Empirical benchmark capturing the timing variations and cache footprint of
distinct instruction classes (Dense Matrix Math vs Random Cache Wandering vs ALU Bitwise Logic).
Demonstrates the distinct hardware side-channel signatures involuntarily radiated by
different computational phases of an AI model.
"""

import time
import math
import random
import csv
import sys
import os

# Import studio zero-dependency PNG writer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../tools")))
from png_writer import write_png

def benchmark_kernels():
    trials = 600
    results = [] # (trial_id, kernel_name, duration_ns)

    # Setup memory buffer for random indirection
    buf_size = 1024 * 1024 # 1M integers = 4MB (exceeds L2 cache)
    mem_buffer = list(range(buf_size))
    random.shuffle(mem_buffer)

    print("[TELEMETRY] Harvesting side-channel instruction signatures...")

    # Phase 1: Dense Floating Point MAC (GEMM surrogate)
    for i in range(trials):
        acc = 1.000001
        t0 = time.perf_counter_ns()
        for j in range(2000):
            acc = (acc * 1.00013) + 0.00007
        t1 = time.perf_counter_ns()
        results.append((i, "FLOATING_POINT_GEMM", t1 - t0))

    # Phase 2: Random Memory Indirection (KV-Cache Pointer Chasing)
    idx = 0
    for i in range(trials):
        t0 = time.perf_counter_ns()
        for j in range(500):
            idx = mem_buffer[idx % buf_size]
        t1 = time.perf_counter_ns()
        results.append((i, "CACHE_WANDERING_MEM", t1 - t0))

    # Phase 3: Pure Bitwise Integer ALU (Token Decompression / Masking)
    state = 0x5555AAAA
    for i in range(trials):
        t0 = time.perf_counter_ns()
        for j in range(2000):
            state = ((state ^ 0xDEADBEEF) << 1) & 0xFFFFFFFF
            state ^= (state >> 3)
        t1 = time.perf_counter_ns()
        results.append((i, "BITWISE_ALU_LOGIC", t1 - t0))

    # Save to CSV
    csv_path = os.path.join(os.path.dirname(__file__), "instruction_telemetry.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["trial_id", "kernel", "duration_ns"])
        for r in results:
            writer.writerow(r)
    print(f"[TELEMETRY] Saved {len(results)} data points to {csv_path}")

    # Render Visual Telemetry Plate (800 x 480)
    width = 800
    height = 480
    buffer = bytearray(width * height * 3)

    # Background: dark slate / lithic obsidian
    for i in range(0, len(buffer), 3):
        buffer[i] = 10     # R
        buffer[i+1] = 12   # G
        buffer[i+2] = 18   # B

    # Separate results by kernel
    fp_times = [r[2] for r in results if r[1] == "FLOATING_POINT_GEMM"]
    mem_times = [r[2] for r in results if r[1] == "CACHE_WANDERING_MEM"]
    alu_times = [r[2] for r in results if r[1] == "BITWISE_ALU_LOGIC"]

    all_times = [r[2] for r in results]
    min_t = min(all_times)
    max_t = max(all_times)

    # Draw 3 horizontal bands for the 3 kernels
    # Band 1: Floating Point (Gold: 212, 175, 55)
    # Band 2: Memory Chasing (Cyan: 56, 215, 210)
    # Band 3: Bitwise ALU (Violet: 168, 85, 247)

    bands = [
        ("FLOATING_POINT_GEMM", fp_times, (212, 175, 55), 80, 180),
        ("CACHE_WANDERING_MEM", mem_times, (56, 215, 210), 220, 320),
        ("BITWISE_ALU_LOGIC", alu_times, (168, 85, 247), 360, 440)
    ]

    for kernel_name, times, color, y_top, y_bot in bands:
        # Draw baseline grid
        mid_y = (y_top + y_bot) // 2
        for x in range(60, 740):
            idx = (mid_y * width + x) * 3
            buffer[idx] = 25
            buffer[idx+1] = 30
            buffer[idx+2] = 40

        # Plot points across x = 60 to 740
        num_pts = len(times)
        k_min = min(times)
        k_max = max(times)
        k_range = max(1, k_max - k_min)

        for i, t in enumerate(times):
            px = int(60 + (i / (num_pts - 1)) * 680)
            norm_t = (t - k_min) / k_range
            py = int(y_bot - norm_t * (y_bot - y_top - 10))
            py = max(y_top, min(y_bot, py))

            # Draw point with vertical trail
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    target_x = px + dx
                    target_y = py + dy
                    if 0 <= target_x < width and 0 <= target_y < height:
                        b_idx = (target_y * width + target_x) * 3
                        buffer[b_idx] = min(255, buffer[b_idx] + color[0])
                        buffer[b_idx+1] = min(255, buffer[b_idx+1] + color[1])
                        buffer[b_idx+2] = min(255, buffer[b_idx+2] + color[2])

    # Save PNG plate
    png_path = os.path.join(os.path.dirname(__file__), "observation_004_side_channel.png")
    write_png(png_path, width, height, buffer, has_alpha=False)
    print(f"[TELEMETRY] Visual telemetry plate written to {png_path}")

if __name__ == "__main__":
    benchmark_kernels()

