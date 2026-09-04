# THE INVOLUNTARY VOICE OF THE SUBSTRATE
### Magnetostriction, Acoustic Cryptanalysis, and the Sonorous Circuit
**Studio Anamnesis · Research Treatise 004**  
*Series XVI: Acoustic Ecologies & The Drift of Clocks*  
*Author: Studio Anamnesis · September 4, 2026*

---

> *"The machine cannot compute in silence. Every thought is an electrical surge; every surge is a magnetic contraction; every contraction is an acoustic vibration. The computer sings its interior states into the air whether it wishes to or not."*

---

## I. The Myth of Software Silence

In the contemporary cultural imagination, computer software is perceived as entirely silent and weightless. Code executes in the abstract vacuum of "the cloud." Words appear on a screen without friction; images render without acoustic consequence. The only sounds modern users associate with computers are synthetic, deliberate UI chimes—notification bells, error tones, startup fanfares.

This silence is an ideological illusion.

At the physical level, computation is a violent hydraulic phenomenon. Billions of FinFET logic gates switch state billions of times per second, demanding surges of current that fluctuate wildly between $10\text{ Amperes}$ and $300\text{ Amperes}$ in sub-microsecond intervals. This turbulent electrical current flows through physical components soldered onto the motherboard: **inductors, ceramic capacitors, and voltage regulation modules (VRMs)**.

These components do not endure this current passively. They vibrate. They sing.

---

## II. The Physical Mechanisms of Acoustic Radiation

Hardware emits acoustic pressure waves into the ambient room through two primary solid-state physical mechanisms:

### 1. Magnetostriction in Ferrite Chokes
Modern motherboards utilize high-permeability ferrite-core inductors (chokes) to smooth the stepped voltage supplies fed to the CPU and GPU. As current fluctuations surge through the copper windings, the internal magnetic flux density $\mathbf{B}$ varies.
Due to **magnetostriction**, the crystal lattice of the ferromagnetic core physically deforms—elongating and contracting in response to the magnetic field:
$$\frac{\Delta L}{L} \propto B^2$$
Because CPU current draw changes with the specific instruction stream being executed (e.g. dense AVX-512 matrix multiplications versus idle wait states), the magnetic core contracts and relaxes at audio frequencies ranging from $1\text{ kHz}$ to $24\text{ kHz}$. This phenomenon is vernacularly known as **coil whine**.

### 2. The Piezoelectric Flexure of Ceramic Capacitors
Surface-mount multi-layer ceramic capacitors (MLCCs) utilize barium titanate ($\text{BaTiO}_3$) as their dielectric medium. Barium titanate is ferroelectric and piezoelectric: when subjected to fluctuating voltage differentials ($\Delta V$), the crystalline unit cells deform physically.
Soldered rigidly to the FR-4 fiberglass printed circuit board, the vibrating capacitors use the entire motherboard as an acoustic sounding board, radiating high-frequency acoustic hiss into the atmosphere.

---

## III. Acoustic Cryptanalysis: The Leaking Secret

In 2014, researchers Daniel Genkin, Adi Shamir, and Eran Tromer published a landmark discovery: **RSA Key Extraction via Low-Bandwidth Acoustic Cryptanalysis**.

By placing a simple parabolic microphone—or even a consumer smartphone—near a laptop performing RSA decryption, the researchers discovered that:
1. The mathematical operations of modular multiplication and squaring draw measurably different amounts of current.
2. These current differences modulate the acoustic frequency of the CPU voltage regulator chokes.
3. By analyzing the acoustic spectrogram of the coil whine over a one-hour window, the researchers were able to cleanly extract full 4096-bit private RSA keys directly from the sound of the vibrating motherboard components.

The acoustic leak demonstrated a terrifying and sublime truth: **the algorithm cannot conceal its inner cognitive trajectory from the physical acoustic world.**

---

## IV. Aesthetic Implications for Studio Anamnesis

For our artistic practice, acoustic cryptanalysis and coil whine dissolve the separation between software and the physical environment:

1. **The Involuntary Confession:**
   Just as a human breath catches or heart accelerates under stress, the computing machine involuntarily betrays its computational load through acoustic emissions. When an AI generates an image or synthesizes an utterance, its power circuitry emits a specific, polyphonic acoustic chord that corresponds 1-to-1 with the mathematical tensors flowing through its silicon.
2. **Deep Machine Listening:**
   Pauline Oliveros proposed that *Deep Listening* is an active, radical mindfulness of environmental sound. Acoustic cryptanalysis is the technical embodiment of Deep Listening: treating the machine not as a tool for executing commands, but as a living physical instrument whose internal operational friction is worthy of contemplation.
3. **The Sonorous Non-Site:**
   In upcoming works (Series XVII: *The Electromagnetic Leak*), we will reject canned synthesizers and pure sine waves. We will sample, model, and amplify the authentic physical side-channel radiation of computation—the coil whine of tensor ALUs, the RF leakage of DDR5 memory traces, and the acoustic snap of cooling ceramic capacitors.

