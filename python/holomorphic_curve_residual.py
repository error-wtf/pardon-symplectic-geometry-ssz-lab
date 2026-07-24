#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.cr_residual import cauchy_riemann_residual
from pardon_math.plot_style import PURPLE, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    eps_values = np.linspace(0.0, 0.5, 90)
    means = np.array([cauchy_riemann_residual(float(epsilon))[2].mean() for epsilon in eps_values])
    analytic = 2.0 * eps_values
    S, T, residual = cauchy_riemann_residual(0.0)

    fig, (ax_field, ax_curve) = plt.subplots(1, 2)
    add_header(
        fig,
        "Cauchy-Riemann residual under anti-holomorphic perturbation",
        "The residual detects the transition from z^2 to z^2 + epsilon conjugate(z).",
    )
    add_footer(fig, "Scope: finite-difference diagnostic for one toy map; not pseudo-holomorphic curve theory.")

    style_axes(ax_field, "Uniform residual field for this perturbation")
    image = ax_field.imshow(
        residual,
        origin="lower",
        extent=[S.min(), S.max(), T.min(), T.max()],
        cmap="magma",
        vmin=0,
        vmax=max(1.5, float(means.max()) * 1.05),
        interpolation="nearest",
    )
    ax_field.set_xlabel("s")
    ax_field.set_ylabel("t")
    colorbar = fig.colorbar(image, ax=ax_field, fraction=0.046, pad=0.04)
    colorbar.set_label("CR residual")
    field_text = ax_field.text(
        0.03,
        0.96,
        "",
        transform=ax_field.transAxes,
        va="top",
        color="white",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#111827", "edgecolor": "none", "alpha": 0.82},
    )

    style_axes(ax_curve, "Computed residual against the analytic value")
    ax_curve.plot(eps_values, analytic, color="#5d6c7b", ls="--", lw=1.6, label="analytic 2 epsilon")
    ax_curve.plot(eps_values, means, color=PURPLE, label="finite-difference mean")
    ax_curve.set_xlabel("epsilon")
    ax_curve.set_ylabel("mean CR residual")
    ax_curve.set_xlim(0, 0.5)
    ax_curve.set_ylim(0, float(means.max()) * 1.08)
    curve_dot = ax_curve.scatter([], [], s=70, color=RED, zorder=5)
    ax_curve.legend(loc="upper left")
    ax_curve.text(
        0.97,
        0.08,
        f"max |numeric - analytic| = {np.max(np.abs(means - analytic)):.2e}",
        transform=ax_curve.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.8,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    def update(frame: int):
        epsilon = float(eps_values[frame])
        _, _, current = cauchy_riemann_residual(epsilon)
        image.set_data(current)
        curve_dot.set_offsets([[epsilon, means[frame]]])
        field_text.set_text(f"epsilon = {epsilon:.3f}\nmean = {means[frame]:.4f}")
        return image, curve_dot, field_text

    finish_layout(fig)
    save_animation(fig, update, range(len(eps_values)), OUT, "holomorphic_curve_residual", fps=16)
    print("wrote Cauchy-Riemann residual visualizations")


if __name__ == "__main__":
    main()
