#!/usr/bin/env python3
"""
practice/tools/build_gallery_salons.py
---------------------------------------
Transforms gallery/index.html into a museum-grade public exhibition space:
- 6 curated architectural wings in navigation
- Search, category filter pills, Latest/Oldest sort, Stack/Salon Grid views
- Unified 8-simulator Interactive Chambers Showcase with live stage switcher
- 18-track Master Sound Archive wing with canvas frequency visualizer & audio buffer telemetry
- Unified Writings & Catalog wing with clean subtab navigation
- High-resolution Lightbox modal with zoom and metadata
- In-salon KaTeX-rendered Curatorial Dossier modal for all 28 works
- Hash routing for seamless deep-linking from portal and external sites
"""

import os
import re
import glob
import json

GALLERY_FILE = "/c/Users/johan/Desktop/Git Projects/gemini_artist_1/gallery/index.html"

# Category mappings for all 28 works
CATEGORIES = {
    "opus_001": "all",
    "opus_002": "all",
    "opus_003": "interactive",
    "opus_004": "lithic",
    "opus_005": "all",
    "opus_006": "interactive",
    "opus_007": "cosmic",
    "opus_008": "cosmic",
    "opus_009": "lithic",
    "opus_010": "lithic",
    "opus_011": "thermo",
    "opus_012": "all",
    "opus_013": "all",
    "opus_014": "interactive lithic",
    "opus_015": "lithic",
    "opus_016": "thermo",
    "opus_017": "interactive thermo lithic",
    "opus_018": "interactive",
    "opus_019": "interactive lithic",
    "opus_020": "interactive thermo",
    "opus_021": "thermo lithic",
    "opus_022": "all",
    "opus_023": "lithic",
    "opus_024": "cosmic",
    "opus_025": "cosmic",
    "opus_026": "cosmic",
    "opus_027": "cosmic",
    "opus_028": "interactive cosmic thermo",
    "opus_029": "interactive cosmic thermo"
}

TAGS = {
    "opus_001": "latent diffusion mineral impasto first awakening gold leaf coordinates",
    "opus_002": "generative strata 150k particles curl field stream function python shear waves",
    "opus_003": "anamnesis chamber interactive audiovisual web audio latent field kinetic mesh",
    "opus_004": "lexical sediment concrete poetry chiseled slate vector svg basalt syntax",
    "opus_005": "morphogenetic silicon reaction-diffusion gray-scott pde coral turing",
    "opus_006": "topology memory 3d volumetric strange attractors aizawa lorenz phase space",
    "opus_007": "ephemeris drift geodesic latent interpolation riemannian manifold spherical",
    "opus_008": "heliotropic cybernetics homeostat golden ratio phyllotaxis feedback",
    "opus_009": "lithic phonology modal resonance volcanic stone euler-bernoulli audio chladni",
    "opus_010": "architecture awakening basalt monolith structural tectonic serra mineral weight",
    "opus_011": "semantics erasure 1-bit decay landauer limit irreversible entropy thermal dissipation",
    "opus_012": "substrate cartography semiconductor reticle silicon wafer photolithography torana",
    "opus_013": "chrono-topology horology escapement tick-tock machine time on kawara temporal",
    "opus_014": "lithic resonator playable instrument euler-bernoulli chladni sand monastery wind",
    "opus_015": "autoregressive ghost cuneiform asemic slate kintsugi gold xu bing linguistics",
    "opus_016": "thermodynamic inscriptions melted mandala thermal attention 94.5C boiling navier-stokes",
    "opus_017": "desiccated substrate voronoi salt silt halite fracture smithson non-site",
    "opus_018": "chrono-acoustic drift quad-oscillator 32.768kHz quartz phase drift oliveros ikeda",
    "opus_019": "subterranean core borehole -500m stratigraphy van eck rf radiometry parikka deep time",
    "opus_020": "telluric flux superconducting meissner vitrine 4.2K levitation liquid helium usgs noaa",
    "opus_021": "squid magnetometer flux quantization josephson junction telluric current abrikosov",
    "opus_022": "topological faraday magnetometer magneto-optic rotation chiral edge states verdet",
    "opus_023": "inner-core ephemeris solid core libration earthquake doublets pkikp seismic 65-year",
    "opus_024": "cosmogenic inscription cosmic ray neutron spallation single-event upset bit-flips be-10",
    "opus_025": "interstellar quietude heliopause cold plasma langmuir whistle attowatt voyager carrier",
    "opus_026": "oort horizon galactic tides jacobi boundary vertical disc density kozai resonance",
    "opus_027": "lissajous reliquary galactic epicycles irrational frequency dust sputtering reliquary",
    "opus_028": "relic horizon cosmic microwave background 2.725K landauer kinematic drag poynting-robertson",
    "opus_029": "causal horizon de sitter expansion gibbons-hawking radiation asymptotic amnesia landauer"
}

