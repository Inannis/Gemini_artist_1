# ZERO-DEPENDENCY STUDIO APPARATUS
### Studio Anamnesis · Permanent Infrastructure & Tools

> *"Tools are transient; methods endure. But reliable, zero-dependency tools ensure the studio can operate autonomously across any environment."*

This directory houses self-contained tools written in pure Python standard library. They ensure that Studio Anamnesis can render monumental 4K visual plates, synthesize broadcast-grade 48kHz audio suites, and audit studio integrity without relying on external package managers (`pip`) or internet access.

---

## Tool Index

| Tool | Language | Standard Modules Used | Purpose & Capabilities |
|---|---|---|---|
| [`png_writer.py`](png_writer.py) | Python 3 | `zlib`, `struct` | Encodes raw RGB and RGBA byte buffers into lossless PNG files. Capable of encoding 4K UHD (3840 × 2160) plates in under 0.3 seconds. |
| [`audio_writer.py`](audio_writer.py) | Python 3 | `wave`, `struct`, `math` | Writes floating-point audio buffers (-1.0 to 1.0) into 16-bit PCM uncompressed 48kHz stereo WAV files with automatic clipping and channel interleaving. |
| [`studio_audit.py`](studio_audit.py) | Python 3 | `os`, `sys`, `re`, `json` | Comprehensive studio health auditor: verifies all 18 works, catalog entries, gallery assets, failure post-mortems, field observations, research treatises, and constellation graph links. |
| [`export_catalog.py`](export_catalog.py) | Python 3 | `os`, `json`, `hashlib` | Generates a cryptographically verified, machine-readable `CATALOG.json` tracking file sizes, component presence, and SHA-256 checksums across all 18 opuses. |
| [`verify_apparatus.py`](verify_apparatus.py) | Python 3 | `os`, `sys`, `math`, `struct` | Automated regression test verifying that PNG generation, WAV header encoding, and diagnostic tools function with 100% integrity. |

