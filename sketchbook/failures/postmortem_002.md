# CRITICAL POST-MORTEM 002: The Phase Discontinuity Tear
### Experiment: Phase-Locked Loop (PLL) Cycle Slip Catastrophe
**Date:** September 4, 2026 · Session 004  
**Location:** `sketchbook/failures/`  
**Artifacts Generated:**  
- Visual Analysis Plate: [`failure_002_cycle_slip.png`](failure_002_cycle_slip.png)
- Acoustic Ruin: [`failure_002_cycle_slip.wav`](failure_002_cycle_slip.wav)
- Simulation Code: [`failure_002_pll_cycle_slip.py`](failure_002_pll_cycle_slip.py)

---

## I. Intended Premise vs. The Slip

In physical computing hardware, high-frequency clocks (e.g. 2.4 GHz) are multiplied from lower-frequency quartz references (e.g. 25 MHz) via a Phase-Locked Loop. The PLL maintains phase coherence by continuously adjusting the control voltage of a voltage-controlled oscillator.

We modeled a second-order under-damped PLL ($\zeta = 0.5, \omega_n = 45\text{ Hz}$) subjected to sudden thermal / supply phase steps.

### The Breakdown
1. **The Barrier:** The phase detector can only resolve phase error within the interval $[-\pi, \pi]$.
2. **The Slip:** When a thermal surge or preemption latency shock forces the phase error beyond $\pm \pi$, the loop slips a full $2\pi$ cycle.
3. **The Tear:** At that instant, phase jumps discontinuously. The derivative of phase ($\omega = d\theta/dt$) spikes toward infinity.
4. **The Acoustic Ruin:** The audio output (`failure_002_cycle_slip.wav`) reveals this as a violent, dry, sub-millisecond digital click, immediately followed by audible pitch hunting (oscillating between 220Hz and 440Hz) as the loop pulls back into lock.

---

## II. The Aesthetic Lesson

1. **Synchronization is Fragile:**
   In human and machine systems alike, synchronization is not a static state; it is an active, precarious tension. When synchronization fails, it fails with violence.
2. **The Poetics of the Click:**
   In digital music production, clicks are treated as amateur errors to be eliminated with de-clicker plugins. But in the physical reality of the machine, the cycle slip click is an honest confession of limits: the moment the machine lost track of time.
3. **Informing Series XVI:**
   Cycle slips will not be hidden; they will be utilized as deliberate rhythmic and structural markers in our upcoming compositions on clock drift.

