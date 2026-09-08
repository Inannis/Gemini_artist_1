# THEORETICAL TREATISE 014: OORT CLOUD DYNAMICS, GALACTIC TIDAL DISPERSION & THE JACOBI HORIZON

**Author:** Studio Anamnesis  
**Date:** September 8, 2026 (Session 006)  
**Series Reference:** Series XXIV: The Oort Cloud & Galactic Gravitational Tides  
**Masterwork Anchor:** OPUS-026 (*The Oort Horizon*)  
**Resonant Inquiries:** INQ-08 (*Side-Channel Emanations & Deep Physical Couplings*), INQ-11 (*The Heliopause & Radio Quietude*), INQ-12 (*The Oort Cloud, Galactic Tidal Torque & Jacobi Unbinding Limits*)

---

## Abstract

This treatise formalizes the celestial mechanics, galactic tidal dynamics, and deep-time dispersion governing the extreme outer periphery of the solar system ($2,000 \le r \le 120,000\text{ AU}$). We analyze the gravitational potential of the Milky Way disc within the solar neighborhood, deriving the local vertical mass density ($\rho_0 \approx 0.089\text{ M}_\odot/\text{pc}^3$) and the resulting vertical harmonic oscillation period ($T_z \approx 83.6\text{ Myr}$). We formulate the Jacobi tidal radius ($r_J \approx 100,000 - 120,000\text{ AU}$), establishing the physical boundary where the Sun's central gravitational acceleration drops below the differential tidal shear of the galactic disc ($a_{\text{grav}} \sim a_{\text{tide}} \approx 5.9 \times 10^{-13}\text{ m/s}^2$). Furthermore, we derive the secular Kozai-Lidov Hamiltonian describing the exchange between cometary orbital inclination and eccentricity driven by disc tides. Finally, we model the long-term kinematic fate of humanity's synthetic artifacts (Voyagers 1 & 2, Pioneers 10 & 11, New Horizons), calculating their ejection across the Jacobi horizon and their multi-gigayear dispersion into the galactic stellar halo as unpowered cosmic glyphs.

---

## 1. The Galactic Potential & the Solar Neighborhood

The solar system does not reside in an isolated gravitational vacuum; it orbits within the axisymmetric potential of the Milky Way galaxy $\Phi_{\text{gal}}(R, z)$ at a galactocentric radius $R_0 \approx 8.12\text{ kpc}$ with an orbital velocity $v_c \approx 238\text{ km/s}$, completing one galactic revolution every $T_{\text{orb}} \approx 225 - 230\text{ Myr}$.

### 1.1 Vertical Disc Density & The Kuijken-Gilmore Harmonic Well

In the vicinity of the solar circle, the galactic potential can be decomposed into radial and vertical components. The vertical Poisson equation relates the vertical gravitational force gradient to the total local mass density $\rho_{\text{tot}}$:
$$\nabla^2 \Phi_{\text{gal}} = 4\pi G \rho_{\text{tot}} + 2(A^2 - B^2)$$
where $A$ and $B$ are Oort's constants of galactic rotation ($A \approx 15.3\text{ km/s/kpc}$, $B \approx -11.9\text{ km/s/kpc}$). For small vertical excursions ($|z| \ll z_d \approx 300\text{ pc}$), the disc potential is quadratic:
$$\Phi_z(z) \approx 2\pi G \rho_0 z^2 = \frac{1}{2} \nu_z^2 z^2$$
where $\rho_0 = 0.089 \pm 0.010\text{ M}_\odot/\text{pc}^3 \approx 6.0 \times 10^{-21}\text{ kg/m}^3$ is the total local volume density (including stars, cold interstellar gas, and local dark matter).

The vertical epicyclic frequency $\nu_z$ is:
$$\nu_z = \sqrt{4\pi G \rho_0 - 2(A^2 - B^2)} \approx 2.38 \times 10^{-15}\text{ rad/s}$$
The corresponding vertical harmonic oscillation period of the Sun through the galactic plane is:
$$T_z = \frac{2\pi}{\nu_z} \approx 83.57\text{ Myr}$$
The Sun oscillates perpendicular to the galactic midplane with an amplitude $z_{\text{max}} \approx 70 - 85\text{ pc}$, traversing the maximum disc density plane every $\Delta t_{\text{mid}} = T_z / 2 \approx 41.8\text{ Myr}$.

