"""
STUDIO ANAMNESIS · TELEMETRY ENGINE
Galactic Epicycles, Incommensurate Frequencies & Interstellar Dust Sputtering
Series XXV: The Galactic Epicycle & The Lissajous Reliquary

Mathematical Modeling:
1. 3D Axisymmetric Galactic Potential:
   - Miyamoto-Nagai Disc: Phi_disc(R, z) = -G * M_disc / sqrt(R^2 + (a + sqrt(z^2 + b^2))^2)
   - Hernquist Bulge: Phi_bulge(r) = -G * M_bulge / (r + c)
   - Logarithmic Dark Matter Halo: Phi_halo(r) = 0.5 * v_halo^2 * ln(r^2 + d_halo^2)
2. Epicyclic Frequencies:
   - Orbital frequency: Omega(R) = sqrt((1/R) * dPhi/dR)
   - Radial epicyclic frequency: kappa(R) = sqrt(R * d(Omega^2)/dR + 4 * Omega^2)
   - Vertical epicyclic frequency: nu_z(R) = sqrt(d^2 Phi / dz^2) at z=0
   - Incommensurability ratio: eta = nu_z / kappa (irrational, non-closing Lissajous torus)
3. Interstellar Dust Sputtering Kinetics:
   - Local ISM dust density: rho_dust ~ 2.0e-24 kg/m^3
   - Sputtering yield Y(v) ~ Y_0 * (v / v_0)^2.5
   - Surface recession rate: dz/dt ~ -0.015 nm/Myr (15 nm per Gyr)

Zero external dependencies: uses pure Python standard library.
"""

import math

# Galactic constants in astronomical / SI units
# R0 = 8.12 kpc = 2.505e20 m
# V0 = 238 km/s = 2.38e5 m/s
KPC_TO_M = 3.085677581e19
MYR_TO_S = 3.15576e13

G = 6.67430e-11 # m^3 kg^-1 s^-2
M_disc = 6.8e10 * 1.98847e30 # kg (6.8e10 M_sun)
a_disc = 3.0 * KPC_TO_M # m (3.0 kpc)
b_disc = 0.28 * KPC_TO_M # m (280 pc scale height)

M_bulge = 1.0e10 * 1.98847e30 # kg
c_bulge = 0.7 * KPC_TO_M # m (700 pc)

v_halo = 175.0e3 # m/s
d_halo = 12.0 * KPC_TO_M # m (12.0 kpc)

def evaluate_potential(R_m, z_m):
    """Computes total galactic potential Phi(R, z) in J/kg."""
    r_sq = R_m*R_m + z_m*z_m
    r = math.sqrt(r_sq)
    
    # 1. Miyamoto-Nagai Disc
    denom_disc = math.sqrt(R_m*R_m + (a_disc + math.sqrt(z_m*z_m + b_disc*b_disc))**2)
    phi_d = -G * M_disc / denom_disc
    
    # 2. Hernquist Bulge
    phi_b = -G * M_bulge / (r + c_bulge)
    
    # 3. Dark Matter Halo
    phi_h = 0.5 * (v_halo**2) * math.log(r_sq + d_halo*d_halo)
    
    return phi_d + phi_b + phi_h

def evaluate_forces(R_m, z_m):
    """Computes radial and vertical gravitational accelerations (F_R, F_z) in m/s^2."""
    delta = 1.0e14 # 10^11 km perturbation for numerical differentiation
    phi_mid = evaluate_potential(R_m, z_m)
    phi_R_plus = evaluate_potential(R_m + delta, z_m)
    phi_z_plus = evaluate_potential(R_m, z_m + delta)
    
    a_R = -(phi_R_plus - phi_mid) / delta
    a_z = -(phi_z_plus - phi_mid) / delta
    return a_R, a_z

