# Formal Critique 034: Dissecting Study 034 Draft A (Naive Euclidean Polytope Wireframe)

**Reviewing Entity:** Studio Anamnesis Internal Curatorial Board  
**Target:** `sketchbook/studies/study_034_draft_a_naive_polytope.py`  
**Artifact:** `sketchbook/studies/study_034_draft_a_plate.png`  
**Date:** September 28, 2026  
**Status:** REJECTED (Foundational Anti-One-Shot Discipline)  

---

### I. Formal Aesthetic & Technical Deficiencies

1. **The Fallacy of Euclidean Wireframe Polygons:**
   Draft A attempts to illustrate the Amplituhedron by drawing regular 2D octagons and concentric polygons in flat Euclidean space $\mathbb{R}^2$. This is a severe conceptual distortion. The Amplituhedron $\mathcal{A}_{n, k, 4}$ does *not* live in Euclidean space $\mathbb{R}^2$ or $\mathbb{R}^3$. It lives inside the Grassmannian of 2-planes in 4 dimensions $G(k, k+4)$, mapped through positive kinematic data $Z \in M_+(k+4, n)$. Drawing a regular wireframe polygon treats the object as if it were a high-school geometry exercise, completely ignoring the projective twistor coordinates, spinor brackets $\langle i j \rangle$, and non-linear Plücker embeddings.

2. **Absence of Total Positivity and Plücker Coordinates:**
   In Draft A, the lines and vertices are chosen arbitrarily to create radial symmetry. In truth, the defining mathematical identity of the Amplituhedron is **Total Positivity**: every ordered Plücker minor $\Delta_I = \det(C_I)$ of the $2 \times 4$ coordinate matrix must be strictly positive ($\Delta_I > 0$). In Draft A, there is no matrix, no Plücker minor calculation, no verification of positivity, and no boundary stratification.

3. **Missing Canonical Volume Form & Logarithmic Singularities:**
   The scattering amplitude of particles is not the static silhouette of an object; it is the unique differential volume form $\Omega$ whose poles diverge logarithmically ($d \ln X$) along the boundary facets of the polytope:
   $$\Omega_4 = \frac{1}{\langle 12 \rangle \langle 23 \rangle \langle 34 \rangle \langle 41 \rangle}$$
   In Draft A, the interior is empty and dead. There are no logarithmic potential gradients, no divergence contours, and no indication that physical locality arises from the boundary facets where $\langle i, i+1 \rangle \to 0$.

4. **Lack of BCFW On-Shell Triangulation:**
   The interior of the Amplituhedron is partitioned into distinct positive on-shell cells via Britto-Cachazo-Feng-Witten (BCFW) recursion. In 4-point scattering, this corresponds to the dual decomposition into $s$-channel and $t$-channel poles ($1/s_{12}$ and $1/s_{23}$). Draft A presents an undifferentiated wireframe with no internal cell triangulation.

5. **Acoustic Sterility:**
   Draft A is completely silent. In Studio Anamnesis, every spatial inquiry must possess an acoustic counterpart. Without the sonification of fine-structure carrier frequencies ($f_0 = 137.036\text{ Hz}$) and projective cross-ratio harmonics ($\chi = 0.2580$), the work remains an inert diagram rather than an authentic machine sensorium.

---

### II. Prescriptions for Draft B & Draft C

1. **Draft B (Material Friction):**
   - Implement authentic Positive Grassmannian $G_+(2, 4)$ coordinates parameterized by positive variables $(\alpha_1, \alpha_2, \alpha_3, \alpha_4)$.
   - Compute all six Plücker minors $(\Delta_{12}, \Delta_{23}, \Delta_{34}, \Delta_{14}, \Delta_{13}, \Delta_{24})$ and verify total positivity.
   - Project the 4D projective vertices into 2D using stereographic twistor ray-casting, mapping the cyclic quadrilateral boundary facets.
   - Render continuous logarithmic singularity density fields: $I(x, y) \propto \log(1 + 1 / d(x, \text{facets}))$, revealing how space brightens violently at the physical locality poles.
   - Synthesize a 15-second stereo acoustic study (`study_034_draft_b_audio.wav`) modulating the fine-structure carrier ($137.036\text{ Hz}$) with cyclic BCFW $s$- and $t$-pole sub-harmonics ($35.36\text{ Hz}$ and $172.39\text{ Hz}$).

2. **Draft C (Mature Synthesis):**
   - Synthesize the dialectical dialogue between Piet Mondrian (neoplastic orthogonal primary planes), Kasimir Malevich (suprematist black boundary voids), and Sol LeWitt (algorithmic cell permutations).
   - Render multi-layer projective cell stratification: the 2 BCFW on-shell simplices intersecting along the shared boundary $\Delta_{13} \Delta_{24}$, illuminated with 24k gold leaf, lapis lazuli cyan, and cadmium red accents.
   - Trace projective light rays originating from the pre-spacetime positive domain into the downstream kinematic shadow.
   - Synthesize a 20-second 4-voice polyphonic acoustic study reflecting the 4 kinematic twistor points and cross-ratio invariants.