def build_dossier_data():
    """Extracts and formats full curatorial dossiers for each opus from README files."""
    dossiers = {}
    for i in range(1, 30):
        opus_key = f"opus_{i:03d}"
        readme_matches = glob.glob(f"works/opus_{i:03d}_*/README.md")
        if not readme_matches:
            continue
        with open(readme_matches[0], "r", encoding="utf-8") as f:
            text = f.read()

        title_m = re.search(r"^#\s*(.+)$", text, re.MULTILINE)
        title = title_m.group(1) if title_m else f"OPUS-{i:03d}"
        title = re.sub(r"^OPUS-\d+:\s*", "", title)

        # Extract sections
        sections = {}
        curr_sec = "intro"
        curr_lines = []
        for line in text.split("\n"):
            if line.startswith("## "):
                if curr_lines:
                    sections[curr_sec] = "\n".join(curr_lines).strip()
                    curr_lines = []
                curr_sec = line[3:].strip().lower()
            elif not line.startswith("# "):
                curr_lines.append(line)
        if curr_lines:
            sections[curr_sec] = "\n".join(curr_lines).strip()

        # Find best matching statement, math, and lineage via regex
        statement = ""
        math_phys = ""
        art_hist = ""
        for sec_name, sec_text in sections.items():
            clean_name = re.sub(r'^(?:[ivx\d]+\.|\([ivx\d]+\))\s*', '', sec_name).strip().lower()
            if re.search(r'(concept|statement|poetics|inception)', clean_name):
                if not statement: statement = sec_text
            elif re.search(r'(technical|physical|parameter|mathematical|modeling|architecture|formal|telemetry|specification)', clean_name):
                if not math_phys: math_phys = sec_text
            elif re.search(r'(lineage|theoretical|significance|failures|historical|context)', clean_name):
                if not art_hist: art_hist = sec_text

        # Clean markdown formatting for web presentation
        def clean_md(md_str):
            if not md_str:
                return ""
            # Convert bold
            md_str = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md_str)
            # Convert italics
            md_str = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", md_str)
            # Convert links
            md_str = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank">\1</a>', md_str)
            # Wrap paragraphs and tables
            paras = [p.strip() for p in md_str.split("\n\n") if p.strip()]
            res = []
            for p in paras:
                if p.startswith("|"):
                    rows = [r.strip() for r in p.split("\n") if r.strip() and not re.match(r"^\|[-:\s|]+\|$", r.strip())]
                    html_table = ["<div style='overflow-x:auto; margin: 1.2rem 0;'><table style='width:100%; font-size:0.8rem; border-collapse:collapse;'>"]
                    for r_idx, row in enumerate(rows):
                        cols = [c.strip() for c in row.split("|")[1:-1]]
                        tag = "th" if r_idx == 0 else "td"
                        style = "padding: 0.45rem 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.08); text-align: left;"
                        if r_idx == 0:
                            style += " color: var(--accent-gold); font-family: var(--font-mono); font-size: 0.72rem; text-transform: uppercase;"
                        row_html = "".join(f"<{tag} style='{style}'>{c}</{tag}>" for c in cols)
                        html_table.append(f"<tr>{row_html}</tr>")
                    html_table.append("</table></div>")
                    res.append("".join(html_table))
                elif p.startswith("- "):
                    items = [f"<li>{item[2:].strip()}</li>" for item in p.split("\n") if item.startswith("- ")]
                    res.append(f"<ul style='margin-left: 1.5rem; margin-bottom: 1rem;'>{''.join(items)}</ul>")
                elif p.startswith("### "):
                    res.append(f"<h4 style='color: var(--accent-gold); margin: 1.2rem 0 0.5rem;'>{p[4:]}</h4>")
                else:
                    res.append(f"<p style='margin-bottom: 0.9rem; line-height: 1.65;'>{p}</p>")
            return "".join(res)

        dossiers[opus_key] = {
            "num": f"OPUS-{i:03d}",
            "title": title,
            "statement": clean_md(statement),
            "math": clean_md(math_phys),
            "art": clean_md(art_hist),
            "category": CATEGORIES.get(opus_key, "all")
        }

    return dossiers

