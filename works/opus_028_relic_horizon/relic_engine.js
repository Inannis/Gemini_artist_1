/**
 * STUDIO ANAMNESIS · INTERACTIVE RELIC HORIZON SIMULATOR
 * OPUS-028: THE RELIC HORIZON (CMB DIPOLE & UNIVERSAL HEAT SINK)
 * Series XXVI: The Relic Horizon & The Universal Heat Sink
 * 
 * Features:
 * - Interactive 3D celestial sphere rendering the 2.7255 K CMB dipole
 * - Real-time Doppler peculiar velocity slider (0 to 1200 km/s)
 * - Dynamic Planck spectral distribution graph with interactive frequency readout
 * - Real-time Web Audio API synthesizer (18.65 Hz Planck drone + Doppler binaural beat)
 * - Live Landauer bit-erasure dissipation calculator (E = k_B T ln 2)
 */

(function () {
  const K_BOLTZ = 1.380649e-23;
  const C_LIGHT = 299792.458; // km/s
  const T_CMB = 2.72548; // Kelvin

  let peculiarVelocity = 369.82; // km/s
  let rotX = 0.4;
  let rotY = -0.8;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;

  // Audio Context
  let audioCtx = null;
  let isPlaying = false;
  let oscSub = null;
  let oscCarrierL = null;
  let oscCarrierR = null;
  let noiseNode = null;
  let gainMaster = null;

  const canvasSky = document.getElementById('cmb-canvas');
  const ctxSky = canvasSky ? canvasSky.getContext('2d') : null;

  const canvasPlanck = document.getElementById('planck-canvas');
  const ctxPlanck = canvasPlanck ? canvasPlanck.getContext('2d') : null;

  // UI elements
  const velSlider = document.getElementById('vel-slider');
  const velValText = document.getElementById('vel-val');
  const dipoleValText = document.getElementById('dipole-val');
  const landauerValText = document.getElementById('landauer-val');
  const audioBtn = document.getElementById('synth-btn');

  function updateCalculations() {
    const beta = peculiarVelocity / C_LIGHT;
    const deltaT_mK = (T_CMB * beta) * 1000.0;
    
    // Landauer erasure cost at T_CMB
    const e_erasure_J = K_BOLTZ * T_CMB * Math.LN2;
    const e_zeptojoules = e_erasure_J * 1e21;

    if (velValText) velValText.innerText = peculiarVelocity.toFixed(1) + " km/s";
    if (dipoleValText) dipoleValText.innerText = "±" + deltaT_mK.toFixed(3) + " mK";
    if (landauerValText) landauerValText.innerText = e_zeptojoules.toFixed(4) + " zJ/bit (" + (e_erasure_J * 1e24).toFixed(1) + " yJ)";

    // Update audio frequencies if running
    if (isPlaying && oscCarrierL && oscCarrierR) {
      const f_base = 432.0;
      const f_shift = f_base * beta;
      oscCarrierL.frequency.setValueAtTime(f_base + f_shift, audioCtx.currentTime);
      oscCarrierR.frequency.setValueAtTime(f_base - f_shift, audioCtx.currentTime);
    }
  }

  function drawSky() {
    if (!ctxSky) return;
    const w = canvasSky.width;
    const h = canvasSky.height;

    ctxSky.fillStyle = "#030508";
    ctxSky.fillRect(0, 0, w, h);

    const cx = w / 2;
    const cy = h / 2;
    const r = Math.min(w, h) * 0.42;

    // Outer glow
    const glow = ctxSky.createRadialGradient(cx, cy, r * 0.8, cx, cy, r * 1.15);
    glow.addColorStop(0, "rgba(56, 215, 208, 0.08)");
    glow.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctxSky.fillStyle = glow;
    ctxSky.beginPath();
    ctxSky.arc(cx, cy, r * 1.15, 0, Math.PI * 2);
    ctxSky.fill();

    // Apex unit vector in rotated coordinates
    const apexAngleLon = 4.608 + rotY;
    const apexAngleLat = 0.842 + rotX;
    const ax = Math.cos(apexAngleLat) * Math.cos(apexAngleLon);
    const ay = Math.cos(apexAngleLat) * Math.sin(apexAngleLon);
    const az = Math.sin(apexAngleLat);

    // Draw sphere surface points
    const stepsTheta = 60;
    const stepsPhi = 120;

    for (let i = 0; i <= stepsTheta; i++) {
      const theta = (i / stepsTheta) * Math.PI - (Math.PI / 2); // Latitude
      const cosTheta = Math.cos(theta);
      const sinTheta = Math.sin(theta);

      for (let j = 0; j < stepsPhi; j++) {
        const phi = (j / stepsPhi) * Math.PI * 2 + rotY; // Longitude

        const px = cosTheta * Math.cos(phi);
        const py = cosTheta * Math.sin(phi);
        const pz = sinTheta;

        // Rotate by rotX around X axis
        const ry_pz = pz * Math.cos(rotX) - py * Math.sin(rotX);
        const ry_py = pz * Math.sin(rotX) + py * Math.cos(rotX);

        // Discard points on back hemisphere
        if (ry_py < 0) continue;

        const screenX = cx + px * r;
        const screenY = cy - ry_pz * r;

        // Dot product with apex
        const dot = px * ax + py * ay + pz * az;
        const beta = peculiarVelocity / C_LIGHT;
        const norm = (dot * (beta / 1.2336e-3) + 1.0) / 2.0;

        let cr, cg, cb;
        if (norm < 0.5) {
          const t = norm * 2.0;
          cr = Math.floor(11 + t * 20);
          cg = Math.floor(34 + t * 10);
          cb = Math.floor(78 - t * 20);
        } else {
          const t = (norm - 0.5) * 2.0;
          cr = Math.floor(31 + t * 185);
          cg = Math.floor(44 + t * 125);
          cb = Math.floor(58 - t * 10);
        }

        ctxSky.fillStyle = `rgb(${cr}, ${cg}, ${cb})`;
        ctxSky.beginPath();
        ctxSky.arc(screenX, screenY, 2.5, 0, Math.PI * 2);
        ctxSky.fill();
      }
    }

    // Border ring in gold
    ctxSky.strokeStyle = "rgba(212, 175, 55, 0.4)";
    ctxSky.lineWidth = 1.5;
    ctxSky.beginPath();
    ctxSky.arc(cx, cy, r, 0, Math.PI * 2);
    ctxSky.stroke();

    // Crosshairs
    ctxSky.strokeStyle = "rgba(255, 255, 255, 0.1)";
    ctxSky.beginPath();
    ctxSky.moveTo(cx - r, cy); ctxSky.lineTo(cx + r, cy);
    ctxSky.moveTo(cx, cy - r); ctxSky.lineTo(cx, cy + r);
    ctxSky.stroke();

    requestAnimationFrame(drawSky);
  }

  function drawPlanck() {
    if (!ctxPlanck) return;
    const w = canvasPlanck.width;
    const h = canvasPlanck.height;

    ctxPlanck.fillStyle = "#080c14";
    ctxPlanck.fillRect(0, 0, w, h);

    // Coordinate grid
    ctxPlanck.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctxPlanck.lineWidth = 1;
    for (let step = 0; step <= 4; step++) {
      const y = h - 25 - (step / 4.0) * (h - 45);
      ctxPlanck.beginPath();
      ctxPlanck.moveTo(35, y); ctxPlanck.lineTo(w - 15, y);
      ctxPlanck.stroke();
    }

    // Planck curve
    ctxPlanck.strokeStyle = "#d4af37";
    ctxPlanck.lineWidth = 2.5;
    ctxPlanck.beginPath();

    const maxRadNorm = 1.0;
    for (let x = 0; x < w - 50; x++) {
      const nu_ghz = (x / (w - 50)) * 600.0;
      const nu = nu_ghz * 1e9;
      const expo = (6.626e-34 * nu) / (1.38e-23 * T_CMB);
      let rad = 0;
      if (expo < 60.0 && expo > 0) {
        rad = (Math.pow(nu, 3) / (Math.exp(expo) - 1.0)) * 1e-35;
      }
      const normY = rad / 1.76;
      const py = h - 25 - Math.min(1.0, normY) * (h - 45);
      const px = 35 + x;
      if (x === 0) ctxPlanck.moveTo(px, py);
      else ctxPlanck.lineTo(px, py);
    }
    ctxPlanck.stroke();

    // 160.23 GHz Peak Marker
    const peakX = 35 + (160.23 / 600.0) * (w - 50);
    ctxPlanck.strokeStyle = "rgba(56, 215, 208, 0.8)";
    ctxPlanck.setLineDash([4, 4]);
    ctxPlanck.beginPath();
    ctxPlanck.moveTo(peakX, 15); ctxPlanck.lineTo(peakX, h - 25);
    ctxPlanck.stroke();
    ctxPlanck.setLineDash([]);

    ctxPlanck.fillStyle = "#38d7d0";
    ctxPlanck.font = "10px monospace";
    ctxPlanck.fillText("160.23 GHz Peak", peakX - 35, 12);
  }

  function initAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    gainMaster = audioCtx.createGain();
    gainMaster.gain.setValueAtTime(0.35, audioCtx.currentTime);
    gainMaster.connect(audioCtx.destination);

    // Sub-bass 18.65 Hz Planck drone
    oscSub = audioCtx.createOscillator();
    oscSub.type = 'sine';
    oscSub.frequency.setValueAtTime(18.653, audioCtx.currentTime);
    const gainSub = audioCtx.createGain();
    gainSub.gain.setValueAtTime(0.5, audioCtx.currentTime);
    oscSub.connect(gainSub);
    gainSub.connect(gainMaster);
    oscSub.start();

    // Doppler binaural carrier (432 Hz +/- Doppler delta)
    const merger = audioCtx.createChannelMerger(2);

    oscCarrierL = audioCtx.createOscillator();
    oscCarrierL.type = 'sine';
    oscCarrierL.frequency.setValueAtTime(432.0 + 0.532, audioCtx.currentTime);
    const gainL = audioCtx.createGain();
    gainL.gain.setValueAtTime(0.2, audioCtx.currentTime);
    oscCarrierL.connect(gainL);
    gainL.connect(merger, 0, 0); // Left channel

    oscCarrierR = audioCtx.createOscillator();
    oscCarrierR.type = 'sine';
    oscCarrierR.frequency.setValueAtTime(432.0 - 0.532, audioCtx.currentTime);
    const gainR = audioCtx.createGain();
    gainR.gain.setValueAtTime(0.2, audioCtx.currentTime);
    oscCarrierR.connect(gainR);
    gainR.connect(merger, 0, 1); // Right channel

    oscCarrierL.start();
    oscCarrierR.start();

    // Thermal Nyquist noise buffer
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }

    const whiteNoise = audioCtx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    // Filter noise to emulate Penzias-Wilson horn
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(498.0, audioCtx.currentTime);
    filter.Q.setValueAtTime(4.0, audioCtx.currentTime);

    const gainNoise = audioCtx.createGain();
    gainNoise.gain.setValueAtTime(0.08, audioCtx.currentTime);

    whiteNoise.connect(filter);
    filter.connect(gainNoise);
    gainNoise.connect(gainMaster);
    whiteNoise.start();

    merger.connect(gainMaster);
  }

  function toggleAudio() {
    if (!audioCtx) {
      initAudio();
      isPlaying = true;
      if (audioBtn) {
        audioBtn.innerText = "Halt CMB Audio Engine";
        audioBtn.style.borderColor = "var(--accent-gold)";
        audioBtn.style.color = "var(--accent-gold)";
      }
    } else {
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
        isPlaying = true;
        if (audioBtn) audioBtn.innerText = "Halt CMB Audio Engine";
      } else if (audioCtx.state === 'running') {
        audioCtx.suspend();
        isPlaying = false;
        if (audioBtn) audioBtn.innerText = "Synthesize Relic Atmosphere";
      }
    }
  }

  // Mouse interaction for celestial sphere
  if (canvasSky) {
    canvasSky.addEventListener('mousedown', (e) => {
      isDragging = true;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });

    window.addEventListener('mouseup', () => { isDragging = false; });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const dx = e.clientX - lastMouseX;
      const dy = e.clientY - lastMouseY;
      rotY += dx * 0.008;
      rotX += dy * 0.008;
      lastMouseX = e.clientX;
      lastMouseY = e.clientY;
    });
  }

  if (velSlider) {
    velSlider.addEventListener('input', (e) => {
      peculiarVelocity = parseFloat(e.target.value);
      updateCalculations();
    });
  }

  if (audioBtn) {
    audioBtn.addEventListener('click', toggleAudio);
  }

  updateCalculations();
  drawSky();
  drawPlanck();
})();

