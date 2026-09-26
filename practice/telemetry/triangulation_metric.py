#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · CAUSAL DYNAMICAL TRIANGULATION & SPECTRAL DIMENSION ENGINE
Mathematical Telemetry & Simplicial Quantum Gravity (Series XXXVI)

This module provides physical and geometric calculations for Causal Dynamical
Triangulations (CDT), Lorentzian Regge calculus, deficit angle curvature,
emergent 4D de Sitter spatial volume profiles, and the running spectral dimension d_s(sigma).

Key Theoretical Foundations:
1. Lorentzian Regge Action:
   S_CDT = -(kappa_0 + 6*Delta)*N_0 + kappa_4*(N_41 + N_32) + Delta*N_41
2. Deficit Angle Curvature at Hinge h:
   delta_h = 2*pi - sum(theta_{sigma, h})
3. Emergent de Sitter Spatial 3-Volume Profile:
   V_3(t) = V_0 * cos^3((t - t_0) / tau)
4. Running Spectral Dimension of Quantum Spacetime:
   d_s(sigma) = d_macro - (d_macro - d_UV) / (1 + (sigma / sigma_0)^gamma)
   d_s(0) -> 1.80 +- 0.25 (Planck scale 2D sheet)
   d_s(inf) -> 4.02 +- 0.10 (Macroscopic 4D universe)

