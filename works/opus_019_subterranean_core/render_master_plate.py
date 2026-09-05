"""
STUDIO ANAMNESIS · OPUS-019
The Subterranean Core: Borehole Radiometry at -500 Meters
Master Plate Compression & Inscription Script
"""

import os
import sys
import shutil

# Add practice/tools to sys.path
studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(studio_root, "practice", "tools"))

from png_writer import write_png

def main():
    raw_path = os.path.join(os.path.dirname(__file__), "master_plate_raw.rgb")
    out_png = os.path.join(os.path.dirname(__file__), "artwork.png")
    gallery_png = os.path.join(studio_root, "gallery", "assets", "opus_019_artwork.png")
    
    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} does not exist.")
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
    
    # Clean up raw byte file to conserve disk space
    os.remove(raw_path)
    print(f"[RENDER] Removed temporary raw buffer. Master plate successfully inscribed.")

if __name__ == "__main__":
    main()