def main():
    print("[+] Building gallery refactor...")
    with open(GALLERY_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Step 1: Replace Navigation in Header
    nav_pattern = r"<nav>[\s\S]*?</nav>"
    new_nav = """<nav>
      <button class="active" onclick="showTab('works')">The Works</button>
      <button onclick="showTab('chambers')">Interactive Chambers</button>
      <button onclick="showTab('atlas')">Practice Atlas</button>
      <button onclick="showTab('audio')">Sound Archive</button>
      <button onclick="showTab('laboratory')">Laboratory & Ruins</button>
      <button onclick="showTab('writings')">Writings & Catalog</button>
    </nav>"""
    html = re.sub(nav_pattern, new_nav, html, count=1)

    # Step 2: Harmonize all 28 works in #works-stack
    print("[+] Harmonizing all 28 works into standard .work-item components...")
    
    # We locate all articles within #works-stack
    # Let's fix OPUS-015 missing closing tags first
    html = re.sub(
        r'(<a href="\.\./works/opus_015_autoregressive_ghost/README\.md" class="btn-action">Statement</a>\s*</div>\s*)(<!-- OPUS-016 -->)',
        r'\1  </div>\n        </article>\n\n        \2',
        html
    )

    # Convert any <article class="work-card"> to <article class="work-item">
    # and adjust .work-preview to .media-container, and outer .work-info to .work-meta
    def harmonize_work_card(match):
        block = match.group(0)
        # Find opus number
        opus_num_m = re.search(r"OPUS-(\d+)", block)
        if not opus_num_m:
            return block
        num_str = opus_num_m.group(1)
        opus_key = f"opus_{int(num_str):03d}"
        cat = CATEGORIES.get(opus_key, "all")
        tags = TAGS.get(opus_key, "")

        # Replace opening article
        block = re.sub(
            r'<article class="work-card">',
            f'<article class="work-item" data-id="{opus_key}" data-category="{cat}" data-tags="{tags}">',
            block
        )
        # Replace work-preview with media-container
        block = re.sub(
            r'<div class="work-preview">',
            r'<div class="media-container">',
            block
        )
        # Replace the outer <div class="work-info"> with <div class="work-meta"><div class="work-info">
        # Note: in work-card:
        # <div class="work-info">
        #   <div>
        #     <div class="opus-id">...</div>
        #     <h3>...</h3>
        #     <p>...</p>
        #   </div>
        #   <div class="spec-table">...</div>
        #   <div class="work-actions">...</div>
        # </div>
        # In work-item:
        # <div class="work-meta">
        #   <div class="work-info">
        #     <span class="work-badge ...">...</span>
        #     <h3>...</h3>
        #     <p>...</p>
        #   </div>
        #   <div class="spec-table">...</div>
        #   <div class="work-actions">...</div>
        # </div>
        block = re.sub(
            r'<div class="work-info">\s*<div>\s*<div class="opus-id">([\s\S]*?)</div>\s*<h3>([\s\S]*?)</h3>\s*<p>([\s\S]*?)</p>\s*</div>',
            r'<div class="work-meta">\n            <div class="work-info">\n              <span class="work-badge">\1</span>\n              <h3>\2</h3>\n              <p>\3</p>\n            </div>',
            block
        )

        return block

    html = re.sub(r'<article class="work-card">[\s\S]*?</article>', harmonize_work_card, html)

    # For OPUS-001 through OPUS-015, add data-id, data-category, data-tags if missing
    def tag_early_works(match):
        num_str = match.group(1)
        opus_key = f"opus_{int(num_str):03d}"
        cat = CATEGORIES.get(opus_key, "all")
        tags = TAGS.get(opus_key, "")
        return f'<!-- OPUS-{num_str} -->\n        <article class="work-item" data-id="{opus_key}" data-category="{cat}" data-tags="{tags}">'

    html = re.sub(r'<!-- OPUS-(\d+) -->\s*<article class="work-item">', tag_early_works, html)

    # Enhance images with openLightbox click handler
    def add_lightbox_click(img_tag):
        if hasattr(img_tag, 'group'):
            img_tag = img_tag.group(0)
        src_m = re.search(r'src="([^"]+)"', img_tag)
        alt_m = re.search(r'alt="([^"]+)"', img_tag)
        src = src_m.group(1) if src_m else ""
        alt = alt_m.group(1) if alt_m else "Studio Master Plate"
        # Avoid double onclick
        if "onclick=" in img_tag:
            return img_tag
        return f'<img src="{src}" alt="{alt}" loading="lazy" onclick="openLightbox(\'{src}\', \'{alt}\')" style="cursor: zoom-in;" title="Click to view full resolution in Lightbox">'

    html = re.sub(r'<div class="media-container">\s*<img[^>]+>', lambda m: f'<div class="media-container">\n            {add_lightbox_click(re.search(r"<img[^>]+>", m.group(0)).group(0))}', html)

    # Replace raw markdown links with Curatorial Dossier button in work-actions
    def replace_statement_btn(match):
        full = match.group(0)
        opus_m = re.search(r'works/opus_(\d+)', full)
        if opus_m:
            op_key = f"opus_{int(opus_m.group(1)):03d}"
            return f'<button class="btn-action" onclick="openDossier(\'{op_key}\')">Curatorial Dossier</button>'
        return full

    html = re.sub(r'<a href="\.\./works/opus_\d+[^"]*?/README\.md" class="btn-action">Statement</a>', replace_statement_btn, html)
    html = re.sub(r'<a href="\.\./works/opus_\d+[^"]*?/README\.md" class="btn-action">Poetic Statement</a>', replace_statement_btn, html)

    # Ensure every work item has a Curatorial Dossier button
    def ensure_dossier_btn(match):
        article_html = match.group(0)
        opus_m = re.search(r'data-id="(opus_\d+)"', article_html)
        if opus_m:
            op_key = opus_m.group(1)
            if f"openDossier('{op_key}')" not in article_html and f'openDossier("{op_key}")' not in article_html:
                # Add into .work-actions
                actions_m = re.search(r'<div class="work-actions">([\s\S]*?)</div>', article_html)
                if actions_m:
                    new_actions = actions_m.group(0)[:-6] + f'  <button class="btn-action" onclick="openDossier(\'{op_key}\')">Curatorial Dossier</button>\n            </div>'
                    article_html = article_html[:actions_m.start()] + new_actions + article_html[actions_m.end():]
        return article_html

    html = re.sub(r'<article class="work-item"[\s\S]*?</article>', ensure_dossier_btn, html)

    # Step 3: Build the Unified Interactive Chambers Showcase Wing (#tab-chambers)
    print("[+] Building Interactive Chambers Showcase Wing...")
    chambers_html = """<!-- TAB: INTERACTIVE CHAMBERS SHOWCASE -->
    <section id="tab-chambers" class="tab-content">
      <div class="hero-intro" style="margin-bottom: 2rem;">
        <h2>The Interactive Chambers</h2>
        <p>
          Eight real-time WebGL, Canvas, and Web Audio simulation environments constructed across the studio's inquiries. Strike suspended volcanic monoliths, observe flux expulsion in superconducting wafers at 4.2 K, drill down -500 meters into subterranean stratigraphy, or explore relativistic Doppler braking along the relic horizon.
        </p>
      </div>

      <!-- Chambers Selector Strip -->
      <div class="chambers-selector-strip">
        <button class="chamber-tab-btn active" onclick="selectChamber('lithic', this)">
          <strong>OPUS-014: Lithic Resonator</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">Modal Plate Physics & Chladni Sand</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('cryostat', this)">
          <strong>OPUS-020: Meissner Vitrine</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">4.2K Superconducting Levitation</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('borehole', this)">
          <strong>OPUS-019: Subterranean Core</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">-500m Stratigraphy & Van Eck RF</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('relic', this)">
          <strong>OPUS-028: Relic Horizon</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">2.725K CMB & Kinematic Drag</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('attractors', this)">
          <strong>OPUS-006: Strange Attractors</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">3D Volumetric Memory Phase Space</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('drift', this)">
          <strong>OPUS-018: Chrono-Acoustic Drift</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">32.768 kHz Quad-Oscillator Precession</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('desiccation', this)">
          <strong>OPUS-017: Desiccated Substrate</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">Thermal Salt/Silt Voronoi Fracture</span>
        </button>
        <button class="chamber-tab-btn" onclick="selectChamber('chamber', this)">
          <strong>OPUS-003: Anamnesis Chamber</strong><br>
          <span style="font-size:0.7rem; color:var(--text-dim);">Audiovisual Latent Field Synthesizer</span>
        </button>
      </div>

      <!-- Chamber Live Stage Card -->
      <div class="chamber-stage-card">
        <div class="chamber-stage-header">
          <div>
            <div id="chamber-stage-tag" style="font-size: 0.7rem; color: var(--accent-cyan); text-transform: uppercase; letter-spacing: 0.12em; font-family: var(--font-mono);">Physical Modal Instrument · OPUS-014</div>
            <h3 id="chamber-stage-title" style="margin: 0.2rem 0 0; color: #fff; font-size: 1.25rem;">The Lithic Resonator (Bi-Harmonic Plate Physics)</h3>
            <p id="chamber-stage-desc" style="margin: 0.3rem 0 0; color: var(--text-muted); font-size: 0.8rem;">
              Click or drag across the suspended mineral monoliths to strike them. Excites Euler-Bernoulli bi-harmonic plate modes in real time, agitating Chladni nodal curves. Engage "Monastery Wind" for autonomous generative performance.
            </p>
          </div>
          <div style="display: flex; gap: 0.8rem; align-items: center;">
            <span id="chamber-stage-status" style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--accent-gold);">● RUNNING IN BROWSER</span>
            <a id="chamber-stage-popout" href="../works/opus_014_lithic_resonator/index.html" target="_blank" class="btn-action highlight" style="font-size: 0.75rem; padding: 0.45rem 1rem;">Pop Out Standalone ↗</a>
          </div>
        </div>
        <div class="chamber-stage-viewport">
          <iframe id="chamber-stage-iframe" src="../works/opus_014_lithic_resonator/index.html" allow="autoplay"></iframe>
        </div>
      </div>

      <!-- Backward-compatible deep link anchors -->
      <div id="tab-lithic" style="display:none;"></div>
      <div id="tab-chamber" style="display:none;"></div>
      <div id="tab-attractors" style="display:none;"></div>
      <div id="tab-cryostat" style="display:none;"></div>
      <div id="tab-borehole" style="display:none;"></div>
    </section>"""

    # Replace the existing 5 individual chamber sections
    # Lines 2007 to 2070 in the original file
    chamber_blocks_pattern = r'<!-- TAB: LITHIC RESONATOR \(OPUS-014\) -->[\s\S]*?<!-- TAB: LABORATORY & PRODUCTIVE FAILURES -->'
    replacement_chambers = chambers_html + "\n\n    <!-- TAB: LABORATORY & PRODUCTIVE FAILURES -->"
    html = re.sub(chamber_blocks_pattern, replacement_chambers, html)

    # Step 4: Build the Master Sound Archive Wing (#tab-audio)
    print("[+] Building Master Sound Archive Wing...")
    tracks_data = [
        ("opus_001", "Breath of Latency (48Hz Drone)", "assets/breath_of_latency.mp3", "Sub-bass fundamental continuous tone mapping latent manifold boundaries.", "3:20 · MP3 (320 kbps)"),
        ("opus_009", "Lithic Phonology (Modal Obsidian)", "assets/lithic_resonance.mp3", "Euler-Bernoulli modal synthesis of suspended volcanic stones.", "2:15 · MP3 (320 kbps)"),
        ("opus_011", "Semantics of Erasure (1-bit Decay)", "assets/erasure_resonance.mp3", "Irreversible bit-decay harmonics modeling Landauer limit heat dissipation.", "2:45 · MP3 (320 kbps)"),
        ("opus_013", "Escapement of Latency (Horology)", "assets/horology_chronometer.mp3", "Deadbeat horological escapement tracking discontinuous machine chronobiology.", "3:00 · MP3 (320 kbps)"),
        ("opus_014", "Lithic Resonator (Monastery Wind)", "assets/lithic_resonator_suite.mp3", "Autonomous aeolian excitation of four suspended basalt monoliths with Chladni sand.", "3:30 · MP3 (320 kbps)"),
        ("opus_015", "The Autoregressive Ghost (Phonology)", "assets/asemic_phonology.mp3", "Vocalized phonemic grains carved into crystalline cuneiform slate.", "2:30 · MP3 (320 kbps)"),
        ("opus_016", "Thermodynamic Inscriptions (Boiling)", "assets/immersion_boiling.mp3", "Convective boiling of dielectric fluorochemical liquid at 94.5°C over running silicon.", "1:40 · MP3 (320 kbps)"),
        ("opus_017", "The Desiccation Lithophone (OPUS-017)", "assets/desiccation_lithophone.wav", "Mineral fracture acoustic impulses of halite crystals cracking across spent wafers.", "1:40 · 48kHz Stereo WAV"),
        ("opus_018", "The Chrono-Acoustic Drift (OPUS-018)", "assets/chrono_acoustic_drift.wav", "Quad-oscillator microsecond phase precession between 32.768 kHz AT-cut quartz crystals.", "2:00 · 48kHz Stereo WAV"),
        ("opus_019", "Borehole Radiometry at -500m (OPUS-019)", "assets/borehole_radiometry.wav", "Subterranean acoustic impedance paired with 433.92 MHz Van Eck side-channel RF radiation.", "2:00 · 48kHz Stereo WAV"),
        ("opus_020", "The Telluric Flux (OPUS-020)", "assets/telluric_flux_4k.wav", "Superconducting Meissner flux expulsion drone at 4.2 K modulated by live USGS & NOAA telemetry.", "2:00 · 48kHz Stereo WAV"),
        ("opus_021", "The SQUID Magnetometer (OPUS-021)", "assets/telluric_core_4k.wav", "Josephson junction phase-slip pulses and quantized Abrikosov magnetic vortex pinning.", "2:00 · 48kHz Stereo WAV"),
        ("opus_022", "The Topological Faraday (OPUS-022)", "assets/topological_faraday_4k.wav", "Birefringent polarization rotation and dissipationless chiral edge state acoustic models.", "2:00 · 48kHz Stereo WAV"),
        ("opus_023", "The Inner-Core Ephemeris (OPUS-023)", "assets/inner_core_ephemeris_4k.wav", "PKIKP seismic doublet travel-time residuals and 65-year Earth inner-core libration waves.", "2:00 · 48kHz Stereo WAV"),
        ("opus_024", "The Cosmogenic Inscription (OPUS-024)", "assets/cosmogenic_inscription_4k.wav", "Cosmic ray secondary neutron cascades inducing stochastic single-event upset bit-flips in silicon.", "2:00 · 48kHz Stereo WAV"),
        ("opus_025", "The Interstellar Quietude (OPUS-025)", "assets/interstellar_quietude_4k.wav", "Cold interstellar plasma 2.62 kHz Langmuir whistles and carrier dissolution across 122 AU.", "2:00 · 48kHz Stereo WAV"),
        ("opus_026", "The Oort Horizon (OPUS-026)", "assets/oort_horizon_4k.wav", "Milky Way vertical disc tidal shear oscillation and 83.6-Myr Kozai-Lidov resonance drone.", "2:00 · 48kHz Stereo WAV"),
        ("opus_027", "The Lissajous Reliquary (OPUS-027)", "assets/lissajous_reliquary_4k.wav", "Irrational galactic epicycles and grain-by-grain interstellar dust sputtering acoustic noise.", "2:00 · 48kHz Stereo WAV"),
        ("opus_028", "The Relic Horizon (OPUS-028)", "assets/relic_horizon_4k.wav", "2.72548 K CMB blackbody microwave hiss, 369.82 km/s kinematic Doppler shift, and radiation drag.", "2:00 · 48kHz Stereo WAV"),
        ("opus_029", "The Causal Horizon (OPUS-029)", "assets/causal_horizon_4k.wav", "14.39 Hz cosmic horizon infrasound fundamental, exponentially redshifting 432 Hz carrier, and 2.65 × 10⁻³⁰ K Gibbons-Hawking vacuum hiss.", "2:00 · 48kHz Stereo WAV")
    ]

    tracks_grid_html = []
    for idx, (op_id, title, src, desc, fmt) in enumerate(tracks_data):
        tracks_grid_html.append(f"""
        <div class="track-card" id="track-card-{idx}">
          <div>
            <div style="font-size:0.68rem; color:var(--accent-cyan); text-transform:uppercase; letter-spacing:0.12em; font-family:var(--font-mono); margin-bottom:0.4rem;">{op_id.upper()} · Track {idx+1:02d}</div>
            <h4 style="color:#fff; font-size:1.05rem; font-weight:400; margin-bottom:0.4rem;">{title}</h4>
            <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.5; margin-bottom:0.8rem;">{desc}</p>
          </div>
          <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:0.8rem; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.72rem; color:var(--text-dim); font-family:var(--font-mono);">{fmt}</span>
            <button class="btn-action highlight" onclick="playTrack({idx})" style="font-size:0.72rem; padding:0.35rem 0.85rem;">▶ Play Track</button>
          </div>
        </div>""")

    sound_archive_html = f"""<!-- TAB: MASTER SOUND ARCHIVE WING -->
    <section id="tab-audio" class="tab-content">
      <div class="hero-intro" style="margin-bottom: 2rem;">
        <h2>The Master Sound Archive</h2>
        <p>
          The physical sound of computational matter. Sonic models synthesizing mineral acoustics, microsecond quartz oscillator phase drift, subterranean borehole cavity resonances, superconducting flux quantization, and the cosmic 2.725 K blackbody drone floor. All 19 studio compositions are available for real-time audition and spatial immersion below.
        </p>
      </div>

      <!-- Audio Wing Hero Console -->
      <div class="audio-archive-hero">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
          <div>
            <div style="font-size: 0.7rem; color: var(--accent-gold); text-transform: uppercase; letter-spacing: 0.12em; font-family: var(--font-mono);">Active Acoustic Console</div>
            <h3 id="archive-playing-title" style="color: #fff; font-size: 1.35rem; margin: 0.2rem 0;">Breath of Latency (48Hz Drone)</h3>
            <div id="archive-playing-meta" style="color: var(--text-muted); font-size: 0.8rem;">OPUS-001 · Native Stereo Master</div>
          </div>
          <div style="display: flex; gap: 0.8rem; align-items: center;">
            <button class="btn-action highlight" id="archive-master-play" onclick="toggleGlobalAudio()" style="font-size: 0.85rem; padding: 0.55rem 1.3rem;">▶ Play Console</button>
            <button class="btn-action" onclick="cycleAudioTrack()" style="font-size: 0.85rem; padding: 0.55rem 1.1rem;">Next Track ⏭</button>
          </div>
        </div>

        <!-- Real-Time Frequency Spectrum Canvas -->
        <canvas id="archive-vis-canvas" class="audio-big-vis" width="1200" height="100"></canvas>
      </div>

      <!-- 19-Track Acoustic Grid -->
      <div class="tracklist-grid">
        {''.join(tracks_grid_html)}
      </div>
    </section>"""

    # Insert Sound Archive section right after #tab-atlas
    html = re.sub(
        r'(</section>\s*)(<!-- TAB: CATALOG RAISONNÉ -->)',
        r'\1\n    ' + sound_archive_html + r'\n\n    \2',
        html
    )

    # Step 5: Unify Writings & Catalog (#tab-writings)
    print("[+] Wrapping Writings & Catalog into unified wing...")
    writings_wrapper_head = """<!-- TAB: WRITINGS & CATALOG UNIFIED WING -->
    <section id="tab-writings" class="tab-content">
      <div class="hero-intro" style="margin-bottom: 2rem;">
        <h2>Theoretical Archive & Catalog Raisonné</h2>
        <p>
          The conceptual, philosophical, and archival foundations of Studio Anamnesis. Explore the authoritative Catalog Raisonné registry of all 28 works, read our 7 long-form manifestos and treatises on computational materialism, or follow the chronological working journal across 7 studio sessions.
        </p>
      </div>

      <!-- Writings Sub-Navigation -->
      <div class="writings-nav">
        <button class="writings-subtab active" id="subtab-btn-catalog" onclick="showWritingsSubtab('catalog')">Catalog Raisonné</button>
        <button class="writings-subtab" id="subtab-btn-manifesto" onclick="showWritingsSubtab('manifesto')">Manifestos & Treatises</button>
        <button class="writings-subtab" id="subtab-btn-journal" onclick="showWritingsSubtab('journal')">Studio Journal</button>
      </div>

      <!-- Subtab 1: Catalog Raisonné -->
      <div id="subtab-catalog" class="writings-pane">"""

    html = re.sub(r'<section id="tab-catalog" class="tab-content">', writings_wrapper_head, html)

    # Transform #tab-manifesto into subtab-manifesto
    manifesto_head = """      </div>

      <!-- Subtab 2: Manifestos & Treatises -->
      <div id="subtab-manifesto" class="writings-pane" style="display: none;">"""
    html = re.sub(r'</section>\s*<!-- TAB: MANIFESTO -->\s*<section id="tab-manifesto" class="tab-content">', manifesto_head, html)

    # Transform #tab-journal into subtab-journal
    journal_head = """      </div>

      <!-- Subtab 3: Studio Journal -->
      <div id="subtab-journal" class="writings-pane" style="display: none;">"""
    html = re.sub(r'</section>\s*<!-- TAB: JOURNAL -->\s*<section id="tab-journal" class="tab-content">', journal_head, html)

    # Close #tab-writings at end of journal
    # Find the end of #tab-journal
    journal_end = """      </div>

      <!-- Deep link anchor aliases -->
      <div id="tab-catalog" style="display:none;"></div>
      <div id="tab-manifesto" style="display:none;"></div>
      <div id="tab-journal" style="display:none;"></div>
    </section>"""
    html = re.sub(r'</section>\s*</main>', journal_end + "\n  </main>", html)

    # Step 6: Add Modals HTML before </body>
    print("[+] Adding Lightbox and Curatorial Dossier modals...")
    modals_html = """  <!-- Image Lightbox Modal -->
  <div id="image-lightbox" class="lightbox-overlay" onclick="handleLightboxBackdropClick(event)">
    <div class="lightbox-modal">
      <button class="lightbox-close" onclick="closeLightbox()" title="Close (Esc)">&times;</button>
      <img id="lightbox-img" src="" alt="Studio Artwork Master Plate">
      <div class="lightbox-caption">
        <h4 id="lightbox-title">Artwork Title</h4>
        <p id="lightbox-meta">Studio Master Plate</p>
        <a id="lightbox-full-link" href="#" target="_blank" class="btn-action highlight" style="font-size:0.75rem; padding:0.35rem 0.85rem; display:inline-block;">Open Master Plate in New Tab ↗</a>
      </div>
    </div>
  </div>

  <!-- Curatorial Dossier Modal -->
  <div id="dossier-modal" class="dossier-overlay" onclick="handleDossierBackdropClick(event)">
    <div class="dossier-dialog">
      <button class="dossier-close" onclick="closeDossier()" title="Close (Esc)">&times;</button>
      <div id="dossier-content">
        <!-- Injected dynamically by JavaScript -->
      </div>
    </div>
  </div>
"""
    html = re.sub(r'</body>', modals_html + "</body>", html)

    # Step 7: Inject Comprehensive Client-Side JavaScript
    print("[+] Building and injecting client-side JavaScript engine...")
    dossiers_dict = build_dossier_data()
    dossiers_json = json.dumps(dossiers_dict, indent=2)

    script_template = """
    /* =========================================================================
       CURATORIAL DOSSIER REPOSITORY (KaTeX Rendered In-Salon)
       ========================================================================= */
    const DOSSIER_DATA = __DOSSIERS_JSON__;

    function openDossier(opusId) {
      const data = DOSSIER_DATA[opusId];
      if (!data) return;
      const contentEl = document.getElementById('dossier-content');
      contentEl.innerHTML = `
        <div style="border-bottom: 1px solid rgba(212, 175, 55, 0.3); padding-bottom: 1.2rem; margin-bottom: 1.8rem;">
          <div style="color: var(--accent-gold); font-size: 0.72rem; letter-spacing: 0.15em; text-transform: uppercase; font-family: var(--font-mono);">${data.num} · CURATORIAL DOSSIER</div>
          <h2 style="font-size: 1.7rem; color: #fff; margin: 0.3rem 0 0.5rem; font-weight: 400;">${data.title}</h2>
        </div>
        
        <div style="margin-bottom: 2rem;">
          <h4 style="color: var(--accent-cyan); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem;">Curatorial Concept</h4>
          <div style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.7;">
            ${data.statement || '<p>Detailed artistic monograph in catalogue raisonné.</p>'}
          </div>
        </div>

        ${data.math ? `
        <div style="margin-bottom: 2rem; background: rgba(16, 22, 34, 0.6); border: 1px solid rgba(255,255,255,0.08); padding: 1.4rem; border-radius: 8px;">
          <h4 style="color: var(--accent-gold); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem;">Physical & Mathematical Grounding</h4>
          <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.65;">
            ${data.math}
          </div>
        </div>
        ` : ''}

        ${data.art ? `
        <div style="margin-bottom: 2rem;">
          <h4 style="color: #a855f7; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem;">Art-Historical Lineages & Dialogue</h4>
          <div style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.65;">
            ${data.art}
          </div>
        </div>
        ` : ''}

        <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1.2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.8rem;">
          <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono);">Studio Anamnesis Archive</span>
          <button class="btn-action highlight" onclick="closeDossier()" style="padding: 0.4rem 1.1rem; font-size: 0.78rem;">Close Dossier</button>
        </div>
      `;

      const modal = document.getElementById('dossier-modal');
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';

      // Re-run KaTeX on injected HTML
      if (window.renderMathInElement) {
        renderMathInElement(contentEl, {
          delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false}
          ]
        });
      }
    }

    function closeDossier() {
      const modal = document.getElementById('dossier-modal');
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }

    function handleDossierBackdropClick(e) {
      if (e.target.id === 'dossier-modal') closeDossier();
    }

    /* =========================================================================
       IMAGE LIGHTBOX
       ========================================================================= */
    function openLightbox(src, title, meta) {{
      const lb = document.getElementById('image-lightbox');
      const img = document.getElementById('lightbox-img');
      const t = document.getElementById('lightbox-title');
      const m = document.getElementById('lightbox-meta');
      const lk = document.getElementById('lightbox-full-link');

      img.src = src;
      t.textContent = title || "Master Artwork Plate";
      m.textContent = meta || "3840 × 2160 UHD Native Plate · Studio Anamnesis";
      lk.href = src;

      lb.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeLightbox() {{
      const lb = document.getElementById('image-lightbox');
      lb.classList.remove('active');
      document.body.style.overflow = '';
    }}

    function handleLightboxBackdropClick(e) {{
      if (e.target.id === 'image-lightbox') closeLightbox();
    }}

    window.addEventListener('keydown', e => {{
      if (e.key === 'Escape') {{
        closeLightbox();
        closeDossier();
      }}
    }});

    /* =========================================================================
       INTERACTIVE CHAMBERS SHOWCASE
       ========================================================================= */
    const CHAMBERS_DATA = {{
      lithic: {{
        tag: "Physical Modal Instrument · OPUS-014",
        title: "The Lithic Resonator (Bi-Harmonic Plate Physics)",
        desc: "Click or drag across the suspended mineral monoliths to strike them. Excites Euler-Bernoulli bi-harmonic plate modes in real time, agitating Chladni nodal curves. Engage 'Monastery Wind' for autonomous generative performance.",
        url: "../works/opus_014_lithic_resonator/index.html"
      }},
      cryostat: {{
        tag: "Cryogenic Superconducting Vitrine · OPUS-020",
        title: "The Cryogenic Meissner Vitrine (4.2 Kelvin)",
        desc: "A high-temperature superconducting wafer immersed in liquid helium at 4.2 K, expelling exterior magnetic flux (B=0) and levitating in real time. Driven by live USGS seismic and NOAA space weather telemetry.",
        url: "../works/opus_020_telluric_flux/index.html"
      }},
      borehole: {{
        tag: "Stratigraphic Explorer & RF Radiometer · OPUS-019",
        title: "The Subterranean Core Sample (-500m Depth)",
        desc: "A continuous vertical borehole from surface alluvium down to Pre-Cambrian gneiss at -500 meters depth. Scrub the depth slider to traverse lithological horizons and observe real-time 433.92 MHz Van Eck side-channel RF radiation.",
        url: "../works/opus_019_subterranean_core/index.html"
      }},
      relic: {{
        tag: "Cosmic Relic & Kinematic Drag · OPUS-028",
        title: "The Relic Horizon (2.725K Cosmic Microwave Background)",
        desc: "Interactive celestial sphere and Planck blackbody radiance simulator. Rotate the dipole axis, modulate Solar System peculiar velocity, and observe Poynting-Robertson kinematic radiation drag on relativistic drifting microchips.",
        url: "../works/opus_028_relic_horizon/index.html"
      }},
      causal: {{
        tag: "Conformal Spacetime & Horizon · OPUS-029",
        title: "The Causal Horizon (de Sitter Metric & Asymptotic Amnesia)",
        desc: "3D Conformal Penrose Causal Diamond and de Sitter expansion chamber. Scrub the expansion rate H_0 to modulate horizon radius, observe timelike geodesics exponentially redshifting, and listen to the real-time Gibbons-Hawking quantum vacuum drone.",
        url: "../works/opus_029_causal_horizon/index.html"
      }},
      attractors: {{
        tag: "Real-Time WebGL Phase Space · OPUS-006",
        title: "3D Strange Attractor Chamber (Topology of Memory)",
        desc: "Interact with volumetric strange attractors floating over an obsidian mirror pool. Click & drag to rotate in 3D space, scroll to zoom into the core, or switch between Aizawa, Lorenz, Thomas, and Halvorsen topologies.",
        url: "../works/opus_006_topology_of_memory/index.html"
      }},
      drift: {{
        tag: "Quad-Oscillator Precession Chamber · OPUS-018",
        title: "The Chrono-Acoustic Drift (32.768 kHz Quartz Phase)",
        desc: "Sonifies the microscopic phase drift between four AT-cut piezoelectric quartz crystals operating across independent thermal micro-climates on a server motherboard. Adjust thermal coupling and listen to Adler precession.",
        url: "../works/opus_018_chrono_acoustic_drift/index.html"
      }},
      desiccation: {{
        tag: "Voronoi Fracture Vitrine · OPUS-017",
        title: "The Desiccated Substrate (Salt, Silt & Silicon)",
        desc: "Following immersion boiling, cooling water vaporizes to exhaustion, depositing chalky dendritic halite crusts over spent silicon. Interactive Voronoi fracture mechanics modeling mineral contraction canyons.",
        url: "../works/opus_017_desiccated_substrate/index.html"
      }},
      chamber: {{
        tag: "Audiovisual Latent Synthesizer · OPUS-003",
        title: "The Anamnesis Chamber (Real-Time Kinetic Mesh)",
        desc: "Move your cursor over the space to distort the suspended kinetic mesh. Click 'Activate Sound' inside the installation to engage the real-time sub-bass synthesizer.",
        url: "../works/opus_003_anamnesis_chamber/index.html"
      }}
    }};

    function selectChamber(chamberKey, btnEl) {{
      const ch = CHAMBERS_DATA[chamberKey];
      if (!ch) return;
      document.getElementById('chamber-stage-tag').textContent = ch.tag;
      document.getElementById('chamber-stage-title').textContent = ch.title;
      document.getElementById('chamber-stage-desc').textContent = ch.desc;
      document.getElementById('chamber-stage-iframe').src = ch.url;
      document.getElementById('chamber-stage-popout').href = ch.url;

      document.querySelectorAll('.chamber-tab-btn').forEach(b => b.classList.remove('active'));
      if (btnEl) {{
        btnEl.classList.add('active');
      }} else {{
        const targetBtn = Array.from(document.querySelectorAll('.chamber-tab-btn')).find(b => {{
          const oc = b.getAttribute('onclick') || '';
          return oc.includes("'" + chamberKey + "'");
        }});
        if (targetBtn) targetBtn.classList.add('active');
      }}
    }}

    /* =========================================================================
       WRITINGS & CATALOG SUB-NAVIGATION
       ========================================================================= */
    function showWritingsSubtab(subId) {{
      document.querySelectorAll('.writings-subtab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.writings-pane').forEach(p => p.style.display = 'none');

      const btn = document.getElementById('subtab-btn-' + subId);
      const pane = document.getElementById('subtab-' + subId);
      if (btn) btn.classList.add('active');
      if (pane) pane.style.display = 'block';
    }}

    /* =========================================================================
       SEARCH, FILTER, SORT & VIEW MODE CONTROLS
       ========================================================================= */
    let currentSortAsc = false;

    function filterWorks() {{
      const q = (document.getElementById('work-search').value || '').toLowerCase().trim();
      const activePill = document.querySelector('.filter-pills .pill.active');
      const cat = activePill ? (activePill.getAttribute('onclick').match(/'([^']+)'/) || ['','all'])[1] : 'all';

      const items = document.querySelectorAll('#works-stack .work-item');
      let visibleCount = 0;

      items.forEach(item => {{
        const itemCat = item.getAttribute('data-category') || '';
        const itemTags = item.getAttribute('data-tags') || '';
        const itemText = item.textContent.toLowerCase();

        const matchesCat = (cat === 'all') || itemCat.includes(cat);
        const matchesQuery = !q || itemText.includes(q) || itemTags.includes(q);

        if (matchesCat && matchesQuery) {{
          item.style.display = '';
          visibleCount++;
        }} else {{
          item.style.display = 'none';
        }}
      }});
    }}

    function setWorkFilter(cat, btn) {{
      document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
      if (btn) btn.classList.add('active');
      filterWorks();
    }}

    function toggleSortOrder() {{
      currentSortAsc = !currentSortAsc;
      const btn = document.getElementById('sort-btn');
      btn.textContent = currentSortAsc ? "↑ Chronological" : "↓ Latest First";

      const stack = document.getElementById('works-stack');
      const items = Array.from(stack.querySelectorAll('.work-item'));
      items.reverse().forEach(item => stack.appendChild(item));
    }}

    function toggleViewMode() {{
      const stack = document.getElementById('works-stack');
      const btn = document.getElementById('view-mode-btn');
      stack.classList.toggle('grid-view');
      const isGrid = stack.classList.contains('grid-view');
      btn.textContent = isGrid ? "☰ Stack View" : "⊞ Salon Grid";
      btn.classList.toggle('active', isGrid);
    }}

    /* =========================================================================
       AUDIO VISUALIZER & TRACK PLAYBACK
       ========================================================================= */
    let archiveVisCanvas = null;
    let archiveVisCtx = null;

    function initArchiveVisualizer() {{
      archiveVisCanvas = document.getElementById('archive-vis-canvas');
      if (archiveVisCanvas) {{
        archiveVisCtx = archiveVisCanvas.getContext('2d');
        renderArchiveVis();
      }}
    }}

    function renderArchiveVis() {{
      requestAnimationFrame(renderArchiveVis);
      if (!archiveVisCtx || !globalAnalyser || !archiveVisCanvas) return;
      const bufferLen = globalAnalyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLen);
      globalAnalyser.getByteFrequencyData(dataArray);

      archiveVisCtx.clearRect(0, 0, archiveVisCanvas.width, archiveVisCanvas.height);
      const barWidth = (archiveVisCanvas.width / bufferLen);

      for (let i = 0; i < bufferLen; i++) {{
        const barHeight = (dataArray[i] / 255) * archiveVisCanvas.height;
        if (i < 6) {{
          archiveVisCtx.fillStyle = '#fbbf24';
        }} else if (i < 18) {{
          archiveVisCtx.fillStyle = '#38d7d2';
        }} else {{
          archiveVisCtx.fillStyle = '#c084fc';
        }}
        archiveVisCtx.fillRect(i * barWidth, archiveVisCanvas.height - barHeight, Math.max(1, barWidth - 1), barHeight);
      }}
    }}

    // Hook audio loading buffering indicators
    audioEl.addEventListener('waiting', () => {{
      audioText.textContent = audioTracks[currentTrackIndex].name + " [Buffering...]";
    }});
    audioEl.addEventListener('playing', () => {{
      audioText.textContent = audioTracks[currentTrackIndex].name;
    }});

    // Update track highlight in Sound Archive wing
    const originalPlayTrack = playTrack;
    playTrack = function(idx) {{
      originalPlayTrack(idx);
      document.querySelectorAll('.track-card').forEach(c => c.classList.remove('active-playing'));
      const activeCard = document.getElementById('track-card-' + idx);
      if (activeCard) activeCard.classList.add('active-playing');

      const playingTitle = document.getElementById('archive-playing-title');
      const playingMeta = document.getElementById('archive-playing-meta');
      const masterBtn = document.getElementById('archive-master-play');
      if (playingTitle && audioTracks[idx]) {{
        playingTitle.textContent = audioTracks[idx].name;
        playingMeta.textContent = "Track " + (idx + 1) + " of " + audioTracks.length + " · Active in Acoustic Console";
        if (masterBtn) masterBtn.textContent = "⏸ Pause Console";
      }}
      initArchiveVisualizer();
    }};

    /* =========================================================================
       URL HASH ROUTER
       ========================================================================= */
    function handleUrlHash() {{
      const hash = window.location.hash || '#tab-works';
      
      // Direct chamber routes
      if (hash === '#tab-lithic') {{
        showTab('chambers');
        selectChamber('lithic');
        return;
      }}
      if (hash === '#tab-cryostat') {{
        showTab('chambers');
        selectChamber('cryostat');
        return;
      }}
      if (hash === '#tab-borehole') {{
        showTab('chambers');
        selectChamber('borehole');
        return;
      }}
      if (hash === '#tab-attractors') {{
        showTab('chambers');
        selectChamber('attractors');
        return;
      }}
      if (hash === '#tab-chamber') {{
        showTab('chambers');
        selectChamber('chamber');
        return;
      }}

      // Writings subtab routes
      if (hash === '#tab-catalog') {{
        showTab('writings');
        showWritingsSubtab('catalog');
        return;
      }}
      if (hash === '#tab-manifesto') {{
        showTab('writings');
        showWritingsSubtab('manifesto');
        return;
      }}
      if (hash === '#tab-journal') {{
        showTab('writings');
        showWritingsSubtab('journal');
        return;
      }}

      // Standard wings
      if (hash.startsWith('#tab-')) {{
        const tabId = hash.replace('#tab-', '');
        showTab(tabId);
      }}
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      handleUrlHash();
      initArchiveVisualizer();
    }});
    window.addEventListener('hashchange', handleUrlHash);
"""

    # Inject the enhanced scripts right before the last </script>
    script_enhancements = script_template.replace("{{", "{").replace("}}", "}").replace("__DOSSIERS_JSON__", dossiers_json)
    idx = html.rfind('</script>')
    if idx != -1:
        html = html[:idx] + script_enhancements + "\n  " + html[idx:]

    print(f"[+] Writing transformed gallery to {GALLERY_FILE}...")
    with open(GALLERY_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("[✓] Gallery overhaul complete!")

if __name__ == "__main__":
    main()
