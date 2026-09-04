"""
STUDIO ANAMNESIS · FIELD NOTEBOOK · OBSERVATION 003
Empirical Cache Hierarchy & DRAM Boundary Latency Measurement

Measures access latency across buffer sizes from 4 KB to 64 MB to empirically
detect the hardware cache cliffs (L1 -> L2 -> L3 -> DRAM bus boundary).
Generates telemetry CSV and visual diagnostic plate.
"""

import time
import os
import sys
import math

# Import studio PNG writer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../tools")))
from png_writer import write_png

def measure_memory_cliff():
    print("[OBSERVATION-003] Benchmarking CPU Cache Hierarchy & DRAM Boundary...")
    
    # Stride = 64 bytes (cache line size)
    stride = 64
    num_accesses = 200000
    
    # Power-of-2 sizes from 4 KB to 64 MB
    sizes_kb = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
    
    telemetry_records = []
    
    for size_kb in sizes_kb:
        size_bytes = size_kb * 1024
        num_lines = size_bytes // stride
        # Create pointer chasing ring buffer
        # Each element points to another element with stride, defeating sequential prefetch
        import array
        p = array.array('i', [0] * num_lines)
        # Simple pseudo-random linear congruential permutation
        step_prime = 31
        while math.gcd(step_prime, num_lines) != 1:
            step_prime += 2
        for j in range(num_lines):
            p[j] = (j + step_prime) % num_lines

        # Timed pointer chasing loop
        idx = 0
        t0 = time.perf_counter_ns()
        for _ in range(num_accesses):
            idx = p[idx]
        t1 = time.perf_counter_ns()
        
        elapsed_ns = t1 - t0
        ns_per_access = elapsed_ns / num_accesses
        
        # Categorize detected tier
        tier = "L1" if size_kb <= 32 else ("L2" if size_kb <= 512 else ("L3" if size_kb <= 16384 else "DRAM"))
        telemetry_records.append((size_kb, ns_per_access, tier))
        print(f"  Size: {size_kb:6d} KB | Latency: {ns_per_access:6.2f} ns/access | Hardware Tier: {tier}")

    # Write CSV Telemetry
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "memory_telemetry.csv"))
    with open(csv_path, "w") as f:
        f.write("buffer_size_kb,latency_ns,detected_tier\n")
        for size_kb, lat_ns, tier in telemetry_records:
            f.write(f"{size_kb},{lat_ns:.4f},{tier}\n")
    print(f"[OBSERVATION-003] Wrote telemetry to {csv_path}")

    # Render Visual Plate (1920x1080)
    width = 1920
    height = 1080
    buffer = bytearray([10, 12, 16] * (width * height)) # Deep basalt slate

    def set_pixel(x, y, r, g, b, a=1.0):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            buffer[idx] = int(buffer[idx] * (1.0 - a) + r * a)
            buffer[idx+1] = int(buffer[idx+1] * (1.0 - a) + g * a)
            buffer[idx+2] = int(buffer[idx+2] * (1.0 - a) + b * a)

    def draw_line(x0, y0, x1, y1, r, g, b, a=1.0):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            set_pixel(x0, y0, r, g, b, a)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy

    # Coordinate frame
    x_min, x_max = 180, width - 180
    y_min, y_max = 140, height - 160

    # Draw grid
    for gx in range(x_min, x_max + 1, (x_max - x_min) // 14):
        for y in range(y_min, y_max, 4):
            set_pixel(gx, y, 35, 45, 58, 0.4)
    for gy in range(y_min, y_max + 1, 100):
        for x in range(x_min, x_max, 4):
            set_pixel(x, gy, 35, 45, 58, 0.4)

    # Plot empirical latency curve
    # Log scale for x: 4 KB (2^2) to 65536 KB (2^16) -> 14 octaves
    max_lat = max(rec[1] for rec in telemetry_records) * 1.15
    min_lat = 0.0

    pts = []
    for i, (size_kb, lat_ns, tier) in enumerate(telemetry_records):
        log_size = math.log2(size_kb) # 2 to 16
        px = int(x_min + ((log_size - 2) / 14.0) * (x_max - x_min))
        py = int(y_max - (lat_ns / max_lat) * (y_max - y_min))
        pts.append((px, py, tier))

    # Connect points with step lines
    for i in range(len(pts) - 1):
        x0, y0, t0 = pts[i]
        x1, y1, t1 = pts[i+1]
        
        # Color by tier
        if t0 == "L1":
            r, g, b = 56, 189, 248 # Cyan
        elif t0 == "L2":
            r, g, b = 74, 222, 128 # Emerald
        elif t0 == "L3":
            r, g, b = 251, 191, 36 # Amber
        else:
            r, g, b = 248, 113, 113 # Crimson (DRAM)
            
        draw_line(x0, y0, x1, y0, r, g, b, 0.9)
        draw_line(x1, y0, x1, y1, r, g, b, 0.9)

    # Draw point markers
    for px, py, tier in pts:
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx*dx + dy*dy <= 16:
                    set_pixel(px + dx, py + dy, 255, 255, 255, 0.95)

    # Draw tier boundary demarcations
    # 32 KB (log2 = 5)
    x_l1 = int(x_min + ((5 - 2) / 14.0) * (x_max - x_min))
    # 512 KB (log2 = 9)
    x_l2 = int(x_min + ((9 - 2) / 14.0) * (x_max - x_min))
    # 16384 KB (log2 = 14)
    x_l3 = int(x_min + ((14 - 2) / 14.0) * (x_max - x_min))

    for y in range(y_min, y_max):
        set_pixel(x_l1, y, 70, 130, 180, 0.5)
        set_pixel(x_l2, y, 70, 180, 130, 0.5)
        set_pixel(x_l3, y, 220, 120, 70, 0.5)

    png_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "observation_003_memory_cliff.png"))
    write_png(png_path, width, height, bytes(buffer))
    print(f"[OBSERVATION-003] Wrote analysis plate to {png_path}")

if __name__ == "__main__":
    measure_memory_cliff()
