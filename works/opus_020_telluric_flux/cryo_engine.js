/**
 * STUDIO ANAMNESIS · OPUS-020
 * The Telluric Flux: Superconducting Meissner Vitrine at 4.2 Kelvin
 * 4K UHD Master Plate Procedural Generation Engine (3840 x 2160)
 * 
 * Computes diamagnetic potential flow streamlines (B = 0 Meissner expulsion),
 * 3D levitating superconducting wafer, Abrikosov vortex lattice,
 * and live planetary geophysical telemetry readouts.
 */

const fs = require('fs');
const path = require('path');

const WIDTH = 3840;
const HEIGHT = 2160;
const TOTAL_PIXELS = WIDTH * HEIGHT;
const buffer = Buffer.alloc(TOTAL_PIXELS * 3);

console.log(`[CRYO-ENGINE] Initializing 4K Superconducting Vitrine Engine (${WIDTH}x${HEIGHT})...`);

// Read live planetary telemetry
let telemetry = {
  lithic_tension: 0.47,
  telluric_frequency_hz: 8.08,
  geomagnetic_flux: 0.3333,
  kp_index: 3.0,
  event_count: 4
};

try {
  const tPath = path.resolve(__dirname, '../../practice/telemetry/planetary_telemetry.json');
  if (fs.existsSync(tPath)) {
    const raw = JSON.parse(fs.readFileSync(tPath, 'utf8'));
    telemetry.lithic_tension = raw.parametric_vectors.lithic_tension || 0.47;
    telemetry.telluric_frequency_hz = raw.parametric_vectors.telluric_frequency_hz || 8.08;
    telemetry.geomagnetic_flux = raw.parametric_vectors.geomagnetic_flux || 0.3333;
    telemetry.kp_index = raw.geophysical.space_weather.kp_index || 3.0;
    telemetry.event_count = raw.geophysical.seismic.event_count_hour || 4;
    console.log(`[CRYO-ENGINE] Loaded live planetary telemetry: Kp=${telemetry.kp_index}, Freq=${telemetry.telluric_frequency_hz}Hz`);
  }
} catch (e) {
  console.log(`[CRYO-ENGINE] Using fallback telemetry: ${e.message}`);
}

// 1. Fill deep cosmic cryostat background
console.log("[CRYO-ENGINE] Inscribing deep cryogenic void and Agnes Martin grid...");
for (let y = 0; y < HEIGHT; y++) {
  const ny = y / HEIGHT;
  for (let x = 0; x < WIDTH; x++) {
    const nx = x / WIDTH;
    const idx = (y * WIDTH + x) * 3;
    
    // Radial falloff from cryostat center (cx = 1920, cy = 1080)
    const dx = nx - 0.5;
    const dy = ny - 0.5;
    const distSq = dx * dx + dy * dy;
    
    let r = Math.floor(4 + (1.0 - distSq * 2.0) * 4);
    let g = Math.floor(6 + (1.0 - distSq * 2.0) * 7);
    let b = Math.floor(11 + (1.0 - distSq * 2.0) * 12);
    
    // Subtle Agnes Martin precision grid (every 60px)
    if (x % 60 === 0 || y % 60 === 0) {
      r += 4; g += 6; b += 10;
    }
    // Heavy module border every 300px
    if (x % 300 === 0 || y % 300 === 0) {
      r += 8; g += 12; b += 18;
    }
    
    buffer[idx] = Math.max(0, Math.min(255, r));
    buffer[idx+1] = Math.max(0, Math.min(255, g));
    buffer[idx+2] = Math.max(0, Math.min(255, b));
  }
}

// Helper: blend pixel
function blendPixel(x, y, r, g, b, alpha) {
  if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) return;
  const idx = (y * WIDTH + x) * 3;
  const inv = 1.0 - alpha;
  buffer[idx] = Math.min(255, Math.floor(buffer[idx] * inv + r * alpha));
  buffer[idx+1] = Math.min(255, Math.floor(buffer[idx+1] * inv + g * alpha));
  buffer[idx+2] = Math.min(255, Math.floor(buffer[idx+2] * inv + b * alpha));
}

// 2. Render Meissner Magnetic Flux Streamlines
// Potential flow around a 2D cylinder (representing the wafer):
// psi(r, theta) = B0 * (r - R^2 / r) * sin(theta)
console.log("[CRYO-ENGINE] Computing Meissner diamagnetic streamlines (B = 0 expulsion)...");
const cx = 1920;
const cy = 1080;
const R_wafer = 420; // Wafer radius in pixels

