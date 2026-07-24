#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import unittest
from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

LAYER_BY_CLASS = {
    "SymplecticTests": "Mathematical invariants",
    "CauchyRiemannTests": "Mathematical invariants",
    "LagrangianTests": "Mathematical invariants",
    "ModuliTests": "Mathematical invariants",
    "KnotTests": "Mathematical invariants",
    "HolonomyTests": "Mathematical invariants",
    "IntegratorTests": "Numerical regression",
    "SSZBridgeTests": "Numerical regression",
    "SSZStateTests": "Numerical regression",
    "HamiltonianDriftTests": "Numerical regression",
    "MethodAssignmentTests": "Fail-closed guardrails",
    "RegimeGuardrailTests": "Fail-closed guardrails",
    "RepoGraphTests": "Artifact and traceability",
    "SSZDocIndexTests": "Artifact and traceability",
    "VisualizationOutputTests": "Artifact and traceability",
    "VisualizationScopeTests": "Artifact and traceability",
    "DocumentationHardeningTests": "Artifact and traceability",
    "PhysicsRepoAuditTests": "Artifact and traceability",
    "TestValidationReportTests": "Artifact and traceability",
}

LAYER_ORDER = (
    "Mathematical invariants",
    "Numerical regression",
    "Fail-closed guardrails",
    "Artifact and traceability",
)

LAYER_NOTES = {
    "Mathematical invariants": "area, radius, CR residuals, intersections, moduli, knots, holonomy",
    "Numerical regression": "energy drift, SSZ bridge, state identities, Hamiltonian report",
    "Fail-closed guardrails": "observable routing, regime split, forbidden-formula rejection",
    "Artifact and traceability": "repo graph, source index, outputs, README, scope boundaries",
}

CRITICAL_CONTRACTS = OrderedDict(
    [
        ("Symplectic area/radius", {"SymplecticTests"}),
        ("CR residual separation", {"CauchyRiemannTests"}),
        ("Integrator drift hierarchy", {"IntegratorTests", "HamiltonianDriftTests"}),
        ("Xi/D state identities", {"SSZBridgeTests", "SSZStateTests"}),
        ("Null observables -> PPN", {"MethodAssignmentTests"}),
        ("Forbidden formulas reject", {"RegimeGuardrailTests"}),
        ("Static holonomy = 1", {"HolonomyTests"}),
        ("Output/source traceability", {"VisualizationOutputTests", "DocumentationHardeningTests"}),
    ]
)

COLORS = {
    "pending": "#d8dee6",
    "passed": "#18864b",
    "failed": "#c0392b",
    "skipped": "#d49a00",
}


def flatten_suite(suite: unittest.TestSuite) -> list[unittest.TestCase]:
    tests: list[unittest.TestCase] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            tests.extend(flatten_suite(item))
        else:
            tests.append(item)
    return tests


def discover() -> tuple[unittest.TestSuite, list[dict[str, str]]]:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    records = []
    for test in flatten_suite(suite):
        cls = test.__class__.__name__
        records.append(
            {
                "id": test.id(),
                "class": cls,
                "name": getattr(test, "_testMethodName", test.id()),
                "layer": LAYER_BY_CLASS.get(cls, "Artifact and traceability"),
                "status": "pending",
            }
        )
    return suite, records


def status_records(
    records: list[dict[str, str]], result: unittest.TestResult
) -> list[dict[str, str]]:
    failed = [test.id() for test, _ in result.failures + result.errors]
    skipped = [test.id() for test, _ in result.skipped]
    for record in records:
        test_id = record["id"]
        if any(item.startswith(test_id) for item in failed):
            record["status"] = "failed"
        elif any(item.startswith(test_id) for item in skipped):
            record["status"] = "skipped"
        else:
            record["status"] = "passed"
    return records


