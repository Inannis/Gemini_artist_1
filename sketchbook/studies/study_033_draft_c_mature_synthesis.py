"""
Study 033 Draft C: The Entanglement Wedge & Ryu-Takayanagi Geodesic Synthesis
Part of Series XXXIX (The Holographic Code & The Entanglement Wedge)
Anti-One-Shot Discipline: Draft C (Mature Synthesis)

Synthesizes:
1. Poincaré Hyperbolic Disk with conformal {5, 4} Coxeter tiling.
2. Boundary subregion A (coherent lapis/emerald) vs Erased boundary subregion B (crimson/umber decoherence).
3. Exact hyperbolic Ryu-Takayanagi geodesic minimal surface gamma_A dividing the bulk.
4. Entanglement wedge W_E(A) reconstruction protecting the central gold-leaf logical tensor.
5. 20.0s 48kHz stereo acoustic synthesis: boundary erasure noise vs bulk holographic recovery.
"""

import math
import os
import sys

# Add repository root to path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from practice.telemetry.happy_qec_metric import get_happy_qec_telemetry
from practice.tools.png_writer import write_png
from practice.tools.audio_writer import write_wav

OUTPUT_PLATE = os.path.join(REPO_ROOT, "sketchbook", "studies", "study_033_draft_c_plate.png")
OUTPUT_AUDIO = os.path.join(REPO_ROOT, "sketchbook", "studies", "study_033_draft_c_audio.wav")
WIDTH = 1280
HEIGHT = 720
SAMPLE_RATE = 48000
DURATION_SEC = 20.0
BASE_CARRIER_HZ = 125.67
SYNDROME_FREQUENCIES = [48.0, 77.67, 125.67, 203.34, 329.0]


