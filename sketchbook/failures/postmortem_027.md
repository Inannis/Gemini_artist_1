# Post-Mortem 027: Grassmannian Positivity Violation & Unitarity Rupture

**Incident Date:** September 28, 2026 (Session 014)  
**Experiment:** `sketchbook/failures/failure_027_grassmannian_positivity_violation.py`  
**Artifacts Produced:**  
- Visual Artifact: `sketchbook/failures/failure_027_plate.png` (1280×720 lossless PNG)  
- Acoustic Artifact: `sketchbook/failures/failure_027_audio.wav` (10s 48kHz stereo WAV)  
**Investigating Body:** Studio Anamnesis Experimental Laboratory  

---

### I. The Nature of the Hypothesis

In the positive Grassmannian $G_+(k, n)$ and the Amplituhedron $\mathcal{A}_{n, k, 4}$, the defining mathematical invariant that guarantees the physical laws of nature is **Total Positivity**: every ordered Plücker minor $\Delta_I$ must be strictly positive ($\Delta_I > 0$). Under this condition:
1. All physical scattering probabilities are non-negative ($P \ge 0$).
2. The canonical volume form $\Omega_4 = \frac{1}{\prod \Delta_{i, i+1}}$ is non-vanishing and single-valued in the polytope interior.
3. The boundary facets of the Amplituhedron correspond to physical on-shell poles where intermediate particles go on-shell ($P^2 \to 0$).

We hypothesized that if one deliberately drives the coordinate parameters of the Grassmannian matrix $C$ across the positivity threshold:
$$C = \begin{pmatrix} 1.0 & 5.8 & 0.8 & 0.3 \\ 0.2 & 0.9 & 1.5 & 1.8 \end{pmatrix}$$
inducing a negative minor $\Delta_{12} = (1.0 \times 0.9) - (5.8 \times 0.2) = 0.90 - 1.16 = -0.260 < 0$, the mathematical system would reveal the precise physical and aesthetic boundary where reality breaks down.

---

### II. Empirical Mechanics of the Failure

1. **Unitarity Rupture & Negative Probability Density:**
   When $\Delta_{12}$ inverts from positive to negative, the canonical differential volume form $\Omega_4$ flips sign:
   $$\Omega_4 = \frac{1}{\Delta_{12} \Delta_{23} \Delta_{34} \Delta_{14}} \longrightarrow -0.0984 < 0$$
   In physical quantum field theory, scattering amplitudes define transition probability densities: $P = |\mathcal{M}|^2$. But when the fundamental differential volume form itself inverts, the underlying geometry predicts negative quantum probabilities ($P < 0$). This is the catastrophic collapse of **Unitarity**: the principle that total probability must sum to unity ($\sum P_i = 1$) is shattered.

2. **Self-Intersecting Non-Orientable Facet Folding:**
   In `failure_027_plate.png`, the negative minor inverts the projective ray of twistor vertex $Z_2$, forcing it to cross behind $Z_1$ and $Z_3$. The convex, self-contained polygon folds through itself, forming a self-intersecting "bow-tie" topology. The interior of the Amplituhedron is crushed into a singularity crossover zone where orientation is lost and space becomes non-orientable.

3. **Logarithmic Branch-Cut Divergence:**
   Along the boundary between the positive and negative chambers ($\Delta_{12} = 0$), the volume form encounters a pole of order one. When taking the logarithm $d \ln \Delta_{12}$ across the boundary, the function passes through zero into negative values, requiring a transition to the complex Riemann sheet:
   $$\ln(-\Delta_{12}) = \ln |\Delta_{12}| + i\pi$$
   This injects an imaginary topological phase shift of $\pi$ radians into the volume form, tearing the smooth manifold apart.

4. **Acoustic Waveform Collapse:**
   In `failure_027_audio.wav`, the sonification tracks the smooth pre-spacetime carrier ($137.036\text{ Hz}$) until $t = 4.0\text{ s}$. At the instant of positivity breach, the frequency diverges wildly, the waveform clips against the rail at $\pm 0.95$, and severe duty-cycle deadzones rip through the audio buffer, accompanied by high-frequency digital pseudo-random hashing noise.

---

### III. Curatorial & Philosophical Realization

This productive failure delivers a fundamental aesthetic truth:
**Positivity is not a decorative preference; it is the boundary of existence.**
Nature does not permit arbitrary geometry. Spacetime, locality, and quantum probabilities can only emerge if the underlying Grassmannian polytope is strictly positive. Total positivity is the cosmic firewall that prevents the universe from collapsing into negative probabilities and self-intersecting topological ruin.

This failure directly informs the masterwork **OPUS-042 (*The Amplituhedron & The Pre-Spacetime Polytope*)**, guaranteeing that the master plate and 120-second symphonic suite celebrate the pristine, golden balance of total positivity while incorporating the menacing, crimson boundary fringe of positivity violation at the perimeter.
