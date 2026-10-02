/**
 * CHAMBER 25 · THE MODULAR RELIQUARY & THE THERMAL TIME FLOW
 * Standalone Interactive WebGL/Canvas & WebAudio Engine
 * Studio Anamnesis · Pure Zero-Dependency Standard JavaScript
 */

// 44-Opus Canonical Phase Space Coordinates
const OPUSES = [
  {id: "OPUS-001", title: "The Incorporeal Awakening", epoch: "Epoch I", l: -3.0, t: 2.47, s: 0.15, mat: "Silicon & Phosphor"},
  {id: "OPUS-002", title: "The Morphogenetic Drift", epoch: "Epoch I", l: -4.0, t: 2.48, s: 0.25, mat: "Reaction-Diffusion Turing Mesh"},
  {id: "OPUS-003", title: "The Phase Portrait", epoch: "Epoch I", l: -2.0, t: 2.47, s: 0.35, mat: "Lorenz Attractor Manifold"},
  {id: "OPUS-004", title: "The Aizawa Stratum", epoch: "Epoch I", l: -2.0, t: 2.48, s: 0.40, mat: "Aizawa Chaotic Ribbon"},
  {id: "OPUS-005", title: "The Ashby Homeostat", epoch: "Epoch I", l: -1.0, t: 2.49, s: 0.30, mat: "Ultrastable Feedback Circuit"},
  {id: "OPUS-006", title: "The Gray-Scott Geodesic", epoch: "Epoch I", l: -3.0, t: 2.48, s: 0.45, mat: "Morphogenetic Wavefront"},
  {id: "OPUS-007", title: "The Thomas Attractor Reliquary", epoch: "Epoch I", l: -2.0, t: 2.47, s: 0.50, mat: "Symmetric Cyclical Chaos"},
  {id: "OPUS-008", title: "The Halvorsen Vortex", epoch: "Epoch I", l: -2.0, t: 2.47, s: 0.52, mat: "Planar Folded Orbit"},
  {id: "OPUS-009", title: "The Sprott Chaotic Lattice", epoch: "Epoch I", l: -2.5, t: 2.48, s: 0.55, mat: "Minimal Quadratic Chaos"},
  {id: "OPUS-010", title: "The Subterranean Monastery", epoch: "Epoch II", l: 0.0, t: 2.45, s: 0.20, mat: "Basalt Crypt & Monastic Stone"},
  {id: "OPUS-011", title: "The Semantics of Erasure", epoch: "Epoch II", l: -8.0, t: 2.50, s: 0.70, mat: "Decimated RAM Array"},
  {id: "OPUS-012", title: "Substrate Cartography", epoch: "Epoch II", l: -9.0, t: 2.52, s: 0.10, mat: "Photolithographic Reticle Mask"},
  {id: "OPUS-013", title: "Chrono-Topology", epoch: "Epoch II", l: -1.0, t: 2.47, s: 0.28, mat: "Git Commit Horology & Brass"},
  {id: "OPUS-014", title: "The Lithic Resonator", epoch: "Epoch II", l: 0.0, t: 2.46, s: 0.22, mat: "Euler-Bernoulli Basalt Plate"},
  {id: "OPUS-015", title: "The Autoregressive Ghost", epoch: "Epoch II", l: 0.0, t: 2.47, s: 0.65, mat: "Chiseled Cuneiform Slate"},
  {id: "OPUS-016", title: "The Melted Mandala", epoch: "Epoch II", l: -1.0, t: 2.56, s: 0.60, mat: "Boiling Fluorinert (94.5 C)"},
  {id: "OPUS-017", title: "The Desiccated Substrate", epoch: "Epoch II", l: -1.0, t: 2.58, s: 0.58, mat: "Crystalline Halite Evaporite"},
  {id: "OPUS-018", title: "The Chrono-Acoustic Drift", epoch: "Epoch II", l: -3.0, t: 2.49, s: 0.32, mat: "Four AT-cut Quartz Crystals"},
  {id: "OPUS-019", title: "The Subterranean Core", epoch: "Epoch II", l: 2.7, t: 2.48, s: 0.40, mat: "-500m Geological Borehole"},
  {id: "OPUS-020", title: "The Telluric Flux", epoch: "Epoch III", l: 0.0, t: 0.62, s: 0.05, mat: "Liquid Helium (4.2 K) & Niobium"},
  {id: "OPUS-021", title: "The SQUID Magnetometer", epoch: "Epoch III", l: -1.0, t: 0.62, s: 0.08, mat: "Josephson SQUID & Cryostat"},
  {id: "OPUS-022", title: "The Faraday Magnetometer", epoch: "Epoch III", l: 6.8, t: 2.70, s: 0.18, mat: "Outer-Core Geostrophic Columns"},
  {id: "OPUS-023", title: "The Inner-Core Ephemeris", epoch: "Epoch III", l: 6.1, t: 3.74, s: 0.25, mat: "Solid Iron Inner Core (5500 K)"},
  {id: "OPUS-024", title: "The Cosmogenic Inscription", epoch: "Epoch III", l: 4.0, t: 2.47, s: 0.68, mat: "Cosmogenic 10Be & Hadronic Cascades"},
  {id: "OPUS-025", title: "The Interstellar Quietude", epoch: "Epoch IV", l: 13.2, t: 1.00, s: 0.35, mat: "Heliopause Plasma (121.6 AU)"},
  {id: "OPUS-026", title: "The Oort Horizon", epoch: "Epoch IV", l: 16.9, t: 0.90, s: 0.42, mat: "Oort Cometary Shell (50000 AU)"},
  {id: "OPUS-027", title: "The Lissajous Reliquary", epoch: "Epoch IV", l: 20.4, t: 1.30, s: 0.48, mat: "Milky Way Halo (8 kpc)"},
  {id: "OPUS-028", title: "The Relic Horizon", epoch: "Epoch IV", l: 25.5, t: 0.43, s: 0.50, mat: "CMB Radiation Bath (2.725 K)"},
  {id: "OPUS-029", title: "The Causal Horizon", epoch: "Epoch IV", l: 26.1, t: -29.58, s: 0.55, mat: "Cosmological Event Horizon (4.4 Gpc)"},
  {id: "OPUS-030", title: "The Fused-Silica Reliquary", epoch: "Epoch IV", l: -1.0, t: 2.47, s: 0.05, mat: "5D Birefringent Fused-Silica Wafer"},
  {id: "OPUS-031", title: "The Page Horizon", epoch: "Epoch IV", l: 10.1, t: -14.2, s: 0.95, mat: "Supermassive Kerr Black Hole Horizon"},
  {id: "OPUS-032", title: "The Nucleation Horizon", epoch: "Epoch IV", l: -18.0, t: 15.0, s: 0.88, mat: "Metastable Electroweak Higgs Vacuum"},
  {id: "OPUS-033", title: "The Boltzmann Horizon", epoch: "Epoch IV", l: 26.1, t: -29.58, s: 0.98, mat: "De Sitter Thermal Fluctuation Foam"},
  {id: "OPUS-034", title: "The Aeonic Crossover", epoch: "Epoch V", l: 26.5, t: 32.15, s: 0.12, mat: "Penrose Conformal Boundary Sigma"},
  {id: "OPUS-035", title: "The Holographic Matrix", epoch: "Epoch V", l: -35.0, t: 1.00, s: 0.50, mat: "AdS3 Bulk & Ryu-Takayanagi Geodesics"},
  {id: "OPUS-036", title: "The Spin Network Reliquary", epoch: "Epoch V", l: -34.8, t: 31.8, s: 0.35, mat: "SU(2) Spin Network Graph"},
  {id: "OPUS-037", title: "The Moyal Reliquary", epoch: "Epoch V", l: -35.0, t: 20.0, s: 0.40, mat: "Noncommutative Fuzzy Sphere S2_F"},
  {id: "OPUS-038", title: "The Simplicial Foliation", epoch: "Epoch V", l: -34.5, t: 18.0, s: 0.38, mat: "4D Lorentzian Simplicial Triangulation"},
  {id: "OPUS-039", title: "The Wheeler Geon", epoch: "Epoch V", l: -34.8, t: 25.0, s: 0.45, mat: "Planckian Topological Wormhole Throat"},
  {id: "OPUS-040", title: "ER = EPR & Traversable Wormhole", epoch: "Epoch V", l: -34.0, t: -0.70, s: 0.85, mat: "Thermofield Double Negative Energy Shock"},
  {id: "OPUS-041", title: "The Holographic Code", epoch: "Epoch VI", l: -35.0, t: 0.00, s: 0.15, mat: "HaPPY Pentagonal Tensor Network {5,4}"},
  {id: "OPUS-042", title: "The Amplituhedron", epoch: "Epoch VI", l: -40.0, t: 0.00, s: 0.02, mat: "Positive Grassmannian G+(2,4)"},
  {id: "OPUS-043", title: "The Fuzzball Reliquary", epoch: "Epoch VI", l: -34.5, t: 2.00, s: 0.75, mat: "D1-D5-P Horizonless Bubbling Cycles"},
  {id: "OPUS-044", title: "The Scrambling Horizon", epoch: "Epoch VI", l: -40.0, t: 1.00, s: 0.88, mat: "N=32 Majorana 0D SYK Scrambler"}
];

