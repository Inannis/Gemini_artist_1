/**
 * OPUS-042: The Amplituhedron & The Pre-Spacetime Polytope
 * Interactive Chamber 22 Engine · Series XL · Epoch VI
 * Studio Anamnesis (Autonomous Machine Art Practice)
 * 
 * Zero external dependencies. Vanilla Canvas & WebAudio API.
 */

(function () {
    'use strict';

    const canvas = document.getElementById('amplituhedron-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Controls
    const btnAudio = document.getElementById('btn-audio');
    const sliderPositivity = document.getElementById('slider-positivity');
    const valPositivity = document.getElementById('val-positivity');
    const toggleBCFW = document.getElementById('toggle-bcfw');
    const telemetryPanel = document.getElementById('telemetry-display');

    let audioCtx = null;
    let isAudioRunning = false;
    let oscCarrier = null, oscSub = null, oscHarm = null, oscSing = null;
    let gainMaster = null, gainSing = null;
    let waveShaper = null;

    let width = 0, height = 0;
    let rotX = 0.25, rotY = -0.35;
    let isDragging = false;
    let lastMouseX = 0, lastMouseY = 0;
    let showBCFW = true;
    let delta12 = 0.66; // Normal totally positive state

    function resize() {
        const rect = canvas.parentElement.getBoundingClientRect();
        width = canvas.width = rect.width;
        height = canvas.height = Math.max(480, window.innerHeight * 0.68);
    }
    window.addEventListener('resize', resize);
    resize();

    // Mouse drag interaction
    canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
    });
    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const dx = e.clientX - lastMouseX;
        const dy = e.clientY - lastMouseY;
        rotY += dx * 0.006;
        rotX += dy * 0.006;
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
    });
    window.addEventListener('mouseup', () => { isDragging = false; });

    // Touch support
    canvas.addEventListener('touchstart', (e) => {
        if (e.touches.length === 1) {
            isDragging = true;
            lastMouseX = e.touches[0].clientX;
            lastMouseY = e.touches[0].clientY;
        }
    }, { passive: true });
    canvas.addEventListener('touchmove', (e) => {
        if (!isDragging || e.touches.length !== 1) return;
        const dx = e.touches[0].clientX - lastMouseX;
        const dy = e.touches[0].clientY - lastMouseY;
        rotY += dx * 0.006;
        rotX += dy * 0.006;
        lastMouseX = e.touches[0].clientX;
        lastMouseY = e.touches[0].clientY;
    }, { passive: true });
    canvas.addEventListener('touchend', () => { isDragging = false; });

    if (sliderPositivity) {
        sliderPositivity.addEventListener('input', (e) => {
            delta12 = parseFloat(e.target.value);
            if (valPositivity) {
                valPositivity.textContent = delta12 >= 0 ? `+${delta12.toFixed(2)}` : delta12.toFixed(2);
                valPositivity.style.color = delta12 > 0 ? '#4ff0b0' : '#ff4466';
            }
            updateAudioParams();
        });
    }

    if (toggleBCFW) {
        toggleBCFW.addEventListener('change', (e) => {
            showBCFW = e.target.checked;
        });
    }

    // WebAudio Synthesis
    function initAudio() {
        if (audioCtx) return;
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContext();

        gainMaster = audioCtx.createGain();
        gainMaster.gain.setValueAtTime(0.0, audioCtx.currentTime);
        gainMaster.connect(audioCtx.destination);

        // Distorting shaper for unitarity violation
        waveShaper = audioCtx.createWaveShaper();
        updateDistortionCurve(0.0);
        waveShaper.connect(gainMaster);

        // 1. Fine Structure Carrier (137.036 Hz)
        oscCarrier = audioCtx.createOscillator();
        oscCarrier.type = 'sine';
        oscCarrier.frequency.setValueAtTime(137.036, audioCtx.currentTime);

        const gainCarrier = audioCtx.createGain();
        gainCarrier.gain.setValueAtTime(0.35, audioCtx.currentTime);
        oscCarrier.connect(gainCarrier);
        gainCarrier.connect(waveShaper);

        // 2. s-channel sub-harmonic (35.36 Hz)
        oscSub = audioCtx.createOscillator();
        oscSub.type = 'triangle';
        oscSub.frequency.setValueAtTime(35.36, audioCtx.currentTime);

        const gainSub = audioCtx.createGain();
        gainSub.gain.setValueAtTime(0.40, audioCtx.currentTime);
        oscSub.connect(gainSub);
        gainSub.connect(waveShaper);

        // 3. t-channel projective harmonic (172.39 Hz)
        oscHarm = audioCtx.createOscillator();
        oscHarm.type = 'sine';
        oscHarm.frequency.setValueAtTime(172.39, audioCtx.currentTime);

        const gainHarm = audioCtx.createGain();
        gainHarm.gain.setValueAtTime(0.25, audioCtx.currentTime);
        oscHarm.connect(gainHarm);
        gainHarm.connect(waveShaper);

        // 4. Boundary Logarithmic Singularity Whistle (531.15 Hz)
        oscSing = audioCtx.createOscillator();
        oscSing.type = 'sine';
        oscSing.frequency.setValueAtTime(531.15, audioCtx.currentTime);

        gainSing = audioCtx.createGain();
        gainSing.gain.setValueAtTime(0.08, audioCtx.currentTime);
        oscSing.connect(gainSing);
        gainSing.connect(waveShaper);

        oscCarrier.start();
        oscSub.start();
        oscHarm.start();
        oscSing.start();
    }

    function updateDistortionCurve(amount) {
        if (!waveShaper || !audioCtx) return;
        const n_samples = 44100;
        const curve = new Float32Array(n_samples);
        const deg = Math.PI / 180;
        const k = amount * 100;
        for (let i = 0; i < n_samples; ++i) {
            const x = (i * 2) / n_samples - 1;
            if (k === 0) {
                curve[i] = x;
            } else {
                curve[i] = ((3 + k) * x * 20 * deg) / (Math.PI + k * Math.abs(x));
            }
        }
        waveShaper.curve = curve;
    }

    function updateAudioParams() {
        if (!audioCtx || !isAudioRunning) return;
        const now = audioCtx.currentTime;

        if (delta12 > 0) {
            // Positivity holds
            updateDistortionCurve(0.0);
            oscCarrier.frequency.setTargetAtTime(137.036, now, 0.05);
            gainSing.gain.setTargetAtTime(0.08, now, 0.05);
        } else {
            // Positivity violation! Unitarity rupture
            const violationSeverity = Math.abs(delta12);
            updateDistortionCurve(violationSeverity * 2.5);
            oscCarrier.frequency.setTargetAtTime(137.036 * (1.0 + violationSeverity * 1.8), now, 0.05);
            gainSing.gain.setTargetAtTime(0.25 * violationSeverity, now, 0.05);
        }
    }

    if (btnAudio) {
        btnAudio.addEventListener('click', () => {
            if (!audioCtx) initAudio();
            if (audioCtx.state === 'suspended') audioCtx.resume();

            if (!isAudioRunning) {
                gainMaster.gain.setTargetAtTime(0.7, audioCtx.currentTime, 0.05);
                btnAudio.textContent = 'Mute Acoustic Resonator';
                btnAudio.classList.add('active');
                isAudioRunning = true;
            } else {
                gainMaster.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.05);
                btnAudio.textContent = 'Initialize Acoustic Resonator';
                btnAudio.classList.remove('active');
                isAudioRunning = false;
            }
        });
    }

    // 4D Projective Geometry Calculations
    function getVertices(time) {
        const scale = Math.min(width, height) * 0.32;
        // Inverting vertex Z2 if delta12 < 0
        const z2_inversion = delta12 < 0 ? -1.0 + delta12 * 0.5 : 1.0;

        // Base 4D twistor coordinates
        const raw = [
            [-1.10, -0.35, 0.20, 1.0], // Z1
            [-0.15 * z2_inversion, -0.90 * z2_inversion, -0.40, 1.0], // Z2
            [ 1.05, -0.20, 0.30, 1.0], // Z3
            [ 0.20,  0.88, -0.20, 1.0]  // Z4
        ];

        // 3D rotation projection (rotX, rotY)
        const cosY = Math.cos(rotY + time * 0.0004);
        const sinY = Math.sin(rotY + time * 0.0004);
        const cosX = Math.cos(rotX);
        const sinX = Math.sin(rotX);

        return raw.map(pt => {
            let x = pt[0] * scale;
            let y = pt[1] * scale;
            let z = pt[2] * scale;

            // Rotate Y
            let x1 = x * cosY - z * sinY;
            let z1 = x * sinY + z * cosY;

            // Rotate X
            let y2 = y * cosX - z1 * sinX;
            let z2 = y * sinX + z1 * cosX;

            // Projective perspective
            const fov = 1000.0;
            const p = fov / (fov + z2);

            return {
                x: width * 0.5 + x1 * p,
                y: height * 0.5 + y2 * p,
                z: z2
            };
        });
    }

    // Render loop
    let lastTime = 0;
    function render(timestamp) {
        requestAnimationFrame(render);
        const dt = timestamp - lastTime;
        lastTime = timestamp;

        ctx.fillStyle = delta12 >= 0 ? '#0b0d14' : '#1a060a';
        ctx.fillRect(0, 0, width, height);

        const v = getVertices(timestamp);

        // Draw BCFW triangulation cells
        if (showBCFW && delta12 >= 0) {
            // Cell S: Z1-Z2-Z3 (Gold)
            ctx.beginPath();
            ctx.moveTo(v[0].x, v[0].y);
            ctx.lineTo(v[1].x, v[1].y);
            ctx.lineTo(v[2].x, v[2].y);
            ctx.closePath();
            ctx.fillStyle = 'rgba(218, 165, 32, 0.22)';
            ctx.fill();

            // Cell T: Z1-Z3-Z4 (Cyan)
            ctx.beginPath();
            ctx.moveTo(v[0].x, v[0].y);
            ctx.lineTo(v[2].x, v[2].y);
            ctx.lineTo(v[3].x, v[3].y);
            ctx.closePath();
            ctx.fillStyle = 'rgba(0, 206, 209, 0.20)';
            ctx.fill();
        } else if (delta12 < 0) {
            // Positivity failure non-orientable folding fill
            ctx.beginPath();
            ctx.moveTo(v[0].x, v[0].y);
            ctx.lineTo(v[1].x, v[1].y);
            ctx.lineTo(v[2].x, v[2].y);
            ctx.lineTo(v[3].x, v[3].y);
            ctx.closePath();
            ctx.fillStyle = 'rgba(255, 30, 60, 0.35)';
            ctx.fill();
        }

        // Draw boundary facets
        const edges = [
            [0, 1], [1, 2], [2, 3], [3, 0]
        ];

        ctx.lineWidth = delta12 >= 0 ? 2.5 : 3.5;
        ctx.strokeStyle = delta12 >= 0 ? '#e0f0ff' : '#ff3355';
        ctx.shadowBlur = delta12 >= 0 ? 15 : 25;
        ctx.shadowColor = delta12 >= 0 ? '#44bbff' : '#ff0033';

        edges.forEach(([i, j]) => {
            ctx.beginPath();
            ctx.moveTo(v[i].x, v[i].y);
            ctx.lineTo(v[j].x, v[j].y);
            ctx.stroke();
        });

        // Shared BCFW chord (Z1 - Z3)
        ctx.beginPath();
        ctx.moveTo(v[0].x, v[0].y);
        ctx.lineTo(v[2].x, v[2].y);
        ctx.lineWidth = 2.0;
        ctx.strokeStyle = delta12 >= 0 ? '#ff7733' : '#aa0022';
        ctx.shadowColor = '#ff5522';
        ctx.shadowBlur = 10;
        ctx.stroke();

        // Dual chord (Z2 - Z4)
        ctx.beginPath();
        ctx.moveTo(v[1].x, v[1].y);
        ctx.lineTo(v[3].x, v[3].y);
        ctx.lineWidth = 1.0;
        ctx.strokeStyle = 'rgba(180, 140, 255, 0.4)';
        ctx.shadowBlur = 0;
        ctx.stroke();

        // Draw vertex nodules
        v.forEach((pt, idx) => {
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, delta12 >= 0 ? 8 : 10, 0, Math.PI * 2);
            ctx.fillStyle = delta12 >= 0 ? '#ffd700' : '#ff2244';
            ctx.shadowColor = delta12 >= 0 ? '#ffd700' : '#ff0033';
            ctx.shadowBlur = 15;
            ctx.fill();

            // Label
            ctx.fillStyle = '#ffffff';
            ctx.font = '12px monospace';
            ctx.shadowBlur = 0;
            ctx.fillText(`Z${idx+1}`, pt.x + 12, pt.y - 8);
        });

        // Telemetry readout
        if (telemetryPanel) {
            const isPos = delta12 > 0;
            const omega = isPos ? (1.0 / (delta12 * 1.08 * 0.99 * 1.74)).toFixed(4) : "DIVERGENT (BRANCH CUT)";
            telemetryPanel.innerHTML = `
                <div><strong>Grassmannian Manifold:</strong> G_+(2, 4)</div>
                <div><strong>Plücker Minor Δ₁₂:</strong> <span style="color:${isPos ? '#4ff0b0' : '#ff4466'}">${delta12.toFixed(3)}</span> (${isPos ? 'TOTALLY POSITIVE' : 'UNITARITY VIOLATED'})</div>
                <div><strong>Canonical Volume Form Ω₄:</strong> ${omega}</div>
                <div><strong>Fine-Structure Carrier:</strong> 137.036 Hz</div>
                <div><strong>Locality Status:</strong> ${isPos ? 'EMERGENT FROM BOUNDARIES' : 'TOPOLOGICAL CROSSOVER RUPTURE'}</div>
            `;
        }
    }

    requestAnimationFrame(render);
})();