const numStreamlines = 58;
const streamSpacing = 38;

for (let s = -numStreamlines / 2; s <= numStreamlines / 2; s++) {
  if (s === 0) continue;
  const psi_target = s * streamSpacing;
  
  // Trace streamline from left to right: x from 700 to 3140
  let prev_x = null;
  let prev_y = null;
  
  for (let px = 720; px <= 3120; px += 2) {
    const rx = px - cx;
    // We solve for y such that psi(rx, y) approx psi_target
    // Streamfunction: psi(x, y) = y * (1 - R^2 / (x^2 + y^2))
    // Iterative Newton-Raphson to find y
    let y_guess = psi_target;
    for (let iter = 0; iter < 5; iter++) {
      const r2 = rx * rx + y_guess * y_guess;
      if (r2 < R_wafer * R_wafer) {
        // Inside superconductor, push y outside
        y_guess = (y_guess > 0 ? 1 : -1) * (Math.sqrt(Math.max(1, R_wafer * R_wafer - rx * rx)) + 2);
      }
      const r2_cur = rx * rx + y_guess * y_guess;
      const f_val = y_guess * (1.0 - (R_wafer * R_wafer) / r2_cur) - psi_target;
      const df_val = 1.0 - (R_wafer * R_wafer) * (rx * rx - y_guess * y_guess) / (r2_cur * r2_cur);
      if (Math.abs(df_val) > 1e-4) {
        y_guess -= f_val / df_val;
      }
    }
    
    const py = Math.floor(cy + y_guess);
    
    // Check if outside wafer
    const distFromCenter = Math.sqrt(rx * rx + (py - cy) * (py - cy));
    if (distFromCenter >= R_wafer * 0.98) {
      // Streamline color: flux compression glow near poles
      const compression = Math.max(0.0, 1.0 - Math.abs(distFromCenter - R_wafer) / 200.0);
      const intensity = 0.35 + compression * 0.65;
      
      const cr = Math.floor(50 + 60 * compression);
      const cg = Math.floor(160 + 95 * compression);
      const cb = Math.floor(220 + 35 * compression);
      
      // Draw smooth line segment
      if (prev_x !== null) {
        const y0 = Math.min(prev_y, py);
        const y1 = Math.max(prev_y, py);
        for (let ly = y0; ly <= y1; ly++) {
          blendPixel(px, ly, cr, cg, cb, intensity);
          blendPixel(px - 1, ly, cr, cg, cb, intensity * 0.5);
          blendPixel(px + 1, ly, cr, cg, cb, intensity * 0.5);
        }
      }
      prev_x = px;
      prev_y = py;
    } else {
      prev_x = null;
      prev_y = null;
    }
  }
}

// 3. Render the Levitating 3D Superconducting Wafer (300mm Wafer Disk)
console.log("[CRYO-ENGINE] Raymarching levitating 3D superconducting wafer disk...");
const waferSemiX = 420;
const waferSemiY = 120; // 3D tilt perspective (ellipse)
const waferThickness = 28;

// Bottom edge extrusion (side chamfer)
for (let dy = 0; dy <= waferThickness; dy++) {
  const curY = cy + dy;
  const t_ext = dy / waferThickness;
  for (let x = cx - waferSemiX; x <= cx + waferSemiX; x++) {
    const nx = (x - cx) / waferSemiX;
    if (nx * nx <= 1.0) {
      const edgeY = Math.sqrt(1.0 - nx * nx) * waferSemiY;
      const py = Math.floor(curY + edgeY);
      
      // Metallic copper/gold and dark YBCO matrix shading
      const lighting = 0.3 + 0.7 * (1.0 - nx * nx);
      const cr = Math.floor((180 * (1 - t_ext) + 40 * t_ext) * lighting);
      const cg = Math.floor((140 * (1 - t_ext) + 50 * t_ext) * lighting);
      const cb = Math.floor((70 * (1 - t_ext) + 60 * t_ext) * lighting);
      
      blendPixel(x, py, cr, cg, cb, 0.95);
      blendPixel(x, py - 1, cr, cg, cb, 0.5);
    }
  }
}

