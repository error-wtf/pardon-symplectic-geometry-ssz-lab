#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
INDEX = ROOT / "data" / "ssz_doc_index.json"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    sections = data["section_counts"]
    keyword_totals = data["keyword_totals"]
    top_keywords = sorted(keyword_totals.items(), key=lambda kv: kv[1], reverse=True)[:14]
    top_files = []
    for f in data["files"]:
        score = sum(f["keyword_hits"].get(k, 0) for k in ["Hamilton", "Lagrange", "geodesic", "Geodesic", "trajectory", "orbit", "phase", "PPN", "Xi", "Ξ", "D(r)"])
        if score:
            top_files.append((score, f["path"]))
    top_files = sorted(top_files, reverse=True)[:12]

    fig, axs = plt.subplots(2, 2, figsize=(13, 9))
    ax0, ax1, ax2, ax3 = axs.ravel()

    sec_names = list(sections.keys())
    sec_vals = [sections[k] for k in sec_names]
    ax0.barh(sec_names, sec_vals, color="#1f78b4")
    ax0.set_title("SSZ documentation files by section")
    ax0.set_xlabel("Markdown files")

    kw_names = [k for k, _ in top_keywords][::-1]
    kw_vals = [v for _, v in top_keywords][::-1]
    ax1.barh(kw_names, kw_vals, color="#6a3d9a")
    ax1.set_title("Top bridge-relevant keyword totals")
    ax1.set_xlabel("hits")

    file_labels = [p.split("/")[-1][:38] for _, p in top_files][::-1]
    file_scores = [s for s, _ in top_files][::-1]
    ax2.barh(file_labels, file_scores, color="#33a02c")
    ax2.set_title("Highest Pardon/SSZ bridge-score files")
    ax2.set_xlabel("score")

    ax3.axis("off")
    ax3.text(
        0.02,
        0.95,
        "Deep-read result:\n"
        f"{data['file_count']} Markdown files scanned.\n"
        "The bridge concentrates around Xi/D/phi,\n"
        "regime guardrails, Lagrange/geodesics,\n"
        "PPN method assignment and validation docs.\n\n"
        "Consequence:\n"
        "SSZ should add symplectic phase-space\n"
        "drift tests and structure-preserving\n"
        "geodesic/ray integrator comparisons.",
        va="top",
        fontsize=12,
    )

    fig.tight_layout()
    fig.savefig(OUT / "ssz_doc_audit.png", dpi=170)

    pulse = ax3.text(0.02, 0.18, "", fontsize=12, color="#d62728")
    messages = [
        "1. Read whole SSZ doc tree",
        "2. Locate Xi/D/phi guardrails",
        "3. Locate Hamilton/geodesic bridge",
        "4. Convert into SSZ phase-space tests",
    ]

    def update(frame: int):
        pulse.set_text(messages[frame % len(messages)])
        return (pulse,)

    FuncAnimation(fig, update, frames=80, interval=120).save(OUT / "ssz_doc_audit.gif", writer=PillowWriter(fps=10))
    plt.close(fig)
    print("wrote SSZ documentation audit visualizations")


if __name__ == "__main__":
    main()
