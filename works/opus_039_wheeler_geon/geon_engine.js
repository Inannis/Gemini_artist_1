/**
 * GEON ENGINE · INTERACTIVE CHAMBER 19
 * Studio Anamnesis · Series XXXVII (Topological Geometrodynamics) · OPUS-039
 * 
 * Implements:
 * 1. Morris-Thorne-Wheeler 3D Hyperboloid Embedding & Raymarcher
 * 2. Trapped Source-Free Electric Flux Streamlines (Charge Without Charge)
 * 3. Interactive WebAudio Resonant Throat Cavity Synthesizer
 * 4. Kerr-Wheeler Frame-Dragging Rotation & Planck Foam Noise
 * 5. Wheeler Supercritical Pinch-Off Catastrophe Animation
 */

(function() {
  const canvas = document.getElementById('geonCanvas');
  const ctx = canvas.getContext('2d');

  // Parameters
  let b0 = 1.414;        // Throat radius in ell_P
  let flux = 1.0;        // Trapped flux units
  let spin = 0.75;       // Frame dragging spin
  let foam = 0.60;       // Planck foam density
  let isRuptured = false;
  let ruptureProgress = 0.0;

  // Camera Orbit Controls
  let rotX = 26 * Math.PI / 180;
  let rotY = 0.0;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;

  // DOM Elements
  const sliderB0 = document.getElementById('slider-b0');
  const sliderFlux = document.getElementById('slider-flux');
  const sliderSpin = document.getElementById('slider-spin');
  const sliderFoam = document.getElementById('slider-foam');

  const valB0 = document.getElementById('val-b0');
  const valFlux = document.getElementById('val-flux');
  const valSpin = document.getElementById('val-spin');
  const valFoam = document.getElementById('val-foam');

  const telFreq = document.getElementById('tel-freq');
  const telStability = document.getElementById('tel-stability');
  const telStatus = document.getElementById('tel-status');
  const telBetti = document.getElementById('tel-betti');
  const telCharge = document.getElementById('tel-charge');
  const btnPinch = document.getElementById('btn-pinch');
  const btnAudio = document.getElementById('btn-audio');

  // Resize Handling
  function resize() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = canvas.parentElement.clientWidth * dpr;
    canvas.height = canvas.parentElement.clientHeight * dpr;
    ctx.scale(dpr, dpr);
  }
  window.addEventListener('resize', resize);
  resize();

  // Mouse / Touch Interaction
  canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });
  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;
    rotY += dx * 0.008;
    rotX = Math.max(-Math.PI * 0.45, Math.min(Math.PI * 0.45, rotX + dy * 0.008));
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });
  window.addEventListener('mouseup', () => { isDragging = false; });

  canvas.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      isDragging = true;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    }
  }, { passive: true });
  window.addEventListener('touchmove', (e) => {
    if (!isDragging || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - lastMouseX;
    const dy = e.touches[0].clientY - lastMouseY;
    rotY += dx * 0.008;
    rotX = Math.max(-Math.PI * 0.45, Math.min(Math.PI * 0.45, rotX + dy * 0.008));
    lastMouseX = e.touches[0].clientX;
    lastMouseY = e.touches[0].clientY;
  }, { passive: true });
  window.addEventListener('touchend', () => { isDragging = false; });

  // Slider Events
  sliderB0.addEventListener('input', (e) => {
    b0 = parseFloat(e.target.value);
    valB0.textContent = b0.toFixed(2);
    updateAudio();
    updateHUD();
  });
  sliderFlux.addEventListener('input', (e) => {
    flux = parseFloat(e.target.value);
    valFlux.textContent = flux.toFixed(2);
    updateAudio();
    updateHUD();
  });
  sliderSpin.addEventListener('input', (e) => {
    spin = parseFloat(e.target.value);
    valSpin.textContent = spin.toFixed(2);
    updateAudio();
  });
  sliderFoam.addEventListener('input', (e) => {
    foam = parseFloat(e.target.value);
    valFoam.textContent = foam.toFixed(2);
  });

  // Telemetry HUD Update
  function updateHUD() {
    const f0 = 77.92 * (1.414 / Math.max(0.05, b0));
    telFreq.textContent = `${f0.toFixed(1)} Hz`;

    // Stability: xi = b0 / (flux * 0.085)
    const xi = b0 / (flux * 0.085);
    telStability.textContent = xi.toFixed(2);

    if (isRuptured || xi <= 1.0) {
      telStatus.innerHTML = '<span class="status-badge status-rupture">SINGULARITY RUPTURE</span>';
      telBetti.textContent = 'b₂ = 0 (Severed)';
      telCharge.textContent = 'TERMINATED IN SINGULARITY';
    } else {
      telStatus.innerHTML = '<span class="status-badge status-stable">STABLE GEON</span>';
      telBetti.textContent = 'b₂ = 1 (Non-Trivial)';
      telCharge.textContent = `±${(flux * 1.60).toFixed(2)} × 10⁻¹⁹ C`;
    }
  }

  // WebAudio Engine
  let audioCtx = null;
  let osc1 = null;
  let osc2 = null;
  let gainNode = null;
  let tremoloGain = null;
  let isAudioPlaying = false;

  window.toggleAudio = function() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      
      // Master Gain
      gainNode = audioCtx.createGain();
      gainNode.gain.setValueAtTime(0.0, audioCtx.currentTime);
      gainNode.connect(audioCtx.destination);

      // Tremolo (Kerr Beat)
      tremoloGain = audioCtx.createGain();
      tremoloGain.gain.setValueAtTime(0.7, audioCtx.currentTime);
      tremoloGain.connect(gainNode);

      // Oscillators
      osc1 = audioCtx.createOscillator();
      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(77.92, audioCtx.currentTime);
      osc1.connect(tremoloGain);
      osc1.start();

      osc2 = audioCtx.createOscillator();
      osc2.type = 'triangle';
      osc2.frequency.setValueAtTime(77.92 * 1.5, audioCtx.currentTime);
      
      const osc2Gain = audioCtx.createGain();
      osc2Gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
      osc2.connect(osc2Gain);
      osc2Gain.connect(tremoloGain);
      osc2.start();
    }

    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    isAudioPlaying = !isAudioPlaying;
    if (isAudioPlaying) {
      gainNode.gain.setTargetAtTime(0.25, audioCtx.currentTime, 0.1);
      btnAudio.textContent = '◼ Pause Audio';
      btnAudio.style.background = 'rgba(56, 215, 210, 0.2)';
    } else {
      gainNode.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.1);
      btnAudio.textContent = '▶ Resonant Audio';
      btnAudio.style.background = '';
    }
    updateAudio();
  };

  function updateAudio() {
    if (!audioCtx || !isAudioPlaying) return;
    const f0 = 77.92 * (1.414 / Math.max(0.05, b0));
    osc1.frequency.setTargetAtTime(f0, audioCtx.currentTime, 0.05);
    osc2.frequency.setTargetAtTime(f0 * 1.5, audioCtx.currentTime, 0.05);
  }

  // Pinch-off Collapse Trigger
  window.triggerPinchCollapse = function() {
    if (isRuptured) {
      // Restore
      isRuptured = false;
      ruptureProgress = 0.0;
      b0 = 1.414;
      sliderB0.value = "1.41";
      valB0.textContent = "1.41";
      btnPinch.textContent = "⚡ Overdrive Pinch";
      btnPinch.className = "btn btn-danger";
      updateAudio();
      updateHUD();
      return;
    }

    isRuptured = true;
    btnPinch.textContent = "↺ Restore Topology";
    btnPinch.className = "btn";
    updateHUD();

    if (audioCtx && isAudioPlaying) {
      // Screaming frequency sweep
      osc1.frequency.setTargetAtTime(950.0, audioCtx.currentTime, 0.4);
      setTimeout(() => {
        gainNode.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.2);
      }, 700);
    }
  };

  // 3D Projection Helpers
  function project(x, y, z, cx, cy) {
    // Rotate around Y-axis (rotY)
    const cosY = Math.cos(rotY);
    const sinY = Math.sin(rotY);
    const x1 = x * cosY - z * sinY;
    const z1 = x * sinY + z * cosY;

    // Rotate around X-axis (rotX)
    const cosX = Math.cos(rotX);
    const sinX = Math.sin(rotX);
    const y2 = y * cosX - z1 * sinX;
    const z2 = y * sinX + z1 * cosX;

    // Weak perspective
    const fov = 750.0;
    const scale = fov / (fov + z2);
    return {
      x: cx + x1 * scale,
      y: cy + y2 * scale,
      scale: scale,
      z: z2
    };
  }

  // Animation Loop
  let time = 0;
  function animate() {
    time += 0.02;

    const w = canvas.width / (window.devicePixelRatio || 1);
    const h = canvas.height / (window.devicePixelRatio || 1);
    const cx = w / 2;
    const cy = h / 2;

    ctx.clearRect(0, 0, w, h);

    // Dynamic b0 under rupture animation
    let effectiveB0 = b0;
    if (isRuptured) {
      ruptureProgress = Math.min(1.0, ruptureProgress + 0.03);
      effectiveB0 = b0 * (1.0 - ruptureProgress) + 0.05 * ruptureProgress;
    }
    const b0_px = effectiveB0 * 45.0;

    // 1. Render Planck Foam Background Particles
    if (foam > 0.05) {
      ctx.fillStyle = 'rgba(56, 215, 210, 0.12)';
      const numFoam = Math.floor(40 * foam);
      for (let i = 0; i < numFoam; i++) {
        const fx = (Math.sin(i * 9.1 + time * 0.4) * 0.5 + 0.5) * w;
        const fy = (Math.cos(i * 13.7 + time * 0.3) * 0.5 + 0.5) * h;
        const fr = (Math.sin(time * 2.0 + i) * 0.5 + 0.5) * 2.0 + 0.5;
        ctx.beginPath();
        ctx.arc(fx, fy, fr, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // 2. Render Secondary Micro-Wormholes
    const secondaryHandles = [
      { x: -160, y: -80, b: 12, s: -0.7 },
      { x: 180, y: 70, b: 14, s: 0.8 },
      { x: -90, y: 120, b: 10, s: 0.5 },
      { x: 110, y: -110, b: 11, s: -0.6 }
    ];

    secondaryHandles.forEach(hnd => {
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.25)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let p = 0; p <= 32; p++) {
        const phi = (p / 32) * Math.PI * 2;
        const pt = project(hnd.x + hnd.b * Math.cos(phi), hnd.y + hnd.b * Math.sin(phi), 0, cx, cy);
        if (p === 0) ctx.moveTo(pt.x, pt.y);
        else ctx.lineTo(pt.x, pt.y);
      }
      ctx.stroke();
    });

    // 3. Render Primary MTW Wormhole Throat Ribs (Dual Sheets)
    const sheets = [+1, -1];
    sheets.forEach(sheetSign => {
      const numRings = 24;
      for (let rIdx = 0; rIdx < numRings; rIdx++) {
        const r = b0_px + Math.pow(rIdx, 1.35) * 6.5;
        const z = sheetSign * 2.0 * Math.sqrt(b0_px * Math.max(0, r - b0_px));
        const redshift = Math.sqrt(Math.max(0.08, 1.0 - (b0_px / r)));

        if (sheetSign > 0) {
          ctx.strokeStyle = `rgba(56, 215, 210, ${0.15 + (1.0 - redshift) * 0.4})`;
        } else {
          ctx.strokeStyle = `rgba(168, 85, 247, ${0.15 + (1.0 - redshift) * 0.4})`;
        }
        ctx.lineWidth = 1;

        ctx.beginPath();
        const numPts = 48;
        for (let p = 0; p <= numPts; p++) {
          const phi = (p / numPts) * Math.PI * 2;
          const phiDrag = phi + (spin * 1.8 / Math.sqrt(Math.max(1.0, r / b0_px))) + time * 0.2 * spin;
          const pt = project(r * Math.cos(phiDrag), z, r * Math.sin(phiDrag), cx, cy);
          if (p === 0) ctx.moveTo(pt.x, pt.y);
          else ctx.lineTo(pt.x, pt.y);
        }
        ctx.stroke();
      }
    });

    // 4. Render Trapped Source-Free Electric Flux Streamlines
    if (!isRuptured) {
      const numLines = Math.floor(28 * flux);
      ctx.lineWidth = 1.5;
      for (let l = 0; l < numLines; l++) {
        const basePhi = (l / numLines) * Math.PI * 2;
        ctx.beginPath();

        const numSteps = 50;
        for (let s = 0; s <= numSteps; s++) {
          const tNorm = (s - numSteps / 2.0) / (numSteps / 2.0); // -1.0 to +1.0
          const sSign = tNorm >= 0 ? 1 : -1;
          const rCur = b0_px + Math.pow(Math.abs(tNorm), 1.6) * 160.0;
          const zCur = sSign * 2.0 * Math.sqrt(b0_px * Math.max(0, rCur - b0_px));
          const phiCur = basePhi + spin * (2.8 / Math.sqrt(Math.max(1.0, rCur / b0_px))) * (sSign > 0 ? 1 : -1) + time * 0.3 * spin;

          const pt = project(rCur * Math.cos(phiCur), zCur, rCur * Math.sin(phiCur), cx, cy);
          if (s === 0) ctx.moveTo(pt.x, pt.y);
          else ctx.lineTo(pt.x, pt.y);
        }

        ctx.strokeStyle = `rgba(212, 175, 55, ${0.4 + 0.3 * Math.sin(time * 3.0 + l)})`;
        ctx.stroke();
      }
    } else {
      // Singularity Shear Blowout Lines
      ctx.strokeStyle = 'rgba(239, 68, 68, 0.7)';
      ctx.lineWidth = 2;
      for (let ray = 0; ray < 24; ray++) {
        const angle = (ray / 24) * Math.PI * 2 + time * 2.0;
        const len = 30 + Math.sin(ray * 5.0 + time * 10.0) * 120.0;
        const pt1 = project(0, 0, 0, cx, cy);
        const pt2 = project(len * Math.cos(angle), len * Math.sin(angle) * 0.5, len * Math.sin(angle), cx, cy);
        ctx.beginPath();
        ctx.moveTo(pt1.x, pt1.y);
        ctx.lineTo(pt2.x, pt2.y);
        ctx.stroke();
      }
    }

    // 5. Throat Neck Non-Contractible 2-Cycle Aperture
    ctx.strokeStyle = isRuptured ? 'rgba(255, 255, 255, 0.9)' : 'rgba(212, 175, 55, 0.85)';
    ctx.lineWidth = isRuptured ? 3 : 2;
    ctx.beginPath();
    for (let p = 0; p <= 64; p++) {
      const phi = (p / 64) * Math.PI * 2;
      const pt = project(b0_px * Math.cos(phi), 0, b0_px * Math.sin(phi), cx, cy);
      if (p === 0) ctx.moveTo(pt.x, pt.y);
      else ctx.lineTo(pt.x, pt.y);
    }
    ctx.stroke();

    requestAnimationFrame(animate);
  }

  animate();
})();
