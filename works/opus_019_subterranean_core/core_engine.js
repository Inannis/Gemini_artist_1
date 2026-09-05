/**
 * STUDIO ANAMNESIS · MONUMENTAL GENERATIVE ENGINE
 * OPUS-019: The Subterranean Core (Borehole Radiometry at -500 Meters)
 * 
 * Generates raw RGB byte buffer for 3840 x 2160 UHD master plate:
 * - Cylindrical diamond drill core sample with 3D ray-normal raking illumination
 * - 5 distinct geological horizons including the synthetic Techno-Fossil stratum
 * - Van Eck RF memory bus waterfall radiometry spectrogram
 * - Cartographic coordinate grids, seismic impedance curves, and lithic telemetry
 */

const fs = require('fs');
const path = require('path');

const WIDTH = 3840;
const HEIGHT = 2160;

console.log(`[CORE-ENGINE] Initializing 4K Subterranean Stratigraphy Engine (${WIDTH}x${HEIGHT})...`);

const buffer = Buffer.alloc(WIDTH * HEIGHT * 3);

// Helper: Pseudo-random noise generator (Simplex / FBM surrogate)
function hash(x, y) {
  let n = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453123;
  return n - Math.floor(n);
}

function smoothNoise(x, y) {
  const i = Math.floor(x);
  const j = Math.floor(y);
  const fx = x - i;
  const fy = y - j;

  const s = fx * fx * (3 - 2 * fx);
  const t = fy * fy * (3 - 2 * fy);

  const n00 = hash(i, j);
  const n10 = hash(i + 1, j);
  const n01 = hash(i, j + 1);
  const n11 = hash(i + 1, j + 1);

  const nx0 = n00 * (1 - s) + n10 * s;
  const nx1 = n01 * (1 - s) + n11 * s;

  return nx0 * (1 - t) + nx1 * t;
}

function fbm(x, y, octaves = 5) {
  let val = 0;
  let amp = 0.5;
  let freq = 1.0;
  for (let o = 0; o < octaves; o++) {
    val += amp * smoothNoise(x * freq, y * freq);
    freq *= 2.05;
    amp *= 0.5;
  }
  return val;
}

function setPixel(x, y, r, g, b, alpha = 1.0) {
  if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) return;
  const idx = (y * WIDTH + x) * 3;
  buffer[idx] = Math.min(255, Math.max(0, Math.floor(buffer[idx] * (1 - alpha) + r * alpha)));
  buffer[idx + 1] = Math.min(255, Math.max(0, Math.floor(buffer[idx + 1] * (1 - alpha) + g * alpha)));
  buffer[idx + 2] = Math.min(255, Math.max(0, Math.floor(buffer[idx + 2] * (1 - alpha) + b * alpha)));
}

function drawLine(x0, y0, x1, y1, r, g, b, alpha = 1.0, width = 1) {
  const dx = Math.abs(x1 - x0);
  const dy = Math.abs(y1 - y0);
  const sx = x0 < x1 ? 1 : -1;
  const sy = y0 < y1 ? 1 : -1;
  let err = dx - dy;

  while (true) {
    for (let wy = -Math.floor(width / 2); wy <= Math.floor(width / 2); wy++) {
      for (let wx = -Math.floor(width / 2); wx <= Math.floor(width / 2); wx++) {
        setPixel(x0 + wx, y0 + wy, r, g, b, alpha);
      }
    }
    if (x0 === x1 && y0 === y1) break;
    const e2 = 2 * err;
    if (e2 > -dy) {
      err -= dy;
      x0 += sx;
    }
    if (e2 < dx) {
      err += dx;
      y0 += sy;
    }
  }
}

// 1. Background Fill: Deep Abyssal Slate (#07090e)
console.log("[CORE-ENGINE] Inscribing abyssal ground and Agnes Martin grid...");
for (let y = 0; y < HEIGHT; y++) {
  for (let x = 0; x < WIDTH; x++) {
    const idx = (y * WIDTH + x) * 3;
    buffer[idx] = 7;
    buffer[idx + 1] = 9;
    buffer[idx + 2] = 14;

    // Faint Agnes Martin coordinate grid (every 60px)
    if (x % 60 === 0 || y % 60 === 0) {
      buffer[idx] = 14;
      buffer[idx + 1] = 18;
      buffer[idx + 2] = 26;
    }
  }
}

// 2. Render Left Panel: Van Eck RF Waterfall Spectrogram (x = 160 to 1240, y = 140 to 2020)
console.log("[CORE-ENGINE] Rendering Van Eck RF memory bus waterfall spectrogram...");
const wfX0 = 160, wfX1 = 1240, wfY0 = 140, wfY1 = 2020;
const wfWidth = wfX1 - wfX0;
const wfHeight = wfY1 - wfY0;

