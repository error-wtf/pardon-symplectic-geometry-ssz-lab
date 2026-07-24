#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from pardon_math.repo_graph import load_repo_graph

OUT = ROOT / "outputs"
GRAPH_PATH = ROOT / "data" / "repo_links.json"

POSITIONS = {
    "pardon": (0.0, 2.0),
    "symplectic": (-1.4, 1.0),
    "vfc": (1.4, 1.0),
    "ssz_docs": (0.0, 0.0),
    "ssz_lagrange": (-2.0, -1.0),
    "ssz_trajectories": (-0.7, -1.25),
    "galactic_year": (0.7, -1.25),
    "chord_partition": (2.0, -1.0),
    "claudes_cycles": (2.6, 0.2),
}

COLORS = {
    "research context": "#6a3d9a",
    "method": "#1f78b4",
    "single source": "#333333",
    "Hamilton/Lagrange anchor": "#33a02c",
    "geodesic integration": "#33a02c",
    "orbit visualization": "#ff7f00",
    "phi eigenmodes": "#e31a1c",
    "discrete cycle verification": "#b15928",
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    graph = load_repo_graph(GRAPH_PATH)
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = graph["edges"]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_title("Pardon geometry + SSZ repository interplay")
    ax.axis("off")
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-1.8, 2.4)

    for source, target, label in edges:
        x0, y0 = POSITIONS[source]
        x1, y1 = POSITIONS[target]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color="#777", lw=1.5, alpha=0.75))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ax.text(mx, my, label, fontsize=7, color="#555", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.7))

    scatters = {}
    for node_id, node in nodes.items():
        x, y = POSITIONS[node_id]
        color = COLORS.get(node["role"], "#999")
        scatters[node_id] = ax.scatter([x], [y], s=1200, color=color, alpha=0.88, edgecolor="black", linewidth=0.8, zorder=3)
        ax.text(x, y, node["label"], color="white", fontsize=8, ha="center", va="center", weight="bold", zorder=4)

    pulse = ax.scatter([], [], s=220, color="#ffd92f", edgecolor="black", zorder=5)
    edge_points = []
    for source, target, _ in edges:
        a = np.array(POSITIONS[source], dtype=float)
        b = np.array(POSITIONS[target], dtype=float)
        for t in np.linspace(0, 1, 18):
            edge_points.append(a * (1 - t) + b * t)
    edge_points = np.array(edge_points)

    def update(frame: int):
        point = edge_points[frame % len(edge_points)]
        pulse.set_offsets(point.reshape(1, 2))
        return (pulse,)

    fig.tight_layout()
    fig.savefig(OUT / "repo_interplay_map.png", dpi=170)
    FuncAnimation(fig, update, frames=len(edge_points), interval=70).save(OUT / "repo_interplay_map.gif", writer=PillowWriter(fps=18))
    plt.close(fig)
    print("wrote repo interplay map visualizations")


if __name__ == "__main__":
    main()
