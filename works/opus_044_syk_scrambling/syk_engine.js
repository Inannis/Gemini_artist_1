/**
 * STUDIO ANAMNESIS · CHAMBER 24
 * The Scrambling Horizon & The SYK Reliquary (OPUS-044)
 * Pure Vanilla JavaScript & WebAudio API · Zero External Dependencies
 */

(function () {
  'use strict';

  const canvas = document.getElementById('chamberCanvas');
  const ctx = canvas.getContext('2d');

  let width = (canvas.width = window.innerWidth - 320);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth - 320;
    height = canvas.height = window.innerHeight;
  });

  // Telemetry & State
  let N = 32;
  let betaJ = 20.0;
  let currentTime = 11.0;
  let autoAnimate = true;
  let rotAngle = 0.0;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;
  let cameraPitch = 0.0;
  let cameraYaw = 0.0;

  // WebAudio API
  let audioCtx = null;
  let isAudioPlaying = false;
  let masterGain = null;
  let oscDrone = null;
  let oscDrone2 = null;
  let oscScramble = null;
  let lfoFlutter = null;
  let lfoGain = null;
  let grainTimer = null;

  // Quartic Couplings Network
  let nodes = [];
  let chords = [];

  function generateCouplings() {
    nodes = [];
    chords = [];
    const rDisc = Math.min(width, height) * 0.38;

    for (let i = 0; i < N; i++) {
      const theta = (2.0 * Math.PI * i) / N;
      // Schwarzian boundary fluctuations
      const fluc = 8.0 * Math.cos(2.0 * theta + 0.4) + 4.5 * Math.sin(3.0 * theta - 0.7);
      const r = rDisc + fluc;
      nodes.append = nodes.push({
        idx: i,
        theta: theta,
        r: r,
        x: r * Math.cos(theta),
        y: r * Math.sin(theta)
      });
    }

    // Sample random chords with Gaussian weights
    const sigmaJ = Math.sqrt(6.0 / Math.pow(N, 3));
    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        if (Math.random() < 0.35) {
          // Box-Muller Gaussian
          const u1 = Math.max(1e-6, Math.random());
          const u2 = Math.random();
          const g = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
          const weight = g * sigmaJ * 45.0;
          chords.push({ i, j, weight });
        }
      }
    }
  }

  function updateHUD() {
    const beta = betaJ / 1.0;
    const lambdaMss = (2.0 * Math.PI) / beta;
    const lambdaSyk = lambdaMss * Math.max(0.0, 1.0 - (2.4069 / betaJ));
    const satPct = (lambdaSyk / lambdaMss) * 100.0;
    const tStar = (beta / (2.0 * Math.PI)) * Math.log(N);
    const otoc = Math.max(0.0, 1.0 - (0.50 / N) * Math.exp(lambdaSyk * Math.min(currentTime, tStar * 1.5)));

    document.getElementById('hudN').textContent = N;
    document.getElementById('hudBeta').textContent = betaJ.toFixed(1);
    document.getElementById('hudBound').textContent = lambdaMss.toFixed(4) + ' s⁻¹';
    document.getElementById('hudLyapunov').textContent = lambdaSyk.toFixed(4) + ' s⁻¹';
    document.getElementById('hudSat').textContent = satPct.toFixed(1) + '%';
    document.getElementById('hudTstar').textContent = tStar.toFixed(2) + ' s';
    document.getElementById('hudOtoc').textContent = otoc.toFixed(4);

    document.getElementById('valN').textContent = N;
    document.getElementById('valBeta').textContent = betaJ.toFixed(1);
    document.getElementById('valTime').textContent = currentTime.toFixed(1) + 's';

    // Update audio parameters if active
    if (audioCtx && isAudioPlaying) {
      if (lfoFlutter) {
        lfoFlutter.frequency.setTargetAtTime(lambdaSyk / (2.0 * Math.PI), audioCtx.currentTime, 0.1);
      }
      if (oscScramble) {
        const sweepFactor = 1.0 + 0.35 * Math.exp(lambdaSyk * Math.min(currentTime, tStar) * 0.15);
        oscScramble.frequency.setTargetAtTime(47.99 * sweepFactor, audioCtx.currentTime, 0.1);
      }
    }
  }

  // Audio Engine
  function toggleAudio() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (!isAudioPlaying) {
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }

      masterGain = audioCtx.createGain();
      masterGain.gain.setValueAtTime(0.001, audioCtx.currentTime);
      masterGain.gain.exponentialRampToValueAtTime(0.35, audioCtx.currentTime + 1.5);
      masterGain.connect(audioCtx.destination);

      // Voice 1: 44.0 Hz Horizon Drone
      oscDrone = audioCtx.createOscillator();
      oscDrone.type = 'sine';
      oscDrone.frequency.setValueAtTime(44.0, audioCtx.currentTime);

      // Voice 2: Sub-octave 22.0 Hz
      oscDrone2 = audioCtx.createOscillator();
      oscDrone2.type = 'sine';
      oscDrone2.frequency.setValueAtTime(22.0, audioCtx.currentTime);

      // LFO for Lyapunov Flutter
      const beta = betaJ;
      const lambdaMss = (2.0 * Math.PI) / beta;
      const lambdaSyk = lambdaMss * Math.max(0.0, 1.0 - (2.4069 / betaJ));
      lfoFlutter = audioCtx.createOscillator();
      lfoFlutter.frequency.setValueAtTime(lambdaSyk / (2.0 * Math.PI), audioCtx.currentTime);

      lfoGain = audioCtx.createGain();
      lfoGain.gain.setValueAtTime(0.25, audioCtx.currentTime);

      const droneGain = audioCtx.createGain();
      droneGain.gain.setValueAtTime(0.5, audioCtx.currentTime);
      lfoFlutter.connect(droneGain.gain);

      oscDrone.connect(droneGain);
      oscDrone2.connect(droneGain);
      droneGain.connect(masterGain);

      // Voice 3: Scrambling Sweep
      oscScramble = audioCtx.createOscillator();
      oscScramble.type = 'triangle';
      oscScramble.frequency.setValueAtTime(47.99, audioCtx.currentTime);
      const scrambleGain = audioCtx.createGain();
      scrambleGain.gain.setValueAtTime(0.2, audioCtx.currentTime);
      oscScramble.connect(scrambleGain);
      scrambleGain.connect(masterGain);

      oscDrone.start();
      oscDrone2.start();
      lfoFlutter.start();
      oscScramble.start();

      // Stochastic Xenakis Grains
      grainTimer = setInterval(() => {
        if (!isAudioPlaying) return;
        const gOsc = audioCtx.createOscillator();
        const gGain = audioCtx.createGain();
        const freq = 160 + Math.random() * 640;
        const dur = 0.05 + Math.random() * 0.15;
        gOsc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gGain.gain.setValueAtTime(0.001, audioCtx.currentTime);
        gGain.gain.exponentialRampToValueAtTime(0.12, audioCtx.currentTime + dur * 0.4);
        gGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur);
        gOsc.connect(gGain);
        gGain.connect(masterGain);
        gOsc.start();
        gOsc.stop(audioCtx.currentTime + dur);
      }, 350);

      isAudioPlaying = true;
      document.getElementById('audioBtn').classList.add('active');
      document.getElementById('audioIcon').textContent = '⏹';
    } else {
      masterGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
      setTimeout(() => {
        if (oscDrone) oscDrone.stop();
        if (oscDrone2) oscDrone2.stop();
        if (lfoFlutter) lfoFlutter.stop();
        if (oscScramble) oscScramble.stop();
        if (grainTimer) clearInterval(grainTimer);
        isAudioPlaying = false;
        document.getElementById('audioBtn').classList.remove('active');
        document.getElementById('audioIcon').textContent = '▶';
      }, 850);
    }
  }

  // Animation Loop
  let lastFrameTime = performance.now();
  function render(now) {
    const dt = (now - lastFrameTime) / 1000.0;
    lastFrameTime = now;

    if (autoAnimate) {
      currentTime += dt * 0.8;
      if (currentTime > 22.0) currentTime = 0.0;
      document.getElementById('sliderTime').value = currentTime.toFixed(1);
      updateHUD();
    }

    rotAngle += dt * 0.15;

    // Clear Canvas with trailing glow
    ctx.fillStyle = '#06080d';
    ctx.fillRect(0, 0, width, height);

    const cx = width / 2.0;
    const cy = height / 2.0;
    const rDisc = Math.min(width, height) * 0.38;

    ctx.save();
    ctx.translate(cx, cy);

    // Apply 3D perspective tilt
    const cosPitch = Math.cos(cameraPitch);
    const sinPitch = Math.sin(cameraPitch);
    const cosYaw = Math.cos(cameraYaw + rotAngle * 0.1);
    const sinYaw = Math.sin(cameraYaw + rotAngle * 0.1);

    // 1. Draw AdS2 Hyperbolic Bulk Gradient
    const bulkGrad = ctx.createRadialGradient(0, 0, 10, 0, 0, rDisc);
    bulkGrad.addColorStop(0.0, 'rgba(88, 28, 135, 0.45)');  // Violet AdS core
    bulkGrad.addColorStop(0.5, 'rgba(14, 116, 144, 0.25)'); // Deep teal
    bulkGrad.addColorStop(0.92, 'rgba(212, 175, 55, 0.15)'); // Amber boundary
    bulkGrad.addColorStop(1.0, 'rgba(56, 215, 210, 0.0)');  // Horizon fade
    ctx.fillStyle = bulkGrad;
    ctx.beginPath();
    ctx.arc(0, 0, rDisc, 0, Math.PI * 2);
    ctx.fill();

    // 2. Draw Concentric OTOC Scrambling Wavefronts
    const tStar = (betaJ / (2.0 * Math.PI)) * Math.log(N);
    const normScramble = Math.min(1.0, currentTime / tStar);
    const waveRadius = rDisc * (1.0 - normScramble * 0.88);

    ctx.strokeStyle = `rgba(244, 63, 94, ${0.4 + 0.3 * Math.sin(now * 0.005)})`;
    ctx.lineWidth = 2.5;
    ctx.setLineDash([8, 6]);
    ctx.beginPath();
    ctx.arc(0, 0, Math.max(15, waveRadius), 0, Math.PI * 2);
    ctx.stroke();
    ctx.setLineDash([]);

    // 3. Draw Hyperbolic Geodesic Chords
    for (let c of chords) {
      const p1 = nodes[c.i];
      const p2 = nodes[c.j];
      if (!p1 || !p2) continue;

      // Project onto canvas
      const x1 = p1.x * cosYaw - p1.y * sinYaw;
      const y1 = (p1.x * sinYaw + p1.y * cosYaw) * cosPitch;
      const x2 = p2.x * cosYaw - p2.y * sinYaw;
      const y2 = (p2.x * sinYaw + p2.y * cosYaw) * cosPitch;

      // Pull toward center based on boundary distance
      let dTh = Math.abs(p1.theta - p2.theta);
      if (dTh > Math.PI) dTh = 2.0 * Math.PI - dTh;
      const pull = Math.sin(dTh / 2.0) * 0.85;

      const midX = (x1 + x2) / 2.0 * (1.0 - pull);
      const midY = (y1 + y2) / 2.0 * (1.0 - pull);

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.quadraticCurveTo(midX, midY, x2, y2);

      if (c.weight >= 0) {
        ctx.strokeStyle = `rgba(212, 175, 55, ${Math.min(0.65, Math.abs(c.weight) * 2.2 + 0.15)})`;
      } else {
        ctx.strokeStyle = `rgba(56, 215, 210, ${Math.min(0.65, Math.abs(c.weight) * 2.2 + 0.15)})`;
      }
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }

    // 4. Draw Majorana Boundary Nodes
    for (let p of nodes) {
      const px = p.x * cosYaw - p.y * sinYaw;
      const py = (p.x * sinYaw + p.y * cosYaw) * cosPitch;

      // Glow halo
      ctx.fillStyle = 'rgba(251, 191, 36, 0.25)';
      ctx.beginPath();
      ctx.arc(px, py, 9, 0, Math.PI * 2);
      ctx.fill();

      // Solid Node
      ctx.fillStyle = '#fef08a';
      ctx.beginPath();
      ctx.arc(px, py, 4.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Highlight scrambling origin node (Node 0)
    if (nodes[0]) {
      const p0 = nodes[0];
      const p0x = p0.x * cosYaw - p0.y * sinYaw;
      const p0y = (p0.x * sinYaw + p0.y * cosYaw) * cosPitch;
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(p0x, p0y, 14 + 4 * Math.sin(now * 0.008), 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
    requestAnimationFrame(render);
  }

  // Event Listeners
  document.getElementById('audioBtn').addEventListener('click', toggleAudio);
  document.getElementById('sliderN').addEventListener('input', (e) => {
    N = parseInt(e.target.value);
    generateCouplings();
    updateHUD();
  });
  document.getElementById('sliderBeta').addEventListener('input', (e) => {
    betaJ = parseFloat(e.target.value);
    updateHUD();
  });
  document.getElementById('sliderTime').addEventListener('input', (e) => {
    currentTime = parseFloat(e.target.value);
    autoAnimate = false;
    document.getElementById('animateBtn').classList.remove('active');
    document.getElementById('animateBtn').textContent = '▶ Resume Auto-Scramble';
    updateHUD();
  });
  document.getElementById('resampleBtn').addEventListener('click', () => {
    generateCouplings();
    updateHUD();
  });
  document.getElementById('animateBtn').addEventListener('click', () => {
    autoAnimate = !autoAnimate;
    const btn = document.getElementById('animateBtn');
    if (autoAnimate) {
      btn.classList.add('active');
      btn.textContent = '⏸ Auto-Scramble Time';
    } else {
      btn.classList.remove('active');
      btn.textContent = '▶ Resume Auto-Scramble';
    }
  });

  // Mouse Interaction (Camera Pitch/Yaw Drag)
  canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });
  window.addEventListener('mouseup', () => (isDragging = false));
  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;
    cameraYaw += dx * 0.005;
    cameraPitch = Math.max(-0.6, Math.min(0.6, cameraPitch + dy * 0.005));
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  // Touch Support
  canvas.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      isDragging = true;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    }
  });
  window.addEventListener('touchend', () => (isDragging = false));
  window.addEventListener('touchmove', (e) => {
    if (!isDragging || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - lastMouseX;
    const dy = e.touches[0].clientY - lastMouseY;
    cameraYaw += dx * 0.006;
    cameraPitch = Math.max(-0.6, Math.min(0.6, cameraPitch + dy * 0.006));
    lastMouseX = e.touches[0].clientX;
    lastMouseY = e.touches[0].clientY;
  });

  // Initialization
  generateCouplings();
  updateHUD();
  requestAnimationFrame(render);
})();
