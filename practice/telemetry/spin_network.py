#!/usr/bin/env python3
"""
spin_network.py
================
Studio Anamnesis · Series XXXIV: Quantum Gravity Foam & Spin Networks
Telemetry & Mathematical Engine for Loop Quantum Gravity (LQG) & Quantum Bounce

Computes:
1. $SU(2)$ Spin Network Discrete Area Eigenvalues: A(j) = 8π γ ℓ_P² √(j(j+1))
2. Minimal Area Gap: Δ_min = 4π √3 γ ℓ_P²
3. Intertwiner Volume Eigenvalues for 4-valent Planckian tetrahedra
4. Loop Quantum Cosmology (LQC) Critical Bounce Density: ρ_crit ≈ 0.41 ρ_P
5. 3D Spin Network Graph Generation with Discrete Geometric Invariants

Zero external dependencies (pure Python standard library).
"""

import math
import sys
from typing import Dict, List, Tuple, Any

# Fundamental physical constants in SI and Planck units
C_LIGHT: float = 299792458.0             # m/s
G_NEWTON: float = 6.67430e-11            # m^3 kg^-1 s^-2
HBAR: float = 1.054571817e-34            # J s

# Planck units
L_PLANCK: float = math.sqrt((HBAR * G_NEWTON) / (C_LIGHT ** 3))   # 1.616255e-35 m
T_PLANCK: float = L_PLANCK / C_LIGHT                              # 5.391247e-44 s
M_PLANCK: float = math.sqrt((HBAR * C_LIGHT) / G_NEWTON)          # 2.176434e-8 kg
RHO_PLANCK: float = M_PLANCK / (L_PLANCK ** 3)                   # 5.15500e96 kg/m^3

# Barbero-Immirzi Parameter (fixed by black hole entropy matching)
GAMMA_IMMIRZI: float = 0.27406717

# Minimal area gap (j = 1/2)
AREA_GAP_PLANCK: float = 4.0 * math.pi * math.sqrt(3.0) * GAMMA_IMMIRZI  # ~ 5.9654 \ell_P^2
AREA_GAP_SI: float = AREA_GAP_PLANCK * (L_PLANCK ** 2)                  # m^2

# Critical bounce density in LQC
RHO_CRIT_FRACTION: float = math.sqrt(3.0) / (32.0 * (math.pi ** 2) * (GAMMA_IMMIRZI ** 3))  # ~ 0.41
RHO_CRIT_SI: float = RHO_CRIT_FRACTION * RHO_PLANCK                     # kg/m^3


def area_eigenvalue(j: float, units: str = "planck") -> float:
    """
    Computes the discrete area eigenvalue of a surface punctured by a spin-j edge.
    Formula: A(j) = 8π γ ℓ_P² √(j(j+1))
    """
    if j < 0.0:
        raise ValueError("Spin j must be non-negative half-integer.")
    factor = 8.0 * math.pi * GAMMA_IMMIRZI * math.sqrt(j * (j + 1.0))
    if units.lower() == "planck":
        return factor
    return factor * (L_PLANCK ** 2)


def lqc_hubble_rate(rho: float) -> float:
    r"""
    Computes the Loop Quantum Cosmology Hubble expansion rate H = \dot{a}/a.
    Formula: H^2 = (8π G / 3) * rho * (1 - rho / rho_crit)
    Returns H in s^-1.
    """
    if rho <= 0.0:
        return 0.0
    if rho >= RHO_CRIT_SI:
        return 0.0  # At or beyond critical bounce density, expansion halts
    term1 = (8.0 * math.pi * G_NEWTON / 3.0) * rho
    quantum_factor = 1.0 - (rho / RHO_CRIT_SI)
    h_sq = term1 * quantum_factor
    return math.sqrt(max(0.0, h_sq))


