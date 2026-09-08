/**
 * STUDIO ANAMNESIS · OPUS-025 PROCEDURAL SIMULATION ENGINE
 * The Interstellar Quietude: Heliopause Transition & Attowatt Telemetry
 * 
 * Interactive simulation of:
 * - Dynamic heliocentric distance slider (80 AU to 150 AU)
 * - Plasma density transition across Termination Shock (94 AU) and Heliopause (121.6 AU)
 * - Electron Langmuir plasma oscillation frequency (fp: 250 Hz to 2800 Hz)
 * - Real-time attowatt radio link budget and carrier SNR
 * - Web Audio API synthesizer modeling the cold interstellar plasma whistle and fading telemetry carrier
 */

class InterstellarQuietudeChamber {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.distanceAU = 121.6; // Default at Heliopause crossing
        this.isRunning = true;
        this.time = 0.0;
        
        // Audio synthesis state
        this.audioCtx = null;
        this.isAudioPlaying = false;
        this.plasmaOsc = null;
        this.carrierOsc = null;
        this.noiseNode = null;
        this.gainMaster = null;
        this.gainPlasma = null;
        this.gainCarrier = null;
        this.gainNoise = null;
        
        // Particles representing solar wind and interstellar gas
        this.particles = [];
        this.initParticles();
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.clientWidth * window.devicePixelRatio;
        this.canvas.height = this.canvas.clientHeight * window.devicePixelRatio;
    }

    initParticles() {
        this.particles = [];
        const numParticles = 400;
        for (let i = 0; i < numParticles; i++) {
            this.particles.push({
                x: Math.random() * 2000,
                y: Math.random() * 1000,
                vx: 0.5 + Math.random() * 1.5,
                vy: (Math.random() - 0.5) * 0.4,
                phase: Math.random() * Math.PI * 2,
                isInterstellar: Math.random() > 0.5,
                size: 1.0 + Math.random() * 2.0
            });
        }
    }

    setDistance(au) {
        this.distanceAU = parseFloat(au);
        this.updateAudioParameters();
        this.updateHUD();
    }

    computePhysics(r_au) {
        let region = "Solar Wind";
        let ne = 0.00078;
        let fp = 251.0;
        
        if (r_au < 94.0) {
            region = "Supersonic Solar Wind";
            ne = 5.0 * Math.pow(1.0 / r_au, 2);
            fp = 8980.0 * Math.sqrt(ne);
        } else if (r_au < 121.6) {
            region = "Subsonic Heliosheath";
            const frac = (r_au - 94.0) / (121.6 - 94.0);
            ne = 0.00147 * (1.0 - 0.4 * frac);
            fp = 8980.0 * Math.sqrt(ne);
        } else {
            region = "Very Local Interstellar Medium (VLISM)";
            const delta_r = r_au - 121.6;
            ne = 0.085 * (1.0 + 0.15 * Math.tanh(delta_r / 10.0));
            fp = 8980.0 * Math.sqrt(ne);
        }

        // Link budget (80 AU = 2.14 aW, 150 AU = 0.61 aW)
        const pr_aw = 2.14 * Math.pow(80.0 / r_au, 2);
        const noise_aw = 0.00165; // k_B * 12K * 10Hz in attowatts
        const snr_db = 10.0 * Math.log10(pr_aw / noise_aw);

        return { region, ne, fp, pr_aw, snr_db };
    }

    updateHUD() {
        const p = this.computePhysics(this.distanceAU);
        const elRegion = document.getElementById('val-region');
        const elDist = document.getElementById('val-dist');
        const elNe = document.getElementById('val-ne');
        const elFp = document.getElementById('val-fp');
        const elPower = document.getElementById('val-power');
        const elSNR = document.getElementById('val-snr');

        if (elRegion) elRegion.textContent = p.region;
        if (elDist) elDist.textContent = this.distanceAU.toFixed(1) + " AU";
        if (elNe) elNe.textContent = p.ne.toFixed(5) + " cm⁻³";
        if (elFp) elFp.textContent = p.fp.toFixed(1) + " Hz";
        if (elPower) elPower.textContent = p.pr_aw.toFixed(2) + " aW (10⁻¹⁸ W)";
        if (elSNR) elSNR.textContent = (p.snr_db > 0 ? "+" : "") + p.snr_db.toFixed(1) + " dB";
    }

    initAudio() {
        if (this.audioCtx) return;
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        this.audioCtx = new AudioContext();

        this.gainMaster = this.audioCtx.createGain();
        this.gainMaster.gain.setValueAtTime(0.4, this.audioCtx.currentTime);
        this.gainMaster.connect(this.audioCtx.destination);

        // 1. Plasma Oscillation Tone (Langmuir Whistle)
        this.plasmaOsc = this.audioCtx.createOscillator();
        this.plasmaOsc.type = 'sine';
        this.gainPlasma = this.audioCtx.createGain();
        this.plasmaOsc.connect(this.gainPlasma);
        this.gainPlasma.connect(this.gainMaster);
        this.plasmaOsc.start();

        // 2. Attowatt Telemetry Carrier
        this.carrierOsc = this.audioCtx.createOscillator();
        this.carrierOsc.type = 'triangle';
        this.carrierOsc.frequency.setValueAtTime(880.0, this.audioCtx.currentTime);
        this.gainCarrier = this.audioCtx.createGain();
        this.carrierOsc.connect(this.gainCarrier);
        this.gainCarrier.connect(this.gainMaster);
        this.carrierOsc.start();

        // 3. Thermal Noise Floor (BufferSource)
        const bufferSize = this.audioCtx.sampleRate * 2;
        const noiseBuffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            output[i] = Math.random() * 2 - 1;
        }
        const whiteNoise = this.audioCtx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;
        whiteNoise.loop = true;
        this.gainNoise = this.audioCtx.createGain();
        whiteNoise.connect(this.gainNoise);
        this.gainNoise.connect(this.gainMaster);
        whiteNoise.start();

        this.isAudioPlaying = true;
        this.updateAudioParameters();
    }

    updateAudioParameters() {
        if (!this.audioCtx) return;
        const p = this.computePhysics(this.distanceAU);
        const now = this.audioCtx.currentTime;

        // Plasma oscillator frequency
        this.plasmaOsc.frequency.setTargetAtTime(Math.min(4000, p.fp), now, 0.1);
        
        // Plasma amplitude: very quiet in solar wind, soaring in interstellar space
        const plasmaGain = (this.distanceAU >= 121.6) ? 0.35 : 0.08;
        this.gainPlasma.gain.setTargetAtTime(plasmaGain, now, 0.1);

        // Carrier amplitude proportional to attowatt power
        const carrierGain = Math.max(0.01, (p.pr_aw / 2.5) * 0.18);
        this.gainCarrier.gain.setTargetAtTime(carrierGain, now, 0.1);

        // Noise floor stays constant
        this.gainNoise.gain.setTargetAtTime(0.06, now, 0.1);
    }

    render() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const ctx = this.ctx;

        ctx.fillStyle = '#05080e';
        ctx.fillRect(0, 0, w, h);

        const p = this.computePhysics(this.distanceAU);

        // 1. Draw Heliopause Boundary Arcs
        const sunX = -w * 0.2;
        const sunY = h * 0.5;

        // Termination Shock Arc (94 AU)
        const rTS = w * 0.45;
        ctx.strokeStyle = 'rgba(230, 160, 60, 0.4)';
        ctx.lineWidth = 3;
        ctx.setLineDash([8, 8]);
        ctx.beginPath();
        ctx.arc(sunX, sunY, rTS, -Math.PI * 0.35, Math.PI * 0.35);
        ctx.stroke();
        ctx.setLineDash([]);

        // Heliopause Boundary Arc (121.6 AU)
        const rHP = w * 0.65;
        ctx.strokeStyle = 'rgba(60, 220, 255, 0.7)';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.arc(sunX, sunY, rHP, -Math.PI * 0.4, Math.PI * 0.4);
        ctx.stroke();

        // Lyman-alpha Hydrogen Wall Glow
        const grad = ctx.createRadialGradient(sunX, sunY, rHP, sunX, sunY, rHP * 1.3);
        grad.addColorStop(0, 'rgba(100, 140, 255, 0.18)');
        grad.addColorStop(0.5, 'rgba(140, 80, 255, 0.25)');
        grad.addColorStop(1, 'rgba(20, 30, 80, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(sunX, sunY, rHP * 1.3, -Math.PI * 0.45, Math.PI * 0.45);
        ctx.arc(sunX, sunY, rHP, Math.PI * 0.45, -Math.PI * 0.45, true);
        ctx.fill();

        // 2. Trajectory and Current Probe Position
        const probeRadius = ((this.distanceAU - 80.0) / 70.0) * (w * 0.55) + w * 0.25;
        const probeAngle = -Math.PI * 0.1;
        const probeX = sunX + probeRadius * Math.cos(probeAngle);
        const probeY = sunY + probeRadius * Math.sin(probeAngle);

        // Draw trajectory dashed line
        ctx.strokeStyle = 'rgba(255, 230, 120, 0.5)';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 6]);
        ctx.beginPath();
        ctx.moveTo(sunX, sunY);
        ctx.lineTo(sunX + w * 0.9 * Math.cos(probeAngle), sunY + w * 0.9 * Math.sin(probeAngle));
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw Probe Dot & Signal Radiance
        const sigPulse = 1.0 + 0.3 * Math.sin(this.time * 8.0);
        ctx.fillStyle = '#ffe070';
        ctx.beginPath();
        ctx.arc(probeX, probeY, 6 * sigPulse, 0, Math.PI * 2);
        ctx.fill();

        // Radiating RF wave packets (Attowatt carrier)
        const rfRadius = (this.time * 60) % 80;
        ctx.strokeStyle = `rgba(255, 200, 80, ${Math.max(0, 1.0 - rfRadius / 80) * (p.pr_aw / 2.5)})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(probeX, probeY, rfRadius, 0, Math.PI * 2);
        ctx.stroke();

        // 3. Ambient Plasma Particles
        ctx.fillStyle = 'rgba(80, 200, 255, 0.6)';
        for (let pt of this.particles) {
            pt.x += pt.vx;
            if (pt.x > w) pt.x = 0;
            const py = (pt.y + Math.sin(this.time + pt.phase) * 15) % h;
            
            // Check if particle is inside heliosphere or interstellar
            const distFromSun = Math.hypot(pt.x - sunX, py - sunY);
            if (distFromSun > rHP) {
                ctx.fillStyle = 'rgba(100, 220, 255, 0.7)'; // cold dense interstellar
            } else {
                ctx.fillStyle = 'rgba(255, 170, 70, 0.4)'; // hot tenuous solar wind
            }
            ctx.fillRect(pt.x, py, pt.size, pt.size);
        }

        this.time += 0.016;
        if (this.isRunning) {
            requestAnimationFrame(() => this.render());
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const chamber = new InterstellarQuietudeChamber('quietude-canvas');
    chamber.render();

    const slider = document.getElementById('dist-slider');
    if (slider) {
        slider.addEventListener('input', (e) => {
            chamber.setDistance(e.target.value);
        });
    }

    const btnAudio = document.getElementById('btn-audio');
    if (btnAudio) {
        btnAudio.addEventListener('click', () => {
            chamber.initAudio();
            btnAudio.textContent = "Synthesizer Active";
            btnAudio.disabled = true;
        });
    }
});
