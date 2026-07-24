#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.plot_style import (
    AMBER,
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
from pardon_math.regime_guardrails import route_regime
from pardon_math.ssz_bridge import (
    BLEND_END,
    BLEND_START,
    PHOTON_SPHERE_END,
    SSZ_PROFILE,
    STRONG_CONTEXT_END,
    D_factor,
    xi_canonical,
    xi_strong,
    xi_weak,
)

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)

    x = np.linspace(1.0, 12.0, 600)
    representative_value = 2.6
    representative = int(np.argmin(np.abs(x - representative_value)))

    fig = plt.figure()
    grid = fig.add_gridspec(2, 1, height_ratios=(2.2, 1.15))
    ax_curve = fig.add_subplot(grid[0])
    ax_bands = fig.add_subplot(grid[1])
    add_header(
        fig,
        "Physical regime and formula domain are different questions",
        "At x=2.6 the physical context is the photon-sphere region, while the operative Xi expression is already the g1 branch.",
    )
    add_footer(
        fig,
        "Scope: exterior x >= 1 routing from pardon_math.regime_guardrails; the labels describe "
        "repository conventions, not observational confirmation of SSZ.",
    )

    style_axes(ax_curve, "Operative field and its two source branches")
    ax_curve.plot(x, xi_strong(x), color=RED, ls=":", lw=1.8, label="g2 saturation")
    ax_curve.plot(x, xi_weak(x), color=BLUE, ls="--", lw=1.8, label="g1 weak branch")
    ax_curve.plot(x, xi_canonical(x), color=PURPLE, lw=3.0, label="operative Xi")
    ax_curve.axvspan(BLEND_START, BLEND_END, color=AMBER, alpha=0.16, label="C2 blend")
    ax_curve.set_xlim(x.min(), x.max())
    ax_curve.set_ylim(0, max(float(xi_strong(x).max()), float(xi_weak(x).max())) * 1.08)
    ax_curve.set_xlabel("x = r/r_s")
    ax_curve.set_ylabel("Xi(x)")
    ax_curve.legend(loc="upper right", ncol=2)
    marker_curve = ax_curve.axvline(x[0], color="#111827", lw=2.1)
    point_curve = ax_curve.scatter([], [], s=75, color=RED, edgecolor="white", linewidth=0.8, zorder=6)

    ax_bands.set_xlim(-0.85, 5.03)
    ax_bands.set_ylim(0.08, 2.92)
    ax_bands.axis("off")

    columns = (
        ("very close", "x < 1.8", "g2 saturation", "#f3d1cd"),
        ("transition", "1.8 <= x <= 2.2", "C2 blend", "#f8e2bd"),
        ("photon sphere", "2.2 < x <= 3", "g1 weak branch", "#e5dcf1"),
        ("strong context", "3 < x <= 10", "g1 weak branch", "#dcefe4"),
        ("weak field", "x > 10", "g1 weak branch", "#dceaf5"),
    )
    row_specs = ((2.30, "Physical"), (1.42, "Range"), (0.54, "Formula"))
    for y, row_label in row_specs:
        ax_bands.text(-0.12, y, row_label, ha="right", va="center", fontsize=9.5, weight="bold", color=INK)
    for index, (physical, interval, formula, color) in enumerate(columns):
        for y, text in ((2.30, physical), (1.42, interval), (0.54, formula)):
            box = FancyBboxPatch(
                (index + 0.04, y - 0.31),
                0.92,
                0.62,
                boxstyle="round,pad=0.012,rounding_size=0.025",
                facecolor=color if y != 1.42 else "white",
                edgecolor="#c5d0da",
                linewidth=1.1,
            )
            ax_bands.add_patch(box)
            ax_bands.text(index + 0.50, y, text, ha="center", va="center", fontsize=8.3, color=INK, weight="bold" if y != 1.42 else "normal")
    highlight = Rectangle((0.015, 0.17), 0.97, 2.52, fill=False, edgecolor=RED, linewidth=2.8)
    ax_bands.add_patch(highlight)

    state_text = ax_curve.text(
        0.985,
        0.05,
        "",
        transform=ax_curve.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.8,
        color=MUTED,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    def update(index: int):
        value = float(x[index])
        xi = float(xi_canonical(value))
        route = route_regime(value)
        marker_curve.set_xdata([value, value])
        point_curve.set_offsets([[value, xi]])
        column_index = {
            "very_close/g2_context": 0,
            "transition_blend": 1,
            "photon_sphere_context": 2,
            "strong_context/g1_formula": 3,
            "weak_field": 4,
        }[route.physical_regime]
        highlight.set_x(column_index + 0.015)
        state_text.set_text(
            f"x={value:.2f}   Xi={xi:.4f}   D={D_factor(value):.4f}\n"
            f"physical: {route.physical_regime}   |   formula: {route.formula_domain}\n"
            f"profile: {SSZ_PROFILE}"
        )
        return marker_curve, point_curve, highlight, state_text

    finish_layout(fig, top=0.82, bottom=0.13, hspace=0.48)
    save_animation(
        fig,
        update,
        np.unique(np.linspace(0, len(x) - 1, 120, dtype=int)),
        OUT,
        "regime_blend_map",
        fps=24,
        static_frame=representative,
    )
    print("wrote regime blend map visualizations")


if __name__ == "__main__":
    main()