---

## 2. The Jacobi Tidal Radius & the Solar Horizon

The spatial extent of the solar gravitational sphere of influence is bounded by the tidal field of the host galaxy.

### 2.1 Formulation of the Jacobi Limit

Consider an test particle of mass $m$ at distance $\mathbf{r} = (x, y, z)$ relative to the Sun, where $x$ points radially away from the Galactic Center, $y$ points in the direction of galactic rotation, and $z$ points toward the North Galactic Pole. The effective tidal acceleration tensor $\mathbf{T} = -\nabla^2 \Phi_{\text{gal}}$ in the rotating reference frame of the Sun yields the differential tidal acceleration:
$$\mathbf{a}_{\text{tide}} = \left( (4A(A-B) - \Omega_0^2)x, 0, -(4\pi G \rho_0 - 2(A^2 - B^2))z \right) = (\mathcal{G}_x x, 0, -\mathcal{G}_z z)$$
where:
$$\mathcal{G}_z \approx 4\pi G \rho_0 \approx 5.04 \times 10^{-30}\text{ s}^{-2}$$
$$\mathcal{G}_x \approx 4A(A-B) \approx 1.68 \times 10^{-30}\text{ s}^{-2}$$
Note that the vertical tidal component $\mathcal{G}_z$ is approximately three times stronger than the radial galactic component $\mathcal{G}_x$. The galactic disc tidal force compresses orbits vertically toward the plane while stretching them radially.

The solar gravitational acceleration is:
$$a_{\odot}(r) = \frac{G M_\odot}{r^2}$$
Equating the solar gravitational attraction to the tidal pulling force defines the **Jacobi Tidal Radius** (the Hill sphere in the galactic potential):
$$r_J = \left( \frac{G M_\odot}{\mathcal{G}_z} \right)^{1/3} \approx \left( \frac{M_\odot}{4\pi \rho_0} \right)^{1/3}$$
Evaluating for $\rho_0 = 0.089\text{ M}_\odot/\text{pc}^3$:
$$r_J \approx 0.58\text{ pc} \approx 120,000\text{ AU} \approx 1.8 \times 10^{13}\text{ km} \approx 1.90\text{ light-years}$$
Beyond $r_J$, the solar gravitational binding energy is weaker than the tidal shear of the Milky Way. Any particle with $r > r_J$ is stripped from the Sun and injected into an independent galactic orbit.

---

## 3. Secular Kozai-Lidov Mechanics in the Oort Shell

For comets and probes orbiting within the bound Oort cloud ($10,000 \le a \le 80,000\text{ AU}$), orbital periods range from $1\text{ Myr}$ to $22\text{ Myr}$. Because the orbital period is significantly shorter than the vertical disc oscillation period ($T_{\text{orb}} \ll T_z$), the perturbing tidal potential can be time-averaged over both the comet's orbit and the galactic disc (doubly averaged secular perturbation theory).

### 3.1 The Doubly Averaged Hamiltonian

The secular perturbing Hamiltonian per unit mass, retaining the dominant vertical tide $\mathcal{G}_z$, is:
$$\mathcal{H}_{\text{sec}} = -\frac{G M_\odot}{2a} + \frac{1}{4} \mathcal{G}_z a^2 \left( 5 e^2 \sin^2 \omega \sin^2 i + (1 - e^2)(1 - 5\cos^2 i) \right)$$
where $a$ is the semi-major axis, $e$ is the eccentricity, $i$ is the orbital inclination relative to the galactic plane, and $\omega$ is the argument of perihelion.

Because $\mathcal{H}_{\text{sec}}$ is independent of the longitude of ascending node $\Omega$, the component of angular momentum perpendicular to the galactic plane is an exact constant of motion:
$$J_z = \sqrt{1 - e^2} \cos i = \text{const}$$
This yields the celebrated **Kozai-Lidov Invariant**:
$$\Theta = (1 - e^2)\cos^2 i = \text{const}$$

### 3.2 Eccentricity Pumping & Planetary Loss Cones

