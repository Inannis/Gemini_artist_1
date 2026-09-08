"""
STUDIO ANAMNESIS · TELEMETRY ENGINE: HELIOPAUSE & INTERSTELLAR PLASMA
Derives physical parameters for Series XXIII (OPUS-025):
- Solar wind density radial decay: n_sw(r) = n_0 * (r_0 / r)^2
- Termination Shock (r_TS ~ 94 AU) compression ratio s ~ 2.6
- Heliopause boundary (r_HP ~ 121.6 AU) jump into Very Local Interstellar Medium (VLISM)
- Cold interstellar plasma density n_e: 0.002 cm^-3 -> 0.085 cm^-3
- Electron Langmuir plasma frequency: f_p = (1 / 2pi) * sqrt(n_e * e^2 / (eps_0 * m_e)) ~ 8980 * sqrt(n_e) Hz
- Attowatt radio link budget: 8.42 GHz X-band carrier, 23W transmitter, 3.66m HGA,
  Friis path loss over 122 AU (>316 dB), received power at DSN 70m dish in attowatts (10^-18 W).
"""

import math

# Fundamental Physical Constants
C = 299792458.0             # Speed of light (m/s)
E_CHARGE = 1.602176634e-19  # Elementary charge (C)
M_ELECTRON = 9.1093837e-31  # Electron mass (kg)
EPSILON_0 = 8.8541878128e-12# Vacuum permittivity (F/m)
K_BOLTZMANN = 1.380649e-23  # Boltzmann constant (J/K)
AU_METERS = 1.495978707e11  # 1 AU in meters

# Heliopause Boundaries
R_TS_AU = 94.0              # Solar wind termination shock (AU)
R_HP_AU = 121.6             # Heliopause boundary (Voyager 1 crossing, Aug 2012)
N_0_1AU = 5.0               # Solar wind proton/electron density at 1 AU (cm^-3)
N_VLISM = 0.085             # Very Local Interstellar Medium electron density (cm^-3)
T_SOLAR_WIND = 1.2e5        # Solar wind temperature (K)
T_VLISM = 7500.0            # Pristine interstellar plasma temperature (K)

# Deep Space Communications (Voyager 1 / DSN 70m Dish)
FREQ_CARRIER_HZ = 8.42e9    # 8.42 GHz X-band
TX_POWER_WATTS = 23.0       # 23 W TWTA transmitter
TX_GAIN_DBI = 48.0          # 3.66m high gain parabolic reflector
RX_GAIN_DBI = 74.2          # Deep Space Network 70m cryogenic dish
RX_TEMP_K = 12.0            # L-He cooled HEMT preamplifier system temperature
BANDWIDTH_HZ = 10.0         # Coherent tracking bandwidth

def compute_plasma_density(r_au: float) -> float:
    """
    Computes electron density n_e (cm^-3) at heliocentric distance r (AU).
    """
    if r_au < R_TS_AU:
        # Supersonic solar wind: r^-2 falloff
        return N_0_1AU * ((1.0 / r_au) ** 2)
    elif r_au < R_HP_AU:
        # Inner heliosheath: shocked, heated, compressed subsonic solar wind
        # Normalized empirical value ~ 0.002 cm^-3
        compression = 2.6
        density_ts = N_0_1AU * ((1.0 / R_TS_AU) ** 2) * compression
        # Slight gradient across sheath
        frac = (r_au - R_TS_AU) / (R_HP_AU - R_TS_AU)
        return density_ts * (1.0 - 0.4 * frac)
    else:
        # Very Local Interstellar Medium (VLISM)
        # Cold, dense interstellar plasma with slight compression nose ramp
        delta_r = r_au - R_HP_AU
        return N_VLISM * (1.0 + 0.15 * math.tanh(delta_r / 10.0))

def compute_plasma_frequency(n_e_cm3: float) -> float:
    """
    Computes electron plasma frequency f_p (Hz) from density (cm^-3).
    f_p = (1 / 2pi) * sqrt(n_e * e^2 / (eps_0 * m_e))
    """
    n_e_m3 = n_e_cm3 * 1.0e6
    omega_p = math.sqrt((n_e_m3 * (E_CHARGE ** 2)) / (EPSILON_0 * M_ELECTRON))
    return omega_p / (2.0 * math.pi)

def compute_link_budget(r_au: float):
    """
    Computes radio transmission budget from deep-space probe at distance r_au.
    Returns:
      dist_meters, path_loss_db, rx_power_watts, rx_power_dbm, noise_power_watts, snr_db
    """
    dist_m = r_au * AU_METERS
    wavelength = C / FREQ_CARRIER_HZ
    # Free Space Path Loss: FSPL = (4 * pi * d / lambda)^2
    fspl = (4.0 * math.pi * dist_m / wavelength) ** 2
    fspl_db = 10.0 * math.log10(fspl)
    
    # Tx power in dBm: 10 * log10(P_watts * 1000)
    tx_power_dbm = 10.0 * math.log10(TX_POWER_WATTS * 1000.0)
    
    # Received power in dBm
    rx_power_dbm = tx_power_dbm + TX_GAIN_DBI + RX_GAIN_DBI - fspl_db
    rx_power_w = (10.0 ** ((rx_power_dbm - 30.0) / 10.0))
    
    # Noise power: P_n = k_B * T_sys * B
    noise_power_w = K_BOLTZMANN * RX_TEMP_K * BANDWIDTH_HZ
    noise_power_dbm = 10.0 * math.log10(noise_power_w * 1000.0)
    
    snr_db = rx_power_dbm - noise_power_dbm
    return {
        "dist_m": dist_m,
        "fspl_db": fspl_db,
        "rx_power_w": rx_power_w,
        "rx_power_dbm": rx_power_dbm,
        "rx_power_attowatts": rx_power_w * 1e18,
        "noise_power_w": noise_power_w,
        "noise_power_dbm": noise_power_dbm,
        "snr_db": snr_db
    }

def profile_heliopause_transect():
    """Generates diagnostic profile across 80 to 150 AU."""
    distances = [80.0, 93.9, 94.1, 105.0, 121.5, 121.7, 135.0, 150.0]
    results = []
    for r in distances:
        ne = compute_plasma_density(r)
        fp = compute_plasma_frequency(ne)
        link = compute_link_budget(r)
        results.append({
            "r_au": r,
            "region": "Solar Wind" if r < R_TS_AU else ("Heliosheath" if r < R_HP_AU else "Interstellar (VLISM)"),
            "n_e_cm3": ne,
            "f_p_hz": fp,
            "rx_attowatts": link["rx_power_attowatts"],
            "snr_db": link["snr_db"]
        })
    return results

if __name__ == "__main__":
    print("=== HELIOPAUSE & INTERSTELLAR PLASMA TELEMETRY ENGINE ===")
    profile = profile_heliopause_transect()
    for row in profile:
        print(f"[{row['r_au']:5.1f} AU] {row['region']:20s} | ne: {row['n_e_cm3']:8.5f} cm^-3 | fp: {row['f_p_hz']:7.1f} Hz | Rx: {row['rx_attowatts']:6.2f} aW | SNR: {row['snr_db']:+5.1f} dB")
