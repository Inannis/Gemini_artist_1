/* =========================================================================
   STUDIO ANAMNESIS · OPUS-031
   THE PAGE HORIZON: Kerr Relativistic Raytracer & Page Curve Simulator
   Real-Time WebGL / Canvas / Web Audio Simulation Engine (Chamber 11)
   ========================================================================= */

(function () {
  'use strict';

  let cvs, ctx;
  let audioCtx = null;
  let isAudioActive = false;

  // Physical State Variables
  let spinA = 0.940;           // Kerr spin parameter a/M
  let inclinationDeg = 74.0;   // Observer inclination
  let pageTimeRatio = 0.54;    // Current evaporation state t/t_evap
  let qnmPulseTime = -999.0;   // Time of last gravitational strike
  let animTime = 0.0;

  // Audio Nodes
  let masterGain = null;
  let droneOsc1 = null, droneOsc2 = null;
  let noiseNode = null, noiseGain = null;
  let qnmGain = null;

  function init() {
    cvs = document.getElementById('horizon-canvas');
    if (!cvs) return;
    ctx = cvs.getContext('2d');
    resize();
    window.addEventListener('resize', resize);

    // Canvas click to strike spacetime
    cvs.addEventListener('pointerdown', function (e) {
      triggerQnmStrike();
    });

    setupControls();
    requestAnimationFrame(renderLoop);
  }

  function resize() {
    if (!cvs) return;
    const rect = cvs.getBoundingClientRect();
    cvs.width = rect.width * window.devicePixelRatio;
    cvs.height = rect.height * window.devicePixelRatio;
  }

  function setupControls() {
    const spinSlider = document.getElementById('spin-slider');
    const incSlider = document.getElementById('inc-slider');
    const pageSlider = document.getElementById('page-slider');
    const audioBtn = document.getElementById('audio-toggle-btn');
    const strikeBtn = document.getElementById('strike-btn');

    if (spinSlider) {
      spinSlider.addEventListener('input', function (e) {
        spinA = parseFloat(e.target.value);
        document.getElementById('spin-val').textContent = spinA.toFixed(3);
      });
    }

    if (incSlider) {
      incSlider.addEventListener('input', function (e) {
        inclinationDeg = parseFloat(e.target.value);
        document.getElementById('inc-val').textContent = inclinationDeg.toFixed(1) + '°';
      });
    }

    if (pageSlider) {
      pageSlider.addEventListener('input', function (e) {
        pageTimeRatio = parseFloat(e.target.value);
        document.getElementById('page-val').textContent = pageTimeRatio.toFixed(2);
        updateEntropyStatus();
      });
    }

    if (audioBtn) {
      audioBtn.addEventListener('click', toggleAudio);
    }

    if (strikeBtn) {
      strikeBtn.addEventListener('click', triggerQnmStrike);
    }
  }

  function updateEntropyStatus() {
    const statusEl = document.getElementById('entropy-status');
    if (!statusEl) return;
    if (pageTimeRatio < 0.52) {
      statusEl.textContent = "Pre-Page Epoch: Monotonic Entanglement Growth (Hawking Radiation Thermal)";
      statusEl.style.color = "#ff9955";
    } else if (pageTimeRatio <= 0.56) {
      statusEl.textContent = "Page Time Critical Transition: Quantum Extremal Surface Nucleation";
      statusEl.style.color = "#00ffcc";
    } else {
      statusEl.textContent = "Post-Page Epoch: Unitary Radiation Purification & Memory Extraction";
      statusEl.style.color = "#88bbff";
    }
  }

  function triggerQnmStrike() {
    qnmPulseTime = animTime;
    if (isAudioActive && audioCtx) {
      playQnmAudioStrike();
    }
  }

  function toggleAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();
    }

    if (!isAudioActive) {
      audioCtx.resume().then(() => {
        setupAudioNodes();
        isAudioActive = true;
        const btn = document.getElementById('audio-toggle-btn');
        if (btn) btn.textContent = 'Mute Acoustic Engine';
      });
    } else {
      if (masterGain) masterGain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
      setTimeout(() => {
        if (audioCtx) audioCtx.suspend();
        isAudioActive = false;
        const btn = document.getElementById('audio-toggle-btn');
        if (btn) btn.textContent = 'Engage Acoustic Engine';
      }, 350);
    }
  }

  function setupAudioNodes() {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;

    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.001, now);
    masterGain.gain.linearRampToValueAtTime(0.7, now + 1.0);
    masterGain.connect(audioCtx.destination);

    // Ergosphere sub-bass drone: 56.6 Hz
    droneOsc1 = audioCtx.createOscillator();
    droneOsc1.type = 'sine';
    droneOsc1.frequency.setValueAtTime(56.6, now);

    droneOsc2 = audioCtx.createOscillator();
    droneOsc2.type = 'triangle';
    droneOsc2.frequency.setValueAtTime(113.2, now);

    const droneGain = audioCtx.createGain();
    droneGain.gain.setValueAtTime(0.25, now);

    droneOsc1.connect(droneGain);
    droneOsc2.connect(droneGain);
    droneGain.connect(masterGain);

    droneOsc1.start();
    droneOsc2.start();

    // Hawking Thermal Noise Node (ScriptProcessor or buffer)
    const bufferSize = 2 * audioCtx.sampleRate;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }

    const whiteNoise = audioCtx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    const biquad = audioCtx.createBiquadFilter();
    biquad.type = 'bandpass';
    biquad.frequency.setValueAtTime(1200, now);
    biquad.Q.setValueAtTime(1.5, now);

    noiseGain = audioCtx.createGain();
    noiseGain.gain.setValueAtTime(0.04, now);

    whiteNoise.connect(biquad);
    biquad.connect(noiseGain);
    noiseGain.connect(masterGain);
    whiteNoise.start();
  }

  function playQnmAudioStrike() {
    if (!audioCtx || !masterGain) return;
    const now = audioCtx.currentTime;

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    // Teukolsky frequency modulated by spin
    const f_qnm = 226.4 * (1.0 + spinA * 0.15);
    osc.frequency.setValueAtTime(f_qnm, now);
    osc.type = 'sine';

    // Damping time tau ~ 0.055s
    gain.gain.setValueAtTime(0.6, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.55);

    osc.connect(gain);
    gain.connect(masterGain);

    osc.start(now);
    osc.stop(now + 0.6);
  }

  function renderLoop(timestamp) {
    animTime = timestamp * 0.001;
    drawFrame();
    requestAnimationFrame(renderLoop);
  }

  function drawFrame() {
    if (!ctx || !cvs) return;
    const w = cvs.width;
    const h = cvs.height;
    ctx.clearRect(0, 0, w, h);

    const cx = w / 2.0;
    const cy = h / 2.0;
    const scale = Math.min(w, h) / 700.0;
    const M = 55.0 * scale;

    const incRad = (inclinationDeg * Math.PI) / 180.0;
    const cosInc = Math.cos(incRad);
    const sinInc = Math.sin(incRad);

    // Horizon radius and ISCO
    const rPlus = M * (1.0 + Math.sqrt(Math.max(0.0, 1.0 - spinA * spinA)));
    const rIsco = M * 2.04;
    const rDiskOut = M * 6.5;

    // Background cosmic space
    const bgGrad = ctx.createRadialGradient(cx, cy, M * 2, cx, cy, Math.max(w, h));
    bgGrad.addColorStop(0, '#040409');
    bgGrad.addColorStop(1, '#010103');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // 1. Rear Lensed Arc of Accretion Disk (Bent over the top by gravity)
    ctx.save();
    ctx.translate(cx, cy);

    const rearGrad = ctx.createRadialGradient(0, -M * 0.3, M * 1.8, 0, -M * 0.3, M * 3.8);
    rearGrad.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
    rearGrad.addColorStop(0.2, 'rgba(120, 200, 255, 0.7)');
    rearGrad.addColorStop(0.6, 'rgba(255, 90, 40, 0.4)');
    rearGrad.addColorStop(1, 'rgba(200, 30, 10, 0.0)');

    ctx.fillStyle = rearGrad;
    ctx.beginPath();
    ctx.arc(0, -M * 0.2, M * 3.2, Math.PI * 0.95, Math.PI * 2.05, false);
    ctx.arc(0, -M * 0.2, M * 1.9, Math.PI * 2.05, Math.PI * 0.95, true);
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    // 2. Main Direct Accretion Disk (Rotated by inclination)
    ctx.save();
    ctx.translate(cx, cy);

    // Draw accretion disk rings with relativistic Doppler asymmetry
    const diskSteps = 45;
    for (let i = 0; i < diskSteps; i++) {
      const rRatio = i / diskSteps;
      const rCurrent = rIsco + rRatio * (rDiskOut - rIsco);
      const rx = rCurrent;
      const ry = rCurrent * Math.max(0.08, cosInc);

      ctx.beginPath();
      ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);

      // Relativistic Doppler beaming gradient across ellipse
      const ringGrad = ctx.createLinearGradient(-rx, 0, rx, 0);
      // Approaching side (left): intense blue-shifted white
      ringGrad.addColorStop(0, 'rgba(235, 250, 255, ' + (0.55 * (1 - rRatio * 0.6)) + ')');
      ringGrad.addColorStop(0.3, 'rgba(80, 190, 255, ' + (0.45 * (1 - rRatio * 0.6)) + ')');
      // Receding side (right): dim red-shifted amber
      ringGrad.addColorStop(0.7, 'rgba(240, 80, 20, ' + (0.28 * (1 - rRatio * 0.6)) + ')');
      ringGrad.addColorStop(1, 'rgba(160, 20, 5, ' + (0.12 * (1 - rRatio * 0.6)) + ')');

      ctx.strokeStyle = ringGrad;
      ctx.lineWidth = 3.5 * scale;
      ctx.stroke();
    }
    ctx.restore();

    // 3. Central Event Horizon & Shadow
    ctx.save();
    ctx.translate(cx, cy);

    // Asymmetric Kerr D-shape shadow path
    ctx.beginPath();
    const shadowSteps = 80;
    for (let s = 0; s <= shadowSteps; s++) {
      const angle = (s / shadowSteps) * Math.PI * 2;
      const rShadowEff = 2.55 * M * (1.0 + 0.14 * spinA * Math.sin(angle));
      const px = rShadowEff * Math.cos(angle);
      const py = rShadowEff * Math.sin(angle);
      if (s === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();

    // Fill event horizon black void
    ctx.fillStyle = '#000000';
    ctx.fill();

    // 4. Multi-Order Photon Rings (Caustic Lensing Boundary)
    ctx.strokeStyle = 'rgba(245, 250, 255, 0.95)';
    ctx.lineWidth = 2.5 * scale;
    ctx.stroke();

    // Secondary thin caustic ring
    ctx.strokeStyle = 'rgba(180, 220, 255, 0.45)';
    ctx.lineWidth = 1.2 * scale;
    ctx.stroke();

    // 5. Quantum Extremal Surface & Entanglement Island (Almheiri-Engelhardt dI)
    // Only visible when Page time progress approaches or exceeds 0.54
    if (pageTimeRatio >= 0.45) {
      const islandAlpha = Math.min(1.0, (pageTimeRatio - 0.45) / 0.15) * 0.75;
      ctx.save();
      ctx.globalAlpha = islandAlpha;
      ctx.strokeStyle = '#00ffcc';
      ctx.lineWidth = 1.5 * scale;

      // Draw logarithmic entanglement spiral filaments inside horizon
      const numFilaments = 12;
      for (let f = 0; f < numFilaments; f++) {
        const fOffset = (f / numFilaments) * Math.PI * 2 + animTime * 0.3;
        ctx.beginPath();
        for (let p = 0; p < 35; p++) {
          const pFrac = p / 35;
          const rIsland = rPlus * (0.84 + 0.14 * pFrac);
          const thetaIsland = fOffset + pFrac * Math.PI * 1.5;
          const ix = rIsland * Math.cos(thetaIsland);
          const iy = rIsland * Math.sin(thetaIsland);
          if (p === 0) ctx.moveTo(ix, iy);
          else ctx.lineTo(ix, iy);
        }
        ctx.stroke();
      }

      // Planck area pixelation grid
      ctx.fillStyle = 'rgba(0, 255, 204, 0.15)';
      const gridSize = 8 * scale;
      for (let gx = -rPlus * 0.9; gx <= rPlus * 0.9; gx += gridSize) {
        for (let gy = -rPlus * 0.9; gy <= rPlus * 0.9; gy += gridSize) {
          if (gx * gx + gy * gy <= (rPlus * 0.95) ** 2 && gx * gx + gy * gy >= (rPlus * 0.7) ** 2) {
            ctx.fillRect(gx, gy, 1.5 * scale, 1.5 * scale);
          }
        }
      }
      ctx.restore();
    }

    // 6. Quasinormal Mode Gravitational Ripples (When struck)
    if (animTime - qnmPulseTime < 2.5) {
      const pulseAge = animTime - qnmPulseTime;
      const rippleRadius = M * 2.5 + pulseAge * 280.0 * scale;
      const rippleAlpha = Math.max(0.0, 1.0 - pulseAge / 2.5) * 0.8;

      ctx.save();
      ctx.strokeStyle = 'rgba(255, 255, 255, ' + rippleAlpha + ')';
      ctx.lineWidth = 2.0 * scale;
      ctx.beginPath();
      ctx.arc(0, 0, rippleRadius, 0, Math.PI * 2);
      ctx.stroke();

      // Secondary quadrupole ring
      ctx.strokeStyle = 'rgba(0, 255, 204, ' + (rippleAlpha * 0.6) + ')';
      ctx.beginPath();
      ctx.arc(0, 0, Math.max(0, rippleRadius - 35 * scale), 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    ctx.restore();
  }

  window.addEventListener('DOMContentLoaded', init);
})();
