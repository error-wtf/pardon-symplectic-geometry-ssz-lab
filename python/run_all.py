#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "python" / "symplectic_lab.py",
    ROOT / "python" / "phase_space_energy.py",
    ROOT / "python" / "symplectic_integrator_comparison.py",
    ROOT / "python" / "holomorphic_curve_residual.py",
    ROOT / "python" / "lagrangian_intersections.py",
    ROOT / "python" / "moduli_space_toy.py",
    ROOT / "python" / "knot_distortion.py",
    ROOT / "python" / "repo_interplay_map.py",
    ROOT / "python" / "ssz_symplectic_bridge.py",
    ROOT / "python" / "phi_ladder_state_visualization.py",
    ROOT / "python" / "method_assignment_flow.py",
    ROOT / "python" / "holonomy_loop_visualization.py",
    ROOT / "python" / "regime_blend_map.py",
    ROOT / "python" / "hamiltonian_drift_report.py",
    ROOT / "python" / "observable_routing_matrix.py",
    ROOT / "python" / "hamiltonian_drift_visualization.py",
    ROOT / "python" / "test_validation_visualization.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n==> {script.name}")
        subprocess.run([sys.executable, str(script)], check=True)


if __name__ == "__main__":
    main()
