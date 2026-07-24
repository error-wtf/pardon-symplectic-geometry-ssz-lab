from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from pardon_math.method_assignment import ROUTES

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def build_rows() -> list[dict[str, str]]:
    return [asdict(route) for key, route in sorted(ROUTES.items())]


def write_outputs() -> None:
    rows = build_rows()
    (DATA / "observable_routing_matrix.json").write_text(
        json.dumps({"source": "ssz method assignment guardrail", "count": len(rows), "routes": rows}, indent=2),
        encoding="utf-8",
    )
    lines = [
        "# Observable Routing Matrix",
        "",
        "This file is generated from `pardon_math.method_assignment.ROUTES`.",
        "It documents the fail-closed SSZ method assignment used by the Pardon/SSZ bridge.",
        "",
        "| Observable | Method | Domain | Guardrail | Claim boundary |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['observable']}` | {row['method']} | {row['domain']} | {row['guardrail']} | {row['claim_boundary']} |"
        )
    lines.append("")
    (DOCS / "observable-routing-matrix.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write_outputs()