def layer_summary(records: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    summary = {}
    for layer in LAYER_ORDER:
        rows = [record for record in records if record["layer"] == layer]
        summary[layer] = {
            "total": len(rows),
            "passed": sum(record["status"] == "passed" for record in rows),
            "failed": sum(record["status"] == "failed" for record in rows),
            "skipped": sum(record["status"] == "skipped" for record in rows),
        }
    return summary


def write_report(records: list[dict[str, str]], result: unittest.TestResult) -> None:
    summary = layer_summary(records)
    payload = {
        "runner": "python unittest discovery",
        "command": "python -m unittest discover -s tests",
        "claim_boundary": (
            "Passing tests establish internal implementation consistency only; "
            "they do not prove Pardon's theorems or physically validate SSZ."
        ),
        "summary": {
            "total": len(records),
            "passed": sum(record["status"] == "passed" for record in records),
            "failed": len(result.failures) + len(result.errors),
            "skipped": len(result.skipped),
            "successful": result.wasSuccessful(),
        },
        "layers": summary,
        "tests": records,
    }
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    (DATA / "test_validation_report.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Test Validation Report",
        "",
        "Generated from the repository's `unittest` discovery run.",
        "",
        "> Passing tests establish internal implementation consistency only. They do not prove ",
        "> Pardon's theorems or physically validate SSZ.",
        "",
        "## Summary",
        "",
        "| Validation layer | Passed | Total | Meaning |",
        "|---|---:|---:|---|",
    ]
    for layer in LAYER_ORDER:
        item = summary[layer]
        lines.append(
            f"| {layer} | {item['passed']} | {item['total']} | {LAYER_NOTES[layer]} |"
        )
    lines.extend(
        [
            "",
            f"Overall: **{payload['summary']['passed']}/{payload['summary']['total']} passed**, "
            f"**{payload['summary']['failed']} failed**, **{payload['summary']['skipped']} skipped**.",
            "",
            "Machine-readable details: `data/test_validation_report.json`.",
            "",
        ]
    )
    (DOCS / "test-validation-report.md").write_text("\n".join(lines), encoding="utf-8")


def build_figure(records: list[dict[str, str]], reveal: int) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(13.6, 7.65))
    fig.patch.set_facecolor("#f5f7f9")
    ax.set_facecolor("#f5f7f9")
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 10)
    ax.axis("off")

    revealed = records[:reveal]
    visible = {record["id"]: record["status"] for record in revealed}
    passed = sum(status == "passed" for status in visible.values())
    failed = sum(status == "failed" for status in visible.values())
    total = len(records)

    ax.text(
        0.55,
        9.45,
        "Executable validation map",
        fontsize=22,
        weight="bold",
        color="#132238",
        va="center",
    )
    ax.text(
        0.58,
        8.93,
        f"Actual unittest results: {passed}/{total} passed"
        + (f", {failed} failed" if failed else ""),
        fontsize=11.5,
        color="#425466",
        va="center",
    )

    layer_y = {
        "Mathematical invariants": 7.75,
        "Numerical regression": 6.25,
        "Fail-closed guardrails": 4.75,
        "Artifact and traceability": 3.25,
    }
    for layer in LAYER_ORDER:
        rows = [record for record in records if record["layer"] == layer]
        y = layer_y[layer]
        card = plt.Rectangle(
            (0.45, y - 0.53),
            10.9,
            1.12,
            facecolor="white",
            edgecolor="#cfd8e3",
            linewidth=1.2,
        )
        ax.add_patch(card)
        ax.text(0.75, y + 0.16, layer, fontsize=12, weight="bold", color="#172b4d")
        ax.text(0.75, y - 0.19, LAYER_NOTES[layer], fontsize=7.8, color="#5f6f7f")

        cell_x = 5.35
        for index, record in enumerate(rows):
            status = visible.get(record["id"], "pending")
            square = plt.Rectangle(
                (cell_x + index * 0.43, y - 0.18),
                0.31,
                0.43,
                facecolor=COLORS[status],
                edgecolor="#ffffff",
                linewidth=0.7,
            )
            ax.add_patch(square)
        layer_passed = sum(
            visible.get(record["id"]) == "passed" for record in rows
        )
        ax.text(
            10.85,
            y + 0.02,
            f"{layer_passed}/{len(rows)}",
            fontsize=11,
            weight="bold",
            color="#18864b" if layer_passed == len(rows) else "#657786",
            ha="right",
            va="center",
        )

    ax.text(11.95, 8.42, "Critical contracts", fontsize=13, weight="bold", color="#172b4d")
    class_status = {}
    for record in records:
        if record["id"] not in visible:
            continue
        class_status.setdefault(record["class"], []).append(visible[record["id"]])
    for index, (label, classes) in enumerate(CRITICAL_CONTRACTS.items()):
        y = 7.85 - index * 0.66
        statuses = [status for cls in classes for status in class_status.get(cls, [])]
        complete = bool(statuses) and all(
            len(class_status.get(cls, []))
            == sum(record["class"] == cls for record in records)
            for cls in classes
        )
        status = (
            "failed"
            if any(item == "failed" for item in statuses)
            else "passed"
            if complete and all(item == "passed" for item in statuses)
            else "pending"
        )
        marker = plt.Rectangle(
            (11.95, y - 0.16),
            0.68,
            0.34,
            facecolor=COLORS[status],
            edgecolor="none",
        )
        ax.add_patch(marker)
        ax.text(
            12.29,
            y + 0.01,
            "PASS" if status == "passed" else "FAIL" if status == "failed" else "...",
            fontsize=7,
            weight="bold",
            color="white" if status != "pending" else "#5f6f7f",
            ha="center",
            va="center",
        )
        ax.text(12.82, y, label, fontsize=8.8, color="#33475b", va="center")

    chain_y = 1.55
    chain = ("Sources", "Core code", "Assertions", "Artifacts / README")
    for index, label in enumerate(chain):
        x = 0.75 + index * 3.2
        box = plt.Rectangle(
            (x, chain_y - 0.34),
            2.45,
            0.68,
            facecolor="#e8f1fb",
            edgecolor="#6b9ac4",
            linewidth=1.1,
        )
        ax.add_patch(box)
        ax.text(x + 1.225, chain_y, label, ha="center", va="center", fontsize=9.5, weight="bold")
        if index < len(chain) - 1:
            ax.annotate(
                "",
                xy=(x + 3.03, chain_y),
                xytext=(x + 2.52, chain_y),
                arrowprops={"arrowstyle": "->", "color": "#526d82", "lw": 1.6},
            )

    ax.text(
        0.6,
        0.48,
        "Claim boundary: green means internal consistency for the tested implementation. "
        "It is not a proof of Pardon results and not physical validation of SSZ.",
        fontsize=9.1,
        color="#6b2533",
        weight="bold",
    )
    fig.tight_layout()
    return fig


