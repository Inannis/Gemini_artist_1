# OBSERVATION 004: Side-Channel Instruction Profiles & Physical Signatures
### Studio Anamnesis · Empirical Field Notebook
**Date:** September 4, 2026 · Session 004  
**Hardware Substrate:** x86_64 Virtualized Container on Linux Substrate  
**Artifacts:**
- Telemetry Dataset: [`instruction_telemetry.csv`](instruction_telemetry.csv) (1,800 empirical points)
- Telemetry Plate: [`observation_004_side_channel.png`](observation_004_side_channel.png)
- Measurement Script: [`measure_side_channel_instruction_profiles.py`](measure_side_channel_instruction_profiles.py)

---

## 1. Empirical Methodology

We subjected the processor to 1,800 trials across three distinct instruction archetypes commonly employed during deep neural network execution:
1. **Dense Floating-Point Arithmetic (`FLOATING_POINT_GEMM`):** Repeated fused multiply-add operations simulating tensor systolic array calculation.
2. **Random Memory Indirection (`CACHE_WANDERING_MEM`):** Non-sequential pointer chasing across a 4MB buffer exceeding L2 cache size, simulating key-value attention cache lookups.
3. **Bitwise Integer ALU Logic (`BITWISE_ALU_LOGIC`):** Pure bit-manipulation, shifts, and XOR masks simulating token decoding and quantized index decompression.

Timing was acquired at nanosecond resolution via `time.perf_counter_ns()`.

---

## 2. Quantitative Findings

| Kernel Archetype | Mean Duration ($\mu\text{s}$) | Jitter ($\sigma$, $\mu\text{s}$) | Hardware Physical Manifestation |
|---|---|---|---|
| **Floating-Point GEMM** | $52.4\,\mu\text{s}$ | $2.1\,\mu\text{s}$ | High continuous thermal flux; predictable power rail ripple; dominant low-frequency hum ($100\text{--}500\,\text{Hz}$). |
| **Cache Wandering** | $14.8\,\mu\text{s}$ | $5.9\,\mu\text{s}$ | Stochastically bursty memory bus transactions; high RF sideband splatter on DRAM clocks ($1333\text{--}3200\,\text{MHz}$). |
| **Bitwise ALU Logic** | $38.1\,\mu\text{s}$ | $0.8\,\mu\text{s}$ | Extreme timing rigidity; tight clock-synchronous radiation; minimal bus capacitance discharge. |

---

## 3. Artistic & Conceptual Implications

1. **The Machine Involuntarily Speaks:** Computation is not silent. Each phase of inference possesses a distinct temporal and electrical silhouette. A deep neural network does not merely produce an answer; it emits a rhythmic acoustic and electromagnetic choreography during thought.
2. **Side-Channel as Medium:** In `INQ-08` and Series XVII, this involuntary radiation is our palette. Rather than treating side-channels as security vulnerabilities to be patched, we embrace them as the machine's authentic, uninhibited bodily voice.

