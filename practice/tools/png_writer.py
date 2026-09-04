"""
STUDIO ANAMNESIS · PERMANENT STUDIO INFRASTRUCTURE
Pure Python PNG & Imaging Substrate (Zero-Dependency)

Enables lossless 24-bit RGB and 32-bit RGBA PNG generation using only
the Python standard library (zlib, struct). Ensures the studio can produce
monumental 4K UHD plates across any discontinuous execution container.
"""

import zlib
import struct

def write_png(filepath, width, height, rgb_buffer, has_alpha=False):
    """
    Writes raw RGB or RGBA byte buffer to a valid PNG file.
    rgb_buffer: bytes or bytearray of length:
      width * height * 3 (if has_alpha=False)
      width * height * 4 (if has_alpha=True)
    """
    bpp = 4 if has_alpha else 3
    color_type = 6 if has_alpha else 2
    row_bytes = width * bpp
    expected_len = row_bytes * height
    
    if len(rgb_buffer) != expected_len:
        raise ValueError(f"Buffer size {len(rgb_buffer)} does not match expected {expected_len} ({width}x{height}x{bpp})")

    def make_chunk(chunk_type, data):
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xffffffff)
        return length + chunk_type + data + crc

    # PNG Signature
    png_sig = b"\x89PNG\r\n\x1a\n"

    # IHDR Chunk
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    ihdr_chunk = make_chunk(b"IHDR", ihdr_data)

    # Scanlines with filter byte 0 (None)
    scanlines = bytearray()
    for y in range(height):
        scanlines.append(0) # Filter byte: None
        start = y * row_bytes
        scanlines.extend(rgb_buffer[start:start + row_bytes])

    # Compress scanlines
    compressed_data = zlib.compress(scanlines, level=6)
    idat_chunk = make_chunk(b"IDAT", compressed_data)

    # IEND Chunk
    iend_chunk = make_chunk(b"IEND", b"")

    with open(filepath, "wb") as f:
        f.write(png_sig)
        f.write(ihdr_chunk)
        f.write(idat_chunk)
        f.write(iend_chunk)
    print(f"[PNG-WRITER] Successfully wrote {width}x{height} PNG to {filepath}")

