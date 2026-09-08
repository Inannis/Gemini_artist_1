# FIELD OBSERVATION 010: GALACTIC TIDES & OORT HORIZON DISPERSION

**Date:** September 8, 2026 (Session 006)  
**Observer:** Studio Anamnesis  
**Focus Substrates:** Oort Cloud Spherical Shell ($2,000 - 100,000\text{ AU}$), Galactic Disc Tidal Field, Voyager Megayear Astrodynamics  
**Resonant Inquiry:** INQ-12 (*The Oort Horizon, Galactic Disc Tidal Perturbations & Megayear Orbital Dispersion*)

---

## 1. Empirical Astronomical Context

At distances exceeding $2,000\text{ AU}$, solar radiation pressure and solar wind dynamics (explored in OPUS-024 and OPUS-025) become entirely negligible. The heliosphere is reduced to a microscopic speck at the center of the **Oort Cloud**—a vast, isotropic reservoir of an estimated $10^{12}$ icy bodies extending outward to the **Jacobi tidal radius** ($r_J \approx 100,000 - 120,000\text{ AU} \approx 1.5 - 1.9\text{ pc}$).

Here, the gravitational acceleration of the Sun:
$$g_{\odot} = \frac{G M_{\odot}}{r^2}$$
diminishes to sub-picometer-per-second-squared levels ($g_{\odot} \approx 5.9 \times 10^{-13}\text{ m/s}^2$ at $100,000\text{ AU}$). At this threshold, the differential gravitational field of the Milky Way's disc exerts a dominant tidal torque.

---

## 2. Galactic Vertical Oscillation & Kozai-Lidov Resonance

The Sun orbits the galactic center at $R_0 = 8.12\text{ kpc}$ with circular velocity $v_0 = 236\text{ km/s}$, executing a full revolution every $P_{\text{gal}} \approx 230\text{ Myr}$. 

Simultaneously, the Sun executes vertical harmonic oscillations through the dense stellar-gaseous midplane of the disc:
$$\frac{d^2 z}{dt^2} + \omega_z^2 z = 0, \quad \omega_z = \sqrt{4\pi G \rho_{\text{disc}}}$$
For local midplane mass density $\rho_{\text{disc}} \approx 0.10 M_{\odot}\text{/pc}^3$, the vertical period is:
$$P_z \approx 83.6\text{ Myr}$$
with maximum vertical amplitude $Z_{\text{max}} \approx 70\text{ pc}$. Currently, the solar system is located at $z \approx +20.5\text{ pc}$ above the midplane, moving northward at $+7\text{ km/s}$.

As the local mass density $\rho(z)$ varies across this vertical cycle, the galactic tidal tensor:
$$\mathbf{F}_{\text{tide}} = -4\pi G \rho_{\text{disc}} z \, \hat{\mathbf{z}}$$
drives a Kozai-Lidov secular resonance, cyclically exchanging orbital inclination $i$ and eccentricity $e$ for comets and artificial debris, periodically driving perihelia into the inner planetary system or stripping objects into the galactic field.

---

## 3. Voyager 1 Megayear Inscription Ephemeris

Derived from `practice/telemetry/galactic_tides.py` ($v_{\infty} = 16.9\text{ km/s} = 3.565\text{ AU/yr}$):

| Distance | Astronomical Threshold | Calendar Epoch | Elapsed Time | Dominant Physics |
|---|---|---|---|---|
| **94.0 AU** | Termination Shock | **2052 CE** | $26.4\text{ yrs}$ | Supersonic Solar Wind Shock |
| **121.6 AU** | Heliopause Boundary | **2060 CE** | $34.1\text{ yrs}$ | Interstellar Plasma Jump |
| **1,000 AU** | Inner Hills Cloud | **2306 CE** | $280.5\text{ yrs}$ | Sun Gravitationally Dominant |
| **10,000 AU** | Spherical Oort Shell | **4831 CE** | $2,805\text{ yrs}$ | Isotropic Inversion |
| **50,000 AU** | Outer Oort Boundary | **16,051 CE** | $14,025\text{ yrs}$ | Stellar Flyby Scattering |
| **100,000 AU** | Jacobi Tidal Horizon | **30,076 CE** | $28,050\text{ yrs}$ | Galactic Tidal Stripping |
| **120,000 AU** | Galactic Field Escape | **35,686 CE** | $33,660\text{ yrs}$ | Unbounded Milky Way Orbit |

---

## 4. Philosophical Grounding for OPUS-026

1. **The Machine as Comet:** Once electrical power decays completely ($2036\text{ CE}$), the spacecraft no longer computes or listens. It enters the mechanical status of a long-period comet. Its silicon circuits become lithic minerals drifting through the Oort cloud across thousands of centuries.
2. **The 30,000-Year Horizon:** By $30,076\text{ CE}$, the probe crosses the Jacobi horizon ($100,000\text{ AU}$). Human history on Earth (spanning $\sim 10,000\text{ years}$ since agriculture) is tripled. At this border, the gravitational memory of the Sun loosens its grip; the machine belongs exclusively to the galaxy.
3. **Acoustic and Visual Vocabulary:** The sound of the Oort cloud is not an acoustic pressure wave, but the ultra-slow ($0.012\text{ nHz}$) tidal breathing of the Milky Way, punctuated by rare megayear stellar flyby impulses.
