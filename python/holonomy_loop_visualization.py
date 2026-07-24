#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.holonomy import dynamic_loop_deviation, triple_clock_product
from pardon_math.plot_style import (
    BLUE,
    GREEN,
    INK,
    MUTED,
    PURPLE,
    RED,
    add_footer,
    add_header,
    configure,
    finish_layout,
    save_animation,
    style_axes,
)
from pardon_math.ssz_bridge import D_factor

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)

    radii = (1.2, 2.5, 8.0)
    d_values = tuple(float(D_factor(radius)) for radius in radii)
    product = triple_clock_product(radii)
    t = np.linspace(0.0, 2.0 * np.pi, 240)
    dynamic = dynamic_loop_deviation(t)
    representative = int(np.argmax(np.abs(dynamic - 1.0)))

    fig, (ax_static, ax_dynamic) = plt.subplots(1, 2)
    add_header(
        fig,
        "Static cancellation versus a dynamic loop diagnostic",
        "A closed product of static clock ratios telescopes exactly; a non-trivial loop requires additional dynamics.",
    )
    add_footer(
        fig,
        "Scope: the static product is an exact identity of D-ratios in this module. "
        "The purple dynamic curve is illustrative only and is not an SSZ prediction.",
    )

    ax_static.set_title("Static three-clock loop: exact cancellation", loc="left", pad=10, color=INK, weight="bold")
    ax_static.set_xlim(-1.75, 1.75)
    ax_static.set_ylim(-1.35, 1.55)
    ax_static.set_aspect("equal")
    ax_static.axis("off")
    points = np.array([[0.0, 1.05], [1.33, -0.73], [-1.33, -0.73]])
    node_colors = (RED, BLUE, GREEN)
    node_labels = ("A", "B", "C")
    for point, label, radius, d_value, color in zip(points, node_labels, radii, d_values, node_colors):
        ax_static.scatter(*point, s=280, color=color, edgecolor="white", linewidth=1.4, zorder=5)
        offset_y = 0.25 if label == "A" else -0.30
        ax_static.text(
            point[0],
            point[1] + offset_y,
            f"{label}: r={radius:g},  D={d_value:.4f}",
            ha="center",
            va="center",
            fontsize=9,
            weight="bold",
            color=INK,
        )

    edge_specs = ((0, 1, 0.16), (1, 2, -0.14), (2, 0, 0.16))
    edge_labels = []
    for start, end, curvature in edge_specs:
        arrow = FancyArrowPatch(
            points[start],
            points[end],
            arrowstyle="-|>",
            mutation_scale=16,
            lw=2.2,
            color=MUTED,
            connectionstyle=f"arc3,rad={curvature}",
            shrinkA=14,
            shrinkB=14,
        )
        ax_static.add_patch(arrow)
        midpoint = 0.5 * (points[start] + points[end])
        normal = np.array([-(points[end] - points[start])[1], (points[end] - points[start])[0]])
        normal /= np.linalg.norm(normal)
        label_point = midpoint + normal * (0.25 if curvature > 0 else -0.25)
        ratio = d_values[start] / d_values[end]
        edge_labels.append(
            ax_static.text(
                label_point[0],
                label_point[1],
                f"D_{node_labels[start]}/D_{node_labels[end]} = {ratio:.4f}",
                ha="center",
                va="center",
                fontsize=8.5,
                color=INK,
                bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#c9d4de"},
            )
        )

    ax_static.text(
        0.0,
        -1.22,
        f"(D_A/D_B)(D_B/D_C)(D_C/D_A) = {product:.12f}",
        ha="center",
        va="center",
        fontsize=10.2,
        weight="bold",
        color=INK,
        bbox={"boxstyle": "round,pad=0.45", "facecolor": "#e5f3ea", "edgecolor": GREEN},
    )

    style_axes(ax_dynamic, "Dynamic toy: an explicitly different assumption")
    ax_dynamic.plot(t, dynamic, color=PURPLE, lw=2.8, label="1 + 0.03 sin(t) cos(2t)")
    ax_dynamic.axhline(1.0, color=MUTED, ls="--", lw=1.4, label="static identity")
    ax_dynamic.fill_between(t, 1.0, dynamic, color=PURPLE, alpha=0.12)
    ax_dynamic.set_xlim(t.min(), t.max())
    padding = 0.15 * float(dynamic.max() - dynamic.min())
    ax_dynamic.set_ylim(float(dynamic.min()) - padding, float(dynamic.max()) + padding)
    ax_dynamic.set_xlabel("loop phase t")
    ax_dynamic.set_ylabel("toy loop product")
    ax_dynamic.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi], ["0", "pi/2", "pi", "3pi/2", "2pi"])
    ax_dynamic.legend(loc="upper right")
    marker = ax_dynamic.scatter([], [], s=75, color=RED, edgecolor="white", linewidth=0.8, zorder=6)
    dynamic_text = ax_dynamic.text(
        0.03,
        0.06,
        "",
        transform=ax_dynamic.transAxes,
        va="bottom",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    def update(index: int):
        marker.set_offsets([[t[index], dynamic[index]]])
        dynamic_text.set_text(f"t = {t[index]:.2f}\ndeviation from 1 = {dynamic[index] - 1.0:+.4f}")
        return marker, dynamic_text, *edge_labels

    finish_layout(fig, top=0.82, bottom=0.14, wspace=0.30)
    save_animation(
        fig,
        update,
        np.unique(np.linspace(0, len(t) - 1, 120, dtype=int)),
        OUT,
        "holonomy_loop",
        fps=20,
        static_frame=representative,
    )
    print("wrote holonomy loop visualizations")


if __name__ == "__main__":
    main()
