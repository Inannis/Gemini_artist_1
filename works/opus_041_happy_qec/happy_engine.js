/**
 * Chamber 21 Engine: The Holographic Code & The Entanglement Wedge
 * Real-time Poincaré Hyperbolic Tiling & WebAudio QEC Synthesizer
 */

const canvas = document.getElementById("happyCanvas");
const ctx = canvas.getContext("2d");

// DOM Elements
const rngSpan = document.getElementById("rngSpan");
const rngErasure = document.getElementById("rngErasure");
const lblSpan = document.getElementById("lblSpan");
const lblErasure = document.getElementById("lblErasure");
const lblAudio = document.getElementById("lblAudio");
const btnAudioToggle = document.getElementById("btnAudioToggle");
const btnReset = document.getElementById("btnReset");

const hudRtLen = document.getElementById("hudRtLen");
const hudStatusBadge = document.getElementById("hudStatusBadge");
const telApex = document.getElementById("telApex");
const telEntropy = document.getElementById("telEntropy");
const telFidelity = document.getElementById("telFidelity");
const telState = document.getElementById("telState");

let width = 0;
let height = 0;
let cx = 0;
let cy = 0;
let rDisk = 0;

let spanDeg = 261.0; // Subregion A angular span
let erasureFrac = 0.275;
let isAudioActive = false;
let audioCtx = null;
let masterGain = null;
let oscs = [];
let noiseNode = null;
let noiseGain = null;

// Telemetry state
let rApex = 0.214;
let rtLength = 4.12;
let entropy = 1.03;
let fidelity = 0.984;
let isProtected = true;

function resize() {
  const rect = canvas.parentElement.getBoundingClientRect();
  width = rect.width;
  height = rect.height;
  canvas.width = width * window.devicePixelRatio;
  canvas.height = height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  cx = width * 0.5;
  cy = height * 0.5;
  rDisk = Math.min(width, height) * 0.42;
}

window.addEventListener("resize", resize);
resize();

function updateStateFromSpan(newSpan) {
  spanDeg = parseFloat(newSpan);
  erasureFrac = Math.max(0.01, Math.min(0.99, (360.0 - spanDeg) / 360.0));
  rngSpan.value = spanDeg;
  rngErasure.value = erasureFrac.toFixed(3);
  recomputeQEC();
}

function updateStateFromErasure(newErasure) {
  erasureFrac = parseFloat(newErasure);
  spanDeg = Math.max(30.0, Math.min(355.0, 360.0 * (1.0 - erasureFrac)));
  rngErasure.value = erasureFrac;
  rngSpan.value = Math.round(spanDeg);
  recomputeQEC();
}

function recomputeQEC() {
  const fAccessible = 1.0 - erasureFrac;
  const fCrit = 0.50;
  isProtected = erasureFrac < fCrit;

  // Hyperbolic RT Apex radius
  const deltaTheta = (spanDeg * Math.PI) / 180.0;
  const halfAng = deltaTheta * 0.5;
  if (halfAng < Math.PI) {
    rApex = Math.tan((Math.PI - halfAng) * 0.5);
    rApex = Math.max(0.0, Math.min(0.99, rApex));
  } else {
    rApex = 0.0;
  }

  rtLength = 2.0 * Math.log(Math.max(1.001, 2.0 / (1.0 - rApex * rApex + 1e-5)));
  entropy = rtLength * 0.25;

  if (isProtected) {
    fidelity = Math.max(0.0, Math.min(1.0, 1.0 - Math.pow(erasureFrac / fCrit, 2)));
  } else {
    fidelity = 0.0;
  }

  // Update UI labels
  lblSpan.textContent = `${Math.round(spanDeg)}° (${(fAccessible * 100).toFixed(1)}%)`;
  lblErasure.textContent = `${erasureFrac.toFixed(3)} (f_crit = 0.500)`;

  hudRtLen.textContent = `γ_A (L = ${rtLength.toFixed(2)})`;
  telApex.textContent = rApex.toFixed(3);
  telEntropy.textContent = `${entropy.toFixed(2)} nats`;
  telFidelity.textContent = `${(fidelity * 100).toFixed(1)}%`;

  if (isProtected) {
    hudStatusBadge.className = "hud-status status-protected";
    hudStatusBadge.textContent = "PROTECTED (Core In Wedge)";
    telState.textContent = "RECONSTRUCTIBLE";
    telState.style.color = "var(--emerald)";
  } else {
    hudStatusBadge.className = "hud-status status-decohered";
    hudStatusBadge.textContent = "DECOHERED / WEDGE RETRACTED";
    telState.textContent = "PHASE COLLAPSE";
    telState.style.color = "var(--red)";
  }

  updateAudioParameters();
}

