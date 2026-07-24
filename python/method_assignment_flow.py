#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.method_assignment import route_observable
from pardon_math.plot_style import (
    AMBER,
    BLUE,
    GREEN,
    INK,
    MUTED,
    PANEL,
    PURPLE,
    RED,
    add_footer,
    add_header,
    configure,
    finish_layout,
    save_animation,
)

OUT = ROOT / "outputs"


ROUTE_SPECS = (
    ("Clock / redshift", "redshift", GREEN),
    ("Light path", "lensing", BLUE),
    ("Orbit / precession", "orbit", AMBER),
    ("Geodesic integration", "geodesic", PURPLE),
)


def main() -> None:
    configure()
    OUT.mkdir(exist_ok=True)
    rows = [
        (
            label,
            route_observable(observable).method,
            route_observable(observable).guardrail,
            color,
        )
        for label, observable, color in ROUTE_SPECS
    ]
    rows.append(
        (
            "Unknown or mixed",
            "STOP and classify",
            "Fail closed; never use one formula for every observable",
            RED,
        )
    )

    fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_header(
        fig,
        "Observable first, method second",
        "The SSZ routing guardrail prevents a clock formula from being reused for light paths or orbital dynamics.",
    )
    add_footer(
        fig,
        "Scope: method-selection guardrail implemented in pardon_math.method_assignment; "
        "the table routes calculations but does not validate an observable or the SSZ model.",
    )

    columns = ((0.055, 0.285, "Observable class"), (0.305, 0.595, "Required method"), (0.615, 0.945, "Critical guardrail"))
    for x0, x1, label in columns:
        ax.text((x0 + x1) / 2, 0.91, label, ha="center", va="center", fontsize=11, weight="bold", color=INK)

    y_positions = [0.79, 0.65, 0.51, 0.37, 0.23]
    row_patches: list[list[FancyBboxPatch]] = []
    row_texts = []
    for y, (observable, method, guardrail, color) in zip(y_positions, rows):
        patches = []
        texts = (
            observable,
            textwrap.fill(method, width=34),
            textwrap.fill(guardrail, width=46),
        )
        for (x0, x1, _), label in zip(columns, texts):
            patch = FancyBboxPatch(
                (x0, y - 0.052),
                x1 - x0,
                0.104,
                boxstyle="round,pad=0.008,rounding_size=0.01",
                facecolor=PANEL,
                edgecolor="#c5d0da",
                linewidth=1.2,
            )
            ax.add_patch(patch)
            patches.append(patch)
            row_texts.append(
                ax.text(
                    (x0 + x1) / 2,
                    y,
                    label,
                    ha="center",
                    va="center",
                    fontsize=9.2 if x0 < 0.6 else 8.7,
                    color=INK,
                    wrap=True,
                )
            )
        ax.add_patch(
            FancyBboxPatch(
                (0.037, y - 0.052),
                0.010,
                0.104,
                boxstyle="round,pad=0.002,rounding_size=0.004",
                facecolor=color,
                edgecolor=color,
            )
        )
        row_patches.append(patches)

    ax.text(
        0.50,
        0.105,
        "Selection rule: classify the measured quantity before writing an equation.",
        ha="center",
        va="center",
        fontsize=11,
        weight="bold",
        color=MUTED,
    )

    def update(active: int):
        artists = []
        for index, patches in enumerate(row_patches):
            color = rows[index][3]
            for patch in patches:
                patch.set_facecolor("#edf4f9" if index == active else PANEL)
                patch.set_edgecolor(color if index == active else "#c5d0da")
                patch.set_linewidth(2.4 if index == active else 1.2)
                artists.append(patch)
        return tuple(artists + row_texts)

    frames = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1, 0, 0]
    finish_layout(fig, left=0.03, right=0.985, top=0.84, bottom=0.12)
    save_animation(fig, update, frames, OUT, "method_assignment_flow", fps=4, static_frame=1)
    print("wrote method assignment flow visualizations")


if __name__ == "__main__":
    main()
