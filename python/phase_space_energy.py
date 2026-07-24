#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.integrators import harmonic_energy, leapfrog
from pardon_math.plot_style import BLUE, GREEN, MUTED, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    dt, steps = 0.04, 640
    trajectory = leapfrog(1.35, 0.0, dt, steps)
    energy = harmonic_energy(trajectory[:, 0], trajectory[:, 1])
    error = np.maximum(np.abs(energy - energy[0]), 1e-16)
    q = np.linspace(-1.75, 1.75, 240)
    p = np.linspace(-1.75, 1.75, 240)
    Q, P = np.meshgrid(q, p)
    H = harmonic_energy(Q, P)
    frame_values = np.unique(np.linspace(1, len(trajectory), 110, dtype=int))

    fig, (ax_phase, ax_error) = plt.subplots(1, 2)
    add_header(
        fig,
        "Leapfrog orbit on harmonic-energy contours",
        f"The phase path and bounded energy error are shown together (dt={dt}, {steps} steps).",
    )
    add_footer(fig, "Scope: harmonic oscillator benchmark for numerical structure preservation; not an SSZ geodesic.")

    style_axes(ax_phase, "Phase-space trajectory")
    ax_phase.set_aspect("equal")
    contours = ax_phase.contour(Q, P, H, levels=np.linspace(0.2, 1.6, 8), colors=BLUE, alpha=0.28, linewidths=1.0)
    ax_phase.clabel(contours, fmt="%.1f", fontsize=7)
    ax_phase.set_xlim(-1.65, 1.65)
    ax_phase.set_ylim(-1.65, 1.65)
    ax_phase.set_xlabel("q")
    ax_phase.set_ylabel("p")
    path_line, = ax_phase.plot([], [], color=GREEN, lw=2.7, label="leapfrog path")
    current = ax_phase.scatter([], [], s=65, color=RED, zorder=5, label="current state")
    ax_phase.legend(loc="upper right")

    style_axes(ax_error, "Absolute energy error")
    ax_error.set_xlabel("step")
    ax_error.set_ylabel("|H_n - H_0|")
    ax_error.set_yscale("log")
    ax_error.set_xlim(0, steps)
    ax_error.set_ylim(max(1e-16, float(error.min()) / 2), float(error.max()) * 2.0)
    error_line, = ax_error.plot([], [], color=RED)
    error_dot = ax_error.scatter([], [], s=55, color=RED, zorder=5)
    ax_error.text(
        0.04,
        0.94,
        f"H_0 = {energy[0]:.8f}\nerror band = {energy.max() - energy.min():.3e}",
        transform=ax_error.transAxes,
        va="top",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    def update(n: int):
        path_line.set_data(trajectory[:n, 0], trajectory[:n, 1])
        current.set_offsets(trajectory[[n - 1]])
        x = np.arange(n)
        error_line.set_data(x, error[:n])
        error_dot.set_offsets([[n - 1, error[n - 1]]])
        return path_line, current, error_line, error_dot

    finish_layout(fig)
    save_animation(fig, update, frame_values, OUT, "phase_space_energy", fps=18)
    print("wrote phase-space energy visualizations")


if __name__ == "__main__":
    main()
