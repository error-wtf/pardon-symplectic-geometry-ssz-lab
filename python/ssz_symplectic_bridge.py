#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.ssz_bridge import D_factor, XI_MAX, effective_potential, hamiltonian_radial, xi_canonical

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    x = np.linspace(1.0, 12.0, 500)
    p = np.linspace(-1.2, 1.2, 260)
    X, P = np.meshgrid(np.linspace(1.0, 8.0, 260), p)
    H = hamiltonian_radial(X, P, ell=2.1)

    fig, axs = plt.subplots(2, 2, figsize=(11, 8))
    ax_xi, ax_d, ax_v, ax_phase = axs.ravel()
    ax_xi.plot(x, xi_canonical(x), color="#6a3d9a", lw=2)
    ax_xi.axhline(XI_MAX, color="#999", ls="--", lw=1, label="Xi_max")
    ax_xi.axvspan(1.8, 2.2, color="#ffd92f", alpha=0.25, label="blend guardrail")
    ax_xi.set_title("SSZ segment density Xi(r/r_s)")
    ax_xi.set_xlabel("x = r/r_s")
    ax_xi.set_ylabel("Xi")
    ax_xi.legend(fontsize=8)
    ax_xi.grid(True, alpha=0.25)

    ax_d.plot(x, D_factor(x), color="#1f78b4", lw=2)
    ax_d.axvline(1.0, color="#999", ls="--", lw=1)
    ax_d.set_title("finite SSZ time dilation D=1/(1+Xi)")
    ax_d.set_xlabel("x = r/r_s")
    ax_d.set_ylabel("D")
    ax_d.grid(True, alpha=0.25)

    for ell, color in [(0.8, "#33a02c"), (1.5, "#ff7f00"), (2.2, "#e31a1c")]:
        ax_v.plot(x, effective_potential(x, ell=ell), color=color, lw=2, label=f"ell={ell}")
    ax_v.set_title("toy SSZ effective potential")
    ax_v.set_xlabel("x = r/r_s")
    ax_v.set_ylabel("V_eff")
    ax_v.set_ylim(0, 4)
    ax_v.grid(True, alpha=0.25)
    ax_v.legend(fontsize=8)

    contours = ax_phase.contour(X, P, H, levels=18, cmap="viridis", alpha=0.8)
    ax_phase.clabel(contours, inline=True, fontsize=6, fmt="%.1f")
    marker = ax_phase.scatter([], [], s=80, color="#d62728")
    ax_phase.set_title("SSZ radial toy Hamiltonian phase space")
    ax_phase.set_xlabel("x = r/r_s")
    ax_phase.set_ylabel("p_r")
    ax_phase.grid(True, alpha=0.25)

    path_x = np.linspace(1.05, 7.5, 160)
    path_p = 0.55 * np.sin(np.linspace(0, 4 * np.pi, 160))

    def update(frame: int):
        idx = frame % len(path_x)
        marker.set_offsets(np.array([[path_x[idx], path_p[idx]]]))
        fig.suptitle("Pardon-style symplectic validation applied to SSZ toy dynamics", fontsize=13)
        return (marker,)

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "ssz_symplectic_bridge.png", dpi=170)
    FuncAnimation(fig, update, frames=len(path_x), interval=55).save(OUT / "ssz_symplectic_bridge.gif", writer=PillowWriter(fps=20))
    plt.close(fig)
    print("wrote SSZ symplectic bridge visualizations")


if __name__ == "__main__":
    main()
