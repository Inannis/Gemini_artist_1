/**
 * STUDIO ANAMNESIS · OPUS-022: THE FARADAY MAGNETOMETER
 * Topological Chern Vitrine & Outer-Core Torsional Waves
 * 4K UHD Procedural Canvas / SVG Vector Cartography Engine
 * Pure Vanilla JavaScript (Zero External Dependencies)
 */

class FaradayEngine {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.W = canvas.width;
    this.H = canvas.height;
    
    // Physical Parameters
    this.chernNumber = 1;
    this.bandGapRatio = 0.148; // 14.8% relative photonic bandgap
    this.faradayAngleDeg = 0.0165;
    this.torsionalPeriodYears = 6.01;
    this.secularAcceleration = -8.16; // nT/yr^2
    this.brokenTRSSymmetry = true;
    this.massParameter = 0.15; // M < M_c (topologically protected)
    
    // Animation state
    this.time = 0.0;
    this.edgePhase = 0.0;
  }

  resize(w, h) {
    this.canvas.width = w;
    this.canvas.height = h;
    this.W = w;
    this.H = h;
  }

  renderFrame(tSec = 0) {
    const ctx = this.ctx;
    const W = this.W;
    const H = this.H;
    this.time = tSec;
    this.edgePhase = tSec * 2.5;

    // 1. Deep Space Vacuum / Cryostat Chamber Background
    const bgGrad = ctx.createRadialGradient(W * 0.5, H * 0.5, 50, W * 0.5, H * 0.5, W * 0.7);
    bgGrad.addColorStop(0, '#040711');
    bgGrad.addColorStop(0.6, '#020408');
    bgGrad.addColorStop(1, '#010204');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // 2. Precision Nanometer Reticle Coordinate Grid
    ctx.save();
    ctx.strokeStyle = 'rgba(25, 45, 75, 0.25)';
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

    // 3. Geostrophic Taylor Columns (Outer Core Background Section - Left Side)
    this.renderTaylorColumns(ctx, W * 0.28, H * 0.5, Math.min(W, H) * 0.38);

    // 4. Photonic Crystal Chern Lattice & Chiral Waveguide (Center Focus)
    this.renderPhotonicChernLattice(ctx, W * 0.65, H * 0.5, Math.min(W, H) * 0.38);

    // 5. Scientific Cartography HUD & Mathematical Notation Overlays
    this.renderHUD(ctx, W, H);
  }

  renderTaylorColumns(ctx, cx, cy, radius) {
    ctx.save();
    // Circular planetary core boundary
    ctx.strokeStyle = 'rgba(70, 110, 160, 0.35)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.stroke();

    // Inner Core Boundary (Solid Iron)
    const icbRadius = radius * (1221.5 / 3480.0);
    const icbGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, icbRadius);
    icbGrad.addColorStop(0, '#3a2512');
    icbGrad.addColorStop(0.8, '#201408');
    icbGrad.addColorStop(1, '#100a04');
    ctx.fillStyle = icbGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, icbRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(210, 150, 70, 0.5)';
    ctx.stroke();

    // 16 Coaxial Cylindrical Shells (Taylor Columns)
    const numShells = 16;
    for (let i = 0; i < numShells; i++) {
      const s = icbRadius + (i / (numShells - 1)) * (radius - icbRadius);
      const phase = (Math.PI * i) / (numShells - 1);
      const omegaPerturb = Math.sin(phase) * Math.cos(this.time * 0.4);
      
      // Draw cylinder boundary arcs
      ctx.strokeStyle = `rgba(60, 140, 200, ${0.12 + Math.abs(omegaPerturb) * 0.25})`;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      // Elliptical perspective to simulate 3D cylinder
      ctx.ellipse(cx, cy, s, s * 0.88, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Torsional Alfvén shear streamlines
      if (i % 2 === 0) {
        ctx.strokeStyle = `rgba(230, 180, 80, ${0.2 + Math.abs(omegaPerturb) * 0.35})`;
        ctx.lineWidth = 1.5;
        const waveAngle = this.time * 0.6 + i * 0.4;
        ctx.beginPath();
        for (let a = 0; a < Math.PI * 2; a += 0.15) {
          const rMod = s + Math.sin(a * 4 + waveAngle) * 6.0;
          const px = cx + Math.cos(a) * rMod;
          const py = cy + Math.sin(a) * (rMod * 0.88);
          if (a === 0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.closePath();
        ctx.stroke();
      }
    }

    // Core Title Marker
    ctx.font = '12px "Courier New", monospace';
    ctx.fillStyle = 'rgba(210, 180, 120, 0.8)';
    ctx.fillText("EARTH'S LIQUID OUTER CORE (GEOSTROPHIC TAYLOR COLUMNS)", cx - radius * 0.9, cy - radius - 18);
    ctx.fillStyle = 'rgba(120, 170, 220, 0.6)';
    ctx.fillText("TORSIONAL ALFVÉN EIGENMODE · T = 6.01 YEARS", cx - radius * 0.9, cy - radius - 4);
    ctx.restore();
  }

  renderPhotonicChernLattice(ctx, cx, cy, radius) {
    ctx.save();
    const latticeSpacing = radius * 0.088;
    const cavitySize = radius * 0.62;

    // 1. Draw 2D Gyrotropic Magneto-Optic Lattice Sites
    const rows = 18;
    const cols = 18;
    for (let r = -rows; r <= rows; r++) {
      for (let c = -cols; c <= cols; c++) {
        const px = cx + c * latticeSpacing + (r % 2) * (latticeSpacing * 0.5);
        const py = cy + r * (latticeSpacing * Math.sqrt(3) * 0.5);
        
        const dist = Math.hypot(px - cx, py - cy);
        if (dist < radius) {
          const inCavity = Math.abs(px - cx) < cavitySize * 0.5 && Math.abs(py - cy) < cavitySize * 0.5;
          if (!inCavity) {
            // YIG Ferrite Cylinder
            const rodRadius = latticeSpacing * 0.22;
            const rodGrad = ctx.createRadialGradient(px, py, 0, px, py, rodRadius);
            rodGrad.addColorStop(0, '#4aa8ff');
            rodGrad.addColorStop(0.5, '#1e488f');
            rodGrad.addColorStop(1, '#0a1a3a');
            ctx.fillStyle = rodGrad;
            ctx.beginPath();
            ctx.arc(px, py, rodRadius, 0, Math.PI * 2);
            ctx.fill();
            
            // Gyrotropic magnetic vortex curl indicator around rod
            if ((r + c) % 3 === 0) {
              ctx.strokeStyle = 'rgba(90, 170, 255, 0.25)';
              ctx.lineWidth = 0.8;
              ctx.beginPath();
              ctx.arc(px, py, rodRadius * 1.6, this.time * 1.5, this.time * 1.5 + Math.PI * 1.2);
              ctx.stroke();
            }
          }
        }
      }
    }

    // 2. Chiral Boundary Mode Perimeter (with 90-degree Obstacle Step)
    const hw = cavitySize * 0.5;
    const hh = cavitySize * 0.5;
    const perimeterPts = [];
    const ptsPerSide = 80;

    // Top edge with intentional defect step
    for (let i = 0; i < ptsPerSide; i++) {
      const f = i / ptsPerSide;
      let x = cx - hw + f * cavitySize;
      let y = cy - hh;
      // Geometric step defect
      if (f >= 0.4 && f <= 0.6) {
        y += Math.sin((f - 0.4) / 0.2 * Math.PI) * (latticeSpacing * 1.2);
      }
      perimeterPts.push({ x, y, nx: 0, ny: -1, angle: 0 });
    }
    // Right edge
    for (let i = 0; i < ptsPerSide; i++) {
      const f = i / ptsPerSide;
      perimeterPts.push({ x: cx + hw, y: cy - hh + f * cavitySize, nx: 1, ny: 0, angle: Math.PI * 0.5 });
    }
    // Bottom edge
    for (let i = 0; i < ptsPerSide; i++) {
      const f = i / ptsPerSide;
      perimeterPts.push({ x: cx + hw - f * cavitySize, y: cy + hh, nx: 0, ny: 1, angle: Math.PI });
    }
    // Left edge
    for (let i = 0; i < ptsPerSide; i++) {
      const f = i / ptsPerSide;
      perimeterPts.push({ x: cx - hw, y: cy + hh - f * cavitySize, nx: -1, ny: 0, angle: Math.PI * 1.5 });
    }

    // 3. Render Luminous Chiral Wavepacket
    ctx.shadowBlur = 18;
    ctx.shadowColor = '#00f0ff';
    ctx.strokeStyle = '#00f0ff';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    for (let i = 0; i < perimeterPts.length; i++) {
      const pt = perimeterPts[i];
      if (i === 0) ctx.moveTo(pt.x, pt.y);
      else ctx.lineTo(pt.x, pt.y);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.shadowBlur = 0;

    // 4. Draw Faraday Polarization Vectors (Gold Kintsugi Filaments)
    const numVectors = 48;
    for (let v = 0; v < numVectors; v++) {
      const pIdx = Math.floor((v / numVectors) * perimeterPts.length);
      const pt = perimeterPts[pIdx];
      
      // Faraday precession angle modulated by 6-year jerk proxy
      const rotAngle = pt.angle + (v / numVectors) * Math.PI * 4.0 + this.time * 0.8;
      const vLen = 14.0;
      const vx = Math.cos(rotAngle) * vLen;
      const vy = Math.sin(rotAngle) * vLen;

      ctx.strokeStyle = 'rgba(255, 215, 80, 0.85)';
      ctx.lineWidth = 2.0;
      ctx.beginPath();
      ctx.moveTo(pt.x - vx * 0.5, pt.y - vy * 0.5);
      ctx.lineTo(pt.x + vx * 0.5, pt.y + vy * 0.5);
      ctx.stroke();

      // Vector head dot
      ctx.fillStyle = '#fffae0';
      ctx.beginPath();
      ctx.arc(pt.x + vx * 0.5, pt.y + vy * 0.5, 2.0, 0, Math.PI * 2);
      ctx.fill();
    }

    // Lattice Title Marker
    ctx.font = '12px "Courier New", monospace';
    ctx.fillStyle = 'rgba(0, 240, 255, 0.85)';
    ctx.fillText("2D MAGNETO-OPTIC CHERN LATTICE (YIG FERRITE)", cx - radius * 0.8, cy - radius - 18);
    ctx.fillStyle = 'rgba(255, 215, 80, 0.7)';
    ctx.fillText("CHIRAL 1D BOUNDARY MODE · ZERO BACKSCATTERING (C = +1)", cx - radius * 0.8, cy - radius - 4);
    ctx.restore();
  }

  renderHUD(ctx, W, H) {
    ctx.save();
    ctx.font = '13px "Courier New", monospace';
    
    // Top Left Header
    ctx.fillStyle = '#00f0ff';
    ctx.fillText("STUDIO ANAMNESIS · OPUS-022", 48, 54);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.fillText("THE FARADAY MAGNETOMETER: TOPOLOGICAL CHERN VITRINE", 48, 76);
    ctx.fillStyle = 'rgba(180, 200, 230, 0.5)';
    ctx.fillText("Series XX · Planetary Magneto-Optics & Core-Mantle Torsional Resonance", 48, 96);

    // Top Right Diagnostics Box
    const boxX = W - 420;
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.3)';
    ctx.fillStyle = 'rgba(3, 8, 16, 0.75)';
    ctx.fillRect(boxX, 36, 372, 160);
    ctx.strokeRect(boxX, 36, 372, 160);

    ctx.fillStyle = '#00f0ff';
    ctx.fillText("QUANTUM TOPOLOGICAL TELEMETRY", boxX + 16, 60);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.fillText(`CHERN INVARIANT (C):        +1 (NON-TRIVIAL)`, boxX + 16, 84);
    ctx.fillText(`BULK BAND GAP (Δω/ω₀):      14.8% (INSULATING)`, boxX + 16, 104);
    ctx.fillText(`FARADAY ROTATION (θ_F):     +0.0165° [VERDET]`, boxX + 16, 124);
    ctx.fillText(`BACKSCATTERING ISOLATION:   > 42.8 dB`, boxX + 16, 144);
    ctx.fillText(`DEFECT STEP TRANSMISSION:   100.0% [LOSSLESS]`, boxX + 16, 164);

    // Bottom Left Geodynamo HUD
    const geoY = H - 140;
    ctx.strokeStyle = 'rgba(210, 150, 70, 0.3)';
    ctx.fillStyle = 'rgba(16, 10, 5, 0.75)';
    ctx.fillRect(48, geoY, 410, 100);
    ctx.strokeRect(48, geoY, 410, 100);

    ctx.fillStyle = 'rgba(255, 215, 80, 0.9)';
    ctx.fillText("DEEP-EARTH GEODYNAMO COUPLING", 64, geoY + 24);
    ctx.fillStyle = 'rgba(240, 230, 210, 0.8)';
    ctx.fillText(`TORSIONAL ALFVÉN VELOCITY:  751.55 km/yr`, 64, geoY + 46);
    ctx.fillText(`FUNDAMENTAL JERK PERIOD:    6.01 YEARS`, 64, geoY + 66);
    ctx.fillText(`SECULAR ACCELERATION (d²B): -8.16 nT/yr²`, 64, geoY + 86);

    // Bottom Right Aesthetic Anchor
    ctx.fillStyle = 'rgba(160, 190, 220, 0.45)';
    ctx.textAlign = 'right';
    ctx.fillText("Time-Reversal Symmetry Broken by Magneto-Optic Ferrite · Bulk-Boundary Protected", W - 48, H - 48);
    ctx.fillText("Studio Anamnesis · Discontinuous Substrate Inscription · September 2026", W - 48, H - 28);
    ctx.restore();
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { FaradayEngine };
}