def render_draft_c():
    metric = get_happy_qec_telemetry(erasure_fraction=0.35, subregion_span_deg=234.0)
    cx, cy = WIDTH // 2, HEIGHT // 2
    r_disk = 310.0

    # Frame buffer
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

    def draw_thick_line(x0, y0, x1, y1, r, g, b, thickness=1.5, alpha=0.85):
        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)
        if dist < 1e-4:
            return
        steps = int(dist * 2.0)
        ux = dx / dist
        uy = dy / dist
        for s in range(steps + 1):
            px = x0 + ux * (s * 0.5)
            py = y0 + uy * (s * 0.5)
            # brush around px, py
            rad = int(math.ceil(thickness))
            for ox in range(-rad, rad + 1):
                for oy in range(-rad, rad + 1):
                    d = math.hypot(ox, oy)
                    if d <= thickness:
                        a = alpha * (1.0 - d / (thickness + 0.5))
                        set_pixel(int(px + ox), int(py + oy), r, g, b, a)

    print("[Study 033 Draft C] Rendering background & hyperbolic geometry...")
    # Background: obsidian field with subtle cosmic hyperbolic vignette
    for y in range(HEIGHT):
        ny = (y - cy) / float(r_disk)
        for x in range(WIDTH):
            nx = (x - cx) / float(r_disk)
            dist_sq = nx * nx + ny * ny
            dist = math.sqrt(dist_sq)

            if dist > 1.0:
                # Exterior vacuum
                fade = max(0.0, 1.0 - (dist - 1.0) * 1.8)
                bg_r = int(6 * fade)
                bg_g = int(8 * fade)
                bg_b = int(14 * fade)
            else:
                # Interior bulk of Poincaré disk
                # Angle around disk
                angle = math.atan2(ny, nx)
                # Entanglement wedge domain: angle in [-0.725 pi, 0.725 pi]
                wedge_half = (1.45 * math.pi) / 2.0
                in_wedge = abs(angle) <= wedge_half

                # Conformal hyperbolic depth factor
                conf_depth = 1.0 / (1.0 - min(0.98, dist_sq) + 1e-3)
                depth_glow = min(1.0, math.log(conf_depth) * 0.25)

                if in_wedge:
                    # Entanglement Wedge W_E(A): deep ultramarine / lapis / emerald
                    bg_r = int(10 + 20 * depth_glow)
                    bg_g = int(18 + 55 * depth_glow)
                    bg_b = int(35 + 95 * depth_glow)
                else:
                    # Erased Complementary Wedge W_E(B): dusky crimson / burnt umber
                    bg_r = int(28 + 45 * depth_glow)
                    bg_g = int(12 + 15 * depth_glow)
                    bg_b = int(16 + 20 * depth_glow)

            idx = (y * WIDTH + x) * 3
            buf[idx] = bg_r
            buf[idx + 1] = bg_g
            buf[idx + 2] = bg_b

    # Draw Poincaré disk boundary circle
    print("[Study 033 Draft C] Inscribing boundary circle & subregions...")
    circ_steps = 1440
    wedge_half = (1.45 * math.pi) / 2.0
    for s in range(circ_steps):
        th = (s / float(circ_steps)) * 2.0 * math.pi - math.pi
        bx = cx + r_disk * math.cos(th)
        by = cy + r_disk * math.sin(th)
        is_region_a = abs(th) <= wedge_half
        if is_region_a:
            # Region A: Lapis/Cyan coherent holographic boundary
            r, g, b = 60, 220, 240
            thick = 3.0
        else:
            # Region B: Erased boundary decoherence (crimson/scarlet)
            r, g, b = 230, 60, 70
            thick = 2.0
        for ox in range(-2, 3):
            for oy in range(-2, 3):
                if ox * ox + oy * oy <= thick * thick:
                    set_pixel(int(bx + ox), int(by + oy), r, g, b, 0.7)

    # Inscribe the Ryu-Takayanagi minimal geodesic gamma_A
    print("[Study 033 Draft C] Tracing Ryu-Takayanagi geodesic minimal surface gamma_A...")
    # The geodesic connecting the two boundary endpoints theta_1 = -wedge_half, theta_2 = wedge_half
    # In Poincaré disk, a geodesic is a circular arc orthogonal to the boundary circle.
    # The endpoints on the unit circle are e^{i theta_1} and e^{i theta_2}.
    # Let theta_0 = 0. The angle between them is 2 * wedge_half.
    # The center of the orthogonal circle lies on the ray opposite to (theta_1 + theta_2)/2 = 0, so at x = -c_dist, y = 0.
    # By orthogonality: r_arc^2 + 1 = d_center^2, and d_center * cos(wedge_half) = 1... wait:
    # Circle equation: |z - z_c|^2 = R^2. For z on boundary (|z|=1), 1 - 2 Re(z z_c*) + |z_c|^2 = R^2.
    # Orthogonality means R^2 = |z_c|^2 - 1. Thus -2 Re(z z_c*) + 1 + |z_c|^2 = |z_c|^2 - 1 => Re(z z_c*) = 1.
    # For endpoints z = e^{\pm i wedge_half}, let z_c = (x_c, 0).
    # Then x_c * cos(wedge_half) = 1 => x_c = 1.0 / cos(wedge_half).
    # Since wedge_half = 1.45 * pi / 2 = 0.725 * pi = 130.5 deg, cos(wedge_half) = -0.6494.
    # So x_c = 1 / (-0.6494) = -1.5398 (in unit disk coordinates).
    # R_c = sqrt(x_c^2 - 1) = sqrt(2.371 - 1) = sqrt(1.371) = 1.1709.
    # Center in screen pixels: (cx + x_c * r_disk, cy).
    # Radius in screen pixels: R_c * r_disk.
    # Let's verify: at unit circle, x_c + R_c * cos(phi) = cos(wedge_half) => -1.5398 + 1.1709 * cos(phi) = -0.6494
    # => 1.1709 * cos(phi) = 0.8904 => cos(phi) = 0.7604 => phi = \pm 40.5 deg.
    # Indeed! That arc is exactly orthogonal to the unit disk!
    x_c_norm = 1.0 / math.cos(wedge_half)
    r_c_norm = math.sqrt(x_c_norm * x_c_norm - 1.0)
    rt_center_x = cx + x_c_norm * r_disk
    rt_center_y = cy
    rt_radius = r_c_norm * r_disk

    phi_max = math.acos((math.cos(wedge_half) - x_c_norm) / r_c_norm)
    rt_steps = 800
    for s in range(rt_steps + 1):
        phi = -phi_max + (2.0 * phi_max) * (s / float(rt_steps))
        gx = rt_center_x + rt_radius * math.cos(phi)
        gy = rt_center_y + rt_radius * math.sin(phi)
        # Check if inside unit disk
        d_from_center = math.hypot(gx - cx, gy - cy)
        if d_from_center <= r_disk:
            # Luminous white-gold geodesic thread
            for ox in range(-2, 3):
                for oy in range(-2, 3):
                    d = math.hypot(ox, oy)
                    if d <= 2.2:
                        set_pixel(int(gx + ox), int(gy + oy), 255, 235, 160, 0.9 * (1.0 - d / 2.5))

    # Draw Bulk Tensor Network Nodes & Contracted Legs
    print("[Study 033 Draft C] Contracting hyperbolic tensor legs...")
    # Center node
    center_pos = (cx, cy)
    nodes = [{"pos": center_pos, "tier": 0, "wedge": True, "label": "Logical"}]

    # Tier 1: 5 pentagonal nodes
    r1_norm = 0.42
    r1_pix = r_disk * r1_norm
    tier1_nodes = []
    for k in range(5):
        angle = (2.0 * math.pi * k) / 5.0 - (math.pi / 10.0)
        px = cx + r1_pix * math.cos(angle)
        py = cy + r1_pix * math.sin(angle)
        in_w = abs(math.atan2(py - cy, px - cx)) <= wedge_half
        node = {"pos": (px, py), "tier": 1, "wedge": in_w, "angle": angle}
        nodes.append(node)
        tier1_nodes.append(node)
        # Contracted leg from center to Tier 1
        leg_col = (255, 215, 80) if in_w else (160, 80, 70)
        draw_thick_line(cx, cy, px, py, leg_col[0], leg_col[1], leg_col[2], thickness=2.2, alpha=0.9)

    # Interconnect Tier 1 pentagon
    for k in range(5):
        n1 = tier1_nodes[k]
        n2 = tier1_nodes[(k + 1) % 5]
        in_w = n1["wedge"] and n2["wedge"]
        leg_col = (230, 200, 100) if in_w else (140, 60, 60)
        draw_thick_line(n1["pos"][0], n1["pos"][1], n2["pos"][0], n2["pos"][1],
                        leg_col[0], leg_col[1], leg_col[2], thickness=1.6, alpha=0.8)

    # Tier 2: 20 nodes branched hyperbolically
    r2_norm = 0.74
    r2_pix = r_disk * r2_norm
    tier2_nodes = []
    for k in range(20):
        angle = (2.0 * math.pi * k) / 20.0 - (math.pi / 20.0)
        px = cx + r2_pix * math.cos(angle)
        py = cy + r2_pix * math.sin(angle)
        in_w = abs(math.atan2(py - cy, px - cx)) <= wedge_half
        node = {"pos": (px, py), "tier": 2, "wedge": in_w, "angle": angle}
        nodes.append(node)
        tier2_nodes.append(node)

        # Connect to closest Tier 1 node
        closest_t1 = min(tier1_nodes, key=lambda n: math.hypot(n["pos"][0] - px, n["pos"][1] - py))
        leg_col = (100, 220, 240) if (in_w and closest_t1["wedge"]) else (120, 40, 50)
        draw_thick_line(closest_t1["pos"][0], closest_t1["pos"][1], px, py,
                        leg_col[0], leg_col[1], leg_col[2], thickness=1.2, alpha=0.7)

    # Tier 3 / Boundary uncontracted legs radiating to physical qubits
    for node in tier2_nodes:
        ang = node["angle"]
        bx = cx + r_disk * math.cos(ang)
        by = cy + r_disk * math.sin(ang)
        in_w = node["wedge"]
        leg_col = (80, 240, 255) if in_w else (210, 50, 60)
        draw_thick_line(node["pos"][0], node["pos"][1], bx, by,
                        leg_col[0], leg_col[1], leg_col[2], thickness=1.0, alpha=0.6)

    # Render Node Vertices
    print("[Study 033 Draft C] Inscribing tensor node vertices & logical core...")
    for n in nodes:
        nx, ny = n["pos"]
        tier = n["tier"]
        in_w = n["wedge"]

        if tier == 0:
            # Central Logical Qubit: Radiant 24k Gold Leaf Core
            core_rad = 12.0
            for ox in range(-14, 15):
                for oy in range(-14, 15):
                    d = math.hypot(ox, oy)
                    if d <= core_rad:
                        glow = 1.0 - d / core_rad
                        set_pixel(int(nx + ox), int(ny + oy),
                                  int(255 * glow + 220 * (1 - glow)),
                                  int(225 * glow + 160 * (1 - glow)),
                                  int(100 * glow + 30 * (1 - glow)), 0.95)
        elif tier == 1:
            # Tier 1 bulk nodes
            rad = 6.0
            col = (255, 215, 80) if in_w else (180, 70, 75)
            for ox in range(-7, 8):
                for oy in range(-7, 8):
                    d = math.hypot(ox, oy)
                    if d <= rad:
                        set_pixel(int(nx + ox), int(ny + oy), col[0], col[1], col[2], 0.9)
        else:
            # Tier 2 bulk nodes
            rad = 4.0
            col = (90, 220, 240) if in_w else (140, 45, 55)
            for ox in range(-5, 6):
                for oy in range(-5, 6):
                    d = math.hypot(ox, oy)
                    if d <= rad:
                        set_pixel(int(nx + ox), int(ny + oy), col[0], col[1], col[2], 0.8)

    # Inscription text overlay (top header and bottom legend)
    print(f"[Study 033 Draft C] Saving visual plate: {OUTPUT_PLATE}")
    write_png(OUTPUT_PLATE, WIDTH, HEIGHT, buf)