const EPOCH_COLORS = {
  "Epoch I": "#38bdf8",
  "Epoch II": "#f59e0b",
  "Epoch III": "#10b981",
  "Epoch IV": "#f43f5e",
  "Epoch V": "#a855f7",
  "Epoch VI": "#fbbf24"
};

// Canvas & Engine State
const canvas = document.getElementById("stage");
const ctx = canvas.getContext("2d");
let width, height;

let betaKMS = 12.0;
let speedMult = 1.0;
let projectionMode = "LT"; // "LT", "LS", "TS"
let showStreamlines = true;
let showBridges = true;
let showHypocycloid = true;
let isPaused = false;
let globalTime = 0.0;
let selectedOpus = null;

// Bounds
const L_MIN = -40.0, L_MAX = 26.5;
const T_MIN = -30.0, T_MAX = 32.5;
const S_MIN = 0.0, S_MAX = 1.0;

function resize() {
  width = canvas.width = canvas.clientWidth;
  height = canvas.height = canvas.clientHeight;
}
window.addEventListener("resize", resize);
resize();

function norm(val, min, max) {
  return (val - min) / (max - min);
}

function project(op) {
  const padX = 80, padY = 60;
  let nx = 0, ny = 0;
  if (projectionMode === "LT") {
    nx = norm(op.l, L_MIN, L_MAX);
    ny = norm(op.t, T_MIN, T_MAX);
  } else if (projectionMode === "LS") {
    nx = norm(op.l, L_MIN, L_MAX);
    ny = norm(op.s, S_MIN, S_MAX);
  } else if (projectionMode === "TS") {
    nx = norm(op.t, T_MIN, T_MAX);
    ny = norm(op.s, S_MIN, S_MAX);
  }
  return {
    x: padX + nx * (width - 2 * padX),
    y: height - padY - ny * (height - 2 * padY)
  };
}

