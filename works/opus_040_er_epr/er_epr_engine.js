/**
 * Chamber 20: ER = EPR & Traversable Wormhole Simulation Engine
 * Studio Anamnesis · Series XXXVIII · Cornerstone #18
 */

const canvas = document.getElementById("glcanvas");
const ctx = canvas.getContext("2d");

let width = canvas.width = canvas.parentElement.clientWidth;
let height = canvas.height = canvas.parentElement.clientHeight;

window.addEventListener("resize", () => {
  width = canvas.width = canvas.parentElement.clientWidth;
  height = canvas.height = canvas.parentElement.clientHeight;
});

// State parameters
let couplingH = 0.45;
let beta = 5.03;
let deltaV = -0.18;
let isTraversable = true;
let pulseActive = 0.0;
let qubitActive = false;
let qubitPos = -1.2;
let qubitState = "idle"; // "idle", "transiting", "emerged", "crushed"
let time = 0;

// Mouse rotation
let rotX = 0.2;
let rotY = 0.0;
let isDragging = false;
let lastMouseX = 0;
let lastMouseY = 0;

canvas.addEventListener("mousedown", (e) => {
  isDragging = true;
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
});
window.addEventListener("mousemove", (e) => {
  if (!isDragging) return;
  const dx = e.clientX - lastMouseX;
  const dy = e.clientY - lastMouseY;
  rotY += dx * 0.005;
  rotX += dy * 0.005;
  rotX = Math.max(-1.0, Math.min(1.0, rotX));
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
});
window.addEventListener("mouseup", () => { isDragging = false; });

// WebAudio Substrate
let audioCtx = null;
let oscLeft = null;
let oscRight = null;
let gainLeft = null;
let gainRight = null;
let masterGain = null;

function initAudio() {
  if (audioCtx) return;
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  
  masterGain = audioCtx.createGain();
  masterGain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  masterGain.connect(audioCtx.destination);
  
  const merger = audioCtx.createChannelMerger(2);
  merger.connect(masterGain);
  
  // Left CFT Carrier
  oscLeft = audioCtx.createOscillator();
  oscLeft.type = "sine";
  oscLeft.frequency.setValueAtTime(96.42, audioCtx.currentTime);
  gainLeft = audioCtx.createGain();
  gainLeft.gain.setValueAtTime(0.5, audioCtx.currentTime);
  oscLeft.connect(gainLeft);
  gainLeft.connect(merger, 0, 0); // Left channel
  oscLeft.start();
  
  // Right CFT Carrier
  oscRight = audioCtx.createOscillator();
  oscRight.type = "sine";
  oscRight.frequency.setValueAtTime(96.42, audioCtx.currentTime);
  gainRight = audioCtx.createGain();
  gainRight.gain.setValueAtTime(0.5, audioCtx.currentTime);
  oscRight.connect(gainRight);
  gainRight.connect(merger, 0, 1); // Right channel
  oscRight.start();
  
  document.getElementById("btn-toggle-audio").innerText = "WebAudio Engine Active";
  document.getElementById("btn-toggle-audio").style.borderColor = "var(--cyan)";
  document.getElementById("btn-toggle-audio").style.color = "var(--cyan)";
}

function playTransitChime(success) {
  if (!audioCtx) return;
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const g = audioCtx.createGain();
  osc.connect(g);
  g.connect(masterGain);
  
  if (success) {
    // Ethereal teleportation chime
    osc.type = "sine";
    osc.frequency.setValueAtTime(771.36, now);
    osc.frequency.exponentialRampToValueAtTime(1157.04, now + 0.4);
    g.gain.setValueAtTime(0.4, now);
    g.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
    osc.start(now);
    osc.stop(now + 1.2);
  } else {
    // Singularity crush distorted burst
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(140.0, now);
    osc.frequency.linearRampToValueAtTime(30.0, now + 0.5);
    g.gain.setValueAtTime(0.6, now);
    g.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
    osc.start(now);
    osc.stop(now + 0.5);
  }
}

// UI Handlers
const sliderCoupling = document.getElementById("slider-coupling");
const sliderBeta = document.getElementById("slider-beta");
const valCoupling = document.getElementById("val-coupling");
const valBeta = document.getElementById("val-beta");
const hudCoupling = document.getElementById("hud-coupling");
const hudShift = document.getElementById("hud-shift");
const hudStatus = document.getElementById("hud-status");

function updatePhysics() {
  couplingH = parseFloat(sliderCoupling.value);
  beta = parseFloat(sliderBeta.value);
  valCoupling.innerText = couplingH.toFixed(2);
  valBeta.innerText = beta.toFixed(2) + " s";
  
  // Delta V = - (h * G / r_+) * exp(2 pi (t0 - t*) / beta)
  deltaV = - couplingH * 0.4;
  isTraversable = (deltaV < 0);
  
  hudCoupling.innerText = `h = ${couplingH.toFixed(2)}`;
  hudShift.innerText = `ΔV = ${deltaV.toFixed(2)}`;
  
  if (isTraversable) {
    hudStatus.className = "hud-status status-open";
    hudStatus.innerText = "TRAVERSABLE (OPEN)";
  } else {
    hudStatus.className = "hud-status status-closed";
    hudStatus.innerText = "CHOKED (SINGULARITY CRUSH)";
  }
}

sliderCoupling.addEventListener("input", updatePhysics);
sliderBeta.addEventListener("input", updatePhysics);

document.getElementById("btn-fire-qubit").addEventListener("click", () => {
  qubitActive = true;
  qubitPos = -1.2;
  qubitState = "transiting";
  document.getElementById("telem-transit").innerText = "Transiting Left Horizon...";
  document.getElementById("telem-transit").style.color = "var(--cyan)";
});

