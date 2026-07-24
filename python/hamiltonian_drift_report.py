from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from pardon_math.ssz_bridge import effective_potential, hamiltonian_radial

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"


def force(q: float, ell: float = 2.0) -> float:
    h = 1e-4 * max(1.0, abs(q))
    return -float((effective_potential(q + h, ell=ell) - effective_potential(q - h, ell=ell)) / (2.0 * h))


def euler(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    q, p = float(q0), float(p0)
    out = np.empty((steps + 1, 2), dtype=float)
    out[0] = (q, p)
    for i in range(1, steps + 1):
        q_new = q + dt * p
        p_new = p + dt * force(q)
        q, p = q_new, p_new
        out[i] = (q, p)
    return out


def symplectic_euler_ssz(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    q, p = float(q0), float(p0)
    out = np.empty((steps + 1, 2), dtype=float)
    out[0] = (q, p)
    for i in range(1, steps + 1):
        p = p + dt * force(q)
        q = q + dt * p
        out[i] = (q, p)
    return out


def leapfrog_ssz(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    q, p = float(q0), float(p0)
    out = np.empty((steps + 1, 2), dtype=float)
    out[0] = (q, p)
    for i in range(1, steps + 1):
        p_half = p + 0.5 * dt * force(q)
        q = q + dt * p_half
        p = p_half + 0.5 * dt * force(q)
        out[i] = (q, p)
    return out


def rk4(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    def rhs(y: np.ndarray) -> np.ndarray:
        return np.array([y[1], force(float(y[0]))], dtype=float)

    y = np.array([q0, p0], dtype=float)
    out = np.empty((steps + 1, 2), dtype=float)
    out[0] = y
    for i in range(1, steps + 1):
        k1 = rhs(y)
        k2 = rhs(y + 0.5 * dt * k1)
        k3 = rhs(y + 0.5 * dt * k2)
        k4 = rhs(y + dt * k3)
        y = y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        out[i] = y
    return out


def drift_summary(traj: np.ndarray) -> dict[str, float]:
    h = hamiltonian_radial(traj[:, 0], traj[:, 1])
    h0 = float(h[0])
    return {
        "initial_H": h0,
        "final_H": float(h[-1]),
        "absolute_drift": abs(float(h[-1]) - h0),
        "max_band": float(np.max(h) - np.min(h)),
        "min_q": float(np.min(traj[:, 0])),
        "max_q": float(np.max(traj[:, 0])),
    }


def build_report(q0: float = 3.0, p0: float = 0.05, dt: float = 0.03, steps: int = 1000) -> list[dict[str, float | str]]:
    methods = {
        "explicit_euler": euler(q0, p0, dt, steps),
        "rk4": rk4(q0, p0, dt, steps),
        "symplectic_euler": symplectic_euler_ssz(q0, p0, dt, steps),
        "leapfrog": leapfrog_ssz(q0, p0, dt, steps),
    }
    rows = []
    for name, traj in methods.items():
        row: dict[str, float | str] = {"method": name, "q0": q0, "p0": p0, "dt": dt, "steps": steps}
        row.update(drift_summary(traj))
        rows.append(row)
    return rows


def write_outputs() -> None:
    rows = build_report()
    fields = ["method", "q0", "p0", "dt", "steps", "initial_H", "final_H", "absolute_drift", "max_band", "min_q", "max_q"]
    with (DATA / "hamiltonian_drift_report.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Hamiltonian Drift Report",
        "",
        "Toy SSZ effective-potential drift check. This is a numerical QA artifact, not a physical validation.",
        "",
        "| Method | Absolute drift | Energy band | q range |",
        "|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['method']}` | {row['absolute_drift']:.6e} | {row['max_band']:.6e} | {row['min_q']:.3f} .. {row['max_q']:.3f} |"
        )
    lines.append("")
    (DOCS / "hamiltonian-drift-report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write_outputs()
