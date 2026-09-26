/**
 * Chamber 15: The Emergent Bulk Engine
 * Real-time Poincaré Hyperbolic Canvas & WebAudio Holographic Resonator
 * Studio Anamnesis · Series XXXIII · OPUS-035
 */

(function () {
  const canvas = document.getElementById('bulkCanvas');
  const ctx = canvas.getContext('2d');

  // Controls
  const sliderSpanA = document.getElementById('sliderSpanA');
  const sliderSpanB = document.getElementById('sliderSpanB');
  const sliderSep = document.getElementById('sliderSep');
  const sliderCutoff = document.getElementById('sliderCutoff');

  const valSpanA = document.getElementById('valSpanA');
  const valSpanB = document.getElementById('valSpanB');
  const valSep = document.getElementById('valSep');
  const valCutoff = document.getElementById('valCutoff');

  const telemetryPhase = document.getElementById('telemetryPhase');
  const telemetrySa = document.getElementById('telemetrySa');
  const telemetrySb = document.getElementById('telemetrySb');
  const telemetryMi = document.getElementById('telemetryMi');
  const telemetryRmin = document.getElementById('telemetryRmin');

  const audioBtn = document.getElementById('audioToggleBtn');

  // Constants
  const CX = canvas.width / 2;
  const CY = canvas.height / 2;
  const DISK_R = 340;
  const C_CHARGE = 12.0;

  // Audio Context state
  let audioCtx = null;
  let isAudioActive = false;
  let oscBulk = null;
  let oscGeodesic = null;
  let filterNoise = null;
  let gainMaster = null;

  function initAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();

    gainMaster = audioCtx.createGain();
    gainMaster.gain.setValueAtTime(0.25, audioCtx.currentTime);
    gainMaster.connect(audioCtx.destination);

    // Bulk cavity drone
    oscBulk = audioCtx.createOscillator();
    oscBulk.type = 'sine';
    oscBulk.frequency.setValueAtTime(43.2, audioCtx.currentTime);

    const gainBulk = audioCtx.createGain();
    gainBulk.gain.setValueAtTime(0.5, audioCtx.currentTime);
    oscBulk.connect(gainBulk);
    gainBulk.connect(gainMaster);
    oscBulk.start();

    // Ryu-Takayanagi geodesic tension overtone
    oscGeodesic = audioCtx.createOscillator();
    oscGeodesic.type = 'triangle';
    oscGeodesic.frequency.setValueAtTime(172.8, audioCtx.currentTime);

    const gainGeodesic = audioCtx.createGain();
    gainGeodesic.gain.setValueAtTime(0.3, audioCtx.currentTime);
    oscGeodesic.connect(gainGeodesic);
    gainGeodesic.connect(gainMaster);
    oscGeodesic.start();
  }

  function updateAudio(sa, mi, rMin) {
    if (!audioCtx || !isAudioActive) return;
    const now = audioCtx.currentTime;

    // Pitch shift geodesic oscillator with minimal surface length
    const freqGeo = 108.0 + (1.0 - rMin) * 240.0;
    oscGeodesic.frequency.setTargetAtTime(freqGeo, now, 0.05);

    // Modulate bulk fundamental frequency with mutual information
    const freqBulk = 43.2 + mi * 12.0;
    oscBulk.frequency.setTargetAtTime(freqBulk, now, 0.08);
  }

  audioBtn.addEventListener('click', () => {
    if (!audioCtx) initAudio();
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    isAudioActive = !isAudioActive;
    if (isAudioActive) {
      gainMaster.gain.setTargetAtTime(0.28, audioCtx.currentTime, 0.1);
      audioBtn.classList.add('active');
      audioBtn.innerHTML = '<span>Disengage Holographic Resonator</span>';
    } else {
      gainMaster.gain.setTargetAtTime(0.0, audioCtx.currentTime, 0.1);
      audioBtn.classList.remove('active');
      audioBtn.innerHTML = '<span>Engage Holographic Resonator</span>';
    }
  });

  // Calculate Ryu-Takayanagi entropy
  function calcEntropy(dThetaRad, eps) {
    const sinHalf = Math.sin(Math.max(1e-4, dThetaRad / 2));
    const arg = (2.0 / eps) * sinHalf;
    if (arg <= 1.0) return 0.0;
    return (C_CHARGE / 3.0) * Math.log(arg);
  }

  // Draw hyperbolic geodesic arc orthogonal to boundary
  function drawGeodesic(th1, th2, strokeStyle, lineWidth, isDashed) {
    let dTh = Math.abs(th2 - th1);
    if (dTh > Math.PI) dTh = 2 * Math.PI - dTh;
    if (dTh < 0.01 || Math.abs(dTh - Math.PI) < 0.01) {
      // Straight line through origin
      ctx.beginPath();
      ctx.strokeStyle = strokeStyle;
      ctx.lineWidth = lineWidth;
      if (isDashed) ctx.setLineDash([6, 6]); else ctx.setLineDash([]);
      ctx.moveTo(CX + DISK_R * Math.cos(th1), CY + DISK_R * Math.sin(th1));
      ctx.lineTo(CX + DISK_R * Math.cos(th2), CY + DISK_R * Math.sin(th2));
      ctx.stroke();
      ctx.setLineDash([]);
      return;
    }

    let thMid = (th1 + th2) / 2;
    if (Math.abs(th2 - th1) > Math.PI) thMid += Math.PI;

    const cosHalf = Math.cos(dTh / 2);
    const dCenter = 1.0 / cosHalf;
    const rArc = Math.tan(dTh / 2);

    const arcCx = CX + dCenter * DISK_R * Math.cos(thMid);
    const arcCy = CY + dCenter * DISK_R * Math.sin(thMid);
    const arcR = rArc * DISK_R;

    const p1x = CX + DISK_R * Math.cos(th1);
    const p1y = CY + DISK_R * Math.sin(th1);
    const p2x = CX + DISK_R * Math.cos(th2);
    const p2y = CY + DISK_R * Math.sin(th2);

    const startAng = Math.atan2(p1y - arcCy, p1x - arcCx);
    const endAng = Math.atan2(p2y - arcCy, p2x - arcCx);

    ctx.save();
    // Clip to disk interior
    ctx.beginPath();
    ctx.arc(CX, CY, DISK_R, 0, Math.PI * 2);
    ctx.clip();

    ctx.beginPath();
    ctx.strokeStyle = strokeStyle;
    ctx.lineWidth = lineWidth;
    if (isDashed) ctx.setLineDash([5, 5]); else ctx.setLineDash([]);
    ctx.arc(arcCx, arcCy, arcR, startAng, endAng, false);
    ctx.stroke();
    ctx.restore();
  }

  let animTime = 0;

  function render() {
    animTime += 0.015;

    const spanADeg = parseFloat(sliderSpanA.value);
    const spanBDeg = parseFloat(sliderSpanB.value);
    const sepDeg = parseFloat(sliderSep.value);
    const cutoffVal = parseFloat(sliderCutoff.value) / 1000.0;

    valSpanA.textContent = `${spanADeg}°`;
    valSpanB.textContent = `${spanBDeg}°`;
    valSep.textContent = `${sepDeg}°`;
    valCutoff.textContent = cutoffVal.toFixed(3);

    const spanARad = (spanADeg * Math.PI) / 180;
    const spanBRad = (spanBDeg * Math.PI) / 180;
    const sepRad = (sepDeg * Math.PI) / 180;

    // Interval A positioned at [ -sep/2 - spanA, -sep/2 ]
    // Interval B positioned at [ +sep/2, +sep/2 + spanB ]
    const aStart = -sepRad / 2 - spanARad;
    const aEnd = -sepRad / 2;
    const bStart = sepRad / 2;
    const bEnd = sepRad / 2 + spanBRad;

    // Entropies
    const sA = calcEntropy(spanARad, cutoffVal);
    const sB = calcEntropy(spanBRad, cutoffVal);

    // Union interval A U B:
    // Disconnected candidate area: S(A) + S(B)
    // Connected candidate area: S(A U B) = S(interval between aStart and bEnd) + S(interval between aEnd and bStart)
    const spanUnion1 = Math.abs(bEnd - aStart);
    const spanUnion2 = sepRad;
    const sConnected = calcEntropy(spanUnion1, cutoffVal) + calcEntropy(spanUnion2, cutoffVal);
    const sDisconnected = sA + sB;

    const isConnected = sConnected < sDisconnected;
    const mi = Math.max(0, sDisconnected - sConnected);
    const rMin = Math.tan((Math.PI - spanARad) / 4);

    // Telemetry updates
    if (isConnected) {
      telemetryPhase.textContent = 'CONNECTED';
      telemetryPhase.className = 'phase-badge phase-connected';
    } else {
      telemetryPhase.textContent = 'DISCONNECTED';
      telemetryPhase.className = 'phase-badge phase-disconnected';
    }

    telemetrySa.textContent = `${sA.toFixed(2)} k_B`;
    telemetrySb.textContent = `${sB.toFixed(2)} k_B`;
    telemetryMi.textContent = `${mi.toFixed(2)} k_B`;
    telemetryRmin.textContent = `${rMin.toFixed(2)} L_AdS`;

    updateAudio(sA, mi, rMin);

    // Canvas drawing
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Bulk manifold gradient
    const grad = ctx.createRadialGradient(CX, CY, 0, CX, CY, DISK_R);
    grad.addColorStop(0, '#050a16');
    grad.addColorStop(0.7, '#070f24');
    grad.addColorStop(1, '#0c1630');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(CX, CY, DISK_R, 0, Math.PI * 2);
    ctx.fill();

    // 2. Hyperbolic metric distance rings
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.08)';
    ctx.lineWidth = 1;
    for (let rNorm of [0.35, 0.65, 0.85, 0.94, 0.98]) {
      ctx.beginPath();
      ctx.arc(CX, CY, DISK_R * rNorm, 0, Math.PI * 2);
      ctx.stroke();
    }

    // 3. MERA tensor network radial spokes
    ctx.strokeStyle = 'rgba(168, 85, 247, 0.06)';
    for (let i = 0; i < 24; i++) {
      const ang = (i * Math.PI * 2) / 24;
      ctx.beginPath();
      ctx.moveTo(CX, CY);
      ctx.lineTo(CX + DISK_R * Math.cos(ang), CY + DISK_R * Math.sin(ang));
      ctx.stroke();
    }

    // 4. Conformal boundary circle
    ctx.strokeStyle = 'rgba(0, 255, 204, 0.4)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(CX, CY, DISK_R, 0, Math.PI * 2);
    ctx.stroke();

    // 5. Boundary intervals A and B
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#00ffcc';
    ctx.beginPath();
    ctx.arc(CX, CY, DISK_R, aStart, aEnd, false);
    ctx.stroke();

    ctx.strokeStyle = '#f59e0b';
    ctx.beginPath();
    ctx.arc(CX, CY, DISK_R, bStart, bEnd, false);
    ctx.stroke();

    // 6. Ryu-Takayanagi Minimal Surfaces
    // Individual minimal surfaces gamma_A and gamma_B
    drawGeodesic(aStart, aEnd, isConnected ? 'rgba(0, 255, 204, 0.4)' : '#00ffcc', isConnected ? 1.5 : 3.0, isConnected);
    drawGeodesic(bStart, bEnd, isConnected ? 'rgba(245, 158, 11, 0.4)' : '#f59e0b', isConnected ? 1.5 : 3.0, isConnected);

    // Connected minimal surfaces connecting interval boundaries
    drawGeodesic(aStart, bEnd, isConnected ? '#c084fc' : 'rgba(192, 132, 252, 0.3)', isConnected ? 3.0 : 1.5, !isConnected);
    drawGeodesic(aEnd, bStart, isConnected ? '#c084fc' : 'rgba(192, 132, 252, 0.3)', isConnected ? 3.0 : 1.5, !isConnected);

    // 7. Core IR Anchor
    ctx.fillStyle = '#00ffcc';
    ctx.beginPath();
    ctx.arc(CX, CY, 3 + Math.sin(animTime * 2) * 1, 0, Math.PI * 2);
    ctx.fill();

    requestAnimationFrame(render);
  }

  [sliderSpanA, sliderSpanB, sliderSep, sliderCutoff].forEach(input => {
    input.addEventListener('input', () => {});
  });

  render();
})();
