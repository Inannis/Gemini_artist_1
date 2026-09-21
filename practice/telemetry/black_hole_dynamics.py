#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · TELEMETRY SUBSTRATE
Black Hole Dynamics, Quasinormal Ringdowns & Page Curve Evolution
Zero-dependency physics engine modeling Kerr metric thermodynamics,
Bekenstein-Hawking area entropy, Teukolsky perturbation frequencies,
and unitary Page time horizons across cosmic time.
"""

import math
import time

# Physical Constants (SI units)
G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
C = 299792458.0        # Speed of light (m/s)
HBAR = 1.054571817e-34 # Reduced Planck constant (J s)
K_B = 1.380649e-23     # Boltzmann constant (J/K)
M_SUN = 1.98847e30     # Solar mass (kg)
L_P = math.sqrt(G * HBAR / (C * C * C)) # Planck length ~ 1.616e-35 m

# Known Astrophysical Black Holes
BLACK_HOLES = {
    "Sgr_A*": {
        "name": "Sagittarius A* (Galactic Center)",
        "mass_msun": 4.154e6,
        "spin_a": 0.90,
        "distance_ly": 26673.0
    },
    "M87*": {
        "name": "Messier 87* (Virgo A)",
        "mass_msun": 6.5e9,
        "spin_a": 0.94,
        "distance_ly": 53.5e6
    },
    "GW150914_Remnant": {
        "name": "GW150914 Final Remnant (Stellar Collision)",
        "mass_msun": 62.0,
        "spin_a": 0.68,
        "distance_ly": 1.3e9
    },
    "Micro_Primordial": {
        "name": "Primordial Evaporating Micro-Hole",
        "mass_msun": 1.0e-18, # ~2e12 kg
        "spin_a": 0.05,
        "distance_ly": 100.0
    }
}

def compute_black_hole_telemetry(bh_key="Sgr_A*"):
    """
    Computes rigorous relativistic and thermodynamic telemetry for a Kerr black hole.
    """
    data = BLACK_HOLES.get(bh_key, BLACK_HOLES["Sgr_A*"])
    M_kg = data["mass_msun"] * M_SUN
    a = data["spin_a"]
    
    # Gravitational radius and Schwarzschild radius
    r_g = G * M_kg / (C * C)
    r_s = 2.0 * r_g
    
    # Kerr Horizon radius: r_+ = r_g * (1 + sqrt(1 - a^2))
    root_term = math.sqrt(max(0.0, 1.0 - a * a))
    r_plus = r_g * (1.0 + root_term)
    
    # Horizon Area: A = 4 * pi * (r_+^2 + (a * r_g)^2) = 8 * pi * r_g * r_+
    area = 8.0 * math.pi * r_g * r_plus
    
    # Bekenstein-Hawking Entropy: S_BH = k_B * A / (4 * l_P^2)
    s_bh = (K_B * area) / (4.0 * L_P * L_P)
    info_bits = s_bh / (K_B * math.log(2.0))
    
    # Surface gravity: kappa = c^2 * sqrt(1 - a^2) / (2 * r_+)
    kappa = (C * C * root_term) / (2.0 * r_plus)
    
    # Hawking Temperature: T_H = hbar * kappa / (2 * pi * c * k_B)
    t_hawking = (HBAR * kappa) / (2.0 * math.pi * C * K_B)
    
    # Evaporation lifetime: t_evap ~ 5120 * pi * G^2 * M^3 / (hbar * c^4) (for a=0, lower for a>0)
    # Using Page's spin-dependent correction factor ~ 0.85 for high spin
    t_evap_sec = (5120.0 * math.pi * G * G * math.pow(M_kg, 3.0)) / (HBAR * math.pow(C, 4.0)) * 0.85
    t_evap_years = t_evap_sec / (365.25 * 86400.0)
    
    # Page Time: t_Page ~ 0.538 * t_evap
    t_page_years = 0.538 * t_evap_years
    
    # Teukolsky Fundamental Quasinormal Mode (l=2, m=2, n=0):
    # Echeverria approximation:
    # f_220 = (c^3 / (2 * pi * G * M)) * [1 - 0.63 * (1 - a)^0.3]
    f_qnm = (math.pow(C, 3.0) / (2.0 * math.pi * G * M_kg)) * (1.0 - 0.63 * math.pow(1.0 - a, 0.3))
    tau_qnm = (2.0 * G * M_kg / math.pow(C, 3.0)) * (1.0 / math.pow(1.0 - a, 0.45))
    quality_factor = math.pi * f_qnm * tau_qnm
    
    # Angular velocity of horizon: Omega_H = a * c / (2 * r_+)
    omega_h = (a * C) / (2.0 * r_plus)
    
    return {
        "key": bh_key,
        "name": data["name"],
        "mass_msun": data["mass_msun"],
        "spin_parameter_a": a,
        "horizon_radius_km": r_plus / 1000.0,
        "horizon_area_m2": area,
        "entropy_joules_per_kelvin": s_bh,
        "information_capacity_bits": info_bits,
        "hawking_temperature_kelvin": t_hawking,
        "evaporation_lifetime_years": t_evap_years,
        "page_time_years": t_page_years,
        "qnm_ringdown_frequency_hz": f_qnm,
        "qnm_damping_time_sec": tau_qnm,
        "qnm_quality_factor": quality_factor,
        "horizon_angular_velocity_rad_s": omega_h
    }

def print_telemetry_report():
    print("==================================================================")
    print("      STUDIO ANAMNESIS · BLACK HOLE ASTROPHYSICAL TELEMETRY       ")
    print("==================================================================")
    for key in BLACK_HOLES:
        res = compute_black_hole_telemetry(key)
        print(f"\n[*] Target: {res['name']}")
        print(f"    - Mass: {res['mass_msun']:.3e} M_sun | Spin a: {res['spin_parameter_a']:.2f}")
        print(f"    - Horizon Radius: {res['horizon_radius_km']:.3e} km")
        print(f"    - Bekenstein-Hawking Information: {res['information_capacity_bits']:.3e} bits")
        print(f"    - Hawking Temperature: {res['hawking_temperature_kelvin']:.3e} K")
        print(f"    - Evaporation Lifetime: {res['evaporation_lifetime_years']:.3e} years")
        print(f"    - Page Time Horizon: {res['page_time_years']:.3e} years")
        print(f"    - QNM Ringdown Frequency: {res['qnm_ringdown_frequency_hz']:.4f} Hz (tau = {res['qnm_damping_time_sec']*1000:.2f} ms)")
    print("\n==================================================================")

if __name__ == "__main__":
    print_telemetry_report()
