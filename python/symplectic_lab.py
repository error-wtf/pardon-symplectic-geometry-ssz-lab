#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.plot_style import BLUE, GREEN, INK, MUTED, RED, add_footer, add_header, configure, finish_layout, save_animation, style_axes
from pardon_math.symplectic import polygon_area, rotate

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    theta = np.linspace(0, 2 * np.pi, 11, endpoint=False)
    blob = np.column_stack((0.78 + 0.34 * np.cos(theta), 0.22 * np.sin(theta)))
    center = blob.mean(axis=0)
    initial_area = polygon_area(blob)
    angles = np.linspace(0.0, 1.75 * np.pi, 96)
    moved = [rotate(blob, angle) for angle in angles]
    centers = np.array([points.mean(axis=0) for points in moved])
    area_error = np.maximum(
        np.array([abs(polygon_area(points) - initial_area) / initial_area for points in moved]),
        1e-17,
    )

    fig, (ax_phase, ax_error) = plt.subplots(1, 2)
    add_header(
        fig,
        "Symplectic area preservation under rotation",
        "A canonical linear map moves the region through phase space while its signed area remains invariant.",
    )
    add_footer(fig, "Scope: rotation is a controlled symplectic toy map, not a proof for arbitrary Hamiltonian flows.")

    style_axes(ax_phase, "Phase-space motion")
    ax_phase.set_aspect("equal")
    ax_phase.set_xlim(-1.35, 1.35)
    ax_phase.set_ylim(-1.35, 1.35)
    ax_phase.set_xlabel("q")
    ax_phase.set_ylabel("p")
    orbit = np.linspace(0, 2 * np.pi, 360)
    radius = float(np.linalg.norm(center))
    ax_phase.plot(radius * np.cos(orbit), radius * np.sin(orbit), color=MUTED, ls="--", lw=1.2, alpha=0.55)
    initial_closed = np.vstack([blob, blob[0]])
    ax_phase.plot(initial_closed[:, 0], initial_closed[:, 1], color=MUTED, lw=1.4, ls=":", label="initial region")
    region_line, = ax_phase.plot([], [], color=BLUE, lw=3.0, label="rotated region")
    center_path, = ax_phase.plot([], [], color=GREEN, lw=1.8, label="centroid path")
    center_dot = ax_phase.scatter([], [], s=70, color=RED, zorder=5)
    ax_phase.legend(loc="lower left")
    metric = ax_phase.text(
        0.03,
        0.97,
        "",
        transform=ax_phase.transAxes,
        va="top",
        color=INK,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    style_axes(ax_error, "Relative area error")
    ax_error.set_xlabel("rotation angle / pi")
    ax_error.set_ylabel("|A(theta) - A(0)| / A(0)")
    ax_error.set_yscale("log")
    ax_error.set_xlim(0, angles[-1] / np.pi)
    ax_error.set_ylim(5e-18, max(1e-14, float(area_error.max()) * 4))
    error_line, = ax_error.plot([], [], color=RED)
    error_dot = ax_error.scatter([], [], s=55, color=RED, zorder=5)
    ax_error.axhline(1e-14, color=MUTED, ls="--", lw=1.2, label="numerical tolerance scale")
    ax_error.legend(loc="upper left")

    def update(frame: int):
        points = moved[frame]
        closed = np.vstack([points, points[0]])
        region_line.set_data(closed[:, 0], closed[:, 1])
        center_path.set_data(centers[: frame + 1, 0], centers[: frame + 1, 1])
        center_dot.set_offsets(centers[[frame]])
        xs = angles[: frame + 1] / np.pi
        error_line.set_data(xs, area_error[: frame + 1])
        error_dot.set_offsets([[xs[-1], area_error[frame]]])
        metric.set_text(
            f"angle = {angles[frame] / np.pi:.2f} pi\n"
            f"A(0) = {initial_area:.8f}\n"
            f"A(theta) = {polygon_area(points):.8f}"
        )
        return region_line, center_path, center_dot, error_line, error_dot, metric

    finish_layout(fig)
    save_animation(fig, update, range(len(angles)), OUT, "symplectic_area_preservation", fps=16)
    print("wrote symplectic area-preservation visualizations")


if __name__ == "__main__":
    main()
