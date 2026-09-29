/**
 * STUDIO ANAMNESIS · CHAMBER 23
 * The Fuzzball Reliquary & The Horizonless Microstates (OPUS-043)
 * Pure Vanilla JavaScript & WebAudio API · Zero External Dependencies
 */

(function () {
  'use strict';

  const canvas = document.getElementById('chamberCanvas');
  const ctx = canvas.getContext('2d');

  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  // Audio Context
  let audioCtx = null;
  let isAudioPlaying = false;
  let masterGain = null;
  let oscF0 = null;
  let oscFrac = null;
  let oscBubble = null;
  let oscMom = null;

  // Simulation Parameters
  let fractionation = 512;
  let stringCoupling = 0.25;
  let showBubbles = true;
  let showRadiation = true;
  let rotX = 0.2;
  let rotY = 0.0;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;

  // Initialize 24 Bubbling Centers in 3D
  const bubbles = [];
  const rFuzzBase = 220;
  for (let i = 0; i < 24; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = (Math.random() - 0.5) * Math.PI;
    const r = Math.pow(Math.random(), 0.6) * rFuzzBase * 0.9;
    bubbles.push({
      x: r * Math.cos(phi) * Math.cos(theta),
      y: r * Math.sin(phi),
      z: r * Math.cos(phi) * Math.sin(theta),
      charge: 0.8 + Math.random() * 0.9,
      radius: 12 + Math.random() * 18,
      phase: Math.random() * Math.PI * 2
    });
  }

  // Initialize 400 fractionated string fibers
  const fibers = [];
  const numFibers = 420;
  for (let i = 0; i < numFibers; i++) {
    const phi0 = Math.random() * Math.PI * 2;
    const theta0 = (Math.random() - 0.5) * Math.PI;
    const turns = 1.5 + Math.random() * 3.5;
    const rScale = 0.3 + Math.random() * 0.7;
    const speed = (Math.random() * 0.4 + 0.2) * (Math.random() > 0.5 ? 1 : -1);
    fibers.push({
      phi0,
      theta0,
      turns,
      rScale,
      speed,
      points: 40,
      hue: Math.random() > 0.4 ? (Math.random() > 0.5 ? 195 : 225) : 42 // Cyan, Royal Blue, or Warm Gold
    });
  }

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);

  // Mouse / Touch Interaction
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
    rotY += dx * 0.006;
    rotX += dy * 0.006;
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
    rotY += dx * 0.006;
    rotX += dy * 0.006;
    lastMouseX = e.touches[0].clientX;
    lastMouseY = e.touches[0].clientY;
  });

  // 3D Projection Helpers
  function project(x, y, z, cx, cy) {
    // Rotate around X
    const cosX = Math.cos(rotX);
    const sinX = Math.sin(rotX);
    const y1 = y * cosX - z * sinX;
    const z1 = y * sinX + z * cosX;

    // Rotate around Y
    const cosY = Math.cos(rotY);
    const sinY = Math.sin(rotY);
    const x2 = x * cosY + z1 * sinY;
    const z2 = -x * sinY + z1 * cosY;

    // Perspective projection
    const fov = 850;
    const scale = fov / (fov + z2 + 400);
    return {
      px: cx + x2 * scale,
      py: cy + y1 * scale,
      scale: scale,
      z: z2
    };
  }

  let time = 0;

  function render() {
    time += 0.015;
    if (!isDragging) {
      rotY += 0.002;
    }

    // Dynamic Fuzzball Radius determined by string coupling and fractionation
    const rFuzzCurrent = rFuzzBase * Math.pow((stringCoupling * stringCoupling * fractionation * 24) / 512.0, 1.0 / 6.0);

    ctx.fillStyle = '#06080d';
    ctx.fillRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;

    // 1. Draw Horizon Surface Glow (Unitary Non-Thermal Radiation)
    if (showRadiation) {
      const grad = ctx.createRadialGradient(cx, cy, rFuzzCurrent * 0.5, cx, cy, rFuzzCurrent * 1.55);
      grad.addColorStop(0, 'rgba(40, 90, 190, 0.22)');
      grad.addColorStop(0.65, 'rgba(230, 180, 70, 0.12)');
      grad.addColorStop(1, 'rgba(6, 8, 13, 0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(cx, cy, rFuzzCurrent * 1.55, 0, Math.PI * 2);
      ctx.fill();
    }

    // 2. Render Bubbling Centers
    if (showBubbles) {
      for (let i = 0; i < bubbles.length; i++) {
        const b = bubbles[i];
        const radPulse = b.radius * (1.0 + 0.15 * Math.sin(time * 2.5 + b.phase));
        const proj = project(b.x, b.y, b.z, cx, cy);

        const bGrad = ctx.createRadialGradient(proj.px, proj.py, 0, proj.px, proj.py, radPulse * proj.scale);
        bGrad.addColorStop(0, 'rgba(255, 240, 200, 0.65)');
        bGrad.addColorStop(0.4, 'rgba(80, 210, 240, 0.35)');
        bGrad.addColorStop(1, 'rgba(80, 210, 240, 0)');

        ctx.fillStyle = bGrad;
        ctx.beginPath();
        ctx.arc(proj.px, proj.py, radPulse * proj.scale, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // 3. Render Entangled Fractionated String Fibers (Eva Hesse Post-Minimalist Texture)
    ctx.lineWidth = 1.1;
    for (let i = 0; i < fibers.length; i++) {
      const f = fibers[i];
      const curAngle = f.phi0 + time * f.speed;

      ctx.beginPath();
      let first = true;
      for (let p = 0; p <= f.points; p++) {
        const t = p / f.points;
        const angle = curAngle + t * f.turns * Math.PI * 2;
        const rNode = rFuzzCurrent * f.rScale * (0.8 + 0.2 * Math.sin(t * Math.PI * 4 + time * 2));
        const zNode = (t - 0.5) * rFuzzCurrent * 1.6;

        const x = rNode * Math.cos(angle);
        const y = rNode * Math.sin(angle) * Math.sin(f.theta0) + zNode * Math.cos(f.theta0);
        const z = -rNode * Math.sin(angle) * Math.cos(f.theta0) + zNode * Math.sin(f.theta0);

        const pt = project(x, y, z, cx, cy);
        if (first) {
          ctx.moveTo(pt.px, pt.py);
          first = false;
        } else {
          ctx.lineTo(pt.px, pt.py);
        }
      }

      const alpha = 0.35 + 0.25 * Math.sin(time + i);
      if (f.hue === 42) {
        ctx.strokeStyle = `rgba(240, 200, 90, ${alpha})`;
      } else if (f.hue === 195) {
        ctx.strokeStyle = `rgba(60, 210, 245, ${alpha})`;
      } else {
        ctx.strokeStyle = `rgba(100, 130, 255, ${alpha * 0.9})`;
      }
      ctx.stroke();
    }

    // 4. Update In-Chamber HUD Readout
    const entropyVal = (2 * Math.PI * Math.sqrt(fractionation * 24)).toFixed(1);
    const radiusVal = (rFuzzCurrent / 72.0).toFixed(3);
    document.getElementById('hudRadius').innerText = `${radiusVal} ℓ_s`;
    document.getElementById('hudEntropy').innerText = `${entropyVal} k_B`;
    document.getElementById('hudFractionation').innerText = `${fractionation}x`;

    requestAnimationFrame(render);
  }

  // WebAudio Synthesizer Engine
  function initAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.0, audioCtx.currentTime);
    masterGain.connect(audioCtx.destination);

    // Fundamental A1 string drone (55 Hz)
    oscF0 = audioCtx.createOscillator();
    oscF0.type = 'sine';
    oscF0.frequency.setValueAtTime(55.0, audioCtx.currentTime);

    const gainF0 = audioCtx.createGain();
    gainF0.gain.setValueAtTime(0.35, audioCtx.currentTime);
    oscF0.connect(gainF0);
    gainF0.connect(masterGain);

    // Fractionated beating mode (57.43 Hz -> 2.43 Hz beating)
    oscFrac = audioCtx.createOscillator();
    oscFrac.type = 'sine';
    oscFrac.frequency.setValueAtTime(57.43, audioCtx.currentTime);

    const gainFrac = audioCtx.createGain();
    gainFrac.gain.setValueAtTime(0.32, audioCtx.currentTime);
    oscFrac.connect(gainFrac);
    gainFrac.connect(masterGain);

    // Bubble topological resonance (82.5 Hz)
    oscBubble = audioCtx.createOscillator();
    oscBubble.type = 'triangle';
    oscBubble.frequency.setValueAtTime(82.5, audioCtx.currentTime);

    const gainBub = audioCtx.createGain();
    gainBub.gain.setValueAtTime(0.18, audioCtx.currentTime);
    oscBubble.connect(gainBub);
    gainBub.connect(masterGain);

    // Momentum mode harmonic (269.44 Hz)
    oscMom = audioCtx.createOscillator();
    oscMom.type = 'sine';
    oscMom.frequency.setValueAtTime(269.44, audioCtx.currentTime);

    const gainMom = audioCtx.createGain();
    gainMom.gain.setValueAtTime(0.12, audioCtx.currentTime);
    oscMom.connect(gainMom);
    gainMom.connect(masterGain);

    oscF0.start();
    oscFrac.start();
    oscBubble.start();
    oscMom.start();
  }

  function toggleAudio() {
    initAudio();
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    if (!isAudioPlaying) {
      masterGain.gain.linearRampToValueAtTime(0.65, audioCtx.currentTime + 1.5);
      isAudioPlaying = true;
      document.getElementById('audioBtn').innerText = 'Mute Sonic Microstates';
      document.getElementById('audioBtn').classList.add('active');
    } else {
      masterGain.gain.linearRampToValueAtTime(0.0, audioCtx.currentTime + 1.0);
      isAudioPlaying = false;
      document.getElementById('audioBtn').innerText = 'Engage Sonic Microstates';
      document.getElementById('audioBtn').classList.remove('active');
    }
  }

  // Hook UI Controls
  document.getElementById('audioBtn').addEventListener('click', toggleAudio);

  document.getElementById('sliderFractionation').addEventListener('input', (e) => {
    fractionation = parseInt(e.target.value, 10);
    if (oscFrac && audioCtx) {
      const deltaF = 55.0 / Math.sqrt(fractionation);
      oscFrac.frequency.setValueAtTime(55.0 + deltaF, audioCtx.currentTime);
    }
  });

  document.getElementById('sliderCoupling').addEventListener('input', (e) => {
    stringCoupling = parseFloat(e.target.value);
  });

  document.getElementById('btnBubbles').addEventListener('click', (e) => {
    showBubbles = !showBubbles;
    e.target.classList.toggle('active', showBubbles);
  });

  document.getElementById('btnRadiation').addEventListener('click', (e) => {
    showRadiation = !showRadiation;
    e.target.classList.toggle('active', showRadiation);
  });

  // Start Animation Loop
  requestAnimationFrame(render);
})();

