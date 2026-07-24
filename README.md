# Pardon Symplectic Geometry SSZ Lab

**Educational geometry lab for John Pardon's 2026 Fields Medal context**

[![License](https://img.shields.io/badge/license-ACSL%201.4-red)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](requirements.txt)
[![Tests](https://img.shields.io/badge/tests-unittest-brightgreen)](tests/)
[![Status](https://img.shields.io/badge/status-educational%20reconstruction-orange)](docs/research-brief.md)

---

## Purpose

This repository is an educational reconstruction and visualization lab for the background mathematics around **John Pardon's 2026 Fields Medal**.

It does **not** claim to reproduce Pardon's proofs, virtual fundamental cycle machinery, Fukaya-category constructions, or curve-counting theorems. It does something narrower and verifiable:

- credit John Pardon and collaborators clearly;
- map the mathematical topics behind the Fields Medal citation;
- provide runnable Python toy models;
- generate PNG/GIF visualizations;
- add tests for numerical consistency;
- show where symplectic thinking is useful for the broader SSZ research suite.

## Core Credit

The mathematical achievements belong to **John Pardon** and his collaborators. The International Mathematical Union credits Pardon for achievements in symplectic geometry, including new approaches to virtual fundamental cycles, Fukaya categories of certain manifolds and counting holomorphic curves, and for contributions to group actions on 3-manifolds and knot theory.

Repository structure, educational notes, tests, and code: **Lino Casu**.

No affiliation with or endorsement by John Pardon, Stony Brook University, the Simons Center for Geometry and Physics, Princeton University, Stanford University, the IMU, Spektrum, Quanta, Nature, or any cited publisher is implied.

## Related SSZ Context

This repository connects conceptually to the local SSZ physics suite under `/home/error/physics/`:

- `ssz-lagrange` uses Lagrange/Hamilton formulations. Symplectic preservation is the natural mathematical language for Hamiltonian flows.
- `ssz-metric-pure` validates tensor and geodesic structure. Phase-space tests can catch numerical integrator errors.
- `ssz-lensing` studies ray propagation and observables. Hamiltonian optics and symplectic integrators are useful for stable ray-tracing.
- `segmented-calculation-suite` and related SSZ tooling benefit from reproducible validation patterns: small core functions, tests, plots, and audit-friendly output.

See `docs/ssz-bridge.md` for the detailed bridge. This bridge is methodological, not a claim that Pardon's theorems validate SSZ.

## Repository Map

```text
pardon-symplectic-geometry-ssz-lab/
├── README.md
├── CREDITS.md
├── SOURCES.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── sources.json
│   └── repo_links.json
├── docs/
│   ├── how-to-run.md
│   ├── math-map.md
│   ├── research-brief.md
│   ├── pardon-mathematics-deep-dive.md
│   ├── ssz-bridge.md
│   ├── segmented-spacetime-application-notes.md
│   ├── cross-repo-synthesis.md
│   └── deep-synthesis-and-roadmap.md
├── python/
│   ├── run_all.py
│   ├── symplectic_lab.py
│   ├── phase_space_energy.py
│   ├── symplectic_integrator_comparison.py
│   ├── holomorphic_curve_residual.py
│   ├── lagrangian_intersections.py
│   ├── moduli_space_toy.py
│   ├── knot_distortion.py
│   ├── repo_interplay_map.py
│   ├── ssz_symplectic_bridge.py
│   └── pardon_math/
└── tests/
    └── test_math_core.py
```

## Quick Start

```bash
cd /home/error/physics/pardon-symplectic-geometry-ssz-lab
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python python/run_all.py
python -m unittest discover -s tests
```

Generated PNG/GIF files appear in `outputs/`.

## Visualization Gallery

Every visualization is generated locally by `python python/run_all.py`. GIFs show the animated behavior; PNG links provide static snapshots for quick inspection.

| Script | Animation | Static PNG | Mathematical intuition |
|---|---|---|---|
| `symplectic_lab.py` | `outputs/symplectic_area_preservation.gif` | `outputs/symplectic_area_preservation.png` | Hamiltonian flow preserves area/symplectic form. |
| `phase_space_energy.py` | `outputs/phase_space_energy.gif` | `outputs/phase_space_energy.png` | Energy contours and orbit in phase space. |
| `symplectic_integrator_comparison.py` | `outputs/symplectic_vs_euler.gif` | `outputs/symplectic_vs_euler.png` | Structure-preserving vs naive integration. |
| `holomorphic_curve_residual.py` | `outputs/holomorphic_curve_residual.gif` | `outputs/holomorphic_curve_residual.png` | Cauchy-Riemann residual under non-holomorphic perturbation. |
| `lagrangian_intersections.py` | `outputs/lagrangian_intersections.gif` | `outputs/lagrangian_intersections.png` | Intersection intuition behind Floer/Fukaya ideas. |
| `moduli_space_toy.py` | `outputs/moduli_space_toy.gif` | `outputs/moduli_space_toy.png` | Degenerating solution spaces and why virtual methods exist. |
| `knot_distortion.py` | `outputs/knot_distortion.gif` | `outputs/knot_distortion.png` | Finite sampled knot distortion. |
| `repo_interplay_map.py` | `outputs/repo_interplay_map.gif` | `outputs/repo_interplay_map.png` | Cross-repo methodology map. |
| `ssz_symplectic_bridge.py` | `outputs/ssz_symplectic_bridge.gif` | `outputs/ssz_symplectic_bridge.png` | SSZ Xi/D/effective-potential bridge. |
| `regime_blend_map.py` | `outputs/regime_blend_map.gif` | `outputs/regime_blend_map.png` | Formula domains vs physical regimes. |
| `holonomy_loop_visualization.py` | `outputs/holonomy_loop.gif` | `outputs/holonomy_loop.png` | Closed-loop frequency-ratio/holonomy toy model. |
| `method_assignment_flow.py` | `outputs/method_assignment_flow.gif` | `outputs/method_assignment_flow.png` | Prime Directive observable routing. |
| `phi_ladder_state_visualization.py` | `outputs/phi_ladder_state.gif` | `outputs/phi_ladder_state.png` | Full phi-ladder state vector details. |
| `ssz_doc_audit_visualization.py` | `outputs/ssz_doc_audit.gif` | `outputs/ssz_doc_audit.png` | Full SSZ documentation audit overview. |

### Symplectic Area Preservation

![Symplectic area preservation](outputs/symplectic_area_preservation.gif)

[Static PNG](outputs/symplectic_area_preservation.png)

### Phase-Space Energy

![Phase-space energy](outputs/phase_space_energy.gif)

[Static PNG](outputs/phase_space_energy.png)

### Symplectic Integrator Comparison

![Symplectic versus Euler integration](outputs/symplectic_vs_euler.gif)

[Static PNG](outputs/symplectic_vs_euler.png)

### Cauchy-Riemann Residual

![Holomorphic curve residual](outputs/holomorphic_curve_residual.gif)

[Static PNG](outputs/holomorphic_curve_residual.png)

### Lagrangian Intersections

![Lagrangian intersections](outputs/lagrangian_intersections.gif)

[Static PNG](outputs/lagrangian_intersections.png)

### Moduli Space Toy Model

![Moduli space toy model](outputs/moduli_space_toy.gif)

[Static PNG](outputs/moduli_space_toy.png)

### Knot Distortion

![Knot distortion](outputs/knot_distortion.gif)

[Static PNG](outputs/knot_distortion.png)

### Repository Interplay Map

![Repository interplay map](outputs/repo_interplay_map.gif)

[Static PNG](outputs/repo_interplay_map.png)

### SSZ Symplectic Bridge

![SSZ symplectic bridge](outputs/ssz_symplectic_bridge.gif)

[Static PNG](outputs/ssz_symplectic_bridge.png)

### Regime Blend Map

![Regime blend map](outputs/regime_blend_map.gif)

[Static PNG](outputs/regime_blend_map.png)

### Holonomy Loop

![Holonomy loop](outputs/holonomy_loop.gif)

[Static PNG](outputs/holonomy_loop.png)

### Method Assignment Flow

![Method assignment flow](outputs/method_assignment_flow.gif)

[Static PNG](outputs/method_assignment_flow.png)

### Phi-Ladder State

![Phi-ladder state](outputs/phi_ladder_state.gif)

[Static PNG](outputs/phi_ladder_state.png)

### SSZ Documentation Audit

![SSZ documentation audit](outputs/ssz_doc_audit.gif)

[Static PNG](outputs/ssz_doc_audit.png)

## Scientific Status

| Layer | Status |
|---|---|
| Source grounding | documented in `SOURCES.md` |
| Credit hygiene | explicit in `CREDITS.md` |
| Mathematical implementation | toy models only |
| Tests | local unittest suite |
| Visual output | generated by `python/run_all.py` |
| SSZ relation | methodological bridge in `docs/ssz-bridge.md` |

## Why This Is Honest

Pardon's research is frontier mathematics. The demos here are not substitutes for his papers. They are controlled toy models that explain background intuitions: symplectic preservation, holomorphic-equation residuals, intersection patterns, virtual-method motivation, and knot distortion.

## License

Anti-Capitalist Software License v1.4, 2026 © Lino Casu. See `LICENSE`.
