#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.moduli import circle_moduli_points, solution_dimension_label
from pardon_math.plot_style import BLUE, GREEN, MUTED, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    values = np.linspace(-0.45, 1.0, 100)
    radii = np.sqrt(np.clip(values, 0, None))
    representative = int(np.argmin(np.abs(values - 0.55)))

    fig, (ax_fiber, ax_family) = plt.subplots(1, 2)
    add_header(
        fig,
        "A degenerating toy moduli family",
        "The real solution set of x^2 + y^2 = a changes from empty to singular to a smooth circle.",
    )
    add_footer(fig, "Scope: elementary family illustrating degeneration; it does not construct a virtual fundamental cycle.")

    style_axes(ax_fiber, "Current fiber")
    ax_fiber.set_xlim(-1.15, 1.15)
    ax_fiber.set_ylim(-1.15, 1.15)
    ax_fiber.set_aspect("equal")
    ax_fiber.set_xlabel("x")
    ax_fiber.set_ylabel("y")
    fiber_line, = ax_fiber.plot([], [], color=BLUE, lw=3)
    singular = ax_fiber.scatter([], [], s=110, color=RED, zorder=5)
    empty_text = ax_fiber.text(0.5, 0.5, "", transform=ax_fiber.transAxes, ha="center", va="center", fontsize=17, color=MUTED)
    state_text = ax_fiber.text(
        0.03,
        0.96,
        "",
        transform=ax_fiber.transAxes,
        va="top",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    style_axes(ax_family, "Family across the singular value")
    ax_family.axvspan(values.min(), 0, color="#f4d7d2", alpha=0.65, label="empty")
    ax_family.axvspan(0, values.max(), color="#dcefe4", alpha=0.65, label="smooth circle")
    ax_family.axvline(0, color=RED, lw=2, label="singular fiber")
    ax_family.plot(values[values >= 0], radii[values >= 0], color=GREEN, label="radius sqrt(a)")
    ax_family.set_xlim(values.min(), values.max())
    ax_family.set_ylim(-0.04, 1.08)
    ax_family.set_xlabel("parameter a")
    ax_family.set_ylabel("fiber radius")
    parameter_line = ax_family.axvline(values[0], color=BLUE, lw=2.2)
    parameter_dot = ax_family.scatter([], [], s=70, color=BLUE, zorder=5)
    ax_family.legend(loc="upper left")

    def update(frame: int):
        value = float(values[frame])
        points = circle_moduli_points(value)
        fiber_line.set_data([], [])
        singular.set_offsets(np.empty((0, 2)))
        empty_text.set_text("")
        if len(points) > 1:
            closed = np.vstack([points, points[0]])
            fiber_line.set_data(closed[:, 0], closed[:, 1])
        elif len(points) == 1:
            singular.set_offsets(points)
        else:
            empty_text.set_text("no real solutions")
        parameter_line.set_xdata([value, value])
        parameter_dot.set_offsets([[value, np.sqrt(value) if value >= 0 else 0]])
        state_text.set_text(f"a = {value:.3f}\n{solution_dimension_label(value)}")
        return fiber_line, singular, empty_text, parameter_line, parameter_dot, state_text

    finish_layout(fig)
    save_animation(fig, update, range(len(values)), OUT, "moduli_space_toy", fps=16, static_frame=representative)
    print("wrote moduli-space visualizations")


if __name__ == "__main__":
    main()
