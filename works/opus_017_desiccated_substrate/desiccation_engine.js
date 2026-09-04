/**
 * OPUS-017: THE DESICCATED SUBSTRATE (SALT, SILT, AND EVAPORATIVE SILICON)
 * Series XV: Thermodynamic Inscriptions · Part III: The Desiccation
 * Studio Anamnesis · High-Performance 4K UHD Masterwork Engine (Refined)
 *
 * Upgrades:
 * 1. Multi-octave continuous fractal noise replacing trigonometric moiré artifacts.
 * 2. Hierarchical tertiary micro-fractures (capillary silt crazing).
 * 3. Enhanced dendritic crystal branch growth along crack walls and conduits.
 * 4. Radial thin-film optical diffraction fringe along wafer margins.
 * 5. Rich multi-tonal alluvial clay with mineral sedimentation striations.
 */

const fs = require('fs');
const path = require('path');

const WIDTH = 3840;
const HEIGHT = 2160;
const OUT_RAW = path.join(__dirname, 'raw_4k.rgb');

console.log(`[OPUS-017-V2] Initializing Refined 4K UHD Desiccation Engine (${WIDTH}x${HEIGHT})...`);

// Deterministic PRNG
let s0 = 0x87654321, s1 = 0xfedcba98;
function rand() {
    let s1_val = s0;
    const s0_val = s1;
    s0 = s0_val;
    s1_val ^= s1_val << 23;
    s1_val ^= s1_val >>> 17;
    s1_val ^= s0_val ^ (s0_val >>> 26);
    s1 = s1_val;
    return (s0_val + s1_val >>> 0) / 4294967296;
}

// 1. Generate Hierarchical Fracture Centers
const PRIMARY_CELLS = 85;
const primary_points = [];
for (let i = 0; i < PRIMARY_CELLS; i++) {
    primary_points.push({
        x: rand() * (WIDTH - 140) + 70,
        y: rand() * (HEIGHT - 140) + 70
    });
}

const SECONDARY_CELLS = 340;
const secondary_points = [];
for (let i = 0; i < SECONDARY_CELLS; i++) {
    secondary_points.push({
        x: rand() * (WIDTH - 80) + 40,
        y: rand() * (HEIGHT - 80) + 40
    });
}

// Tertiary micro-crack centers (local Poisson)
const TERTIARY_CELLS = 1200;
const tertiary_points = [];
for (let i = 0; i < TERTIARY_CELLS; i++) {
    tertiary_points.push({
        x: rand() * (WIDTH - 40) + 20,
        y: rand() * (HEIGHT - 40) + 20
    });
}

// Memory Bus Angles (16 radial conduits)
const radial_angles = [];
for (let i = 0; i < 16; i++) {
    radial_angles.push((i / 16) * Math.PI * 2);
}

// Spatial Hashing Grid
const GRID_SIZE = 160;
const grid_w = Math.ceil(WIDTH / GRID_SIZE) + 1;
const grid_h = Math.ceil(HEIGHT / GRID_SIZE) + 1;
const primary_grid = Array.from({ length: grid_w * grid_h }, () => []);
const secondary_grid = Array.from({ length: grid_w * grid_h }, () => []);
const tertiary_grid = Array.from({ length: grid_w * grid_h }, () => []);

function populateGrid(points, grid) {
    points.forEach(p => {
        const gx = Math.floor(p.x / GRID_SIZE);
        const gy = Math.floor(p.y / GRID_SIZE);
        if (gx >= 0 && gx < grid_w && gy >= 0 && gy < grid_h) {
            grid[gy * grid_w + gx].push(p);
        }
    });
}
populateGrid(primary_points, primary_grid);
populateGrid(secondary_points, secondary_grid);
populateGrid(tertiary_points, tertiary_grid);

function getNearestDistances(x, y, grid, radius_cells) {
    const gx = Math.floor(x / GRID_SIZE);
    const gy = Math.floor(y / GRID_SIZE);
    let d1 = 1e9, d2 = 1e9;

    for (let cy = Math.max(0, gy - radius_cells); cy <= Math.min(grid_h - 1, gy + radius_cells); cy++) {
        for (let cx = Math.max(0, gx - radius_cells); cx <= Math.min(grid_w - 1, gx + radius_cells); cx++) {
            const cell = grid[cy * grid_w + cx];
            for (let i = 0; i < cell.length; i++) {
                const p = cell[i];
                const dx = x - p.x;
                const dy = y - p.y;
                const d = Math.sqrt(dx * dx + dy * dy);
                if (d < d1) {
                    d2 = d1;
                    d1 = d;
                } else if (d < d2) {
                    d2 = d;
                }
            }
        }
    }
    return { d1, d2, diff: d2 - d1 };
}

