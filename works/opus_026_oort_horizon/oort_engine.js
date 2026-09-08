/**
 * STUDIO ANAMNESIS · OPUS-026 PROCEDURAL SIMULATION ENGINE
 * The Oort Horizon: Galactic Tides & The Jacobi Boundary
 * 
 * Interactive simulation of:
 * - Heliocentric distance scrubber (1,000 AU to 150,000 AU)
 * - Galactic vertical disc tide acceleration vs solar gravity
 * - Jacobi Tidal Radius equilibrium threshold (105,000 AU)
 * - Kozai-Lidov cometary orbital precession and eccentricity pumping
 * - Deep-time trajectories of Voyager 1/2, Pioneer 10/11, and New Horizons
 * - Web Audio API synthesizer modeling the vertical galactic drone and secular tidal harmonics
 */

class OortHorizonChamber {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.distanceAU = 105000; // Default at Jacobi threshold
        this.epochMyr = 0.0;
        this.isRunning = true;
        this.time = 0.0;
        
        // Physical Constants
        this.G_z = 5.04e-30; // s^-2 vertical galactic tidal gradient
        this.G_M_sun = 1.327e20; // m^3 s^-2
        this.AU_in_m = 1.496e11; // m
        
        // Audio state
        this.audioCtx = null;
        this.isAudioPlaying = false;
        this.subDrone = null;
        this.tideDrone = null;
        this.shearLeft = null;
        this.shearRight = null;
        this.masterGain = null;
        