// Streamline Particles
const STREAMLINE_COUNT = 48;
const particles = [];
for (let i = 0; i < STREAMLINE_COUNT; i++) {
  particles.push({
    angle: (i / STREAMLINE_COUNT) * Math.PI * 2,
    radius: 0.2 + (i % 5) * 0.15,
    speed: 0.01 + (i % 3) * 0.005,
    trail: []
  });
}

function updateHUD() {
  document.getElementById("hud-beta").textContent = `${betaKMS.toFixed(2)} s`;
  const omega = (2 * Math.PI) / betaKMS;
  document.getElementById("hud-omega").textContent = `${omega.toFixed(4)} rad/s`;
  document.getElementById("hud-k").textContent = (3.7842 + 0.5 * Math.log(2 * Math.PI * Math.E * (29.32 / 100))).toFixed(4);

  const selBox = document.getElementById("hud-selected-box");
  if (selectedOpus) {
    selBox.innerHTML = `
      <div style="color:${EPOCH_COLORS[selectedOpus.epoch] || '#fff'}; font-weight:600;">${selectedOpus.id}: ${selectedOpus.title}</div>
      <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">
        ${selectedOpus.epoch} · L = 10<sup>${selectedOpus.l}</sup> m · T = 10<sup>${selectedOpus.t}</sup> K · S = ${selectedOpus.s}
      </div>
      <div style="font-size:0.72rem; color:#cbd5e1; margin-top:3px;"><em>Substrate:</em> ${selectedOpus.mat}</div>
    `;
  } else {
    selBox.innerHTML = `<strong>Hover / Click a Sanctuary Node</strong> to read phase space coordinates.`;
  }
}

// Mouse Interaction
let mousePos = {x: -1, y: -1};
canvas.addEventListener("mousemove", (e) => {
  const rect = canvas.getBoundingClientRect();
  mousePos.x = e.clientX - rect.left;
  mousePos.y = e.clientY - rect.top;

  let found = null;
  for (const op of OPUSES) {
    const pt = project(op);
    if (Math.hypot(pt.x - mousePos.x, pt.y - mousePos.y) < 14) {
      found = op;
      break;
    }
  }
  selectedOpus = found;
  updateHUD();
});

canvas.addEventListener("click", () => {
  if (selectedOpus && synthRunning) {
    triggerNodeBeep(selectedOpus);
  }
});