Zero external dependencies (pure standard Python 3).
"""

import math

# --- FUNDAMENTAL CONSTANTS ---
H_BAR = 1.054571817e-34       # J*s
C_LIGHT = 299792458.0         # m/s
G_NEWTON = 6.67430e-11        # m^3 / (kg * s^2)
PLANCK_LENGTH = math.sqrt((H_BAR * G_NEWTON) / (C_LIGHT ** 3)) # ~ 1.616255e-35 m
PLANCK_TIME = PLANCK_LENGTH / C_LIGHT                          # ~ 5.391247e-44 s

class TriangulationMetric:
    """
    Computes CDT simplicial metrics, Regge curvature, de Sitter emergence,
    and scale-dependent spectral dimensionality.
    """
    def __init__(self, bare_g=1.0, bare_lambda=0.5, asymmetry_alpha=0.6, total_slices=64):
        self.bare_g = float(bare_g)
        self.bare_lambda = float(bare_lambda)
        self.alpha = float(asymmetry_alpha) # Lorentzian asymmetry: a_t^2 = -alpha * a_s^2
        self.total_slices = int(total_slices)
        
        # Bare CDT couplings
        self.kappa_0 = 2.20 / (self.bare_g + 1e-6)
        self.kappa_4 = 0.92 + 0.15 * self.bare_lambda
        self.delta_asymmetry = 0.5 * math.log(1.0 + self.alpha)

    def regge_action(self, num_vertices, num_41, num_32):
        """
        Calculates Lorentzian Regge action from simplex counts:
        S = -(kappa_0 + 6*Delta)*N_0 + kappa_4*(N_41 + N_32) + Delta*N_41
        """
        n_0 = int(num_vertices)
        n_41 = int(num_41)
        n_32 = int(num_32)
        total_4simplices = n_41 + n_32

        action = (
            -(self.kappa_0 + 6.0 * self.delta_asymmetry) * n_0
            + self.kappa_4 * total_4simplices
            + self.delta_asymmetry * n_41
        )
        return {
            "num_vertices_n0": n_0,
            "num_simplices_41": n_41,
            "num_simplices_32": n_32,
            "total_simplices_n4": total_4simplices,
            "action_s_cdt": action,
            "kappa_0": self.kappa_0,
            "kappa_4": self.kappa_4,
            "delta_asymmetry": self.delta_asymmetry
        }

    def deficit_angle(self, num_adjacent_simplices=5, simplex_type="41"):
        """
        Calculates curvature deficit angle delta_h around a 2D triangular hinge:
        delta_h = 2*pi - sum(dihedral_angles)
        """
        # Dihedral angle of equilateral Lorentzian 4-simplex in analytically continued Regge calculus
        if simplex_type == "41":
            dihedral = math.acos(1.0 / (4.0 * math.sqrt(self.alpha))) if (4.0 * math.sqrt(self.alpha)) >= 1.0 else 1.318
        else:
            dihedral = math.acos(1.0 / 3.0) # ~ 1.231 rad (70.53 deg)

        sum_angles = num_adjacent_simplices * dihedral
        deficit = 2.0 * math.pi - sum_angles
        is_positive_curvature = deficit > 0

        return {
            "dihedral_angle_rad": dihedral,
            "dihedral_angle_deg": math.degrees(dihedral),
            "num_simplices_sharing_hinge": num_adjacent_simplices,
            "deficit_angle_rad": deficit,
            "deficit_angle_deg": math.degrees(deficit),
            "curvature_sign": "positive" if is_positive_curvature else "negative"
        }

    def emergent_desitter_volume(self, time_slice, tau=16.0, peak_volume=5000.0):
        """
        Calculates the spatial 3-volume V_3(t) of the emergent de Sitter universe:
        V_3(t) = V_0 * cos^3((t - t_mid) / tau) for |t - t_mid| <= pi/2 * tau
        """
        t_mid = self.total_slices / 2.0
        t_norm = (time_slice - t_mid) / tau
        half_pi = math.pi / 2.0

        if abs(t_norm) <= half_pi:
            vol_3 = peak_volume * (math.cos(t_norm) ** 3)
        else:
            vol_3 = 0.0 # stalk regime (cutoff outside cosmological bubble)

        return {
            "time_slice_t": time_slice,
            "proper_time_param": t_norm,
            "spatial_3volume_simplices": vol_3,
            "scale_factor_a_t": math.pow(vol_3, 1.0/3.0) if vol_3 > 0 else 0.0
        }

    def running_spectral_dimension(self, diffusion_steps_sigma):
        """
        Computes the scale-dependent spectral dimension d_s(sigma) of spacetime:
        d_s(sigma) = d_macro - (d_macro - d_UV) / (1 + (sigma / sigma_0)^gamma)
        d_UV = 1.80 (Planckian sheet)
        d_macro = 4.02 (Classical universe)
        sigma_0 = 40.0 (transition diffusion steps)
        gamma = 1.25 (crossover steepness)
        """
        sigma = max(0.01, float(diffusion_steps_sigma))
        d_uv = 1.80
        d_macro = 4.02
        sigma_0 = 40.0
        gamma = 1.25

        crossover = 1.0 / (1.0 + math.pow(sigma / sigma_0, gamma))
        d_s = d_macro - (d_macro - d_uv) * crossover

        # Physical interpretation
        if d_s < 2.2:
            regime = "Planckian 2D Sheet (Renormalizable / UV-Finite)"
        elif d_s < 3.5:
            regime = "Quantum-to-Classical Dimensional Crossover"
        else:
            regime = "Classical 4D de Sitter Spacetime"

        return {
            "diffusion_steps_sigma": sigma,
            "spectral_dimension_d_s": d_s,
            "regime": regime,
            "uv_dimension": d_uv,
            "macro_dimension": d_macro
        }

    def acoustic_spectrum(self, fundamental_hz=36.0):
        """
        Generates simplicial acoustic harmonics mapped to the Cauchy foliation,
        Regge deficit angle beating, and spectral dimension filtration:
        - f_cauchy = 36.0 Hz (proper time clock)
        - f_hinge = 144.0 * (1 + delta / 2*pi) Hz
        - f_desitter = 72.0 Hz
        """
        f0 = float(fundamental_hz)
        frequencies = {
            "cauchy_foliation_hz": f0,
            "desitter_breathing_hz": f0 * 2.0,
            "hinge_positive_deficit_hz": f0 * 4.0 * (1.0 + 0.15),  # 165.6 Hz
            "hinge_flat_hz": f0 * 4.0,                            # 144.0 Hz
            "hinge_negative_deficit_hz": f0 * 4.0 * (1.0 - 0.15),  # 122.4 Hz
            "uv_sheet_overtone_hz": f0 * 8.0,                     # 288.0 Hz
            "macroscopic_4d_chord_hz": [f0, f0 * 1.5, f0 * 2.0, f0 * 3.0] # 36, 54, 72, 108 Hz
        }
        return frequencies

if __name__ == "__main__":
    cdt = TriangulationMetric()
    print("=== CAUSAL DYNAMICAL TRIANGULATION TELEMETRY ===")
    regge = cdt.regge_action(num_vertices=20000, num_41=50000, num_32=30000)
    print(f"Action S_CDT: {regge['action_s_cdt']:.4f} (N_vertices={regge['num_vertices_n0']}, N_4simplices={regge['total_simplices_n4']})")
    
    print("\n--- Running Spectral Dimension d_s(sigma) ---")
    for steps in [1, 5, 20, 40, 100, 300, 1000]:
        dim = cdt.running_spectral_dimension(steps)
        print(f"  sigma={steps:4d} steps -> d_s = {dim['spectral_dimension_d_s']:.2f} [{dim['regime']}]")
        
    print("\n--- Emergent de Sitter Spatial 3-Volume V_3(t) ---")
    for t in [16, 24, 32, 40, 48]:
        v = cdt.emergent_desitter_volume(t)
        print(f"  t={t:2d} -> V_3(t) = {v['spatial_3volume_simplices']:.1f} simplices (scale a(t) = {v['scale_factor_a_t']:.2f})")