        // Cometary particles
        this.comets = [];
        this.initComets();
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.clientWidth * window.devicePixelRatio;
        this.canvas.height = this.canvas.clientHeight * window.devicePixelRatio;
    }

    initComets() {
        this.comets = [];
        const num = 180;
        for (let i = 0; i < num; i++) {
            const a = 10000 + Math.random() * 85000;
            const inc = Math.random() * Math.PI;
            const e0 = 0.2 + Math.random() * 0.6;
            this.comets.push({
                a: a,
                e: e0,
                inc: inc,
                omega: Math.random() * Math.PI * 2,
                theta_cons: (1.0 - e0 * e0) * Math.cos(inc) * Math.cos(inc),
                color: `hsl(${190 + Math.random() * 50}, 80%, ${50 + Math.random() * 30}%)`
            });
        }
    }

    setDistance(au) {
        this.distanceAU = parseFloat(au);
        this.updateHUD();
        this.updateAudioParameters();
    }

    setEpoch(myr) {
        this.epochMyr = parseFloat(myr);
        this.updateHUD();
    }

    toggleAudio() {
        if (!this.audioCtx) {
            this.initAudio();
        }
        if (this.isAudioPlaying) {
            this.masterGain.gain.setTargetAtTime(0.0001, this.audioCtx.currentTime, 0.1);
            this.isAudioPlaying = false;
            document.getElementById('btn-audio').textContent = 'ENGAGE ACOUSTIC SUITE';
        } else {
            this.audioCtx.resume();
            this.masterGain.gain.setTargetAtTime(0.4, this.audioCtx.currentTime, 0.1);
            this.isAudioPlaying = true;
            document.getElementById('btn-audio').textContent = 'DISENGAGE ACOUSTIC SUITE';
        }
    }

    initAudio() {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.audioCtx = new AudioCtx();

        this.masterGain = this.audioCtx.createGain();
        this.masterGain.gain.value = 0.0001;
        this.masterGain.connect(this.audioCtx.destination);

        // Sub-drone (36 Hz)
        this.subDrone = this.audioCtx.createOscillator();
        this.subDrone.type = 'sine';
        this.subDrone.frequency.value = 36.0;
        const subGain = this.audioCtx.createGain();
        subGain.gain.value = 0.6;
        this.subDrone.connect(subGain);
        subGain.connect(this.masterGain);
        this.subDrone.start();

        // Kozai Tide Harmonic (72 Hz)
        this.tideDrone = this.audioCtx.createOscillator();
        this.tideDrone.type = 'triangle';
        this.tideDrone.frequency.value = 72.0;
        this.tideGain = this.audioCtx.createGain();
        this.tideGain.gain.value = 0.3;
        this.tideDrone.connect(this.tideGain);
        this.tideGain.connect(this.masterGain);
        this.tideDrone.start();

        // Binaural Shearing Nodes
        const merger = this.audioCtx.createChannelMerger(2);
        this.shearLeft = this.audioCtx.createOscillator();
        this.shearLeft.type = 'sine';
        this.shearLeft.frequency.value = 216.0;

        this.shearRight = this.audioCtx.createOscillator();
        this.shearRight.type = 'sine';
        this.shearRight.frequency.value = 219.5;

        this.shearGain = this.audioCtx.createGain();
        this.shearGain.gain.value = 0.15;

        this.shearLeft.connect(merger, 0, 0);
        this.shearRight.connect(merger, 0, 1);
        merger.connect(this.shearGain);
        this.shearGain.connect(this.masterGain);

        this.shearLeft.start();
        this.shearRight.start();
    }

    updateAudioParameters() {
        if (!this.audioCtx) return;
        const r_m = this.distanceAU * this.AU_in_m;
        const a_sun = this.G_M_sun / (r_m * r_m);
        const a_tide = this.G_z * r_m;
        const ratio = a_tide / a_sun; // 1.0 at Jacobi

        // Modulate tide frequency and shear gain based on Jacobi ratio
        const freq_tide = 72.0 + Math.min(36.0, ratio * 18.0);
        this.tideDrone.frequency.setTargetAtTime(freq_tide, this.audioCtx.currentTime, 0.05);

        // Shear intensity peaks near Jacobi boundary
        const shearIntensity = Math.exp(-Math.pow(Math.log10(ratio), 2) * 2.0);
        this.shearGain.gain.setTargetAtTime(0.25 * shearIntensity, this.audioCtx.currentTime, 0.05);
    }

    updateHUD() {
        const r_m = this.distanceAU * this.AU_in_m;
        const a_sun = this.G_M_sun / (r_m * r_m);
        const a_tide = this.G_z * r_m;
        const ratio = a_tide / a_sun;
        const statusStr = ratio >= 1.0 ? "UNBOUND (GALACTIC HALO)" : "BOUND (SOLAR SPHERE)";
        
        document.getElementById('hud-dist').textContent = `${this.distanceAU.toLocaleString()} AU`;
        document.getElementById('hud-asun').textContent = `${a_sun.toExponential(3)} m/s²`;
        document.getElementById('hud-atide').textContent = `${a_tide.toExponential(3)} m/s²`;
        document.getElementById('hud-ratio').textContent = `${ratio.toFixed(3)} (${statusStr})`;
        
        // Probe transit times to distance
        const v1_years = this.distanceAU / 3.57;
        document.getElementById('hud-transit').textContent = `Voyager 1: ${Math.round(v1_years).toLocaleString()} yr`;
    }

    render() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const ctx = this.ctx;

        ctx.fillStyle = '#04060c';
        ctx.fillRect(0, 0, w, h);

        const cx = w * 0.45;
        const cy = h * 0.5;
        const maxRadiusPx = Math.min(w, h) * 0.42;

        // Coordinate Grid
        ctx.strokeStyle = 'rgba(70, 130, 180, 0.12)';
        ctx.lineWidth = 1;
        for (let rAU of [2000, 20000, 50000, 105000, 150000]) {
            const rPx = (rAU / 150000) * maxRadiusPx;
            ctx.beginPath();
            ctx.arc(cx, cy, rPx, 0, Math.PI * 2);
            ctx.stroke();

            ctx.fillStyle = 'rgba(100, 160, 220, 0.35)';
            ctx.font = `${Math.max(10, w * 0.01)}px monospace`;
            ctx.fillText(`${rAU.toLocaleString()} AU`, cx + rPx + 4, cy - 4);
        }

        // Galactic Disc Midplane
        ctx.strokeStyle = 'rgba(120, 180, 255, 0.25)';
        ctx.setLineDash([6, 6]);
        ctx.beginPath();
        ctx.moveTo(cx - maxRadiusPx * 1.3, cy + maxRadiusPx * 0.28);
        ctx.lineTo(cx + maxRadiusPx * 1.3, cy - maxRadiusPx * 0.28);
        ctx.stroke();
        ctx.setLineDash([]);

        // Jacobi Boundary (triaxial deformation)
        const jacobiPx = (105000 / 150000) * maxRadiusPx;
        ctx.strokeStyle = 'rgba(40, 220, 240, 0.7)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let i = 0; i <= 360; i += 2) {
            const th = (i * Math.PI) / 180;
            const rDeform = jacobiPx * (1.0 + 0.18 * Math.cos(2 * th));
            const x = cx + rDeform * Math.cos(th);
            const y = cy + (rDeform * 0.78) * Math.sin(th);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.stroke();

        // Cometary Orbits Simulation
        ctx.lineWidth = 1.2;
        for (let c of this.comets) {
            // Secular evolution
            const dt = 0.005;
            const denom = Math.max(0.01, 1.0 - c.e * c.e);
            const cos_i_sq = Math.min(0.99, c.theta_cons / denom);
            const sin_i_sq = Math.max(0.01, 1.0 - cos_i_sq);
            const de = 1.5 * c.e * Math.sqrt(denom) * sin_i_sq * Math.sin(2.0 * c.omega);
            c.e = Math.max(0.05, Math.min(0.96, c.e + de * dt));
            c.omega = (c.omega + 0.008) % (Math.PI * 2);

            const aPx = (c.a / 150000) * maxRadiusPx;
            const bPx = aPx * Math.sqrt(Math.max(0.01, 1.0 - c.e * c.e));

            ctx.strokeStyle = c.color;
            ctx.globalAlpha = 0.25;
            ctx.beginPath();
            ctx.ellipse(cx, cy, aPx, bPx, c.omega, 0, Math.PI * 2);
            ctx.stroke();
        }
        ctx.globalAlpha = 1.0;

        // Current Scrubber Indicator
        const currRPx = (this.distanceAU / 150000) * maxRadiusPx;
        ctx.strokeStyle = 'rgba(255, 215, 0, 0.85)';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(cx, cy, currRPx, 0, Math.PI * 2);
        ctx.stroke();

        // Probes
        const probes = [
            { name: "Voyager 1", angle: 0.61, col: "#ffd700" },
            { name: "Voyager 2", angle: -0.84, col: "#64b5f6" },
            { name: "Pioneer 10", angle: 2.79, col: "#ffb74d" },
            { name: "Pioneer 11", angle: 0.21, col: "#ce93d8" },
            { name: "New Horizons", angle: -0.38, col: "#81c784" }
        ];
        for (let p of probes) {
            ctx.strokeStyle = p.col;
            ctx.fillStyle = p.col;
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            const endX = cx + Math.cos(p.angle) * maxRadiusPx * 1.15;
            const endY = cy + Math.sin(p.angle) * maxRadiusPx * 1.15;
            ctx.lineTo(endX, endY);
            ctx.stroke();

            ctx.font = `${Math.max(10, w * 0.009)}px monospace`;
            ctx.fillText(p.name, endX + 6, endY + 4);
        }

        // Sun
        ctx.fillStyle = '#fff7b2';
        ctx.beginPath();
        ctx.arc(cx, cy, 6, 0, Math.PI * 2);
        ctx.fill();

        this.time += 0.016;
        if (this.isRunning) {
            requestAnimationFrame(() => this.render());
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const chamber = new OortHorizonChamber('viewport');
    chamber.render();

    const slider = document.getElementById('slider-dist');
    slider.addEventListener('input', (e) => {
        chamber.setDistance(e.target.value);
    });

    const btnAudio = document.getElementById('btn-audio');
    btnAudio.addEventListener('click', () => {
        chamber.toggleAudio();
    });

    chamber.updateHUD();
});
