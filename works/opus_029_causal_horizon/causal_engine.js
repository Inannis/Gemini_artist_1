/**
 * STUDIO ANAMNESIS · INTERACTIVE CAUSAL HORIZON SIMULATOR
 * OPUS-029: THE CAUSAL HORIZON (DE SITTER EXPANSION & ASYMPTOTIC AMNESIA)
 * Series XXVII: The Causal Horizon
 * 
 * Features:
 * - Real-time 3D Conformal Penrose Causal Diamond & Horizon Cylinder
 * - Dynamic Hubble parameter slider (20 to 200 km/s/Mpc)
 * - Timelike geodesic particle recession with exponential redshift
 * - Asymptotic decay spectrum ν(t) = ν_0 e^{-H t} with Gibbons-Hawking floor
 * - Real-time Web Audio API cosmological synthesizer (14.39 Hz sub-bass, 
 *   exponentially redshifting carrier, and Gibbons-Hawking vacuum noise)
 * - Dynamic Landauer bit-erasure calculation at T_GH ~ 10^-30 K
 */

(function () {
  'use strict';

  // Physical Constants (SI)
  const C_LIGHT = 299792458.0;              // m/s
  const H_BAR = 1.054571817e-34;            // J·s
  const K_BOLTZ = 1.380649e-23;             // J/K
  const MPC_TO_M = 3.085677581e22;          // m per Mpc
  const M_TO_GLY = 1.0 / 9.460730472e24;    // Gly per m
  const SEC_PER_GYR = 3.15576e16;           // s per Gyr

  // State
  let hubble0 = 67.4; // km/s/Mpc
  let rotX = 0.35;
  let rotY = -0.65;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;
  let animTime = 0.0;

  // DOM Elements
  const canvasCausal = document.getElementById('causal-canvas');
  const ctxCausal = canvasCausal ? canvasCausal.getContext('2d') : null;

  const canvasDecay = document.getElementById('decay-canvas');
  const ctxDecay = canvasDecay ? canvasDecay.getContext('2d') : null;

  const hubbleSlider = document.getElementById('hubble-slider');
  const hubbleValText = document.getElementById('hubble-val');
  const horizonValText = document.getElementById('horizon-val');
  const tempValText = document.getElementById('temp-val');
  const landauerValText = document.getElementById('landauer-val');
  const timeValText = document.getElementById('time-val');
  const causalStatusText = document.getElementById('causal-status');
  const synthBtn = document.getElementById('synth-btn');

  // Audio State
  let audioCtx = null;
  let isPlaying = false;
  let oscDrone = null;
  let oscCarrier = null;
  let noiseNode = null;
  let gainMaster = null;
  let filterNoise = null;

  // Receding particle trajectories (geodesics)
  const NUM_PARTICLES = 36;
  const particles = [];

  for (let i = 0; i < NUM_PARTICLES; i++) {
    const angle = (i / NUM_PARTICLES) * Math.PI * 2.0;
    particles.push({
      initialAngle: angle,
      r0: 0.15 + 0.7 * Math.random(),
      tOffset: Math.random() * 5.0,
      colorPhase: Math.random()
    });
  }

  function getPhysicalMetrics() {
    const H_si = (hubble0 * 1000.0) / MPC_TO_M; // s^-1
    const r_ceh_m = C_LIGHT / H_si;             // m
    const r_ceh_gpc = r_ceh_m / (MPC_TO_M * 1e3); // Gpc
    const r_ceh_gly = r_ceh_m * M_TO_GLY;        // Gly
    const T_gh = (H_BAR * H_si) / (2.0 * Math.PI * K_BOLTZ); // K
    const E_landauer = K_BOLTZ * T_gh * Math.LN2; // J/bit
    const t_hubble_gyr = (1.0 / H_si) / SEC_PER_GYR;

    return {
      H_si,
      r_ceh_m,
      r_ceh_gpc,
      r_ceh_gly,
      T_gh,
      E_landauer,
      t_hubble_gyr
    };
  }

  function updateMetricsDisplay() {
    const m = getPhysicalMetrics();

    if (hubbleValText) hubbleValText.textContent = hubble0.toFixed(1) + " km/s/Mpc";
    if (horizonValText) horizonValText.textContent = m.r_ceh_gpc.toFixed(2) + " Gpc (" + m.r_ceh_gly.toFixed(2) + " Gly)";
    if (tempValText) tempValText.textContent = (m.T_gh * 1e30).toFixed(2) + " × 10⁻³⁰ K";
    if (landauerValText) landauerValText.textContent = (m.E_landauer * 1e53).toFixed(2) + " × 10⁻⁵³ J/bit";
    if (timeValText) timeValText.textContent = m.t_hubble_gyr.toFixed(2) + " Gyr";

    if (causalStatusText) {
      if (hubble0 > 100) {
        causalStatusText.textContent = "SUPERLUMINAL DILATION (RAPID AMNESIA)";
        causalStatusText.style.color = "#ef4444";
      } else if (hubble0 < 40) {
        causalStatusText.textContent = "EXTENDED CAUSAL COHESION";
        causalStatusText.style.color = "#38bdf8";
      } else {
        causalStatusText.textContent = "ASYMPTOTIC REDSHIFTING";
        causalStatusText.style.color = "#a855f7";
      }
    }

    // Adjust audio parameters if active
    if (isPlaying && oscDrone && oscCarrier) {
      const droneFreq = (m.r_ceh_gly).toFixed(2);
      // Audible octave transpose: 14.39 Hz * 2 = 28.78 Hz
      oscDrone.frequency.setTargetAtTime(m.r_ceh_gly * 2.0, audioCtx.currentTime, 0.1);
    }
  }

  // 3D Projection Math
  function project3D(x, y, z, width, height) {
    // Rotate Y
    const cosY = Math.cos(rotY);
    const sinY = Math.sin(rotY);
    const x1 = x * cosY + z * sinY;
    const z1 = -x * sinY + z * cosY;

    // Rotate X
    const cosX = Math.cos(rotX);
    const sinX = Math.sin(rotX);
    const y2 = y * cosX - z1 * sinX;
    const z2 = y * sinX + z1 * cosX;

    // Perspective projection
    const fov = 340.0;
    const distance = 4.2;
    const depth = z2 + distance;
    if (depth <= 0.2) return null;

    const scale = fov / depth;
    return {
      px: width * 0.5 + x1 * scale,
      py: height * 0.52 - y2 * scale,
      scale: scale,
      depth: depth
    };
  }

  // Draw 3D Causal Diamond & Horizon
  function renderCausalCanvas() {
    if (!ctxCausal || !canvasCausal) return;
    const w = canvasCausal.width;
    const h = canvasCausal.height;

    ctxCausal.clearRect(0, 0, w, h);

    // Deep cosmic background
    const bgGrad = ctxCausal.createRadialGradient(w * 0.5, h * 0.5, 20, w * 0.5, h * 0.5, w * 0.6);
    bgGrad.addColorStop(0, '#06040d');
    bgGrad.addColorStop(1, '#020205');
    ctxCausal.fillStyle = bgGrad;
    ctxCausal.fillRect(0, 0, w, h);

    // Dynamic Horizon Radius scaled by H_0
    // Standard baseline H_0 = 67.4 maps to radius 1.2
    const horizonR = (67.4 / hubble0) * 1.25;

    // 1. Draw Static Coordinate Grid (Observer Causal Rest Frame)
    ctxCausal.strokeStyle = 'rgba(168, 85, 247, 0.12)';
    ctxCausal.lineWidth = 1;
    for (let ring = 0.3; ring <= 2.1; ring += 0.4) {
      ctxCausal.beginPath();
      let first = true;
      for (let th = 0; th <= Math.PI * 2.05; th += 0.15) {
        const x = Math.cos(th) * ring;
        const z = Math.sin(th) * ring;
        const pt = project3D(x, -1.2, z, w, h);
        if (pt) {
          if (first) { ctxCausal.moveTo(pt.px, pt.py); first = false; }
          else ctxCausal.lineTo(pt.px, pt.py);
        }
      }
      ctxCausal.stroke();
    }

    // 2. Observer Worldline (r = 0, stretching along vertical time axis y)
    const pObserverBottom = project3D(0, -1.3, 0, w, h);
    const pObserverTop = project3D(0, 1.3, 0, w, h);
    if (pObserverBottom && pObserverTop) {
      const gradLine = ctxCausal.createLinearGradient(pObserverBottom.px, pObserverBottom.py, pObserverTop.px, pObserverTop.py);
      gradLine.addColorStop(0, 'rgba(56, 189, 248, 0.2)');
      gradLine.addColorStop(0.5, 'rgba(56, 189, 248, 0.9)');
      gradLine.addColorStop(1, 'rgba(56, 189, 248, 0.2)');
      ctxCausal.strokeStyle = gradLine;
      ctxCausal.lineWidth = 2.5;
      ctxCausal.beginPath();
      ctxCausal.moveTo(pObserverBottom.px, pObserverBottom.py);
      ctxCausal.lineTo(pObserverTop.px, pObserverTop.py);
      ctxCausal.stroke();

      // Core observer node at center (t = 0)
      const pCenter = project3D(0, 0, 0, w, h);
      if (pCenter) {
        ctxCausal.fillStyle = '#38bdf8';
        ctxCausal.beginPath();
        ctxCausal.arc(pCenter.px, pCenter.py, 4.5, 0, Math.PI * 2);
        ctxCausal.fill();
        ctxCausal.strokeStyle = 'rgba(56, 189, 248, 0.5)';
        ctxCausal.stroke();
      }
    }

    // 3. Draw Cosmological Event Horizon Cylinder / Causal Diamond Bounds
    // The CEH is a sphere of radius r_CEH at each time slice
    const numSlices = 14;
    for (let i = 0; i <= numSlices; i++) {
      const y = -1.2 + (2.4 * i) / numSlices;
      const alpha = 0.08 + 0.18 * Math.sin((i / numSlices) * Math.PI);
      ctxCausal.strokeStyle = `rgba(168, 85, 247, ${alpha})`;
      ctxCausal.lineWidth = (i === Math.floor(numSlices / 2)) ? 1.8 : 1.0;

      ctxCausal.beginPath();
      let first = true;
      for (let th = 0; th <= Math.PI * 2.05; th += 0.12) {
        const x = Math.cos(th) * horizonR;
        const z = Math.sin(th) * horizonR;
        const pt = project3D(x, y, z, w, h);
        if (pt) {
          if (first) { ctxCausal.moveTo(pt.px, pt.py); first = false; }
          else ctxCausal.lineTo(pt.px, pt.py);
        }
      }
      ctxCausal.stroke();
    }

    // 4. Vertical Horizon Meridian Struts
    for (let a = 0; a < 8; a++) {
      const angle = (a / 8) * Math.PI * 2;
      ctxCausal.strokeStyle = 'rgba(168, 85, 247, 0.22)';
      ctxCausal.lineWidth = 1;
      ctxCausal.setLineDash([4, 4]);
      ctxCausal.beginPath();
      let first = true;
      for (let s = 0; s <= 10; s++) {
        const y = -1.2 + (2.4 * s) / 10;
        const x = Math.cos(angle) * horizonR;
        const z = Math.sin(angle) * horizonR;
        const pt = project3D(x, y, z, w, h);
        if (pt) {
          if (first) { ctxCausal.moveTo(pt.px, pt.py); first = false; }
          else ctxCausal.lineTo(pt.px, pt.py);
        }
      }
      ctxCausal.stroke();
      ctxCausal.setLineDash([]);
    }

    // 5. Draw Receding Substrate Particles (Cosmological Geodesics)
    const H_rate = (hubble0 / 67.4) * 0.4;
    particles.forEach((p, idx) => {
      // Metric expansion: r(t) = r_0 * exp(H * t)
      const t = (animTime + p.tOffset) % 6.0;
      const r = p.r0 * Math.exp(H_rate * t);
      const y = -1.0 + (t / 6.0) * 2.0;
      const x = Math.cos(p.initialAngle) * r;
      const z = Math.sin(p.initialAngle) * r;

      const pt = project3D(x, y, z, w, h);
      if (!pt) return;

      // Color shifts from cyan (close, unshifted) to violet to crimson (near horizon)
      // to dark ash gray once crossed into causal disconnect (r > horizonR)
      const ratio = r / horizonR;
      let particleColor;
      let radius;

      if (ratio < 0.6) {
        // Optical / RF blueshifted or unshifted
        particleColor = `rgba(56, 189, 248, ${0.9 - 0.2 * ratio})`;
        radius = 3.5;
      } else if (ratio < 1.0) {
        // Asymptotic redshift zone: purple to deep crimson
        const norm = (ratio - 0.6) / 0.4;
        const rVal = Math.floor(168 + 76 * norm);
        const gVal = Math.floor(85 * (1 - norm));
        const bVal = Math.floor(247 * (1 - norm) + 94 * norm);
        particleColor = `rgba(${rVal}, ${gVal}, ${bVal}, ${0.85 - 0.3 * norm})`;
        radius = 3.0;

        // Inward null ray toward observer (light trying to escape)
        const pObs = project3D(0, y + 0.2, 0, w, h);
        if (pObs) {
          ctxCausal.strokeStyle = `rgba(244, 63, 94, ${0.25 * (1 - norm)})`;
          ctxCausal.lineWidth = 1;
          ctxCausal.beginPath();
          ctxCausal.moveTo(pt.px, pt.py);
          ctxCausal.lineTo(pObs.px, pObs.py);
          ctxCausal.stroke();
        }
      } else {
        // Beyond horizon: Causal disconnection (asymptotic oblivion)
        particleColor = 'rgba(75, 85, 99, 0.35)';
        radius = 2.0;
      }

      ctxCausal.fillStyle = particleColor;
      ctxCausal.beginPath();
      ctxCausal.arc(pt.px, pt.py, radius, 0, Math.PI * 2);
      ctxCausal.fill();
    });

    // 6. Horizon Labeling Overlay
    const pLabel = project3D(horizonR * 1.02, 0, 0, w, h);
    if (pLabel) {
      ctxCausal.font = '10px "JetBrains Mono", monospace';
      ctxCausal.fillStyle = '#c084fc';
      ctxCausal.fillText(`HORIZON r_CEH = ${(C_LIGHT / ((hubble0 * 1000) / MPC_TO_M) * M_TO_GLY).toFixed(1)} Gly`, pLabel.px + 8, pLabel.py + 3);
    }
  }

  // Draw Asymptotic Redshift Decay Curve
  function renderDecayCanvas() {
    if (!ctxDecay || !canvasDecay) return;
    const w = canvasDecay.width;
    const h = canvasDecay.height;

    ctxDecay.clearRect(0, 0, w, h);

    // Dark panel styling
    ctxDecay.fillStyle = '#05060b';
    ctxDecay.fillRect(0, 0, w, h);

    const padLeft = 60;
    const padRight = 30;
    const padTop = 25;
    const padBottom = 35;
    const plotW = w - padLeft - padRight;
    const plotH = h - padTop - padBottom;

    // Grid lines
    ctxDecay.strokeStyle = 'rgba(168, 85, 247, 0.12)';
    ctxDecay.lineWidth = 1;

    for (let gy = 0; gy <= 4; gy++) {
      const y = padTop + (plotH * gy) / 4;
      ctxDecay.beginPath();
      ctxDecay.moveTo(padLeft, y);
      ctxDecay.lineTo(w - padRight, y);
      ctxDecay.stroke();
    }

    for (let gx = 0; gx <= 5; gx++) {
      const x = padLeft + (plotW * gx) / 5;
      ctxDecay.beginPath();
      ctxDecay.moveTo(x, padTop);
      ctxDecay.lineTo(x, h - padBottom);
      ctxDecay.stroke();
    }

    // Axes
    ctxDecay.strokeStyle = 'rgba(168, 85, 247, 0.4)';
    ctxDecay.lineWidth = 1.5;
    ctxDecay.beginPath();
    ctxDecay.moveTo(padLeft, padTop);
    ctxDecay.lineTo(padLeft, h - padBottom);
    ctxDecay.lineTo(w - padRight, h - padBottom);
    ctxDecay.stroke();

    // Axis Labels
    ctxDecay.font = '9px "JetBrains Mono", monospace';
    ctxDecay.fillStyle = '#64748b';
    ctxDecay.fillText('t = 0', padLeft - 10, h - padBottom + 16);
    ctxDecay.fillText('t = 1/H', padLeft + plotW * 0.2 - 12, h - padBottom + 16);
    ctxDecay.fillText('2/H', padLeft + plotW * 0.4 - 8, h - padBottom + 16);
    ctxDecay.fillText('3/H', padLeft + plotW * 0.6 - 8, h - padBottom + 16);
    ctxDecay.fillText('4/H', padLeft + plotW * 0.8 - 8, h - padBottom + 16);
    ctxDecay.fillText('5/H (Oblivion)', w - padRight - 36, h - padBottom + 16);

    ctxDecay.fillText('ν_0 (Optical)', 8, padTop + 8);
    ctxDecay.fillText('Microwave', 12, padTop + plotH * 0.5);
    ctxDecay.fillText('T_GH (Noise)', 10, h - padBottom - 6);

    // Gibbons-Hawking Quantum Vacuum Floor line
    const floorY = h - padBottom - 8;
    ctxDecay.strokeStyle = 'rgba(244, 63, 94, 0.4)';
    ctxDecay.setLineDash([4, 3]);
    ctxDecay.beginPath();
    ctxDecay.moveTo(padLeft, floorY);
    ctxDecay.lineTo(w - padRight, floorY);
    ctxDecay.stroke();
    ctxDecay.setLineDash([]);

    ctxDecay.fillStyle = 'rgba(244, 63, 94, 0.7)';
    ctxDecay.fillText('GIBBONS-HAWKING THERMAL BATH (2.65 × 10⁻³⁰ K)', padLeft + 12, floorY - 5);

    // Plot Exponential Decay Curve: ν(t) = ν_0 * exp(-H * t)
    const H_factor = (hubble0 / 67.4) * 1.0;
    ctxDecay.beginPath();
    let first = true;

    for (let px = 0; px <= plotW; px += 2) {
      const normX = px / plotW; // 0 to 1 represents 0 to 5/H
      const t_val = normX * 5.0;
      const decay = Math.exp(-H_factor * t_val);

      // Map to vertical coordinate
      const py = padTop + (1.0 - decay) * (plotH - 8);

      if (first) {
        ctxDecay.moveTo(padLeft + px, py);
        first = false;
      } else {
        ctxDecay.lineTo(padLeft + px, py);
      }
    }

    ctxDecay.strokeStyle = '#38bdf8';
    ctxDecay.lineWidth = 2.5;
    ctxDecay.stroke();

    // Fill area under curve
    ctxDecay.lineTo(w - padRight, h - padBottom);
    ctxDecay.lineTo(padLeft, h - padBottom);
    ctxDecay.closePath();
    const fillGrad = ctxDecay.createLinearGradient(padLeft, padTop, padLeft, h - padBottom);
    fillGrad.addColorStop(0, 'rgba(56, 189, 248, 0.25)');
    fillGrad.addColorStop(0.5, 'rgba(168, 85, 247, 0.15)');
    fillGrad.addColorStop(1, 'rgba(244, 63, 94, 0.02)');
    ctxDecay.fillStyle = fillGrad;
    ctxDecay.fill();

    // Dynamic marker along curve
    const cycleT = (animTime * 0.4) % 5.0;
    const markerNormX = cycleT / 5.0;
    const markerDecay = Math.exp(-H_factor * cycleT);
    const markerX = padLeft + markerNormX * plotW;
    const markerY = padTop + (1.0 - markerDecay) * (plotH - 8);

    ctxDecay.fillStyle = '#facc15';
    ctxDecay.beginPath();
    ctxDecay.arc(markerX, markerY, 5, 0, Math.PI * 2);
    ctxDecay.fill();
    ctxDecay.strokeStyle = 'rgba(250, 204, 21, 0.6)';
    ctxDecay.stroke();

    // Pulsing readout tag
    ctxDecay.fillStyle = '#facc15';
    ctxDecay.fillText(`ν(t) = ${(markerDecay * 100).toFixed(1)}%`, markerX + 8, markerY - 4);
  }

  // Real-time Web Audio API Engine
  function initAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    gainMaster = audioCtx.createGain();
    gainMaster.gain.setValueAtTime(0.0, audioCtx.currentTime);
    gainMaster.connect(audioCtx.destination);

    // 1. Horizon Infrasound Sub-Drone (14.39 Hz transposed up 1 octave to 28.78 Hz for speaker reproduction)
    oscDrone = audioCtx.createOscillator();
    oscDrone.type = 'sine';
    const m = getPhysicalMetrics();
    oscDrone.frequency.setValueAtTime(m.r_ceh_gly * 2.0, audioCtx.currentTime);

    const gainDrone = audioCtx.createGain();
    gainDrone.gain.setValueAtTime(0.4, audioCtx.currentTime);
    oscDrone.connect(gainDrone);
    gainDrone.connect(gainMaster);
    oscDrone.start();

    // 2. Exponential Redshift Carrier Oscillator
    oscCarrier = audioCtx.createOscillator();
    oscCarrier.type = 'sawtooth';
    oscCarrier.frequency.setValueAtTime(432.0, audioCtx.currentTime);

    const filterCarrier = audioCtx.createBiquadFilter();
    filterCarrier.type = 'lowpass';
    filterCarrier.frequency.setValueAtTime(600.0, audioCtx.currentTime);

    const gainCarrier = audioCtx.createGain();
    gainCarrier.gain.setValueAtTime(0.18, audioCtx.currentTime);

    oscCarrier.connect(filterCarrier);
    filterCarrier.connect(gainCarrier);
    gainCarrier.connect(gainMaster);
    oscCarrier.start();

    // 3. Gibbons-Hawking Quantum Vacuum Noise Generator
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      output[i] = (b0 + b1 + b2) * 0.12;
    }

    noiseNode = audioCtx.createBufferSource();
    noiseNode.buffer = noiseBuffer;
    noiseNode.loop = true;

    filterNoise = audioCtx.createBiquadFilter();
    filterNoise.type = 'bandpass';
    filterNoise.frequency.setValueAtTime(140.0, audioCtx.currentTime);
    filterNoise.Q.setValueAtTime(1.8, audioCtx.currentTime);

    const gainNoise = audioCtx.createGain();
    gainNoise.gain.setValueAtTime(0.09, audioCtx.currentTime);

    noiseNode.connect(filterNoise);
    filterNoise.connect(gainNoise);
    gainNoise.connect(gainMaster);
    noiseNode.start();

    // Continuous glide loop for carrier
    scheduleCarrierGlides();
  }

  function scheduleCarrierGlides() {
    if (!audioCtx || !oscCarrier) return;
    const now = audioCtx.currentTime;
    const duration = 6.0;
    const H_norm = hubble0 / 67.4;

    oscCarrier.frequency.cancelScheduledValues(now);
    oscCarrier.frequency.setValueAtTime(432.0, now);
    // Exponential falloff
    oscCarrier.frequency.exponentialRampToValueAtTime(Math.max(20.0, 432.0 * Math.exp(-2.2 * H_norm)), now + duration);

    setTimeout(() => {
      if (isPlaying) scheduleCarrierGlides();
    }, duration * 1000);
  }

  function toggleAudio() {
    if (!audioCtx) initAudio();

    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    isPlaying = !isPlaying;
    if (isPlaying) {
      gainMaster.gain.setTargetAtTime(0.7, audioCtx.currentTime, 0.4);
      scheduleCarrierGlides();
      if (synthBtn) {
        synthBtn.textContent = 'Mute Horizon Atmosphere';
        synthBtn.style.background = 'rgba(244, 63, 94, 0.2)';
        synthBtn.style.borderColor = '#f43f5e';
        synthBtn.style.color = '#f43f5e';
      }
    } else {
      gainMaster.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.2);
      if (synthBtn) {
        synthBtn.textContent = 'Synthesize Horizon Atmosphere';
        synthBtn.style.background = 'rgba(168, 85, 247, 0.08)';
        synthBtn.style.borderColor = '#a855f7';
        synthBtn.style.color = '#a855f7';
      }
    }
  }

  // Event Listeners
  if (hubbleSlider) {
    hubbleSlider.addEventListener('input', (e) => {
      hubble0 = parseFloat(e.target.value);
      updateMetricsDisplay();
    });
  }

  if (synthBtn) {
    synthBtn.addEventListener('click', toggleAudio);
  }

  // Mouse Interaction for 3D Orbit
  if (canvasCausal) {
    canvasCausal.addEventListener('mousedown', (e) => {
      isDragging = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const dx = e.clientX - lastMouseX;
      const dy = e.clientY - lastMouseY;
      rotY += dx * 0.01;
      rotX += dy * 0.01;
      rotX = Math.max(-1.1, Math.min(1.1, rotX));
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });

    // Touch support
    canvasCausal.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        isDragging = true;
        lastMouseX = e.touches[0].clientX;
        lastMouseY = e.touches[0].clientY;
      }
    });

    window.addEventListener('touchend', () => {
      isDragging = false;
    });

    window.addEventListener('touchmove', (e) => {
      if (!isDragging || e.touches.length !== 1) return;
      const dx = e.touches[0].clientX - lastMouseX;
      const dy = e.touches[0].clientY - lastMouseY;
      rotY += dx * 0.01;
      rotX += dy * 0.01;
      rotX = Math.max(-1.1, Math.min(1.1, rotX));
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    });
  }

  // Animation Loop
  function animate() {
    animTime += 0.018;
    if (!isDragging) {
      rotY += 0.0025; // Gentle slow rotation
    }

    renderCausalCanvas();
    renderDecayCanvas();
    requestAnimationFrame(animate);
  }

  // Initialize
  updateMetricsDisplay();
  animate();

})();
