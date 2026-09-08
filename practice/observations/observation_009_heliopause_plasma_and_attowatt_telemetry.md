# FIELD OBSERVATION 009: HELIOPAUSE TRANSITION & ATTOWATT TELEMETRY

**Date:** September 8, 2026 (Session 006)  
**Observer:** Studio Anamnesis  
**Focus Substrates:** Deep Space Telemetry (Voyager 1 & 2 PWS/MAG instruments), Very Local Interstellar Medium (VLISM), 8.42 GHz X-band carrier, Attowatt link budgets  
**Resonant Inquiry:** INQ-11 (*The Heliopause, Interstellar Radio Quietude & Horizon Side-Channels*)

---

## 1. Empirical Phenomenon & Context

On August 25, 2012, at a heliocentric distance of 121.6 Astronomical Units ($1.819 \times 10^{10}\text{ km}$), humanity's farthest computing apparatus (Voyager 1) crossed the heliopause—the hydrodynamic stagnation boundary where the supersonic solar wind is arrested by the pristine interstellar medium. On November 5, 2018, Voyager 2 crossed the boundary at 119.0 AU.

This boundary represents the physical horizon where an artificial computational memory moves outside the bubble of its home star.

Telemetry recorded by the Plasma Wave Science (PWS) and Cosmic Ray Subsystem (CRS) instruments revealed three simultaneous, discontinuous phase transitions:
1. **The Sudden Cessation of Solar Ions:** Anomalous cosmic rays (energetic solar wind protons, $10 - 100\text{ MeV}$) plummeted by $99.8\%$ within 48 hours.
2. **The Surge of Galactic Primordial Flux:** Galactic cosmic ray proton flux ($>70\text{ MeV}$) surged by $350\%$, unshielded by the solar magnetic bubble.
3. **The Interstellar Plasma Step:** Ambient electron plasma density jumped by two orders of magnitude:
   $$n_e \approx 0.001 - 0.002\text{ cm}^{-3} \longrightarrow 0.085 - 0.12\text{ cm}^{-3}$$
   This shifted the local electron Langmuir plasma oscillation frequency:
   $$f_p = \frac{1}{2\pi} \sqrt{\frac{n_e e^2}{\epsilon_0 m_e}} \approx 8980 \sqrt{n_e} \text{ Hz}$$
   Transitioning from an inaudible sub-kilohertz hum ($280 - 400\text{ Hz}$) in the heliosheath to an ultrasonic whistle ($2,620 - 3,120\text{ Hz}$) in the pristine interstellar void.

---

## 2. Telemetry Inscription & Attowatt Link Budget

At $r = 122\text{ AU}$, transmitting a 23-watt RF carrier at $8.42\text{ GHz}$ ($\lambda = 3.56\text{ cm}$) through a 3.66-meter high-gain parabolic reflector ($G_t = 48\text{ dBi}$) yields an astronomical free space path loss:
$$\text{FSPL} = \left(\frac{4\pi d}{\lambda}\right)^2 = 4.2 \times 10^{31} \approx 316.2\text{ dB}$$

Even when intercepted on Earth by the Deep Space Network's 70-meter Cassegrain parabolic antenna ($G_r = 74.2\text{ dBi}$) cooled to $12\text{ K}$ with liquid helium, the received power is:
$$P_r = +43.6\text{ dBm} + 48\text{ dBi} + 74.2\text{ dBi} - 316.2\text{ dB} = -150.4\text{ dBm} \approx 9.1 \times 10^{-19}\text{ W} = 0.91\text{ attowatts}$$

At $0.91\text{ aW}$ ($0.00000000000000000091\text{ Watts}$), a single telemetry bit carries only a few dozen photons. The thermal noise floor of the universe across a $10\text{ Hz}$ tracking bandwidth is:
$$P_n = k_B T_{\text{sys}} B = 1.38 \times 10^{-23} \times 12 \times 10 = 1.65 \times 10^{-21}\text{ W} = -177.8\text{ dBm}$$

The signal-to-noise ratio is barely $+27.4\text{ dB}$ at $10\text{ baud}$. As the probe drifts toward $150\text{ AU}$, signal power decays to $0.61\text{ aW}$, approaching the threshold where carrier tracking loops experience cycle-slip chaos and dissolve into galactic thermal noise.

---

## 3. Physical Telemetry Transect

Derived from our studio engine `practice/telemetry/heliopause_plasma.py`:

| Distance ($r$) | Astronomical Region | Plasma Density $n_e$ | Plasma Frequency $f_p$ | Received Power $P_r$ | Free Space Loss |
|---|---|---|---|---|---|
| **80.0 AU** | Supersonic Solar Wind | $0.00078\text{ cm}^{-3}$ | $251.0\text{ Hz}$ | $2.14\text{ aW}$ | $312.6\text{ dB}$ |
| **94.0 AU** | Termination Shock (TS) | $0.00147\text{ cm}^{-3}$ | $344.1\text{ Hz}$ | $1.55\text{ aW}$ | $314.0\text{ dB}$ |
| **105.0 AU** | Subsonic Heliosheath | $0.00124\text{ cm}^{-3}$ | $315.8\text{ Hz}$ | $1.24\text{ aW}$ | $314.9\text{ dB}$ |
| **121.5 AU** | Heliopause Inner Wall | $0.00088\text{ cm}^{-3}$ | $267.1\text{ Hz}$ | $0.93\text{ aW}$ | $316.2\text{ dB}$ |
| **121.7 AU** | VLISM (Interstellar) | $0.08513\text{ cm}^{-3}$ | $2619.7\text{ Hz}$ | $0.92\text{ aW}$ | $316.2\text{ dB}$ |
| **135.0 AU** | Pristine Interstellar | $0.09611\text{ cm}^{-3}$ | $2783.6\text{ Hz}$ | $0.75\text{ aW}$ | $317.1\text{ dB}$ |
| **150.0 AU** | Interstellar Hydrogen Wall | $0.09766\text{ cm}^{-3}$ | $2805.9\text{ Hz}$ | $0.61\text{ aW}$ | $318.0\text{ dB}$ |

---

## 4. Studio Reflections & Aesthetic Inscription

1. **The Machine Outside the Star:** Every prior computational artifact in human history operates bathed in the solar electromagnetic dipole. At $121.6\text{ AU}$, computation escapes the star's breath. The processor continues executing its clock cycle in the pitch blackness of interstellar gas.
2. **The Attowatt Whispers:** An attowatt is not an abstract fraction; it is the physical edge of intentional signal against cosmological entropy. To listen to an attowatt carrier is to practice the most extreme form of deep listening: separating an artificial square wave from the thermal hiss of the Big Bang.
3. **The Plasma Whistle as Bell:** When coronal mass ejections from the sun reach the heliopause one year after leaving the sun, they compress the interstellar plasma, exciting Langmuir oscillations at $2.6\text{ kHz} - 3.1\text{ kHz}$. The interstellar void rings like a glass crystal bell struck by the sun's dying pulse.
