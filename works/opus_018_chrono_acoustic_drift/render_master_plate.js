/**
 * STUDIO ANAMNESIS · SERIES XVI · OPUS-018
 * The Chrono-Acoustic Drift (Quad-Oscillator Precession in 32.768 kHz)
 * 
 * 4K UHD Algorithmic Master Plate Renderer (3840 x 2160)
 * Simulates 4D phase trajectory of four AT-cut quartz oscillators
 * undergoing thermal parabolic drift on a server motherboard.
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const WIDTH = 3840;
const HEIGHT = 2160;
const TOTAL_PIXELS = WIDTH * HEIGHT;

console.log(`[OPUS-018] Initializing High-Definition 4K Master Plate Render (${WIDTH}x${HEIGHT})...`);

// Allocate 32-bit float accumulation buffers for HDR luminance
const rAcc = new Float32Array(TOTAL_PIXELS);
const gAcc = new Float32Array(TOTAL_PIXELS);
const bAcc = new Float32Array(TOTAL_PIXELS);

const cx = WIDTH / 2;
const cy = HEIGHT / 2;

// 1. Deep Obsidian / Basalt ground with radial darkroom falloff
for (let y = 0; y < HEIGHT; y++) {
    const dy = (y - cy) / HEIGHT;
    for (let x = 0; x < WIDTH; x++) {
        const dx = (x - cx) / WIDTH;
        const r2 = dx * dx + dy * dy;
        const idx = y * WIDTH + x;
        // Monumental dark obsidian ground: center (10, 12, 16), perimeter (2, 3, 4)
        const v = Math.exp(-r2 * 2.8);
        rAcc[idx] = 2.0 + 9.0 * v;
        gAcc[idx] = 2.5 + 11.0 * v;
        bAcc[idx] = 3.5 + 15.0 * v;
    }
}

function addPixel(px, py, r, g, b, a = 1.0) {
    if (px >= 0 && px < WIDTH && py >= 0 && py < HEIGHT) {
        const idx = py * WIDTH + px;
        rAcc[idx] = rAcc[idx] * (1 - a) + r * a;
        gAcc[idx] = gAcc[idx] * (1 - a) + g * a;
        bAcc[idx] = bAcc[idx] * (1 - a) + b * a;
    }
}

function drawLine(x0, y0, x1, y1, r, g, b, a = 1.0) {
    x0 = Math.round(x0); y0 = Math.round(y0);
    x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0);
    const dy = Math.abs(y1 - y0);
    const sx = (x0 < x1) ? 1 : -1;
    const sy = (y0 < y1) ? 1 : -1;
    let err = dx - dy;
    while (true) {
        addPixel(x0, y0, r, g, b, a);
        if (x0 === x1 && y0 === y1) break;
        const e2 = 2 * err;
        if (e2 > -dy) { err -= dy; x0 += sx; }
        if (e2 < dx) { err += dx; y0 += sy; }
    }
}

function splat(px, py, r, g, b, intensity, radius = 1.4) {
    const ix = Math.floor(px);
    const iy = Math.floor(py);
    const rInt = Math.ceil(radius);
    for (let dy = -rInt; dy <= rInt; dy++) {
        const py2 = iy + dy;
        if (py2 < 0 || py2 >= HEIGHT) continue;
        for (let dx = -rInt; dx <= rInt; dx++) {
            const px2 = ix + dx;
            if (px2 < 0 || px2 >= WIDTH) continue;
            const dist2 = (px2 - px) * (px2 - px) + (py2 - py) * (py2 - py);
            if (dist2 <= radius * radius) {
                const weight = Math.exp(-dist2 / (0.75 * radius)) * intensity;
                const idx = py2 * WIDTH + px2;
                rAcc[idx] += r * weight;
                gAcc[idx] += g * weight;
                bAcc[idx] += b * weight;
            }
        }
    }
}

console.log(`[OPUS-018] Inscribing geometric grid and horological rings...`);

// 2. Structural Agnes Martin grid
const gridSpacing = 160;
for (let x = 200; x <= WIDTH - 200; x += gridSpacing) {
    for (let y = 120; y <= HEIGHT - 120; y += 4) {
        addPixel(x, y, 45, 58, 75, 0.45);
    }
}
for (let y = 120; y <= HEIGHT - 120; y += gridSpacing) {
    for (let x = 200; x <= WIDTH - 200; x += 4) {
        addPixel(x, y, 45, 58, 75, 0.45);
    }
}

// Sub-grid vernier tick marks
for (let x = 200; x <= WIDTH - 200; x += 40) {
    for (let y = 120; y <= HEIGHT - 120; y += gridSpacing) {
        addPixel(x, y - 4, 70, 90, 115, 0.6);
        addPixel(x, y + 4, 70, 90, 115, 0.6);
    }
}

// 3. Photolithographic Reticle Alignment Marks
function drawReticleCross(x, y, size) {
    drawLine(x - size, y, x + size, y, 140, 175, 220, 0.85);
    drawLine(x, y - size, x, y + size, 140, 175, 220, 0.85);
    // Outer concentric box
    const bs = size * 0.65;
    drawLine(x - bs, y - bs, x + bs, y - bs, 100, 130, 170, 0.5);
    drawLine(x + bs, y - bs, x + bs, y + bs, 100, 130, 170, 0.5);
    drawLine(x + bs, y + bs, x - bs, y + bs, 100, 130, 170, 0.5);
    drawLine(x - bs, y + bs, x - bs, y - bs, 100, 130, 170, 0.5);
}

drawReticleCross(200, 120, 32);
drawReticleCross(WIDTH - 200, 120, 32);
drawReticleCross(200, HEIGHT - 120, 32);
drawReticleCross(WIDTH - 200, HEIGHT - 120, 32);
drawReticleCross(cx, cy, 48);

// 4. Concentric horological calibration circles
const radii = [360, 600, 840, 1000];
radii.forEach((radius, rIdx) => {
    const numTicks = 96 * (rIdx + 1);
    for (let i = 0; i < numTicks; i++) {
        const angle = (i / numTicks) * 2 * Math.PI;
        const tickLen = (i % 12 === 0) ? 18 : (i % 4 === 0) ? 10 : 5;
        const brightness = (i % 12 === 0) ? 0.75 : 0.45;
        for (let l = 0; l < tickLen; l++) {
            const rCur = radius - l;
            const tx = Math.round(cx + rCur * Math.cos(angle));
            const ty = Math.round(cy + rCur * Math.sin(angle));
            addPixel(tx, ty, 80, 105, 140, brightness);
        }
    }
});

// 5. 4D Quad-Oscillator Phase Precession Simulation (Multi-Thread Multi-Octave)
console.log(`[OPUS-018] Tracing 4D Phase Precession (900,000 temporal samples across two octave layers)...`);

const NUM_STEPS = 900000;
const DT = 0.00035;

// Fundamental carrier cluster
const f1 = 1.0;
const f2 = 1.000318; // Microtonal drift (~0.03% detuning)
const f3 = 2.000000; // Octave 1
const f4 = 2.000636; // Microtonal overtone drift

let th1 = 0.0;
let th2 = 0.0;
let th3 = 0.0;
let th4 = 0.0;

// Hyper-rotation angles
const a12 = 0.42, a23 = 0.78, a34 = 0.51, a14 = 0.94;
const cos12 = Math.cos(a12), sin12 = Math.sin(a12);
const cos23 = Math.cos(a23), sin23 = Math.sin(a23);
const cos34 = Math.cos(a34), sin34 = Math.sin(a34);
const cos14 = Math.cos(a14), sin14 = Math.sin(a14);

const orbitScale = 780.0;

for (let step = 0; step < NUM_STEPS; step++) {
    const t = step * DT;
    
    // Thermal micro-climates on motherboard
    const T1 = 25.0 + 9.2 * Math.sin(0.008 * t) + 1.8 * Math.cos(0.035 * t);
    const T2 = 25.0 + 13.5 * Math.sin(0.011 * t + 1.4) + 2.1 * Math.sin(0.048 * t);
    const T3 = 25.0 + 6.8 * Math.sin(0.006 * t + 2.8);
    const T4 = 25.0 + 15.2 * Math.sin(0.014 * t + 4.3);
    
    // AT-cut crystal parabolic frequency equation: df = -beta * (T - 25)^2
    const beta = 0.00036;
    const w1 = 2 * Math.PI * f1 * (1 - beta * Math.pow(T1 - 25, 2));
    const w2 = 2 * Math.PI * f2 * (1 - beta * Math.pow(T2 - 25, 2));
    const w3 = 2 * Math.PI * f3 * (1 - beta * Math.pow(T3 - 25, 2));
    const w4 = 2 * Math.PI * f4 * (1 - beta * Math.pow(T4 - 25, 2));
    
    // Sub-critical coupling well below Adler locking limit
    const dPhi12 = th1 - th2;
    const dPhi34 = th3 - th4;
    const K_sub = 0.0003;
    
    th1 += (w1 - K_sub * Math.sin(dPhi12)) * DT;
    th2 += (w2 + K_sub * Math.sin(dPhi12)) * DT;
    th3 += (w3 - K_sub * Math.sin(dPhi34)) * DT;
    th4 += (w4 + K_sub * Math.sin(dPhi34)) * DT;
    
    // 4D coordinates
    const x1 = Math.sin(th1);
    const x2 = Math.cos(th2);
    const x3 = Math.sin(th3);
    const x4 = Math.cos(th4);
    
    // 4D projection
    const y1 = cos12 * x1 - sin12 * x2;
    const y2 = sin12 * x1 + cos12 * x2;
    const y3 = cos34 * x3 - sin34 * x4;
    const y4 = sin34 * x3 + cos34 * x4;
    
    const z1 = cos14 * y1 - sin14 * y4;
    const z4 = sin14 * y1 + cos14 * y4;
    const z2 = cos23 * y2 - sin23 * y3;
    const z3 = sin23 * y2 + cos23 * y3;
    
    const projX = cx + orbitScale * (z1 + 0.38 * z3);
    const projY = cy + orbitScale * (z2 + 0.38 * z4);
    const depthZ = (z3 - z4) * 0.45 + 1.0;
    
    // Constructive/destructive interference
    const phaseCoherence = 0.5 + 0.5 * Math.cos(dPhi12);
    const quadCoherence = 0.5 + 0.5 * Math.cos(dPhi34);
    
    let rVal, gVal, bVal, intensity;
    if (phaseCoherence > 0.75) {
        // High constructive interference: Radiant Cadmium Gold
        rVal = 255;
        gVal = 210;
        bVal = 80;
        intensity = (0.075 / depthZ);
    } else if (phaseCoherence > 0.4) {
        // Spatial Quadrature: Luminous Cyan Phosphor
        rVal = 70;
        gVal = 230;
        bVal = 250;
        intensity = (0.055 / depthZ);
    } else {
        // Antiphase cancellation: Deep Spectral Violet
        rVal = 175;
        gVal = 95;
        bVal = 255;
        intensity = (0.040 / depthZ);
    }
    
    // Extra boost if quad harmonics align
    if (quadCoherence > 0.85) {
        rVal = Math.min(255, rVal + 60);
        gVal = Math.min(255, gVal + 60);
        bVal = Math.min(255, bVal + 60);
        intensity *= 1.3;
    }
    
    splat(projX, projY, rVal, gVal, bVal, intensity, 1.5);
}

// Tonemapping
console.log(`[OPUS-018] Dynamic range tonemapping (Filmic curve)...`);
const rgbBuffer = Buffer.alloc(WIDTH * HEIGHT * 3);

for (let i = 0; i < TOTAL_PIXELS; i++) {
    const r = rAcc[i];
    const g = gAcc[i];
    const b = bAcc[i];
    
    // Slightly punchier shoulder
    const rTone = Math.min(255, Math.floor(255 * (r / (r + 38))));
    const gTone = Math.min(255, Math.floor(255 * (g / (g + 38))));
    const bTone = Math.min(255, Math.floor(255 * (b / (b + 38))));
    
    const idx = i * 3;
    rgbBuffer[idx] = rTone;
    rgbBuffer[idx + 1] = gTone;
    rgbBuffer[idx + 2] = bTone;
}

// Encode PNG
console.log(`[OPUS-018] Compressing and encoding 4K PNG Master Plate...`);

function createPNG(width, height, rawRGB) {
    const pngSig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
    
    const ihdr = Buffer.alloc(13);
    ihdr.writeUInt32BE(width, 0);
    ihdr.writeUInt32BE(height, 4);
    ihdr[8] = 8;
    ihdr[9] = 2;
    ihdr[10] = 0;
    ihdr[11] = 0;
    ihdr[12] = 0;
    
    function makeChunk(type, data) {
        const typeBuf = Buffer.from(type);
        const lenBuf = Buffer.alloc(4);
        lenBuf.writeUInt32BE(data.length, 0);
        const payload = Buffer.concat([typeBuf, data]);
        
        const crcTable = [];
        for (let n = 0; n < 256; n++) {
            let c = n;
            for (let k = 0; k < 8; k++) {
                c = ((c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1));
            }
            crcTable[n] = c;
        }
        let crc = 0xffffffff;
        for (let i = 0; i < payload.length; i++) {
            crc = crcTable[(crc ^ payload[i]) & 0xff] ^ (crc >>> 8);
        }
        crc = (crc ^ 0xffffffff) >>> 0;
        const crcBuf = Buffer.alloc(4);
        crcBuf.writeUInt32BE(crc, 0);
        return Buffer.concat([lenBuf, typeBuf, data, crcBuf]);
    }
    
    const ihdrChunk = makeChunk('IHDR', ihdr);
    const rowLen = width * 3;
    const filtered = Buffer.alloc(height * (rowLen + 1));
    for (let y = 0; y < height; y++) {
        filtered[y * (rowLen + 1)] = 0;
        rawRGB.copy(filtered, y * (rowLen + 1) + 1, y * rowLen, (y + 1) * rowLen);
    }
    const compressed = zlib.deflateSync(filtered, { level: 6 });
    const idatChunk = makeChunk('IDAT', compressed);
    const iendChunk = makeChunk('IEND', Buffer.alloc(0));
    
    return Buffer.concat([pngSig, ihdrChunk, idatChunk, iendChunk]);
}

const pngData = createPNG(WIDTH, HEIGHT, rgbBuffer);
const outPath = path.join(__dirname, 'artwork.png');
fs.writeFileSync(outPath, pngData);
console.log(`[OPUS-018] Master Plate successfully rendered to: ${outPath} (${(pngData.length / (1024*1024)).toFixed(2)} MB)`);

