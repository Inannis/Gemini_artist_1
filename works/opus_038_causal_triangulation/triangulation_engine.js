/**
 * STUDIO ANAMNESIS · CHAMBER 18: THE SIMPLICIAL FOLIATION
 * Interactive 3D Causal Dynamical Triangulation & Spectral Dimension Engine
 * Zero external dependencies (Vanilla Canvas + Web Audio API).
 */

const canvas = document.getElementById("triangulation-canvas");
const ctx = canvas.getContext("2d");

let width, height;
let rotX = 0.35, rotY = -0.55;
let isDragging = false;
let lastMouseX = 0, lastMouseY = 0;
let zoom = 1.0;

// State parameters
let activeSlice = 16;
let asymmetryAlpha = 0.60;
let couplingKappa0 = 2.20;
let diffusionSteps = 40;
let isPlayingAudio = false;

// Geometry cache
const NUM_SLICES = 32;
let slicesVertices = [];

function resize() {
  const container = document.getElementById("viewport-container");
  width = canvas.width = container.clientWidth;
  height = canvas.height = container.clientHeight;
}

function initGeometry() {
  slicesVertices = [];
  const isPolymer = couplingKappa0 < 1.2;

  for (let s = 0; s < NUM_SLICES; s++) {
    const t_norm = (s - 15.5) / 15.5; // -1 to +1
    let spatialRadius;

    if (isPolymer) {
      // Branched polymer collapse: narrow fluctuating neck
      spatialRadius = 30 + 40 * Math.abs(Math.sin(s * 1.7));
    } else {
      // Extended de Sitter phase: V_3 ~ cos^3(t)
      const cosVal = Math.max(0.1, Math.cos(t_norm * Math.PI * 0.48));
      spatialRadius = 35 + 240 * Math.pow(cosVal, 1.5) * (0.8 + 0.4 * asymmetryAlpha);
    }

    const n_verts = Math.max(6, Math.floor(spatialRadius / 10));
    const slicePts = [];
    const y_pos = (s - 15.5) * 22; // vertical time coordinate

    for (let v = 0; v < n_verts; v++) {
      const angle = (v / n_verts) * Math.PI * 2;
      const r_jitter = spatialRadius * (0.9 + 0.2 * Math.sin(v * 3 + s * 2));
      const x = Math.cos(angle) * r_jitter;
      const z = Math.sin(angle) * r_jitter;
      slicePts.push({ x, y: y_pos, z, slice: s });
    }
    slicesVertices.push(slicePts);
  }
}

function project(p) {
  // 3D Rotation around Y then X
  const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
  const x1 = p.x * cosY + p.z * sinY;
  const z1 = -p.x * sinY + p.z * cosY;

  const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
  const y2 = p.y * cosX - z1 * sinX;
  const z2 = p.y * sinX + z1 * cosX;

  const cameraDist = 800;
  const scale = (cameraDist / (cameraDist + z2)) * zoom;
  return {
    x: width / 2 + x1 * scale,
    y: height / 2 + y2 * scale,
    scale: scale,
    z: z2
  };
}

