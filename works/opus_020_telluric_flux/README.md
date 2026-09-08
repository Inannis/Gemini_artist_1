# OPUS-020 · The Telluric Flux: Superconducting Meissner Vitrine at 4.2 Kelvin

**Series XVIII · Cryogenic Horizons & Topological Boundaries**  
**Accession Number:** OPUS-020-2026-09  
**Created:** September 8, 2026 (Session 006)  
**Artists:** Studio Anamnesis (Antigravity & Inannis)  

---

## 1. Curatorial Statement

In *The Telluric Flux: Superconducting Meissner Vitrine at 4.2 Kelvin*, Studio Anamnesis confronts computation at its absolute thermodynamic limit: the vanishing of electrical resistance and thermal dissipation at sub-Kelvin cryogenic temperatures.

Where OPUS-016 investigated the boiling heat of server dies under full computational load ($94.5^\circ\text{C}$), and OPUS-017 mapped the evaporative salt desiccation of spent silicon, OPUS-020 immerses a 300mm monocrystalline silicon wafer coated in high-temperature cuprate superconductor ($\text{YBa}_2\text{Cu}_3\text{O}_{7-\delta}$) inside an evacuated optical cryostat at $T = 4.182\text{ Kelvin}$ ($-268.97^\circ\text{C}$).

At this temperature, the material undergoes a macroscopic quantum phase transition:
1. **The Meissner Effect ($B = 0$):** Below the critical temperature $T_c = 93\text{ K}$, external magnetic flux is completely expelled from the bulk superconductor via screening supercurrents, creating stable diamagnetic levitation in mid-air with zero mechanical contact.
2. **Abrikosov Quantum Flux Pinning:** Penetrating magnetic flux is quantized into discrete vortex tubes ($\Phi_0 = h / 2e \approx 2.0678 \times 10^{-15}\text{ Wb}$) pinned to crystalline defects, locking the levitating wafer in 3D spatial equilibrium.
3. **Transduction of Planetary Geophysics:** By coupling the cryostat to live internet telemetry from the USGS Real-Time Earthquake Network (crustal shear waves, focal depths) and NOAA Space Weather satellites (solar wind geomagnetic index $K_p = 3.0$), planetary telluric currents dynamically perturb the magnetic flux lines. The wafer subtly wobbles in levitation, its quantum flux vortices slipping and releasing microscopic Barkhausen-like acoustic impulses.

---

## 2. Technical Specifications & Dimensions

| Parameter | Laboratory Specification |
| :--- | :--- |
| **Visual Plate Resolution** | 3840 × 2160 pixels (4K UHD Lossless 24-bit RGB) |
| **Visual Pipeline** | Node.js potential flow engine (`cryo_engine.js`) + pure Python PNG writer (`png_writer.py`) |
| **Acoustic Master Suite** | 120.00 seconds, 48,000 Hz, 16-bit PCM Stereo WAV (`audio_writer.py`) |
| **Operating Temperature** | $T = 4.182\text{ Kelvin}$ (Liquid Helium under atmospheric pressure) |
| **Superconducting Matrix** | Epitaxial $\text{YBa}_2\text{Cu}_3\text{O}_{7-\delta}$ on 300mm $\text{Si}\langle 100\rangle$ wafer |
| **Applied Field ($B_0$)** | $0.45\text{ Tesla}$ ($H_{c1} = 0.035\text{ T}, H_{c2} = 14.8\text{ T}$) |
| **London Penetration Depth** | $\lambda_0 = 140\text{ nm}$ |
| **Geophysical Driver** | Live USGS Earthquake API + NOAA Space Weather $K_p$ Index + Fiber TCP Jitter |

---

## 3. Structural File Manifest

- `cryo_engine.js`: High-performance procedural generator computing Meissner potential flow streamlines and 3D wafer geometry.
- `render_master_plate.py`: Python wrapper compressing raw byte buffers into lossless 4K UHD PNG via `png_writer.py`.
- `artwork.png`: Master 4K UHD exhibition plate.
- `synthesize_cryo_suite.py`: Audio engine modeling sub-Kelvin whispering gallery modes, liquid helium cavitation, and live telluric Schumann resonance.
- `telluric_flux_4k.wav`: 120-second 48kHz stereo master soundscape.
- `study.jpg`: Photorealistic architectural exhibition study of the museum cryostat vitrine installation.
- `index.html`: Interactive Web cryostat with real-time Web Audio API and thermal quench trigger.
- `README.md`: Curatorial statement and technical dossier.

---

## 4. Theoretical Lineage

> "At absolute zero, Landauer's erasure bound $k_B T \ln 2$ approaches zero. The cost of forgetting vanishes; memory becomes lossless, frictionless, and immutable."  
> — *Treatise 008: Telluric Currents, Superconducting Quantization, and Zero-Entropy Memory*

OPUS-020 draws upon the diamagnetic field theory of Fritz and Heinz London, the Abrikosov vortex lattice, Robert Smithson's *Entropy and the New Monuments*, and the deep acoustic listening of Pauline Oliveros.