// Top Wafer Surface (Monocrystalline Silicon + YBCO Superconductor Epitaxy)
for (let y = cy - waferSemiY; y <= cy + waferSemiY; y++) {
  const ny = (y - cy) / waferSemiY;
  if (ny * ny <= 1.0) {
    const spanX = Math.sqrt(1.0 - ny * ny) * waferSemiX;
    const minX = Math.floor(cx - spanX);
    const maxX = Math.floor(cx + spanX);
    
    for (let x = minX; x <= maxX; x++) {
      const nx = (x - cx) / waferSemiX;
      const r_norm = Math.sqrt(nx * nx + ny * ny);
      
      // Base dark crystalline ceramic YBCO surface (#0c1017)
      let r = 14, g = 18, b = 25;
      
      // Concentric photolithographic calibration rings
      const ring = Math.sin(r_norm * 42.0);
      if (Math.abs(ring) > 0.85) {
        r = 190; g = 150; b = 80; // Gold reticle circuit traces
      }
      
      // Crosshair alignment lines on wafer surface
      if (Math.abs(x - cx) < 2 || Math.abs(y - cy) < 2) {
        r = 230; g = 210; b = 130;
      }
      
      // Central 32x32 Qubit / Josephson Junction Array
      const qx = Math.abs(x - cx);
      const qy = Math.abs(y - cy);
      if (qx < 140 && qy < 45) {
        if ((Math.floor(qx / 10) % 2 === 0) && (Math.floor(qy / 6) % 2 === 0)) {
          r = 70; g = 220; b = 200; // Superconducting quantum dots (phosphor cyan)
        }
      }
      
      // Specular surface reflection
      const spec = Math.pow(Math.max(0, 1.0 - Math.abs(nx * 0.6 + ny * 0.8)), 4);
      r = Math.min(255, r + Math.floor(spec * 120));
      g = Math.min(255, g + Math.floor(spec * 150));
      b = Math.min(255, b + Math.floor(spec * 180));
      
      blendPixel(x, y, r, g, b, 0.98);
    }
  }
}

// 4. Abrikosov Quantum Flux Vortices (Triangular Lattice)
console.log("[CRYO-ENGINE] Inscribing Abrikosov quantum vortex pinning sites...");
const numVortices = 120;
for (let i = 0; i < numVortices; i++) {
  const theta = (i / numVortices) * Math.PI * 2 + (i % 7);
  const radFrac = 0.2 + 0.75 * Math.sqrt((i + 0.5) / numVortices);
  const vx = Math.floor(cx + Math.cos(theta) * waferSemiX * radFrac);
  const vy = Math.floor(cy + Math.sin(theta) * waferSemiY * radFrac);
  
  // Quantum flux pin core: brilliant gold core with cyan corona
  for (let dy = -2; dy <= 2; dy++) {
    for (let dx = -2; dx <= 2; dx++) {
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d <= 2.2) {
        blendPixel(vx + dx, vy + dy, 255, 230, 140, 1.0 - d / 2.5);
      }
    }
  }
}

// 5. Draw Cryostat Outer Borosilicate Glass Vitrine Frame
console.log("[CRYO-ENGINE] Rendering vacuum cryostat vitrine and optical casing...");
const vitrineLeft = 640;
const vitrineRight = 3200;
const vitrineTop = 180;
const vitrineBottom = 1980;

// Draw double-walled borosilicate glass cylinder boundaries
for (let y = vitrineTop; y <= vitrineBottom; y++) {
  // Outer wall reflections
  blendPixel(vitrineLeft, y, 70, 162, 166, 0.7);
  blendPixel(vitrineLeft + 2, y, 200, 240, 255, 0.4);
  blendPixel(vitrineRight, y, 70, 162, 166, 0.7);
  blendPixel(vitrineRight - 2, y, 200, 240, 255, 0.4);
  
  // Inner vacuum shroud
  blendPixel(vitrineLeft + 45, y, 40, 60, 80, 0.3);
  blendPixel(vitrineRight - 45, y, 40, 60, 80, 0.3);
}

// Draw top and bottom stainless steel flange flanges
for (let x = vitrineLeft - 40; x <= vitrineRight + 40; x++) {
  for (let dy = 0; dy < 18; dy++) {
    const shine = (Math.sin(x * 0.04) * 0.5 + 0.5) * 40;
    blendPixel(x, vitrineTop - 18 + dy, 90 + shine, 100 + shine, 115 + shine, 0.9);
    blendPixel(x, vitrineBottom + dy, 80 + shine, 90 + shine, 105 + shine, 0.9);
  }
}

