#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from hamiltonian_drift_report import leapfrog_ssz
from pardon_math.plot_style import (
    AMBER,
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
from pardon_math.ssz_bridge import (
    BLEND_END,
    BLEND_START,
    D_factor,
    SSZ_PROFILE,
    effective_potential,
    hamiltonian_radial,
    xi_canonical,
    xi_strong,
    xi_weak,
)

OUT = ROOT / "outputs"


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)

    ell = 2.0
    path = leapfrog_ssz(3.0, 0.05, 0.03, 1000)
    x_max = float(path[:, 0].max()) * 1.04
    x = np.linspace(1.0, x_max, 700)
    q_mesh = np.linspace(float(path[:, 0].min()) * 0.96, x_max, 260)
    p_mesh = np.linspace(0.0, float(path[:, 1].max()) * 1.10, 220)
    Q, P = np.meshgrid(q_mesh, p_mesh)
    H = hamiltonian_radial(Q, P, ell=ell)

    fig, axes = plt.subplots(2, 2)
    ax_xi, ax_d, ax_v, ax_phase = axes.ravel()
    add_header(
        fig,
        "From SSZ scalar field to Hamiltonian motion",
        "A numbered dependency chain: Xi(x) -> D(x) -> V_eff(x) -> an integrated radial phase path.",
    )
    add_footer(
        fig,
        "Scope: exterior x >= 1 toy bridge using the declared SSZ profile and leapfrog integrator; "
        "not a theorem of John Pardon and not physical validation of SSZ.",
    )

    style_axes(ax_xi, "1  Operative field Xi(x)")
    ax_xi.plot(x, xi_weak(x), color=BLUE, ls="--", lw=1.5, label="g1 weak branch")
    ax_xi.plot(x, xi_strong(x), color=RED, ls=":", lw=1.8, label="g2 saturation")
    ax_xi.plot(x, xi_canonical(x), color=PURPLE, lw=2.8, label="operative Xi")
    ax_xi.axvspan(BLEND_START, BLEND_END, color=AMBER, alpha=0.16)
    ax_xi.set_xlim(x.min(), x.max())
    ax_xi.set_xlabel("x = r/r_s")
    ax_xi.set_ylabel("Xi")
    ax_xi.legend(loc="upper right", ncol=1)

    style_axes(ax_d, "2  Derived clock factor D = 1/(1 + Xi)")
    ax_d.plot(x, D_factor(x), color=BLUE, lw=2.8)
    ax_d.axvspan(BLEND_START, BLEND_END, color=AMBER, alpha=0.16)
    ax_d.set_xlim(x.min(), x.max())
    ax_d.set_xlabel("x = r/r_s")
    ax_d.set_ylabel("D")

    style_axes(ax_v, "3  Toy effective potential")
    for current_ell, color in ((1.0, GREEN), (ell, AMBER), (3.0, RED)):
        ax_v.plot(
            x,
            effective_potential(x, ell=current_ell),
            color=color,
            lw=2.5 if current_ell == ell else 1.5,
            alpha=1.0 if current_ell == ell else 0.75,
            label=f"ell = {current_ell:.0f}",
        )
    ax_v.set_xlim(x.min(), x.max())
    ax_v.set_xlabel("x = r/r_s")
    ax_v.set_ylabel("V_eff")
    ax_v.legend(loc="upper right", ncol=3)

    style_axes(ax_phase, "4  Numerically integrated radial path")
    contours = ax_phase.contour(Q, P, H, levels=10, colors=MUTED, alpha=0.36, linewidths=0.8)
    ax_phase.clabel(contours, inline=True, fontsize=7, fmt="%.2f")
    ax_phase.set_xlim(q_mesh.min(), q_mesh.max())
    ax_phase.set_ylim(p_mesh.min(), p_mesh.max())
    ax_phase.set_xlabel("q = r/r_s")
    ax_phase.set_ylabel("p_r")
    path_line, = ax_phase.plot([], [], color=PURPLE, lw=3.0, label="leapfrog trajectory")
    phase_dot = ax_phase.scatter([], [], s=65, color=RED, edgecolor="white", linewidth=0.8, zorder=6)
    ax_phase.legend(loc="lower right")

    xi_marker = ax_xi.axvline(path[0, 0], color=RED, lw=1.7)
    d_marker = ax_d.axvline(path[0, 0], color=RED, lw=1.7)
    v_marker = ax_v.axvline(path[0, 0], color=RED, lw=1.7)
    state_text = ax_phase.text(
        0.03,
        0.96,
        "",
        transform=ax_phase.transAxes,
        va="top",
        fontsize=8.8,
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#c9d4de"},
    )

    frames = np.unique(np.linspace(1, len(path), 120, dtype=int))

    def update(n: int):
        q, p = path[n - 1]
        path_line.set_data(path[:n, 0], path[:n, 1])
        phase_dot.set_offsets([[q, p]])
        for marker in (xi_marker, d_marker, v_marker):
            marker.set_xdata([q, q])
        state_text.set_text(
            f"profile: {SSZ_PROFILE}\nstep {n - 1:4d}\n"
            f"q = {q:6.3f},  p_r = {p:6.3f}\n"
            f"Xi = {xi_canonical(q):.4f},  D = {D_factor(q):.4f}\n"
            f"H = {hamiltonian_radial(q, p, ell=ell):.6f}"
        )
        return path_line, phase_dot, xi_marker, d_marker, v_marker, state_text

    finish_layout(fig, top=0.83, bottom=0.13, hspace=0.40)
    save_animation(fig, update, frames, OUT, "ssz_symplectic_bridge", fps=18)
    print("wrote SSZ symplectic bridge visualizations")


if __name__ == "__main__":
    main()
