# POST-MORTEM 012: EPICYCLIC RESONANCE MODE-LOCKING & TORUS COLLAPSE

**Date:** September 8, 2026 (Session 006)  
**Experiment:** `sketchbook/failures/failure_012_epicyclic_resonance_torus_collapse.py`  
**Artifacts:** `failure_012_resonance_collapse.png` (1200 × 1200 visual plate), `failure_012_mode_lock_shriek.wav` (20.0s 48kHz stereo acoustic ruin)  
**Inquiry Reference:** INQ-13 (*The Galactic Epicycle, Dust Sputtering & Incommensurate Orbits*)

---

## 1. Experimental Hypothesis

In Series XXV, we investigated the multi-gigayear trajectory of an unbound spacecraft orbiting within the galactic potential of the Milky Way. We hypothesized that numerical integration could be made computationally stable and visually repeatable by forcing the vertical and radial epicyclic frequencies into an exact rational harmonic resonance ($2:1$, setting $\nu_z / \kappa \equiv 2.0000$ rather than the natural irrational value $2.1131...$).

---

## 2. The Catastrophic Failure Mechanism

1. **Destruction of the Ergodic Torus:** In nature, the irrational ratio $\nu_z / \kappa \approx 2.1131$ ensures that orbits never close, smoothly and stably filling a 3D toroidal volume over billions of years without resonant accumulation.
2. **Parametric Instability & Mode Locking:** Forcing an exact $2:1$ frequency commensurability creates a non-linear Mathieu-type parametric resonance. The vertical oscillation component $z^2(t)$ acts as a periodic driver at frequency $2\nu_z = 4\kappa$, which couples directly into the radial epicyclic equation:
   $$\ddot{R} + \kappa^2 (R - R_0) \propto z^2$$
3. **Resonant Eccentricity Divergence:** Orbital energy rapidly drains from the vertical degree of freedom into radial motion. Within three galactic rotations, radial excursions explode from $\Delta R \approx \pm 0.4\text{ kpc}$ to $|R - R_0| > 25\text{ kpc}$. The simulated spacecraft is hurled out of the galactic disc into intergalactic space.
4. **Visual Ruin (`failure_012_resonance_collapse.png`):** The clean, concentric blue phase curves abruptly deform into jagged, orange-and-crimson shockfronts tearing across the coordinate axes.
5. **Acoustic Ruin (`failure_012_mode_lock_shriek.wav`):** The stable $36\text{ Hz} / 72\text{ Hz}$ harmonic interval destabilizes into an ascending parametric screech that distorts, cross-modulates, and blows out into clipped noise.

---

## 3. Aesthetic Insight & Elevation to Masterwork OPUS-027

- **The Sublime Necessity of Irrationality:** Irrational numbers are not imperfections; they are the dynamical glue that stabilizes galactic discs. If galactic frequencies were rational harmonics, celestial systems would tear themselves apart through parametric resonance.
- **The True Shape of Deep-Time Drift:** In OPUS-027 (*The Lissajous Reliquary*), we embrace the authentic irrational frequency ratio $\nu_z / \kappa = 2.1131$. The artwork will present an open, infinite, non-repeating Lissajous tapestry—a majestic visual and acoustic testament to the incommensurate geometry of the Milky Way.