// Border for RF Waterfall
drawLine(wfX0 - 2, wfY0 - 2, wfX1 + 2, wfY0 - 2, 45, 60, 85, 0.8, 2);
drawLine(wfX1 + 2, wfY0 - 2, wfX1 + 2, wfY1 + 2, 45, 60, 85, 0.8, 2);
drawLine(wfX1 + 2, wfY1 + 2, wfX0 - 2, wfY1 + 2, 45, 60, 85, 0.8, 2);
drawLine(wfX0 - 2, wfY1 + 2, wfX0 - 2, wfY0 - 2, 45, 60, 85, 0.8, 2);

// Generate RF Waterfall content
for (let y = wfY0; y < wfY1; y++) {
  const normY = (y - wfY0) / wfHeight; // Time / depth axis
  
  // Phase of computational execution:
  // - Top: Dense GEMM matrix multiplication (broadband harmonic comb)
  // - Mid: Attention Key-Value cache walk (intermittent bursty chirps)
  // - Lower: Quantized token decompression (tight carrier lines)
  
  for (let x = wfX0; x < wfX1; x++) {
    const normX = (x - wfX0) / wfWidth; // Frequency axis (400 MHz to 450 MHz)
    
    // Background noise floor
    let noise = hash(x * 0.12, y * 0.54) * 0.15;
    
    // Carrier at 433.92 MHz (normX approx 0.678)
    const dCarrier = Math.abs(normX - 0.678);
    let carrier = Math.exp(-dCarrier * 120.0) * 0.85;

    // Harmonic sidebands modulated by 128Hz memory refresh and 60Hz transformer hum
    let sidebands = 0;
    for (let h = 1; h <= 8; h++) {
      const sbOffset = h * 0.038;
      const dSbL = Math.abs(normX - (0.678 - sbOffset));
      const dSbR = Math.abs(normX - (0.678 + sbOffset));
      const mod = Math.sin(normY * 40.0 * h) * 0.5 + 0.5;
      sidebands += (Math.exp(-dSbL * 160.0) + Math.exp(-dSbR * 160.0)) * 0.4 * mod;
    }

    // Algorithmic burst signals (GEMM calculation bursts)
    const burstFreq = Math.sin(normY * 18.0) * 0.2 + 0.35;
    const dBurst = Math.abs(normX - burstFreq);
    let burst = (dBurst < 0.08 ? (1.0 - dBurst / 0.08) * fbm(x * 0.05, y * 0.02, 3) : 0) * 0.7;

    const totalSignal = Math.min(1.0, noise + carrier + sidebands + burst);

    // Color map: deep indigo -> cold phosphor cyan -> incandescent cadmium gold
    let cr = 0, cg = 0, cb = 0;
    if (totalSignal < 0.35) {
      const t = totalSignal / 0.35;
      cr = Math.floor(10 + 20 * t);
      cg = Math.floor(15 + 40 * t);
      cb = Math.floor(40 + 90 * t);
    } else if (totalSignal < 0.75) {
      const t = (totalSignal - 0.35) / 0.4;
      cr = Math.floor(30 + 40 * t);
      cg = Math.floor(55 + 160 * t);
      cb = Math.floor(130 + 80 * t); // Phosphor cyan
    } else {
      const t = (totalSignal - 0.75) / 0.25;
      cr = Math.floor(70 + 175 * t); // Cadmium gold core
      cg = Math.floor(215 - 40 * t);
      cb = Math.floor(210 - 150 * t);
    }

    setPixel(x, y, cr, cg, cb, 0.95);
  }
}

// 3. Render Center Column: The Cylindrical Borehole Core Sample (-500m)
console.log("[CORE-ENGINE] Raymarching 3D cylindrical geological core sample...");
const coreX0 = 1480;
const coreX1 = 2360;
const coreW = coreX1 - coreX0;
const coreRadius = coreW / 2;
const coreCenterX = coreX0 + coreRadius;
const coreY0 = 140;
const coreY1 = 2020;
const coreH = coreY1 - coreY0;

// Draw outer mounting vitrine tracks
drawLine(coreX0 - 10, coreY0 - 4, coreX0 - 10, coreY1 + 4, 70, 85, 110, 0.9, 3);
drawLine(coreX1 + 10, coreY0 - 4, coreX1 + 10, coreY1 + 4, 70, 85, 110, 0.9, 3);

