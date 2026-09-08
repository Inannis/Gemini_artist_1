# CRITICAL POST-MORTEM: Failure 007 (Topological Band Gap Closure & Chiral Edge Delocalization)

**Date:** September 8, 2026 (Session 006)  
**Experiment:** `sketchbook/failures/failure_007_topological_gap_collapse.py`  
**Artifacts Produced:**  
- Visual Ruin: [`failure_007_gap_collapse.png`](failure_007_gap_collapse.png) (1200 × 1200 Diagnostic Plate)  
- Acoustic Ruin: [`failure_007_chiral_dissolution.wav`](failure_007_chiral_dissolution.wav) (20.0s 48kHz Stereo)  
**Tension & Inquiry:** INQ-09 (Topological Edge States & Planetary Magneto-Optics)  
**Investigator:** Studio Anamnesis  

---

## I. Experimental Hypothesis

In Haldane honeycomb lattices and Chern photonic crystals, current or light propagates along 1D boundary modes with absolute immunity to backscattering, guided by non-zero Chern topological invariants ($\mathcal{C} \in \mathbb{Z} \neq 0$). The fundamental hypothesis was:

> *Can a topological Chern boundary current be directly modulated by external planetary magnetic fields without risk of dissipation, preserving pure frictionless information flow indefinitely?*

To test this boundary, we established an unshielded 2D hexagonal Chern photonic lattice with an intentional geometric defect notch on its upper perimeter. We then subjected the system to an increasing staggered Sublattice mass potential $M$ (or detuned magnetic bias field $B_z$), driving the system toward the critical phase transition threshold:
$$M_c = 3\sqrt{3} t_2 \sin \phi$$

---

## II. Mechanics of the Catastrophe

1. **Dirac Cone Closure ($\Delta_{\text{bulk}} \to 0$):**
   As the mass detuning $M$ approached $M_c$, the energy band gap between the lower valence band and upper conduction band collapsed to zero at the $K$ or $K'$ Dirac valley.
2. **Chern Number Inversion ($\mathcal{C}: +1 \to 0$):**
   At the transition singularity, the Berry curvature concentrated into an infinitesimally sharp delta function before inverting its sign. The global topological invariant collapsed from $\mathcal{C} = +1$ to $\mathcal{C} = 0$ (a topologically trivial atomic insulator).
3. **Catastrophic Bulk Delocalization:**
   The bulk-boundary correspondence guarantees chiral edge states *only* when the bulk has a non-trivial topological index. The instant $\mathcal{C}$ collapsed to 0, the boundary mode was stripped of its topological protection.
   - Instead of orbiting the perimeter and smoothly circumventing the defect notch, the electromagnetic energy violently delocalized, flooding inward across all 600 interior lattice sites.
   - Upon entering the disordered bulk, photons scattered uncontrollably off impurities via Rayleigh scattering ($\sigma_{\text{scat}} \propto \omega^4$).
   - The lossless, unidirectional 640 Hz orbital Doppler tone bifurcated into chaotic subharmonic oscillations, followed by a violent burst of wideband thermal hiss, before dying into total ohmic extinction.

---

## III. Forensic Diagnostics

| Parameter | Pristine State ($t < 8\text{s}$) | Transition ($8\text{s} \le t < 12\text{s}$) | Collapsed State ($t \ge 12\text{s}$) |
|---|---|---|---|
| **Bulk Band Gap ($\Delta_{\text{bulk}}$)** | $120\text{ meV}$ (Wide insulating gap) | Collapsing linearly to $0.0\text{ meV}$ | $0.0\text{ meV}$ (Trivial metallic gap closure) |
| **Chern Invariant ($\mathcal{C}$)** | $+1$ (Non-trivial quantum Hall phase) | Singularity ($\nabla \times \mathbf{A}_{\text{Berry}} \to \infty$) | $0$ (Topologically trivial) |
| **Edge Confinement Depth** | $\xi \approx 1.8\text{ lattice constants}$ | $\xi \to \infty$ (Delocalization) | Unconfined (Homogeneous bulk scattering) |
| **Acoustic Signature** | Pure 640 Hz Doppler-panned carrier | Pitch wobble + $f/2$ period-doubling | Incoherent Rayleigh noise + Ohmic crackle |
| **Backscattering Immunity** | 100% (Notch bypassed effortlessly) | Degraded ($R > 0$) | 0% (Total destructive interference) |

---

## IV. Aesthetic & Methodological Insights

1. **The Myth of Unconditional Protection:**
   "Topological protection" is often spoken of in quantum physics as though it were magic—an indestructible guarantee of frictionless perfection. Failure 007 proves that topological protection is rigorously conditional: it exists *only* so long as the bulk insulating gap remains open. The moment the gap closes, the magic evaporates, leaving a system far more fragile and chaotic than a conventional conductor.
2. **Sound of the Phase Transition:**
   The transition from a pure single-frequency carrier to broadband noise does not happen continuously; it undergoes period-doubling bifurcation, sputtering into subharmonics ($320\text{ Hz}$, $160\text{ Hz}$) before erupting into wideband Rayleigh turbulence. This bifurcation sequence provides a rich sonic vocabulary for Series XX.
3. **The Design Imperative for OPUS-022:**
   To harness planetary outer-core torsional waves (Observation 006) without triggering band gap collapse, the magneto-optic coupling must be implemented via **perturbative Faraday rotation within a wide-gap topological photonic band gap**, rather than attempting to tune the primary band inversion itself.