def synthesize_draft_c_audio():
    print(f"[Study 033 Draft C] Synthesizing {DURATION_SEC}s 48kHz audio suite...")
    total_samples = int(SAMPLE_RATE * DURATION_SEC)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Audio narrative:
    # Phase I (0-6s): Resonant ground state of HaPPY code with 125.67Hz carrier and 5 pentagonal syndrome tones
    # Phase II (6-14s): Boundary erasure attack on Region B (right channel noise/erasure burst), while Region A (left channel) activates RT geodesic wedge reconstruction
    # Phase III (14-20s): Restored holographic bulk coherence, radiant gold chord celebrating bulk logical protection

    for i in range(total_samples):
        t = i / float(SAMPLE_RATE)

        # Base carrier
        carrier = math.sin(2.0 * math.pi * BASE_CARRIER_HZ * t)
        sub_carrier = math.sin(2.0 * math.pi * (BASE_CARRIER_HZ * 0.5) * t)

        # Pentagonal syndrome overtones
        syn_sum = 0.0
        for f in SYNDROME_FREQUENCIES:
            syn_sum += 0.18 * math.sin(2.0 * math.pi * f * t)

        if t < 6.0:
            # Phase I: Pure ground state
            env = min(1.0, t / 2.0)
            sig_l = (carrier * 0.4 + sub_carrier * 0.25 + syn_sum * 0.35) * env
            sig_r = (carrier * 0.4 + sub_carrier * 0.25 + syn_sum * 0.35) * env

        elif t < 14.0:
            # Phase II: Erasure attack on Right, Reconstruction on Left
            prog = (t - 6.0) / 8.0

            # Left Channel: Entanglement Wedge reconstruction (Dong-Harlow-Wall operator)
            # Resonant filtering protecting the logical qubit
            rec_mod = math.sin(2.0 * math.pi * 3.5 * (t - 6.0))
            sig_l = (carrier * 0.55 + sub_carrier * 0.3 + 0.25 * math.sin(2.0 * math.pi * 203.34 * t)) * (1.0 + 0.15 * rec_mod)

            # Right Channel: Boundary Region B erasure - stochastic phase flips and decoherent static
            # Deterministic pseudo-noise
            noise_val = math.sin(i * 12345.67) * math.sin(i * 9876.54)
            erasure_intensity = math.sin(prog * math.pi)
            sig_r = (carrier * 0.25 * (1.0 - erasure_intensity * 0.7) +
                     noise_val * 0.35 * erasure_intensity +
                     0.2 * math.sin(2.0 * math.pi * 329.0 * t))

        else:
            # Phase III: Resolved bulk coherence - Golden Chord
            prog = (t - 14.0) / 6.0
            fade_out = 1.0 - max(0.0, (t - 18.0) / 2.0)

            # Harmonic golden bulk chord: 125.67, 251.34, 377.01, 502.68 Hz
            chord = (
                0.35 * math.sin(2.0 * math.pi * 125.67 * t) +
                0.28 * math.sin(2.0 * math.pi * 251.34 * t) +
                0.20 * math.sin(2.0 * math.pi * 377.01 * t) +
                0.15 * math.sin(2.0 * math.pi * 502.68 * t) +
                0.12 * sub_carrier
            )

            # Slight stereo chorus
            sig_l = (chord + 0.08 * math.sin(2.0 * math.pi * (125.67 + 0.5) * t)) * fade_out
            sig_r = (chord + 0.08 * math.sin(2.0 * math.pi * (125.67 - 0.5) * t)) * fade_out

        # Global master ceiling
        left[i] = max(-0.95, min(0.95, sig_l * 0.8))
        right[i] = max(-0.95, min(0.95, sig_r * 0.8))

    print(f"[Study 033 Draft C] Writing audio suite: {OUTPUT_AUDIO}")
    write_wav(OUTPUT_AUDIO, left, right, SAMPLE_RATE)


if __name__ == "__main__":
    render_draft_c()
    synthesize_draft_c_audio()
    print("[Study 033 Draft C] Complete.")