document.getElementById("btn-trigger-pulse").addEventListener("click", () => {
  pulseActive = 1.0;
  couplingH = 0.65;
  sliderCoupling.value = 0.65;
  updatePhysics();
});

document.getElementById("btn-toggle-audio").addEventListener("click", initAudio);

// Animation Loop
function render() {
  time += 0.02;
  if (pulseActive > 0.0) pulseActive = Math.max(0.0, pulseActive - 0.02);
  
  ctx.fillStyle = "#030509";
  ctx.fillRect(0, 0, width, height);
  
  const cx = width * 0.5;
  const cy = height * 0.5;
  const scale = Math.min(width, height) * 0.35;
  
  // 3D Perspective Projection
  function project(x, y, z) {
    // Rotate around Y
    const x1 = x * Math.cos(rotY) + z * Math.sin(rotY);
    const z1 = -x * Math.sin(rotY) + z * Math.cos(rotY);
    // Rotate around X
    const y2 = y * Math.cos(rotX) - z1 * Math.sin(rotX);
    const z2 = y * Math.sin(rotX) + z1 * Math.cos(rotX);
    
    const fov = 3.5;
    const distance = 4.0;
    const pz = distance + z2;
    const px = cx + (x1 / pz) * scale * fov;
    const py = cy + (y2 / pz) * scale * fov;
    return { px, py, pz };
  }
  
  // Draw Hyperbolic Throat Rings
  const numRings = 36;
  for (let i = 0; i <= numRings; i++) {
    const t_z = (i / numRings) * 2.4 - 1.2; // z in [-1.2, 1.2]
    // Throat neck radius affected by coupling
    const throatConstriction = isTraversable ? 0.45 : (0.45 - couplingH * 0.3);
    const r_throat = Math.sqrt(Math.max(0.04, throatConstriction + 0.5 * (t_z ** 2)));
    
    ctx.beginPath();
    const ringSegments = 40;
    for (let j = 0; j <= ringSegments; j++) {
      const theta = (j / ringSegments) * Math.PI * 2;
      const x = t_z;
      const y = r_throat * Math.cos(theta);
      const z = r_throat * Math.sin(theta);
      const p = project(x, y, z);
      if (j === 0) ctx.moveTo(p.px, p.py);
      else ctx.lineTo(p.px, p.py);
    }
    
    // Ring Color: Cyan (Left) -> Gold (Right), violet in center
    const t_color = (t_z + 1.2) / 2.4;
    if (Math.abs(t_z) < 0.2 && pulseActive > 0.0) {
      ctx.strokeStyle = `rgba(185, 75, 255, ${0.4 + pulseActive * 0.6})`;
      ctx.lineWidth = 2.5;
    } else if (!isTraversable && Math.abs(t_z) < 0.3) {
      ctx.strokeStyle = "rgba(239, 68, 68, 0.7)";
      ctx.lineWidth = 2.0;
    } else {
      const r_c = Math.floor(38 * (1 - t_color) + 212 * t_color);
      const g_c = Math.floor(215 * (1 - t_color) + 175 * t_color);
      const b_c = Math.floor(208 * (1 - t_color) + 55 * t_color);
      ctx.strokeStyle = `rgba(${r_c}, ${g_c}, ${b_c}, 0.25)`;
      ctx.lineWidth = 1.0;
    }
    ctx.stroke();
  }
  
  // Draw Gao-Jafferis-Wall Negative Energy Shockwave Sheet
  if (isTraversable || pulseActive > 0.0) {
    ctx.beginPath();
    const shockSegments = 30;
    for (let i = 0; i <= shockSegments; i++) {
      const theta = (i / shockSegments) * Math.PI * 2;
      const p = project(0.0, 1.2 * Math.cos(theta), 1.2 * Math.sin(theta));
      if (i === 0) ctx.moveTo(p.px, p.py);
      else ctx.lineTo(p.px, p.py);
    }
    ctx.strokeStyle = `rgba(185, 75, 255, ${0.3 + pulseActive * 0.7})`;
    ctx.lineWidth = 3.0;
    ctx.stroke();
  }
  
  // Qubit Transit Animation
  if (qubitActive) {
    qubitPos += 0.015;
    
    // Check if qubit hits throat center
    if (Math.abs(qubitPos) < 0.1) {
      if (!isTraversable) {
        qubitActive = false;
        qubitState = "crushed";
        document.getElementById("telem-transit").innerText = "CRUSHED in Spacelike Singularity (UV = 1)";
        document.getElementById("telem-transit").style.color = "var(--red)";
        playTransitChime(false);
      }
    }
    
    if (qubitPos > 1.2) {
      qubitActive = false;
      qubitState = "emerged";
      document.getElementById("telem-transit").innerText = "EMERGED safely on Right Boundary (CFT_R)";
      document.getElementById("telem-transit").style.color = "var(--gold)";
      playTransitChime(true);
    }
    
    if (qubitActive) {
      const pQubit = project(qubitPos, 0.0, 0.0);
      ctx.beginPath();
      ctx.arc(pQubit.px, pQubit.py, 7.0, 0, Math.PI * 2);
      ctx.fillStyle = "#ffffff";
      ctx.shadowColor = "#38d7d0";
      ctx.shadowBlur = 15;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }
  
  // Update Audio Phase modulation
  if (audioCtx && oscRight) {
    const drift = 0.5 * Math.sin(time * (2.0 * Math.PI / beta));
    oscRight.frequency.setValueAtTime(96.42 + drift * (isTraversable ? 0.2 : 4.0), audioCtx.currentTime);
  }
  
  requestAnimationFrame(render);
}

render();

