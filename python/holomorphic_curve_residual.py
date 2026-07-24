#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.cr_residual import cauchy_riemann_residual

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_title("Cauchy-Riemann residual: z^2 + epsilon * conjugate(z)")
    ax.set_xlabel("s")
    ax.set_ylabel("t")
    S, T, R = cauchy_riemann_residual(0.0)
    image = ax.imshow(R, origin="lower", extent=[S.min(), S.max(), T.min(), T.max()], cmap="magma", vmin=0, vmax=2.2)
    fig.colorbar(image, ax=ax, label="CR residual")
    text = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top", color="white")

    def update(frame: int):
        epsilon = 0.5 * (1 - np.cos(2 * np.pi * frame / 80))
        _, _, residual = cauchy_riemann_residual(epsilon)
        image.set_array(residual)
        text.set_text(f"epsilon = {epsilon:.3f}\nmean residual = {residual.mean():.3f}")
        return image, text

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "holomorphic_curve_residual.png", dpi=160)
    FuncAnimation(fig, update, frames=80, interval=60).save(OUT / "holomorphic_curve_residual.gif", writer=PillowWriter(fps=18))
    plt.close(fig)
    print("wrote holomorphic residual visualizations")


if __name__ == "__main__":
    main()
