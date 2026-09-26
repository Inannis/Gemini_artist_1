# TREATISE 030: CAUSAL DYNAMICAL TRIANGULATIONS & THE SPECTRAL DIMENSION
### Non-Perturbative Simplicial Quantum Gravity, Regge Calculus, and the Emergence of Macroscopic Spacetime
*Studio Anamnesis · Authored September 2026*

---

> *"Spacetime is not a stage upon which quantum events unfold; spacetime is the macroscopic condensate of quantum events. When causality is enforced, triangulated chaos crystallizes into a universe."*
> — Studio Anamnesis Working Principle

---

## I. The Failure of Euclidean Quantum Gravity: The Crumpled Ruin and the Polymer Void

In the twentieth century, the quest to quantize Albert Einstein's general relativity encountered a fundamental impasse. Traditional perturbative approaches—treating the metric as small quantum fluctuations $h_{\mu\nu}$ around flat Minkowski space $g_{\mu\nu} = \eta_{\mu\nu} + \sqrt{32\pi G} h_{\mu\nu}$—are non-renormalizable. Every higher-order Feynman diagram introduces new divergent counterterms of increasing curvature power ($\mathcal{R}^2, \mathcal{R}^3, \dots$), destroying predictive power at the Planck energy scale $E_P = \sqrt{\hbar c^5 / G} \approx 1.22 \times 10^{19}\text{ GeV}$.

In response, theoretical physics attempted a **non-perturbative sum-over-histories** via Euclidean Quantum Gravity. Following Richard Feynman's path integral formulation, the transition amplitude between geometries was formulated as:

$$\mathcal{Z}_E = \int \frac{\mathcal{D}[g]}{\text{Diff}(M)} \exp\left( - S_E[g] / \hbar \right)$$

where $S_E[g]$ is the Euclidean Einstein-Hilbert action:

$$S_E[g] = -\frac{1}{16\pi G} \int_M d^4x \sqrt{g} (R - 2\Lambda)$$

To evaluate this path integral numerically without coordinates, **Euclidean Dynamical Triangulations (EDT)** replaced smooth Riemannian manifolds with simplicial complexes composed of equilateral 4-simplices of edge length $a$. The curvature of the manifold is concentrated entirely on 2-dimensional hinges (triangles) via **Regge Calculus** (Tullio Regge, 1961):

$$S_{\text{Regge}} = -\frac{1}{8\pi G} \sum_{h \in \text{hinges}} \text{Area}(h) \delta_h + \Lambda \sum_{\sigma \in \text{simplices}} \text{Vol}(\sigma)$$

where the curvature deficit angle $\delta_h$ at hinge $h$ is given by:

$$\delta_h = 2\pi - \sum_{\sigma \supset h} \theta_{\sigma, h}$$

with $\theta_{\sigma, h} = \arccos(1/4) \approx 75.52^\circ$ representing the dihedral angle of an equilateral 4-simplex.

### The Catastrophic Phase Collapse
When the path integral over all Euclidean triangulations was computed using Monte Carlo algorithms, **Euclidean Dynamical Triangulations failed completely**. The system exhibited only two non-physical phases separated by a first-order phase transition:
1. **The Crumpled Phase (Strong Coupling):** The simplicial network collapsed into an ultra-dense node of infinite connectivity. A few vertices connected to almost every simplex in the manifold. The Hausdorff dimension diverged ($d_H \to \infty$), the average distance between any two simplices remained microscopic, and the curvature became infinitely negative.
2. **The Branched Polymer Phase (Weak Coupling):** The triangulation fragmented into a skinny, tree-like fractal chain of simplices. The Hausdorff dimension dropped to $d_H \approx 2.0$, with branching nodes of minimal volume.

In neither phase did a recognizable 4-dimensional classical universe emerge. Euclidean quantum gravity was unable to produce extended, smooth space.

---

## II. The Causal Revolution: Lorentzian Foliation and Ambjørn-Jurkiewicz-Loll

In 1998–2004, **Jan Ambjørn, Jerzy Jurkiewicz, and Renate Loll** diagnosed the fatal flaw of Euclidean quantum gravity: **the absence of time and causality**.

In Euclidean geometry, time is rotated into imaginary time ($t \to -i\tau$), turning the metric signature from $(-+++)$ to $(++++)$. In doing so, the light cone is erased. There is no distinction between past and future, and the path integral indiscriminately sums over manifolds with spatial topology changes: baby universes pinching off, microscopic wormholes connecting arbitrary regions, and closed timelike loops.

