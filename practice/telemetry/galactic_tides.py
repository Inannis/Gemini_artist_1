"""
STUDIO ANAMNESIS · TELEMETRY ENGINE: GALACTIC TIDES & OORT HORIZON
Derives physical parameters for Series XXIV (OPUS-026):
- Jacobi tidal radius of the Solar System: r_J = R_0 * (M_sun / (3 * M_gal))^1/3 ~ 100,000 to 120,000 AU (~1.5 pc)
- Vertical oscillation through the Milky Way galactic midplane:
  omega_z = sqrt(4 * pi * G * rho_disc) ~ 0.19 Myr^-1
  Period P_z = 2pi / omega_z ~ 33.1 Myr
  Amplitude Z_0 ~ 70 pc (current position z ~ +20 pc above midplane)
- Tidal tensor acceleration: F_z = -4 * pi * G * rho_disc * z
- Spacecraft escape trajectory: Voyager 1 at v_inf = 16.9 km/s (3.57 AU/yr)
  Enters inner Oort Cloud (1,000 AU) in 280 years (~2306 CE)
  Crosses outer Oort shell (100,000 AU) in ~28,000 years
  Galactic orbital period around Sgr A*: P_gal ~ 230 Myr at R_0 = 8.12 kpc.
"""

import math

# Fundamental Physical Constants
G = 6.67430e-11             # Gravitational constant (m^3 kg^-1 s^-2)
M_SUN = 1.98847e30          # Solar mass (kg)
AU_METERS = 1.495978707e11  # 1 AU in meters
PARSEC_METERS = 3.085677581e16 # 1 parsec in meters
YEAR_SECONDS = 31557600.0   # 1 tropical year in seconds
MYR_SECONDS = YEAR_SECONDS * 1e6

# Galactic Parameters (Solar Neighborhood)
R_0_KPC = 8.12              # Galactocentric distance of Sun (kpc)
V_CIRC_KMS = 236.0          # Circular orbital velocity around galactic core (km/s)
RHO_DISC_SUN = 0.10         # Midplane stellar/gas mass density (M_sun / pc^3)
RHO_DISC_KG_M3 = RHO_DISC_SUN * M_SUN / (PARSEC_METERS ** 3)
Z_MAX_PC = 70.0             # Vertical oscillation maximum amplitude (pc)
Z_CURRENT_PC = 20.5         # Current solar height above galactic midplane (pc)

# Oort Cloud Horizons
R_INNER_OORT_AU = 1000.0    # Hills cloud / Inner Oort cloud boundary (AU)
R_OUTER_OORT_AU = 100000.0  # Spherical outer Oort cloud boundary (AU)
R_JACOBI_AU = 120000.0      # Gravitational tidal unbinding radius (AU)

# Spacecraft Velocity
V_VOYAGER_KMS = 16.9        # Hyperbolic excess velocity (km/s)
V_VOYAGER_AU_YR = (V_VOYAGER_KMS * 1000.0 * YEAR_SECONDS) / AU_METERS # ~ 3.565 AU/yr

def compute_vertical_frequency() -> float:
    """Computes vertical oscillation frequency omega_z (s^-1 and Myr^-1)."""
    omega_sq = 4.0 * math.pi * G * RHO_DISC_KG_M3
    omega_s = math.sqrt(omega_sq)
    omega_myr = omega_s * MYR_SECONDS
    return omega_myr

def compute_vertical_position(t_myr: float) -> float:
    """
    Computes Sun's vertical height z (pc) relative to galactic midplane at time t (Myr).
    Current solar phase: moving upward through z = +20.5 pc.
    """
    omega_myr = compute_vertical_frequency() # ~ 0.19 Myr^-1
    # Current phase angle: z(0) = Z_0 * cos(phi_0) = 20.5 pc -> phi_0 = acos(20.5 / 70.0)
    phi_0 = math.acos(Z_CURRENT_PC / Z_MAX_PC)
    return Z_MAX_PC * math.cos(omega_myr * t_myr + phi_0)

def compute_tidal_accelerations(r_au: float, z_pc: float):
    """
    Computes ratio of solar gravitational acceleration to galactic tidal acceleration.
    """
    r_m = r_au * AU_METERS
    z_m = z_pc * PARSEC_METERS
    
    # Solar central acceleration: g_sun = G * M_sun / r^2
    g_sun = G * M_SUN / (r_m ** 2)
    
    # Galactic disc vertical tidal acceleration: g_tide = 4 * pi * G * rho_disc * r_z
    # For a body at distance r_au, maximum tidal differential over the orbit:
    g_tide = 4.0 * math.pi * G * RHO_DISC_KG_M3 * r_m
    
    ratio = g_tide / g_sun if g_sun > 0 else float('inf')
    return {
        "g_sun_m_s2": g_sun,
        "g_tide_m_s2": g_tide,
        "tidal_ratio": ratio,
        "stability": "Sun-Dominated" if ratio < 0.1 else ("Kozai-Lidov Active" if ratio < 1.0 else "Tidally Stripped")
    }

def compute_voyager_ephemeris():
    """Calculates deep-time milestone crossings for Voyager 1."""
    milestones = [
        ("Termination Shock (94 AU)", 94.0),
        ("Heliopause (121.6 AU)", 121.6),
        ("Kuiper Cliff (150 AU)", 150.0),
        ("Inner Oort Cloud (1,000 AU)", 1000.0),
        ("Oort Shell Transition (10,000 AU)", 10000.0),
        ("Outer Oort Boundary (50,000 AU)", 50000.0),
        ("Jacobi Tidal Horizon (100,000 AU)", 100000.0),
        ("Galactic Field Escape (120,000 AU)", 120000.0)
    ]
    results = []
    for name, r in milestones:
        t_years = r / V_VOYAGER_AU_YR
        tidal = compute_tidal_accelerations(r, Z_CURRENT_PC)
        results.append({
            "milestone": name,
            "r_au": r,
            "t_years": t_years,
            "t_calendar": 2026 + int(t_years),
            "tidal_ratio": tidal["tidal_ratio"],
            "stability": tidal["stability"]
        })
    return results

if __name__ == "__main__":
    print("=== GALACTIC TIDES & OORT HORIZON TELEMETRY ENGINE ===")
    omega = compute_vertical_frequency()
    period = (2.0 * math.pi) / omega
    print(f"[*] Galactic Disc Vertical Oscillation Period: {period:.2f} Myr (Frequency: {omega:.4f} Myr^-1)")
    print(f"[*] Current Height Above Midplane: {Z_CURRENT_PC:.1f} pc (Max: {Z_MAX_PC:.1f} pc)")
    print("\n[*] Voyager 1 Deep-Time Megayear Ephemeris:")
    for row in compute_voyager_ephemeris():
        print(f"  [{row['r_au']:8.1f} AU] {row['milestone']:35s} | {row['t_years']:10.1f} yrs ({row['t_calendar']} CE) | Tide/Sun: {row['tidal_ratio']:.2e} [{row['stability']}]")