class SpinNetworkGraph:
    """
    Represents a discrete, background-independent spin network graph in 3D.
    Nodes carry discrete 3-volume; edges carry SU(2) spin representations j and 2-area.
    """
    def __init__(self, num_nodes: int = 48, seed: int = 42):
        self.num_nodes = num_nodes
        self.seed = seed
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self._build_graph()

    def _pseudo_rand(self, idx: int) -> float:
        # Deterministic zero-dependency pseudo-random float [0, 1)
        val = math.sin(idx * 12.9898 + self.seed * 78.233) * 43758.5453
        return val - math.floor(val)

    def _build_graph(self):
        # 1. Place nodes in a normalized spherical cluster
        for i in range(self.num_nodes):
            u = self._pseudo_rand(i * 3 + 1)
            v = self._pseudo_rand(i * 3 + 2)
            w = self._pseudo_rand(i * 3 + 3)
            
            theta = 2.0 * math.pi * u
            phi = math.acos(2.0 * v - 1.0)
            r = (w ** (1.0 / 3.0)) * 0.95
            
            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)
            
            # Quanta of volume (proportional to node valence)
            self.nodes.append({
                "id": i,
                "x": x, "y": y, "z": z,
                "volume_planck": 0.0,
                "valence": 0
            })

        # 2. Connect nearby nodes with SU(2) spin edges
        # Available spin representations: j in {1/2, 1, 3/2, 2, 5/2, 3}
        spins_allowed = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        
        edge_count = 0
        for i in range(self.num_nodes):
            for j_idx in range(i + 1, self.num_nodes):
                n1 = self.nodes[i]
                n2 = self.nodes[j_idx]
                dist = math.sqrt((n1["x"] - n2["x"]) ** 2 + 
                                 (n1["y"] - n2["y"]) ** 2 + 
                                 (n1["z"] - n2["z"]) ** 2)
                
                # Connection threshold for geometric proximity
                if dist < 0.42:
                    edge_count += 1
                    spin_choice = spins_allowed[int(self._pseudo_rand(edge_count * 5) * len(spins_allowed))]
                    area_val = area_eigenvalue(spin_choice, units="planck")
                    
                    self.edges.append({
                        "node1": i,
                        "node2": j_idx,
                        "spin": spin_choice,
                        "area_planck": area_val,
                        "length": dist
                    })
                    
                    n1["valence"] += 1
                    n2["valence"] += 1

        # 3. Compute volume eigenvalues for each node from incident spins
        for n in self.nodes:
            # Tetrahedral intertwiner volume approximation V ~ (sum j_i)^(3/2) * 0.3
            incident_spins = [e["spin"] for e in self.edges if e["node1"] == n["id"] or e["node2"] == n["id"]]
            sum_j = sum(incident_spins)
            n["volume_planck"] = (sum_j ** 1.5) * 0.35 if sum_j > 0 else 0.0

    def total_area(self) -> float:
        return sum(e["area_planck"] for e in self.edges)

    def total_volume(self) -> float:
        return sum(n["volume_planck"] for n in self.nodes)

    def summary(self) -> Dict[str, Any]:
        return {
            "num_nodes": len(self.nodes),
            "num_edges": len(self.edges),
            "total_area_planck": round(self.total_area(), 3),
            "total_volume_planck": round(self.total_volume(), 3),
            "area_gap_planck": round(AREA_GAP_PLANCK, 3),
            "immirzi_parameter": GAMMA_IMMIRZI,
            "critical_density_fraction": round(RHO_CRIT_FRACTION, 4)
        }


def print_spin_network_report():
    print("=" * 72)
    print("      STUDIO ANAMNESIS · SERIES XXXIV: SPIN NETWORK TELEMETRY       ")
    print("=" * 72)
    print(f"Planck Length ℓ_P           : {L_PLANCK:.4e} m")
    print(f"Planck Time τ_P             : {T_PLANCK:.4e} s")
    print(f"Planck Density ρ_P          : {RHO_PLANCK:.4e} kg/m³")
    print(f"Barbero-Immirzi Parameter γ : {GAMMA_IMMIRZI:.6f}")
    print(f"Minimal Area Gap Δ_min      : {AREA_GAP_PLANCK:.4f} ℓ_P² ({AREA_GAP_SI:.4e} m²)")
    print(f"LQC Critical Bounce Density : {RHO_CRIT_FRACTION:.4f} ρ_P ({RHO_CRIT_SI:.4e} kg/m³)")
    print("-" * 72)
    print("SU(2) Area Operator Spectrum [A(j) = 8π γ ℓ_P² √(j(j+1))]:")
    for j in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        a_p = area_eigenvalue(j, "planck")
        a_si = area_eigenvalue(j, "si")
        print(f"  j = {j:3.1f} | A(j) = {a_p:8.4f} ℓ_P² | {a_si:.4e} m²")
    print("-" * 72)
    
    net = SpinNetworkGraph(num_nodes=64, seed=108)
    info = net.summary()
    print("Cluster Spin Network Realization:")
    print(f"  Nodes (Quanta of Volume)  : {info['num_nodes']}")
    print(f"  Edges (Quanta of Area)    : {info['num_edges']}")
    print(f"  Total Quantum Area        : {info['total_area_planck']} ℓ_P²")
    print(f"  Total Quantum Volume      : {info['total_volume_planck']} ℓ_P³")
    print("=" * 72)


if __name__ == "__main__":
    print_spin_network_report()