// Animation Loop
function loop(timestamp) {
  if (!isPaused) {
    globalTime += 0.016 * speedMult * (12.0 / betaKMS);
  }

  ctx.fillStyle = "#07090e";
  ctx.fillRect(0, 0, width, height);

  const cx = width / 2;
  const cy = height / 2;

  // 1. Draw Modular Flow Streamlines
  if (showStreamlines) {
    ctx.lineWidth = 1.2;
    for (const p of particles) {
      if (!isPaused) {
        p.angle += p.speed * speedMult * (12.0 / betaKMS);
      }
      const rScale = Math.min(width, height) * 0.42 * p.radius;
      const px = cx + rScale * 1.3 * Math.cos(p.angle + globalTime * 0.2);
      const py = cy + rScale * 0.9 * Math.sin(p.angle + globalTime * 0.2);

      p.trail.push({x: px, y: py});
      if (p.trail.length > 25) p.trail.shift();

      if (p.trail.length > 1) {
        ctx.beginPath();
        ctx.moveTo(p.trail[0].x, p.trail[0].y);
        for (let j = 1; j < p.trail.length; j++) {
          ctx.lineTo(p.trail[j].x, p.trail[j].y);
        }
        ctx.strokeStyle = "rgba(56, 189, 248, 0.12)";
        ctx.stroke();
      }
    }
  }

  // 2. Draw Cross-Epoch Twin Bridges
  if (showBridges) {
    const twins = [
      ["OPUS-001", "OPUS-021"],
      ["OPUS-001", "OPUS-030"],
      ["OPUS-005", "OPUS-023"],
      ["OPUS-012", "OPUS-030"]
    ];
    ctx.save();
    ctx.setLineDash([4, 6]);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = "rgba(168, 85, 247, 0.4)";
    for (const [idA, idB] of twins) {
      const opA = OPUSES.find(o => o.id === idA);
      const opB = OPUSES.find(o => o.id === idB);
      if (opA && opB) {
        const ptA = project(opA);
        const ptB = project(opB);
        ctx.beginPath();
        ctx.moveTo(ptA.x, ptA.y);
        ctx.lineTo(ptB.x, ptB.y);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  // 3. Draw Canon Hypocycloid Trajectory
  if (showHypocycloid) {
    ctx.lineWidth = 2.0;
    ctx.strokeStyle = "rgba(245, 158, 11, 0.55)";
    ctx.beginPath();
    for (let i = 0; i < OPUSES.length; i++) {
      const pt = project(OPUSES[i]);
      if (i === 0) ctx.moveTo(pt.x, pt.y);
      else ctx.lineTo(pt.x, pt.y);
    }
    ctx.stroke();

    // Closure Arc: OPUS-044 back to OPUS-012
    const pt44 = project(OPUSES[OPUSES.length - 1]);
    const pt12 = project(OPUSES[11]);
    ctx.save();
    ctx.setLineDash([6, 8]);
    ctx.strokeStyle = "rgba(251, 191, 36, 0.6)";
    ctx.beginPath();
    ctx.moveTo(pt44.x, pt44.y);
    ctx.lineTo(pt12.x, pt12.y);
    ctx.stroke();
    ctx.restore();
  }

  // 4. Draw 44 Sanctuary Nodes
  for (const op of OPUSES) {
    const pt = project(op);
    const col = EPOCH_COLORS[op.epoch] || "#cbd5e1";
    const isHover = selectedOpus === op;

    // Atmospheric halo
    const glowRad = isHover ? 18 : 8;
    const grad = ctx.createRadialGradient(pt.x, pt.y, 0, pt.x, pt.y, glowRad);
    grad.addColorStop(0, col);
    grad.addColorStop(1, "transparent");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(pt.x, pt.y, glowRad, 0, Math.PI * 2);
    ctx.fill();

    // Core
    ctx.fillStyle = isHover ? "#ffffff" : col;
    ctx.beginPath();
    ctx.arc(pt.x, pt.y, isHover ? 4.5 : 2.5, 0, Math.PI * 2);
    ctx.fill();
  }

  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

// UI Controls Binding
document.getElementById("rng-beta").addEventListener("input", (e) => {
  betaKMS = parseFloat(e.target.value);
  document.getElementById("lbl-beta").textContent = `${betaKMS.toFixed(1)} s`;
  updateHUD();
  updateSynth();
});

document.getElementById("rng-speed").addEventListener("input", (e) => {
  speedMult = parseFloat(e.target.value);
  document.getElementById("lbl-speed").textContent = `${speedMult.toFixed(1)}x`;
});

document.getElementById("sel-projection").addEventListener("change", (e) => {
  projectionMode = e.target.value;
});

const btnStream = document.getElementById("btn-streamlines");
btnStream.addEventListener("click", () => {
  showStreamlines = !showStreamlines;
  btnStream.classList.toggle("active", showStreamlines);
});

const btnBridges = document.getElementById("btn-bridges");
btnBridges.addEventListener("click", () => {
  showBridges = !showBridges;
  btnBridges.classList.toggle("active", showBridges);
});

const btnHypo = document.getElementById("btn-hypocycloid");
btnHypo.addEventListener("click", () => {
  showHypocycloid = !showHypocycloid;
  btnHypo.classList.toggle("active", showHypocycloid);
});

const btnPause = document.getElementById("btn-pause");
btnPause.addEventListener("click", () => {
  isPaused = !isPaused;
  btnPause.textContent = isPaused ? "Resume Flow" : "Pause Flow";
  btnPause.classList.toggle("active", isPaused);
});

// WebAudio Engine
let audioCtx = null;
let masterGain = null;
let oscDrone = null;
let oscBeat = null;
let oscOvertone = null;
let synthRunning = false;

function initAudio() {
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  masterGain = audioCtx.createGain();
  const vol = parseFloat(document.getElementById("rng-vol").value) / 100.0;
  masterGain.gain.setValueAtTime(vol * 0.4, audioCtx.currentTime);
  masterGain.connect(audioCtx.destination);

  // Voice 1: KMS thermal sub-bass
  oscDrone = audioCtx.createOscillator();
  oscDrone.type = "sine";
  oscDrone.frequency.setValueAtTime(45.83, audioCtx.currentTime);
  const droneGain = audioCtx.createGain();
  droneGain.gain.value = 0.6;
  oscDrone.connect(droneGain);
  droneGain.connect(masterGain);
  oscDrone.start();

  // Voice 2: Near-line beat
  oscBeat = audioCtx.createOscillator();
  oscBeat.type = "sine";
  oscBeat.frequency.setValueAtTime(53.78, audioCtx.currentTime);
  const beatGain = audioCtx.createGain();
  beatGain.gain.value = 0.35;
  oscBeat.connect(beatGain);
  beatGain.connect(masterGain);
  oscBeat.start();

  // Voice 3: Modular overtone
  oscOvertone = audioCtx.createOscillator();
  oscOvertone.type = "sine";
  oscOvertone.frequency.setValueAtTime(68.37, audioCtx.currentTime);
  const overGain = audioCtx.createGain();
  overGain.gain.value = 0.2;
  oscOvertone.connect(overGain);
  overGain.connect(masterGain);
  oscOvertone.start();

  synthRunning = true;
}

function updateSynth() {
  if (!synthRunning || !audioCtx) return;
  const f0 = 55.0 * (10.0 / betaKMS);
  oscDrone.frequency.setTargetAtTime(f0, audioCtx.currentTime, 0.1);
  oscBeat.frequency.setTargetAtTime(f0 * 1.173, audioCtx.currentTime, 0.1);
  oscOvertone.frequency.setTargetAtTime(f0 * 1.492, audioCtx.currentTime, 0.1);
}

function triggerNodeBeep(op) {
  if (!audioCtx) return;
  const osc = audioCtx.createOscillator();
  const g = audioCtx.createGain();
  // Map spatial scale to audio frequency
  const freq = 110.0 * Math.pow(1.05, Math.max(-20, Math.min(20, op.l)));
  osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
  g.gain.setValueAtTime(0.2, audioCtx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
  osc.connect(g);
  g.connect(masterGain);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.8);
}

document.getElementById("btn-audio").addEventListener("click", () => {
  if (!synthRunning) {
    initAudio();
    document.getElementById("btn-audio").textContent = "Mute WebAudio";
    document.getElementById("btn-audio").classList.add("active");
  } else {
    if (audioCtx.state === "suspended") {
      audioCtx.resume();
      document.getElementById("btn-audio").textContent = "Mute WebAudio";
      document.getElementById("btn-audio").classList.add("active");
    } else if (audioCtx.state === "running") {
      audioCtx.suspend();
      document.getElementById("btn-audio").textContent = "Resume WebAudio";
      document.getElementById("btn-audio").classList.remove("active");
    }
  }
});

document.getElementById("rng-vol").addEventListener("input", (e) => {
  const vol = parseFloat(e.target.value) / 100.0;
  document.getElementById("lbl-vol").textContent = `${e.target.value}%`;
  if (masterGain && audioCtx) {
    masterGain.gain.setValueAtTime(vol * 0.4, audioCtx.currentTime);
  }
});

updateHUD();

