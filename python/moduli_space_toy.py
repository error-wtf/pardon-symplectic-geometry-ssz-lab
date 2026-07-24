#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.moduli import circle_moduli_points, solution_dimension_label

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.set_title("Toy moduli space: x^2 + y^2 = a")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)
    pts_plot, = ax.plot([], [], color="#1f77b4", lw=3)
    point = ax.scatter([], [], s=90, color="#d62728")
    text = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top")
    values = np.concatenate([np.linspace(1.0, 0.0, 50), np.linspace(0.0, -0.4, 25), np.linspace(-0.4, 1.0, 60)])

    def update(frame: int):
        a = float(values[frame])
        pts = circle_moduli_points(a)
        if len(pts) > 1:
            closed = np.vstack([pts, pts[0]])
            pts_plot.set_data(closed[:, 0], closed[:, 1])
            point.set_offsets(np.empty((0, 2)))
        elif len(pts) == 1:
            pts_plot.set_data([], [])
            point.set_offsets(pts)
        else:
            pts_plot.set_data([], [])
            point.set_offsets(np.empty((0, 2)))
        text.set_text(f"a = {a:.3f}\nspace = {solution_dimension_label(a)}")
        return pts_plot, point, text

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "moduli_space_toy.png", dpi=160)
    FuncAnimation(fig, update, frames=len(values), interval=55).save(OUT / "moduli_space_toy.gif", writer=PillowWriter(fps=20))
    plt.close(fig)
    print("wrote moduli-space toy visualizations")


if __name__ == "__main__":
    main()
