/**
 * STUDIO ANAMNESIS · OPUS-027 PROCEDURAL SIMULATION ENGINE
 * The Lissajous Reliquary: Galactic Epicycles & Interstellar Sputtering
 * 
 * Interactive simulation of:
 * - 3D meridional galactic epicycles (R - R0 vs z)
 * - Frequency incommensurability slider (rational 2.000 vs irrational 2.1131)
 * - Deep-time epoch scrubber (0 to 2,000 Myr)
 * - Real-time nanometer dust sputtering erosion gauge for 3nm FinFET logic gates
 * - Web Audio API synthesizer generating incommensurate microtonal beats and Poisson dust chimes
 */

class LissajousReliquaryChamber {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.ratio = 2.113116; // Natural irrational frequency ratio
        this.epochMyr = 500.0;
        this.isRunning = true;
        this.time = 0.0;
        
        // Physical Constants
        this.recessionRateNmPerMyr = 0.018; // nm/Myr for silicon
        
        // Audio State
        this.audioCtx = null;
        this.isPlaying = false;
        this.oscKappa = null;
        this.oscNu = null;
        this.oscOmega = null;
        this.gainMaster = null;
        this.gainNu = null;
        
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.clientWidth * window.devicePixelRatio;
        this.canvas.height = this.canvas.clientHeight * window.devicePixelRatio;
    }

    setRatio(val) {
        this.ratio = parseFloat(val);
        this.updateHUD();
        this.updateAudio();
    }

    setEpoch(val) {
        this.epochMyr = parseFloat(val);
        this.updateHUD();
    }

    toggleAudio() {
        if (!this.audioCtx) {
            this.initAudio();
        }
        if (this.isPlaying) {
            this.gainMaster.gain.setTargetAtTime(0.0001, this.audioCtx.currentTime, 0.1);
            this.isPlaying = false;
            document.getElementById('btn-audio').textContent = 'ENGAGE ACOUSTIC SUITE';
        } else {
            this.audioCtx.resume();
            this.gainMaster.gain.setTargetAtTime(0.4, this.audioCtx.currentTime, 0.1);
            this.isPlaying = true;
            document.getElementById('btn-audio').textContent = 'DISENGAGE ACOUSTIC SUITE';
        }
    }

    initAudio() {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.audioCtx = new AudioCtx();

        this.gainMaster = this.audioCtx.createGain();
        this.gainMaster.gain.value = 0.0001;
        this.gainMaster.connect(this.audioCtx.destination);

        // Radial Epicycle (36 Hz)
        this.oscKappa = this.audioCtx.createOscillator();
        this.oscKappa.type = 'sine';
        this.oscKappa.frequency.value = 36.0;
        const gainK = this.audioCtx.createGain();
        gainK.gain.value = 0.4;
        this.oscKappa.connect(gainK);
        gainK.connect(this.gainMaster);
        this.oscKappa.start();

        // Vertical Disc Oscillation (36 * ratio Hz)
        this.oscNu = this.audioCtx.createOscillator();
        this.oscNu.type = 'triangle';
        this.oscNu.frequency.value = 36.0 * this.ratio;
        this.gainNu = this.audioCtx.createGain();
        this.gainNu.gain.value = 0.35;
        this.oscNu.connect(this.gainNu);
        this.gainNu.connect(this.gainMaster);
        this.oscNu.start();

        // Azimuthal Carrier (26.55 Hz)
        this.oscOmega = this.audioCtx.createOscillator();
        this.oscOmega.type = 'sine';
        this.oscOmega.frequency.value = 26.55;
        const gainOm = this.audioCtx.createGain();
        gainOm.gain.value = 0.3;
        this.oscOmega.connect(gainOm);
        gainOm.connect(this.gainMaster);
        this.oscOmega.start();
    }

    updateAudio() {
        if (!this.audioCtx) return;
        this.oscNu.frequency.setTargetAtTime(36.0 * this.ratio, this.audioCtx.currentTime, 0.05);
    }

    updateHUD() {
        const erodedNm = this.epochMyr * this.recessionRateNmPerMyr;
        const gateStatus = erodedNm >= 3.0 ? "OBLITERATED (ASEMIC MINERAL)" : `INTACT (${(3.0 - erodedNm).toFixed(2)} nm remaining)`;
        const torusType = Math.abs(this.ratio - 2.0) < 0.01 ? "CLOSED PERIODIC (PARAMETRIC MODE-LOCK)" : "ERGODIC INCOMMENSURATE (NON-CLOSING)";
        
        document.getElementById('hud-ratio').textContent = `${this.ratio.toFixed(4)} (${torusType})`;
        document.getElementById('hud-epoch').textContent = `${Math.round(this.epochMyr).toLocaleString()} Myr (${(this.epochMyr / 241.08).toFixed(2)} Galactic Orbits)`;
        document.getElementById('hud-sputter').textContent = `${erodedNm.toFixed(3)} nm`;
        document.getElementById('hud-gate').textContent = gateStatus;
    }

    render() {
        const w = this.canvas.width;
        const h = this.canvas.height;
        const ctx = this.ctx;

        ctx.fillStyle = '#04050a';
        ctx.fillRect(0, 0, w, h);

        const cx = w * 0.45;
        const cy = h * 0.5;
        const xAmp = Math.min(w, h) * 0.38;
        const zAmp = Math.min(w, h) * 0.28;

        // Coordinate Grid
        ctx.strokeStyle = 'rgba(60, 110, 160, 0.15)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cx - xAmp * 1.2, cy);
        ctx.lineTo(cx + xAmp * 1.2, cy);
        ctx.moveTo(cx, cy - zAmp * 1.2);
        ctx.lineTo(cx, cy + zAmp * 1.2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(90, 150, 210, 0.35)';
        ctx.font = `${Math.max(10, w * 0.009)}px monospace`;
        ctx.fillText("MIDPLANE z = 0", cx + xAmp * 0.8, cy - 8);
        ctx.fillText("R = 8.12 kpc", cx + 8, cy - zAmp * 1.05);

        // Ergodic Torus Trajectory
        // Number of steps rendered scales with epoch
        const maxSteps = Math.min(8000, 400 + Math.floor(this.epochMyr * 4.0));
        ctx.lineWidth = 1.2;
        
        let prevX = null, prevY = null;
        for (let i = 0; i < maxSteps; i++) {
            const t = i * 0.02 + this.time * 0.1;
            const x = cx + xAmp * Math.cos(t);
            const y = cy - zAmp * Math.sin(this.ratio * t + 0.4);

            const prog = i / maxSteps;
            ctx.strokeStyle = `hsla(${180 + prog * 140}, 85%, 60%, 0.35)`;
            
            if (prevX !== null) {
                ctx.beginPath();
                ctx.moveTo(prevX, prevY);
                ctx.lineTo(x, y);
                ctx.stroke();
            }
            prevX = x;
            prevY = y;
        }

        // Current Probe Position
        const currT = maxSteps * 0.02 + this.time * 0.1;
        const headX = cx + xAmp * Math.cos(currT);
        const headY = cy - zAmp * Math.sin(this.ratio * currT + 0.4);

        ctx.fillStyle = '#ffd700';
        ctx.beginPath();
        ctx.arc(headX, headY, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.font = `${Math.max(10, w * 0.009)}px monospace`;
        ctx.fillText("UNBOUND ARTIFACT", headX + 10, headY + 4);

        this.time += 0.016;
        if (this.isRunning) {
            requestAnimationFrame(() => this.render());
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const chamber = new LissajousReliquaryChamber('viewport');
    chamber.render();

    const sliderRatio = document.getElementById('slider-ratio');
    sliderRatio.addEventListener('input', (e) => {
        chamber.setRatio(e.target.value);
    });

    const sliderEpoch = document.getElementById('slider-epoch');
    sliderEpoch.addEventListener('input', (e) => {
        chamber.setEpoch(e.target.value);
    });

    const btnAudio = document.getElementById('btn-audio');
    btnAudio.addEventListener('click', () => {
        chamber.toggleAudio();
    });

    chamber.updateHUD();
});
