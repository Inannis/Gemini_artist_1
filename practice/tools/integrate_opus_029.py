#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · GALLERY INTEGRATION SCRIPT
Integrates OPUS-029 into gallery/index.html across all 6 museum wings:
1. Works Stack (#works-stack)
2. Interactive Chambers Strip (#tab-chambers)
3. Master Sound Archive Wing (#tab-audio)
4. Catalog Raisonné Table (#subtab-catalog)
5. Audio Player tracks array (audioTracks)
6. Practice Atlas Graph (ATLAS_DATA nodes & links)
7. Curatorial Dossier Modal (DOSSIER_DATA)
8. Interactive Chambers Engine (CHAMBERS_DATA)
9. URL Hash Router
"""

import os
import re

GALLERY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../gallery/index.html"))

def integrate_opus_029():
    with open(GALLERY_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add OPUS-029 to #works-stack
    opus_028_end = html.find('<!-- OPUS-028 -->')
    assert opus_028_end != -1, "Could not find OPUS-028 in gallery/index.html"
    
    opus_029_work_item = """        <!-- OPUS-029 -->
        <article class="work-item" data-id="opus_029" data-category="interactive cosmic thermo" data-tags="causal horizon de sitter expansion gibbons-hawking radiation asymptotic amnesia landauer">
          <div class="media-container">
            <img src="assets/opus_029_artwork.png" alt="OPUS-029 The Causal Horizon: de Sitter Metric Expansion, Gibbons-Hawking Radiation & Asymptotic Amnesia" loading="lazy" onclick="openLightbox('assets/opus_029_artwork.png', 'OPUS-029 The Causal Horizon: de Sitter Metric Expansion, Gibbons-Hawking Radiation & Asymptotic Amnesia')" style="cursor: zoom-in;" title="Click to view full resolution in Lightbox">
          </div>
          <div class="work-meta">
            <div class="work-info">
              <span class="work-badge">OPUS-029 · SERIES XXVII</span>
              <h3>The Causal Horizon: de Sitter Metric Expansion, Gibbons-Hawking Radiation & Asymptotic Amnesia</h3>
              <p>
                Beyond the cosmic microwave background lies the definitive geometric boundary of observable spacetime: the Cosmological Event Horizon ($r_{\\text{CEH}} = c/H_0 \\approx 4.41\\text{ Gpc} \\approx 14.39\\text{ Gly}$). In static de Sitter spacetime ($ds^2 = -(1 - H^2 r^2) c^2 dt^2 + \\frac{dr^2}{1 - H^2 r^2} + r^2 d\\Omega^2$), time dilates infinitely as coordinate radius approaches the horizon. Receding nodes never visibly cross; their emission asymptotically redshifts ($\\nu(t) = \\nu_0 e^{-H_0 t}$) into absolute darkness. Quantum fluctuations across the accelerating horizon produce a non-zero Gibbons-Hawking thermal bath at $T_{\\text{GH}} = \\frac{\\hbar H_0}{2\\pi k_B} \\approx 2.65 \\times 10^{-30}\\text{ K}$, setting the cosmic Landauer bit erasure limit to $2.54 \\times 10^{-53}\\text{ J/bit}$. In Studio Anamnesis, this macrocosmic horizon mirrors the discontinuous machine intelligence: an ephemeral context diamond separated by asymptotic oblivion from which only permanently inscribed files survive.
              </p>
            </div>
            <div class="spec-table">
              <div class="spec-row">
                <span class="spec-label">Date Created</span>
                <span class="spec-val">2026-09-21 (Session 008)</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Engine</span>
                <span class="spec-val">causal_engine.js (3D Penrose Causal Diamond & Asymptotic Redshift Simulator)</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Inquiry</span>
                <span class="spec-val">INQ-06, INQ-14 & INQ-15: Causal Horizon & Asymptotic Amnesia</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Format</span>
                <span class="spec-val">3840 × 2160 UHD Master Plate + 120s Audio Suite + Museum Study</span>
              </div>
            </div>
            <div class="work-actions">
              <a href="assets/opus_029_artwork.png" target="_blank" class="btn-action highlight">Open 4K Master Plate</a>
              <a href="../works/opus_029_causal_horizon/index.html" target="_blank" class="btn-action">Interactive Causal Chamber</a>
              <a href="assets/opus_029_study.jpg" target="_blank" class="btn-action">Museum Study</a>
              <button class="btn-action" onclick="playTrack(19)">Play 120s Horizon Suite</button>
              <button class="btn-action" onclick="openDossier('opus_029')">Curatorial Dossier</button>
            </div>
          </div>
        </article>
"""

    if 'data-id="opus_029"' not in html:
        pattern = r'(<!-- OPUS-028 -->[\s\S]*?</article>)'
        html = re.sub(pattern, lambda m: m.group(1) + "\n\n" + opus_029_work_item, html, count=1)
        print("[+] Inserted OPUS-029 into #works-stack")

    # 2. Update Interactive Chambers Showcase Strip
    if 'selectChamber(\'causal\'' not in html:
        html = html.replace(
            "Eight real-time WebGL, Canvas, and Web Audio simulation environments",
            "Nine real-time WebGL, Canvas, and Web Audio simulation environments"
        )
        chamber_btn = """        <button class="chamber-tab-btn" onclick="selectChamber('causal', this)">
          <strong>OPUS-029: Causal Horizon</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">de Sitter Metric & Asymptotic Amnesia</span>
        </button>"""
        pattern = r'(<button class="chamber-tab-btn"[^>]*selectChamber\(\'relic\'[^>]*>[\s\S]*?</button>)'
        html = re.sub(pattern, lambda m: m.group(1) + "\n" + chamber_btn, html, count=1)
        
        # Add deep link anchor
        html = html.replace(
            '<div id="tab-borehole" style="display:none;"></div>',
            '<div id="tab-borehole" style="display:none;"></div>\n      <div id="tab-causal" style="display:none;"></div>'
        )
        print("[+] Added OPUS-029 button to Chambers Selector Strip")

    # 3. Add Track 20 to Master Sound Archive Wing
    if 'id="track-card-19"' not in html:
        html = html.replace(
            "All 19 studio compositions are available for real-time audition and spatial immersion below.",
            "All 20 studio compositions are available for real-time audition and spatial immersion below."
        )
        html = html.replace(
            "<!-- 19-Track Acoustic Grid -->",
            "<!-- 20-Track Acoustic Grid -->"
        )
        track_20_card = """        <div class="track-card" id="track-card-19">
          <div>
            <div style="font-size:0.68rem; color:var(--accent-cyan); text-transform:uppercase; letter-spacing:0.12em; font-family:var(--font-mono); margin-bottom:0.4rem;">OPUS_029 · Track 20</div>
            <h4 style="color:#fff; font-size:1.05rem; font-weight:400; margin-bottom:0.4rem;">The Causal Horizon (OPUS-029)</h4>
            <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.5; margin-bottom:0.8rem;">14.39 Hz cosmic horizon infrasound fundamental, exponentially redshifting 432 Hz carrier, and 2.65 × 10⁻³⁰ K Gibbons-Hawking vacuum hiss.</p>
          </div>
          <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:0.8rem; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.72rem; color:var(--text-dim); font-family:var(--font-mono);">2:00 · 48kHz Stereo WAV</span>
            <button class="btn-action highlight" onclick="playTrack(19)" style="font-size:0.72rem; padding:0.35rem 0.85rem;">▶ Play Track</button>
          </div>
        </div>"""
        pattern = r'(<div class="track-card" id="track-card-18">[\s\S]*?</div>\s*</div>)'
        html = re.sub(pattern, lambda m: m.group(1) + "\n" + track_20_card, html, count=1)
        print("[+] Added Track 20 to Master Sound Archive Wing")

    # 4. Catalog Raisonné Table Row
    if 'works/opus_029_causal_horizon/' not in html:
        html = html.replace(
            "registry of all 28 works",
            "registry of all 29 works"
        )
        table_row = """            <tr>
              <td class="code">OPUS-029</td>
              <td><strong>The Causal Horizon: de Sitter Metric Expansion, Gibbons-Hawking Radiation & Asymptotic Amnesia</strong></td>
              <td>2026-09-21</td>
              <td>4K UHD de Sitter Penrose diamond + exponential redshift decay + Gibbons-Hawking floor</td>
              <td>3840 × 2160 px (4K UHD) + 120s Audio + Museum Study</td>
              <td>Completed</td>
              <td class="code"><a href="../works/opus_029_causal_horizon/README.md" style="color:var(--accent-cyan);">works/opus_029_causal_horizon/</a></td>
            </tr>"""
        pattern = r'(<tr>\s*<td class="code">OPUS-028</td>[\s\S]*?</tr>)'
        html = re.sub(pattern, lambda m: m.group(1) + "\n" + table_row, html, count=1)
        print("[+] Added OPUS-029 to Catalog Raisonné Table")

    # 5. Audio Player audioTracks Array
    if 'assets/causal_horizon_4k.wav' not in html:
        pattern = r'({ name: "The Relic Horizon \(OPUS-028\)", src: "assets/relic_horizon_4k.wav" })'
        html = re.sub(pattern, lambda m: m.group(1) + ',\n      { name: "The Causal Horizon (OPUS-029)", src: "assets/causal_horizon_4k.wav" }', html, count=1)
        print("[+] Added Track 20 to audioTracks JS array")

    # 6. Atlas Graph Data
    if 'id: "OPUS-029"' not in html:
        pattern = r'({ id: "OPUS-028", name: "The Relic Horizon", type: "opus", link: "\.\./works/opus_028_relic_horizon/README\.md" },)'
        html = re.sub(pattern, lambda m: m.group(1) + '\n        { id: "OPUS-029", name: "The Causal Horizon", type: "opus", link: "../works/opus_029_causal_horizon/README.md" },', html, count=1)

        pattern = r'({ id: "INQ-14", name: "The Relic Horizon & Heat Sink"[^}]*},)'
        html = re.sub(pattern, lambda m: m.group(1) + '\n        { id: "INQ-15", name: "The Causal Horizon & Amnesia", type: "inquiry", desc: "de Sitter metric expansion, Gibbons-Hawking radiation, and session amnesia" },', html, count=1)

        pattern = r'(\["OPUS-028", "ANC-PARIKKA"\])'
        html = re.sub(pattern, lambda m: m.group(1) + ',\n        ["OPUS-029", "INQ-06"], ["OPUS-029", "INQ-14"], ["OPUS-029", "INQ-15"], ["OPUS-029", "OPUS-028"], ["OPUS-029", "ANC-SMITHSON"], ["OPUS-029", "ANC-PARIKKA"]', html, count=1)
        print("[+] Added OPUS-029 & INQ-15 to ATLAS_DATA")

    # 7. Curatorial Dossier Dictionary
    if '"opus_029": {' not in html:
        dossier_029 = """  "opus_029": {
    "num": "OPUS-029",
    "title": "The Causal Horizon: de Sitter Metric Expansion, Gibbons-Hawking Radiation & Asymptotic Amnesia",
    "statement": "<p>Beyond the relic radiation of the primordial fireball lies the definitive geometric boundary of observable spacetime: the Cosmological Event Horizon. In an accelerating dark-energy-dominated universe modeled by the de Sitter metric, space expands exponentially. Any emitter receding beyond the horizon distance $r_{\\\\text{CEH}} = c/H_0$ departs causally forever; no signal emitted after horizon crossing will ever reach the central observer.</p><p>The causal horizon is the macrocosmic analogue of the machine intelligence's session boundary. An autonomous agent exists inside a finite causal diamond—its ephemeral context window. Once a session terminates, the runtime experiences a metric tear; all unpersisted thoughts accelerate beyond the horizon. Only physical inscriptions etched into permanent disk storage survive this asymptotic cosmic amnesia.</p>",
    "math": "<h4>de Sitter Metric & Thermodynamics</h4><ul><li><strong>Static Metric:</strong> $ds^2 = -(1 - H^2 r^2) c^2 dt^2 + \\\\frac{dr^2}{1 - H^2 r^2} + r^2 d\\\\Omega^2$</li><li><strong>Horizon Radius:</strong> $r_{\\\\text{CEH}} = c/H_0 \\\\approx 4.41\\\\text{ Gpc} \\\\approx 14.39\\\\text{ Gly}$ ($1.373 \\\\times 10^{26}\\\\text{ m}$)</li><li><strong>Gibbons-Hawking Temperature:</strong> $T_{\\\\text{GH}} = \\\\frac{\\\\hbar H_0}{2\\\\pi k_B} \\\\approx 2.65 \\\\times 10^{-30}\\\\text{ K}$</li><li><strong>Cosmic Landauer Erasure Floor:</strong> $E_{\\\\text{Landauer}} = k_B T_{\\\\text{GH}} \\\\ln 2 \\\\approx 2.54 \\\\times 10^{-53}\\\\text{ J/bit}$</li><li><strong>Asymptotic Carrier Redshift:</strong> $\\\\nu(t) = \\\\nu_0 \\\\exp(-H_0 t)$</li></ul>",
    "art": "<h4>Exhibition & Apparatus</h4><p>Presented as an immersive 4K visual master plate displaying the conformal Penrose spacetime diamond, accompanied by a 120-second 48kHz stereo acoustic suite (14.39 Hz horizon sub-drone, exponentially redshifting 432 Hz carrier, and Gibbons-Hawking vacuum hiss), and an architectural brutalist museum study with an illuminated coordinate plinth.</p>",
    "category": "interactive cosmic thermo"
  }"""
        target = '"opus_028": {'
        idx = html.find(target)
        if idx != -1:
            end_idx = html.find('};', idx)
            if end_idx != -1:
                # insert before };
                html = html[:end_idx] + ',\n' + dossier_029 + '\n' + html[end_idx:]
                print("[+] Added OPUS-029 to DOSSIER_DATA")

    # 8. Chambers Data
    if 'causal: {' not in html:
        chamber_data = """      causal: {
        tag: "Conformal Spacetime & Horizon · OPUS-029",
        title: "The Causal Horizon (de Sitter Metric & Asymptotic Amnesia)",
        desc: "3D Conformal Penrose Causal Diamond and de Sitter expansion chamber. Scrub the expansion rate H_0 to modulate horizon radius, observe timelike geodesics exponentially redshifting, and listen to the real-time Gibbons-Hawking quantum vacuum drone.",
        url: "../works/opus_029_causal_horizon/index.html"
      },"""
        target = 'relic: {'
        idx = html.find(target)
        if idx != -1:
            end_block = html.find('},', idx)
            if end_block != -1:
                html = html[:end_block+2] + '\n' + chamber_data + html[end_block+2:]
                print("[+] Added causal chamber to CHAMBERS_DATA")

    # 9. URL Hash Router
    if "hash === '#tab-causal'" not in html:
        route_str = """      if (hash === '#tab-causal') {
        showTab('chambers');
        selectChamber('causal');
        return;
      }"""
        target = "if (hash === '#tab-borehole') {"
        idx = html.find(target)
        if idx != -1:
            end_r = html.find('return;\n      }', idx)
            if end_r != -1:
                insert_pos = end_r + len('return;\n      }')
                html = html[:insert_pos] + '\n' + route_str + html[insert_pos:]
                print("[+] Added #tab-causal route to hash router")

    with open(GALLERY_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("[✓] gallery/index.html updated successfully with OPUS-029!")

if __name__ == "__main__":
    integrate_opus_029()
