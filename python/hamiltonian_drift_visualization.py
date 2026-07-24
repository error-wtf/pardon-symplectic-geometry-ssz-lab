#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from hamiltonian_drift_report import euler, leapfrog_ssz, rk4, symplectic_euler_ssz
from pardon_math.plot_style import (
    BLUE,
    GREEN,
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
from pardon_math.ssz_bridge import hamiltonian_radial

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)

    q0, p0, dt, steps = 3.0, 0.05, 0.03, 1000
    methods = {
        "explicit Euler": (euler(q0, p0, dt, steps), RED),
        "RK4": (rk4(q0, p0, dt, steps), PURPLE),
        "symplectic Euler": (symplectic_euler_ssz(q0, p0, dt, steps), BLUE),
        "leapfrog": (leapfrog_ssz(q0, p0, dt, steps), GREEN),
    }
    errors = {}
    bands = {}
    for name, (trajectory, _) in methods.items():
        energy = np.asarray(hamiltonian_radial(trajectory[:, 0], trajectory[:, 1]), dtype=float)
        errors[name] = np.maximum(np.abs(energy - energy[0]), 1e-16)
        bands[name] = np.maximum.accumulate(energy) - np.minimum.accumulate(energy)

    q_all = np.concatenate([trajectory[:, 0] for trajectory, _ in methods.values()])
    p_all = np.concatenate([trajectory[:, 1] for trajectory, _ in methods.values()])
    q_pad = 0.04 * float(np.ptp(q_all))
    p_pad = 0.08 * float(np.ptp(p_all))

    fig = plt.figure()
    grid = fig.add_gridspec(2, 2, width_ratios=(1.35, 1.0), height_ratios=(1.0, 1.0))
    ax_phase = fig.add_subplot(grid[:, 0])
    ax_error = fig.add_subplot(grid[0, 1])
    ax_band = fig.add_subplot(grid[1, 1])
    add_header(
        fig,
        "Hamiltonian drift on the toy SSZ radial potential",
        "The paths nearly overlap because they solve the same outbound trajectory; energy error separates the methods.",
    )
    add_footer(
        fig,
        "Scope: numerical QA for one toy effective potential (q0=3, p0=0.05, dt=0.03); "
        "trajectory agreement and small drift do not physically validate SSZ.",
    )

    style_axes(ax_phase, "Radial phase paths, fully framed")
    ax_phase.set_xlim(float(q_all.min()) - q_pad, float(q_all.max()) + q_pad)
    ax_phase.set_ylim(float(p_all.min()) - p_pad, float(p_all.max()) + p_pad)
    ax_phase.set_xlabel("q = r/r_s")
    ax_phase.set_ylabel("radial momentum p_r")
    ax_phase.text(
        0.03,
        0.04,
        "Strong overlap is expected here.\nThe right panels reveal integration error.",
        transform=ax_phase.transAxes,
        va="bottom",
        fontsize=9,
        color=MUTED,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    style_axes(ax_error, "Absolute Hamiltonian error")
    ax_error.set_yscale("log")
    ax_error.set_xlim(0, steps)
    ax_error.set_ylim(5e-16, max(float(values.max()) for values in errors.values()) * 1.6)
    ax_error.set_xlabel("integration step")
    ax_error.set_ylabel("|H_n - H_0|")

    style_axes(ax_band, "Cumulative energy band")
    names = list(methods)
    colors = [methods[name][1] for name in names]
    positions = np.arange(len(names))
    bars = ax_band.bar(positions, np.full(len(names), 1e-16), color=colors, alpha=0.88)
    ax_band.set_yscale("log")
    ax_band.set_ylim(5e-16, max(float(values.max()) for values in bands.values()) * 2.0)
    ax_band.set_xticks(positions, ["Euler", "RK4", "sympl.\nEuler", "leapfrog"])
    ax_band.set_ylabel("max(H) - min(H)")

    phase_lines = {}
    phase_endpoints = {}
    error_lines = {}
    for name, (trajectory, color) in methods.items():
        phase_lines[name], = ax_phase.plot([], [], color=color, lw=2.4, label=name)
        phase_endpoints[name] = ax_phase.scatter([], [], s=45, color=color, edgecolor="white", linewidth=0.7, zorder=6)
        error_lines[name], = ax_error.plot([], [], color=color, lw=2.0, label=name)
    ax_phase.legend(loc="upper left")
    ax_error.legend(loc="lower right", fontsize=8)

    band_text = ax_band.text(
        0.98,
        0.96,
        "",
        transform=ax_band.transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#c9d4de"},
    )
    frame_values = np.unique(np.linspace(1, steps + 1, 150, dtype=int))

    def update(n: int):
        artists = []
        indices = np.arange(n)
        current_rows = []
        for index, name in enumerate(names):
            trajectory, _ = methods[name]
            phase_lines[name].set_data(trajectory[:n, 0], trajectory[:n, 1])
            phase_endpoints[name].set_offsets([trajectory[n - 1]])
            error_lines[name].set_data(indices, errors[name][:n])
            current_band = max(float(bands[name][n - 1]), 1e-16)
            bars[index].set_height(current_band)
            current_rows.append(f"{name}: {current_band:.2e}")
            artists.extend((phase_lines[name], phase_endpoints[name], error_lines[name], bars[index]))
        band_text.set_text("energy band through current step\n" + "\n".join(current_rows))
        return tuple(artists + [band_text])

    finish_layout(fig, top=0.82, bottom=0.14, wspace=0.30, hspace=0.43)
    save_animation(fig, update, frame_values, OUT, "hamiltonian_drift_report", fps=20)
    print("wrote Hamiltonian drift visualizations")


if __name__ == "__main__":
    main()
