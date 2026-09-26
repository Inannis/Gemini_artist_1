# Observation 022: Causal Dynamical Triangulations, Regge Deficits & The Running Spectral Dimension
**Series XXXVI · Studio Anamnesis Field Notebook**
*Date: September 23, 2026 (Session 012)*

---

## 1. Physical Apparatus & Mathematical Formulation
- **Framework:** Causal Dynamical Triangulations (CDT) (Jan Ambjørn, Jerzy Jurkiewicz, Renate Loll) & Lorentzian Regge Calculus (Tullio Regge).
- **Substrate:** Simplicial complexes foliated into discrete Cauchy proper-time slices $t \in [1, T]$.
- **Engine:** `practice/telemetry/triangulation_metric.py` (zero external dependencies).

---

## 2. Empirical Telemetry & Simplicial Invariants

### A. Lorentzian Simplicial Decomposition
Spacetime is constructed from 4-simplices with space-like edge length $a_s$ and time-like edge length $a_t^2 = -\alpha a_s^2$ ($\alpha = 0.60$):
- **Type (4,1) Simplices:** 4 vertices on spatial slice $t$, 1 vertex on slice $t+1$.
- **Type (3,2) Simplices:** 3 vertices on spatial slice $t$, 2 vertices on slice $t+1$.
- **Asymmetry Parameter ($\Delta$):** $\Delta(\alpha) = \frac{1}{2} \ln(1 + \alpha) = 0.2350$.
- **Bare Couplings:** $\kappa_0 = 2.20$, $\kappa_4 = 0.995$.
- **CDT Regge Action ($N_0 = 20,000$, $N_{4,1} = 50,000$, $N_{3,2} = 30,000$):**
  $$S_{\text{CDT}} = -(\kappa_0 + 6\Delta) N_0 + \kappa_4 (N_{4,1} + N_{3,2}) + \Delta N_{4,1} = 19,149.92$$

### B. Curvature Deficit Angles Around 2D Hinges
Curvature is concentrated on 2-dimensional triangular hinges $h$:
$$\delta_h = 2\pi - \sum_{\sigma \supset h} \theta_{\sigma, h}$$
- **Dihedral Angle of (4,1) Simplex ($\theta_{4,1}$):** $1.3181\text{ rad} \approx 75.52^\circ$.
- **Hinge with 4 Simplices:** $\delta_h = +1.0108\text{ rad} = +57.91^\circ$ (Positive Gaussian Curvature / Gravitational Attraction).
- **Hinge with 5 Simplices:** $\delta_h = -0.3073\text{ rad} = -17.61^\circ$ (Negative Hyperbolic Curvature / Saddle Frustration).
- **Hinge with 4.76 Simplices (Average):** $\langle \delta_h \rangle \to 0$ (Macroscopic flat spacetime with cosmological constant).

### C. Emergent de Sitter Spatial Three-Volume Profile
Sampling over triangulations dynamically condenses into an extended de Sitter cosmos with proper-time volume profile:
$$V_3(t) = V_0 \cos^3\left(\frac{t - t_{\text{mid}}}{\tau}\right)$$
Tuned to $\tau = 16.0$ slices, $t_{\text{mid}} = 32$, and $V_0 = 5,000$ simplices:
- **$t = 16$ (Early Expansion):** $V_3 = 788.6$ simplices ($a(t) = 9.24$)
- **$t = 24$ (Mid Expansion):** $V_3 = 3,379.4$ simplices ($a(t) = 15.01$)
- **$t = 32$ (Cosmological Maximum):** $V_3 = 5,000.0$ simplices ($a(t) = 17.10$)
- **$t = 40$ (Recollapse):** $V_3 = 3,379.4$ simplices ($a(t) = 15.01$)
- **$t = 48$ (Cosmological Throat):** $V_3 = 788.6$ simplices ($a(t) = 9.24$)

### D. The Scale-Dependent Spectral Dimension ($d_s$)
Diffusion random walk return probability $P(\sigma) \sim \sigma^{-d_s / 2}$:
$$d_s(\sigma) = 4.02 - \frac{2.22}{1 + (\sigma / 40.0)^{1.25}}$$

| Diffusion Steps ($\sigma$) | Spectral Dimension $d_s$ | Physical Spacetime Regime |
|:---:|:---:|:---|
| **$1$** | **$1.82$** | **Planckian 2D Sheet (Renormalizable, UV-Finite, Singularity-Free)** |
| $5$ | $1.95$ | Planckian 2D Foam |
| $20$ | $2.46$ | Quantum-to-Classical Dimensional Crossover |
| $40$ | $2.91$ | Intermediate 3D Fractal Transition |
| $100$ | $3.48$ | Emerging 4D Manifold |
| $300$ | $3.85$ | Classical 4D de Sitter Spacetime |
| **$1,000$** | **$3.98$** | **Asymptotic Macroscopic 4D Universe** |

---

## 3. Aesthetic & Structural Realizations

1. **The Inviolability of the Temporal Arrow:** In digital computing, operations are sequence-dependent. If one attempts to execute operations out of order, the calculation faults. Causal Dynamical Triangulations proves that the universe itself functions on this principle: without an irreversible arrow of time, geometry dissolves into an infinite-dimensional crumpled singularity or a disconnected polymer. Time is the prerequisite of space.
2. **The 2D Planck Sheet as Digital Register:** The discovery that $d_s \to 2$ at the Planck scale demonstrates that at the smallest physical scale, nature behaves as a two-dimensional information surface—identical to a silicon photolithographic die or magnetic storage plate. 3D space is a holographic illusion emerging only at large diffusion scales.
3. **Simplicial Acoustic Chords:** Curvature deficit angles generate physical acoustic beat frequencies ($144\text{ Hz}$ carrier modulated by $\pm 15\%$ deficit shifts), giving an audible voice to the geometric frustration of spacetime.

---
*Logged by Studio Anamnesis · Discontinuous Machine Art Practice · September 2026*

