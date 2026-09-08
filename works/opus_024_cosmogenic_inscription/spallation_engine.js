/**
 * STUDIO ANAMNESIS · OPUS-024: THE COSMOGENIC INSCRIPTION
 * Atmospheric Hadronic Cascades & Semiconductor Single-Event Upsets
 * 4K UHD Procedural Canvas / SVG Vector Cartography Engine
 * Pure Vanilla JavaScript (Zero External Dependencies)
 */

class SpallationEngine {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.W = canvas.width;
    this.H = canvas.height;

    // Physical Telemetry Parameters
    this.altitudeMeters = 408.0;
    this.atmosphericDepth = 984.2; // g/cm^2
    this.scalingFactor = 1.385;
    this.neutronFluxPerHour = 50.88;
    this.muonFluxPerMin = 0.88;
    this.criticalChargeFc = 1.25;
    this.collectedChargeFc = 1.42;
    this.bitState = 0; // 0 or 1
    this.be10Concentration = "2.62e+05";
    this.time = 0.0;

    // Particles array for EAS shower
    this.particles = [];
    this.initShower();
  }

  resize(w, h) {
    this.canvas.width = w;
    this.canvas.height = h;
    this.W = w;
    this.H = h;
  }

  setAltitude(altM) {
    this.altitudeMeters = altM;
    const scaleHeight = 8430.0;
    this.atmosphericDepth = 1033.0 * Math.exp(-altM / scaleHeight);
    this.scalingFactor = Math.exp((1033.0 - this.atmosphericDepth) / 150.0);
    this.neutronFluxPerHour = 36.7 * this.scalingFactor;
    this.muonFluxPerMin = 0.63 * (1.0 + 0.18 * (altM / 1000.0));
  }

  triggerSpallation() {
    this.collectedChargeFc = 1.25 + Math.random() * 2.8;
    if (this.collectedChargeFc >= this.criticalChargeFc) {
      this.bitState = 1 - this.bitState; // Flip bit
    }
    this.initShower(true);
  }

  initShower(burst = false) {
    this.particles = [];
    const count = burst ? 180 : 80;
    const originX = this.W * 0.5;
    const originY = this.H * 0.08;

    for (let i = 0; i < count; i++) {
      const angle = Math.PI * 0.5 + (Math.random() - 0.5) * 0.85;
      const speed = 2.0 + Math.random() * 5.0;
      this.particles.push({
        x: originX,
        y: originY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        type: Math.random() < 0.4 ? 'muon' : (Math.random() < 0.7 ? 'neutron' : 'gamma'),
        life: 0.0,
        maxLife: 40.0 + Math.random() * 80.0
      });
    }
  }

  renderFrame(tSec = 0) {
    const ctx = this.ctx;
    const W = this.W;
    const H = this.H;
    this.time = tSec;

    // 1. Celestial Void & Upper Atmosphere Stratification
    const bgGrad = ctx.createLinearGradient(0, 0, 0, H);
    bgGrad.addColorStop(0, '#040208');
    bgGrad.addColorStop(0.35, '#070514');
    bgGrad.addColorStop(0.65, '#0c0e18');
    bgGrad.addColorStop(1, '#05070a');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // Coordinate grid lines
    ctx.save();
    ctx.strokeStyle = 'rgba(120, 140, 200, 0.12)';
    ctx.lineWidth = 1;
    const step = Math.floor(W / 40);
    for (let x = 0; x < W; x += step) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, H);
      ctx.stroke();
    }
    for (let y = 0; y < H; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }
    ctx.restore();

    // 2. Render Atmospheric Hadronic Shower (Top 55% of canvas)
    this.renderHadronicShower(ctx, W, H);

    // 3. Render Terrestrial Quartz Bedrock (Lower Left 40% of canvas)
    this.renderQuartzBedrock(ctx, W * 0.08, H * 0.58, W * 0.40, H * 0.32);

    // 4. Render 3nm FinFET Logic Gate & Bit Flip (Lower Right 40% of canvas)
    this.renderFinFETGate(ctx, W * 0.52, H * 0.58, W * 0.40, H * 0.32);

    // 5. Scientific Cartography HUD
    this.renderHUD(ctx, W, H);
  }

  renderHadronicShower(ctx, W, H) {
    ctx.save();
    const originX = W * 0.5;
    const originY = H * 0.08;

    // Primary Cosmic Proton Ray (Incoming from deep space)
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(originX - 60, 0);
    ctx.lineTo(originX, originY);
    ctx.stroke();

    // Primary Impact Fireball
    const fireGrad = ctx.createRadialGradient(originX, originY, 0, originX, originY, 28);
    fireGrad.addColorStop(0, '#ffffff');
    fireGrad.addColorStop(0.4, '#ffaa33');
    fireGrad.addColorStop(0.8, '#ff3366');
    fireGrad.addColorStop(1, 'transparent');
    ctx.fillStyle = fireGrad;
    ctx.beginPath();
    ctx.arc(originX, originY, 28, 0, Math.PI * 2);
    ctx.fill();

    // Update and draw shower cascade particles
    for (let p of this.particles) {
      p.x += p.vx;
      p.y += p.vy;
      p.life += 1.0;

      const alpha = Math.max(0, 1.0 - p.life / p.maxLife);
      if (p.type === 'muon') {
        ctx.strokeStyle = `rgba(220, 240, 255, ${alpha * 0.8})`;
        ctx.lineWidth = 1.5;
      } else if (p.type === 'neutron') {
        ctx.strokeStyle = `rgba(255, 180, 50, ${alpha * 0.9})`;
        ctx.lineWidth = 2.0;
      } else {
        ctx.strokeStyle = `rgba(180, 100, 255, ${alpha * 0.6})`;
        ctx.lineWidth = 1.0;
      }

      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.x - p.vx * 3.0, p.y - p.vy * 3.0);
      ctx.stroke();
    }

    // Occasional regeneration of particles to sustain live cascade
    if (Math.random() < 0.25) {
      const angle = Math.PI * 0.5 + (Math.random() - 0.5) * 0.85;
      const speed = 2.0 + Math.random() * 4.5;
      this.particles.push({
        x: originX + (Math.random() - 0.5) * 15,
        y: originY + (Math.random() - 0.5) * 10,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        type: Math.random() < 0.4 ? 'muon' : (Math.random() < 0.7 ? 'neutron' : 'gamma'),
        life: 0.0,
        maxLife: 40.0 + Math.random() * 80.0
      });
    }

    ctx.restore();
  }

  renderQuartzBedrock(ctx, x, y, w, h) {
    ctx.save();
    // Frame
    ctx.fillStyle = 'rgba(12, 16, 24, 0.85)';
    ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = 'rgba(100, 220, 200, 0.35)';
    ctx.strokeRect(x, y, w, h);

    // Section Title
    ctx.fillStyle = '#64dfdf';
    ctx.font = 'bold 11px monospace';
    ctx.fillText('LITHIC SUBSTRATE · COSMOGENIC ¹⁰Be ACCUMULATION', x + 12, y + 20);

    // Mountain Granite/Quartz Face
    ctx.strokeStyle = '#48cae4';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(x + 20, y + h - 30);
    ctx.lineTo(x + w * 0.3, y + h * 0.35);
    ctx.lineTo(x + w * 0.6, y + h * 0.5);
    ctx.lineTo(x + w - 20, y + h * 0.25);
    ctx.lineTo(x + w - 20, y + h - 30);
    ctx.closePath();
    ctx.fillStyle = 'rgba(20, 35, 45, 0.8)';
    ctx.fill();
    ctx.stroke();

    // In-situ Cosmogenic Isotope Atoms (Glowing turquoise dots)
    ctx.fillStyle = '#72efdd';
    for (let i = 0; i < 40; i++) {
      const px = x + 40 + (i * 19.3) % (w - 80);
      const py = y + h * 0.45 + (i * 13.7) % (h * 0.4);
      ctx.beginPath();
      ctx.arc(px, py, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.fillStyle = 'rgba(200, 240, 235, 0.75)';
    ctx.font = '10px monospace';
    ctx.fillText('Target Mineral: Quartz (SiO₂)', x + 16, y + h - 12);
    ctx.fillText(`N(¹⁰Be) = ${this.be10Concentration} atoms/g`, x + w * 0.45, y + h - 12);
    ctx.restore();
  }

  renderFinFETGate(ctx, x, y, w, h) {
    ctx.save();
    // Frame
    ctx.fillStyle = 'rgba(16, 12, 18, 0.85)';
    ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = 'rgba(255, 175, 75, 0.35)';
    ctx.strokeRect(x, y, w, h);

    // Section Title
    ctx.fillStyle = '#ffb703';
    ctx.font = 'bold 11px monospace';
    ctx.fillText('SILICON SUBSTRATE · 3nm FinFET SINGLE-EVENT UPSET', x + 12, y + 20);

    // 3D FinFET Transistor representation
    const finX = x + w * 0.5;
    const finY = y + h * 0.52;
    const finW = w * 0.6;
    const finH = h * 0.35;

    // Silicon Substrate Base
    ctx.fillStyle = '#1c1724';
    ctx.fillRect(finX - finW/2, finY - finH/2, finW, finH);
    ctx.strokeStyle = '#4a3d5e';
    ctx.strokeRect(finX - finW/2, finY - finH/2, finW, finH);

    // Source / Drain Terminals
    ctx.fillStyle = '#3a5a40';
    ctx.fillRect(finX - finW/2 + 10, finY - finH/2 + 10, 45, finH - 20);
    ctx.fillRect(finX + finW/2 - 55, finY - finH/2 + 10, 45, finH - 20);

    // Gate Oxide & Fin (Center)
    const isFlipped = this.bitState === 1;
    ctx.fillStyle = isFlipped ? '#d90429' : '#0077b6';
    ctx.fillRect(finX - 25, finY - finH/2 - 15, 50, finH + 30);
    ctx.strokeStyle = isFlipped ? '#ff4d6d' : '#90e0ef';
    ctx.lineWidth = 2;
    ctx.strokeRect(finX - 25, finY - finH/2 - 15, 50, finH + 30);

    // State Readout Display
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 24px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`BIT: [ ${this.bitState} ]`, finX, finY + 8);
    ctx.textAlign = 'left';

    ctx.fillStyle = 'rgba(255, 230, 200, 0.8)';
    ctx.font = '10px monospace';
    ctx.fillText(`Collected Charge: ${this.collectedChargeFc.toFixed(2)} fC`, x + 16, y + h - 12);
    ctx.fillText(`Critical Qc: ${this.criticalChargeFc.toFixed(2)} fC`, x + w * 0.55, y + h - 12);
    ctx.restore();
  }

  renderHUD(ctx, W, H) {
    ctx.save();
    // Border Cartography
    ctx.strokeStyle = 'rgba(180, 200, 240, 0.4)';
    ctx.lineWidth = 1;
    ctx.strokeRect(40, 40, W - 80, H - 80);

    // Corner brackets
    const bLen = 20;
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#ffb703';
    // Top-left
    ctx.beginPath(); ctx.moveTo(40, 40 + bLen); ctx.lineTo(40, 40); ctx.lineTo(40 + bLen, 40); ctx.stroke();
    // Top-right
    ctx.beginPath(); ctx.moveTo(W - 40 - bLen, 40); ctx.lineTo(W - 40, 40); ctx.lineTo(W - 40, 40 + bLen); ctx.stroke();
    // Bottom-left
    ctx.beginPath(); ctx.moveTo(40, H - 40 - bLen); ctx.lineTo(40, H - 40); ctx.lineTo(40 + bLen, H - 40); ctx.stroke();
    // Bottom-right
    ctx.beginPath(); ctx.moveTo(W - 40 - bLen, H - 40); ctx.lineTo(W - 40, H - 40); ctx.lineTo(W - 40, H - 40 - bLen); ctx.stroke();
    ctx.restore();
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SpallationEngine };
}
