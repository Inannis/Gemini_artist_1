#!/usr/bin/env python3
"""
OPUS-017: Master Plate Renderer & Encoder
Coordinates the high-performance 4K generation engine and writes the lossless
UHD master PNG plate using pure Python infrastructure.
"""

import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STUDIO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
sys.path.append(os.path.join(STUDIO_ROOT, "practice/tools"))

from png_writer import write_png

WIDTH = 3840
HEIGHT = 2160
RAW_PATH = os.path.join(SCRIPT_DIR, "raw_4k.rgb")
PNG_PATH = os.path.join(SCRIPT_DIR, "artwork.png")
GALLERY_ASSET = os.path.join(STUDIO_ROOT, "gallery/assets/opus_017_artwork.png")

def render_master():
    print("[OPUS-017] Executing desiccation engine...")
    t0 = time.time()
    
    # Run Node.js engine to produce raw binary 4K stream
    js_engine = os.path.join(SCRIPT_DIR, "desiccation_engine.js")
    cmd = ["node", js_engine]
    res = subprocess.run(cmd, cwd=SCRIPT_DIR)
    if res.returncode != 0:
        raise RuntimeError("Engine execution failed")
        
    print(f"[OPUS-017] Engine completed in {time.time() - t0:.2f}s.")
    
    # Read raw RGB bytes
    print(f"[OPUS-017] Reading raw stream from {RAW_PATH}...")
    with open(RAW_PATH, "rb") as f:
        raw_bytes = f.read()
        
    expected_len = WIDTH * HEIGHT * 3
    if len(raw_bytes) != expected_len:
        raise ValueError(f"Raw buffer size mismatch: got {len(raw_bytes)}, expected {expected_len}")
        
    # Encode lossless PNG
    print(f"[OPUS-017] Encoding lossless 4K UHD PNG to {PNG_PATH}...")
    t_enc = time.time()
    write_png(PNG_PATH, WIDTH, HEIGHT, raw_bytes, has_alpha=False)
    print(f"[OPUS-017] PNG encoded in {time.time() - t_enc:.2f}s.")
    
    # Copy to gallery assets
    print(f"[OPUS-017] Installing master plate to {GALLERY_ASSET}...")
    os.makedirs(os.path.dirname(GALLERY_ASSET), exist_ok=True)
    with open(PNG_PATH, "rb") as src, open(GALLERY_ASSET, "wb") as dst:
        dst.write(src.read())
        
    # Clean up raw stream to conserve disk space
    if os.path.exists(RAW_PATH):
        os.remove(RAW_PATH)
        print("[OPUS-017] Cleaned up temporary raw stream.")
        
    print(f"[OPUS-017] Master plate generation complete in {time.time() - t0:.2f}s total.")

if __name__ == "__main__":
    render_master()