def create_placeholder(records: list[dict[str, str]]) -> None:
    OUT.mkdir(exist_ok=True)
    fig = build_figure(records, reveal=0)
    png = OUT / "test_validation_matrix.png"
    gif = OUT / "test_validation_matrix.gif"
    fig.savefig(png, dpi=160)
    plt.close(fig)
    with Image.open(png) as image:
        image.save(gif, format="GIF")


def render_animation(records: list[dict[str, str]]) -> None:
    frames = []
    frame_count = len(records) + 12
    for frame in range(frame_count):
        reveal = min(frame + 1, len(records))
        fig = build_figure(records, reveal)
        fig.canvas.draw()
        rgba = bytes(fig.canvas.buffer_rgba())
        width, height = fig.canvas.get_width_height()
        frames.append(Image.frombytes("RGBA", (width, height), rgba).convert("RGB"))
        plt.close(fig)
    frames[-1].save(
        OUT / "test_validation_matrix.gif",
        save_all=True,
        append_images=frames[1:],
        duration=110,
        loop=0,
        optimize=True,
    )
    final_fig = build_figure(records, len(records))
    final_fig.savefig(OUT / "test_validation_matrix.png", dpi=160)
    plt.close(final_fig)


def main() -> None:
    suite, records = discover()
    # Seed self-referential report/output checks before executing the full suite.
    # The final artifacts are overwritten immediately with the actual results.
    write_report(records, unittest.TestResult())
    create_placeholder(records)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    records = status_records(records, result)
    write_report(records, result)
    render_animation(records)
    print(stream.getvalue().strip())
    print("wrote executable test validation report and visualizations")
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