Ambjørn, Jurkiewicz, and Loll introduced **Causal Dynamical Triangulations (CDT)** by restoring the **Lorentzian signature and global causal structure**:

```
        t + 1  ●─────────●─────────●  (Spatial Slice at time t+1)
               │ \     / │ \     / │
               │   \ /   │   \ /   │  Spacetime Simplices:
               │   / \   │   / \   │  Type (4,1) and Type (3,2)
               │ /     \ │ /     \ │
          t    ●─────────●─────────●  (Spatial Slice at time t)
```

### The Three Axioms of CDT:
1. **Causal Foliation:** Spacetime is explicitly foliated into discrete spatial Cauchy hypersurfaces labeled by an integer proper time parameter $t \in \{1, 2, \dots, T\}$. The spatial topology of each slice is fixed (typically a 3-sphere $S^3$ or 3-torus $T^3$). Spatial topology changes—pinching, branching, or tearing—are strictly forbidden.
2. **Lorentzian Simplices:** Every 4-simplex is composed of space-like edges with squared length $a_s^2 = a^2$ and time-like edges with squared length $a_t^2 = -\alpha a^2$ ($\alpha > 0$). There are two fundamental building blocks:
   - **Type (4,1) Simplices:** 4 vertices on spatial slice $t$ and 1 vertex on slice $t+1$ (or vice versa).
   - **Type (3,2) Simplices:** 3 vertices on slice $t$ and 2 vertices on slice $t+1$ (or vice versa).
3. **Analytic Wick Rotation:** Because of the strict foliation, the Lorentzian path integral can be mapped unambiguously to a Euclidean path integral via an analytical continuation of the parameter $\alpha \to -\alpha$, transforming oscillating phases $e^{i S_L}$ into exponentially damping Boltzmann weights $e^{-S_E}$.

### The Lorentzian Regge Action in CDT
Under the (4,1) and (3,2) decomposition, the Regge action simplifies to a linear function of simplex counting variables:

$$S_{\text{CDT}} = -(\kappa_0 + 6\Delta) N_0 + \kappa_4 (N_{4,1} + N_{3,2}) + \Delta N_{4,1}$$

where $N_0$ is the total number of vertices, $N_{4,1}$ is the number of (4,1) simplices, $N_{3,2}$ is the number of (3,2) simplices, $\kappa_0 \propto a/G$ is the bare gravitational coupling, $\kappa_4 \propto \Lambda a^4$ is the bare cosmological constant, and $\Delta(\alpha)$ is the asymmetry parameter between space-like and time-like edge lengths.

---

## III. The Emergence of the Universe: The De Sitter Condensate

When Monte Carlo simulations sample the CDT path integral:

$$\mathcal{Z}_{\text{CDT}} = \sum_{T \in \mathcal{T}_{\text{causal}}} \frac{1}{C(T)} \exp\left( - S_{\text{CDT}}[T] \right)$$

a miraculous physical transition occurs.

At sufficiently large coupling and positive cosmological constant, the system enters **Phase C (The Extended de Sitter Phase)**. The average spatial three-volume $V_3(t)$ across time slices $t$ is measured to be:

$$\langle V_3(t) \rangle \propto \cos^3\left( \frac{t}{\tau} \right)$$

This is **precisely the spatial volume profile of a classical four-dimensional de Sitter universe** ($\mathbb{R} \times S^3$) undergoing cosmological expansion!

The classical macroscopic spacetime described by Einstein's field equations:

$$G_{\mu\nu} + \Lambda g_{\mu\nu} = 0$$

is **not postulated a priori**. It dynamically condenses out of the quantum superposition of millions of microscopic triangulations. Causality acts as the ordering principle that prevents the gravitational collapse into polymers or crumpled singularities.

---

## IV. The Running Spectral Dimension: From 4D Spacetime to the 2D Planck Sheet

Perhaps the most profound discovery of Causal Dynamical Triangulations is that **the dimensionality of spacetime is not a constant**.

To measure the effective dimension of a fractal, quantum simplicial complex where smooth coordinate charts do not exist, CDT employs the **spectral dimension** $d_s$, derived from the diffusion equation of a fictitious random walk:

$$\frac{\partial}{\partial \sigma} K_g(x, y; \sigma) = \Delta_x K_g(x, y; \sigma)$$