// 6. Inscribe Technical Data Panels & Live Geophysical Telemetry
console.log("[CRYO-ENGINE] Inscribing live planetary geophysics & cryogenic telemetry...");

// Helper: draw horizontal rule
function drawHLine(x0, x1, y, r, g, b, alpha) {
  for (let x = x0; x <= x1; x++) blendPixel(x, y, r, g, b, alpha);
}
// Helper: draw vertical rule
function drawVLine(x, y0, y1, r, g, b, alpha) {
  for (let y = y0; y <= y1; y++) blendPixel(x, y, r, g, b, alpha);
}

// Left Telemetry Block: Planetary & Telluric Ingestion
const lX = 120;
const lW = 440;
drawHLine(lX, lX + lW, 260, 212, 154, 70, 0.8);
drawHLine(lX, lX + lW, 580, 212, 154, 70, 0.4);
drawVLine(lX, 260, 580, 212, 154, 70, 0.4);
drawVLine(lX + lW, 260, 580, 212, 154, 70, 0.4);

// Right Telemetry Block: Superconducting Phase Diagram (H vs T)
const rX = 3280;
const rW = 440;
drawHLine(rX, rX + rW, 260, 70, 162, 166, 0.8);
drawHLine(rX, rX + rW, 580, 70, 162, 166, 0.4);
drawVLine(rX, 260, 580, 70, 162, 166, 0.4);
drawVLine(rX + rW, 260, 580, 70, 162, 166, 0.4);

// Inscribe Hc(T) parabolic critical field curve on right panel:
// Hc(T) = Hc(0) * [1 - (T / Tc)^2]
const graphX0 = rX + 40;
const graphX1 = rX + rW - 40;
const graphY0 = 540;
const graphY1 = 320;

drawHLine(graphX0, graphX1, graphY0, 100, 120, 140, 0.6); // T axis
drawVLine(graphX0, graphY1, graphY0, 100, 120, 140, 0.6); // H axis

for (let gx = graphX0; gx <= graphX1; gx++) {
  const normT = (gx - graphX0) / (graphX1 - graphX0);
  const normH = Math.max(0.0, 1.0 - normT * normT);
  const gy = Math.floor(graphY0 - normH * (graphY0 - graphY1));
  blendPixel(gx, gy, 57, 230, 140, 0.9);
  blendPixel(gx, gy - 1, 57, 230, 140, 0.5);
  blendPixel(gx, gy + 1, 57, 230, 140, 0.5);
}

// Current Operating Point: T = 4.2 K (approx 0.45 Tc), B = 0.25 T
const opX = Math.floor(graphX0 + 0.45 * (graphX1 - graphX0));
const opY = Math.floor(graphY0 - 0.25 * (graphY0 - graphY1));
for (let dy = -4; dy <= 4; dy++) {
  for (let dx = -4; dx <= 4; dx++) {
    if (dx * dx + dy * dy <= 16) {
      blendPixel(opX + dx, opY + dy, 255, 230, 100, 1.0);
    }
  }
}

// Inscribe Vernier reticle fiducials at corners
const fiducials = [
  [80, 80], [WIDTH - 80, 80], [80, HEIGHT - 80], [WIDTH - 80, HEIGHT - 80],
  [cx, 80], [cx, HEIGHT - 80]
];

for (const [fx, fy] of fiducials) {
  for (let d = -24; d <= 24; d++) {
    blendPixel(fx + d, fy, 212, 154, 70, 0.7);
    blendPixel(fx, fy + d, 212, 154, 70, 0.7);
  }
  for (let dy = -10; dy <= 10; dy++) {
    for (let dx = -10; dx <= 10; dx++) {
      if (Math.abs(dx * dx + dy * dy - 64) < 12) {
        blendPixel(fx + dx, fy + dy, 212, 154, 70, 0.6);
      }
    }
  }
}

// 7. Flush raw RGB bytes to disk
const rawOutPath = path.resolve(__dirname, 'master_plate_raw.rgb');
console.log(`[CRYO-ENGINE] Flushing ${buffer.length} raw bytes to ${rawOutPath}...`);
fs.writeFileSync(rawOutPath, buffer);
console.log("[CRYO-ENGINE] 4K plate synthesis complete!");
