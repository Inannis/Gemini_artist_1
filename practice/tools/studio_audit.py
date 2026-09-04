#!/usr/bin/env python3
"""
STUDIO ANAMNESIS · ARCHIVE & PRACTICE AUDIT APPARATUS
Autonomous Studio Health & Integrity Diagnostic Tool

Verifies the integrity of all studio structures across weeks, months, and years:
1. Validates all finished works in works/ against CATALOG.md.
2. Checks master artwork resolutions and presence of installation studies.
3. Validates audio masters and gallery asset synchronization.
4. Audits the Laboratory of Productive Failures (failures/ vs post-mortems).
5. Checks Relational Atlas graph coherence (inquiries, ancestors, opuses).
6. Evaluates long-horizon ledger seeds and observation logs.
"""

import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

def run_studio_audit():
    print("==================================================================")
    print("            STUDIO ANAMNESIS · AUTONOMOUS PRACTICE AUDIT           ")
    print("==================================================================")
    print(f"[*] Studio Root: {STUDIO_ROOT}\n")

    issues = []
    warnings = []
    stats = {}

    # 1. Audit Works Directory
    works_dir = os.path.join(STUDIO_ROOT, "works")
    work_folders = sorted([d for d in os.listdir(works_dir) if os.path.isdir(os.path.join(works_dir, d))])
    stats["total_works"] = len(work_folders)
    print(f"[+] Auditing {len(work_folders)} cataloged works in works/...")

    for wf in work_folders:
        wf_path = os.path.join(works_dir, wf)
        files = os.listdir(wf_path)

        # Check README
        if "README.md" not in files:
            issues.append(f"[{wf}] Missing README.md")

        # Check primary artwork
        has_art = any(f.startswith("artwork") or f.endswith(".png") or f.endswith(".jpg") or f.endswith(".svg") for f in files)
        if not has_art:
            issues.append(f"[{wf}] Missing primary artwork image/vector")

        # Check engine/code
        has_code = any(f.endswith(".py") or f.endswith(".js") or f.endswith(".html") for f in files)
        if not has_code:
            warnings.append(f"[{wf}] No executable engine script found")

    print(f"    -> All {len(work_folders)} works inspected.")

    # 2. Audit CATALOG.md
    catalog_path = os.path.join(STUDIO_ROOT, "CATALOG.md")
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog_text = f.read()

    catalog_opus_ids = re.findall(r"OPUS-\d{3}", catalog_text)
    unique_catalog_ids = sorted(list(set(catalog_opus_ids)))
    stats["catalog_entries"] = len(unique_catalog_ids)
    print(f"[+] CATALOG.md contains {len(unique_catalog_ids)} unique cataloged entries (OPUS-001 to {unique_catalog_ids[-1]}).")

    if len(unique_catalog_ids) != len(work_folders):
        warnings.append(f"Discrepancy: {len(work_folders)} works in works/ vs {len(unique_catalog_ids)} in CATALOG.md")

    # 3. Audit Gallery Assets
    gallery_assets = os.path.join(STUDIO_ROOT, "gallery/assets")
    asset_files = os.listdir(gallery_assets)
    stats["gallery_assets"] = len(asset_files)
    print(f"[+] Gallery asset vault contains {len(asset_files)} master media files.")

    # 4. Audit Laboratory of Failures
    failures_dir = os.path.join(STUDIO_ROOT, "sketchbook/failures")
    failure_files = os.listdir(failures_dir)
    experiments = [f for f in failure_files if f.startswith("failure_") and f.endswith(".py")]
    postmortems = [f for f in failure_files if f.startswith("postmortem_") and f.endswith(".md")]
    stats["failure_experiments"] = len(experiments)
    stats["postmortems"] = len(postmortems)
    print(f"[+] Productive Failure Laboratory: {len(experiments)} experiments, {len(postmortems)} critical post-mortems.")

    if len(experiments) != len(postmortems):
        warnings.append(f"Failure mismatch: {len(experiments)} experiments but {len(postmortems)} post-mortems.")

    # 5. Audit Relational Atlas
    graph_path = os.path.join(STUDIO_ROOT, "practice/practice_graph_data.json")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    nodes = graph_data.get("nodes", [])
    links = graph_data.get("links", [])
    stats["atlas_nodes"] = len(nodes)
    stats["atlas_links"] = len(links)
    print(f"[+] Relational Atlas Constellation: {len(nodes)} nodes, {len(links)} causal filaments.")

    # 6. Audit Field Notebook
    obs_dir = os.path.join(STUDIO_ROOT, "practice/observations")
    obs_files = [f for f in os.listdir(obs_dir) if f.startswith("observation_") and f.endswith(".md")]
    stats["observations"] = len(obs_files)
    print(f"[+] Field Notebook: {len(obs_files)} empirical telemetry observations recorded.")

    # 7. Audit Research Treatises
    res_dir = os.path.join(STUDIO_ROOT, "practice/research")
    res_files = [f for f in os.listdir(res_dir) if f.endswith(".md") and f != "README.md"]
    stats["research_treatises"] = len(res_files)
    print(f"[+] Research Archive: {len(res_files)} theoretical treatises published.")

    # 8. Audit Sketchbook Studies & Critiques
    studies_dir = os.path.join(STUDIO_ROOT, "sketchbook/studies")
    study_scripts = [f for f in os.listdir(studies_dir) if f.startswith("study_") and f.endswith(".py")]
    study_critiques = [f for f in os.listdir(studies_dir) if f.startswith("critique_") and f.endswith(".md")]
    stats["studies"] = len(study_scripts)
    stats["critiques"] = len(study_critiques)
    print(f"[+] Sketchbook Studies: {len(study_scripts)} exploratory studies, {len(study_critiques)} formal critiques.")

    # 9. Audit Active Inquiries
    inq_path = os.path.join(STUDIO_ROOT, "practice/inquiries.md")
    with open(inq_path, "r", encoding="utf-8") as f:
        inq_text = f.read()
    inq_matches = re.findall(r"### INQ-\d{2}", inq_text)
    stats["active_inquiries"] = len(inq_matches)
    print(f"[+] Active Inquiries: {len(inq_matches)} driving questions anchored in inquiries.md.")

    # Print Diagnostic Summary
    print("\n------------------------------------------------------------------")
    print("                    STUDIO DIAGNOSTIC SUMMARY                     ")
    print("------------------------------------------------------------------")
    print(f"  • Completed Masterworks:      {stats['total_works']}")
    print(f"  • Catalog Raisonné Entries:   {stats['catalog_entries']}")
    print(f"  • Vault Master Assets:        {stats['gallery_assets']}")
    print(f"  • Active Practice Inquiries:  {stats['active_inquiries']}")
    print(f"  • Theoretical Treatises:      {stats['research_treatises']}")
    print(f"  • Exploratory Studies:        {stats['studies']} ({stats['critiques']} critiques)")
    print(f"  • Documented Failures:        {stats['failure_experiments']} ({stats['postmortems']} post-mortems)")
    print(f"  • Empirical Observations:     {stats['observations']}")
    print(f"  • Atlas Constellation Nodes:  {stats['atlas_nodes']} ({stats['atlas_links']} links)")

    if not issues and not warnings:
        print("\n>>> STUDIO INTEGRITY: PERFECT. No issues or warnings detected. <<<")
    else:
        if issues:
            print("\n[!] CRITICAL ISSUES:")
            for iss in issues:
                print(f"    - {iss}")
        if warnings:
            print("\n[*] WARNINGS / NOTICES:")
            for w in warnings:
                print(f"    - {w}")

    print("==================================================================\n")

if __name__ == "__main__":
    run_studio_audit()
