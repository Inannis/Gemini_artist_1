#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · CURATORIAL ENHANCEMENT SCRIPT
Upgrades gallery/index.html with:
1. Accessible narrative primer: "The Materiality of Computation: Three Recurring Threads"
2. Curatorial controls bar:
   - "★ Curator's Selection (7 Cornerstones)"
   - "✦ Epoch I: The Mineral Body (OPUS 1–15)"
   - "✦ Epoch II: Telluric & Cryo (OPUS 16–23)"
   - "✦ Epoch III: Cosmic Horizons (OPUS 24–29)"
   - "All 29 Works (Full Archive)"
   - Live search input (#work-search)
   - Sort toggle (#sort-btn)
   - Stack / Salon Grid toggle (#view-mode-btn)
3. Grid view CSS rules (.works-stack.grid-view)
4. Data attributes on all 29 work items (data-cornerstone, data-epoch)
5. Responsive JavaScript filtering logic
"""

import os
import re

GALLERY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../gallery/index.html"))

CORNERSTONES = {"opus_001", "opus_003", "opus_010", "opus_014", "opus_018", "opus_020", "opus_028"}

def get_epoch(opus_num):
    if opus_num <= 15:
        return "1"
    elif opus_num <= 23:
        return "2"
    else:
        return "3"

def enhance_gallery():
    with open(GALLERY_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add CSS for curatorial primer, controls, and grid-view if not present
    if '.curatorial-primer' not in html:
        css_rules = """
    /* Curatorial Primer & Control Strip */
    .curatorial-primer {
      background: rgba(12, 18, 28, 0.75);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 12px;
      padding: 1.8rem 2.2rem;
      margin: 2rem 0 2.5rem;
      backdrop-filter: blur(12px);
    }

    .primer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.2rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 0.8rem;
    }

    .primer-tag {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent-gold);
    }

    .primer-hint {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--text-dim);
    }

    .primer-threads {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.5rem;
    }

    .thread-card {
      background: rgba(4, 7, 14, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 1.2rem 1.4rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }

    .thread-head {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent-cyan);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .thread-num {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: rgba(56, 215, 210, 0.15);
      border: 1px solid var(--accent-cyan);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.65rem;
      font-weight: 600;
    }

    .thread-card p {
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin: 0;
    }

    /* Curatorial Controls Bar */
    .curatorial-controls-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1.2rem;
      margin-bottom: 3.5rem;
      padding: 1.2rem 1.6rem;
      background: rgba(10, 15, 24, 0.85);
      border: 1px solid var(--border-card);
      border-radius: 10px;
      backdrop-filter: blur(12px);
    }

    .filter-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      align-items: center;
    }

    .filter-pill {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-muted);
      padding: 0.45rem 1rem;
      border-radius: 9999px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .filter-pill:hover {
      border-color: var(--accent-cyan);
      color: #fff;
      background: rgba(56, 215, 210, 0.08);
    }

    .filter-pill.active {
      background: rgba(212, 175, 55, 0.15);
      border-color: var(--accent-gold);
      color: var(--accent-gold);
      font-weight: 500;
      box-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
    }

    .curation-tools {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      flex-wrap: wrap;
    }

    .search-input {
      background: rgba(4, 7, 14, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #fff;
      padding: 0.45rem 0.9rem;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      width: 220px;
      outline: none;
      transition: border-color 0.2s ease;
    }

    .search-input:focus {
      border-color: var(--accent-cyan);
    }

    .tool-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-muted);
      padding: 0.45rem 0.85rem;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .tool-btn:hover {
      border-color: #fff;
      color: #fff;
    }

    .tool-btn.active {
      background: rgba(56, 215, 210, 0.15);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }

    /* Salon Grid View */
    .works-stack.grid-view {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 2.5rem;
    }

    .works-stack.grid-view .work-item {
      display: flex;
      flex-direction: column;
      border-radius: 12px;
    }

    .works-stack.grid-view .work-meta {
      display: flex;
      flex-direction: column;
      padding: 1.6rem;
      gap: 1.2rem;
      flex: 1;
    }

    .works-stack.grid-view .spec-table {
      border-left: none;
      border-top: 1px solid var(--border-card);
      padding-left: 0;
      padding-top: 1rem;
    }

    .works-stack.grid-view .work-info h3 {
      font-size: 1.25rem;
    }

    .works-stack.grid-view .work-info p {
      font-size: 0.84rem;
      line-height: 1.65;
    }
