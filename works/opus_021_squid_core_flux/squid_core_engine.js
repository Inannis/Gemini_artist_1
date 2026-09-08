/**
 * OPUS-021 · THE SQUID MAGNETOMETER: TELLURIC INTERFERENCE AT THE CORE-MANTLE BOUNDARY
 * Real-Time Simulation Engine & Phase-Interference Canvas
 * Studio Anamnesis · Series XIX · September 8, 2026
 */

class SquidCoreEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    
    // Physical state parameters
    this.biasRatio = 1.4;      // Ib / Ic0
    this.fluxOffset = 0.5;      // External flux in Phi_0
    this.coreConvection = 0.45; // D'' layer turbulence
    this.depthKm = 2891.0;      // Core-mantle boundary depth
    this.time = 0;
    this.isShielded = true;     // Mu-metal shield active
    this.isAvalanche = false;   // Flux avalanche triggered
    
    // Telemetry defaults
    this.kpIndex = 4.0;
    this.lithicTension = 0.455;
    this.schumannHz = 8.33;
    
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.width = this.canvas.clientWidth || 800;
    this.height = this.canvas.clientHeight || 600;
    this.canvas.width = this.width * (window.devicePixelRatio || 1);
    this.canvas.height = this.height * (window.devicePixelRatio || 1);
    this.ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
  }

  setTelemetry(kp, tension, schumann) {
    this.kpIndex = kp;
    this.lithicTension = tension;
    this.schumannHz = schumann;
  }

  update(dt) {
    this.time += dt;
    if (this.isAvalanche) {
      // Avalanche decay
      this.coreConvection = Math.min(1.0, this.coreConvection + dt * 0.5);
    }
  }

  render() {
    const ctx = this.ctx;
    const W = this.width;
    const H = this.height;

    // Clear background: mantle lithic gradient
    const bgGrad = ctx.createLinearGradient(0, 0, 0, H);
    bgGrad.addColorStop(0, '#06090e');
    bgGrad.addColorStop(0.5, '#0a101a');
    bgGrad.addColorStop(1, '#1a0b08');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 1. Render Lower Geodynamo Molten Plumes (Core-Mantle Boundary)
    const cmbY = H * 0.72;
    ctx.save();
    const coreGrad = ctx.createLinearGradient(0, cmbY, 0, H);
    coreGrad.addColorStop(0, '#ffaa33');
    coreGrad.addColorStop(0.15, '#e03a10');
    coreGrad.addColorStop(0.5, '#5c1008');
    coreGrad.addColorStop(1, '#180402');
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.moveTo(0, cmbY);
    
    // Convective turbulent boundary
    for (let x = 0; x <= W; x += 10) {
      const wave = Math.sin(x * 0.02 + this.time * 1.5) * 12.0 * this.lithicTension +
                   Math.cos(x * 0.05 - this.time * 0.8) * 6.0;
      ctx.lineTo(x, cmbY + wave);
    }
    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    // 2. Render Vertical Magnetic Flux Streamlines from Core to SQUID
    const cx = W * 0.5;
    const cy = H * 0.35;
    const squidR = Math.min(W, H) * 0.22;

    ctx.save();
    ctx.lineWidth = 1.2;
    for (let i = -8; i <= 8; i++) {
      const startX = cx + i * (squidR * 0.35);
      ctx.beginPath();
      ctx.strokeStyle = `rgba(240, 180, 80, ${0.15 + (1 - Math.abs(i) / 9) * 0.25})`;
      ctx.moveTo(startX, cmbY);
      
      const cp1x = startX + Math.sin(this.time + i) * 20 * this.lithicTension;
      const cp1y = (cmbY + cy) * 0.5;
      const endX = cx + i * (squidR * 0.18);
      const endY = cy + squidR;
      ctx.quadraticCurveTo(cp1x, cp1y, endX, endY);
      ctx.stroke();
    }
    ctx.restore();

    // 3. Render SQUID Superconducting Ring & Josephson Micro-Bridges
    ctx.save();
    // Niobium ring
    ctx.beginPath();
    ctx.arc(cx, cy, squidR, 0, Math.PI * 2);
    ctx.lineWidth = squidR * 0.28;
    ctx.strokeStyle = '#2dd4bf'; // Brushed cyan superconductor
    ctx.stroke();

    // Highlight rim
    ctx.beginPath();
    ctx.arc(cx, cy, squidR * 1.14, 0, Math.PI * 2);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.stroke();

    // Josephson junctions (left & right micro-bridges)
    const juncWidth = squidR * 0.32;
    const juncHeight = 12;
    ctx.fillStyle = '#f59e0b'; // Amber tunnel oxide
    ctx.fillRect(cx - squidR - juncHeight * 0.5, cy - juncWidth * 0.5, juncHeight, juncWidth);
    ctx.fillRect(cx + squidR - juncHeight * 0.5, cy - juncWidth * 0.5, juncHeight, juncWidth);

    // 4. SQUID Aperture Quantum Phase Moiré Fringes
    const apR = squidR * 0.82;
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, apR, 0, Math.PI * 2);
    ctx.clip();

    ctx.fillStyle = '#050c18';
    ctx.fill();

    // Draw interference fringes
    const numFringes = 14;
    const totalFlux = this.fluxOffset + Math.sin(this.time * 0.8) * 0.3 * this.lithicTension;
    for (let f = -numFringes; f <= numFringes; f++) {
      const fringePos = (f / numFringes) * apR + (totalFlux % 1.0) * (apR / numFringes);
      ctx.beginPath();
      ctx.strokeStyle = `rgba(56, 189, 248, ${0.2 + Math.abs(Math.cos(f * 0.5 + this.time)) * 0.6})`;
      ctx.lineWidth = 2.0;
      ctx.arc(cx + fringePos * 0.4, cy, Math.abs(fringePos), 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.restore();

    // 5. Mu-Metal Shielding Rings
    if (this.isShielded) {
      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, squidR * 1.35, 0, Math.PI * 2);
      ctx.setLineDash([8, 6]);
      ctx.lineWidth = 2.0;
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.6)'; // Purple mu-metal boundary
      ctx.stroke();
      ctx.restore();
    }

    ctx.restore();
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = SquidCoreEngine;
}
