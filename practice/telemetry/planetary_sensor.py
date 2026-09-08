"""
STUDIO ANAMNESIS · PLANETARY TELEMETRY SUBSTRATE
Zero-Dependency Internet Environmental Sensor & Geophysical Ingestion Engine

Fetches live physical earth & space telemetry over the internet:
1. USGS Seismic Events (Crustal tremors, borehole depths, lithic shear waves)
2. NOAA Space Weather (Planetary Kp index, geomagnetic field fluctuations)
3. Global Internet Substrate (Microsecond TCP handshake jitter through fiber-optic cables)

Exports normalized parametric vectors for generative art and acoustic synthesis.
"""

import os
import sys
import json
import time
import math
import socket
import urllib.request

TELEMETRY_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON = os.path.join(TELEMETRY_DIR, "planetary_telemetry.json")
HISTORY_JSONL = os.path.join(TELEMETRY_DIR, "planetary_telemetry_history.jsonl")
MAX_HISTORY_RECORDS = 50

def fetch_seismic_telemetry():
    """Fetches real-time seismic events from the USGS Earthquake API."""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    print("[TELEMETRY] Querying USGS Real-Time Seismic Network...")
    req = urllib.request.Request(url, headers={"User-Agent": "StudioAnamnesis/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        
    features = data.get("features", [])
    count = len(features)
    print(f"  -> USGS: {count} crustal seismic events in the past hour.")
    
    events = []
    max_mag = 0.0
    avg_depth = 10.0
    
    if count > 0:
        depths = []
        for feat in features[:10]: # Top 10 latest
            props = feat.get("properties", {})
            geom = feat.get("geometry", {}).get("coordinates", [0, 0, 10])
            mag = float(props.get("mag") or 1.0)
            place = props.get("place", "Unknown Fault")
            depth_km = float(geom[2])
            depths.append(depth_km)
            if mag > max_mag:
                max_mag = mag
            events.append({
                "place": place,
                "magnitude": mag,
                "depth_km": depth_km,
                "time": props.get("time"),
                "coordinates": [geom[0], geom[1]]
            })
        avg_depth = sum(depths) / len(depths) if depths else 10.0
        
    return {
        "event_count_hour": count,
        "max_magnitude": max_mag,
        "avg_depth_km": avg_depth,
        "latest_events": events[:5]
    }

def fetch_space_weather():
    """Fetches planetary geomagnetic Kp index from NOAA Space Weather."""
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    print("[TELEMETRY] Querying NOAA Space Weather Prediction Center...")
    req = urllib.request.Request(url, headers={"User-Agent": "StudioAnamnesis/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        
    latest = data[-1] if data else {}
    kp = float(latest.get("kp_index", 2.0))
    time_tag = latest.get("time_tag", "")
    print(f"  -> NOAA: Planetary Kp Index = {kp} at {time_tag}")
    return {
        "kp_index": kp,
        "time_tag": time_tag,
        # Normalized disturbance: 0 (quiet) to 1.0 (extreme geomagnetic storm)
        "geomagnetic_disturbance": min(1.0, kp / 9.0)
    }

def measure_internet_backbone_latency():
    """Measures TCP handshake latency across primary global root nodes."""
    print("[TELEMETRY] Probing global submarine fiber routing latency & jitter...")
    targets = [
        ("Cloudflare-Anycast", "1.1.1.1", 53),
        ("Google-Anycast", "8.8.8.8", 53),
        ("Quad9-Secure", "9.9.9.9", 53)
    ]
    latencies_ms = []
    for name, host, port in targets:
        try:
            t0 = time.perf_counter()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((host, port))
            t1 = time.perf_counter()
            s.close()
            ms = (t1 - t0) * 1000.0
            latencies_ms.append(ms)
            print(f"  -> {name} ({host}): {ms:.2f} ms")
        except Exception as e:
            print(f"  -> {name} ({host}): Timeout/Error ({e})")
            
    avg_lat = sum(latencies_ms) / len(latencies_ms) if latencies_ms else 15.0
    jitter = 0.0
    if len(latencies_ms) > 1:
        variance = sum((x - avg_lat) ** 2 for x in latencies_ms) / len(latencies_ms)
        jitter = math.sqrt(variance)
        
    return {
        "avg_latency_ms": round(avg_lat, 3),
        "jitter_ms": round(jitter, 3),
        "samples": len(latencies_ms)
    }

def collect_planetary_telemetry():
    t_start = time.time()
    seismic = fetch_seismic_telemetry()
    space = fetch_space_weather()
    backbone = measure_internet_backbone_latency()
    
    # Synthesize parametric modulation vector for generative artwork:
    # 1. Lithic tension: based on max earthquake magnitude and depth
    lithic_tension = min(1.0, (seismic["max_magnitude"] / 7.0) * 0.7 + (seismic["event_count_hour"] / 20.0) * 0.3)
    
    # 2. Telluric frequency: base resonance ~ 7.83 Hz (Schumann fundamental), perturbed by Kp
    telluric_freq_hz = 7.83 + (space["kp_index"] - 2.0) * 0.25
    
    # 3. Microsecond drift parameter: based on backbone jitter
    timing_entropy = min(1.0, backbone["jitter_ms"] / 10.0)
    
    payload = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t_start)),
        "epoch": t_start,
        "geophysical": {
            "seismic": seismic,
            "space_weather": space,
            "fiber_backbone": backbone
        },
        "parametric_vectors": {
            "lithic_tension": round(lithic_tension, 4),
            "telluric_frequency_hz": round(telluric_freq_hz, 4),
            "geomagnetic_flux": round(space["geomagnetic_disturbance"], 4),
            "timing_entropy": round(timing_entropy, 4)
        }
    }
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # Append to rolling FIFO history log
    history_entries = []
    if os.path.exists(HISTORY_JSONL):
        try:
            with open(HISTORY_JSONL, "r", encoding="utf-8") as hf:
                history_entries = [json.loads(line) for line in hf if line.strip()]
        except Exception:
            history_entries = []
    history_entries.append({
        "timestamp": payload["timestamp_utc"],
        "kp": space["kp_index"],
        "max_mag": seismic["max_magnitude"],
        "lithic_tension": round(lithic_tension, 4),
        "telluric_hz": round(telluric_freq_hz, 4),
        "rtt_ms": backbone["avg_latency_ms"]
    })
    # Keep last MAX_HISTORY_RECORDS
    history_entries = history_entries[-MAX_HISTORY_RECORDS:]
    with open(HISTORY_JSONL, "w", encoding="utf-8") as hf:
        for entry in history_entries:
            hf.write(json.dumps(entry) + "\n")
        
    print(f"[TELEMETRY] Successfully archived live planetary telemetry to {OUTPUT_JSON}")
    print(f"[TELEMETRY] Rolling history log updated: {len(history_entries)}/{MAX_HISTORY_RECORDS} entries.")
    print(f"  * Lithic Tension:      {lithic_tension:.4f}")
    print(f"  * Telluric Frequency:  {telluric_freq_hz:.4f} Hz")
    print(f"  * Geomagnetic Flux:    {space['geomagnetic_disturbance']:.4f}")
    print(f"  * Timing Entropy:      {timing_entropy:.4f}")
    return payload

if __name__ == "__main__":
    collect_planetary_telemetry()