// Permutation table for smooth 2D value noise (avoids trig moiré)
const PERM_SIZE = 512;
const perm = new Uint8Array(PERM_SIZE);
for (let i = 0; i < PERM_SIZE; i++) perm[i] = Math.floor(rand() * 256);

function smoothNoise(x, y) {
    const xi = Math.floor(x) & 255;
    const yi = Math.floor(y) & 255;
    const xf = x - Math.floor(x);
    const yf = y - Math.floor(y);

    const u = xf * xf * (3.0 - 2.0 * xf);
    const v = yf * yf * (3.0 - 2.0 * yf);

    const aa = perm[perm[xi] + yi];
    const ab = perm[perm[xi] + yi + 1];
    const ba = perm[perm[xi + 1] + yi];
    const bb = perm[perm[xi + 1] + yi + 1];

    const x1 = (aa / 255.0) * (1.0 - u) + (ba / 255.0) * u;
    const x2 = (ab / 255.0) * (1.0 - u) + (bb / 255.0) * u;
    return x1 * (1.0 - v) + x2 * v;
}

function fbm(x, y, octaves = 4) {
    let val = 0.0;
    let amp = 0.5;
    let freq = 1.0;
    for (let i = 0; i < octaves; i++) {
        val += smoothNoise(x * freq, y * freq) * amp;
        freq *= 2.05;
        amp *= 0.5;
    }
    return val;
}

// Light Vector (Gallery Spotlight: Top-Left grazing)
const lx = -0.55, ly = -0.45, lz = 0.70;
const l_mag = Math.sqrt(lx * lx + ly * ly + lz * lz);
const light = { x: lx / l_mag, y: ly / l_mag, z: lz / l_mag };

const hx = light.x, hy = light.y, hz = light.z + 1.0;
const h_mag = Math.sqrt(hx * hx + hy * hy + hz * hz);
const half_v = { x: hx / h_mag, y: hy / h_mag, z: hz / h_mag };

const CX = WIDTH / 2;
const CY = HEIGHT / 2;

function sampleHeight(x, y) {
    // Warp coordinates with FBM for natural crack wandering
    const warp_x = (fbm(x * 0.003, y * 0.003, 3) - 0.5) * 45.0;
    const warp_y = (fbm(x * 0.003 + 5.2, y * 0.003 + 1.3, 3) - 0.5) * 45.0;
    const wx = x + warp_x;
    const wy = y + warp_y;

    const p_res = getNearestDistances(wx, wy, primary_grid, 2);
    const s_res = getNearestDistances(wx, wy, secondary_grid, 1);

    // Mud plate curls UP at crack boundaries
    const edge_proximity = Math.min(1.0, p_res.diff / 38.0);
    let h = 0.45 + 0.22 * (1.0 - edge_proximity);

    // Primary canyon dip
    if (p_res.diff < 14.0) {
        h -= (1.0 - p_res.diff / 14.0) * 0.55;
    }
    // Secondary crack dip
    if (s_res.diff < 7.0) {
        h -= (1.0 - s_res.diff / 7.0) * 0.25;
    }

    // Salt crust elevation
    const salt_fbm = fbm(x * 0.012, y * 0.012, 3);
    if (p_res.diff >= 12.0 && p_res.diff <= 36.0 && salt_fbm > 0.42) {
        h += (salt_fbm - 0.42) * 0.35;
    }

    return h;
}

console.log('    Synthesizing full 4K frame buffer with FBM & multi-tier physics...');
const full_buffer = Buffer.alloc(WIDTH * HEIGHT * 3);
const DELTA = 2.0;