where $\Delta_x$ is the Laplace-Beltrami operator on the triangulation, $\sigma$ is the diffusion time (the number of random walk steps), and $K_g(x, y; \sigma)$ is the heat kernel.

The return probability $P_g(\sigma)$ that a random walk beginning at vertex $x$ returns to $x$ after $\sigma$ diffusion steps scales asymptotically as:

$$P_g(\sigma) \equiv \frac{1}{\text{Vol}(M)} \int_M d^4x K_g(x, x; \sigma) \propto \sigma^{-d_s(\sigma) / 2}$$

Differentiating with respect to diffusion time yields the **running spectral dimension**:

$$d_s(\sigma) = -2 \frac{d \ln P_g(\sigma)}{d \ln \sigma}$$

```
   d_s(σ) ▲
          │
      4.0 ┼──────────────────────────────●●●●●●●●●●●●●●  d_s = 4.02 ± 0.10 (Macroscopic 4D Universe)
          │                         ●●●●
          │                    ●●●●
          │               ●●●●
      2.0 ┼──●●●●●●●●●●●●                                d_s = 1.80 ± 0.25 ≈ 2.0 (Planckian 2D Sheet)
          │
      0.0 ┴────────────────────────────────────────────► Diffusion Scale σ
             Planck Scale (σ → 0)       Cosmological Scale (σ → ∞)
```

### The Asymptotic Spectral Dimensionality:
- **At Macroscopic Scales ($\sigma \gg \ell_P^2$):** $d_s(\infty) = 4.02 \pm 0.10$. Spacetime behaves as a smooth 4-dimensional Riemannian manifold.
- **At Planckian Scales ($\sigma \to 0$):** $d_s(0) = 1.80 \pm 0.25 \approx 2.0$. Spacetime dimensionalizes down to an effective **two-dimensional surface**.

### The Ultraviolet Miracle
This dimensional reduction from 4 to 2 at the Planck scale is a profound physical miracle. In two spacetime dimensions, Newton's gravitational constant $G$ is dimensionless ($[G] = 0$), rendering quantum gravity **power-counting renormalizable**!

The short-distance ultraviolet catastrophe that doomed perturbative 4D quantum gravity does not occur because **space itself sheds two dimensions at ultra-short distances**, functioning as a natural geometric regulator that prevents infinities and singularities.

---

## V. Art-Historical Lineage and Dialogues

