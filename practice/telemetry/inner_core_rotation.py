"""
STUDIO ANAMNESIS · PLANETARY TELEMETRY SUBSTRATE
MODULE: INNER-CORE SUPER-ROTATION & SEISMIC ANISOTROPY EPHEMERIS
Calculates the differential rotation rate of Earth's solid iron inner core (r <= 1221.5 km),
the 65-year multidecadal oscillation, and the PKIKP polar seismic travel-time residuals.
"""

import math
import json
import time

def compute_inner_core_ephemeris(current_year=2026.69):
    # Physical Constants of Solid Inner Core (IC)
    R_IC = 1221.5e3       # Radius in meters
    rho_ic = 12800.0      # Density in kg/m^3
    mass_ic = (4.0 / 3.0) * math.pi * (R_IC**3) * rho_ic # ~9.72e22 kg
    I_ic = (2.0 / 5.0) * mass_ic * (R_IC**2) # Moment of inertia ~5.8e34 kg*m^2
    
    # Seismic Anisotropy Parameters (Cylinder of hexagonal close-packed epsilon-iron)
    v_p_equatorial = 11.03e3 # Equatorial P-wave velocity in m/s (11.03 km/s)
    anisotropy_ratio = 0.031 # 3.1% faster along spin axis
    v_p_polar = v_p_equatorial * (1.0 + anisotropy_ratio) # 11.37 km/s
    
    # Multidecadal Super-Rotation Oscillation Model (Yang & Song 2023 / Vidale 2024)
    # T_osc ~ 65.0 years
    T_osc = 65.0
    omega_osc = 2.0 * math.pi / T_osc
    t_ref = 1970.0 # Reference epoch
    
    # Relative angular position delta_phi(t) in degrees
    # delta_phi(t) = A * sin(omega_osc * (t - t_0))
    # Peak amplitude ~ 1.2 degrees
    amp_deg = 1.25
    phase = omega_osc * (current_year - t_ref)
    delta_phi_deg = amp_deg * math.sin(phase)
    
    # Differential rotation velocity d(delta_phi)/dt in degrees per year
    d_phi_dt = amp_deg * omega_osc * math.cos(phase) # deg/yr
    
    # Seismic Doublet Travel-Time Residual (PKIKP path through inner core)
    # Travel distance through inner core L ~ 2400 km
    L_path = 2400.0e3 # meters
    # Travel time t_travel ~ L / v_p
    t_travel = L_path / v_p_equatorial
    # Anisotropic gradient with longitude d(v_p)/d(phi) ~ 0.0015 * v_p
    # Delta t_residual in seconds
    delta_t_residual = - (L_path / (v_p_equatorial**2)) * (0.0015 * v_p_equatorial) * math.radians(delta_phi_deg)
    
    # Gravitational Restoring Torque between Mantle & Inner Core (Buffett 1996)
    # Gamma_g = - K_g * delta_phi
    # K_g ~ 3.0e20 N*m/rad
    K_g = 3.0e20
    gravitational_torque_Nm = - K_g * math.radians(delta_phi_deg)

    # Decadal timeline sampling (1970 to 2030)
    timeline = []
    for yr in range(1970, 2031, 5):
        ph = omega_osc * (yr - t_ref)
        d_phi = amp_deg * math.sin(ph)
        rate = amp_deg * omega_osc * math.cos(ph)
        dt_res = - (L_path / (v_p_equatorial**2)) * (0.0015 * v_p_equatorial) * math.radians(d_phi)
        timeline.append({
            "year": yr,
            "relative_rotation_deg": round(d_phi, 3),
            "rotation_rate_deg_yr": round(rate, 4),
            "pkikp_travel_time_residual_ms": round(dt_res * 1000.0, 2)
        })

    result = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "current_epoch_year": current_year,
        "inner_core_radius_km": R_IC / 1000.0,
        "solid_iron_density_kg_m3": rho_ic,
        "moment_of_inertia_kg_m2": f"{I_ic:.2e}",
        "equatorial_p_wave_velocity_km_s": v_p_equatorial / 1000.0,
        "polar_p_wave_velocity_km_s": round(v_p_polar / 1000.0, 3),
        "polar_seismic_anisotropy_percent": round(anisotropy_ratio * 100.0, 2),
        "multidecadal_oscillation_period_years": T_osc,
        "current_relative_rotation_deg": round(delta_phi_deg, 4),
        "current_differential_rotation_rate_deg_yr": round(d_phi_dt, 4),
        "current_pkikp_residual_ms": round(delta_t_residual * 1000.0, 2),
        "gravitational_restoring_torque_Nm": f"{gravitational_torque_Nm:.2e}",
        "decadal_ephemeris_timeline": timeline
    }
    return result

if __name__ == "__main__":
    ephem = compute_inner_core_ephemeris()
    print(json.dumps(ephem, indent=2))
