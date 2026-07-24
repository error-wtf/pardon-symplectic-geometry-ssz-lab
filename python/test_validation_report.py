#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
    "EvidenceLedgerTests": "Artifact and traceability",
    "VisualizationOutputTests": "Artifact and traceability",
    "VisualizationQualityTests": "Artifact and traceability",
    "VisualizationScopeTests": "Artifact and traceability",
    "DocumentationHardeningTests": "Artifact and traceability",
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
    "Numerical regression": "energy drift, SSZ C1/C2 blend, state identities, Hamiltonian report",
    "Fail-closed guardrails": "observable routing, regime split, forbidden-formula rejection",
    "Artifact and traceability": "output dimensions and motion, README scope, claim boundaries, traceability",
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


def assign_status(records: list[dict[str, str]], result: unittest.TestResult) -> None:
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


def write_report(records: list[dict[str, str]], result: unittest.TestResult) -> None:
    layers = {}
    for layer in LAYER_ORDER:
        rows = [record for record in records if record["layer"] == layer]
        layers[layer] = {
            "total": len(rows),
            "passed": sum(record["status"] == "passed" for record in rows),
            "failed": sum(record["status"] == "failed" for record in rows),
            "skipped": sum(record["status"] == "skipped" for record in rows),
        }
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
        "layers": layers,
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
        "> Passing tests establish internal implementation consistency only. They do not prove",
        "> Pardon's theorems or physically validate SSZ.",
        "",
        "## Summary",
        "",
        "| Validation layer | Passed | Total | Meaning |",
        "|---|---:|---:|---|",
    ]
    for layer in LAYER_ORDER:
        item = layers[layer]
        lines.append(f"| {layer} | {item['passed']} | {item['total']} | {LAYER_NOTES[layer]} |")
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


def main() -> None:
    suite, records = discover()
    write_report(records, unittest.TestResult())
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    assign_status(records, result)
    write_report(records, result)
    print(stream.getvalue().strip())
    print("wrote executable test validation reports")
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
