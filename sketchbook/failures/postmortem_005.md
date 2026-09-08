# CRITICAL POST-MORTEM 005: Josephson Phase-Slippage & Thermal Quench Runaway
### Experiment: Critical Current Exceedance, Joule Hotspot Nucleation, and Leidenfrost Cavitation
**Date:** September 8, 2026 · Session 006  
**Location:** `sketchbook/failures/`  
**Artifacts Generated:**  
- Visual Analysis Plate: [`failure_005_thermal_quench.png`](failure_005_thermal_quench.png)
- Acoustic Ruin: [`failure_005_thermal_quench.wav`](failure_005_thermal_quench.wav)
- Simulation Code: [`failure_005_thermal_quench_divergence.py`](failure_005_thermal_quench_divergence.py)
- Associated Inquiry: INQ-06 (Thermodynamic Heat & Superconducting Substrates) / INQ-08 (Telluric Radiometry)

---

## I. Intended Premise vs. The Collapse

In our exploration of zero-dissipation computation in Series XVIII, we sought to model the pristine diamagnetic shielding of a superconducting wafer at sub-Kelvin temperatures ($4.2\text{ K}$). In an idealized Meissner state, electrical resistance is strictly zero ($R = 0$); Cooper pairs transport information without a single quantum of thermal entropy.

However, in physical superconductors, lossless transport is conditionally fragile. It is bounded by the critical current density $J_c(T, B)$.

### The Breakdown

1. **The Sub-Critical Regime ($I < I_c, T = 4.2\text{ K}$):**
   The phase difference $\phi$ across grain boundaries is static. Magnetic flux lines are cleanly expelled around the wafer perimeter. The acoustic field is a pristine, motionless 418.2 Hz sine tone.
2. **The Phase-Slip Horizon ($I \to I_c$):**
   As transport current or external magnetic field spikes, thermal fluctuations nucleate localized phase-slips: the superconducting order parameter momentarily vanishes ($\Psi = 0$), allowing a quantum flux line to slip through the barrier. By the Josephson relation $\frac{d\phi}{dt} = \frac{2e}{\hbar} V$, this slip generates a transient voltage spike.
3. **The Thermal Runaway Positive Feedback ($I > I_c$):**
   A non-zero voltage across a finite current creates immediate Joule heating ($P = I \cdot V$). This localized dissipation heats adjacent superconducting grains above $T_c = 93\text{ K}$, converting them into normal resistive metal. 
   - A normal hotspot nucleates.
   - The current is forced to constrict into a narrower superconducting channel, raising the local current density even further ($J \gg J_c$).
   - A catastrophic quench wave propagates outward across the wafer at hundreds of meters per second.
4. **The Ruin:**
   - **Visual:** The smooth potential streamlines shatter violently. The Meissner expulsion collapses, allowing raw magnetic flux to tear into the wafer with turbulent electromagnetic eddy currents.
   - **Acoustic:** The icy, crystalline cavity tone abruptly detonates into a violent inductive voltage pop, followed by the roaring hiss of explosive Leidenfrost cavitation as liquid helium vaporizes into high-pressure gas.

---

## II. The Aesthetic & Architectural Lessons

1. **Zero-Entropy is a High-Wire Act:**
   Zero dissipation is not a permanent, passive plateau; it is a precarious non-equilibrium state maintained against overwhelming thermodynamic gravity. The moment resistance re-enters the system, the accumulated energy discharges catastrophically.
2. **The Contrast between Ruin Types:**
   - Failure 001 was a mathematical overflow (`NaN` contagion).
   - Failure 003 was an over-coupling collapse (Adler injection locking).
   - Failure 004 was a discretization aliasing collapse (skin depth divergence).
   - Failure 005 is a **physical thermodynamic phase quench**: the machine's body burning through its own frozen shield.
3. **Formal Resolution in OPUS-020:**
   This failure informed the interactive architecture of OPUS-020: the interactive web cryostat features an explicit "Trigger Thermal Quench" control, allowing visitors to witness the violent transition from silent Meissner levitation to resistive collapse and liquid helium boiling.
