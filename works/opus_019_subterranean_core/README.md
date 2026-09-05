# OPUS-019 · The Subterranean Core: Borehole Radiometry at -500 Meters

**Series XVII · Deep Time Stratigraphy & Media Geology**  
**Accession Number:** OPUS-019-2026-09  
**Created:** September 5, 2026 (Session 005)  
**Artists:** Johan Lisabeth & Antigravity (Studio Anamnesis)  

---

## 1. Curatorial Statement

In *The Subterranean Core: Borehole Radiometry at -500 Meters*, Studio Anamnesis investigates the deep-time physical substrates of computation and memory. Where contemporary culture imagines digital information as weightless, cloud-like, and immaterial, media archaeology reminds us that computation is profoundly lithic: etched into silicon cut from quartz monocrystals, wired with copper excavated from subterranean seams, and powered by the combustion of fossilized Carboniferous forests.

Extending a continuous vertical borehole down to a depth of -500 meters, OPUS-019 recovers a stratigraphic column that spans five distinct epochs:
1. **Holocene Sediment & Alluvial Silt** (0.0m to -60.0m): Porous topsoil saturated with agricultural fertilizers and micro-plastic filaments ($v_s \approx 1450 \text{ m/s}$).
2. **Jurassic Aeolian Sandstone** (60.0m to -180.0m): Fossilized cross-bedded dune fields forming a dry, porous acoustic resonator ($v_s \approx 2800 \text{ m/s}$).
3. **Carboniferous Anthracite Seam** (180.0m to -310.0m): Compressed botanical carbon acting as a massive mechanical acoustic absorber ($v_s \approx 1850 \text{ m/s}$).
4. **The Techno-Fossil Stratum** (310.0m to -410.0m): A crushed lithified stratum of oxidized silicon microprocessors, copper bus interconnects, and gold wirebonds. This layer emits intense, periodic electromagnetic Van Eck memory bus radiation (433.92 MHz carrier with 128/256 Hz sidebands).
5. **Pre-Cambrian Crystalline Gneiss** (410.0m to -500.0m): High-grade metamorphic basement rock pierced by hydrothermal quartz veins under lithostatic pressure ($v_s \approx 3650 \text{ m/s}$, $T \approx 28.5 ^\circ\text{C}$).

The artwork operates across three entangled media registers:
- **Visual Master Plate (4K UHD Lossless PNG):** A monumental 3840 × 2160 composition displaying the raymarched 3D core sample flanked by an RF waterfall spectrogram, shear-wave velocity profiles, and photolithographic alignment reticles.
- **Acoustic Master Suite (120s 48kHz Stereo WAV):** An acoustic descent through the borehole, synthesizing low-frequency mechanical shaft resonances (18.2 Hz), hydrothermal quartz fracture crackle, and demodulated AM Van Eck side-channel radiation.
- **Interactive Museum Vitrine (HTML5/Canvas/Web Audio):** A real-time virtual laboratory enabling the investigator to navigate between 0m and -500m, audition the acoustic resonance of each stratum, and inspect live RF oscilloscopes.

---

## 2. Technical Specifications & Dimensions

| Parameter | Specification |
| :--- | :--- |
| **Visual Plate Resolution** | 3840 × 2160 pixels (4K UHD Lossless 24-bit RGB) |
| **Visual Pipeline** | Node.js raymarching + Python standard library PNG writer (`png_writer.py`) |
| **Acoustic Master Suite** | 120.00 seconds, 48,000 Hz, 16-bit PCM Stereo WAV (`audio_writer.py`) |
| **Museum Vitrine Dimensions** | Cylindrical Borosilicate Vitrine: $\varnothing 122\text{ mm} \times 4.0\text{ m}$ height |
| **Installation Hardware** | Dual 2700K/5600K fiber-optic collimators, 2× green-phosphor CRT oscilloscopes |
| **Carrier Frequency** | 433.920 MHz (UHF ISM band Van Eck side-channel leakage) |
| **Borehole Depth** | -500.0 meters true vertical depth (TVD) |
| **Geothermal Gradient** | $+0.028 ^\circ\text{C}/\text{m}$ ($14.5 ^\circ\text{C}$ surface to $28.5 ^\circ\text{C}$ basal) |

---

## 3. Structural File Manifest

- `core_engine.js`: Algorithmic engine that raymarches the 3D core, renders the Van Eck waterfall, and writes raw RGB bytes.
- `render_master_plate.py`: Python wrapper compressing raw buffer into 4K PNG via `png_writer.py`.
- `artwork.png`: Master 4K UHD exhibition plate.
- `synthesize_borehole_suite.py`: Audio synthesis engine modeling borehole acoustics and RF sideband modulation.
- `borehole_radiometry.wav`: 120-second 48kHz stereo master audio track.
- `study.jpg`: Photorealistic architectural exhibition study of the museum vitrine installation.
- `index.html`: Interactive web application and depth-scrubber.
- `README.md`: This curatorial document and technical dossier.

---

## 4. Theoretical Lineage

> "The history of media is not a progression of ethereal concepts, but an excavation of raw elements: zinc, coltan, lithium, and quartz ripped from the ground and forced to vibrate under electrical current."  
> — *Treatise 007: Geological Waveguides & Subterranean Radiometry*

OPUS-019 draws directly upon the media ecology of **Jussi Parikka** (*A Geology of Media*), the techno-epistemology of **Friedrich Kittler** (*Gramophone, Film, Typewriter*), and the structural austerity of **Agnes Martin**. It asserts that memory is never deleted; it merely settles into the lithosphere.
