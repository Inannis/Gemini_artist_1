/**
 * STUDIO ANAMNESIS · CHAMBER 13 INTERACTIVE ENGINE
 * The Boltzmann Horizon: Ergodic Phase Space & Poincaré Recurrence
 * Zero-dependency procedural Canvas & Web Audio API simulation.
 */

(function () {
  'use strict';

  // --- DOM Elements ---
  const canvas = document.getElementById('recurrence-canvas');
  const ctx = canvas.getContext('2d');
  const container = document.getElementById('canvas-container');

  const hudTemp = document.getElementById('hud-temp');
  const hudDist = document.getElementById('hud-dist');
  const hudState = document.getElementById('hud-state');

  const btnAudio = document.getElementById('btn-audio');
  const audioIcon = document.getElementById('audio-icon');
  const audioText = document.getElementById('audio-text');
  const btnRecurrenceStrike = document.getElementById('btn-recurrence-strike');
  const btnNucleate = document.getElementById('btn-nucleate-cluster');

  const sliderWinding = document.getElementById('slider-winding');
  const valWinding = document.getElementById('val-winding');
  const sliderOmega3 = document.getElementById('slider-omega3');
  const valOmega3 = document.getElementById('val-omega3');
  const sliderSpeed = document.getElementById('slider-speed');
  const valSpeed = document.getElementById('val-speed');
  const sliderTime = document.getElementById('slider-time');
  const valTime = document.getElementById('val-time');
  const sliderTemp = document.getElementById('slider-temp');
  const valTemp = document.getElementById('val-temp');

  // --- Physical & Simulation State ---
  let width = (canvas.width = container.clientWidth);
  let height = (canvas.height = container.clientHeight);

  let omega1 = 1.0;
  let omega2 = parseFloat(sliderWinding.value);
  let omega3 = parseFloat(sliderOmega3.value);
  let speedMult = parseFloat(sliderSpeed.value);
  let logTime = parseFloat(sliderTime.value);
  let tempMult = parseFloat(sliderTemp.value);

  let timeSim = 0.0;
  let trajectoryHistory = [];
  const maxHistory = 4000;

  let clusters = [];
  let strikePulse = 0.0;
  let audioContext = null;
  let audioActive = false;

  // Shepard-Risset Synth State
  let shepardNodes = [];
  let droneGain = null;

  // --- Audio Synthesis Engine ---
  function initAudio() {
    if (audioContext) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    audioContext = new AudioCtx();

    // 1. Gibbons-Hawking Sub-Bass Drone (26.55 Hz)
    const droneOsc = audioContext.createOscillator();
    droneOsc.type = 'sine';
    droneOsc.frequency.setValueAtTime(26.55, audioContext.currentTime);

    const droneFilter = audioContext.createBiquadFilter();
    droneFilter.type = 'lowpass';
    droneFilter.frequency.setValueAtTime(80.0, audioContext.currentTime);

    droneGain = audioContext.createGain();
    droneGain.gain.setValueAtTime(0.35, audioContext.currentTime);

    droneOsc.connect(droneFilter);
    droneFilter.connect(droneGain);
    droneGain.connect(audioContext.destination);
    droneOsc.start();

    // 2. Shepard-Risset Pitch Glissando Bank (10 Octaves)
    const baseFreq = 27.5; // A0
    const numOctaves = 8;
    for (let i = 0; i < numOctaves; i++) {
      const osc = audioContext.createOscillator();
      osc.type = 'sine';

      const gain = audioContext.createGain();
      gain.gain.setValueAtTime(0.0, audioContext.currentTime);

      osc.connect(gain);
      gain.connect(audioContext.destination);
      osc.start();

      shepardNodes.push({ osc, gain, octIndex: i });
    }

    audioActive = true;
    audioIcon.textContent = '■';
    audioText.textContent = 'Mute Sound Engine';
  }

  function updateShepardAudio(t) {
    if (!audioActive || !audioContext) return;

    const sweepRate = 0.06 * speedMult;
    const baseFreq = 27.5;
    const numOctaves = shepardNodes.length;
    const cyclicT = (t * sweepRate) % 1.0;
    const octaveCenter = Math.log2(220.0 / baseFreq);
    const octaveSigma = 1.4;

    for (let i = 0; i < numOctaves; i++) {
      const node = shepardNodes[i];
      const octPos = (i + cyclicT) % numOctaves;
      const freq = baseFreq * Math.pow(2.0, octPos);

      const distOct = octPos - octaveCenter;
      const amp = Math.exp(-0.5 * Math.pow(distOct / octaveSigma, 2)) * 0.18;

      node.osc.frequency.setTargetAtTime(freq, audioContext.currentTime, 0.05);
      node.gain.gain.setTargetAtTime(amp, audioContext.currentTime, 0.05);
    }
  }

  function triggerQuartzChime() {
    if (!audioActive || !audioContext) return;
    const chimes = [43.2, 89.4, 235.4, 520.1, 1040.2];
    chimes.forEach((f, idx) => {
      const osc = audioContext.createOscillator();
      const gain = audioContext.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(f, audioContext.currentTime);

      const decayTime = 1.5 + idx * 0.3;
      gain.gain.setValueAtTime(0.08, audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + decayTime);

      osc.connect(gain);
      gain.connect(audioContext.destination);
      osc.start();
      osc.stop(audioContext.currentTime + decayTime + 0.1);
    });
  }

  function triggerRecurrenceStrike() {
    strikePulse = 1.0;
    hudState.textContent = 'POINCARÉ RECURRENCE OCCURRING (ε → 0)';
    hudState.style.color = '#38d7d0';

    if (audioActive && audioContext) {
      const cornerstones = [43.2, 78.4, 125.1, 226.4];
      cornerstones.forEach((f) => {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(f, audioContext.currentTime);

        gain.gain.setValueAtTime(0.18, audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + 4.5);

        osc.connect(gain);
        gain.connect(audioContext.destination);
        osc.start();
        osc.stop(audioContext.currentTime + 4.6);
      });
    }

    setTimeout(() => {
      hudState.textContent = 'Asymptotic Ergodic Drift';
      hudState.style.color = 'var(--accent-gold)';
    }, 4500);
  }

  // --- UI Event Handlers ---
  sliderWinding.addEventListener('input', (e) => {
    omega2 = parseFloat(e.target.value);
    valWinding.textContent = omega2.toFixed(4);
  });

  sliderOmega3.addEventListener('input', (e) => {
    omega3 = parseFloat(e.target.value);
    valOmega3.textContent = omega3.toFixed(4);
  });

  sliderSpeed.addEventListener('input', (e) => {
    speedMult = parseFloat(e.target.value);
    valSpeed.textContent = speedMult.toFixed(2) + ' ×';
  });

  sliderTime.addEventListener('input', (e) => {
    logTime = parseFloat(e.target.value);
    valTime.textContent = '10^' + logTime.toFixed(0) + ' yr';
  });

  sliderTemp.addEventListener('input', (e) => {
    tempMult = parseFloat(e.target.value);
    valTemp.textContent = tempMult.toFixed(1) + ' × T_dS';
    hudTemp.textContent = (2.655 * tempMult).toFixed(3) + ' × 10⁻³⁰ K';
  });

  btnAudio.addEventListener('click', () => {
    if (!audioContext) {
      initAudio();
    } else if (audioContext.state === 'suspended') {
      audioContext.resume();
      audioActive = true;
      audioIcon.textContent = '■';
      audioText.textContent = 'Mute Sound Engine';
    } else {
      audioContext.suspend();
      audioActive = false;
      audioIcon.textContent = '▶';
      audioText.textContent = 'Activate Sound Engine';
    }
  });

  btnRecurrenceStrike.addEventListener('click', () => {
    triggerRecurrenceStrike();
  });

  btnNucleate.addEventListener('click', () => {
    const cx = width / 2;
    const cy = height / 2;
    const ang = Math.random() * Math.PI * 2;
    const dist = 60 + Math.random() * 180;
    clusters.push({
      x: cx + dist * Math.cos(ang),
      y: cy + dist * Math.sin(ang),
      radius: 20 + Math.random() * 25,
      life: 1.0
    });
    triggerQuartzChime();
  });

  window.addEventListener('resize', () => {
    width = canvas.width = container.clientWidth;
    height = canvas.height = container.clientHeight;
  });

  // --- Simulation Animation Loop ---
  function animate() {
    requestAnimationFrame(animate);

    ctx.fillStyle = '#020308';
    ctx.fillRect(0, 0, width, height);

    const cx = width / 2;
    const cy = height / 2;
    const rHorizon = Math.min(width, height) * 0.42;

    timeSim += 0.015 * speedMult;
    updateShepardAudio(timeSim);

    // 1. Draw de Sitter Horizon
    ctx.save();
    ctx.beginPath();
    const multipoles = [
      { m: 3, amp: 0.016, phase: 0.42 },
      { m: 5, amp: 0.011, phase: 1.25 },
      { m: 8, amp: 0.007, phase: 2.48 }
    ];

    for (let a = 0; a <= Math.PI * 2 + 0.1; a += 0.05) {
      let r = rHorizon;
      for (let mp of multipoles) {
        r += rHorizon * mp.amp * Math.cos(mp.m * a + mp.phase + timeSim * 0.2);
      }
      const hx = cx + r * Math.cos(a);
      const hy = cy + r * Math.sin(a);
      if (a === 0) ctx.moveTo(hx, hy);
      else ctx.lineTo(hx, hy);
    }
    ctx.closePath();

    // Horizon interior glow
    const grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, rHorizon);
    grad.addColorStop(0, 'rgba(15, 25, 45, 0.4)');
    grad.addColorStop(0.7, 'rgba(30, 50, 85, 0.35)');
    grad.addColorStop(0.95, 'rgba(56, 215, 208, 0.25)');
    grad.addColorStop(1, 'rgba(212, 175, 55, 0.8)');
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.strokeStyle = strikePulse > 0.1 ? '#fff' : 'rgba(212, 175, 55, 0.7)';
    ctx.lineWidth = 2 + strikePulse * 4;
    ctx.stroke();
    ctx.restore();

    // 2. Compute Current Toroidal Phase Space Trajectory Step
    const r1 = rHorizon * 0.62;
    const r2 = rHorizon * 0.26;
    const r3 = rHorizon * 0.09;

    const tx = (r1 + r2 * Math.cos(omega2 * timeSim) + r3 * Math.cos(omega3 * timeSim)) * Math.cos(omega1 * timeSim);
    const ty = ((r1 + r2 * Math.cos(omega2 * timeSim) + r3 * Math.cos(omega3 * timeSim)) * Math.sin(omega1 * timeSim)) * 0.65 +
               (r2 * Math.sin(omega2 * timeSim)) * 0.40;

    const curX = cx + tx;
    const curY = cy + ty;

    trajectoryHistory.push({ x: curX, y: curY, t: timeSim });
    if (trajectoryHistory.length > maxHistory) trajectoryHistory.shift();

    // Calculate distance to initial point (0, 0)
    const distToOrigin = Math.sqrt(tx * tx + ty * ty) / rHorizon;
    hudDist.textContent = distToOrigin.toFixed(4);

    // 3. Render Trajectory Filaments
    ctx.save();
    ctx.lineWidth = 1.4;
    for (let i = 1; i < trajectoryHistory.length; i += 2) {
      const p0 = trajectoryHistory[i - 1];
      const p1 = trajectoryHistory[i];
      const frac = i / trajectoryHistory.length;

      ctx.beginPath();
      ctx.moveTo(p0.x, p0.y);
      ctx.lineTo(p1.x, p1.y);

      if (frac < 0.5) {
        ctx.strokeStyle = `rgba(56, 215, 208, ${frac * 0.7})`;
      } else {
        ctx.strokeStyle = `rgba(212, 175, 55, ${frac * 0.9})`;
      }
      ctx.stroke();
    }
    ctx.restore();

    // 4. Render Spontaneous Microstate Clusters
    for (let c of clusters) {
      ctx.save();
      ctx.strokeStyle = `rgba(255, 235, 160, ${c.life})`;
      ctx.fillStyle = `rgba(56, 215, 208, ${c.life * 0.25})`;
      ctx.beginPath();
      for (let s = 0; s < 6; s++) {
        const ang = s * (Math.PI / 3);
        const px = c.x + c.radius * Math.cos(ang);
        const py = c.y + c.radius * Math.sin(ang);
        if (s === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Fade out slowly
      c.life -= 0.003;
      ctx.restore();
    }
    clusters = clusters.filter(c => c.life > 0.0);

    // 5. Central Recurrence Singularity
    ctx.save();
    const coreGlow = ctx.createRadialGradient(cx, cy, 2, cx, cy, 45 + strikePulse * 90);
    coreGlow.addColorStop(0, '#ffffff');
    coreGlow.addColorStop(0.3, 'rgba(212, 175, 55, 0.85)');
    coreGlow.addColorStop(0.7, 'rgba(56, 215, 208, 0.4)');
    coreGlow.addColorStop(1, 'rgba(0,0,0,0)');

    ctx.fillStyle = coreGlow;
    ctx.beginPath();
    ctx.arc(cx, cy, 45 + strikePulse * 90, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Decay strike pulse
    if (strikePulse > 0.01) {
      strikePulse *= 0.94;
    }
  }

  animate();
})();

