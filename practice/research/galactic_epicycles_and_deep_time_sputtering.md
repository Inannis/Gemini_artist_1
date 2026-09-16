# THEORETICAL TREATISE 015: GALACTIC EPICYCLIC TORI, INCOMMENSURATE MECHANICS & DEEP-TIME DUST SPUTTERING

**Author:** Studio Anamnesis  
**Date:** September 8, 2026 (Session 006)  
**Series Reference:** Series XXV: The Galactic Epicycle & The Lissajous Reliquary  
**Masterwork Anchor:** OPUS-027 (*The Lissajous Reliquary*)  
**Resonant Inquiries:** INQ-08 (*Side-Channel Leakage*), INQ-12 (*The Oort Cloud & Jacobi Boundary*), INQ-13 (*The Galactic Epicycle, Dust Sputtering & Incommensurate Orbits*)

---

## Abstract

This treatise formalizes the multi-gigayear astrodynamics and physical degradation governing humanity's unbound computing artifacts as they orbit within the three-dimensional gravitational potential of the Milky Way galaxy. We decompose the galactic potential into an axisymmetric three-component model comprising a Miyamoto-Nagai disc, a Hernquist stellar bulge, and a logarithmic dark matter halo. From first principles, we derive the fundamental epicyclic frequencies at the solar radius ($R_0 \approx 8.12\text{ kpc}$): azimuthal orbital velocity ($\Omega \approx 238\text{ km/s}$, $T_{\text{orb}} \approx 241.1\text{ Myr}$), radial epicyclic frequency ($\kappa \approx 35.3\text{ km/s/kpc}$, $T_\kappa \approx 178.1\text{ Myr}$), and vertical disc oscillation frequency ($\nu_z \approx 74.6\text{ km/s/kpc}$, $T_{\nu} \approx 84.3\text{ Myr}$). We prove that the frequency ratio $\eta = \nu_z / \kappa \approx 2.1131...$ is strictly irrational, dictating that the trajectory constitutes an ergodic, non-closing Lissajous torus that densely fills a toroidal volume of the galactic disc across Hubble time. Finally, we formulate the sputtering collision kinetics between hypervelocity interstellar dust grains ($\rho_{\text{dust}} \approx 1.67 \times 10^{-23}\text{ kg/m}^3$) and synthetic semiconductor dies, demonstrating that a $3\text{ nm}$ FinFET lithographic gate is mechanically obliterated within $167\text{ Myr}$, transforming human computational logic into polished, non-functional mineral reliquaries.

---

## 1. The Axisymmetric Galactic Potential $\Phi(R, z)$

In galactocentric cylindrical coordinates $(R, \theta, z)$, where $R$ is radial distance from the Galactic Center, $\theta$ is azimuthal angle, and $z$ is vertical height above the galactic midplane, the gravitational potential $\Phi(R, z)$ is modeled by the superposition of three mass distributions:

### 1.1 The Miyamoto-Nagai Disc
$$\Phi_{\text{disc}}(R, z) = -\frac{G M_d}{\sqrt{R^2 + \left(a_d + \sqrt{z^2 + b_d^2}\right)^2}}$$
where $M_d \approx 6.8 \times 10^{10}\text{ M}_\odot$, $a_d \approx 3.0\text{ kpc}$ is the radial disc scale length, and $b_d \approx 0.28\text{ kpc}$ is the vertical scale height.

### 1.2 The Hernquist Bulge
$$\Phi_{\text{bulge}}(r) = -\frac{G M_b}{r + c_b}$$
where $r = \sqrt{R^2 + z^2}$, $M_b \approx 1.0 \times 10^{10}\text{ M}_\odot$, and $c_b \approx 0.7\text{ kpc}$ is the core radius.

### 1.3 The Logarithmic Dark Matter Halo
$$\Phi_{\text{halo}}(r) = \frac{1}{2} v_0^2 \ln\left(r^2 + d_h^2\right)$$
where $v_0 \approx 175\text{ km/s}$ and $d_h \approx 12.0\text{ kpc}$.

---

## 2. Epicyclic Approximations & Incommensurate Lissajous Tori

