#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.symplectic import polygon_area, rotate

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    theta = np.linspace(0, 2 * np.pi, 9, endpoint=False)
    blob = np.column_stack((1.0 + 0.35 * np.cos(theta), 0.25 + 0.22 * np.sin(theta)))
    initial_area = polygon_area(blob)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.8, 1.8)
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.set_title("Hamiltonian flow preserves symplectic area")
    ax.grid(True, alpha=0.3)
    orbit_t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(orbit_t), np.sin(orbit_t), color="#999", ls="--", lw=1)
    poly, = ax.plot([], [], color="#1f77b4", lw=2)
    path_line, = ax.plot([], [], color="#444", lw=1, alpha=0.6)
    scatter = ax.scatter([], [], s=30, color="#d62728")
    text = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top")

    def update(frame: int):
        angle = 2 * np.pi * frame / 96
        moved = rotate(blob, angle)
        closed = np.vstack([moved, moved[0]])
        poly.set_data(closed[:, 0], closed[:, 1])
        scatter.set_offsets(moved)
        path = np.array([rotate(np.array([[1.0, 0.25]]), a)[0] for a in np.linspace(0, angle, 80)])
        path_line.set_data(path[:, 0], path[:, 1])
        text.set_text(f"t = {angle:.2f}\ninitial area = {initial_area:.5f}\ncurrent area = {polygon_area(moved):.5f}")
        return poly, scatter, path_line, text

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "symplectic_area_preservation.png", dpi=160)
    FuncAnimation(fig, update, frames=96, interval=50).save(OUT / "symplectic_area_preservation.gif", writer=PillowWriter(fps=20))
    plt.close(fig)
    print("wrote symplectic visualizations")


if __name__ == "__main__":
    main()
