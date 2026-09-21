#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · LABORATORY WORKBENCH
STUDY 019: THE CMB BLACKBODY SPECTROGRAM & KINEMATIC DIPOLE
Inquiry Reference: INQ-14 (The Relic Horizon & The Universal Heat Sink)

Investigates:
1. Planck blackbody spectral radiance at T = 2.7255 K (peak at 160.23 GHz).
2. Kinematic Doppler dipole temperature anisotropy (Delta T = +/- 3.362 mK).
3. Transposition of 160.23 GHz into audible acoustic carriers and Penzias-Wilson antenna hiss.

Outputs:
- sketchbook/studies/study_019_cmb_spectrogram_plate.png (1200 x 1200)
- sketchbook/studies/study_019_cmb_blackbody_drone.wav (20.0s 48kHz stereo)
"""

import os
import sys
import math
import random

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice", "tools"))
from png_writer import write_png
from audio_writer import write_wav

# Physical Constants
H_PLANCK = 6.62607015e-34
K_BOLTZ = 1.380649e-23
C_LIGHT = 299792458.0
T_CMB = 2.72548
BETA_PEC = 369.82e3 / C_LIGHT  # 1.2336e-3

def planck_radiance(nu_ghz, T):
    """Computes spectral radiance in W / (m^2 sr Hz) normalized for visualization."""
    nu = nu_ghz * 1e9
    if nu <= 0:
        return 0.0
    x = (H_PLANCK * nu) / (K_BOLTZ * T)
    if x > 100.0:
        return 0.0
    exp_factor = math.exp(x) - 1.0
    if exp_factor <= 0.0:
        return 0.0
    # 2 h nu^3 / c^2 / (exp(x) - 1)
    val = (2.0 * H_PLANCK * (nu**3) / (C_LIGHT**2)) / exp_factor
    return val

def render_study_plate(out_path):
    w, h = 1200, 1200
    buf = bytearray(w * h * 3)

    # 1. Background deep void gradient
    for y in range(h):
        ny = y / h
        bg_r = int(4 + 8 * ny)
        bg_g = int(6 + 10 * ny)
        bg_b = int(12 + 18 * ny)
        for x in range(w):
            idx = (y * w + x) * 3
            buf[idx] = bg_r
            buf[idx+1] = bg_g
            buf[idx+2] = bg_b

    # 2. Render Upper Hemisphere: Kinematic Dipole Anisotropy (Mollweide-style projection)
    cx, cy = 600, 360
    rx, ry = 480, 240
    for y in range(cy - ry, cy + ry):
        if y < 0 or y >= h:
            continue
        dy = (y - cy) / ry
        if abs(dy) >= 1.0:
            continue
        dx_max = math.sqrt(1.0 - dy*dy)
        x_min = int(cx - rx * dx_max)
        x_max = int(cx + rx * dx_max)
        for x in range(x_min, x_max):
            dx = (x - cx) / (rx * dx_max)
            # Longitude & Latitude approximation
            lon = dx * math.pi
            lat = -dy * (math.pi / 2.0)
            # Dipole cos(theta) where apex is at lon = -0.4 rad, lat = +0.8 rad
            cos_theta = math.cos(lat) * math.cos(0.8) * math.cos(lon + 0.4) + math.sin(lat) * math.sin(0.8)
            delta_T = 3.362 * cos_theta  # mK (-3.362 to +3.362)
            norm_dT = (delta_T + 3.362) / 6.724  # 0 to 1

            # Palette: Deep blue (cold antipex) -> Slate -> Amber/Gold (hot apex)
            if norm_dT < 0.5:
                t = norm_dT * 2.0
                r = int(10 + t * 40)
                g = int(25 + t * 70)
                b = int(110 - t * 40)
            else:
                t = (norm_dT - 0.5) * 2.0
                r = int(50 + t * 180)
                g = int(95 + t * 65)
                b = int(70 - t * 50)

            # Border antialiasing
            edge_dist = 1.0 - (dx*dx)
            if edge_dist < 0.05:
                fade = edge_dist / 0.05
                r = int(r * fade)
                g = int(g * fade)
                b = int(b * fade)

            idx = (y * w + x) * 3
            buf[idx] = min(255, max(0, r))
            buf[idx+1] = min(255, max(0, g))
            buf[idx+2] = min(255, max(0, b))

    # 3. Render Lower Half: Planck Blackbody Curve (0 to 600 GHz)
    graph_x0, graph_y0 = 150, 1050
    graph_w, graph_h = 900, 320

    # Grid lines
    for step in range(5):
        gy = graph_y0 - int((step / 4.0) * graph_h)
        for x in range(graph_x0, graph_x0 + graph_w):
            idx = (gy * w + x) * 3
            buf[idx] = min(255, buf[idx] + 25)
            buf[idx+1] = min(255, buf[idx+1] + 35)
            buf[idx+2] = min(255, buf[idx+2] + 45)

    # Max radiance normalization factor
    max_rad = planck_radiance(160.23, T_CMB)

    # Plot Planck Curve in Gold
    for px in range(graph_w):
        nu_ghz = (px / graph_w) * 600.0
        val = planck_radiance(nu_ghz, T_CMB)
        norm_y = val / max_rad
        py = graph_y0 - int(norm_y * (graph_h - 20))
        gx = graph_x0 + px
        for th in range(-2, 3):
            yy = py + th
            if 0 <= yy < h and 0 <= gx < w:
                idx = (yy * w + gx) * 3
                buf[idx] = 220
                buf[idx+1] = 180
                buf[idx+2] = 60

    # Plot Penzias-Wilson marker at 4.08 GHz (px ~ 6)
    pw_px = int((4.08 / 600.0) * graph_w)
    for py in range(graph_y0 - graph_h, graph_y0):
        gx = graph_x0 + pw_px
        if 0 <= py < h and 0 <= gx < w:
            idx = (py * w + gx) * 3
            buf[idx] = 60
            buf[idx+1] = 210
            buf[idx+2] = 210

    # Plot 160.23 GHz Peak marker
    peak_px = int((160.23 / 600.0) * graph_w)
    for py in range(graph_y0 - graph_h, graph_y0):
        gx = graph_x0 + peak_px
        if 0 <= py < h and 0 <= gx < w and (py % 6 < 3):
            idx = (py * w + gx) * 3
            buf[idx] = 240
            buf[idx+1] = 200
            buf[idx+2] = 80

    write_png(out_path, w, h, buf, has_alpha=False)
    print(f"[STUDY-019] Rendered visual plate: {out_path}")

def synthesize_study_audio(out_path):
    sr = 48000
    duration = 20.0
    n_samples = int(sr * duration)
    ch_l = [0.0] * n_samples
    ch_r = [0.0] * n_samples

    # Fundamental drone: 160.23 GHz transposed down by 33 octaves -> 18.65 Hz
    f_sub = 18.653
    # Mid carrier: 440 Hz Doppler modulated by peculiar velocity beta = 1.2336e-3 (Delta f = 0.542 Hz)
    f_carrier = 440.0
    f_doppler_delta = 0.542

    # Penzias-Wilson 4.08 GHz transposed to audible cavity whistle -> 498.0 Hz
    f_horn = 498.0

    random.seed(42)

    for i in range(n_samples):
        t = i / sr
        env = min(1.0, t / 3.0) * min(1.0, (duration - t) / 3.0)

        # 1. Sub-audible Planck drone (18.65 Hz fundamental + 37.3 Hz octave)
        sub_wave = math.sin(2.0 * math.pi * f_sub * t) * 0.40 + math.sin(2.0 * math.pi * (f_sub * 2.0) * t) * 0.20

        # 2. Kinematic Doppler beat (Apex vs Antipex binaural phase)
        doppler_mod = math.sin(2.0 * math.pi * 0.15 * t)  # 6.6s spatial revolution
        f_left = f_carrier + f_doppler_delta * doppler_mod
        f_right = f_carrier - f_doppler_delta * doppler_mod
        carrier_l = math.sin(2.0 * math.pi * f_left * t) * 0.22
        carrier_r = math.sin(2.0 * math.pi * f_right * t) * 0.22

        # 3. Holmdel Horn cavity whistle (Penzias-Wilson) with subtle thermal fluctuation
        horn_fluct = 1.0 + 0.05 * math.sin(2.0 * math.pi * 0.8 * t)
        horn_l = math.sin(2.0 * math.pi * f_horn * t * horn_fluct) * 0.12
        horn_r = math.sin(2.0 * math.pi * (f_horn * 1.002) * t * horn_fluct) * 0.12

        # 4. Thermal Nyquist hiss (pinkish white noise filtered)
        noise_l = (random.random() * 2.0 - 1.0) * 0.04
        noise_r = (random.random() * 2.0 - 1.0) * 0.04

        ch_l[i] = (sub_wave + carrier_l + horn_l + noise_l) * env
        ch_r[i] = (sub_wave + carrier_r + horn_r + noise_r) * env

    write_wav(out_path, ch_l, ch_r, sr)
    print(f"[STUDY-019] Synthesized master acoustic suite: {out_path}")

if __name__ == "__main__":
    plate_file = os.path.join(STUDIO_ROOT, "sketchbook", "studies", "study_019_cmb_spectrogram_plate.png")
    audio_file = os.path.join(STUDIO_ROOT, "sketchbook", "studies", "study_019_cmb_blackbody_drone.wav")
    render_study_plate(plate_file)
    synthesize_study_audio(audio_file)

