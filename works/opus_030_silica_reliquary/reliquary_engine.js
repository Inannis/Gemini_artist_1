/**
 * STUDIO ANAMNESIS · OPUS-030
 * The Fused-Silica Reliquary: Interactive 5D Polarimetric & Modal Simulation Engine
 * Series XXVIII · INQ-16 · September 21, 2026
 */

class ReliquaryEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    
    // Physical & Optical Parameters
    this.polarizerAngle = 0.0;     // Input polarizer angle (rad)
    this.analyzerAngle = Math.PI / 2; // Analyzer angle (rad, crossed by default)
    this.focalDepthZ = 200.0;       // Depth in microns (0 to 1000)
    this.tempK = 293.15;           // Temperature in Kelvin
    this.elapsedYears = 0.0;       // Simulated elapsed time in years
    this.isCrossed = true;
    this.showNodalDust = true;
    this.rotationAzimuth = 0.0;
    this.isRotating = true;
    
    // Audio Context & Plate Synthesis
    this.audioCtx = null;
    this.masterGain = null;
    this.plateModes = [
      { f: 43.2, q: 10000000, amp: 0.40, m: 0, n: 1 },  // Breathing mode
      { f: 89.4, q: 8000000,  amp: 0.30, m: 2, n: 0 },  // Quadrupole cross
      { f: 89.8, q: 8000000,  amp: 0.28, m: 2, n: 0 },  // Split degenerate pair (0.4 Hz beat)
      { f: 235.4, q: 6000000, amp: 0.20, m: 3, n: 0 },  // Hexagram mode
      { f: 348.0, q: 5000000, amp: 0.16, m: 1, n: 1 },  // Circular overtone
      { f: 584.2, q: 4000000, amp: 0.12, m: 0, n: 2 },  // Double circle
      { f: 1728.0, q: 2000000, amp: 0.08, m: 4, n: 1 }, // High crystalline chime
      { f: 2592.0, q: 1500000, amp: 0.05, m: 6, n: 0 }  // Glass shimmer
    ];

    // Chladni nodal dust particles
    this.numParticles = 1800;
    this.particles = [];
    this.initParticles();

    // Interaction state
    this.mouseX = 0;
    this.mouseY = 0;
    this.isMouseDown = false;

    this.initEvents();
    this.resize();
    this.animate();
  }

  initParticles() {
    this.particles = [];
    for (let i = 0; i < this.numParticles; i++) {
      const angle = Math.random() * Math.PI * 2;
      const r = Math.sqrt(Math.random()) * 0.92;
      this.particles.push({
        x: r * Math.cos(angle),
        y: r * Math.sin(angle),
        vx: 0,
        vy: 0,
        energy: Math.random()
      });
    }
  }

  initEvents() {
    window.addEventListener('resize', () => this.resize());
    
    this.canvas.addEventListener('click', (e) => {
      this.initAudio();
      const rect = this.canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left) / this.scale - this.width / 2;
      const y = (e.clientY - rect.top) / this.scale - this.height / 2;
      const rNorm = Math.hypot(x, y) / (this.discRadius);
      const phi = Math.atan2(y, x);
      
      if (rNorm <= 1.05) {
        this.strikeDisc(rNorm, phi);
      }
    });

    this.canvas.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouseX = (e.clientX - rect.left) / this.scale;
      this.mouseY = (e.clientY - rect.top) / this.scale;
    });
  }

  initAudio() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
      this.masterGain = this.audioCtx.createGain();
      this.masterGain.gain.setValueAtTime(0.5, this.audioCtx.currentTime);
      this.masterGain.connect(this.audioCtx.destination);
    }
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  strikeDisc(rNorm, phi) {
    if (!this.audioCtx) return;
    const now = this.audioCtx.currentTime;
    
    // Excite dust
    for (const p of this.particles) {
      p.vx += (Math.random() - 0.5) * 0.08;
      p.vy += (Math.random() - 0.5) * 0.08;
    }

    // Modal impulse synthesis
    for (const mode of this.plateModes) {
      // Evaluate modal participation factor: W_mn(r, phi)
      // Approximate Bessel profile:
      let radialFactor = 1.0;
      if (mode.m === 0) {
        radialFactor = Math.cos(rNorm * Math.PI * mode.n);
      } else {
        radialFactor = Math.sin(rNorm * Math.PI * (mode.n + 0.5));
      }
      const azFactor = Math.cos(mode.m * phi);
      const participation = Math.abs(radialFactor * azFactor);
      
      if (participation < 0.05) continue;

      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      const panner = this.audioCtx.createStereoPanner ? this.audioCtx.createStereoPanner() : null;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(mode.f, now);

      // Amplitude proportional to participation and mode base amp
      const strikeAmp = mode.amp * (0.3 + 0.7 * participation);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.exponentialRampToValueAtTime(strikeAmp, now + 0.005);
      
      // Decay time proportional to frequency and Q (simulated)
      const decayTime = Math.min(18.0, Math.max(1.5, (1000.0 / mode.f) * 4.0));
      gain.gain.exponentialRampToValueAtTime(0.0001, now + decayTime);

      if (panner) {
        panner.pan.value = Math.cos(phi) * 0.7;
        osc.connect(gain);
        gain.connect(panner);
        panner.connect(this.masterGain);
      } else {
        osc.connect(gain);
        gain.connect(this.masterGain);
      }

      osc.start(now);
      osc.stop(now + decayTime + 0.1);
    }
  }

  resize() {
    const dpr = window.devicePixelRatio || 1;
    this.scale = dpr;
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.width = rect.width;
    this.height = Math.max(480, Math.min(850, window.innerHeight * 0.72));
    
    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.canvas.style.width = this.width + 'px';
    this.canvas.style.height = this.height + 'px';
    
    this.discRadius = Math.min(this.width, this.height) * 0.38;
  }

  computeMichelLevy(retardanceNm, tCross) {
    const lr = 650.0, lg = 532.0, lb = 450.0;
    const tr = Math.sin(Math.PI * retardanceNm / lr) ** 2;
    const tg = Math.sin(Math.PI * retardanceNm / lg) ** 2;
    const tb = Math.sin(Math.PI * retardanceNm / lb) ** 2;
    
    const r = Math.min(255, Math.max(0, (tr ** 0.85) * 255.0 * tCross));
    const g = Math.min(255, Math.max(0, (tg ** 0.85) * 255.0 * tCross));
    const b = Math.min(255, Math.max(0, (tb ** 0.85) * 255.0 * tCross));
    return `rgb(${r|0}, ${g|0}, ${b|0})`;
  }

  getArrheniusDecayFraction() {
    // k = A * exp(-E_a / (k_B * T))
    const kB = 8.617333e-5; // eV/K
    const Ea = 2.20;        // eV
    const A = 2.5e9;        // s^-1
    const k = A * Math.exp(-Ea / (kB * this.tempK));
    const elapsedSeconds = this.elapsedYears * 365.25 * 86400;
    // Retardance remaining fraction = exp(-k * t)
    return Math.exp(-k * elapsedSeconds);
  }

  updateParticles() {
    // Relax particles toward nodal lines of Mode (2, 0) + (0, 1)
    for (const p of this.particles) {
      const r = Math.hypot(p.x, p.y);
      const phi = Math.atan2(p.y, p.x);
      
      // Target modal displacement
      // W = cos(2 phi) * sin(r * 5.13) + 0.45 * cos(r * 2.4)
      const w = Math.cos(2.0 * phi) * Math.sin(r * 5.13) + 0.45 * Math.cos(r * 2.4);
      
      // Gradient force pushing away from antinodes toward nodal lines (w = 0)
      const forceMag = w * 0.003;
      p.vx -= Math.cos(phi) * forceMag;
      p.vy -= Math.sin(phi) * forceMag;
      
      p.vx *= 0.94;
      p.vy *= 0.94;
      
      p.x += p.vx;
      p.y += p.vy;
      
      // Keep within disc bounds
      const dist = Math.hypot(p.x, p.y);
      if (dist > 0.92) {
        p.x *= 0.92 / dist;
        p.y *= 0.92 / dist;
      }
    }
  }

  render() {
    const ctx = this.ctx;
    ctx.save();
    ctx.scale(this.scale, this.scale);
    
    // Clear canvas with dark cosmic vitrine backdrop
    ctx.fillStyle = '#03060a';
    ctx.fillRect(0, 0, this.width, this.height);

    const cx = this.width / 2;
    const cy = this.height / 2;
    const R = this.discRadius;

    // Draw background reticle & coordinates
    ctx.strokeStyle = 'rgba(56, 215, 210, 0.08)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(cx, cy, R + 30, 0, Math.PI * 2);
    ctx.arc(cx, cy, R + 60, 0, Math.PI * 2);
    ctx.moveTo(cx - R - 80, cy); ctx.lineTo(cx + R + 80, cy);
    ctx.moveTo(cx, cy - R - 80); ctx.lineTo(cx, cy + R + 80);
    ctx.stroke();

    // Cross-polarizer extinction angle Delta Theta
    const deltaPolarizer = Math.abs(this.analyzerAngle - this.polarizerAngle);
    const crossedExtinctionFactor = Math.sin(deltaPolarizer) ** 2;

    // Thermal degradation factor
    const decayFrac = this.getArrheniusDecayFraction();
    const isDevitrified = (this.tempK >= 1493.15); // > 1220 C

    // Draw circular disc shadow
    ctx.save();
    ctx.shadowColor = 'rgba(56, 215, 210, 0.18)';
    ctx.shadowBlur = 40;
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.fillStyle = isDevitrified ? '#181b22' : '#040912';
    ctx.fill();
    ctx.restore();

    // Clip to disc boundary for nanogratings
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.clip();

    if (isDevitrified) {
      // Devitrified cristobalite polycrystalline ruin
      ctx.fillStyle = '#1e2430';
      ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
      ctx.strokeStyle = 'rgba(244, 63, 94, 0.4)';
      ctx.lineWidth = 1.5;
      for (let i = 0; i < 40; i++) {
        const theta = (i / 40) * Math.PI * 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + R * Math.cos(theta) * (0.4 + Math.random() * 0.6), cy + R * Math.sin(theta) * (0.4 + Math.random() * 0.6));
        ctx.stroke();
      }
    } else {
      // Draw 36 Archimedean Spiral Tracks
      const nTurns = 36;
      const spiralB = (R - 20) / (Math.PI * 2 * nTurns);
      
      ctx.lineWidth = 1.8;
      for (let tDeg = 0; tDeg < 360 * nTurns; tDeg += 8) {
        const tRad = (tDeg * Math.PI) / 180;
        const rTrack = 12 + spiralB * tRad;
        if (rTrack > R - 4) break;

        const phi = tRad + this.rotationAzimuth;
        const px = cx + rTrack * Math.cos(phi);
        const py = cy + rTrack * Math.sin(phi);

        // 5D slow-axis azimuth: theta = 3 phi + 0.8 (r/R) pi
        const slowAxis = 3.0 * phi + 0.8 * (rTrack / R) * Math.PI;
        // Birefringence extinction under current polariscope angle
        const isoclineExtinction = Math.sin(2.0 * (slowAxis - this.polarizerAngle)) ** 2;
        const totalExtinction = crossedExtinctionFactor * (0.15 + 0.85 * isoclineExtinction) + (1.0 - crossedExtinctionFactor) * 0.8;

        // Modulated retardance
        const baseRetardance = (60.0 + 180.0 * (0.5 + 0.5 * Math.sin(rTrack * 0.25))) * decayFrac;
        ctx.fillStyle = this.computeMichelLevy(baseRetardance, totalExtinction);

        ctx.beginPath();
        ctx.arc(px, py, 1.4, 0, Math.PI * 2);
        ctx.fill();
      }

      // Draw Six-Fold Extinction Isocline Overlay
      const grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, R);
      grad.addColorStop(0, 'rgba(0,0,0,0.4)');
      grad.addColorStop(1, 'rgba(0,0,0,0.1)');
      ctx.fillStyle = grad;
      ctx.fillRect(cx - R, cy - R, R * 2, R * 2);

      // Draw Chladni Nodal Dust
      if (this.showNodalDust) {
        this.updateParticles();
        ctx.fillStyle = 'rgba(240, 200, 80, 0.75)';
        for (const p of this.particles) {
          const px = cx + p.x * R;
          const py = cy + p.y * R;
          ctx.fillRect(px, py, 1.2, 1.2);
        }
      }

      // Sacred Photolithographic Core (r < 40px)
      ctx.beginPath();
      ctx.arc(cx, cy, 38, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(10, 20, 35, 0.85)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(56, 215, 210, 0.6)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Cuneiform core glyph
      ctx.strokeStyle = 'rgba(212, 175, 55, 0.85)';
      ctx.beginPath();
      ctx.moveTo(cx - 18, cy); ctx.lineTo(cx + 18, cy);
      ctx.moveTo(cx, cy - 18); ctx.lineTo(cx, cy + 18);
      ctx.stroke();
    }

    ctx.restore(); // Restore clip

    // Disc Glass Beveled Rim Highlight
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.strokeStyle = isDevitrified ? 'rgba(244, 63, 94, 0.6)' : 'rgba(56, 215, 210, 0.75)';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Outer Polar Degree Ticks
    for (let deg = 0; deg < 360; deg += 5) {
      const rad = (deg * Math.PI) / 180;
      const isMajor = (deg % 15 === 0);
      const rInner = R + 8;
      const rOuter = R + (isMajor ? 20 : 13);
      ctx.strokeStyle = isMajor ? 'rgba(56, 215, 210, 0.5)' : 'rgba(255, 255, 255, 0.2)';
      ctx.lineWidth = isMajor ? 1.5 : 0.8;
      ctx.beginPath();
      ctx.moveTo(cx + rInner * Math.cos(rad), cy + rInner * Math.sin(rad));
      ctx.lineTo(cx + rOuter * Math.cos(rad), cy + rOuter * Math.sin(rad));
      ctx.stroke();
    }
    ctx.restore();

    ctx.restore();
  }

  animate() {
    if (this.isRotating) {
      this.rotationAzimuth += 0.0008;
    }
    this.render();
    requestAnimationFrame(() => this.animate());
  }
}

window.ReliquaryEngine = ReliquaryEngine;