rngSpan.addEventListener("input", (e) => updateStateFromSpan(e.target.value));
rngErasure.addEventListener("input", (e) => updateStateFromErasure(e.target.value));

btnReset.addEventListener("click", () => {
  updateStateFromSpan(261.0);
});

// WebAudio Setup
function initAudio() {
  if (audioCtx) return;
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  audioCtx = new AudioContextClass();

  masterGain = audioCtx.createGain();
  masterGain.gain.setValueAtTime(0.25, audioCtx.currentTime);
  masterGain.connect(audioCtx.destination);

  // 5 Golden-ratio syndrome oscillators
  const phi = (1.0 + Math.sqrt(5.0)) / 2.0;
  const fFund = 48.0;
  const freqs = [0, 1, 2, 3, 4].map(k => fFund * Math.pow(phi, k));

  freqs.forEach((freq, idx) => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = idx === 2 ? "sine" : (idx % 2 === 0 ? "sine" : "triangle");
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

    const baseGain = idx === 2 ? 0.35 : 0.15;
    gain.gain.setValueAtTime(baseGain, audioCtx.currentTime);

    osc.connect(gain);
    gain.connect(masterGain);
    osc.start();

    oscs.push({ osc, gain, baseFreq: freq, baseGain });
  });

  // Noise generator for erasure
  const bufferSize = audioCtx.sampleRate * 2;
  const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const output = noiseBuffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    output[i] = Math.random() * 2 - 1;
  }

  const whiteNoise = audioCtx.createBufferSource();
  whiteNoise.buffer = noiseBuffer;
  whiteNoise.loop = true;

  noiseGain = audioCtx.createGain();
  noiseGain.gain.setValueAtTime(0.0, audioCtx.currentTime);

  whiteNoise.connect(noiseGain);
  noiseGain.connect(masterGain);
  whiteNoise.start();

  updateAudioParameters();
}

function updateAudioParameters() {
  if (!audioCtx) return;
  const now = audioCtx.currentTime;

  if (isProtected) {
    // Coherent tuning
    oscs.forEach((item, idx) => {
      item.osc.frequency.setTargetAtTime(item.baseFreq, now, 0.05);
      item.gain.gain.setTargetAtTime(item.baseGain * fidelity, now, 0.05);
    });
    noiseGain.gain.setTargetAtTime(0.01 * erasureFrac, now, 0.05);
  } else {
    // Dissonant collapse
    oscs.forEach((item, idx) => {
      const detuneFactor = 1.0 + (Math.random() - 0.5) * 0.15;
      item.osc.frequency.setTargetAtTime(item.baseFreq * detuneFactor, now, 0.05);
      item.gain.gain.setTargetAtTime(item.baseGain * 0.3, now, 0.05);
    });
    noiseGain.gain.setTargetAtTime(0.18, now, 0.05);
  }
}

btnAudioToggle.addEventListener("click", () => {
  if (!audioCtx) {
    initAudio();
  }
  if (audioCtx.state === "suspended") {
    audioCtx.resume();
  }
  isAudioActive = !isAudioActive;
  if (isAudioActive) {
    masterGain.gain.setTargetAtTime(0.28, audioCtx.currentTime, 0.08);
    btnAudioToggle.textContent = "Mute Chamber";
    btnAudioToggle.classList.add("active");
    lblAudio.textContent = "Active (48kHz Golden Resonator)";
  } else {
    masterGain.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.08);
    btnAudioToggle.textContent = "Activate Audio";
    btnAudioToggle.classList.remove("active");
    lblAudio.textContent = "Muted";
  }
});

// Render Animation Loop
let animTime = 0.0;

