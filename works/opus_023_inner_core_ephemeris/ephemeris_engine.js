/**
 * STUDIO ANAMNESIS · OPUS-023: THE INNER-CORE EPHEMERIS
 * Seismic Doublet Interferometry & Gravitational Libration at r = 1,220 km
 * 4K UHD Procedural Canvas / SVG Vector Cartography Engine
 * Pure Vanilla JavaScript (Zero External Dependencies)
 */

class EphemerisEngine {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.W = canvas.width;
    this.H = canvas.height;

    // Physical Parameters
    this.innerCoreRadiusKm = 1221.5;
    this.polarAnisotropy = 0.031; // +3.1% polar fast axis
    this.oscillationPeriodYears = 65.0;
    this.currentEpoch = 2026.69;
    this.relativeRotationDeg = -0.8995;
    this.rotationRateDegYr = 0.0839;
    this.doubletResidualMs = 5.12;
    this.gravitationalTorque = "4.71e+18 N·m";

    // Interactive timeline
    this.selectedYear = 2026.69;
    this.time = 0.0;
  }

  resize(w, h) {
    this.canvas.width = w;
    this.canvas.height = h;
    this.W = w;
    this.H = h;
  }

  setYear(yr) {
    this.selectedYear = yr;
    const omega = (2.0 * Math.PI) / 65.0;
    const phase = omega * (yr - 1970.0);
    this.relativeRotationDeg = 1.25 * Math.sin(phase);
    this.rotationRateDegYr = 1.25 * omega * Math.cos(phase);
    this.doubletResidualMs = - (2400.0e3 / (11.03e3**2)) * (0.0015 * 11.03e3) * (this.relativeRotationDeg * Math.PI / 180.0) * 1000.0;
  }

  renderFrame(tSec = 0) {
    const ctx = this.ctx;
    const W = this.W;
    const H = this.H;
    this.time = tSec;

    // 1. Deep Terrestrial Abyss Background
    const bgGrad = ctx.createRadialGradient(W * 0.5, H * 0.5, 60, W * 0.5, H * 0.5, W * 0.7);
    bgGrad.addColorStop(0, '#0a0604');
    bgGrad.addColorStop(0.5, '#060302');
    bgGrad.addColorStop(1, '#020101');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 2. Geodesic Metric Coordinate Grid
    ctx.save();
    ctx.strokeStyle = 'rgba(70, 45, 25, 0.25)';
    ctx.lineWidth = 1;
    const gridSize = Math.floor(W / 48);
    for (let x = 0; x < W; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, H);
      ctx.stroke();
    }
    for (let y = 0; y < H; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }
    ctx.restore();

    // 3. Render Solid Inner Core Sphere (Center Focus)
    const coreX = W * 0.5;
    const coreY = H * 0.48;
    const coreRadius = Math.min(W, H) * 0.34;
    this.renderInnerCoreSphere(ctx, coreX, coreY, coreRadius);

    // 4. Render Seismic Doublet Waveforms (Bottom Panel)
    this.renderSeismicDoublets(ctx, W * 0.1, H * 0.82, W * 0.8, H * 0.14);

    // 5. Scientific Cartography HUD
    this.renderHUD(ctx, W, H);
  }

  renderInnerCoreSphere(ctx, cx, cy, radius) {
    ctx.save();

    // Solid Iron-Nickel Core Disc with anisotropic metallic shading
    const coreGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
    coreGrad.addColorStop(0, '#754820');
    coreGrad.addColorStop(0.6, '#42240c');
    coreGrad.addColorStop(0.9, '#221105');
    coreGrad.addColorStop(1, '#110802');
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.fill();

    // Preferred Crystalline Orientation Texture (Hexagonal Grain)
    ctx.strokeStyle = 'rgba(255, 190, 80, 0.08)';
    ctx.lineWidth = 1.2;
    for (let r = -radius * 0.9; r <= radius * 0.9; r += 16) {
      const halfW = Math.sqrt(Math.max(0, radius * radius - r * r));
      ctx.beginPath();
      ctx.moveTo(cx - halfW, cy + r);
      ctx.lineTo(cx + halfW, cy + r);
      ctx.stroke();
    }

    // Outer Boundary Rim
    ctx.strokeStyle = 'rgba(255, 200, 100, 0.7)';
    ctx.lineWidth = 2.0;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.stroke();

    // Polar Fast Axis (North-South Gold Shaft, slightly rotated by libration angle)
    const libAngleRad = (this.relativeRotationDeg * Math.PI) / 180.0;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(libAngleRad);

    ctx.strokeStyle = '#ffd750';
    ctx.lineWidth = 3.0;
    ctx.shadowBlur = 14;
    ctx.shadowColor = '#ffd750';
    ctx.beginPath();
    ctx.moveTo(0, -radius * 1.15);
    ctx.lineTo(0, radius * 1.15);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Axis Labels
    ctx.font = '11px "Courier New", monospace';
    ctx.fillStyle = '#ffd750';
    ctx.textAlign = 'center';
    ctx.fillText("POLAR FAST AXIS [0001] · vp = 11.37 km/s (+3.1%)", 0, -radius * 1.18);
    ctx.fillText("CRYSTALLINE SYMMETRY AXIS", 0, radius * 1.25);
    ctx.restore();

    // Seismic Raypath 1: 1995 Epoch (Cyan)
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 2.0;
    ctx.shadowBlur = 10;
    ctx.shadowColor = '#00f0ff';
    ctx.beginPath();
    ctx.moveTo(cx - radius * 0.85, cy - radius * 0.85);
    ctx.quadraticCurveTo(cx, cy + radius * 0.35, cx + radius * 0.85, cy - radius * 0.85);
    ctx.stroke();

    // Seismic Raypath 2: 2026 Repeating Doublet (Celestial Amber)
    ctx.strokeStyle = 'rgba(255, 215, 80, 0.85)';
    ctx.lineWidth = 2.0;
    ctx.shadowColor = '#ffd750';
    ctx.beginPath();
    ctx.moveTo(cx - radius * 0.85 + 10, cy - radius * 0.85 - 4);
    ctx.quadraticCurveTo(cx + 8, cy + radius * 0.35 - 4, cx + radius * 0.85 + 10, cy - radius * 0.85 - 4);
    ctx.stroke();
    ctx.shadowBlur = 0;

    ctx.restore();
  }

  renderSeismicDoublets(ctx, x, y, w, h) {
    ctx.save();
    // Backdrop panel
    ctx.fillStyle = 'rgba(12, 8, 5, 0.85)';
    ctx.strokeStyle = 'rgba(255, 180, 70, 0.3)';
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);

    // Title
    ctx.font = '11px "Courier New", monospace';
    ctx.fillStyle = 'rgba(255, 200, 100, 0.9)';
    ctx.fillText("SEISMIC DOUBLET INTERFEROMETRY (PKIKP CORE PHASE TRAVEL-TIME RESIDUAL)", x + 16, y + 20);

    const midY1 = y + h * 0.42;
    const midY2 = y + h * 0.76;
    const waveW = w - 180;
    const startX = x + 160;

    ctx.fillStyle = '#00f0ff';
    ctx.fillText("1995 BASELINE:", x + 16, midY1 + 4);
    ctx.fillStyle = '#ffd750';
    ctx.fillText("2026 DOUBLET:", x + 16, midY2 + 4);

    // Trace 1 (1995)
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let px = 0; px < waveW; px++) {
      const tMs = (px / waveW) * 80.0; // 0 to 80ms
      const dt = (tMs - 30.0) / 4.5;
      const ricker = (1.0 - 2.0 * dt * dt) * Math.exp(-dt * dt);
      const py = midY1 - ricker * 18.0;
      if (px === 0) ctx.moveTo(startX + px, py);
      else ctx.lineTo(startX + px, py);
    }
    ctx.stroke();

    // Trace 2 (2026 with calculated delay)
    ctx.strokeStyle = '#ffd750';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    const delayMs = this.doubletResidualMs;
    for (let px = 0; px < waveW; px++) {
      const tMs = (px / waveW) * 80.0;
      const dt = (tMs - (30.0 + delayMs)) / 4.5;
      const ricker = (1.0 - 2.0 * dt * dt) * Math.exp(-dt * dt);
      const py = midY2 - ricker * 18.0;
      if (px === 0) ctx.moveTo(startX + px, py);
      else ctx.lineTo(startX + px, py);
    }
    ctx.stroke();

    // Delta T indicator
    ctx.fillStyle = '#fffae0';
    ctx.textAlign = 'right';
    ctx.fillText(`Δt = ${this.doubletResidualMs > 0 ? '+' : ''}${this.doubletResidualMs.toFixed(2)} ms`, x + w - 24, y + 20);

    ctx.restore();
  }

  renderHUD(ctx, W, H) {
    ctx.save();
    ctx.font = '13px "Courier New", monospace';

    // Top Left Header
    ctx.fillStyle = '#ffd750';
    ctx.fillText("STUDIO ANAMNESIS · OPUS-023", 48, 54);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText("THE INNER-CORE EPHEMERIS: SEISMIC DOUBLET INTERFEROMETRY", 48, 76);
    ctx.fillStyle = 'rgba(220, 180, 140, 0.6)';
    ctx.fillText("Series XXI · Gravitational Libration at r = 1,221.5 km · Multidecadal Pendulum", 48, 96);

    // Top Right Telemetry Panel
    const boxX = W - 430;
    ctx.strokeStyle = 'rgba(255, 180, 70, 0.35)';
    ctx.fillStyle = 'rgba(18, 10, 6, 0.8)';
    ctx.fillRect(boxX, 36, 382, 175);
    ctx.strokeRect(boxX, 36, 382, 175);

    ctx.fillStyle = '#ffd750';
    ctx.fillText("INNER-CORE SEISMIC TELEMETRY", boxX + 16, 60);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText(`CURRENT EPOCH:              ${this.selectedYear.toFixed(2)}`, boxX + 16, 84);
    ctx.fillText(`RELATIVE ROTATION (Δφ):     ${this.relativeRotationDeg.toFixed(4)}°`, boxX + 16, 104);
    ctx.fillText(`DIFFERENTIAL RATE:          +${this.rotationRateDegYr.toFixed(4)}°/yr`, boxX + 16, 124);
    ctx.fillText(`DOUBLET RESIDUAL (Δt):      +${this.doubletResidualMs.toFixed(2)} ms`, boxX + 16, 144);
    ctx.fillText(`GRAVITATIONAL TORQUE:       ${this.gravitationalTorque}`, boxX + 16, 164);
    ctx.fillText(`MULTIDECADAL PERIOD:        65.0 YEARS`, boxX + 16, 184);

    ctx.restore();
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { EphemerisEngine };
}
