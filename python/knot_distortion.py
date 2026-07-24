#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.knot import distortion_sample, trefoil

OUT = ROOT / "outputs"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    pts = trefoil()
    ratio, i, j = distortion_sample(pts)
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("Sampled knot distortion on a trefoil-like polygon")
    ax.set_axis_off()
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="#1f77b4", lw=2)
    chord, = ax.plot([], [], [], color="#d62728", lw=3)
    chosen = ax.scatter([], [], [], s=60, color="#d62728")
    ax.text2D(0.03, 0.94, f"max sampled ratio approx {ratio:.3f}", transform=ax.transAxes)
    max_range = float(np.max(np.ptp(pts, axis=0))) / 2
    mid = pts.mean(axis=0)
    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)

    def update(frame: int):
        ax.view_init(elev=24, azim=360 * frame / 120)
        pair = pts[[i, j]]
        chord.set_data(pair[:, 0], pair[:, 1])
        chord.set_3d_properties(pair[:, 2])
        chosen._offsets3d = (pair[:, 0], pair[:, 1], pair[:, 2])
        return chord, chosen

    update(0)
    fig.tight_layout()
    fig.savefig(OUT / "knot_distortion.png", dpi=160)
    FuncAnimation(fig, update, frames=120, interval=50).save(OUT / "knot_distortion.gif", writer=PillowWriter(fps=20))
    plt.close(fig)
    print(f"sampled distortion ratio: {ratio:.6f}")
    print("wrote knot distortion visualizations")


if __name__ == "__main__":
    main()
