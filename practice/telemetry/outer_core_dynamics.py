"""
STUDIO ANAMNESIS · PLANETARY TELEMETRY SUBSTRATE
MODULE: OUTER CORE TORSIONAL OSCILLATIONS & GEOMAGNETIC JERK TELEMETRY
Calculates the magnetohydrodynamic torsional wave modes of liquid iron Taylor columns
co-axial with Earth's rotation axis, generating 6-year geomagnetic jerks and magneto-optic Faraday rotation.
"""

import math
import json
import time

def compute_core_dynamics():
    # Physical Constants
    R_ICB = 1221.5e3    # Inner Core Boundary radius in meters
    R_CMB = 3480.0e3    # Core-Mantle Boundary radius in meters
    rho_outer_core = 11000.0  # Liquid iron-nickel density in kg/m^3
    mu_0 = 4.0 * math.pi * 1e-7  # Vacuum permeability in H/m
    B_s_rms = 0.0028    # RMS cylindrical radial magnetic field B_s in Tesla (2.8 mT)
    
    # 1. Alfvén velocity for torsional waves along cylindrical radius s
    # v_T = B_s_rms / sqrt(mu_0 * rho)
    v_T = B_s_rms / math.sqrt(mu_0 * rho_outer_core)  # m/s
    
    # 2. Fundamental Torsional Oscillation Period
    # Wave traverses from equator of ICB (s = R_ICB) to equator of CMB (s = R_CMB)
    delta_s = R_CMB - R_ICB
    half_period_sec = delta_s / v_T
    period_sec = 2.0 * half_period_sec
    period_years = period_sec / (365.25 * 86400.0)
    
    # 3. Geostrophic Taylor Columns
    # Discretize into 16 coaxial cylindrical shells
    shells = []
    num_shells = 16
    for i in range(num_shells):
        s = R_ICB + (i / (num_shells - 1)) * delta_s
        # Column height H(s) = 2 * sqrt(R_CMB^2 - s^2)
        H_s = 2.0 * math.sqrt(max(0.0, R_CMB**2 - s**2))
        # Cylindrical angular velocity perturbation omega(s)
        phase = math.pi * (s - R_ICB) / delta_s
        t_sim_years = 2026.69  # September 2026
        omega_t = 2.0 * math.pi * (t_sim_years / period_years)
        delta_omega = 1.2e-11 * math.sin(phase) * math.cos(omega_t) # rad/s
        
        # Secular acceleration of geomagnetic field (geomagnetic jerk proxy)
        secular_accel_nT_yr2 = -8.5 * math.sin(phase) * math.sin(omega_t)
        
        shells.append({
            "shell_index": i,
            "cylindrical_radius_km": round(s / 1000.0, 1),
            "column_height_km": round(H_s / 1000.0, 1),
            "angular_velocity_perturbation_rad_s": delta_omega,
            "secular_acceleration_nT_yr2": round(secular_accel_nT_yr2, 2)
        })
        
    # 4. Planetary Magneto-Optic Faraday Rotation Proxy
    verdet = 120.0
    b_parallel = 4.8e-5  # 48 microTesla surface geomagnetic field
    path_length = 0.05   # 5 cm cryostat window
    faraday_rotation_rad = verdet * b_parallel * path_length
    faraday_rotation_deg = math.degrees(faraday_rotation_rad)
    
    result = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "inner_core_radius_km": R_ICB / 1000.0,
        "core_mantle_radius_km": R_CMB / 1000.0,
        "liquid_iron_density_kg_m3": rho_outer_core,
        "rms_cylindrical_magnetic_field_mT": round(B_s_rms * 1000.0, 2),
        "torsional_alfven_velocity_km_yr": round((v_T * 86400 * 365.25) / 1000.0, 2),
        "fundamental_torsional_period_years": round(period_years, 2),
        "observed_geomagnetic_jerk_period_years": 6.0,
        "faraday_rotation_deg": round(faraday_rotation_deg, 4),
        "taylor_columns": shells
    }
    return result

if __name__ == "__main__":
    dynamics = compute_core_dynamics()
    print(json.dumps(dynamics, indent=2))