function draw() {
  ctx.fillStyle = "#03040a";
  ctx.fillRect(0, 0, width, height);

  // Background cosmological radial glow
  const grad = ctx.createRadialGradient(width/2, height/2, 20, width/2, height/2, width*0.7);
  grad.addColorStop(0, "rgba(8, 20, 42, 0.4)");
  grad.addColorStop(1, "rgba(2, 3, 8, 0.0)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);

  // Draw time-like links (amber / gold)
  ctx.lineWidth = 1;
  for (let s = 0; s < NUM_SLICES - 1; s++) {
    const pts1 = slicesVertices[s];
    const pts2 = slicesVertices[s+1];
    const isSliceActive = (s === activeSlice || s + 1 === activeSlice);

    ctx.strokeStyle = isSliceActive ? "rgba(245, 158, 11, 0.85)" : "rgba(245, 158, 11, 0.25)";
    for (let i = 0; i < pts1.length; i++) {
      const p1Proj = project(pts1[i]);
      // Connect to adjacent vertices in next slice
      const targetIdx = Math.floor((i / pts1.length) * pts2.length);
      for (let offset = -1; offset <= 1; offset++) {
        const j = (targetIdx + offset + pts2.length) % pts2.length;
        const p2Proj = project(pts2[j]);
        ctx.beginPath();
        ctx.moveTo(p1Proj.x, p1Proj.y);
        ctx.lineTo(p2Proj.x, p2Proj.y);
        ctx.stroke();
      }
    }
  }

  // Draw space-like links within each slice (cyan / ice)
  for (let s = 0; s < NUM_SLICES; s++) {
    const pts = slicesVertices[s];
    const isSliceActive = (s === activeSlice);
    ctx.strokeStyle = isSliceActive ? "rgba(56, 189, 248, 0.95)" : "rgba(56, 189, 248, 0.40)";
    ctx.lineWidth = isSliceActive ? 2 : 1;

    for (let i = 0; i < pts.length; i++) {
      const p1 = project(pts[i]);
      const p2 = project(pts[(i + 1) % pts.length]);
      ctx.beginPath();
      ctx.moveTo(p1.x, p1.y);
      ctx.lineTo(p2.x, p2.y);
      ctx.stroke();
    }
  }

  // Draw vertices (glowing nodes)
  for (let s = 0; s < NUM_SLICES; s++) {
    const pts = slicesVertices[s];
    const isSliceActive = (s === activeSlice);

    for (let i = 0; i < pts.length; i++) {
      const proj = project(pts[i]);
      const r = Math.max(1.5, (isSliceActive ? 4 : 2.5) * proj.scale);

      ctx.fillStyle = isSliceActive ? "#f59e0b" : "#38bdf8";
      ctx.beginPath();
      ctx.arc(proj.x, proj.y, r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Telemetry HUD overlay
  ctx.fillStyle = "rgba(148, 163, 184, 0.7)";
  ctx.font = "11px 'SF Mono', monospace";
  ctx.fillText(`CAUCHY FOLIATION · t = ${activeSlice} / 31`, 24, 30);
  ctx.fillText(`LORENTZIAN SIGNATURE · α = ${asymmetryAlpha.toFixed(2)}`, 24, 48);

  requestAnimationFrame(draw);
}

// User Controls
function updateSlice(val) {
  activeSlice = parseInt(val);
  document.getElementById("val-slice").innerText = `${activeSlice} / 31`;
  updateTelemetry();
}

function updateAsymmetry(val) {
  asymmetryAlpha = parseFloat(val);
  document.getElementById("val-asymmetry").innerText = asymmetryAlpha.toFixed(2);
  initGeometry();
  updateTelemetry();
}

function updateCoupling(val) {
  couplingKappa0 = parseFloat(val);
  const desc = couplingKappa0 < 1.2 ? `${couplingKappa0.toFixed(2)} (Branched Polymer!)` : `${couplingKappa0.toFixed(2)} (de Sitter Phase)`;
  document.getElementById("val-coupling").innerText = desc;
  initGeometry();
  updateTelemetry();
}

function updateDiffusion(val) {
  diffusionSteps = parseInt(val);
  document.getElementById("val-diffusion").innerText = `${diffusionSteps} steps`;
  updateTelemetry();
}

function updateTelemetry() {
  // Running spectral dimension formula: d_s = 4.02 - 2.22 / (1 + (sigma/40)^1.25)
  const crossover = 1.0 / (1.0 + Math.pow(diffusionSteps / 40.0, 1.25));
  const d_s = 4.02 - 2.22 * crossover;
  document.getElementById("telem-ds").innerText = d_s.toFixed(2);

  let regime = "Planckian 2D Sheet";
  let col = "var(--accent-cyan)";
  if (d_s > 3.6) {
    regime = "Classical 4D de Sitter";
    col = "var(--accent-emerald)";
  } else if (d_s > 2.2) {
    regime = "Dimensional Crossover";
    col = "var(--accent-gold)";
  }
  const regimeEl = document.getElementById("telem-regime");
  regimeEl.innerText = regime;
  regimeEl.style.color = col;

  // Spatial volume
  const t_norm = (activeSlice - 15.5) / 15.5;
  const isPolymer = couplingKappa0 < 1.2;
  const vol = isPolymer ? Math.floor(120 + 80 * Math.random()) : Math.floor(5000 * Math.pow(Math.max(0.05, Math.cos(t_norm * Math.PI * 0.48)), 3));
  document.getElementById("telem-vol").innerText = `${vol.toLocaleString()} simplices`;

  if (filterNode) {
    // Dynamically adjust audio filter based on spectral dimension
    filterNode.frequency.setTargetAtTime(80 + (d_s - 1.8) * 800, audioCtx.currentTime, 0.1);
  }
}

// Mouse Drag Orbit
window.addEventListener("mousedown", (e) => {
  if (e.target === canvas) {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  }
});

window.addEventListener("mousemove", (e) => {
  if (isDragging) {
    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;
    rotY += dx * 0.008;
    rotX = Math.max(-Math.PI/2.2, Math.min(Math.PI/2.2, rotX + dy * 0.008));
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  }
});

window.addEventListener("mouseup", () => { isDragging = false; });
window.addEventListener("wheel", (e) => {
  if (e.target === canvas) {
    zoom = Math.max(0.5, Math.min(2.5, zoom - e.deltaY * 0.001));
    e.preventDefault();
  }
}, { passive: false });

window.addEventListener("resize", () => {
  resize();
  initGeometry();
});

// Web Audio API Synthesizer
let audioCtx = null;
let masterGain = null;
let filterNode = null;
let oscCauchy = null;
let oscHingePos = null;
let oscHingeNeg = null;
let tickTimer = null;

function toggleSimplicialAudio() {
  const btn = document.getElementById("audio-toggle-btn");
  if (!isPlayingAudio) {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
    }

    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.0, audioCtx.currentTime);
    masterGain.gain.linearRampToValueAtTime(0.35, audioCtx.currentTime + 1.5);

    filterNode = audioCtx.createBiquadFilter();
    filterNode.type = "lowpass";
    filterNode.frequency.setValueAtTime(450, audioCtx.currentTime);

    // Cauchy fundamental (36 Hz)
    oscCauchy = audioCtx.createOscillator();
    oscCauchy.type = "sine";
    oscCauchy.frequency.setValueAtTime(36.0, audioCtx.currentTime);

    // Deficit angle modes
    oscHingePos = audioCtx.createOscillator();
    oscHingePos.type = "triangle";
    oscHingePos.frequency.setValueAtTime(165.6, audioCtx.currentTime);

    oscHingeNeg = audioCtx.createOscillator();
    oscHingeNeg.type = "triangle";
    oscHingeNeg.frequency.setValueAtTime(122.4, audioCtx.currentTime);

    const posGain = audioCtx.createGain();
    posGain.gain.value = 0.15;
    const negGain = audioCtx.createGain();
    negGain.gain.value = 0.15;

    oscCauchy.connect(filterNode);
    oscHingePos.connect(posGain).connect(filterNode);
    oscHingeNeg.connect(negGain).connect(filterNode);
    filterNode.connect(masterGain).connect(audioCtx.destination);

    oscCauchy.start();
    oscHingePos.start();
    oscHingeNeg.start();

    // 1 Hz Cauchy Tick Pulse
    tickTimer = setInterval(() => {
      if (audioCtx && isPlayingAudio) {
        const tickOsc = audioCtx.createOscillator();
        const tickGain = audioCtx.createGain();
        tickOsc.frequency.setValueAtTime(72.0, audioCtx.currentTime);
        tickGain.gain.setValueAtTime(0.18, audioCtx.currentTime);
        tickGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.08);
        tickOsc.connect(tickGain).connect(audioCtx.destination);
        tickOsc.start();
        tickOsc.stop(audioCtx.currentTime + 0.09);
      }
    }, 1000);

    isPlayingAudio = true;
    btn.innerText = "Halt Acoustic Engine";
    btn.classList.add("active");
  } else {
    if (masterGain && audioCtx) {
      masterGain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
      setTimeout(() => {
        if (oscCauchy) oscCauchy.stop();
        if (oscHingePos) oscHingePos.stop();
        if (oscHingeNeg) oscHingeNeg.stop();
        if (tickTimer) clearInterval(tickTimer);
      }, 600);
    }
    isPlayingAudio = false;
    btn.innerText = "Start Acoustic Engine";
    btn.classList.remove("active");
  }
}

// Initial boot
resize();
initGeometry();
updateTelemetry();
draw();