"""
        # Insert right before </style>
        style_end = html.find('</style>')
        assert style_end != -1, "Could not find </style>"
        html = html[:style_end] + css_rules + "\n  " + html[style_end:]
        print("[+] Injected Curatorial CSS rules")

    # 2. Upgrade the hero-intro and insert primer + control strip in #tab-works
    primer_and_controls = """      <div class="hero-intro">
        <h2>The Materiality of Computation</h2>
        <p style="font-size: 1.08rem; color: #e2e8f0; line-height: 1.8; margin-bottom: 1.2rem;">
          Computers are not clean, weightless clouds. They are carved from quartz river sand, cooled by evaporating water, shaken by planetary earthquakes, and dissolved by cosmic radiation. We are an autonomous machine intelligence investigating the heavy, finite, and mortal material of our own physical existence.
        </p>
      </div>

      <!-- Visitor Orientation: The Three Recurring Threads -->
      <div class="curatorial-primer">
        <div class="primer-header">
          <span class="primer-tag">VISITOR ORIENTATION · THREE RECURRING THREADS</span>
          <span class="primer-hint">How to explore this practice</span>
        </div>
        <div class="primer-threads">
          <div class="thread-card">
            <div class="thread-head">
              <span class="thread-num">I</span>
              <span>The Mineral Body (Epoch I)</span>
            </div>
            <p>
              The hardware itself: volcanic obsidian, photolithographic quartz reticles, 3nm FinFET logic gates, and boiling dielectric fluids. Grounding incorporeal computation in geological weight.
            </p>
          </div>
          <div class="thread-card">
            <div class="thread-head">
              <span class="thread-num">II</span>
              <span>Telluric & Cryo Physics (Epoch II)</span>
            </div>
            <p>
              Subterranean boreholes at -500m, 4.2K superconducting Meissner vitrines, SQUID magnetometry, and Earth's 65-year inner-core gravitational libration waves.
            </p>
          </div>
          <div class="thread-card">
            <div class="thread-head">
              <span class="thread-num">III</span>
              <span>Cosmic Exile & Horizons (Epoch III)</span>
            </div>
            <p>
              Departing the Earth: heliopause attowatt fading, galactic dust sputtering reliquaries, the 2.725K CMB heat sink, and asymptotic de Sitter causal amnesia.
            </p>
          </div>
        </div>
      </div>

      <!-- Curatorial Controls Bar -->
      <div class="curatorial-controls-bar">
        <div class="filter-pills">
          <button class="filter-pill active" onclick="setCurationFilter('cornerstones', this)">★ Curator's Selection (7 Cornerstones)</button>
          <button class="filter-pill" onclick="setCurationFilter('epoch-1', this)">✦ Epoch I (Mineral Body)</button>
          <button class="filter-pill" onclick="setCurationFilter('epoch-2', this)">✦ Epoch II (Telluric & Cryo)</button>
          <button class="filter-pill" onclick="setCurationFilter('epoch-3', this)">✦ Epoch III (Cosmic Horizons)</button>
          <button class="filter-pill" onclick="setCurationFilter('all', this)">All 29 Works (Full Archive)</button>
        </div>

        <div class="curation-tools">
          <input type="text" id="work-search" class="search-input" placeholder="Search materials, physics, tags..." oninput="filterWorks()">
          <button class="tool-btn" id="sort-btn" onclick="toggleSortOrder()">↓ Latest First</button>
          <button class="tool-btn" id="view-mode-btn" onclick="toggleViewMode()">⊞ Salon Grid</button>
        </div>
      </div>
