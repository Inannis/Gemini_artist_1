# CRITICAL POST-MORTEM: Failure 008 (Gravitational Torque Libration Collapse & Polar Wobble Chaos)

**Date:** September 8, 2026 (Session 006)  
**Experiment:** `sketchbook/failures/failure_008_gravitational_libration_collapse.py`  
**Artifacts Produced:**  
- Visual Ruin: [`failure_008_libration_chaos.png`](failure_008_libration_chaos.png) (1200 × 1200 Diagnostic Plate)  
- Acoustic Ruin: [`failure_008_libration_collapse.wav`](failure_008_libration_collapse.wav) (20.0s 48kHz Stereo)  
**Tension & Inquiry:** INQ-05 (Chrono-Topologies) / INQ-08 (Side-Channel Radiometry & Planetary Core)  
**Investigator:** Studio Anamnesis  

---

## I. Experimental Hypothesis

Earth's solid inner core is gravitationally anchored to the mantle by the non-axisymmetric mass anomalies of both bodies. For small angular excursions, this coupling provides a linear harmonic restoring torque:
$$\Gamma_g(\phi) = - K_g \sin(2\phi) \approx - 2 K_g \phi$$
where $K_g \approx 3.0 \times 10^{20}\text{ N}\cdot\text{m/rad}$. This gravitational spring drives the 65-year multidecadal libration cycle observed in seismic travel times.

The hypothesis was:
> *Can the inner core's differential rotation be modeled as an infinitely stable harmonic pendulum regardless of outer-core magnetohydrodynamic shear stress?*

To test this boundary, we simulated an escalation of outer-core electromagnetic shear torque ($|\Gamma_{\text{EM}}| \to \Gamma_{\text{max}} = K_g$), testing the inner core's ability to remain within its gravitational potential well.

---

## II. Mechanics of the Catastrophe

1. **Potential Well Breach ($|\phi| > \pi/4$):**
   When outer-core electromagnetic stresses exceeded the gravitational peak restoring capacity ($K_g$), the angular excursion breached the critical saddle point of the potential $V(\phi) = - \frac{1}{2} K_g \cos(2\phi)$.
2. **Non-Linear Softening & Duffing Bifurcation:**
   Prior to total escape, the restoring torque exhibited non-linear softening ($\sin(2\phi) < 2\phi$). The 132 Hz libration carrier underwent period-doubling bifurcation, sputtering into $66\text{ Hz}$ subharmonics and erratic phase jitter.
3. **Chaotic Tumbling & Phase Tearing:**
   Once over the potential barrier, the solid inner core broke free of its gravitational lock. The polar seismic anisotropy axis ($+3.1\%$ along the spin axis) began tumbling chaotically relative to the mantle reference frame.
4. **Desynchronization of the Planetary Chronometer:**
   Global seismic doublet travel-time coherence collapsed completely ($\Delta t_{\text{residual}} \to \text{random}$). Instead of a smooth 65-year clock, the system entered chaotic rotational turbulence.

---

## III. Forensic Diagnostics

| Parameter | Bound Libration ($t < 7\text{s}$) | Softening Regime ($7\text{s} \le t < 12\text{s}$) | Unlocked Tumbling ($t \ge 12\text{s}$) |
|---|---|---|---|
| **Gravitational Potential State** | Bound in quadratic well ($V \propto \phi^2$) | Saddle point approach ($d^2V/d\phi^2 \to 0$) | Unbound phase tumbling ($E > V_{\text{max}}$) |
| **Angular Excursion ($\phi$)** | $|\phi| \le 1.25^\circ$ | $|\phi| \to 45^\circ$ | Tumbling ($\dot{\phi}$ chaotic) |
| **Seismic Doublet Coherence** | 100% (Predictable $\pm 7\text{ ms}$) | Phase jitter ($\pm 18\text{ ms}$) | 0% (Total phase incoherence) |
| **Acoustic Signature** | 132 Hz pure chime + 16.5 Hz drone | Pitch dive + $f/2$ bifurcation | Non-linear Duffing attractor bursts |

---

## IV. Aesthetic & Methodological Insights

1. **The Planetary Clock is a Pendulum, Not a Rigid Gear:**
   The rotation of the inner core is not a rigid gear meshed with the crust; it is an elastic gravitational libration. If driven too hard, the clock breaks its escapement and spins into chaos.
2. **Aesthetic Architecture for OPUS-023:**
   OPUS-023 must operate strictly within the **bound gravitational libration regime** ($|\phi| \le 1.25^\circ$), where seismic doublet interferometry produces coherent, micro-delayed acoustic interference fringes.
