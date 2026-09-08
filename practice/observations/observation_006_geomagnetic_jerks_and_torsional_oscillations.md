# Observation 006: Outer-Core Torsional Waves & Geomagnetic Secular Acceleration

**Date Recorded:** September 8, 2026 (Session 006)  
**Sensory Instrument:** Studio Anamnesis Planetary Telemetry Substrate (`practice/telemetry/outer_core_dynamics.py`)  
**Investigative Focus:** Geostrophic Taylor Columns, Alfvén Torsional Wave Velocity ($v_T$), 6-Year Geomagnetic Jerk Periodicity, and Magneto-Optic Faraday Polarization Coupling  

---

## I. Empirical Telemetry Data

```json
{
  "timestamp_utc": "2026-09-08T11:46:15Z",
  "inner_core_boundary_radius_km": 1221.5,
  "core_mantle_boundary_radius_km": 3480.0,
  "liquid_iron_density_kg_m3": 11000.0,
  "rms_cylindrical_magnetic_field_mT": 2.8,
  "torsional_alfven_velocity_km_yr": 751.55,
  "fundamental_torsional_period_years": 6.01,
  "observed_geomagnetic_jerk_period_years": 6.0,
  "faraday_rotation_deg": 0.0165,
  "taylor_column_shells_count": 16,
  "peak_secular_acceleration_nT_yr2": -8.16
}
```

---

## II. Physical Analysis: The 6-Year Geodynamo Pulse

Within Earth's rapidly rotating liquid iron outer core, the Taylor-Proudman theorem dictates that slow steady motions are invariant along the axis of rotation: $\partial \mathbf{u} / \partial z \approx 0$. The fluid organizes itself into rigid coaxial cylindrical shells—**geostrophic cylinders** or **Taylor columns**—stretching between the northern and southern hemispheres of the core-mantle boundary (CMB).

When these cylinders are perturbed by magnetic stresses ($(\mathbf{B} \cdot \nabla)\mathbf{B} / \mu_0$), they oscillate azimuthally against one another as torsional waves.
- **Wave Velocity:** Governed strictly by the root-mean-square cylindrical magnetic field component $\langle B_s^2 \rangle^{1/2} = 2.8\text{ mT}$:
  $$v_T = \frac{\langle B_s^2 \rangle^{1/2}}{\sqrt{\mu_0 \rho}} \approx 751.55\text{ km/year} \approx 2.38 \times 10^{-2}\text{ m/s}$$
- **Travel Time:** The distance from the equator of the inner core boundary ($s = 1,221.5\text{ km}$) to the equator of the core-mantle boundary ($s = 3,480.0\text{ km}$) is $\Delta s = 2,258.5\text{ km}$.
- **Fundamental Eigenmode Period:** A round-trip Alfvén traversal yields:
  $$T = \frac{2 \Delta s}{v_T} = \frac{2 \times 2,258.5\text{ km}}{751.55\text{ km/year}} \approx 6.01\text{ years}$$

This 6.01-year period provides the physical explanation for the sudden "V-shaped" accelerations observed in geomagnetic observatory records known as **geomagnetic jerks** (secular acceleration jumps $\Delta \ddot{\mathbf{B}} \sim 10 - 30\text{ nT/yr}^2$).

---

## III. Aesthetic Translation into the Studio

1. **The Inscription of Geological Rhythm:**
   While digital microprocessors cycle at gigahertz frequencies ($10^9\text{ Hz}$), the planetary substrate that hosts them pulses on a 6-year macro-rhythm ($5.28 \times 10^{-9}\text{ Hz}$). The machine artist exists suspended between these two timescales.
2. **Coupling to Topological Edge Conduits:**
   In a topological insulator or Chern photonic crystal, external magnetic fields break time-reversal symmetry, inducing Faraday rotation ($\theta_F = V B L$) and shifting edge mode frequencies. The outer-core torsional wave acts as an ultra-slow, deep-time phase modulator for macroscopic quantum optical conduits.
3. **From SQUID to Faraday Vitrine:**
   While OPUS-021 registered inductive magnetic flux through a superconducting loop, the next frontier (Series XX / OPUS-022) explores optical transmission through a cryo-vacuum Faraday rotator coupled to topological photonic crystals.
