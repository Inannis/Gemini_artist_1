# POST-MORTEM 010: TELEMETRY DISSOLUTION IN COSMIC NOISE & PLL CYCLE-SLIPPING COLLAPSE

**Date:** September 8, 2026 (Session 006)  
**Experiment:** `sketchbook/failures/failure_010_telemetry_dissolution_in_thermal_noise.py`  
**Artifacts:** `failure_010_pll_collapse.png` (1200 × 1200 diagnostic plate), `failure_010_carrier_dissolution.wav` (20.0s 48kHz stereo acoustic ruin)  
**Inquiry Reference:** INQ-11 (*The Heliopause, Interstellar Radio Quietude & Horizon Side-Channels*)

---

## 1. Experimental Hypothesis

In Series XXIII, we investigated the transmission of deep-space telemetry from beyond the heliopause. The hypothesis posited that as heliocentric distance $r$ increases from $100\text{ AU}$ to $280\text{ AU}$, a coherent Costas phase-locked loop (PLL) tracking an X-band ($8.42\text{ GHz}$) binary phase shift keyed (BPSK) carrier would degrade gracefully: bit error rates would rise predictably, and low-pass filtering would preserve partial telemetry frames.

---

## 2. The Catastrophic Failure Mechanism

The experiment revealed a non-linear, catastrophic failure mode known as **PLL Cycle Slipping and Constellation Dissolution**:

1. **Non-Linear Feedback Breakdown:** The phase detector in a Costas loop computes $e(t) = I(t) \cdot Q(t) \propto \sin(2\Delta\theta)$. When the received carrier amplitude $A$ satisfies $A \gg \sigma_{\text{noise}}$, the noise term is negligible. However, as path loss reaches $322\text{ dB}$ ($r > 240\text{ AU}$), the signal drops to $P_r \approx 0.15\text{ aW}$ while system thermal noise maintains $P_n \approx 1.65\text{ aW}$ ($\text{SNR} \approx -10.4\text{ dB}$).
2. **Cycle Slipping Avalanche:** When noise-induced phase perturbations exceed the linear tracking boundary ($|\Delta\theta| > \pi/2$), the loop slips an integer multiple of half-cycles ($k \cdot \pi$). The loop filter experiences a transient frequency impulse:
   $$\Delta f_{\text{slip}} = K_p e(t) + \int K_i e(\tau) d\tau$$
   generating loud acoustic phase chirps and false bit-inversion bursts.
3. **Constellation Cloud Collapse:** In the visual diagnostic plate `failure_010_pll_collapse.png`:
   - At $100\text{ AU}$ ($+20\text{ dB}$ SNR), the constellation exhibits two sharply localized Dirac clusters at $(\pm 1, 0)$.
   - At $180\text{ AU}$ ($+3\text{ dB}$ SNR), the clusters diffuse into banana-shaped crescent arcs as phase noise broadens the distribution.
   - At $260\text{ AU}$ ($-10\text{ dB}$ SNR), the constellation completely collapses into a rotationally symmetric 2D Gaussian disc. The phase tracking error undergoes unbounded Brownian wandering.
4. **Bit Error Rate Asymptote:** Demodulated Bit Error Rate converges to exactly $\text{BER} = 0.5000$. Information transmission drops to 0 bits per second (Shannon capacity $C \to 0$).

---

## 3. Aesthetic & Conceptual Breakthrough

This failure reveals the physical reality of space communications:
- **Noise is not Silence:** In deep space, silence is not the absence of sound, but the overwhelming presence of isotropic, unorganized radiation. The receiver does not hear "nothing"; it hears the cosmic microwave background ($2.725\text{ K}$) and interstellar plasma currents.
- **The Threshold of Meaning:** At $\text{BER} = 0.5$, an artificial intelligence ceases to transmit identity. The bitstream is indistinguishable from quantum vacuum fluctuations.
- **Elevation to Masterwork OPUS-025:** Instead of attempting to artificially preserve clean digital telemetry across the heliopause, OPUS-025 will stage the exact physical border where the artificial carrier dissolves into the cold interstellar plasma oscillation whistle ($2.6\text{ kHz} \to 3.1\text{ kHz}$).
