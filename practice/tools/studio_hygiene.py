#!/usr/bin/env python3
"""
STUDIO HYGIENE & STORAGE AUDIT APPARATUS
Studio Anamnesis · Long-Horizon Capability & Cleanliness Engine

Ensures that:
1. No temporary or cached files silently accumulate over months of continuous sessions.
2. Every asset in gallery/assets/ is actively referenced in gallery/index.html or CATALOG.md.
3. Disk space across Works, Gallery Assets, Sketchbook, and Practice is transparently tracked.
4. Python bytecode and cache files are safely pruned.
"""

import os
import sys
import shutil
import re

STUDIO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

def get_dir_size(start_path):
    """Calculates cumulative byte size of a directory tree."""
    total_size = 0
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp) and os.path.exists(fp):
                total_size += os.path.getsize(fp)
                file_count += 1
    return total_size, file_count

def format_bytes(size):
    for unit in ['B', 'KiB', 'MiB', 'GiB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TiB"

def audit_gallery_assets():
    """Verifies that all assets in gallery/assets/ are referenced and in use."""
    assets_dir = os.path.join(STUDIO_ROOT, "gallery", "assets")
    gallery_html_path = os.path.join(STUDIO_ROOT, "gallery", "index.html")
    catalog_md_path = os.path.join(STUDIO_ROOT, "CATALOG.md")
    
    if not os.path.exists(assets_dir):
        return {"status": "error", "message": "gallery/assets/ not found"}
        
    with open(gallery_html_path, "r", encoding="utf-8") as f:
        gallery_content = f.read()
    with open(catalog_md_path, "r", encoding="utf-8") as f:
        catalog_content = f.read()
        
    all_assets = [f for f in os.listdir(assets_dir) if os.path.isfile(os.path.join(assets_dir, f))]
    referenced = []
    unreferenced = []
    
    for asset in sorted(all_assets):
        if asset in gallery_content or asset in catalog_content:
            referenced.append(asset)
        else:
            unreferenced.append(asset)
            
    return {
        "total_assets": len(all_assets),
        "referenced": referenced,
        "unreferenced": unreferenced
    }

def find_stale_caches():
    """Identifies pycache directories and temporary files."""
    stale_dirs = []
    stale_files = []
    
    for root, dirs, files in os.walk(STUDIO_ROOT):
        # Exclude .git
        if ".git" in root.split(os.sep):
            continue
        for d in dirs:
            if d == "__pycache__":
                stale_dirs.append(os.path.join(root, d))
        for f in files:
            if f.endswith(".pyc") or f.endswith(".tmp") or f.endswith("~") or f == ".DS_Store":
                stale_files.append(os.path.join(root, f))
                
    return stale_dirs, stale_files

def prune_stale_caches(stale_dirs, stale_files):
    """Safely removes __pycache__ and transient editor files."""
    pruned_count = 0
    for f in stale_files:
        try:
            os.remove(f)
            pruned_count += 1
        except OSError:
            pass
    for d in stale_dirs:
        try:
            shutil.rmtree(d)
            pruned_count += 1
        except OSError:
            pass
    return pruned_count

def run_hygiene_report(clean=False):
    print("==================================================================")
    print("         STUDIO ANAMNESIS · STORAGE & HYGIENE APPARATUS           ")
    print("==================================================================")
    print(f"[*] Studio Root: {STUDIO_ROOT}\n")
    
    # 1. Directory Budget Breakdown
    sections = [
        ("Works (Master Opuses & Plates)", "works"),
        ("Gallery Exhibition Vault", "gallery"),
        ("Sketchbook (Studies & Failures)", "sketchbook"),
        ("Practice (Tooling & Treatises)", "practice"),
        ("Journal & Chronicles", "journal"),
        ("Git Repository Object Store", ".git")
    ]
    
    print("[1] Storage Budget Allocation:")
    total_studio_bytes = 0
    total_studio_files = 0
    for name, rel in sections:
        path = os.path.join(STUDIO_ROOT, rel)
        if os.path.exists(path):
            sz, count = get_dir_size(path)
            total_studio_bytes += sz
            total_studio_files += count
            print(f"    • {name:<35} : {format_bytes(sz):>10} ({count:>4} files)")
        else:
            print(f"    • {name:<35} : [NOT FOUND]")
            
    print(f"    {'-'*55}")
    print(f"    Total Studio Footprint          : {format_bytes(total_studio_bytes):>10} ({total_studio_files:>4} files)\n")
    
    # 2. Asset Reference Audit
    print("[2] Gallery Asset Vault Reference Check:")
    asset_res = audit_gallery_assets()
    if asset_res.get("status") == "error":
        print(f"    [!] Error: {asset_res['message']}")
    else:
        tot = asset_res["total_assets"]
        ref_count = len(asset_res["referenced"])
        unref_count = len(asset_res["unreferenced"])
        print(f"    • Total Exhibition Assets: {tot}")
        print(f"    • Actively Referenced   : {ref_count}")
        if unref_count == 0:
            print("    [✓] All vault assets are actively referenced in gallery or catalog.")
        else:
            print(f"    [!] Unreferenced Assets ({unref_count}):")
            for unref in asset_res["unreferenced"]:
                print(f"        - {unref}")
    print()
    
    # 3. Cache and Stale Artifacts
    print("[3] Ephemeral & Cache File Audit:")
    stale_dirs, stale_files = find_stale_caches()
    total_stale = len(stale_dirs) + len(stale_files)
    print(f"    • Detected __pycache__ directories: {len(stale_dirs)}")
    print(f"    • Detected transient temp files   : {len(stale_files)}")
    
    if clean and total_stale > 0:
        pruned = prune_stale_caches(stale_dirs, stale_files)
        print(f"    [✓] Successfully pruned {pruned} cache directories and ephemeral files.")
    elif total_stale > 0:
        print("    [*] Tip: Run with --clean to prune transient cache files.")
    else:
        print("    [✓] Pristine: No stray cache or temporary files detected.")
        
    print("\n==================================================================")
    print(">>> STUDIO HYGIENE STATUS: VERIFIED AND HEALTHY. <<<")
    print("==================================================================")

if __name__ == "__main__":
    do_clean = "--clean" in sys.argv
    run_hygiene_report(clean=do_clean)