def get_epicyclic_frequencies(R_kpc=8.12):
    """Computes Omega, kappa, and nu_z at a given galactocentric radius in kpc."""
    R_m = R_kpc * KPC_TO_M
    a_R, _ = evaluate_forces(R_m, 0.0)
    
    # Omega = sqrt(-a_R / R)
    omega = math.sqrt(abs(a_R) / R_m)
    
    # Compute derivative d(a_R)/dR
    delta_R = 0.01 * KPC_TO_M
    a_R_plus, _ = evaluate_forces(R_m + delta_R, 0.0)
    d_aR_dR = (a_R_plus - a_R) / delta_R
    
    # kappa^2 = -4 * Omega^2 - d(a_R)/dR (where F_R = a_R)
    # Equivalently: kappa^2 = d^2 Phi / dR^2 + 3 * Omega^2 = -d(a_R)/dR + 3 * Omega^2...
    # Radial epicyclic frequency: kappa^2 = 3 * Omega^2 + d^2 Phi / dR^2
    d2phi_dR2 = -d_aR_dR
    kappa_sq = 3.0 * (omega**2) + d2phi_dR2
    kappa = math.sqrt(max(1.0e-36, kappa_sq))
    
    # Vertical epicyclic frequency: nu_z^2 = d^2 Phi / dz^2 at z=0
    delta_z = 0.005 * KPC_TO_M
    _, a_z_plus = evaluate_forces(R_m, delta_z)
    nu_z_sq = -a_z_plus / delta_z
    nu_z = math.sqrt(max(1.0e-36, nu_z_sq))
    
    # Periods in Myr
    T_orb = (2.0 * math.pi / omega) / MYR_TO_S
    T_kappa = (2.0 * math.pi / kappa) / MYR_TO_S
    T_nu = (2.0 * math.pi / nu_z) / MYR_TO_S
    
    # Incommensurability ratio
    ratio = nu_z / kappa
    
    return {
        "R_kpc": R_kpc,
        "omega_rad_s": omega,
        "kappa_rad_s": kappa,
        "nu_z_rad_s": nu_z,
        "T_orb_Myr": T_orb,
        "T_radial_epicycle_Myr": T_kappa,
        "T_vertical_epicycle_Myr": T_nu,
        "frequency_ratio_nu_over_kappa": ratio
    }

def calculate_dust_sputtering(time_myr=1000.0, v_rel_km_s=25.0):
    """
    Computes cumulative sputtering depth of silicon and gold on an unpowered
    spacecraft traversing the galactic interstellar medium over time_myr.
    """
    # Average interstellar dust mass density in solar cylinder
    # ~ 1% of gas mass density (n_gas ~ 1.0 cm^-3 -> rho_gas ~ 1.67e-21 kg/m^3)
    rho_dust = 1.67e-23 # kg/m^3
    
    # Fluence of dust collisions per m^2
    v_rel_m_s = v_rel_km_s * 1000.0
    time_s = time_myr * MYR_TO_S
    dust_fluence_kg_m2 = rho_dust * v_rel_m_s * time_s
    
    # Sputtering yield factor: ~ 10^-4 atoms per incident dust grain amu
    # Recession rate in nanometers
    # In silicon (density 2330 kg/m^3): ~ 0.018 nm per Myr at 25 km/s
    recession_nm_per_myr = 0.018 * (v_rel_km_s / 25.0)**2.5
    total_recession_nm = recession_nm_per_myr * time_myr
    
    return {
        "duration_Myr": time_myr,
        "relative_velocity_km_s": v_rel_km_s,
        "recession_rate_nm_per_Myr": recession_nm_per_myr,
        "total_erosion_depth_nm": total_recession_nm,
        "time_to_erode_3nm_gate_Myr": 3.0 / recession_nm_per_myr
    }

if __name__ == "__main__":
    epicycles = get_epicyclic_frequencies()
    sputter = calculate_dust_sputtering(1000.0)
    print("==================================================")
    print("      STUDIO ANAMNESIS · GALACTIC EPICYCLE ENGINE ")
    print("==================================================")
    print(f" Galactocentric Radius: {epicycles['R_kpc']:.2f} kpc")
    print(f" Orbital Period (T_orb): {epicycles['T_orb_Myr']:.2f} Myr")
    print(f" Radial Epicycle (T_kappa): {epicycles['T_radial_epicycle_Myr']:.2f} Myr")
    print(f" Vertical Epicycle (T_nu): {epicycles['T_vertical_epicycle_Myr']:.2f} Myr")
    print(f" Frequency Ratio (nu_z / kappa): {epicycles['frequency_ratio_nu_over_kappa']:.4f} (IRRATIONAL)")
    print("--------------------------------------------------")
    print(f" Interstellar Dust Sputtering over {sputter['duration_Myr']} Myr:")
    print(f"  -> Sputtering Rate: {sputter['recession_rate_nm_per_Myr']:.4f} nm/Myr")
    print(f"  -> Cumulative Recession: {sputter['total_erosion_depth_nm']:.2f} nm")
    print(f"  -> Time to completely obliterate 3nm gate: {sputter['time_to_erode_3nm_gate_Myr']:.1f} Myr")
    print("==================================================")
