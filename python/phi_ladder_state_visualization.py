#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.plot_style import (
    AMBER,
    BLUE,
    GREEN,
    PURPLE,
    RED,
    add_footer,
    add_header,
    configure,
    finish_layout,
    save_animation,
    style_axes,
)
from pardon_math.ssz_bridge import PHI
from pardon_math.ssz_state import phi_ladder, regime_label, state_vector

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)

    ks = np.arange(0, 6)
    xs = phi_ladder(0, 5)
    states = state_vector(xs)
    labels = [regime_label(float(x)) for x in xs]
    regime_colors = {
        "g2/very_close": RED,
        "blend": AMBER,
        "photon_sphere": PURPLE,
        "strong_context/g1_formula": PURPLE,
        "weak": BLUE,
    }
    colors = [regime_colors[label] for label in labels]
    representative = int(np.argmin(np.abs(xs - 1.0)))

    fig, axes = plt.subplots(2, 2)
    ax_ladder, ax_xid, ax_count, ax_level = axes.ravel()
    add_header(
        fig,
        "Phi ladder and the derived SSZ state",
        "Exterior ladder k=0..5 under the lab's declared local-saturation SSZ source profile.",
    )
    add_footer(
        fig,
        "Scope: exact transformations under SSZ profile local_saturation_c2_blend_v1; alternative documented "
        "inner profiles give different k=1 values. This is not an empirical result or Pardon's work.",
    )

    style_axes(ax_ladder, "1  Geometric ladder x_k = phi^k")
    ax_ladder.plot(ks, xs, color=BLUE, lw=2.2)
    ax_ladder.scatter(ks, xs, c=colors, s=55, zorder=4)
    ax_ladder.set_yscale("log")
    ax_ladder.set_xlabel("integer level k")
    ax_ladder.set_ylabel("x_k = r/r_s")
    ax_ladder.set_xticks(ks)

    style_axes(ax_xid, "2  Operative field and reciprocal clock factor")
    ax_xid.plot(xs, states["Xi"], marker="o", color=PURPLE, label="Xi")
    ax_xid.plot(xs, states["D"], marker="s", color=GREEN, label="D = 1/(1+Xi)")
    ax_xid.set_xscale("log")
    ax_xid.set_xlabel("x_k")
    ax_xid.set_ylabel("dimensionless value")
    ax_xid.legend(loc="center right")

    style_axes(ax_count, "3  Effective segment count N_eff = 4(1 + Xi)")
    ax_count.plot(xs, states["N_eff"], marker="o", color=AMBER)
    ax_count.set_xscale("log")
    ax_count.set_xlabel("x_k")
    ax_count.set_ylabel("N_eff")

    style_axes(ax_level, "4  Local level nu = log(1 + Xi) / log(phi)")
    ax_level.plot(xs, states["nu"], marker="o", color=RED)
    ax_level.set_xscale("log")
    ax_level.set_xlabel("x_k")
    ax_level.set_ylabel("nu")

    ladder_dot = ax_ladder.scatter([], [], s=130, facecolor="none", edgecolor="#111827", linewidth=2.0, zorder=6)
    xid_line = ax_xid.axvline(xs[0], color="#111827", lw=1.8)
    count_line = ax_count.axvline(xs[0], color="#111827", lw=1.8)
    level_line = ax_level.axvline(xs[0], color="#111827", lw=1.8)
    info = ax_ladder.text(
        0.03,
        0.96,
        "",
        transform=ax_ladder.transAxes,
        va="top",
        fontsize=8.8,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    def update(index: int):
        ladder_dot.set_offsets([[ks[index], xs[index]]])
        for marker in (xid_line, count_line, level_line):
            marker.set_xdata([xs[index], xs[index]])
        info.set_text(
            f"k = {ks[index]:+d}\n"
            f"x_k = {xs[index]:.5f}\n"
            f"regime = {labels[index]}\n"
            f"x_(k+1)/x_k = phi = {PHI:.6f}"
        )
        return ladder_dot, xid_line, count_line, level_line, info

    frames = list(range(len(xs))) * 5
    finish_layout(fig, top=0.83, bottom=0.13, hspace=0.42)
    save_animation(
        fig,
        update,
        frames,
        OUT,
        "phi_ladder_state",
        fps=5,
        static_frame=representative,
    )
    print("wrote phi ladder state visualizations")


if __name__ == "__main__":
    main()
