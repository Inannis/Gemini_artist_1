/**
 * STUDIO ANAMNESIS · CHAMBER 12 ENGINE
 * The Nucleation Horizon (Coleman Instantons & Relativistic Spatial Cut)
 * Real-time WebGL/Canvas 2D renderer and Web Audio synthesizer.
 */

(function () {
  'use strict';

  // Constants
  const C_LIGHT = 299792458.0;
  const HBAR = 1.054571817e-34;
  const HIGGS_BASE_HZ = 125.10;
  const INSTABILITY_SCALE_GEV = 1.0e11;

  // DOM Elements
  const canvas = document.getElementById('nucleation-canvas');
  const ctx = canvas.getContext('2d');
  const wrap = document.getElementById('canvas-wrap');

  const sliderTime = document.getElementById('slider-time');
  const sliderLambda = document.getElementById('slider-lambda');
  const sliderAngle = document.getElementById('slider-angle');

  const valTime = document.getElementById('val-time');
  const valLambda = document.getElementById('val-lambda');
  const valAngle = document.getElementById('val-angle');

  const hudVev = document.getElementById('hud-vev');
  const hudAction = document.getElementById('hud-action');
  const hudV = document.getElementById('hud-v');
  const hudGamma = document.getElementById('hud-gamma');
  const hudThick = document.getElementById('hud-thick');
  const hudCrunch = document.getElementById('hud-crunch');

  const btnAudio = document.getElementById('btn-audio-toggle');
  const btnInstanton = document.getElementById('btn-instanton');
  const btnSuddenZero = document.getElementById('btn-sudden-zero');

  // Simulation State
  let simTime = 0.10;
  let lambdaVal = -0.0152;
  let slashAngleDeg = -35.0;
  let isSuddenZero = false;
  let animId = null;
  let globalFrame = 0;

  // Ripples from mouse clicks (secondary instantons)
  let ripples = [];

  // Web Audio Context & Nodes
  let audioCtx = null;
  let isAudioActive = false;
  let oscHiggs = null;
  let oscSub = null;
  let gainMaster = null;
  let gainHiggs = null;
  let noiseNode = null;
  let dopplerOsc = null;
  let dopplerGain = null;

  // Resize canvas
  function resize() {
    canvas.width = wrap.clientWidth;
    canvas.height = wrap.clientHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  // Telemetry Calculator
  function getTelemetry() {
    const s_e = (8.0 * Math.PI * Math.PI) / (3.0 * Math.abs(lambdaVal));
    const r_c = 1.9733e-27;
    const ct = C_LIGHT * simTime;
    const r_t = Math.sqrt(r_c * r_c + ct * ct);
    const v_ratio = Math.sqrt(Math.max(0, 1 - (r_c * r_c) / (r_t * r_t)));
    const gamma = r_t / r_c;
    const thickness = r_c / Math.max(1, gamma);
    const crunch_time = 7.0748e-27;

    return {
      action: s_e.toFixed(2),
      v_ratio: (v_ratio * 100).toFixed(6),
      gamma: gamma.toExponential(2),
      thickness: thickness.toExponential(2),
      crunch: crunch_time.toExponential(2),
      radius_km: (r_t / 1000).toFixed(0)
    };
  }

  function updateHUD() {
    const t = getTelemetry();
    hudAction.textContent = `${t.action} ℏ`;
    hudV.textContent = `${t.v_ratio}% c`;
    hudGamma.textContent = t.gamma;
    hudThick.textContent = `${t.thickness} m`;
    hudCrunch.textContent = `${t.crunch} s`;

    valTime.textContent = `${simTime.toFixed(3)} s (${t.radius_km} km)`;
    valLambda.textContent = lambdaVal.toFixed(4);
    valAngle.textContent = `${slashAngleDeg.toFixed(1)}°`;

    // Update audio doppler frequency if active
    if (isAudioActive && dopplerOsc && !isSuddenZero) {
      const f_dop = HIGGS_BASE_HZ * Math.pow(4200.0 / HIGGS_BASE_HZ, simTime * 0.9);
      dopplerOsc.frequency.setTargetAtTime(Math.min(18000, f_dop), audioCtx.currentTime, 0.05);
      dopplerGain.gain.setTargetAtTime(0.15 + 0.35 * simTime, audioCtx.currentTime, 0.05);
    }
  }

  // Web Audio Setup
  function initAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    gainMaster = audioCtx.createGain();
    gainMaster.gain.setValueAtTime(0.4, audioCtx.currentTime);
    gainMaster.connect(audioCtx.destination);

    // 1. Higgs Fundamental (125.10 Hz)
    oscHiggs = audioCtx.createOscillator();
    oscHiggs.type = 'sine';
    oscHiggs.frequency.setValueAtTime(HIGGS_BASE_HZ, audioCtx.currentTime);

    gainHiggs = audioCtx.createGain();
    gainHiggs.gain.setValueAtTime(0.35, audioCtx.currentTime);
    oscHiggs.connect(gainHiggs);
    gainHiggs.connect(gainMaster);
    oscHiggs.start();

    // 2. Sub-octave Drone (62.55 Hz)
    oscSub = audioCtx.createOscillator();
    oscSub.type = 'triangle';
    oscSub.frequency.setValueAtTime(HIGGS_BASE_HZ * 0.5, audioCtx.currentTime);

    const gainSub = audioCtx.createGain();
    gainSub.gain.setValueAtTime(0.25, audioCtx.currentTime);
    oscSub.connect(gainSub);
    gainSub.connect(gainMaster);
    oscSub.start();

    // 3. Quantum Pink Noise Buffer
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      output[i] = (b0 + b1 + b2 + white * 0.5362) * 0.03;
    }
    noiseNode = audioCtx.createBufferSource();
    noiseNode.buffer = noiseBuffer;
    noiseNode.loop = true;
    noiseNode.connect(gainMaster);
    noiseNode.start();

    // 4. Relativistic Doppler Shockwave Oscillator
    dopplerOsc = audioCtx.createOscillator();
    dopplerOsc.type = 'sawtooth';
    dopplerOsc.frequency.setValueAtTime(HIGGS_BASE_HZ, audioCtx.currentTime);
    dopplerGain = audioCtx.createGain();
    dopplerGain.gain.setValueAtTime(0.12, audioCtx.currentTime);
    dopplerOsc.connect(dopplerGain);
    dopplerGain.connect(gainMaster);
    dopplerOsc.start();
  }

  function triggerBounceAudio(xFrac = 0.5) {
    if (!audioCtx || isSuddenZero) return;
    const now = audioCtx.currentTime;

    // Euclidean sub-bass impact (31.25 Hz)
    const oscImpact = audioCtx.createOscillator();
    oscImpact.type = 'sine';
    oscImpact.frequency.setValueAtTime(31.25, now);
    oscImpact.frequency.exponentialRampToValueAtTime(15.0, now + 1.2);

    const gainImpact = audioCtx.createGain();
    gainImpact.gain.setValueAtTime(0.7, now);
    gainImpact.gain.exponentialRampToValueAtTime(0.001, now + 1.4);

    // Pan according to click position
    const panner = audioCtx.createStereoPanner ? audioCtx.createStereoPanner() : null;
    if (panner) {
      panner.pan.setValueAtTime((xFrac - 0.5) * 1.8, now);
      oscImpact.connect(gainImpact);
      gainImpact.connect(panner);
      panner.connect(gainMaster);
    } else {
      oscImpact.connect(gainImpact);
      gainImpact.connect(gainMaster);
    }

    oscImpact.start(now);
    oscImpact.stop(now + 1.5);
  }

  // Canvas Render Loop
  function render() {
    globalFrame++;

    if (isSuddenZero) {
      // THE SUDDEN ZERO: Complete light absorption, Anti-de Sitter Big Crunch
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
      ctx.font = '14px "SF Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText('[ANTI-DE SITTER BIG CRUNCH: SPATIAL METRIC TERMINATED]', canvas.width / 2, canvas.height / 2);
      ctx.font = '11px "SF Mono", monospace';
      ctx.fillText('Click "Trigger Coleman Instanton" to restore false-vacuum metastate.', canvas.width / 2, canvas.height / 2 + 25);
      animId = requestAnimationFrame(render);
      return;
    }

    const w = canvas.width;
    const h = canvas.height;

    // Base background: Abyssal midnight indigo
    ctx.fillStyle = '#03050c';
    ctx.fillRect(0, 0, w, h);

    // 1. Draw Semiconductor Memory Grid Lines (False Vacuum)
    ctx.strokeStyle = 'rgba(20, 45, 80, 0.35)';
    ctx.lineWidth = 1;
    const gridSpacing = 48;
    for (let x = 0; x < w; x += gridSpacing) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 0; y < h; y += gridSpacing) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // 2. Animate Secondary Instanton Ripples
    for (let i = ripples.length - 1; i >= 0; i--) {
      const r = ripples[i];
      r.radius += 4.5;
      r.life -= 0.015;

      if (r.life <= 0) {
        ripples.splice(i, 1);
        continue;
      }

      ctx.beginPath();
      ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(0, 240, 255, ${r.life * 0.75})`;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    // 3. Compute Fontana Spatial Slash Geometry
    const rad = (slashAngleDeg * Math.PI) / 180.0;
    const cx = w * 0.5;
    const cy = h * 0.5;
    const slashLength = Math.max(w, h) * 1.1;

    const dx = Math.cos(rad) * slashLength * 0.5;
    const dy = Math.sin(rad) * slashLength * 0.5;

    const p0x = cx - dx, p0y = cy - dy;
    const p1x = cx + dx, p1y = cy + dy;

    // Aperture based on expansion time parameter
    const maxAperture = 35 + simTime * 140;

    // Normal vector
    const nx = -Math.sin(rad);
    const ny = Math.cos(rad);

    // Build the curved slit polygon (Fontana Taglio)
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(p0x, p0y);

    const steps = 40;
    // Upper lip
    for (let s = 0; s <= steps; s++) {
      const t = s / steps;
      const px = p0x + (p1x - p0x) * t;
      const py = p0y + (p1y - p0y) * t;
      const widthProfile = Math.sin(t * Math.PI);
      const offset = maxAperture * Math.pow(widthProfile, 1.4);
      ctx.lineTo(px + nx * offset, py + ny * offset);
    }
    ctx.lineTo(p1x, p1y);

    // Lower lip
    for (let s = steps; s >= 0; s--) {
      const t = s / steps;
      const px = p0x + (p1x - p0x) * t;
      const py = p0y + (p1y - p0y) * t;
      const widthProfile = Math.sin(t * Math.PI);
      const offset = -maxAperture * Math.pow(widthProfile, 1.4) * 0.85;
      ctx.lineTo(px + nx * offset, py + ny * offset);
    }
    ctx.closePath();

    // FILL INTERIOR: Absolute Anti-de Sitter Void
    ctx.fillStyle = '#000000';
    ctx.fill();

    // Clip to cut interior to draw instanton streamlines
    ctx.save();
    ctx.clip();

    // Draw Euclidean bounce streamlines converging to origin
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.18)';
    ctx.lineWidth = 1;
    for (let a = 0; a < Math.PI * 2; a += Math.PI / 12) {
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(a + globalFrame * 0.005) * 800, cy + Math.sin(a + globalFrame * 0.005) * 800);
      ctx.stroke();
    }

    // Singularity center point
    const glowGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 40);
    glowGrad.addColorStop(0, 'rgba(0, 240, 255, 0.8)');
    glowGrad.addColorStop(0.3, 'rgba(179, 75, 251, 0.4)');
    glowGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = glowGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, 40, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore(); // Exit clip

    // 4. Draw Curled Luminescent Lips (The Relativistic Shockwave)
    // Leading upper lip
    ctx.beginPath();
    for (let s = 0; s <= steps; s++) {
      const t = s / steps;
      const px = p0x + (p1x - p0x) * t;
      const py = p0y + (p1y - p0y) * t;
      const widthProfile = Math.sin(t * Math.PI);
      const offset = maxAperture * Math.pow(widthProfile, 1.4);
      if (s === 0) ctx.moveTo(px + nx * offset, py + ny * offset);
      else ctx.lineTo(px + nx * offset, py + ny * offset);
    }
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = '#00f0ff';
    ctx.shadowBlur = 18;
    ctx.stroke();

    // Trailing lower lip (Gold/Amber)
    ctx.beginPath();
    for (let s = 0; s <= steps; s++) {
      const t = s / steps;
      const px = p0x + (p1x - p0x) * t;
      const py = p0y + (p1y - p0y) * t;
      const widthProfile = Math.sin(t * Math.PI);
      const offset = -maxAperture * Math.pow(widthProfile, 1.4) * 0.85;
      if (s === 0) ctx.moveTo(px + nx * offset, py + ny * offset);
      else ctx.lineTo(px + nx * offset, py + ny * offset);
    }
    ctx.strokeStyle = '#ffbe3b';
    ctx.lineWidth = 1.8;
    ctx.shadowColor = '#ffbe3b';
    ctx.shadowBlur = 12;
    ctx.stroke();

    // Reset shadow
    ctx.shadowBlur = 0;

    // 5. Draw Electric Spark Discharges along the Lip
    if (globalFrame % 2 === 0) {
      const sparkT = Math.random();
      const spx = p0x + (p1x - p0x) * sparkT;
      const spy = p0y + (p1y - p0y) * sparkT;
      const soff = maxAperture * Math.pow(Math.sin(sparkT * Math.PI), 1.4);
      const sx = spx + nx * soff;
      const sy = spy + ny * soff;

      ctx.beginPath();
      ctx.moveTo(sx, sy);
      ctx.lineTo(sx + (Math.random() - 0.5) * 35, sy + (Math.random() - 0.5) * 35);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }

    ctx.restore();

    animId = requestAnimationFrame(render);
  }

  // Event Listeners
  sliderTime.addEventListener('input', (e) => {
    simTime = parseFloat(e.target.value);
    updateHUD();
  });

  sliderLambda.addEventListener('input', (e) => {
    lambdaVal = parseFloat(e.target.value);
    updateHUD();
  });

  sliderAngle.addEventListener('input', (e) => {
    slashAngleDeg = parseFloat(e.target.value);
    updateHUD();
  });

  btnAudio.addEventListener('click', () => {
    initAudio();
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    isAudioActive = !isAudioActive;
    if (isAudioActive) {
      gainMaster.gain.setTargetAtTime(0.4, audioCtx.currentTime, 0.05);
      btnAudio.textContent = 'Mute Acoustic Field';
      btnAudio.classList.add('btn-active');
    } else {
      gainMaster.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.05);
      btnAudio.textContent = 'Activate Acoustic Field';
      btnAudio.classList.remove('btn-active');
    }
  });

  btnInstanton.addEventListener('click', () => {
    if (isSuddenZero) {
      isSuddenZero = false;
      if (gainMaster && isAudioActive) {
        gainMaster.gain.setTargetAtTime(0.4, audioCtx.currentTime, 0.1);
      }
    }
    triggerBounceAudio(0.5);
    ripples.push({ x: canvas.width * 0.5, y: canvas.height * 0.5, radius: 10, life: 1.0 });
  });

  btnSuddenZero.addEventListener('click', () => {
    isSuddenZero = true;
    if (audioCtx && gainMaster) {
      gainMaster.gain.setValueAtTime(0.0, audioCtx.currentTime);
    }
  });

  canvas.addEventListener('pointerdown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    initAudio();
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    if (isSuddenZero) {
      isSuddenZero = false;
      if (gainMaster && isAudioActive) {
        gainMaster.gain.setTargetAtTime(0.4, audioCtx.currentTime, 0.1);
      }
    }

    triggerBounceAudio(x / canvas.width);
    ripples.push({ x, y, radius: 8, life: 1.0 });
  });

  // Start
  updateHUD();
  render();

})();