function draw() {
  animTime += 0.016;
  ctx.clearRect(0, 0, width, height);

  // Background deep gradient
  const bgGrad = ctx.createRadialGradient(cx, cy, 10, cx, cy, rDisk * 1.5);
  bgGrad.addColorStop(0, "#080e1b");
  bgGrad.addColorStop(0.7, "#04070e");
  bgGrad.addColorStop(1, "#020306");
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, width, height);

  const wedgeHalf = (spanDeg * Math.PI) / 360.0;

  // In Poincaré disk, compute orthogonal circle for RT geodesic
  const cosW = Math.cos(wedgeHalf);
  let rtCenterX = 0;
  let rtRadius = 0;
  let hasOrthogonalCircle = false;

  if (Math.abs(cosW) > 0.01) {
    const xCNorm = 1.0 / cosW;
    if (xCNorm * xCNorm > 1.0) {
      const rCNorm = Math.sqrt(xCNorm * xCNorm - 1.0);
      rtCenterX = cx + xCNorm * rDisk;
      rtRadius = rCNorm * rDisk;
      hasOrthogonalCircle = true;
    }
  }

  // Draw Bulk Poincaré Disk
  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, rDisk, 0, Math.PI * 2);
  ctx.clip();

  // Draw Entanglement Wedge / Complementary domain
  if (hasOrthogonalCircle) {
    // Fill complementary wedge B
    ctx.fillStyle = "rgba(180, 45, 55, 0.12)";
    ctx.fillRect(cx - rDisk, cy - rDisk, rDisk * 2, rDisk * 2);

    // Fill Entanglement Wedge A
    ctx.save();
    ctx.beginPath();
    ctx.arc(rtCenterX, cy, rtRadius, 0, Math.PI * 2);
    ctx.rect(cx + rDisk * 1.5, cy - rDisk * 1.5, -rDisk * 3, rDisk * 3);
    ctx.clip("evenodd");

    const wedgeGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, rDisk);
    wedgeGrad.addColorStop(0, "rgba(56, 215, 208, 0.22)");
    wedgeGrad.addColorStop(0.8, "rgba(20, 80, 140, 0.18)");
    wedgeGrad.addColorStop(1, "rgba(10, 30, 60, 0.10)");
    ctx.fillStyle = wedgeGrad;
    ctx.fillRect(cx - rDisk, cy - rDisk, rDisk * 2, rDisk * 2);
    ctx.restore();
  }

  // Draw Concentric Hyperbolic Rings
  for (let k = 1; k <= 5; k++) {
    const rRing = rDisk * Math.tanh(k * 0.45);
    ctx.beginPath();
    ctx.arc(cx, cy, rRing, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Draw Ryu-Takayanagi Minimal Geodesic Surface γ_A
  if (hasOrthogonalCircle) {
    ctx.beginPath();
    ctx.arc(rtCenterX, cy, rtRadius, 0, Math.PI * 2);
    ctx.strokeStyle = isProtected ? "rgba(255, 220, 120, 0.95)" : "rgba(239, 68, 68, 0.9)";
    ctx.lineWidth = 2.5;
    ctx.shadowColor = isProtected ? "#d4af37" : "#ef4444";
    ctx.shadowBlur = 12;
    ctx.stroke();
    ctx.shadowBlur = 0;
  }

  // Draw {5, 4} Pentagonal Tensor Network Bonds
  const t1Nodes = [];
  const r1 = rDisk * 0.46;
  for (let k = 0; k < 5; k++) {
    const ang = (Math.PI * 2 * k) / 5.0 - Math.PI / 10.0 + Math.sin(animTime * 0.2) * 0.02;
    const px = cx + r1 * Math.cos(ang);
    const py = cy + r1 * Math.sin(ang);
    const inWedge = hasOrthogonalCircle ? Math.hypot(px - rtCenterX, py - cy) >= rtRadius : true;
    t1Nodes.push({ x: px, y: py, ang, inWedge });

    // Center to T1 leg
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(px, py);
    ctx.strokeStyle = inWedge ? "rgba(255, 215, 80, 0.8)" : "rgba(180, 70, 70, 0.4)";
    ctx.lineWidth = 2.2;
    ctx.stroke();
  }

  // T1 pentagon edges
  for (let k = 0; k < 5; k++) {
    const n1 = t1Nodes[k];
    const n2 = t1Nodes[(k + 1) % 5];
    ctx.beginPath();
    ctx.moveTo(n1.x, n1.y);
    ctx.lineTo(n2.x, n2.y);
    ctx.strokeStyle = (n1.inWedge && n2.inWedge) ? "rgba(240, 205, 100, 0.6)" : "rgba(140, 60, 60, 0.3)";
    ctx.lineWidth = 1.6;
    ctx.stroke();
  }

  // Tier 2 nodes & outer boundary legs
  const r2 = rDisk * 0.78;
  for (let k = 0; k < 20; k++) {
    const ang = (Math.PI * 2 * k) / 20.0 - Math.PI / 20.0;
    const px = cx + r2 * Math.cos(ang);
    const py = cy + r2 * Math.sin(ang);
    const inWedge = hasOrthogonalCircle ? Math.hypot(px - rtCenterX, py - cy) >= rtRadius : true;

    // Connect to nearest T1
    let closestT1 = t1Nodes[0];
    let minDist = 1e9;
    t1Nodes.forEach(n => {
      const d = Math.hypot(n.x - px, n.y - py);
      if (d < minDist) { minDist = d; closestT1 = n; }
    });

    ctx.beginPath();
    ctx.moveTo(closestT1.x, closestT1.y);
    ctx.lineTo(px, py);
    ctx.strokeStyle = (inWedge && closestT1.inWedge) ? "rgba(56, 215, 208, 0.5)" : "rgba(120, 50, 60, 0.25)";
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // Boundary leg
    const bx = cx + rDisk * Math.cos(ang);
    const by = cy + rDisk * Math.sin(ang);
    ctx.beginPath();
    ctx.moveTo(px, py);
    ctx.lineTo(bx, by);
    ctx.strokeStyle = inWedge ? "rgba(56, 215, 208, 0.4)" : "rgba(235, 55, 65, 0.3)";
    ctx.lineWidth = 1.0;
    ctx.stroke();

    // T2 node hub
    ctx.beginPath();
    ctx.arc(px, py, 3.5, 0, Math.PI * 2);
    ctx.fillStyle = inWedge ? "#38d7d0" : "#991b1b";
    ctx.fill();
  }

  // T1 node hubs
  t1Nodes.forEach(n => {
    ctx.beginPath();
    ctx.arc(n.x, n.y, 6.0, 0, Math.PI * 2);
    ctx.fillStyle = n.inWedge ? "#f59e0b" : "#dc2626";
    ctx.fill();
  });

  // Central Logical Qubit Hub
  const pulse = Math.sin(animTime * 3.0) * 2.0;
  ctx.beginPath();
  ctx.arc(cx, cy, 14.0 + pulse, 0, Math.PI * 2);
  const coreGrad = ctx.createRadialGradient(cx, cy, 2, cx, cy, 14.0 + pulse);
  if (isProtected) {
    coreGrad.addColorStop(0, "#ffffff");
    coreGrad.addColorStop(0.5, "#fbbf24");
    coreGrad.addColorStop(1, "#d97706");
  } else {
    coreGrad.addColorStop(0, "#fca5a5");
    coreGrad.addColorStop(0.6, "#ef4444");
    coreGrad.addColorStop(1, "#7f1d1d");
  }
  ctx.fillStyle = coreGrad;
  ctx.shadowColor = isProtected ? "#d4af37" : "#ef4444";
  ctx.shadowBlur = isProtected ? 20 : 10;
  ctx.fill();
  ctx.shadowBlur = 0;

  ctx.restore(); // Restore bulk clip

  // Draw Conformal Boundary Rings (Region A vs Region B)
  ctx.lineWidth = 5.0;

  // Region A: Cyan Arc
  ctx.beginPath();
  ctx.arc(cx, cy, rDisk, -wedgeHalf, wedgeHalf, false);
  ctx.strokeStyle = "#38d7d0";
  ctx.shadowColor = "#38d7d0";
  ctx.shadowBlur = 10;
  ctx.stroke();

  // Region B: Erased Red Arc
  ctx.beginPath();
  ctx.arc(cx, cy, rDisk, wedgeHalf, -wedgeHalf, false);
  ctx.strokeStyle = "#ef4444";
  ctx.shadowColor = "#ef4444";
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.shadowBlur = 0;

  requestAnimationFrame(draw);
}

// Initial telemetry compute and animation start
recomputeQEC();
requestAnimationFrame(draw);
