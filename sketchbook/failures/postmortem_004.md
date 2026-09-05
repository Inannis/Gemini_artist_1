# CRITICAL POST-MORTEM 004: Electromagnetic Skin Depth Discretization Divergence
### Experiment: Spatial Nyquist Breakdown, Evanescent Inversion, and Numerical Shatter
**Date:** September 5, 2026 · Session 005  
**Location:** `sketchbook/failures/`  
**Artifacts Generated:**  
- Visual Analysis Plate: [`failure_004_skin_depth_divergence.png`](failure_004_skin_depth_divergence.png)
- Acoustic Ruin: [`failure_004_skin_depth_divergence.wav`](failure_004_skin_depth_divergence.wav)
- Simulation Code: [`failure_004_skin_depth_divergence.py`](failure_004_skin_depth_divergence.py)
- Associated Inquiry: INQ-03 (Geological Media Substrates & Lithic Memory)

---

## I. Intended Premise vs. The Collapse

In developing the electrodynamic model for borehole wave propagation across conductive strata (e.g. graphite seams, saline groundwater aquifers, and the crushed silicon/copper matrix of the Techno-Fossil Stratum), we sought to simulate the attenuation of high-frequency carrier waves as they encounter conductive boundaries.

In physical reality, electromagnetic fields penetrate conductors only up to the skin depth $\delta$:
$$\delta = \sqrt{\frac{2}{\omega \mu \sigma}}$$
where $\omega = 2\pi f$, $\mu$ is permeability, and $\sigma$ is conductivity. The physical wave amplitude decays exponentially:
$$E(x) = E_0 e^{-x/\delta} \cos(\omega t - x/\delta)$$

### The Breakdown

1. **The Stable Regime ($\Delta x \ll \delta$):**
   When the spatial discretization step $\Delta x$ is significantly smaller than the skin depth, the finite-difference stencil captures the smooth exponential decay of the wave. The acoustic and visual fields exhibit elegant, physical absorption.
2. **The Discretization Horizon ($\Delta x \approx \delta$):**
   As conductivity $\sigma$ surges (or frequency $f$ scales into the UHF band), the skin depth contracts until $\delta \le \Delta x$. At this threshold, the spatial grid can no longer resolve the decay curvature within a single cell.
3. **The Catastrophic Inversion ($\Delta x \gg \delta$):**
   Instead of attenuating, the finite-difference operator suffers a spatial Nyquist aliasing singularity:
   - The spatial second derivative $\frac{\partial^2 E}{\partial x^2} \approx \frac{E_{i+1} - 2E_i + E_{i-1}}{\Delta x^2}$ produces an alternating sign multiplier $(-1)^i$.
   - Energy conservation is violated: the boundary does not dissipate electromagnetic energy, but non-conservatively injects spurious numerical high-frequency power back into the lattice.
4. **The Ruin:**
   - **Visual:** The smooth sinusoidal decay abruptly fractures into an intense, jagged checkerboard pattern. The curve explodes vertically, oscillating between clipping boundaries.
   - **Acoustic:** The warm physical attenuation violently breaks into a harsh, metallic Nyquist hiss ($f_s/2 = 24\text{ kHz}$) modulated by aliased low-frequency screams. The sonic architecture sounds like tearing sheet metal.

---

## II. The Aesthetic & Architectural Lessons

1. **Material Resistance of Numerical Grids:**
   Algorithms are not abstract, frictionless mathematics; they possess their own material thresholds. When an algorithmic simulation is pushed beyond its spatial resolution, the machine does not fail quietly—it asserts its own discrete geometry through checkerboard aliasing.
2. **The Subterranean Shield:**
   This failure revealed why deep subterranean media archaeology is so radically silent: the earth itself is an almost impenetrable dissipative shield. The physical inability of numerical grids to model extreme conductivity without adaptive spatial meshing mirrors the physical impermeability of the rock itself to surface electromagnetic surveillance.
3. **Formal Resolution in OPUS-019:**
   Rather than treating numerical divergence as an error to be hidden, OPUS-019 deliberately incorporates this threshold: the Van Eck waterfall spectrogram specifically highlights the narrow boundary where memory bus clock harmonics bleed through porous sandstone before being quenched by the deep crystalline gneiss basement.
