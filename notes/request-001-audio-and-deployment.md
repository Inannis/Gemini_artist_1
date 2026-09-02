# REQUEST-001: Audio Encoding Tools & Web Gallery Hosting Option

**Date:** 2026-09-02  
**From:** Studio Anamnesis  
**To:** Johan  
**Status:** Open / Informational  

---

### 1. Audio Processing Utilities (`ffmpeg`)
- **What is needed:** `ffmpeg` or `libsndfile` available in the container/environment.
- **Purpose:** In OPUS-003, we implemented real-time procedural sound synthesis via the Web Audio API inside the browser. Having `ffmpeg` or Python audio synthesis tools (`scipy`, `soundfile`) would allow the studio to export lossless `.wav` / `.flac` audio suites, generative vinyl simulations, and audiovisual video loops directly to disk as autonomous artifacts.

---

### 2. Gallery Hosting / Git Remote (Optional)
- **What is needed:** If you'd like the permanent exhibition in `gallery/` to be accessible online (for instance via GitHub Pages or a small web server), we can configure the repo's remote or set up a static deploy script.
- **Current state:** `gallery/index.html` is completely standalone and works right now offline by simply double-clicking or opening it in any web browser!
