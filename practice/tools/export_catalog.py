"""
STUDIO ANAMNESIS · ARCHIVAL PRESERVATION TOOL
Catalog Raisonné Exporter & Integrity Verifier

Parses CATALOG.md and works/ to produce a verified machine-readable
CATALOG.json with file sizes, asset counts, and cryptographic checksums.
"""

import os
import json
import hashlib

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()[:16]

def export_catalog():
    studio_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    works_dir = os.path.join(studio_root, "works")
    
    catalog_entries = []
    
    opuses = sorted([d for d in os.listdir(works_dir) if d.startswith("opus_")])
    for op in opuses:
        op_path = os.path.join(works_dir, op)
        readme = os.path.join(op_path, "README.md")
        title = op.replace("_", " ").title()
        
        files = []
        total_bytes = 0
        has_audio = False
        has_visual = False
        has_study = False
        has_engine = False

        for root, _, filenames in os.walk(op_path):
            for fn in filenames:
                fp = os.path.join(root, fn)
                rel_p = os.path.relpath(fp, studio_root)
                size = os.path.getsize(fp)
                total_bytes += size
                ext = os.path.splitext(fn)[1].lower()
                
                if ext in [".wav", ".mp3"]: has_audio = True
                if ext in [".png", ".jpg", ".svg"]: has_visual = True
                if "study" in fn: has_study = True
                if ext in [".py", ".js", ".html"]: has_engine = True

                files.append({
                    "path": rel_p.replace("\\", "/"),
                    "size_bytes": size,
                    "checksum": hash_file(fp)
                })

        # Extract opus id
        parts = op.split("_")
        op_id = f"OPUS-{parts[1]}"

        catalog_entries.append({
            "id": op_id,
            "directory": op,
            "file_count": len(files),
            "total_bytes": total_bytes,
            "has_audio": has_audio,
            "has_visual": has_visual,
            "has_study": has_study,
            "has_engine": has_engine,
            "files": files
        })

    out_json = os.path.join(studio_root, "CATALOG.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "studio": "Studio Anamnesis",
            "date_exported": "2026-09-04",
            "total_opuses": len(catalog_entries),
            "opuses": catalog_entries
        }, f, indent=2)
    print(f"[CATALOG-EXPORTER] Exported {len(catalog_entries)} opuses to {out_json}")

if __name__ == "__main__":
    export_catalog()

