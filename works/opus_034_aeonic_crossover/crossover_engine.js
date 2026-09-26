/**
 * OPUS-034: THE AEONIC CROSSOVER
 * Chamber 14: Interactive Penrose Crossover & Hawking Point Simulator
 * Real-time Canvas 2D + Web Audio API Engine
 * Zero external dependencies.
 */

(function() {
  'use strict';

  const canvas = document.getElementById('crossover-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // Simulation State
  const state = {
    omega: 0.56,              // Conformal factor Omega
    strain: 0.082,            // Quadrupole shear strain h+
    selectedRing: 'all',      // 'all', 'r1', 'r2', 'r3'
    showStokes: true,         // Display polarization vectors
    showWeylLines: true,      // Display Weyl curvature flowlines
    isPlayingAudio: false,
    audioInitialized: false,
    centerX: 0,
    centerY: 0,
    isDragging: false,
    dragStartX: 0,
    dragStartY: 0,
    time: 0
  };

  // Audio Context & Nodes
  let audioCtx = null;
  let masterGain = null;
  let oscCarrier = null;
  let oscQNM = null;
  let oscTremolo = null;
  let tremoloGain = null;
  let noiseNode = null;

  function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * (window.devicePixelRatio || 1);
    canvas.height = rect.height * (window.devicePixelRatio || 1);
    if (!state.centerX && !state.centerY) {
      state.centerX = canvas.width * 0.5;
      state.centerY = canvas.height * 0.5;
    }
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // Mouse / Touch Interaction
  canvas.addEventListener('mousedown', (e) => {
    state.isDragging = true;
    state.dragStartX = e.clientX * (window.devicePixelRatio || 1) - state.centerX;
    state.dragStartY = e.clientY * (window.devicePixelRatio || 1) - state.centerY;
  });

  window.addEventListener('mousemove', (e) => {
    if (!state.isDragging) return;
    state.centerX = e.clientX * (window.devicePixelRatio || 1) - state.dragStartX;
    state.centerY = e.clientY * (window.devicePixelRatio || 1) - state.dragStartY;
  });

  window.addEventListener('mouseup', () => {
    state.isDragging = false;
  });

  // Touch Support
  canvas.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      state.isDragging = true;
      state.dragStartX = e.touches[0].clientX * (window.devicePixelRatio || 1) - state.centerX;
      state.dragStartY = e.touches[0].clientY * (window.devicePixelRatio || 1) - state.centerY;
    }
  }, { passive: true });

  window.addEventListener('touchmove', (e) => {
    if (!state.isDragging || e.touches.length !== 1) return;
    state.centerX = e.touches[0].clientX * (window.devicePixelRatio || 1) - state.dragStartX;
    state.centerY = e.touches[0].clientY * (window.devicePixelRatio || 1) - state.dragStartY;
  }, { passive: true });

  window.addEventListener('touchend', () => {
    state.isDragging = false;
  });

  // Web Audio Initialization
  function initAudio() {
    if (state.audioInitialized) return;
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();

      masterGain = audioCtx.createGain();
      masterGain.gain.setValueAtTime(0.001, audioCtx.currentTime);
      masterGain.connect(audioCtx.destination);

      // Carrier Oscillator (43.2 Hz fundamental)
      oscCarrier = audioCtx.createOscillator();
      oscCarrier.type = 'sine';
      oscCarrier.frequency.setValueAtTime(43.2, audioCtx.currentTime);

      // QNM Ringdown Oscillator (287.89 Hz)
      oscQNM = audioCtx.createOscillator();
      oscQNM.type = 'sine';
      oscQNM.frequency.setValueAtTime(287.89, audioCtx.currentTime);

      const qnmGain = audioCtx.createGain();
      qnmGain.gain.setValueAtTime(0.25, audioCtx.currentTime);
      oscQNM.connect(qnmGain);

      // Tremolo LFO (4.2 Hz Hawking Ring Beat)
      oscTremolo = audioCtx.createOscillator();
      oscTremolo.frequency.setValueAtTime(4.2, audioCtx.currentTime);

      tremoloGain = audioCtx.createGain();
      tremoloGain.gain.setValueAtTime(0.4, audioCtx.currentTime);
      oscTremolo.connect(tremoloGain.gain);

      // Connect Carrier through Tremolo
      oscCarrier.connect(tremoloGain);
      tremoloGain.connect(masterGain);
      qnmGain.connect(masterGain);

      // White/Brownian noise buffer for CMB hiss
      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99 * b0 + white * 0.05;
        output[i] = b0 * 0.15;
      }
      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = noiseBuffer;
      noiseNode.loop = true;
      const noiseGain = audioCtx.createGain();
      noiseGain.gain.setValueAtTime(0.18, audioCtx.currentTime);
      noiseNode.connect(noiseGain);
      noiseGain.connect(masterGain);

      oscCarrier.start();
      oscQNM.start();
      oscTremolo.start();
      noiseNode.start();

      state.audioInitialized = true;
    } catch (e) {
      console.warn("Web Audio initialization failed:", e);
    }
  }

  function toggleAudio() {
    if (!state.audioInitialized) initAudio();
    if (!audioCtx) return;

    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    const btn = document.getElementById('btn-audio-toggle');
    if (!state.isPlayingAudio) {
      masterGain.gain.setTargetAtTime(0.75, audioCtx.currentTime, 0.2);
      state.isPlayingAudio = true;
      if (btn) btn.textContent = '⏸ Mute Chamber Acoustic Suite';
    } else {
      masterGain.gain.setTargetAtTime(0.001, audioCtx.currentTime, 0.2);
      state.isPlayingAudio = false;
      if (btn) btn.textContent = '▶ Engage Chamber Acoustic Suite';
    }
  }

  // Update Telemetry HUD
  function updateTelemetry() {
    const elOmega = document.getElementById('telem-omega');
    const elWeyl = document.getElementById('telem-weyl');
    const elVar = document.getElementById('telem-var');
    const elAeon = document.getElementById('telem-aeon');

    if (elOmega) elOmega.textContent = state.omega.toFixed(3);
    if (elWeyl) {
      const weylVal = Math.pow(state.omega, 1.8) * (1.0 - state.omega * 0.4);
      elWeyl.textContent = weylVal.toFixed(4);
    }
    if (elVar) {
      elVar.textContent = (0.68 + (1.0 - state.omega) * 0.12).toFixed(3);
    }
    if (elAeon) {
      elAeon.textContent = state.omega < 0.2 ? 'Aeon n+1 (Newborn Fireball)' : 'Aeon n (Cold Massless Future)';
    }

    // Update real-time audio modulation
    if (state.audioInitialized && audioCtx && state.isPlayingAudio) {
      const targetCarrier = 43.2 * (0.8 + state.omega * 0.6);
      oscCarrier.frequency.setTargetAtTime(targetCarrier, audioCtx.currentTime, 0.1);
      const targetQNM = 287.89 * (0.5 + (1.0 - state.omega) * 0.8);
      oscQNM.frequency.setTargetAtTime(targetQNM, audioCtx.currentTime, 0.1);
    }
  }

  // Animation Loop
  function draw() {
    state.time += 0.015;
    const W = canvas.width;
    const H = canvas.height;

    // 1. Clear background (Cosmic Deep Indigo)
    ctx.fillStyle = '#03050c';
    ctx.fillRect(0, 0, W, H);

    // 2. Dual-Conformal Background Hemispheres
    const grad = ctx.createLinearGradient(0, 0, W, 0);
    grad.addColorStop(0.0, 'rgba(8, 14, 32, 0.95)');    // Cold prior aeon
    grad.addColorStop(0.5, 'rgba(18, 28, 55, 0.6)');    // Crossover bridge Sigma
    grad.addColorStop(1.0, 'rgba(42, 28, 16, 0.95)');   // Hot newborn aeon
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // 3. Central Hawking Point & Rings
    const cx = state.centerX;
    const cy = state.centerY;
    const scale = (W / 1920) * (0.6 + state.omega * 0.8);

    const rings = [
      { id: 'r1', deg: 4.2, r: 4.2 * 26.0 * scale, color: 'rgba(56, 215, 208, 0.85)' },
      { id: 'r2', deg: 11.8, r: 11.8 * 26.0 * scale, color: 'rgba(212, 175, 55, 0.85)' },
      { id: 'r3', deg: 24.5, r: 24.5 * 26.0 * scale, color: 'rgba(140, 185, 245, 0.75)' }
    ];

    // Render Concentric Variance Suppression Zones
    rings.forEach((ring) => {
      if (state.selectedRing !== 'all' && state.selectedRing !== ring.id) return;

      ctx.save();
      ctx.beginPath();
      // Quadrupole elliptical deformation
      const numPoints = 120;
      for (let p = 0; p <= numPoints; p++) {
        const phi = (p / numPoints) * Math.PI * 2;
        const strainVal = 1.0 + state.strain * Math.cos(2.0 * phi);
        const curR = ring.r * strainVal;
        const px = cx + Math.cos(phi) * curR;
        const py = cy + Math.sin(phi) * curR;
        if (p === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();

      // Variance suppression aura
      ctx.lineWidth = 14 * scale;
      ctx.strokeStyle = 'rgba(6, 12, 26, 0.75)'; // Stillness cooling
      ctx.stroke();

      // Sharp polarization ring edge
      ctx.lineWidth = 2.2 * scale;
      ctx.strokeStyle = ring.color;
      ctx.shadowColor = ring.color;
      ctx.shadowBlur = 12 * scale;
      ctx.stroke();
      ctx.restore();

      // Render Stokes Q/U fine polarization ticks if enabled
      if (state.showStokes) {
        ctx.save();
        ctx.strokeStyle = 'rgba(220, 240, 255, 0.45)';
        ctx.lineWidth = 1.0;
        const numTicks = 48;
        for (let t = 0; t < numTicks; t++) {
          const phi = (t / numTicks) * Math.PI * 2;
          const strainVal = 1.0 + state.strain * Math.cos(2.0 * phi);
          const baseR = ring.r * strainVal;
          const px = cx + Math.cos(phi) * baseR;
          const py = cy + Math.sin(phi) * baseR;

          // Tangential polarization angle
          const tickLen = 8.0 * scale;
          const tangAngle = phi + Math.PI * 0.5 + 0.15 * Math.sin(4.0 * phi);
          ctx.beginPath();
          ctx.moveTo(px - Math.cos(tangAngle) * tickLen, py - Math.sin(tangAngle) * tickLen);
          ctx.lineTo(px + Math.cos(tangAngle) * tickLen, py + Math.sin(tangAngle) * tickLen);
          ctx.stroke();
        }
        ctx.restore();
      }
    });

    // 4. Weyl Curvature Streamlines (C_abcd -> 0)
    if (state.showWeylLines) {
      ctx.save();
      ctx.strokeStyle = 'rgba(56, 215, 208, 0.18)';
      ctx.lineWidth = 1.2;
      for (let i = -6; i <= 6; i++) {
        ctx.beginPath();
        const startY = cy + i * 45 * scale;
        for (let x = 0; x < W; x += 15) {
          const wave = Math.sin(x * 0.006 + state.time + i * 0.4) * 22 * scale;
          const y = startY + wave;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      ctx.restore();
    }

    // 5. Central Hawking Point Focal Singularity
    ctx.save();
    const coreGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 35 * scale);
    coreGrad.addColorStop(0.0, '#ffffff');
    coreGrad.addColorStop(0.2, '#38d7d0');
    coreGrad.addColorStop(0.6, 'rgba(212, 175, 55, 0.4)');
    coreGrad.addColorStop(1.0, 'transparent');
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, 35 * scale, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    updateTelemetry();
    requestAnimationFrame(draw);
  }

  // UI Event Bindings
  function bindControls() {
    const sliderOmega = document.getElementById('slider-omega');
    if (sliderOmega) {
      sliderOmega.addEventListener('input', (e) => {
        state.omega = parseFloat(e.target.value);
      });
    }

    const sliderStrain = document.getElementById('slider-strain');
    if (sliderStrain) {
      sliderStrain.addEventListener('input', (e) => {
        state.strain = parseFloat(e.target.value);
      });
    }

    const ringBtns = document.querySelectorAll('.ring-select-btn');
    ringBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        ringBtns.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        state.selectedRing = e.target.getAttribute('data-ring');
      });
    });

    const chkStokes = document.getElementById('chk-stokes');
    if (chkStokes) {
      chkStokes.addEventListener('change', (e) => {
        state.showStokes = e.target.checked;
      });
    }

    const chkWeyl = document.getElementById('chk-weyl');
    if (chkWeyl) {
      chkWeyl.addEventListener('change', (e) => {
        state.showWeylLines = e.target.checked;
      });
    }

    const btnAudio = document.getElementById('btn-audio-toggle');
    if (btnAudio) {
      btnAudio.addEventListener('click', toggleAudio);
    }
  }

  bindControls();
  requestAnimationFrame(draw);
})();

