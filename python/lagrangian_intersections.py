#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.lagrangian import curve_a, curve_b, nearest_intersections
from pardon_math.plot_style import BLUE, AMBER, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    curve_0 = curve_a()
    phases = np.linspace(0.0, 0.99, 90)
    moving_curves = [curve_b(float(phase)) for phase in phases]
    intersections = [nearest_intersections(curve_0, moving) for moving in moving_curves]
    counts = np.array([len(points) for points in intersections])
    representative = int(np.argmax(counts))

    fig, (ax_torus, ax_count) = plt.subplots(1, 2)
    add_header(
        fig,
        "Toy Lagrangian intersections under phase translation",
        "A fixed periodic curve is intersected by a translated diagonal; separated periodic crossings change with phase.",
    )
    add_footer(fig, "Scope: sampled and clustered intersections in a torus-square toy model; not Floer homology or a Fukaya category.")

    style_axes(ax_torus, "Curves on the unit torus square")
    ax_torus.set_xlim(0, 1)
    ax_torus.set_ylim(0, 1)
    ax_torus.set_aspect("equal")
    ax_torus.set_xlabel("x mod 1")
    ax_torus.set_ylabel("y mod 1")
    ax_torus.plot(curve_0[:, 0], curve_0[:, 1], color=BLUE, label="fixed L0")
    moving_line, = ax_torus.plot([], [], color=AMBER, label="translated L1")
    hits = ax_torus.scatter([], [], s=75, color=RED, edgecolor="white", linewidth=0.8, zorder=5, label="detected intersections")
    ax_torus.legend(loc="lower right")
    phase_text = ax_torus.text(
        0.03,
        0.96,
        "",
        transform=ax_torus.transAxes,
        va="top",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    style_axes(ax_count, "Separated intersection candidates vs phase")
    ax_count.step(phases, counts, where="mid", color=BLUE, lw=2.2)
    ax_count.set_xlim(0, 1)
    ax_count.set_ylim(-0.3, max(1.5, float(counts.max()) + 0.8))
    ax_count.set_xlabel("translation phase")
    ax_count.set_ylabel("separated candidate count")
    count_marker = ax_count.scatter([], [], s=75, color=RED, zorder=5)
    ax_count.text(
        0.03,
        0.96,
        "Candidates are local minima of periodic distance.\nSampling still bounds numerical precision.",
        transform=ax_count.transAxes,
        va="top",
        color="#5d6c7b",
    )

    def update(frame: int):
        moving = moving_curves[frame]
        current_hits = intersections[frame]
        moving_line.set_data(moving[:, 0], moving[:, 1])
        hits.set_offsets(current_hits if len(current_hits) else np.empty((0, 2)))
        count_marker.set_offsets([[phases[frame], counts[frame]]])
        phase_text.set_text(f"phase = {phases[frame]:.3f}\ncount = {counts[frame]}")
        return moving_line, hits, count_marker, phase_text

    finish_layout(fig)
    save_animation(
        fig,
        update,
        range(len(phases)),
        OUT,
        "lagrangian_intersections",
        fps=16,
        static_frame=representative,
    )
    print("wrote Lagrangian intersection visualizations")


if __name__ == "__main__":
    main()