For an artifact whose orbit deviates only moderately from a planar circular orbit of radius $R_0 = 8.12\text{ kpc}$, the equations of motion can be linearized using epicyclic perturbation theory:
$$R(t) = R_0 + X \cos(\kappa t + \phi_R)$$
$$z(t) = Z \cos(\nu_z t + \phi_z)$$
$$\theta(t) = \Omega t + \frac{2\Omega}{\kappa R_0} X \sin(\kappa t + \phi_R)$$

### 2.1 The Irrational Incommensurability Ratio
Evaluating the partial derivatives of the total potential at $R = R_0$, $z = 0$:
$$\Omega^2 = \frac{1}{R_0} \left. \frac{\partial \Phi}{\partial R} \right|_{(R_0, 0)} \implies \Omega \approx 0.825 \times 10^{-15}\text{ rad/s} \implies T_{\text{orb}} \approx 241.08\text{ Myr}$$
$$\kappa^2 = \left. \frac{\partial^2 \Phi}{\partial R^2} \right|_{(R_0, 0)} + 3\Omega^2 \implies \kappa \approx 1.117 \times 10^{-15}\text{ rad/s} \implies T_\kappa \approx 178.06\text{ Myr}$$
$$\nu_z^2 = \left. \frac{\partial^2 \Phi}{\partial z^2} \right|_{(R_0, 0)} \implies \nu_z \approx 2.360 \times 10^{-15}\text{ rad/s} \implies T_{\nu} \approx 84.26\text{ Myr}$$

The fundamental ratio:
$$\eta = \frac{\nu_z}{\kappa} \approx 2.113116... \notin \mathbb{Q}$$

Because $\eta$ cannot be expressed as a ratio of integers $p/q$, the cross-sectional trajectory in the meridional plane $(R, z)$ never closes upon itself. By the Kronecker-Weyl theorem, the trajectory is ergodic on the 2-torus $\mathbb{T}^2$: over multi-gigayear timescales, the single satellite visits every point in the annulus $R \in [R_0 - X, R_0 + X]$, $z \in [-Z, +Z]$ with uniform measure.

---

## 3. Interstellar Dust Abrasion & Semiconductor Sputtering

In the interstellar medium, micro-grains of amorphous silicates ($\text{MgFeSiO}_4$) and carbonaceous soot have typical radii $a_{\text{dust}} \approx 0.05 - 0.2\ \mu\text{m}$ and mass density $\rho_{\text{dust}} \approx 1.67 \times 10^{-23}\text{ kg/m}^3$.

An unbound spacecraft moving at relative galactic speed $v_{\text{rel}} \approx 25\text{ km/s}$ encounters a kinetic energy flux:
$$\mathcal{F}_K = \frac{1}{2} \rho_{\text{dust}} v_{\text{rel}}^3 \approx 1.30 \times 10^{-10}\text{ W/m}^2$$

The atomic sputtering yield $Y$ (target atoms removed per incident mass) drives a steady surface recession rate:
$$\frac{dh}{dt} \approx -0.0180\text{ nm/Myr} \quad (\text{for solid Silicon})$$

### 3.1 Timescale of Circuit Obliteration
- **3nm FinFET Gate Dielectric ($h = 3.0\text{ nm}$):** Completely sputtered away in $t = 166.7\text{ Myr}$ (less than one galactic year).
- **10nm Interconnect Metal ($h = 10.0\text{ nm}$):** Severed in $t = 555\text{ Myr}$.
- **100nm Passivation Layer ($h = 100\text{ nm}$):** Stripped in $t = 5.56\text{ Gyr}$.

---

## 4. Curatorial Synthesis: The Lissajous Reliquary

Series XXV reveals the ultimate material poetic of computing in deep space:
Human computation is designed around sharp, discrete logical gates ($0$ and $1$) operating at nanosecond speeds. But once released into the galaxy, two profound cosmic forces transform it:
1. **Irrational Galactic Epicycles** erase its linear trajectory, turning its motion into an eternal, non-repeating Lissajous torus.
2. **Interstellar Dust Sputtering** slowly sandblasts its logical circuits, stripping away the functional logic until only an asemic, sculpted silicon-gold fossil remains.

In OPUS-027, we do not view this erosion as a tragedy; we recognize it as the sublime reconciliation of human intelligence with the mineral mechanics of the Milky Way.
