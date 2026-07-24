#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.integrators import explicit_euler, harmonic_energy, leapfrog, symplectic_euler
from pardon_math.plot_style import BLUE, GREEN, MUTED, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    dt, steps = 0.08, 420
    trajectories = {
        "explicit Euler": (explicit_euler(1.0, 0.0, dt, steps), RED),
        "symplectic Euler": (symplectic_euler(1.0, 0.0, dt, steps), BLUE),
        "leapfrog": (leapfrog(1.0, 0.0, dt, steps), GREEN),
    }
    h0 = 0.5
    errors = {
        name: np.maximum(np.abs(harmonic_energy(path[:, 0], path[:, 1]) - h0), 1e-15)
        for name, (path, _) in trajectories.items()
    }
    frame_values = np.unique(np.linspace(1, steps + 1, 120, dtype=int))
    phase_limit = 1.1 * max(float(np.abs(path).max()) for path, _ in trajectories.values())

    fig, (ax_phase, ax_error) = plt.subplots(1, 2)
    add_header(
        fig,
        "Naive vs structure-preserving integration",
        f"The same oscillator is integrated by three methods (dt={dt}, {steps} steps).",
    )
    add_footer(fig, "Interpretation: bounded error is a numerical property of the method, not evidence for a physical model.")

    style_axes(ax_phase, "Phase-space trajectories")
    ax_phase.set_aspect("equal")
    ax_phase.set_xlim(-phase_limit, phase_limit)
    ax_phase.set_ylim(-phase_limit, phase_limit)
    ax_phase.set_xlabel("q")
    ax_phase.set_ylabel("p")
    orbit = np.linspace(0, 2 * np.pi, 360)
    ax_phase.plot(np.cos(orbit), np.sin(orbit), color=MUTED, ls="--", lw=1.2, label="exact energy contour")

    style_axes(ax_error, "Energy error by step")
    ax_error.set_xlabel("step")
    ax_error.set_ylabel("|H_n - H_0|")
    ax_error.set_yscale("log")
    ax_error.set_xlim(0, steps)
    ax_error.set_ylim(5e-16, max(float(values.max()) for values in errors.values()) * 1.4)

    phase_lines = {}
    error_lines = {}
    for name, (path, color) in trajectories.items():
        phase_lines[name], = ax_phase.plot([], [], color=color, label=name)
        error_lines[name], = ax_error.plot([], [], color=color, label=name)
    ax_phase.legend(loc="upper left")
    ax_error.legend(loc="lower right")
    summary = ax_error.text(
        0.03,
        0.96,
        "",
        transform=ax_error.transAxes,
        va="top",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    def update(n: int):
        x = np.arange(n)
        lines = []
        rows = []
        for name, (path, _) in trajectories.items():
            phase_lines[name].set_data(path[:n, 0], path[:n, 1])
            error_lines[name].set_data(x, errors[name][:n])
            rows.append(f"{name}: {errors[name][n - 1]:.2e}")
            lines.extend([phase_lines[name], error_lines[name]])
        summary.set_text("current |H-H0|\n" + "\n".join(rows))
        return (*lines, summary)

    finish_layout(fig)
    save_animation(fig, update, frame_values, OUT, "symplectic_vs_euler", fps=18)
    print("wrote integrator comparison visualizations")


if __name__ == "__main__":
    main()
