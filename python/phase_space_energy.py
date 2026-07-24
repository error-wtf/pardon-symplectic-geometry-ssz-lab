#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.integrators import leapfrog, harmonic_energy

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    q = np.linspace(-1.8, 1.8, 220)
    p = np.linspace(-1.8, 1.8, 220)
    Q, P = np.meshgrid(q, p)
    H = harmonic_energy(Q, P)
    traj = leapfrog(1.35, 0.0, 0.04, 320)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.contour(Q, P, H, levels=12, cmap="viridis", alpha=0.75)
    ax.set_aspect("equal")
    ax.set_title("Phase-space energy contours")
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.grid(True, alpha=0.25)
    line, = ax.plot([], [], color="#d62728", lw=2)
    dot = ax.scatter([], [], s=50, color="#d62728")
    text = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top")

    def update(frame: int):
        path = traj[: frame + 1]
        line.set_data(path[:, 0], path[:, 1])
        dot.set_offsets(traj[[frame]])
        e = harmonic_energy(traj[frame, 0], traj[frame, 1])
        text.set_text(f"step = {frame}\nH = {float(e):.6f}")
        return line, dot, text

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "phase_space_energy.png", dpi=160)
    FuncAnimation(fig, update, frames=len(traj), interval=25).save(OUT / "phase_space_energy.gif", writer=PillowWriter(fps=30))
    plt.close(fig)
    print("wrote phase-space energy visualizations")


if __name__ == "__main__":
    main()
