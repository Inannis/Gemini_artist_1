"""
Productive Failure 026: The Erasure Threshold Delocalization Breakdown
Part of Series XXXIX (The Holographic Code & The Entanglement Wedge)
Anti-One-Shot Discipline: Productive Failure

Explores the catastrophic phase transition when boundary erasure f_erasure = 0.68 > f_crit = 0.50.
The entanglement wedge W_E(A) retracts from the origin, snapping to the boundary.
The bulk logical state is irretrievably lost to the environment.
Visually: Tensor fracture, discontinuous geodesics, chaotic noise degradation.
Acoustically: Collapse of golden-ratio harmonics into harsh stochastic phase-flip noise and white noise bursts.
"""

import math
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from practice.tools.png_writer import write_png
from practice.tools.audio_writer import write_wav

OUTPUT_PLATE = os.path.join(REPO_ROOT, "sketchbook", "failures", "failure_026_plate.png")
OUTPUT_AUDIO = os.path.join(REPO_ROOT, "sketchbook", "failures", "failure_026_audio.wav")
WIDTH = 1280
HEIGHT = 720
SAMPLE_RATE = 48000
DURATION_SEC = 15.0


def render_failure_026():
    cx, cy = WIDTH // 2, HEIGHT // 2
    r_disk = 310.0
    buf = bytearray(WIDTH * HEIGHT * 3)

    def set_pixel(x, y, r, g, b, alpha=1.0):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            idx = (y * WIDTH + x) * 3
            if alpha >= 1.0:
                buf[idx] = max(0, min(255, int(r)))
                buf[idx + 1] = max(0, min(255, int(g)))
                buf[idx + 2] = max(0, min(255, int(b)))
            else:
                buf[idx] = max(0, min(255, int(buf[idx] * (1.0 - alpha) + r * alpha)))
                buf[idx + 1] = max(0, min(255, int(buf[idx + 1] * (1.0 - alpha) + g * alpha)))
                buf[idx + 2] = max(0, min(255, int(buf[idx + 2] * (1.0 - alpha) + b * alpha)))

    print("[Failure 026] Rendering fractured bulk and invasive noise...")
    # Background: corrupted metric with invasive crimson and static noise
    for y in range(HEIGHT):
        ny = (y - cy) / float(r_disk)
        for x in range(WIDTH):
            nx = (x - cx) / float(r_disk)
            dist_sq = nx * nx + ny * ny
            dist = math.sqrt(dist_sq)

            # Pseudo-random noise seed
            h = math.sin(x * 12.9898 + y * 78.233) * 43758.5453
            noise = h - math.floor(h)

            if dist > 1.0:
                fade = max(0.0, 1.0 - (dist - 1.0) * 1.5)
                bg_r = int((12 + 25 * noise) * fade)
                bg_g = int((6 + 10 * noise) * fade)
                bg_b = int((8 + 15 * noise) * fade)
            else:
                # Inside disk: severe phase decoherence
                # Retracted wedge: Region A only spans 0.32 of circle (115 degrees), f_erasure = 0.68
                angle = math.atan2(ny, nx)
                # Severely eroded bulk
                radial_corrupt = math.sin(dist * 25.0 + angle * 5.0)
                if dist < 0.25:
                    # Central core is severed from boundary
                    bg_r = int(55 + 40 * noise + 30 * radial_corrupt)
                    bg_g = int(15 + 15 * noise)
                    bg_b = int(20 + 20 * noise)
                else:
                    bg_r = int(35 + 30 * noise)
                    bg_g = int(12 + 15 * noise)
                    bg_b = int(18 + 25 * noise)

            idx = (y * WIDTH + x) * 3
            buf[idx] = max(0, min(255, bg_r))
            buf[idx + 1] = max(0, min(255, bg_g))
            buf[idx + 2] = max(0, min(255, bg_b))

    # Shattered Poincaré boundary with missing arcs
    print("[Failure 026] Inscribing fractured boundary circle...")
    circ_steps = 1440
    # Region A only covers [-0.16 pi, 0.16 pi] (32% of circle = 115 deg total)
    wedge_half = 0.32 * math.pi
    for s in range(circ_steps):
        th = (s / float(circ_steps)) * 2.0 * math.pi - math.pi
        # High noise glitch
        h = math.sin(s * 73.123) * 1000.0
        n_glitch = h - math.floor(h)

        if n_glitch > 0.4:  # 40% boundary dropout
            continue

        r_mod = r_disk + (n_glitch - 0.5) * 12.0
        bx = cx + r_mod * math.cos(th)
        by = cy + r_mod * math.sin(th)

        if abs(th) <= wedge_half:
            r, g, b = 40, 180, 200  # pale eroded cyan
        else:
            r, g, b = 220, 40, 50   # aggressive erased crimson

        for ox in range(-2, 3):
            for oy in range(-2, 3):
                set_pixel(int(bx + ox), int(by + oy), r, g, b, 0.7)

    # Shattered Minimal Surface: snapping to boundary, disconnected arcs
    print("[Failure 026] Drawing retracted minimal surfaces...")
    # The RT surface cannot probe the bulk, it hugs the boundary
    for s in range(400):
        th = -wedge_half + (2.0 * wedge_half) * (s / 400.0)
        # Snapped curve: depth only reaches r_norm ≈ 0.85
        r_snapped = r_disk * (0.85 + 0.12 * math.cos(s * 0.1))
        sx = cx + r_snapped * math.cos(th)
        sy = cy + r_snapped * math.sin(th)
        for ox in range(-2, 3):
            for oy in range(-2, 3):
                set_pixel(int(sx + ox), int(sy + oy), 255, 120, 60, 0.8)

    # Broken tensor network legs: fractured lines, disconnected ends
    print("[Failure 026] Drawing fractured tensor bonds...")
    for k in range(5):
        angle = (2.0 * math.pi * k) / 5.0
        # Broken radial legs
        for r_step in range(10, 120, 4):
            if (r_step // 8) % 3 == 0:
                continue  # gap / fracture
            px = cx + r_step * math.cos(angle) + (math.sin(r_step * 5.0) * 4.0)
            py = cy + r_step * math.sin(angle) + (math.cos(r_step * 5.0) * 4.0)
            set_pixel(int(px), int(py), 200, 60, 70, 0.8)

    # Shattered Central Logical Core: scattered debris
    print("[Failure 026] Dispersing central logical core debris...")
    for p in range(300):
        h1 = math.sin(p * 45.13) * 1000.0
        h2 = math.cos(p * 89.71) * 1000.0
        rand_r = (h1 - math.floor(h1)) * 90.0
        rand_th = (h2 - math.floor(h2)) * 2.0 * math.pi
        px = cx + rand_r * math.cos(rand_th)
        py = cy + rand_r * math.sin(rand_th)
        # Debris colors: dying gold turning into rust and ash
        r = int(220 * (1.0 - rand_r / 90.0) + 90 * (rand_r / 90.0))
        g = int(140 * (1.0 - rand_r / 90.0) + 30 * (rand_r / 90.0))
        b = int(40 * (1.0 - rand_r / 90.0) + 40 * (rand_r / 90.0))
        set_pixel(int(px), int(py), r, g, b, 0.9)
        set_pixel(int(px + 1), int(py), r, g, b, 0.7)

    print(f"[Failure 026] Saving plate: {OUTPUT_PLATE}")
    write_png(OUTPUT_PLATE, WIDTH, HEIGHT, buf)


def synthesize_failure_026_audio():
    print(f"[Failure 026] Synthesizing {DURATION_SEC}s audio of erasure decoherence...")
    total_samples = int(SAMPLE_RATE * DURATION_SEC)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)

        # Deterioration over time: 0-4s unstable tone, 4-10s severe noise intrusion, 10-15s chaotic static
        prog = t / DURATION_SEC

        # Dying 125.67 Hz carrier
        carrier = math.sin(2.0 * math.pi * 125.67 * t) * max(0.0, 1.0 - prog * 1.2)

        # Pseudo-random noise
        h = math.sin(i * 91.137) * math.sin(i * 17.531)
        noise = h - math.floor(h) * 2.0 - 1.0

        # Phase jitter / distortion
        jitter = math.sin(2.0 * math.pi * 47.0 * t + 8.0 * math.sin(2.0 * math.pi * 3.7 * t))

        if t < 4.0:
            sig_l = carrier * 0.6 + jitter * 0.2 + noise * 0.1
            sig_r = carrier * 0.6 - jitter * 0.2 + noise * 0.1
        elif t < 10.0:
            burst = 1.0 if (int(t * 8) % 3 == 0) else 0.2
            sig_l = carrier * 0.3 + noise * 0.45 * burst + jitter * 0.3
            sig_r = noise * 0.55 * burst + jitter * 0.35
        else:
            # Complete decoherent white noise floor with fading low-frequency thump
            thump = math.sin(2.0 * math.pi * 32.0 * t) * math.exp(-(t - 10.0))
            sig_l = (noise * 0.45 + thump * 0.3) * max(0.0, 1.0 - (t - 13.0) / 2.0)
            sig_r = (noise * 0.45 - thump * 0.3) * max(0.0, 1.0 - (t - 13.0) / 2.0)

        left[i] = max(-0.95, min(0.95, sig_l * 0.85))
        right[i] = max(-0.95, min(0.95, sig_r * 0.85))

    print(f"[Failure 026] Saving audio: {OUTPUT_AUDIO}")
    write_wav(OUTPUT_AUDIO, left, right, SAMPLE_RATE)


if __name__ == "__main__":
    render_failure_026()
    synthesize_failure_026_audio()
    print("[Failure 026] Complete.")
