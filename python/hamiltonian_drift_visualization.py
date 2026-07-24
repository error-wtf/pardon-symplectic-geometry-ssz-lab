#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from hamiltonian_drift_report import euler, hamiltonian_radial, leapfrog_ssz, rk4, symplectic_euler_ssz

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    q0, p0, dt, steps = 3.0, 0.05, 0.03, 1000
    methods = {
        "explicit Euler": (euler(q0, p0, dt, steps), "#d62728"),
        "RK4": (rk4(q0, p0, dt, steps), "#9467bd"),
        "symplectic Euler": (symplectic_euler_ssz(q0, p0, dt, steps), "#1f77b4"),
        "leapfrog": (leapfrog_ssz(q0, p0, dt, steps), "#2ca02c"),
    }
    h0 = {name: float(hamiltonian_radial(traj[0, 0], traj[0, 1])) for name, (traj, _) in methods.items()}
    err = {name: np.abs(hamiltonian_radial(traj[:, 0], traj[:, 1]) - h0[name]) + 1e-15 for name, (traj, _) in methods.items()}

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 5))
    ax0.set_title("Toy SSZ radial phase paths")
    ax0.set_xlabel("q = r/r_s")
    ax0.set_ylabel("p")
    ax0.grid(True, alpha=0.25)
    ax0.set_xlim(2.8, 16.6)
    ax0.set_ylim(0.035, 0.08)
    ax1.set_title("Hamiltonian error |H-H0|")
    ax1.set_xlabel("step")
    ax1.set_ylabel("absolute error")
    ax1.set_yscale("log")
    ax1.grid(True, which="both", alpha=0.25)
    ax1.set_xlim(0, steps)
    ax1.set_ylim(1e-10, max(float(v.max()) for v in err.values()) * 1.4)

    phase_lines = {}
    error_lines = {}
    for name, (traj, color) in methods.items():
        phase_lines[name], = ax0.plot([], [], color=color, lw=2.0, label=name)
        error_lines[name], = ax1.plot([], [], color=color, lw=2.0, label=name)
    ax0.legend(loc="upper right", fontsize=8)
    ax1.legend(loc="lower right", fontsize=8)

    frame_count = 220
    frame_indices = np.linspace(1, steps + 1, frame_count, dtype=int)

    def update(frame: int):
        n = int(frame_indices[frame])
        x = np.arange(n)
        artists = []
        for name, (traj, _) in methods.items():
            phase_lines[name].set_data(traj[:n, 0], traj[:n, 1])
            error_lines[name].set_data(x, err[name][:n])
            artists.extend([phase_lines[name], error_lines[name]])
        return artists

    update(frame_count - 1)
    fig.tight_layout()
    fig.savefig(OUT / "hamiltonian_drift_report.png", dpi=160)
    FuncAnimation(fig, update, frames=frame_count, interval=30).save(
        OUT / "hamiltonian_drift_report.gif", writer=PillowWriter(fps=24)
    )
    plt.close(fig)
    print("wrote Hamiltonian drift visualizations")


if __name__ == "__main__":
    main()
