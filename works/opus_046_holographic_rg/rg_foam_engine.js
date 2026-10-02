/**
 * OPUS-046: CHAMBER 26 INTERACTIVE ENGINE
 * Holographic Renormalization Group Flow & The Wheeler-DeWitt Quantum Foam
 * Pure Standard HTML5 Canvas & WebAudio API · Zero External Dependencies
 */

(function() {
  const canvas = document.getElementById("simCanvas");
  const ctx = canvas.getContext("2d");

  // DOM Elements
  const statZ = document.getElementById("statZ");
  const statMu = document.getElementById("statMu");
  const statG = document.getElementById("statG");
  const statBeta = document.getElementById("statBeta");
  const statC = document.getElementById("statC");
  const statSigma = document.getElementById("statSigma");
  const statTheta = document.getElementById("statTheta");
  const statEntropy = document.getElementById("statEntropy");
  const statFreq = document.getElementById("statFreq");
  const statRegime = document.getElementById("statRegime");

  const sliderZ = document.getElementById("sliderZ");
  const sliderLp = document.getElementById("sliderLp");
  const sliderB = document.getElementById("sliderB");
  const lblZ = document.getElementById("lblZ");
  const lblLp = document.getElementById("lblLp");
  const lblB = document.getElementById("lblB");

  const btnUV = document.getElementById("btnUV");
  const btnCrossover = document.getElementById("btnCrossover");
  const btnIR = document.getElementById("btnIR");
  const btnOscillate = document.getElementById("btnOscillate");
  const btnAudio = document.getElementById("btnAudio");

  // Simulation State
  let probeZ = 1.00;
  let lp = 0.065;
  let bCoupling = 0.15;
  let autoOscillate = false;
  let timeSec = 0;

  // Streamline Particles
  const PARTICLE_COUNT = 240;
  const particles = [];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
      x: Math.random(),
      v: Math.random(), // normalized vertical depth [0, 1]
      speed: 0.0015 + Math.random() * 0.002,
      phase: Math.random() * Math.PI * 2
    });
  }

  // WebAudio Architecture
  let audioCtx = null;
  let isAudioPlaying = false;
  let oscIR = null;
  let oscFifth = null;
  let oscFlutter = null;
  let filterUV = null;
  let noiseNode = null;
  let masterGain = null;

  function initAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.35, audioCtx.currentTime);
    masterGain.connect(audioCtx.destination);

    // 1. IR Fundamental Drone (43.20 Hz)
    oscIR = audioCtx.createOscillator();
    oscIR.type = "sine";
    oscIR.frequency.setValueAtTime(43.20, audioCtx.currentTime);
    const gainIR = audioCtx.createGain();
    gainIR.gain.setValueAtTime(0.50, audioCtx.currentTime);
    oscIR.connect(gainIR);
    gainIR.connect(masterGain);
    oscIR.start();

    // 2. IR Fifth Harmonic (64.80 Hz)
    oscFifth = audioCtx.createOscillator();
    oscFifth.type = "sine";
    oscFifth.frequency.setValueAtTime(64.80, audioCtx.currentTime);
    const gainFifth = audioCtx.createGain();
    gainFifth.gain.setValueAtTime(0.20, audioCtx.currentTime);
    oscFifth.connect(gainFifth);
    gainFifth.connect(masterGain);
    oscFifth.start();

    // 3. Wheeler-DeWitt Flutter (86.40 Hz)
    oscFlutter = audioCtx.createOscillator();
    oscFlutter.type = "sine";
    oscFlutter.frequency.setValueAtTime(86.40, audioCtx.currentTime);
    const gainFlutter = audioCtx.createGain();
    gainFlutter.gain.setValueAtTime(0.18, audioCtx.currentTime);
    oscFlutter.connect(gainFlutter);
    gainFlutter.connect(masterGain);
    oscFlutter.start();

    // 4. Swept UV Filter with Noise
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
    const whiteNoise = audioCtx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    filterUV = audioCtx.createBiquadFilter();
    filterUV.type = "bandpass";
    filterUV.frequency.setValueAtTime(240.0, audioCtx.currentTime);
    filterUV.Q.setValueAtTime(4.0, audioCtx.currentTime);

    noiseNode = audioCtx.createGain();
    noiseNode.gain.setValueAtTime(0.12, audioCtx.currentTime);

    whiteNoise.connect(filterUV);
    filterUV.connect(noiseNode);
    noiseNode.connect(masterGain);
    whiteNoise.start();
  }

  function updateAudioParams(metrics) {
    if (!audioCtx || !isAudioPlaying) return;
    const now = audioCtx.currentTime;

    // Filter frequency tracks dual energy scale
    const targetFreq = Math.min(2200, Math.max(50, 43.20 * Math.pow(metrics.mu, 0.75)));
    filterUV.frequency.setTargetAtTime(targetFreq, now, 0.08);

    // Quantum foam noise gain increases at the sub-Planckian barrier
    const targetNoiseGain = 0.04 + 0.35 * metrics.thetaFoam;
    noiseNode.gain.setTargetAtTime(targetNoiseGain, now, 0.08);

    // IR drone swells in deep bulk
    oscIR.frequency.setTargetAtTime(43.20 + 0.8 * Math.sin(timeSec * 0.3), now, 0.1);
  }

  function toggleAudio() {
    if (!audioCtx) initAudio();
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
    isAudioPlaying = !isAudioPlaying;
    if (isAudioPlaying) {
      btnAudio.textContent = "Silence Acoustic Sonification";
      btnAudio.classList.add("playing");
      masterGain.gain.setTargetAtTime(0.35, audioCtx.currentTime, 0.1);
    } else {
      btnAudio.textContent = "Activate Acoustic Sonification";
      btnAudio.classList.remove("playing");
      masterGain.gain.setTargetAtTime(0.00, audioCtx.currentTime, 0.1);
    }
  }

  // Physics Calculations
  function computePhysics(zVal) {
    const z_UV = 0.12;
    const z_IR = 9.50;
    const z = Math.max(0.04, zVal);
    const mu = 1.0 / z;

    // Non-conformal beta function: beta(g) = -0.40 g + b g^3
    const epsilon = 0.40;
    const g_IR = Math.sqrt(epsilon / bCoupling);
    const gRunning = g_IR / Math.sqrt(1.0 + (Math.pow(g_IR / 0.10, 2) - 1.0) * Math.pow(z / z_IR, 2.0 * epsilon));
    const betaG = -epsilon * gRunning + bCoupling * Math.pow(gRunning, 3);

    // Holographic c-function
    const c_UV = 12.00;
    const warpFactor = 1.0 + 0.18 * Math.pow(gRunning, 2);
    const cFunction = c_UV / Math.pow(warpFactor, 2);
    const deltaS = Math.max(0, c_UV - cFunction);

    // Wheeler-DeWitt metric fluctuation variance: Delta g ~ ell_P / z
    const foamRatio = lp / z;
    const metricVariance = Math.pow(foamRatio, 2) * (1.0 + 0.45 * Math.pow(Math.sin(Math.PI * foamRatio), 2));

    // Sub-Planckian topological breakdown index Theta in [0, 1]
    const thetaFoam = 1.0 / (1.0 + Math.exp(6.0 * (z - lp * 2.2) / lp));

    // Mode frequency
    const fMode = 43.20 * Math.pow(z_IR / z, 0.60);

    let regime = "Macroscopic IR Bulk Geometry";
    if (thetaFoam > 0.55) {
      regime = "Sub-Planckian Quantum Foam";
    } else if (z < 2.50) {
      regime = "Callan-Symanzik Crossover Flow";
    }

    return {
      z, mu, gRunning, betaG, cFunction, deltaS,
      metricVariance, thetaFoam, fMode, regime
    };
  }

  function resize() {
    canvas.width = canvas.clientWidth * window.devicePixelRatio;
    canvas.height = canvas.clientHeight * window.devicePixelRatio;
  }
  window.addEventListener("resize", resize);
  resize();

  // Animation Loop
  function render() {
    timeSec += 0.016;

    if (autoOscillate) {
      probeZ = 0.40 + 4.2 * (1.0 - Math.cos(timeSec * 0.45));
      sliderZ.value = probeZ.toFixed(2);
      lblZ.textContent = probeZ.toFixed(2);
    }

    const metrics = computePhysics(probeZ);
    updateAudioParams(metrics);

    // Update HUD Stats
    statZ.textContent = metrics.z.toFixed(3);
    statMu.textContent = metrics.mu.toFixed(3);
    statG.textContent = metrics.gRunning.toFixed(3);
    statBeta.textContent = (metrics.betaG >= 0 ? "+" : "") + metrics.betaG.toFixed(4);
    statC.textContent = metrics.cFunction.toFixed(2);
    statSigma.textContent = metrics.metricVariance.toFixed(5);
    statTheta.textContent = metrics.thetaFoam.toFixed(4);
    statEntropy.textContent = metrics.deltaS.toFixed(3) + " k_B";
    statFreq.textContent = metrics.fMode.toFixed(1) + " Hz";
    statRegime.textContent = metrics.regime;

    const w = canvas.width;
    const h = canvas.height;

    // Clear with dark basalt background
    ctx.fillStyle = "#05070a";
    ctx.fillRect(0, 0, w, h);

    // 1. Draw Wheeler-DeWitt Interference Fringes on Superspace
    ctx.lineWidth = 1;
    const fringeCols = 18;
    for (let c = 0; c < fringeCols; c++) {
      const u = c / fringeCols;
      const kx = (u - 0.5) * 10.0;
      ctx.beginPath();
      for (let y = 0; y < h; y += 12) {
        const v = y / h;
        const zv = 0.15 * Math.exp(v * Math.log(9.5 / 0.15));
        const kz = (zv - 1.0) * 3.5;
        const phase = kz * kz - kx * kx;
        const xOffset = Math.sin(phase * 1.5 + timeSec * 0.5) * 18.0 * (1.0 - v * 0.4);
        const px = u * w + xOffset;
        if (y === 0) ctx.moveTo(px, y);
        else ctx.lineTo(px, y);
      }
      ctx.strokeStyle = `rgba(56, 189, 248, ${0.03 + 0.05 * (1.0 - u)})`;
      ctx.stroke();
    }

    // 2. Holographic Domain Wall Slices (Warped Horizontal Layers)
    const numLayers = 54;
    for (let l = 0; l < numLayers; l++) {
      const vLayer = l / (numLayers - 1);
      const zLayer = 0.15 * Math.exp(vLayer * Math.log(9.5 / 0.15));
      const gLayer = 1.633 / Math.sqrt(1.0 + (Math.pow(1.633 / 0.10, 2) - 1.0) * Math.pow(zLayer / 9.5, 0.80));
      const warp = 0.18 * Math.pow(gLayer, 2) * Math.sin(vLayer * Math.PI);
      const baseY = (vLayer + warp * 0.10) * h;

      const jitter = 32.0 * Math.pow(lp / zLayer, 1.35);

      // Color from UV cyan to IR amber
      const r = Math.floor(35 + 215 * Math.pow(vLayer, 1.3));
      const g = Math.floor(165 + 70 * Math.sin(vLayer * Math.PI) - 80 * vLayer);
      const b = Math.floor(250 * (1.0 - vLayer * 0.7) + 30 * vLayer);

      ctx.beginPath();
      for (let x = 0; x < w; x += 10) {
        const pxNorm = x / w;
        const fluc = jitter * Math.sin(pxNorm * 18.0 + l * 0.6 + timeSec)
                   + (jitter * 0.45) * Math.cos(pxNorm * 42.0 - l * 1.2);
        const py = baseY + fluc;
        if (x === 0) ctx.moveTo(x, py);
        else ctx.lineTo(x, py);
      }
      ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${0.28 + 0.5 * (1.0 - vLayer * 0.3)})`;
      ctx.stroke();
    }

    // 3. Callan-Symanzik Beta Flow Particles
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.v += p.speed;
      if (p.v > 1.0) {
        p.v = 0.0;
        p.x = Math.random();
      }

      const zParticle = 0.15 * Math.exp(p.v * Math.log(9.5 / 0.15));
      const py = p.v * h;
      let px = p.x * w + Math.sin(p.x * 12.0 + zParticle * 2.0 + timeSec * 0.8) * 45.0 * (1.0 - p.v * 0.5);

      // Sub-Planckian jitter near boundary
      if (zParticle < 0.45) {
        px += (lp / zParticle) * 22.0 * Math.sin(py * 0.2 + p.phase);
      }

      const pr = Math.floor(55 + 195 * p.v);
      const pg = Math.floor(185 - 80 * p.v);
      const pb = Math.floor(245 - 170 * p.v);

      ctx.beginPath();
      ctx.arc(px, py, 1.8 + 1.4 * p.v, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${pr}, ${pg}, ${pb}, ${0.5 + 0.4 * (1.0 - p.v * 0.5)})`;
      ctx.fill();
    }

    // 4. Sub-Planckian Quantum Foam Micro-Wormhole Bubbling at UV Boundary (Top)
    const foamCount = Math.floor(60 + metrics.thetaFoam * 240);
    for (let f = 0; f < foamCount; f++) {
      const fx = (Math.sin(f * 97.3 + timeSec * 0.8) * 0.5 + 0.5) * w;
      const distFromTop = Math.abs(Math.sin(f * 43.1 + timeSec * 0.5)) * (h * 0.14);
      const fy = distFromTop;
      const rad = 2 + Math.abs(Math.sin(f * 13.7 + timeSec * 2.0)) * 6;

      ctx.beginPath();
      ctx.arc(fx, fy, rad, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(56, 189, 248, ${0.25 + 0.55 * (1.0 - distFromTop / (h * 0.14))})`;
      ctx.fill();
    }

    // 5. Active Probe Indicator Line
    const probeV = Math.log(metrics.z / 0.15) / Math.log(9.5 / 0.15);
    const probeY = Math.max(10, Math.min(h - 10, probeV * h));

    ctx.beginPath();
    ctx.setLineDash([8, 6]);
    ctx.moveTo(0, probeY);
    ctx.lineTo(w, probeY);
    ctx.strokeStyle = "rgba(245, 158, 11, 0.85)";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.setLineDash([]);

    // Probe Label
    ctx.font = "bold 12px monospace";
    ctx.fillStyle = "#f59e0b";
    ctx.fillText(`PROBE CUTOFF: z = ${metrics.z.toFixed(2)} | μ = ${metrics.mu.toFixed(2)} | c = ${metrics.cFunction.toFixed(2)}`, 24, probeY - 10);

    requestAnimationFrame(render);
  }

  // Event Listeners
  sliderZ.addEventListener("input", function() {
    autoOscillate = false;
    btnOscillate.classList.remove("active");
    probeZ = parseFloat(sliderZ.value);
    lblZ.textContent = probeZ.toFixed(2);
  });

  sliderLp.addEventListener("input", function() {
    lp = parseFloat(sliderLp.value);
    lblLp.textContent = lp.toFixed(3);
  });

  sliderB.addEventListener("input", function() {
    bCoupling = parseFloat(sliderB.value);
    lblB.textContent = bCoupling.toFixed(2);
  });

  btnUV.addEventListener("click", function() {
    autoOscillate = false;
    btnOscillate.classList.remove("active");
    probeZ = 0.08;
    sliderZ.value = probeZ;
    lblZ.textContent = probeZ.toFixed(2);
  });

  btnCrossover.addEventListener("click", function() {
    autoOscillate = false;
    btnOscillate.classList.remove("active");
    probeZ = 1.60;
    sliderZ.value = probeZ;
    lblZ.textContent = probeZ.toFixed(2);
  });

  btnIR.addEventListener("click", function() {
    autoOscillate = false;
    btnOscillate.classList.remove("active");
    probeZ = 7.50;
    sliderZ.value = probeZ;
    lblZ.textContent = probeZ.toFixed(2);
  });

  btnOscillate.addEventListener("click", function() {
    autoOscillate = !autoOscillate;
    if (autoOscillate) {
      btnOscillate.classList.add("active");
    } else {
      btnOscillate.classList.remove("active");
    }
  });

  btnAudio.addEventListener("click", toggleAudio);

  requestAnimationFrame(render);
})();