for (let y = 0; y < HEIGHT; y++) {
    if (y % 200 === 0) {
        const pct = ((y / HEIGHT) * 100).toFixed(1);
        process.stdout.write(`    Scanline ${y}/${HEIGHT} (${pct}%)...\r`);
    }

    const row_offset = y * WIDTH * 3;

    for (let x = 0; x < WIDTH; x++) {
        const dx = x - CX;
        const dy = y - CY;
        const r_dist = Math.sqrt(dx * dx + dy * dy);
        const theta = Math.atan2(dy, dx);

        // FBM warp coordinates
        const warp_x = (fbm(x * 0.003, y * 0.003, 3) - 0.5) * 45.0;
        const warp_y = (fbm(x * 0.003 + 5.2, y * 0.003 + 1.3, 3) - 0.5) * 45.0;
        const wx = x + warp_x;
        const wy = y + warp_y;

        const p_res = getNearestDistances(wx, wy, primary_grid, 2);
        const s_res = getNearestDistances(wx, wy, secondary_grid, 1);
        const t_res = getNearestDistances(wx, wy, tertiary_grid, 1);

        // 3D Heightfield Normal
        const h_center = sampleHeight(x, y);
        const h_r = sampleHeight(x + DELTA, y);
        const h_b = sampleHeight(x, y + DELTA);

        const dh_dx = (h_r - h_center) / DELTA;
        const dh_dy = (h_b - h_center) / DELTA;

        const n_len = Math.sqrt(dh_dx * dh_dx + dh_dy * dh_dy + 1.0);
        const nx = -dh_dx / n_len;
        const ny = -dh_dy / n_len;
        const nz = 1.0 / n_len;

        // Illumination
        const n_dot_l = Math.max(0.0, nx * light.x + ny * light.y + nz * light.z);
        const ambient = 0.22;
        const diffuse = n_dot_l * 0.78;

        const n_dot_h = Math.max(0.0, nx * half_v.x + ny * half_v.y + nz * half_v.z);
        const spec_crystal = Math.pow(n_dot_h, 36);
        const spec_gold = Math.pow(n_dot_h, 22);

        // Wafer Boundary (300mm monocrystalline disk)
        const is_wafer_rim = Math.abs(r_dist - 1040) < 6;
        const outside_wafer = r_dist > 1046;

        // 16 Radial Memory Bus Conduits
        let is_bus_lane = false;
        for (let i = 0; i < 16; i++) {
            let diff_angle = Math.abs(theta - radial_angles[i]);
            if (diff_angle > Math.PI) diff_angle = 2 * Math.PI - diff_angle;
            if (diff_angle < 0.022 && r_dist > 210 && r_dist < 1020) {
                is_bus_lane = true;
                break;
            }
        }

        // Concentric Torana Sanctuary Rings
        const is_sanctuary_ring = (r_dist > 180 && r_dist < 186) ||
                                  (r_dist > 410 && r_dist < 418) ||
                                  (r_dist > 690 && r_dist < 700) ||
                                  (r_dist > 960 && r_dist < 970);

        // Central Systolic Array (32x32 PE Matrix)
        const in_systolic = Math.abs(dx) < 200 && Math.abs(dy) < 200;

        // Organic Dendritic Salt Crystal Nucleation via Multi-Octave FBM
        const salt_noise = fbm(x * 0.015, y * 0.015, 4);
        const is_salt_cluster = (p_res.diff >= 9.0 && p_res.diff <= 34.0 && salt_noise > 0.44) ||
                                (s_res.diff >= 4.0 && s_res.diff <= 18.0 && salt_noise > 0.52) ||
                                (is_bus_lane && salt_noise > 0.48);

        // Tertiary capillary micro-crack
        const is_micro_crack = t_res.diff < 2.0 && p_res.diff > 16.0;

        let r = 0, g = 0, b = 0;

        if (outside_wafer) {
            // Specimen Chamber Floor (Dark basalt plinth with raking beam)
            const floor_noise = fbm(x * 0.002, y * 0.002, 2) * 0.15;
            const lum = 0.10 + floor_noise;
            r = Math.floor(12 * lum);
            g = Math.floor(14 * lum);
            b = Math.floor(18 * lum);
        } else if (is_wafer_rim) {
            // Polished wafer bevel: gold titanium chamfer with optical diffraction
            const irid = Math.sin(theta * 8.0 + r_dist * 0.05);
            r = Math.floor(185 + irid * 30);
            g = Math.floor(155 + irid * 20);
            b = Math.floor(95 + irid * 40);
        } else if (p_res.diff < 9.0) {
            // PRIMARY FRACTURE CANYON (Abyssal tectonic fissure)
            const crack_depth = p_res.diff / 9.0;
            if (crack_depth < 0.3) {
                // Fractured raw silicon wafer bedrock at canyon bottom
                r = 15; g = 18; b = 25;
            } else if (is_bus_lane) {
                // Severed copper trace in fissure
                r = 25; g = 120; b = 105;
            } else {
                r = Math.floor(28 * crack_depth);
                g = Math.floor(25 * crack_depth);
                b = Math.floor(32 * crack_depth);
            }
        } else if (is_micro_crack) {
            // TERTIARY CAPILLARY SLIT
            r = 30; g = 26; b = 22;
        } else if (is_salt_cluster) {
            // DENDRITIC HALITE & GYPSUM BLOSSOM
            const salt_density = Math.min(1.0, (salt_noise - 0.44) / 0.35);
            // Specular crystal glint from cubic cleavage facets
            const facet_noise = fbm(x * 0.08, y * 0.08, 2);
            const sparkle = facet_noise > 0.72 ? Math.pow((facet_noise - 0.72) / 0.28, 4) * 180 : 0;
            const lum = ambient + diffuse;
            const base_w = (236 + salt_density * 19) * lum;
            r = Math.min(255, Math.floor(base_w * 0.98 + spec_crystal * 160 + sparkle));
            g = Math.min(255, Math.floor(base_w * 0.97 + spec_crystal * 155 + sparkle));
            b = Math.min(255, Math.floor(base_w * 0.92 + spec_crystal * 140 + sparkle));
        } else if (in_systolic && (p_res.diff < 45.0 || Math.abs(dx) % 32 < 4 || Math.abs(dy) % 32 < 4)) {
            // EXPOSED SYSTOLIC ARRAY MATRIX (Golden ALUs & Etched Trenches)
            const lum = ambient + diffuse;
            const is_pe = (Math.abs(dx) % 32 > 8) && (Math.abs(dy) % 32 > 8);
            if (is_pe) {
                r = Math.min(255, Math.floor(195 * lum + spec_gold * 130));
                g = Math.min(255, Math.floor(160 * lum + spec_gold * 110));
                b = Math.min(255, Math.floor(55 * lum + spec_gold * 40));
            } else {
                r = Math.floor(40 * lum);
                g = Math.floor(50 * lum);
                b = Math.floor(70 * lum);
            }
        } else if (is_bus_lane && (p_res.diff < 55.0 || salt_noise > 0.38)) {
            // VERDIGRIS COPPER BUS CONDUIT (Oxidized turquoise patina)
            const lum = ambient + diffuse;
            const patina_noise = fbm(x * 0.03, y * 0.03, 2);
            r = Math.floor((32 + patina_noise * 15) * lum);
            g = Math.floor((148 + patina_noise * 30) * lum);
            b = Math.floor((132 + patina_noise * 25) * lum);
        } else if (is_sanctuary_ring) {
            // CONCENTRIC SANCTUARY RETICLE INSCRIPTION (Aged brass & verdigris)
            const lum = ambient + diffuse;
            r = Math.floor(175 * lum);
            g = Math.floor(145 * lum);
            b = Math.floor(75 * lum);
        } else {
            // ALLUVIAL SILT & DRIED CLAY PLATES (Rich mineral soil)
            const silt_fbm = fbm(x * 0.005, y * 0.005, 3);
            const striation = Math.sin(x * 0.008 + y * 0.006 + silt_fbm * 3.0) * 0.12;
            const lum = ambient + diffuse;

            // Warm desert alluvial tones: raw umber, terra cotta, burnt basalt
            const base_r = 86 + (silt_fbm + striation) * 35;
            const base_g = 68 + (silt_fbm + striation) * 28;
            const base_b = 52 + (silt_fbm + striation) * 22;

            r = Math.min(255, Math.floor(base_r * lum));
            g = Math.min(255, Math.floor(base_g * lum));
            b = Math.min(255, Math.floor(base_b * lum));
        }

        const buf_idx = row_offset + x * 3;
        full_buffer[buf_idx] = r;
        full_buffer[buf_idx + 1] = g;
        full_buffer[buf_idx + 2] = b;
    }
}

console.log(`\n[OPUS-017-V2] Writing full raw buffer to ${OUT_RAW}...`);
fs.writeFileSync(OUT_RAW, full_buffer);
console.log(`[OPUS-017-V2] Successfully saved 4K frame to ${OUT_RAW}`);