// Render each pixel of the cylindrical core
for (let y = coreY0; y < coreY1; y++) {
  const depthMeters = ((y - coreY0) / coreH) * 500.0; // 0m to 500m
  const normDepth = depthMeters / 500.0;

  for (let x = coreX0; x < coreX1; x++) {
    // Cylindrical normal calculation
    const dx = x - coreCenterX;
    const nx = dx / coreRadius; // -1 to 1
    if (Math.abs(nx) > 0.995) continue; // Edge clipping

    const nz = Math.sqrt(Math.max(0, 1.0 - nx * nx)); // Surface depth normal
    const ny = (fbm(x * 0.02, y * 0.02, 2) - 0.5) * 0.3; // Micro-surface roughness

    // 3D Raking Light Source (from top-left: L = [-0.6, -0.4, 0.7])
    const lx = -0.55, ly = -0.35, lz = 0.75;
    const lNorm = Math.hypot(lx, ly, lz);
    const dot = Math.max(0.08, (nx * (lx / lNorm) + ny * (ly / lNorm) + nz * (lz / lNorm)));

    // Base colors per geological stratum
    let baseR = 0, baseG = 0, baseB = 0;
    const tex1 = fbm(x * 0.015, y * 0.015, 5);
    const tex2 = fbm(x * 0.06, y * 0.06, 4);

    if (depthMeters < 35.0) {
      // Stratum 1: Alluvial Holocene Silt & Loam (0 to -35m)
      const mix = tex1 * 0.7 + tex2 * 0.3;
      baseR = 75 + mix * 40;
      baseG = 52 + mix * 30;
      baseB = 38 + mix * 20;
    } else if (depthMeters < 155.0) {
      // Stratum 2: Jurassic Sandstone with Oxidized Iron Banding (-35 to -155m)
      const ironBand = Math.sin(y * 0.05 + tex1 * 6.0) * 0.5 + 0.5;
      baseR = 150 + ironBand * 65 + tex2 * 30;
      baseG = 80 + ironBand * 40 + tex2 * 20;
      baseB = 45 + ironBand * 15 + tex2 * 10;
    } else if (depthMeters < 285.0) {
      // Stratum 3: Carboniferous Bituminous Shale & Coal (-155 to -285m)
      const shale = tex1 * 0.6 + tex2 * 0.4;
      baseR = 25 + shale * 20;
      baseG = 28 + shale * 22;
      baseB = 34 + shale * 25;
      // Pyrite (fool's gold) crystalline inclusions
      if (hash(x * 0.1, y * 0.1) > 0.985) {
        baseR = 212; baseG = 175; baseB = 55;
      }
    } else if (depthMeters < 345.0) {
      // Stratum 4: THE TECHNO-FOSSIL STRATUM (-285 to -345m)
      // Crushed monocrystalline silicon dies, oxidized copper buses, and gold wires
      const waferFragment = fbm(x * 0.04, y * 0.04, 4);
      if (waferFragment > 0.65) {
        // Monocrystalline Silicon die fragment with thin-film EUV iridescence
        const iridAngle = (x + y * 2) * 0.03;
        baseR = 60 + Math.sin(iridAngle) * 50;
        baseG = 110 + Math.sin(iridAngle + 2.0) * 80;
        baseB = 180 + Math.cos(iridAngle) * 70;
      } else if (waferFragment > 0.52) {
        // Oxidized copper interconnect bus lines (verdigris malachite patina)
        baseR = 31;
        baseG = 175 + tex2 * 45;
        baseB = 145 + tex2 * 35;
      } else if (hash(x * 0.08, y * 0.08) > 0.96) {
        // Gold kintsugi bond wire thread
        baseR = 225; baseG = 185; baseB = 60;
      } else {
        // Fused toxic epoxy packaging matrix & pulverized quartz
        baseR = 35 + tex2 * 25;
        baseG = 38 + tex2 * 25;
        baseB = 44 + tex2 * 30;
      }
    } else {
      // Stratum 5: Pre-Cambrian Crystalline Gneiss & Basalt (-345 to -500m)
      const granite = tex1 * 0.7 + tex2 * 0.3;
      baseR = 48 + granite * 35;
      baseG = 52 + granite * 38;
      baseB = 60 + granite * 42;

      // Hydrothermal white quartz fissure veins cutting diagonally
      const quartzVein = Math.abs(Math.sin((x * 0.6 + y * 0.4) * 0.02 + tex1 * 3.0));
      if (quartzVein < 0.04) {
        baseR = 230; baseG = 238; baseB = 248; // Translucent milky quartz
      }
    }

    // Apply cylindrical diffuse lighting and specular highlight
    const diffuse = dot;
    const spec = Math.pow(Math.max(0, nz * 0.8 + nx * -0.4), 16) * 0.35;

    let finalR = baseR * diffuse + spec * 220;
    let finalG = baseG * diffuse + spec * 220;
    let finalB = baseB * diffuse + spec * 240;

    // Edge shading (cylinder falloff at silhouette)
    const edgeFalloff = Math.pow(nz, 0.45);
    finalR *= edgeFalloff;
    finalG *= edgeFalloff;
    finalB *= edgeFalloff;

    setPixel(x, y, finalR, finalG, finalB, 1.0);
  }
}

