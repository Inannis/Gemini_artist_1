/**
 * moyal_engine.js
 * Studio Anamnesis · Chamber 17 Engine
 * Non-Commutative Spacetime, Fuzzy Sphere & Dirac Operator Synthesizer
 * Zero external dependencies (vanilla Canvas & WebAudio API).
 */

(function() {
  const canvas = document.getElementById("moyal-canvas");
  const ctx = canvas.getContext("2d");
  
  // Controls & Telemetry
  const paramTheta = document.getElementById("param-theta");
  const paramDim = document.getElementById("param-dim");
  const paramShells = document.getElementById("param-shells");
  const paramSpeed = document.getElementById("param-speed");
  
  const valTheta = document.getElementById("val-theta");
  const valDim = document.getElementById("val-dim");
  const valShells = document.getElementById("val-shells");
  const valSpeed = document.getElementById("val-speed");
  
  const telemTheta = document.getElementById("telem-theta");
  const telemUncertainty = document.getElementById("telem-uncertainty");
  const telemCells = document.getElementById("telem-cells");
  const telemDirac = document.getElementById("telem-dirac");
  
  const audioToggle = document.getElementById("audio-toggle");

  // State
  let thetaRatio = parseFloat(paramTheta.value);
  let matrixDim = parseInt(paramDim.value);
  let shellCount = parseInt(paramShells.value);
  let rotSpeed = parseFloat(paramSpeed.value);
  
  let rotX = 0.52;
  let rotY = 0.65;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;
  
  let cells = [];
  let links = [];

  // Generate Quantum Matrix Cells on Fuzzy Sphere
  function generateFuzzyManifold() {
    cells = [];
    links = [];
    
    const goldenAngle = Math.PI * (3.0 - Math.sqrt(5.0));
    const baseRadius = 260.0;
    
    for (let s = 0; s < shellCount; s++) {
      let shellN = matrixDim;
      let shellRadius = baseRadius;
      let tier = "MID";
      
      if (shellCount === 1) {
        shellN = matrixDim;
        shellRadius = baseRadius;
        tier = "MID";
      } else if (shellCount === 2) {
        if (s === 0) { shellN = matrixDim; shellRadius = baseRadius * 1.25; tier = "UV"; }
        else { shellN = Math.max(16, Math.floor(matrixDim / 2)); shellRadius = baseRadius * 0.65; tier = "IR"; }
      } else {
        if (s === 0) { shellN = Math.min(64, Math.floor(matrixDim * 1.3)); shellRadius = baseRadius * 1.35; tier = "UV"; }
        else if (s === 1) { shellN = matrixDim; shellRadius = baseRadius * 0.90; tier = "MID"; }
        else { shellN = Math.max(12, Math.floor(matrixDim * 0.5)); shellRadius = baseRadius * 0.50; tier = "IR"; }
      }
      
      let totalPts = shellN * shellN;
      let thetaN = (2.0 / Math.sqrt(shellN * shellN - 1.0)) * thetaRatio;
      
      let shellStartIndex = cells.length;
      
      for (let k = 0; k < totalPts; k++) {
        let z_k = 1.0 - (2.0 * k + 1.0) / totalPts;
        let r_xy = Math.sqrt(Math.max(0.0, 1.0 - z_k * z_k));
        let phi_k = k * goldenAngle;
        
        let x_k = r_xy * Math.cos(phi_k);
        let y_k = r_xy * Math.sin(phi_k);
        
        // Non-commutative Moyal matrix perturbation
        let dx = thetaN * 0.35 * Math.sin(7.0 * phi_k) * z_k;
        let dy = thetaN * 0.35 * Math.cos(7.0 * phi_k) * z_k;
        let dz = -thetaN * 0.35 * (x_k * Math.sin(phi_k) + y_k * Math.cos(phi_k));
        
        x_k += dx;
        y_k += dy;
        z_k += dz;
        let mag = Math.sqrt(x_k * x_k + y_k * y_k + z_k * z_k);
        x_k /= mag;
        y_k /= mag;
        z_k /= mag;
        
        cells.push({
          x: x_k * shellRadius,
          y: y_k * shellRadius,
          z: z_k * shellRadius,
          tier: tier,
          shellIdx: s,
          k: k
        });
      }
      
      // Commutator links between adjacent cells
      let stride = Math.max(10, Math.floor(totalPts / 120));
      for (let i = shellStartIndex; i < cells.length; i += stride) {
        for (let j = i + 1; j < Math.min(i + 16, cells.length); j++) {
          let c1 = cells[i];
          let c2 = cells[j];
          let ddx = c1.x - c2.x;
          let ddy = c1.y - c2.y;
          let ddz = c1.z - c2.z;
          let distSq = ddx * ddx + ddy * ddy + ddz * ddz;
          if (distSq < (shellRadius * 0.32) * (shellRadius * 0.32)) {
            links.push({ from: i, to: j, tier: tier });
          }
        }
      }
    }
    
    updateTelemetry();
  }

  function updateTelemetry() {
    let theta_si = (thetaRatio * 2.61228e-70).toExponential(3);
    let unc_si = (0.5 * thetaRatio * 2.61228e-70).toExponential(3);
    let totalCells = cells.length;
    let diracF0 = (27.50 * Math.sqrt(1.0 + 0.1 * (thetaRatio - 1.0))).toFixed(2);
    
    valTheta.textContent = thetaRatio.toFixed(2) + " ℓ_P²";
    valDim.textContent = matrixDim.toString();
    valShells.textContent = shellCount.toString();
    valSpeed.textContent = rotSpeed.toFixed(2) + "x";
    
    telemTheta.textContent = theta_si + " m²";
    telemUncertainty.textContent = "≥ " + unc_si + " m²";
    telemCells.textContent = totalCells.toLocaleString();
    telemDirac.textContent = diracF0 + " Hz (A₀)";
    
    if (audioActive) {
      updateAudioFrequencies();
    }
  }

  // Canvas Resize
  function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
  }

  window.addEventListener("resize", resizeCanvas);

  // Mouse & Touch Interaction
  canvas.addEventListener("mousedown", (e) => {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  window.addEventListener("mouseup", () => { isDragging = false; });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;
    rotY += dx * 0.007;
    rotX += dy * 0.007;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  // Touch Support
  canvas.addEventListener("touchstart", (e) => {
    if (e.touches.length === 1) {
      isDragging = true;
      lastMouseX = e.touches[0].clientX;
      lastMouseY = e.touches[0].clientY;
    }
  }, { passive: true });

  canvas.addEventListener("touchmove", (e) => {
    if (!isDragging || e.touches.length !== 1) return;
    const dx = e.touches[0].clientX - lastMouseX;
    const dy = e.touches[0].clientY - lastMouseY;
    rotY += dx * 0.008;
    rotX += dy * 0.008;
    lastMouseX = e.touches[0].clientX;
    lastMouseY = e.touches[0].clientY;
  }, { passive: true });

  window.addEventListener("touchend", () => { isDragging = false; });

  // Control Listeners
  paramTheta.addEventListener("input", () => {
    thetaRatio = parseFloat(paramTheta.value);
    generateFuzzyManifold();
  });

  paramDim.addEventListener("input", () => {
    matrixDim = parseInt(paramDim.value);
    generateFuzzyManifold();
  });

  paramShells.addEventListener("input", () => {
    shellCount = parseInt(paramShells.value);
    generateFuzzyManifold();
  });

  paramSpeed.addEventListener("input", () => {
    rotSpeed = parseFloat(paramSpeed.value);
    valSpeed.textContent = rotSpeed.toFixed(2) + "x";
  });

  // WebAudio Dirac Operator Chords
  let audioCtx = null;
  let audioActive = false;
  let masterGain = null;
  let oscillators = [];
  let filterNode = null;

  function initAudio() {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    audioCtx = new AudioContextClass();
    
    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.0001, audioCtx.currentTime);
    
    filterNode = audioCtx.createBiquadFilter();
    filterNode.type = "lowpass";
    filterNode.frequency.setValueAtTime(650, audioCtx.currentTime);
    filterNode.Q.setValueAtTime(2.5, audioCtx.currentTime);
    
    filterNode.connect(masterGain);
    masterGain.connect(audioCtx.destination);
    
    // 5 Dirac operator harmonics: f_n = 55 * (n + 0.5)
    const baseHarmonics = [27.5, 82.5, 137.5, 192.5, 247.5];
    oscillators = [];
    
    baseHarmonics.forEach((freq, idx) => {
      let osc = audioCtx.createOscillator();
      let oscGain = audioCtx.createGain();
      
      osc.type = idx === 0 ? "sine" : "triangle";
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      
      let amp = [0.45, 0.30, 0.22, 0.15, 0.10][idx];
      oscGain.gain.setValueAtTime(amp, audioCtx.currentTime);
      
      osc.connect(oscGain);
      oscGain.connect(filterNode);
      osc.start();
      
      oscillators.push({ osc, gain: oscGain, baseFreq: freq });
    });
  }

  function updateAudioFrequencies() {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    const freqScale = Math.sqrt(1.0 + 0.15 * (thetaRatio - 1.0));
    
    oscillators.forEach((o, idx) => {
      let f = o.baseFreq * freqScale;
      // Slight non-commutative micro-detune based on matrix dimension
      let detune = (idx + 1) * (matrixDim - 32) * 0.1;
      o.osc.frequency.setTargetAtTime(f + detune, now, 0.1);
    });
    
    filterNode.frequency.setTargetAtTime(500 + thetaRatio * 200, now, 0.1);
  }

  audioToggle.addEventListener("click", () => {
    if (!audioCtx) {
      initAudio();
    }
    
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }
    
    audioActive = !audioActive;
    if (audioActive) {
      masterGain.gain.setTargetAtTime(0.28, audioCtx.currentTime, 0.2);
      audioToggle.textContent = "Mute Dirac Acoustics";
      audioToggle.classList.add("active");
    } else {
      masterGain.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.2);
      audioToggle.textContent = "Engage Dirac Acoustics";
      audioToggle.classList.remove("active");
    }
  });

  // Render Loop
  let lastTime = performance.now();

  function render(time) {
    const dt = (time - lastTime) * 0.001;
    lastTime = time;
    
    if (!isDragging) {
      rotY += 0.25 * rotSpeed * dt;
      rotX += 0.08 * rotSpeed * dt;
    }
    
    const rect = canvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;
    const cx = w * 0.5;
    const cy = h * 0.5;
    
    // Clear
    ctx.fillStyle = "#020308";
    ctx.fillRect(0, 0, w, h);
    
    // Draw background Moyal symplectic curl ripple
    let waveT = time * 0.0008;
    ctx.save();
    ctx.strokeStyle = "rgba(0, 245, 235, 0.035)";
    ctx.lineWidth = 1;
    for (let r = 80; r < Math.max(w, h) * 0.8; r += 50) {
      ctx.beginPath();
      let steps = 48;
      for (let s = 0; s <= steps; s++) {
        let th = (s / steps) * Math.PI * 2.0;
        let warp = thetaRatio * 12.0 * Math.sin(6.0 * th + waveT) * Math.cos(4.0 * th - waveT);
        let px = cx + (r + warp) * Math.cos(th);
        let py = cy + (r + warp) * Math.sin(th);
        if (s === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
    }
    ctx.restore();
    
    const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
    const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
    
    // Transform cells
    let projectedCells = [];
    for (let i = 0; i < cells.length; i++) {
      let c = cells[i];
      
      // Yaw (Y)
      let x1 = c.x * cosY + c.z * sinY;
      let y1 = c.y;
      let z1 = -c.x * sinY + c.z * cosY;
      
      // Pitch (X)
      let x2 = x1;
      let y2 = y1 * cosX - z1 * sinX;
      let z2 = y1 * sinX + z1 * cosX;
      
      let fov = 850.0;
      let dist = fov / (fov + z2);
      let px = cx + x2 * dist;
      let py = cy - y2 * dist;
      
      projectedCells.push({
        id: i,
        px: px,
        py: py,
        z: z2,
        dist: dist,
        tier: c.tier,
        shellIdx: c.shellIdx
      });
    }
    
    // Draw commutator links
    ctx.lineWidth = 1.0;
    for (let l = 0; l < links.length; l++) {
      let c1 = projectedCells[links[l].from];
      let c2 = projectedCells[links[l].to];
      
      let avgZ = (c1.z + c2.z) * 0.5;
      let alpha = Math.max(0.04, Math.min(0.40, (avgZ + 350.0) / 700.0));
      
      if (links[l].tier === "UV") {
        ctx.strokeStyle = `rgba(0, 245, 235, ${alpha * 0.6})`;
      } else if (links[l].tier === "MID") {
        ctx.strokeStyle = `rgba(195, 115, 255, ${alpha * 0.7})`;
      } else {
        ctx.strokeStyle = `rgba(255, 195, 45, ${alpha * 0.8})`;
      }
      
      ctx.beginPath();
      ctx.moveTo(c1.px, c1.py);
      ctx.lineTo(c2.px, c2.py);
      ctx.stroke();
    }
    
    // Sort cells back to front
    projectedCells.sort((a, b) => a.z - b.z);
    
    // Draw cells
    for (let i = 0; i < projectedCells.length; i++) {
      let p = projectedCells[i];
      let light = Math.max(0.15, Math.min(1.0, (p.z + 300.0) / 600.0));
      
      let r = 2.4 * p.dist;
      let color;
      if (p.tier === "UV") {
        r = 2.0 * p.dist;
        color = `rgba(0, 245, 235, ${light * 0.85})`;
      } else if (p.tier === "MID") {
        r = 2.8 * p.dist;
        color = `rgba(195, 115, 255, ${light * 0.90})`;
      } else {
        r = 3.8 * p.dist;
        color = `rgba(255, 195, 45, ${light * 0.95})`;
      }
      
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(p.px, p.py, Math.max(1.0, r), 0, Math.PI * 2);
      ctx.fill();
    }
    
    requestAnimationFrame(render);
  }

  // Initialization
  resizeCanvas();
  generateFuzzyManifold();
  requestAnimationFrame(render);
})();

