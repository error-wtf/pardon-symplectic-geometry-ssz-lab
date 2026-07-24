#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.knot import cumulative_lengths, distortion_sample, trefoil
from pardon_math.plot_style import BLUE, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes

OUT = ROOT / "outputs"


def distortion_matrix(points: np.ndarray) -> np.ndarray:
    cumulative, total = cumulative_lengths(points)
    n = len(points)
    result = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i + 2, n):
            chord = float(np.linalg.norm(points[i] - points[j]))
            if chord < 1e-9:
                continue
            along = abs(cumulative[j] - cumulative[i])
            ratio = min(along, total - along) / chord
            result[i, j] = ratio
            result[j, i] = ratio
    return result


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    points = trefoil(180)
    ratio, index_a, index_b = distortion_sample(points)
    matrix = distortion_matrix(points)

    fig = plt.figure()
    add_header(
        fig,
        "Sampled distortion of a trefoil-like knot",
        "Intrinsic arc distance is compared with Euclidean chord distance for every sampled point pair.",
    )
    add_footer(fig, "Scope: finite polygonal sampling. The reported maximum is resolution-dependent and is not a knot-distortion theorem.")
    grid = fig.add_gridspec(1, 2, width_ratios=(1.05, 1.0))
    ax_knot = fig.add_subplot(grid[0, 0], projection="3d")
    ax_matrix = fig.add_subplot(grid[0, 1])

    ax_knot.set_title("Maximizing sampled chord", loc="left", pad=10, color="#14263d", weight="bold")
    ax_knot.set_axis_off()
    ax_knot.plot(points[:, 0], points[:, 1], points[:, 2], color=BLUE, lw=2.5)
    selected = points[[index_a, index_b]]
    chord, = ax_knot.plot(selected[:, 0], selected[:, 1], selected[:, 2], color=RED, lw=3.5)
    ax_knot.scatter(selected[:, 0], selected[:, 1], selected[:, 2], s=65, color=RED, edgecolor="white")
    ax_knot.text2D(
        0.03,
        0.92,
        f"max sampled ratio = {ratio:.3f}\npair = ({index_a}, {index_b})",
        transform=ax_knot.transAxes,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#c9d4de"},
    )
    extent = float(np.max(np.ptp(points, axis=0))) / 2
    midpoint = points.mean(axis=0)
    ax_knot.set_xlim(midpoint[0] - extent, midpoint[0] + extent)
    ax_knot.set_ylim(midpoint[1] - extent, midpoint[1] + extent)
    ax_knot.set_zlim(midpoint[2] - extent, midpoint[2] + extent)

    style_axes(ax_matrix, "Pairwise intrinsic/chord ratio")
    image = ax_matrix.imshow(matrix, origin="lower", cmap="viridis", vmin=1, vmax=float(np.nanpercentile(matrix, 99.5)))
    ax_matrix.scatter([index_b, index_a], [index_a, index_b], s=55, facecolors="none", edgecolors=RED, linewidths=1.8)
    ax_matrix.set_xlabel("sample index j")
    ax_matrix.set_ylabel("sample index i")
    colorbar = fig.colorbar(image, ax=ax_matrix, fraction=0.046, pad=0.04)
    colorbar.set_label("intrinsic distance / chord distance")

    def update(frame: int):
        ax_knot.view_init(elev=24, azim=30 + 360 * frame / 72)
        return (chord,)

    finish_layout(fig, left=0.045, right=0.965)
    save_animation(fig, update, range(72), OUT, "knot_distortion", fps=18, static_frame=0)
    print(f"sampled distortion ratio: {ratio:.6f}")
    print("wrote knot-distortion visualizations")


if __name__ == "__main__":
    main()
