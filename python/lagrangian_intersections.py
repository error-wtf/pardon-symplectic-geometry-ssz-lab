#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.lagrangian import curve_a, curve_b, nearest_intersections

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    A = curve_a()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_title("Toy Lagrangian intersections on a torus square")
    ax.set_xlabel("x mod 1")
    ax.set_ylabel("y mod 1")
    ax.grid(True, alpha=0.25)
    ax.plot(A[:, 0], A[:, 1], lw=2, color="#1f77b4", label="L0")
    line_b, = ax.plot([], [], lw=2, color="#ff7f0e", label="L1")
    scatter = ax.scatter([], [], s=70, color="#d62728", zorder=5, label="near intersections")
    text = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top")
    ax.legend(loc="lower right")

    def update(frame: int):
        phase = frame / 96
        B = curve_b(phase)
        hits = nearest_intersections(A, B)
        line_b.set_data(B[:, 0], B[:, 1])
        scatter.set_offsets(hits if len(hits) else np.empty((0, 2)))
        text.set_text(f"phase = {phase:.2f}\nnear intersections = {len(hits)}")
        return line_b, scatter, text

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "lagrangian_intersections.png", dpi=160)
    FuncAnimation(fig, update, frames=96, interval=60).save(OUT / "lagrangian_intersections.gif", writer=PillowWriter(fps=18))
    plt.close(fig)
    print("wrote Lagrangian intersection visualizations")


if __name__ == "__main__":
    main()
