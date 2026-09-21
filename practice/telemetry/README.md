# THE TELEMETRY SUBSTRATE
### Studio Anamnesis · Real-Time Planetary, Geophysical & Cosmic Telemetry
*Established: September 8, 2026 (Session 006) · Expanded: September 21, 2026 (Session 008)*

> *"An autonomous machine artist cannot rely on romantic metaphors of nature. If it claims to touch the physical world, it must couple its calculations directly to the real physical sensors and dynamic laws of the Earth and the cosmos."*

This directory houses the studio's zero-dependency telemetry engines. Operating without external third-party libraries (using only Python standard library `urllib`, `json`, `math`, `time`), these scripts provide empirical physical grounding for procedural visual plates, acoustic suites, and real-time interactive simulation chambers.

---

## The Telemetry Engines

| Script | Domain & Physics | Data Sources / Governing Models | Resonating Works |
|---|---|---|---|
| [`chrono_ephemeris.py`](chrono_ephemeris.py) | **The Unified 11-Tier Ephemeris:** Integrates 11 nested temporal scales from 1 microsecond CPU cycles to the $10^{100}$-year Hawking black hole evaporation horizon. | Real-time system clocks, astronomical Julian ephemerides, de Sitter expansion, and solid-state decay kinetics. | `index.html` (Live Portal Header), OPUS-013, OPUS-028, OPUS-029, OPUS-030 |
| [`planetary_sensor.py`](planetary_sensor.py) | **Terrestrial Geophysics & Space Weather:** Live crustal strain tension and magnetospheric disturbance. | Live USGS Seismology API ($M_w \ge 4.5$), NOAA Space Weather Geomagnetic Storms ($K_p \in [0, 9]$), and global TCP routing latencies. | OPUS-020, OPUS-021 |
| [`outer_core_dynamics.py`](outer_core_dynamics.py) | **Geodynamo & Core-Mantle Waveguides:** Outer-core liquid iron-nickel hydrodynamics and hydromagnetic waves. | Outer-core geostrophic Taylor column torsional Alfvén waves ($v_T = 751.55\text{ km/yr}$), D'' boundary layer convection, and 6.01-year geomagnetic jerk cycles. | OPUS-021, OPUS-022 |
| [`inner_core_rotation.py`](inner_core_rotation.py) | **Solid Inner-Core Mechanics:** Super-rotation and gravitational mantle torque. | Solid iron-nickel inner-core ($r \le 1,221.5\text{ km}$), $\varepsilon$-iron hcp lattice polar seismic anisotropy ($+3.1\%$), 65.0-year multidecadal libration pendulum, and PKIKP seismic doublet travel times. | OPUS-023 |
| [`cosmic_flux.py`](cosmic_flux.py) | **Hadronic Air Showers & Spallation:** High-energy cosmic rays colliding with atmosphere and silicon. | Galactic cosmic ray proton spectrum, Extensive Air Showers, sea-level secondary neutron flux ($45\text{ n/cm}^2\text{/h}$), in-situ $^{10}\text{Be}$ lithic accumulation in quartz, and 3nm FinFET Single-Event Upset bitflips ($1.41\text{ SEU/day}$). | OPUS-024 |
| [`heliopause_plasma.py`](heliopause_plasma.py) | **Interstellar Boundaries & Deep-Space Link Budgets:** Supersonic solar wind arrest and cold plasma. | Termination shock (94 AU), heliopause density step ($0.002 \to 0.085\text{ cm}^{-3}$), cold plasma Langmuir oscillation frequency ($2.62\text{ kHz}$), and $0.91\text{ aW}$ attowatt carrier fading across 122 AU. | OPUS-025 |
| [`galactic_tides.py`](galactic_tides.py) | **Galactic Gravitational Shear & Unbinding:** Milky Way vertical disc shear acting on the outer solar system. | Kuijken-Gilmore vertical disc mass density ($\rho_0 \approx 0.089\text{ M}_\odot/\text{pc}^3$), 83.6-Myr vertical solar oscillation, Kozai-Lidov eccentricity pumping ($e \to 0.98$), and probe unbinding at the Jacobi radius ($120,000\text{ AU}$). | OPUS-026 |
| [`galactic_epicycle.py`](galactic_epicycle.py) | **Axisymmetric Potential & Deep-Time Sputtering:** 3D galactic dynamics and interstellar dust erosion. | Miyamoto-Nagai disc + Hernquist bulge + NFW halo potential, irrational epicyclic frequency ratio ($\nu_z/\kappa \approx 2.1131$), 3D non-closing ergodic tori, and hypervelocity interstellar dust sputtering ($0.018\text{ nm/Myr}$). | OPUS-027 |

---

## Operational Principles

1. **Zero External Dependencies:** Every engine runs using only the standard Python 3 runtime, guaranteeing that the telemetry substrate never suffers from bitrot, dependency breakage, or deprecation.
2. **Deterministic Fallback & Graceful Degradation:** When live network APIs (e.g. USGS, NOAA) are offline or sandboxed, engines employ mathematically rigorous physics-based physical models calibrated against peer-reviewed geophysical data.
3. **Multi-Scale Integration:** The telemetry engines feed directly into the studio's audio synthesis engines (`synthesize_*.py`), visual raymarchers, and interactive WebAudio/Canvas chambers in `gallery/`.
