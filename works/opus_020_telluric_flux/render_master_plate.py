"""
STUDIO ANAMNESIS · OPUS-020
The Telluric Flux: Superconducting Meissner Vitrine at 4.2 Kelvin
Master Plate Compression & Inscription Script
"""

import os
import sys
import shutil
import subprocess

studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from png_writer import write_png

def main():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    js_engine = os.path.join(work_dir, "cryo_engine.js")
    raw_path = os.path.join(work_dir, "master_plate_raw.rgb")
    out_png = os.path.join(work_dir, "artwork.png")
    gallery_png = os.path.join(studio_root, "gallery", "assets", "opus_020_artwork.png")
    
    print("[RENDER] Executing procedural cryo engine...")
    subprocess.run(["node", js_engine], check=True)
    
    if not os.path.exists(raw_path):
        print(f"[!] Error: {raw_path} not found.")
        sys.exit(1)
        
    print(f"[RENDER] Reading raw buffer from {raw_path}...")
    with open(raw_path, "rb") as f:
        buffer = f.read()
        
    width = 3840
    height = 2160
    print(f"[RENDER] Compressing 4K plate ({width}x{height}, {len(buffer)} bytes) to lossless PNG...")
    write_png(out_png, width, height, buffer, has_alpha=False)
    
    print(f"[RENDER] Mirroring master plate to gallery: {gallery_png}...")
    shutil.copyfile(out_png, gallery_png)
    
    # Prune temporary raw buffer to keep disk tidy
    if os.path.exists(raw_path):
        os.remove(raw_path)
        print(f"[RENDER] Pruned temporary raw buffer. Master plate successfully inscribed.")

if __name__ == "__main__":
    main()