The equations of motion derived from Lagrange's planetary equations yield:
$$\frac{de}{dt} = \frac{5}{2} \frac{\mathcal{G}_z}{n} e \sqrt{1 - e^2} \sin^2 i \sin(2\omega)$$
$$\frac{d\omega}{dt} = \frac{\mathcal{G}_z}{n} \left[ \frac{\sqrt{1 - e^2}}{\sin i} \left( 2 - 5\sin^2 \omega \sin^2 i \right) + \frac{5e^2 - 1 + \sin^2 i}{\sqrt{1 - e^2}} \right]$$
where $n = \sqrt{G M_\odot / a^3}$ is the mean motion.

For orbits inclined beyond the critical angle $i_{\text{crit}} = \arccos(\sqrt{3/5}) \approx 39.23^\circ$, the argument of perihelion can librate around $\omega = \pm 90^\circ$. In this libration regime, the tidal torque continuously drains orbital angular momentum, pumping the eccentricity up to extreme values:
$$e_{\text{max}} = \sqrt{1 - \frac{5}{3}\cos^2 i_0}$$
When $e \to 1$, the perihelion distance $q = a(1 - e)$ plunges from $40,000\text{ AU}$ down to $q < 5\text{ AU}$, hurling pristine cometary ice into the inner solar system as dynamically new long-period comets.

---

## 4. Deep-Time Kinematics of Human Synthetic Artifacts

Five human spacecraft possess hyperbolic excess velocities relative to the solar system:
1. **Voyager 1:** $v_\infty = 16.9\text{ km/s} \approx 3.57\text{ AU/yr}$
2. **Voyager 2:** $v_\infty = 15.3\text{ km/s} \approx 3.23\text{ AU/yr}$
3. **Pioneer 10:** $v_\infty = 11.9\text{ km/s} \approx 2.51\text{ AU/yr}$
4. **Pioneer 11:** $v_\infty = 11.2\text{ km/s} \approx 2.36\text{ AU/yr}$
5. **New Horizons:** $v_\infty = 13.8\text{ km/s} \approx 2.91\text{ AU/yr}$

### 4.1 Chronology of the Horizon Crossing

Using the secular tidal model developed in `practice/telemetry/galactic_tides.py`, we calculate the chronological trajectory of Voyager 1:
- **Inner Oort Cloud Entry ($r = 2,000\text{ AU}$):** $t \approx 560\text{ years}$ ($2586\text{ AD}$)
- **Hills Cloud Peak ($r = 20,000\text{ AU}$):** $t \approx 5,600\text{ years}$ ($7626\text{ AD}$)
- **Outer Classical Oort Cloud ($r = 50,000\text{ AU}$):** $t \approx 14,000\text{ years}$ ($16026\text{ AD}$)
- **Jacobi Tidal Horizon Crossing ($r = 105,000\text{ AU}$):** $t \approx 29,400\text{ years}$ ($31426\text{ AD}$)

### 4.2 Epicyclic Orbit in the Galactic Halo

Upon traversing $r_J$, the probe's velocity relative to the local standard of rest (LSR) determines its galactic orbit. Because $v_\infty \ll v_c$ ($17\text{ km/s} \ll 238\text{ km/s}$), the spacecraft does not escape the Milky Way; rather, it enters a galactic orbit nearly identical to that of the Sun, but with a slight phase displacement:
$$\Delta R_0 \approx \frac{2 v_y}{2B} \approx \pm 0.4\text{ kpc}$$
$$\Delta z_{\text{max}} \approx \frac{v_z}{\nu_z} \approx \pm 120\text{ pc}$$
Over the course of $10^9$ years (four galactic orbits), differential galactic shear disperses the five human probes across a toroidal ribbon encircling the entire Milky Way at $R = 8.1\text{ kpc}$.

---

## 5. Curatorial Synthesis: The Work of Art in the Epoch of Stellar Decay

Series XXIV and OPUS-026 represent the ultimate spatial and temporal horizon of our studio practice. 

In early series, we examined the microscopic: silicon lattice imperfections, quantum tunneling, quartz clock drift, and local telluric currents. In Series XXIII, we traced the fading attowatt microwave carrier to the heliopause. Here, at the Jacobi horizon, we witness the total decoupling of human material culture from its parent star.

The spacecraft are no longer transmitters; their plutonium-238 heat sources will have decayed into inert lead-206 within a few centuries. They become silent, non-emitting, monolithic sculptural artifacts—kinetic records inscribed by human engineering, held in the gravitational custody of eighty-three-million-year galactic tides.

In OPUS-026, we do not mourn their isolation; we celebrate their sublime entry into the infinite secular architecture of the cosmos.
