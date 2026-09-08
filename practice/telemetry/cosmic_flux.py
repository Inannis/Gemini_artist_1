"""
STUDIO ANAMNESIS · PLANETARY TELEMETRY SUBSTRATE
Atmospheric Cosmic Ray Spallation & Single-Event Upset (SEU) Telemetry Engine
Zero External Dependencies (Pure Python Standard Library)
"""

import math
import sys

class CosmicRayTelemetry:
    def __init__(self, altitude_meters=408.0, latitude_deg=47.3769):
        self.altitude = altitude_meters
        self.latitude = latitude_deg
        
        # Physical constants
        self.sea_level_neutron_flux = 0.0125  # neutrons / cm^2 / s for E > 10 MeV
        self.sea_level_muon_flux = 0.0167     # muons / cm^2 / s (1 / cm^2 / min)
        self.hadronic_attenuation_length = 150.0 # g / cm^2
        self.sea_level_depth = 1033.0         # g / cm^2
        
        # Microelectronics parameters (3nm FinFET SRAM cell)
        self.critical_charge_fC = 1.25        # Critical charge to flip a bit
        self.seu_cross_section_cm2 = 1.8e-14  # SEU cross-section per bit for fast neutrons
        
        # Cosmogenic nuclide production in quartz (atoms / g SiO2 / yr at SLHL)
        self.p10_slhl = 4.01
        self.half_life_be10_years = 1.387e6

    def atmospheric_depth(self, h_m):
        """Calculates atmospheric depth in g/cm^2 as a function of altitude."""
        # Standard US Atmosphere exponential profile
        scale_height = 8430.0 # meters
        return self.sea_level_depth * math.exp(-h_m / scale_height)

    def calculate_fluxes(self, h_m=None):
        """Calculates secondary neutron and muon flux at altitude."""
        if h_m is None:
            h_m = self.altitude
            
        depth = self.atmospheric_depth(h_m)
        delta_x = self.sea_level_depth - depth
        
        # Hadronic cascade scaling (neutrons)
        scaling_factor = math.exp(delta_x / self.hadronic_attenuation_length)
        # Geomagnetic latitude cut-off rigidity scaling (Størmer theory)
        lat_rad = math.radians(self.latitude)
        geomag_factor = 0.6 + 0.4 * (math.sin(lat_rad) ** 2)
        
        neutron_flux = self.sea_level_neutron_flux * scaling_factor * geomag_factor
        muon_flux = self.sea_level_muon_flux * (1.0 + 0.18 * (h_m / 1000.0)) * geomag_factor
        
        return {
            "altitude_m": h_m,
            "atmospheric_depth_g_cm2": depth,
            "scaling_factor": scaling_factor,
            "neutron_flux_cm2_s": neutron_flux,
            "neutron_flux_cm2_hour": neutron_flux * 3600.0,
            "muon_flux_cm2_s": muon_flux,
            "muon_flux_cm2_min": muon_flux * 60.0
        }

    def calculate_seu_rate(self, memory_gigabits=64.0, h_m=None):
        """Calculates Single-Event Upset rate in a memory array."""
        fluxes = self.calculate_fluxes(h_m)
        j_n = fluxes["neutron_flux_cm2_s"]
        n_bits = memory_gigabits * 1e9
        
        # SEUs per second = J_n * sigma * n_bits
        upsets_per_sec = j_n * self.seu_cross_section_cm2 * n_bits
        upsets_per_day = upsets_per_sec * 86400.0
        fit_per_mbit = (upsets_per_sec * 1e9) / (memory_gigabits * 1024.0)
        
        return {
            "memory_gigabits": memory_gigabits,
            "neutron_flux_cm2_s": j_n,
            "upsets_per_day": upsets_per_day,
            "hours_between_upsets": 24.0 / max(1e-9, upsets_per_day),
            "fit_per_megabit": fit_per_mbit
        }

    def calculate_cosmogenic_be10(self, exposure_years=100000.0, erosion_rate_cm_yr=0.0001, h_m=None):
        """Calculates in-situ Be-10 concentration in quartz rock face."""
        fluxes = self.calculate_fluxes(h_m)
        scaling = fluxes["scaling_factor"]
        p_be10 = self.p10_slhl * scaling
        lambda_be10 = math.log(2.0) / self.half_life_be10_years
        
        rock_density = 2.65 # g/cm^3
        mu_attenuation = self.hadronic_attenuation_length # g/cm^2
        effective_decay = lambda_be10 + (rock_density * erosion_rate_cm_yr) / mu_attenuation
        
        concentration = (p_be10 / effective_decay) * (1.0 - math.exp(-effective_decay * exposure_years))
        
        return {
            "exposure_years": exposure_years,
            "production_rate_atoms_g_yr": p_be10,
            "steady_state_atoms_g": p_be10 / effective_decay,
            "current_concentration_atoms_g": concentration
        }

if __name__ == "__main__":
    telem = CosmicRayTelemetry(altitude_meters=408.0, latitude_deg=47.3769)
    f = telem.calculate_fluxes()
    seu = telem.calculate_seu_rate(memory_gigabits=64.0)
    be10 = telem.calculate_cosmogenic_be10(exposure_years=50000.0)
    
    print("=" * 65)
    print("      STUDIO ANAMNESIS · COSMIC RAY SPALLATION TELEMETRY      ")
    print("=" * 65)
    print(f"Altitude:                 {f['altitude_m']:.1f} m ASL")
    print(f"Atmospheric Depth:        {f['atmospheric_depth_g_cm2']:.2f} g/cm²")
    print(f"Hadronic Flux Scaling:    {f['scaling_factor']:.3f}x sea-level")
    print(f"Atmospheric Neutron Flux: {f['neutron_flux_cm2_hour']:.2f} neutrons/cm²/hour")
    print(f"Atmospheric Muon Flux:    {f['muon_flux_cm2_min']:.2f} muons/cm²/minute")
    print("-" * 65)
    print(f"Memory Array Size:        {seu['memory_gigabits']:.0f} Gbit (3nm FinFET)")
    print(f"Critical Node Charge:     1.25 fC")
    print(f"Cosmogenic SEU Rate:      {seu['upsets_per_day']:.3f} bit flips/day")
    print(f"Mean Time Between Bitflip:{seu['hours_between_upsets']:.1f} hours")
    print("-" * 65)
    print(f"Cosmogenic ¹⁰Be Inscription (Quartz, 50 kyr exposure):")
    print(f"Concentration:            {be10['current_concentration_atoms_g']:.2e} atoms/g(SiO₂)")
    print("=" * 65)
