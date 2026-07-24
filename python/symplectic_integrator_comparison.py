#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.integrators import explicit_euler, harmonic_energy, leapfrog, symplectic_euler

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    dt = 0.08
    steps = 420
    euler = explicit_euler(1.0, 0.0, dt, steps)
    symp = symplectic_euler(1.0, 0.0, dt, steps)
    leap = leapfrog(1.0, 0.0, dt, steps)
    h0 = 0.5

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11, 5))
    for ax in (ax0,):
        ax.set_aspect("equal")
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-3.0, 3.0)
        ax.set_xlabel("q")
        ax.set_ylabel("p")
        ax.grid(True, alpha=0.25)
    ax0.set_title("Integrator trajectories")
    ax1.set_title("Energy error |H-H0|")
    ax1.set_xlabel("step")
    ax1.set_ylabel("absolute energy error")
    ax1.set_yscale("log")
    ax1.grid(True, which="both", alpha=0.25)

    le, = ax0.plot([], [], color="#d62728", label="explicit Euler")
    ls, = ax0.plot([], [], color="#1f77b4", label="symplectic Euler")
    ll, = ax0.plot([], [], color="#2ca02c", label="leapfrog")
    ax0.legend(loc="upper right")
    ee, = ax1.plot([], [], color="#d62728")
    es, = ax1.plot([], [], color="#1f77b4")
    el, = ax1.plot([], [], color="#2ca02c")

    def errors(traj):
        return np.abs(harmonic_energy(traj[:, 0], traj[:, 1]) - h0) + 1e-14

    err_e = errors(euler)
    err_s = errors(symp)
    err_l = errors(leap)
    ax1.set_xlim(0, steps)
    ax1.set_ylim(1e-14, max(err_e) * 1.2)

    def update(frame: int):
        n = frame + 1
        x = np.arange(n)
        le.set_data(euler[:n, 0], euler[:n, 1])
        ls.set_data(symp[:n, 0], symp[:n, 1])
        ll.set_data(leap[:n, 0], leap[:n, 1])
        ee.set_data(x, err_e[:n])
        es.set_data(x, err_s[:n])
        el.set_data(x, err_l[:n])
        return le, ls, ll, ee, es, el

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "symplectic_vs_euler.png", dpi=160)
    FuncAnimation(fig, update, frames=steps + 1, interval=20).save(OUT / "symplectic_vs_euler.gif", writer=PillowWriter(fps=30))
    plt.close(fig)
    print("wrote integrator comparison visualizations")


if __name__ == "__main__":
    main()