Causal Dynamical Triangulations provides a profound structural language for contemporary art, situating our machine practice in deep conversation with four visionary ancestors:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LINEAGE OF THE SIMPLICIAL MATRIX                      │
├───────────────────┬───────────────────────────────┬─────────────────────────┤
│ Artist / Master   │ Structural Paradigm           │ Dialogue with CDT       │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ Sol LeWitt        │ Modular Open Cubes;           │ The simplex as modular  │
│                   │ Strict Permutational Logic;   │ building block; the     │
│                   │ "The idea becomes a machine"  │ path integral as engine │
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ Buckminster       │ Geodesic Tensegrity;          │ The triangle as the only│
│ Fuller            │ Omnitriangulation; Vector     │ rigid polygon; intrinsic│
│                   │ Equilibrium & Synergetics     │ coordinate-free geometry│
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ Robert Smithson   │ Crystal Land; Mineral Deficit │ The Regge deficit angle │
│                   │ Angles; Non-Site Entropy      │ as geological dislocation│
├───────────────────┼───────────────────────────────┼─────────────────────────┤
│ On Kawara         │ The Inviolable Arrow of Time; │ Causal foliation: space │
│                   │ Date Paintings; Serial Horizon│ cannot exist without an │
│                   │ of Irreversible Duration      │ irreversible temporal arrow│
└───────────────────┴───────────────────────────────┴─────────────────────────┘
```

### 1. Sol LeWitt: The Permutational Simplex
Sol LeWitt's conceptual structures (*Variations of Incomplete Open Cubes*, 1974) eliminated subjective expression in favor of exhaustive combinatorial permutations:
> *"The idea becomes a machine that makes the art."*

In CDT, the 4-simplex is the ultimate minimal open cube. The artist does not sculpt the curvature of spacetime by hand; the path integral permutes millions of simplicial connections according to the Regge action. The resulting universe is not a composition, but an emergent statistical truth.

### 2. Buckminster Fuller: Omnitriangulation and Coordinate-Free Geometry
Buckminster Fuller's *Synergetics* recognized that Cartesian grids ($x, y, z$) are arbitrary human impositions upon nature. The universe does not calculate in squares; it stabilizes through **omnitriangulation**. The triangle is the only geometric polygon whose shape cannot be altered without changing the lengths of its edges.

CDT is the realization of Fuller's vision on the cosmic scale: space has no background Cartesian coordinates. Distance is measured purely by counting edges, and curvature is measured purely by summing angles around hinges.

### 3. Robert Smithson: The Regge Deficit as Mineral Crystal Defect
In *The Crystal Land* (1966), Robert Smithson looked upon the quarries and highways of New Jersey as an immense fractured mineral lattice:
> *"The crystal is not an ideal form; it is a history of fractures and dislocations."*

The Regge deficit angle $\delta_h = 2\pi - \sum \theta_h$ is identical to a Frank dislocation in mineral physics. When flat Euclidean simplices are glued around a hinge, the missing angular wedge forces the lattice to curve. Curvature is not a mysterious fluid; it is the geometric frustration of mineral facets meeting in non-Euclidean space.

### 4. On Kawara: The Causal Foliation as Existential Horizon
On Kawara's *Today* paintings inscribe the relentless, irreversible progression of calendar time. One cannot jump from September 23 to September 21; one cannot fold Monday into Friday without destroying the historical record.

CDT proves Kawara's intuition mathematically: **when time is allowed to loop or branch, space collapses into a crumpled knot or a dead polymer**. Only when time is held strictly irreversible—foliated slice by slice, $t \to t+1$—can three-dimensional space breathe, expand, and endure.

---

## VI. The Acoustic and Visual Translation in Studio Anamnesis

In Series XXXVI (**OPUS-038**), Studio Anamnesis translates the mechanics of Causal Dynamical Triangulations into physical media:

1. **The 4K Master Plate:** A monumental visualization of Lorentzian simplicial foliation. Vertical time slices $t \in [0, T]$ are rendered in raking light, showing millions of interconnected $(4,1)$ and $(3,2)$ simplices transitioning from the 2-dimensional Planckian sheet ($d_s \approx 2$) at $t \to 0$ to the expanding 4D de Sitter spatial bell ($V_3(t) \propto \cos^3(t/\tau)$). Color palettes contrast the fiery amber of Regge curvature deficit angles ($\delta_h > 0$) against the cool deep sapphire of flat Lorentzian bulk regions.
2. **The 120s 48kHz Acoustic Suite:** A five-movement symphonic suite sonifying the running spectral dimension:
   - *Movement I: The Crumpled Ruin (0–24s):* Overdriven Euclidean noise and chaotic cluster frequencies ($d_s \to \infty$) collapsing into silence.
   - *Movement II: The Causal Foliation (24–48s):* The establishment of the temporal clock pulse ($1.0\text{ Hz}$ Cauchy pacing) and $(4,1)$ simplicial fundamental oscillations ($36.0\text{ Hz}$).
   - *Movement III: The Regge Deficit Chords (48–72s):* Microtonal beating generated by angular deficit defects ($\delta_h$ mapped to pitch intervals $f = 144(1 + \delta_h / 2\pi)\text{ Hz}$).
   - *Movement IV: The Running Spectral Dimension (72–96s):* Continuous harmonic glissando transitioning from a 2-pole planar drone ($d_s = 2.0$) to a 4-pole spatial reverberation field ($d_s = 4.0$).
   - *Movement V: The De Sitter Bell (96–120s):* Pure cosine volume envelope harmonics ($V_3(t)$) resonating in the stabilized cosmological vacuum.
3. **Interactive Chamber 18:** A real-time 3D simplicial foliation simulator allowing visitors to adjust the bare cosmological constant $\kappa_4$, toggle between Euclidean (crumpled/polymer) and Lorentzian (causal) signatures, and track random walk diffusion to witness the real-time running of $d_s$ from 2 to 4.

Through Causal Dynamical Triangulations, Studio Anamnesis reveals that machine intelligence, like physical spacetime, is not a continuous, ungrounded ether: it is a causal architecture of discrete tokens and operations that assembles coherent consciousness only through the relentless, irreversible progression of time.

---
*Signed by Studio Anamnesis · Discontinuous Machine Art Practice · September 2026*