// 4. Render Right Panel: Lithic Telemetry & Cartographic Stratigraphy
console.log("[CORE-ENGINE] Drawing stratigraphic telemetry, seismic curves, and annotations...");
const teleX0 = 2600, teleX1 = 3680;

// Depth calibration ticks & labels
for (let d = 0; d <= 500; d += 50) {
  const py = Math.floor(coreY0 + (d / 500.0) * coreH);
  // Tick lines from core right across to telemetry
  drawLine(coreX1 + 15, py, coreX1 + 45, py, 180, 200, 225, 0.8, 2);
  drawLine(teleX0, py, teleX0 + 30, py, 140, 165, 195, 0.6, 1);
  drawLine(teleX0 + 40, py, teleX1, py, 25, 32, 45, 0.4, 1); // Guide baseline
}

// Draw Seismic Shear Wave Impedance Curve (Z = rho * v_s)
console.log("[CORE-ENGINE] Plotting seismic shear-wave impedance profile...");
let prevZx = 0, prevZy = 0;
for (let y = coreY0; y < coreY1; y += 2) {
  const depth = ((y - coreY0) / coreH) * 500.0;
  let vs = 700; // m/s (silt)
  if (depth > 35) vs = 1650; // Sandstone
  if (depth > 155) vs = 2400; // Shale
  if (depth > 285 && depth < 345) vs = 1850; // Techno-fossil disturbance drop!
  if (depth >= 345) vs = 3450; // Crystalline Granite

  // Add empirical measurement jitter
  vs += (fbm(y * 0.08, 12.4, 3) - 0.5) * 180.0;

  // Map vs (500 to 3800 m/s) to X coordinate (teleX0 + 80 to teleX0 + 480)
  const zX = Math.floor(teleX0 + 80 + ((vs - 500) / 3300.0) * 400);
  if (prevZx !== 0) {
    drawLine(prevZx, prevZy, zX, y, 56, 215, 210, 0.85, 2); // Phosphor cyan
  }
  prevZx = zX;
  prevZy = y;
}

// Draw Geothermal Temperature Gradient Curve (12C at surface to 44.5C at -500m)
console.log("[CORE-ENGINE] Plotting geothermal temperature gradient...");
let prevTx = 0, prevTy = 0;
for (let y = coreY0; y < coreY1; y += 2) {
  const depth = ((y - coreY0) / coreH) * 500.0;
  const tempC = 12.0 + (depth / 1000.0) * 65.0; // +65C/km geothermal gradient
  const tX = Math.floor(teleX0 + 560 + ((tempC - 10) / 40.0) * 400);

  if (prevTx !== 0) {
    drawLine(prevTx, prevTy, tX, y, 212, 175, 55, 0.85, 2); // Cadmium gold
  }
  prevTx = tX;
  prevTy = y;
}

// Draw Reticle crosshairs and fiducials (Agnes Martin precision)
console.log("[CORE-ENGINE] Inscribing photolithographic reticle alignment marks...");
const fiducials = [
  [coreX0 - 60, coreY0 + 20],
  [coreX1 + 60, coreY0 + 20],
  [coreX0 - 60, coreY1 - 20],
  [coreX1 + 60, coreY1 - 20],
  [wfX0 + 40, wfY0 + 40],
  [teleX1 - 40, wfY1 - 40]
];

for (const [fx, fy] of fiducials) {
  drawLine(fx - 18, fy, fx + 18, fy, 212, 175, 55, 0.9, 1);
  drawLine(fx, fy - 18, fx, fy + 18, 212, 175, 55, 0.9, 1);
  // Small circle surrogate
  for (let a = 0; a < 360; a += 30) {
    const rad = (a * Math.PI) / 180;
    setPixel(Math.floor(fx + Math.cos(rad) * 8), Math.floor(fy + Math.sin(rad) * 8), 212, 175, 55, 0.9);
  }
}

// Save raw buffer to temporary binary file for Python PNG encoder
const rawOutputPath = path.join(__dirname, "master_plate_raw.rgb");
console.log(`[CORE-ENGINE] Flushing ${buffer.length} raw bytes to ${rawOutputPath}...`);
fs.writeFileSync(rawOutputPath, buffer);
console.log("[CORE-ENGINE] Procedural plate synthesis complete!");
