/**
 * spin_engine.js
 * Studio Anamnesis · Chamber 16 Engine
 * Loop Quantum Gravity Spin Network Simulator & Audio Synthesizer
 * Zero external dependencies.
 */

(function() {
  const canvas = document.getElementById("spin-canvas");
  const ctx = canvas.getContext("2d");
  
  // Controls & Telemetry Elements
  const paramGamma = document.getElementById("param-gamma");
  const paramRho = document.getElementById("param-rho");
  const paramNodes = document.getElementById("param-nodes");
  
  const valGamma = document.getElementById("val-gamma");
  const valRho = document.getElementById("val-rho");
  const valNodes = document.getElementById("val-nodes");
  
  const telemGap = document.getElementById("telem-gap");
  const telemHubble = document.getElementById("telem-hubble");
  const telemState = document.getElementById("telem-state");
  const telemVol = document.getElementById("telem-vol");
  
  const audioToggle = document.getElementById("audio-toggle");

  // Spin colors
  const SPIN_COLORS = {
    0.5: "#00f5eb",
    1.0: "#2deb87",
    1.5: "#ffc32d",
    2.0: "#c373ff",
    2.5: "#ff73b9",
    3.0: "#ffffff"
  };

  // State
  let gamma = parseFloat(paramGamma.value);
  let rhoNorm = parseFloat(paramRho.value);
  let numNodes = parseInt(paramNodes.value);
  
  let rotX = 0.44;
  let rotY = 0.68;
  let isDragging = false;
  let lastMouseX = 0;
  let lastMouseY = 0;
  
  let nodes = [];
  let edges = [];
  let totalVolume = 0;

  // Build Graph
  function generateGraph() {
    nodes = [];
    edges = [];
    totalVolume = 0;
    
    // Deterministic pseudo-random
    function pseudoRand(seed) {
      let x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
      return x - Math.floor(x);
    }

    for (let i = 0; i < numNodes; i++) {
      let u = pseudoRand(i * 3 + 1);
      let v = pseudoRand(i * 3 + 2);
      let w = pseudoRand(i * 3 + 3);
      
      let theta = 2.0 * Math.PI * u;
      let phi = Math.acos(2.0 * v - 1.0);
      let r = Math.cbrt(w) * 0.95;
      
      nodes.push({
        id: i,
        x: r * Math.sin(phi) * Math.cos(theta),
        y: r * Math.sin(phi) * Math.sin(theta),
        z: r * Math.cos(phi),
        valence: 0,
        volume: 0
      });
    }

    const spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0];
    let edgeSeed = 100;
    
    for (let i = 0; i < numNodes; i++) {
      for (let j = i + 1; j < numNodes; j++) {
        let n1 = nodes[i];
        let n2 = nodes[j];
        let d = Math.hypot(n1.x - n2.x, n1.y - n2.y, n1.z - n2.z);
        if (d < 0.46) {
          edgeSeed++;
          let spin = spins[Math.floor(pseudoRand(edgeSeed) * spins.length)];
          edges.push({
            n1: i,
            n2: j,
            spin: spin,
            dist: d
          });
          n1.valence++;
          n2.valence++;
        }
      }
    }

    // Compute volume
    for (let n of nodes) {
      let incidentSpins = edges.filter(e => e.n1 === n.id || e.n2 === n.id).map(e => e.spin);
      let sumJ = incidentSpins.reduce((a, b) => a + b, 0);
      n.volume = sumJ > 0 ? Math.pow(sumJ, 1.5) * 0.35 : 0;
      totalVolume += n.volume;
    }
  }

  // Mouse interaction
  canvas.addEventListener("mousedown", (e) => {
    isDragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
  });

  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    let dx = e.clientX - lastMouseX;
    let dy = e.clientY - lastMouseY;
    rotY += dx * 0.008;
    rotX += dy * 0.008;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  });

  // UI Event Listeners
  paramGamma.addEventListener("input", (e) => {
    gamma = parseFloat(e.target.value);
    valGamma.textContent = gamma.toFixed(3);
    updateTelemetry();
    updateAudio();
  });

  paramRho.addEventListener("input", (e) => {
    rhoNorm = parseFloat(e.target.value);
    valRho.textContent = rhoNorm.toFixed(2);
    updateTelemetry();
    updateAudio();
  });

  paramNodes.addEventListener("input", (e) => {
    numNodes = parseInt(e.target.value);
    valNodes.textContent = numNodes;
    generateGraph();
    updateTelemetry();
  });

  function updateTelemetry() {
    let gap = 4.0 * Math.PI * Math.sqrt(3.0) * gamma;
    telemGap.textContent = gap.toFixed(3) + " ℓ_P²";
    
    // Hubble rate: H = sqrt(rho * (1 - rho/rho_crit))
    let hRatio = Math.sqrt(Math.max(0.0, rhoNorm * (1.0 - rhoNorm))) * 2.0;
    telemHubble.textContent = hRatio.toFixed(3) + " H_max";
    
    if (rhoNorm >= 0.95) {
      telemState.textContent = "QUANTUM BOUNCE";
      telemState.className = "phase-badge phase-bounce";
    } else if (rhoNorm > 0.60) {
      telemState.textContent = "Decelerating Contraction";
      telemState.className = "phase-badge phase-bounce";
    } else {
      telemState.textContent = "Stable Expansion";
      telemState.className = "phase-badge phase-stable";
    }
    
    telemVol.textContent = totalVolume.toFixed(1) + " ℓ_P³";
  }

  // Web Audio Synthesizer
  let audioCtx = null;
  let isAudioPlaying = false;
  let oscillators = [];
  let masterGain = null;
  let droneGain = null;

  function initAudio() {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();
    masterGain = audioCtx.createGain();
    masterGain.gain.setValueAtTime(0.25, audioCtx.currentTime);
    masterGain.connect(audioCtx.destination);

    // Drone
    let droneOsc = audioCtx.createOscillator();
    droneOsc.type = "sine";
    droneOsc.frequency.setValueAtTime(36.0, audioCtx.currentTime);
    droneGain = audioCtx.createGain();
    droneGain.gain.setValueAtTime(0.4, audioCtx.currentTime);
    droneOsc.connect(droneGain);
    droneGain.connect(masterGain);
    droneOsc.start();
    oscillators.push({ osc: droneOsc, type: "drone" });

    // Ladder Oscillators for spins [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    const spins = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0];
    spins.forEach((j, idx) => {
      let osc = audioCtx.createOscillator();
      let g = audioCtx.createGain();
      let f = 86.4 * Math.sqrt(j * (j + 1.0)) * (gamma / 0.274);
      osc.type = "sine";
      osc.frequency.setValueAtTime(f, audioCtx.currentTime);
      g.gain.setValueAtTime(0.12 / Math.sqrt(idx + 1), audioCtx.currentTime);
      osc.connect(g);
      g.connect(masterGain);
      osc.start();
      oscillators.push({ osc: osc, gain: g, spin: j, type: "ladder" });
    });
  }

  function updateAudio() {
    if (!audioCtx || !isAudioPlaying) return;
    oscillators.forEach(item => {
      if (item.type === "ladder") {
        let f = 86.4 * Math.sqrt(item.spin * (item.spin + 1.0)) * (gamma / 0.274);
        item.osc.frequency.setTargetAtTime(f, audioCtx.currentTime, 0.05);
      } else if (item.type === "drone") {
        let fDrone = 36.0 + (1.0 - rhoNorm) * 20.0;
        item.osc.frequency.setTargetAtTime(fDrone, audioCtx.currentTime, 0.05);
      }
    });
    if (droneGain) {
      let bAmp = 0.3 + 0.5 * Math.pow(rhoNorm, 2);
      droneGain.gain.setTargetAtTime(bAmp, audioCtx.currentTime, 0.05);
    }
  }

  audioToggle.addEventListener("click", () => {
    if (!audioCtx) {
      initAudio();
      isAudioPlaying = true;
      audioToggle.classList.add("active");
      audioToggle.textContent = "Silence Area Sonification";
    } else {
      if (audioCtx.state === "suspended") {
        audioCtx.resume();
        isAudioPlaying = true;
        audioToggle.classList.add("active");
        audioToggle.textContent = "Silence Area Sonification";
      } else if (audioCtx.state === "running") {
        audioCtx.suspend();
        isAudioPlaying = false;
        audioToggle.classList.remove("active");
        audioToggle.textContent = "Resume Area Sonification";
      }
    }
  });

  // Render Loop
  let time = 0;
  function render() {
    time += 0.012;
    
    // Auto slight drift
    if (!isDragging) {
      rotY += 0.002;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    let cx = canvas.width / 2;
    let cy = canvas.height / 2;
    // Scale breathes slightly with cosmological density
    let bounceFactor = 1.0 - rhoNorm * 0.35 + 0.03 * Math.sin(time * 2.0);
    let scale = 290.0 * bounceFactor;

    let cosRx = Math.cos(rotX), sinRx = Math.sin(rotX);
    let cosRy = Math.cos(rotY), sinRy = Math.sin(rotY);

    // Project nodes
    let projNodes = nodes.map(n => {
      let x1 = n.x * cosRy + n.z * sinRy;
      let y1 = n.y;
      let z1 = -n.x * sinRy + n.z * cosRy;

      let x2 = x1;
      let y2 = y1 * cosRx - z1 * sinRx;
      let z2 = y1 * sinRx + z1 * cosRx;

      let distCam = 2.6 - z2;
      return {
        id: n.id,
        px: cx + (x2 / distCam) * scale,
        py: cy + (y2 / distCam) * scale,
        pz: z2,
        volume: n.volume,
        valence: n.valence
      };
    });

    // Draw edges
    edges.forEach(e => {
      let p1 = projNodes[e.n1];
      let p2 = projNodes[e.n2];
      let avgZ = (p1.pz + p2.pz) * 0.5;
      let alpha = Math.max(0.15, Math.min(1.0, 0.6 + avgZ * 0.4));
      
      ctx.beginPath();
      ctx.moveTo(p1.px, p1.py);
      ctx.lineTo(p2.px, p2.py);
      ctx.strokeStyle = SPIN_COLORS[e.spin] || "#ffffff";
      ctx.globalAlpha = alpha * 0.75;
      ctx.lineWidth = Math.max(1, e.spin * 1.5 * (gamma / 0.274));
      ctx.stroke();
    });

    // Draw nodes
    let sortedNodes = [...projNodes].sort((a, b) => a.pz - b.pz);
    sortedNodes.forEach(n => {
      let alpha = Math.max(0.2, Math.min(1.0, 0.7 + n.pz * 0.4));
      let rad = Math.max(3.0, 2.5 + Math.cbrt(n.volume) * 3.5);
      
      let grad = ctx.createRadialGradient(n.px, n.py, 0, n.px, n.py, rad * 2.2);
      grad.addColorStop(0, "rgba(255, 255, 240, 1)");
      grad.addColorStop(0.4, "rgba(255, 195, 45, 0.8)");
      grad.addColorStop(1, "rgba(255, 195, 45, 0)");

      ctx.beginPath();
      ctx.arc(n.px, n.py, rad * 2.2, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.globalAlpha = alpha;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(n.px, n.py, rad * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = "#ffffff";
      ctx.globalAlpha = 1.0;
      ctx.fill();
    });

    ctx.globalAlpha = 1.0;
    requestAnimationFrame(render);
  }

  // Initialize
  generateGraph();
  updateTelemetry();
  render();
})();

