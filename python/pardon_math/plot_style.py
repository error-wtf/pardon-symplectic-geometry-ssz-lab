from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

FIGSIZE = (12.8, 7.2)
PNG_DPI = 150

BG = "#f4f7fa"
PANEL = "#ffffff"
INK = "#14263d"
MUTED = "#5d6c7b"
GRID = "#d8e0e8"
BLUE = "#2f6b9a"
TEAL = "#1b8f8a"
GREEN = "#258750"
AMBER = "#d48a1f"
RED = "#c4473a"
PURPLE = "#7656a8"
LIGHT_BLUE = "#dceaf5"


def configure() -> None:
    plt.rcParams.update(
        {
            "figure.figsize": FIGSIZE,
            "figure.dpi": 100,
            "figure.facecolor": BG,
            "axes.facecolor": PANEL,
            "axes.edgecolor": "#bdc9d5",
            "axes.labelcolor": INK,
            "axes.titlecolor": INK,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.size": 10,
            "font.family": "DejaVu Sans",
            "legend.frameon": False,
            "legend.fontsize": 9,
            "grid.color": GRID,
            "grid.alpha": 0.7,
            "grid.linewidth": 0.8,
            "lines.linewidth": 2.2,
            "savefig.facecolor": BG,
        }
    )


def style_axes(ax: plt.Axes, title: str | None = None) -> None:
    if title:
        ax.set_title(title, loc="left", pad=10)
    ax.grid(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def add_header(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.suptitle(title, x=0.055, y=0.965, ha="left", fontsize=20, weight="bold", color=INK)
    fig.text(0.056, 0.915, subtitle, ha="left", va="top", fontsize=10.5, color=MUTED)


def add_footer(fig: plt.Figure, text: str) -> None:
    fig.text(0.055, 0.025, text, ha="left", va="bottom", fontsize=8.5, color=MUTED)


def finish_layout(
    fig: plt.Figure,
    *,
    left: float = 0.065,
    right: float = 0.975,
    top: float = 0.84,
    bottom: float = 0.12,
    wspace: float = 0.28,
    hspace: float = 0.35,
) -> None:
    fig.subplots_adjust(left=left, right=right, top=top, bottom=bottom, wspace=wspace, hspace=hspace)


def save_animation(
    fig: plt.Figure,
    update: Callable[[int], object],
    frames: Iterable[int],
    out_dir: Path,
    stem: str,
    *,
    fps: int = 16,
    static_frame: int | None = None,
) -> None:
    frame_values = list(frames)
    if not frame_values:
        raise ValueError("animation requires at least one frame")
    update(frame_values[-1] if static_frame is None else static_frame)
    fig.savefig(out_dir / f"{stem}.png", dpi=PNG_DPI)
    animation = FuncAnimation(
        fig,
        update,
        frames=frame_values,
        interval=1000 / fps,
        blit=False,
        cache_frame_data=False,
    )
    animation.save(out_dir / f"{stem}.gif", writer=PillowWriter(fps=fps))
    plt.close(fig)