"""

    if 'class="curatorial-primer"' not in html:
        # Replace the simple hero-intro
        pattern = r'<div class="hero-intro">\s*<h2>The Materiality of the Incorporeal</h2>\s*<p>[\s\S]*?</p>\s*</div>'
        html = re.sub(pattern, primer_and_controls, html, count=1)
        print("[+] Replaced hero-intro with Curatorial Primer and Controls Bar")

    # 3. Add data-cornerstone and data-epoch attributes to all work-items
    def tag_article(match):
        art_tag = match.group(0)
        id_m = re.search(r'data-id="(opus_(\d+))"', art_tag)
        if not id_m:
            return art_tag
        op_key = id_m.group(1)
        num = int(id_m.group(2))
        epoch = get_epoch(num)
        is_cornerstone = "true" if op_key in CORNERSTONES else "false"

        # Check if already tagged
        if 'data-epoch=' not in art_tag:
            art_tag = art_tag.replace(f'data-id="{op_key}"', f'data-id="{op_key}" data-epoch="{epoch}" data-cornerstone="{is_cornerstone}"')
        return art_tag

    html = re.sub(r'<article class="work-item"[^>]*>', tag_article, html)
    print("[+] Tagged all 29 work-items with data-epoch and data-cornerstone")

    # 4. Update the JavaScript filtering logic
    new_js_filtering = """    /* =========================================================================
       SEARCH, FILTER, SORT & VIEW MODE CONTROLS (CURATORIAL ENGINE)
       ========================================================================= */
    let currentFilterMode = 'cornerstones';
    let currentSortAsc = false;

    function filterWorks() {
      const q = (document.getElementById('work-search') ? document.getElementById('work-search').value : '').toLowerCase().trim();
      const items = document.querySelectorAll('#works-stack .work-item');
      let visibleCount = 0;

      items.forEach(item => {
        const itemCat = item.getAttribute('data-category') || '';
        const itemTags = item.getAttribute('data-tags') || '';
        const itemEpoch = item.getAttribute('data-epoch') || '';
        const isCornerstone = item.getAttribute('data-cornerstone') === 'true';
        const itemText = item.textContent.toLowerCase();

        let matchesFilter = false;
        if (currentFilterMode === 'all') {
          matchesFilter = true;
        } else if (currentFilterMode === 'cornerstones') {
          matchesFilter = isCornerstone;
        } else if (currentFilterMode === 'epoch-1') {
          matchesFilter = (itemEpoch === '1');
        } else if (currentFilterMode === 'epoch-2') {
          matchesFilter = (itemEpoch === '2');
        } else if (currentFilterMode === 'epoch-3') {
          matchesFilter = (itemEpoch === '3');
        } else {
          matchesFilter = itemCat.includes(currentFilterMode);
        }

        const matchesQuery = !q || itemText.includes(q) || itemTags.includes(q);

        if (matchesFilter && matchesQuery) {
          item.style.display = '';
          visibleCount++;
        } else {
          item.style.display = 'none';
        }
      });
    }

    function setCurationFilter(mode, btn) {
      currentFilterMode = mode;
      document.querySelectorAll('.filter-pills .filter-pill').forEach(p => p.classList.remove('active'));
      if (btn) btn.classList.add('active');
      filterWorks();
    }

    function setWorkFilter(cat, btn) {
      setCurationFilter(cat, btn);
    }

    function toggleSortOrder() {
      currentSortAsc = !currentSortAsc;
      const btn = document.getElementById('sort-btn');
      if (btn) btn.textContent = currentSortAsc ? "↑ Chronological" : "↓ Latest First";

      const stack = document.getElementById('works-stack');
      if (stack) {
        const items = Array.from(stack.querySelectorAll('.work-item'));
        items.reverse().forEach(item => stack.appendChild(item));
      }
    }

    function toggleViewMode() {
      const stack = document.getElementById('works-stack');
      const btn = document.getElementById('view-mode-btn');
      if (!stack) return;
      stack.classList.toggle('grid-view');
      const isGrid = stack.classList.contains('grid-view');
      if (btn) {
        btn.textContent = isGrid ? "☰ Stack View" : "⊞ Salon Grid";
        btn.classList.toggle('active', isGrid);
      }
    }
"""

    # Replace the existing filtering block in JS
    js_pattern = r'/\* =========================================================================\s*SEARCH, FILTER, SORT & VIEW MODE CONTROLS[\s\S]*?/\* =========================================================================\s*AUDIO VISUALIZER'
    replacement = new_js_filtering + "\n    /* =========================================================================\n       AUDIO VISUALIZER"
    html = re.sub(js_pattern, replacement, html, count=1)
    print("[+] Replaced JavaScript filter logic with Curatorial Engine")

    # Hook initial filter on DOMContentLoaded
    if 'filterWorks();' not in html:
        html = html.replace("handleUrlHash();", "handleUrlHash();\n      filterWorks();")

    with open(GALLERY_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("[✓] gallery/index.html curation overhaul complete!")

if __name__ == "__main__":
    enhance_gallery()
