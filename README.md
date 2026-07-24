# Pardon Symplectic Geometry and SSZ Lab

**Executable geometric models, numerical diagnostics and an explicitly bounded bridge to Segmented Spacetime (SSZ).**

[![License](https://img.shields.io/badge/license-ACSL%201.4-red)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](requirements.txt)
[![Tests](https://img.shields.io/badge/tests-49%2F49%20passing-18864b)](docs/test-validation-report.md)
[![Artifacts](https://img.shields.io/badge/visuals-13%20GIF%20%2B%2013%20PNG-336699)](VISUALIZATION_INDEX.md)
[![Status](https://img.shields.io/badge/status-archived%20reference-lightgrey)](docs/research-brief.md)

> [!IMPORTANT]
> This repository does not reproduce or prove John Pardon's theorems, does not implement virtual fundamental cycles or Fukaya categories, and does not establish the physical validity of SSZ. It contains controlled toy models, numerical QA and explicit claim boundaries.

## What This Repository Shows

The useful connection between the two subjects is methodological:

```text
geometric structure
    -> choose the correct mathematical object
    -> preserve its invariants numerically
    -> expose approximation and regime boundaries
    -> interpret only what the calculation supports
```

The code demonstrates three concrete ideas:

1. **Hamiltonian structure matters.** A visually plausible trajectory can still accumulate artificial energy or phase-space error.
2. **Degeneracy and domain changes must be explicit.** Intersections, moduli fibers and SSZ formula transitions cannot be interpreted safely without their parameter domain.
3. **An observable determines its method.** A clock-rate equation is not a complete light-path or orbital calculation.

The mathematical context is documented in [Pardon Mathematics Deep Dive](docs/pardon-mathematics-deep-dive.md). The SSZ connection is documented in [SSZ Bridge](docs/ssz-bridge.md) and [Full Deep Analysis](docs/ssz-pardon-full-deep-analysis.md).

## Declared SSZ Profile

All generated artifacts that numerically evaluate `Xi` or `D` use one fixed source profile:

```text
profile: local_saturation_c2_blend_v1

x < 1.8          Xi = min(1 - exp(-phi*x), Xi_max)
1.8 <= x <= 2.2  C2 smootherstep blend
x > 2.2          Xi = 1/(2x)

D(x) = 1/(1 + Xi(x))
Xi_max = 1 - exp(-phi)
```

The local SSZ documentation also contains the complementary inner decay form `1 - exp(-phi/x)`. It is implemented as `xi_decay()` for explicit comparison, but it is never substituted silently into generated results. Both forms agree at `x=1` and differ elsewhere. Public physics panels are restricted to the exterior comparison domain `x >= 1`. This source-profile declaration and domain boundary are therefore part of the result, not a footnote.

Formula domains and physical regimes are kept separate:

| Radius `x = r/r_s` | Physical context | Operative formula |
|---:|---|---|
| `< 1.8` | very close | g2 saturation |
| `1.8 .. 2.2` | transition | C2 blend |
| `2.2 .. 3` | photon-sphere context | g1 weak branch |
| `3 .. 10` | strong context | g1 weak branch |
| `> 10` | weak field | g1 weak branch |

See [Claim Boundaries](docs/claim-boundaries.md) for the precise scientific status of every layer.

## Mathematical Models

| Context | Executable model | Directly demonstrated | Not demonstrated |
|---|---|---|---|
| Symplectic geometry | `symplectic_lab.py` | Area preservation under a controlled canonical rotation | General Hamiltonian-flow theorem |
| Numerical Hamiltonian dynamics | `phase_space_energy.py`, `symplectic_integrator_comparison.py` | Phase paths and energy-error behavior | Universal superiority of one integrator |
| Holomorphic maps | `holomorphic_curve_residual.py` | Cauchy-Riemann residual under anti-holomorphic perturbation | Pseudo-holomorphic curve theory |
| Lagrangian intersections | `lagrangian_intersections.py` | Phase-sensitive intersections of two periodic curves | Floer homology or a Fukaya category |
| Moduli spaces | `moduli_space_toy.py` | Empty, singular and smooth fibers of one family | Virtual fundamental-cycle machinery |
| Knot distortion | `knot_distortion.py` | Finite sampled intrinsic/chord ratio | Pardon's knot-distortion theorem |

## Key Visual Results

The README contains only the figures needed to understand the central mathematical and SSZ conclusions. All 13 reproducible animation/PNG pairs are cataloged in [VISUALIZATION_INDEX.md](VISUALIZATION_INDEX.md).

### 1. Structure-Preserving Integration

All three methods integrate the same harmonic oscillator. Explicit Euler deforms the phase path and accumulates energy error; the structure-preserving methods keep the qualitative orbit bounded over this run.

![Naive and structure-preserving integration](outputs/symplectic_vs_euler.gif)

[Static PNG](outputs/symplectic_vs_euler.png)

This is a numerical benchmark, not a claim that every symplectic method is more accurate at every step.

### 2. SSZ Dependency Chain

The bridge follows one explicit computational chain: `Xi(x) -> D(x) -> V_eff(x) -> radial phase path`. The phase path is produced by the repository's leapfrog integration, not by an illustrative sinusoid.

![SSZ scalar-to-Hamiltonian bridge](outputs/ssz_symplectic_bridge.gif)

[Static PNG](outputs/ssz_symplectic_bridge.png)

The effective Hamiltonian is a local toy diagnostic built from the documented `D^2[epsilon + ell^2/x^2]` potential form. It is not presented as a complete SSZ geodesic solver.

### 3. Hamiltonian Drift

The four phase paths nearly overlap because they solve the same outbound radial initial-value problem. The energy panels reveal what the phase portrait alone hides: different integrators accumulate different Hamiltonian error bands.

![Hamiltonian drift on the toy SSZ potential](outputs/hamiltonian_drift_report.gif)

[Static PNG](outputs/hamiltonian_drift_report.png) | [Numeric report](docs/hamiltonian-drift-report.md)

### 4. Regime Is Not Formula Domain

The highlighted column is selected by the same `route_regime()` function used in tests. At `x=2.6`, for example, the physical context is the photon-sphere regime while the operative field expression is already the g1 branch.

![Physical regime and formula-domain routing](outputs/regime_blend_map.gif)

[Static PNG](outputs/regime_blend_map.png)

### 5. Observable-Specific Method Routing

The rows are generated from the same routing objects used by the test suite. Clock observables use direct `Xi/D` relations; light paths require the PPN spatial contribution; orbits and geodesics require PPN or Hamilton/Lagrange machinery with invariant checks. Unknown classes fail closed.

![Observable-specific method assignment](outputs/method_assignment_flow.gif)

[Static PNG](outputs/method_assignment_flow.png) | [Routing matrix](docs/observable-routing-matrix.md)

### 6. Static Cancellation and Dynamic Holonomy

For three static clocks, the closed product of `D` ratios telescopes exactly to one. The second panel is intentionally labeled as a separate toy assumption: a non-trivial loop signal needs time dependence, path dependence or non-spherical structure.

![Static and dynamic holonomy diagnostic](outputs/holonomy_loop.gif)

[Static PNG](outputs/holonomy_loop.png)

## Why the Pardon Context Is Useful

John Pardon's cited work concerns difficult structures in symplectic geometry and topology: pseudo-holomorphic curves, virtual fundamental cycles, contact homology, Fukaya categories and knot distortion. This lab does not reconstruct those results. It uses elementary examples to retain four relevant habits:

- preserve geometric structure rather than trusting coordinates alone;
- treat singular or non-transverse solution spaces carefully;
- separate local computations from global conclusions;
- distinguish a runnable example from a theorem.

Those habits transfer directly to SSZ numerical work. They do not transfer theorem-level evidence from Pardon to SSZ.

## Executable Validation

The test suite contains **49 checks** covering mathematical invariants, numerical regressions, SSZ profile and C1/C2 blend continuity, routing guardrails, artifact dimensions, nonblank static frames, visible GIF motion, Markdown links and traceability.

```bash
python -m unittest discover -s tests
```

Results are generated as text and structured data rather than as a decorative dashboard:

- [Readable test report](docs/test-validation-report.md)
- [Machine-readable test report](data/test_validation_report.json)
- [Source-to-code traceability](docs/source-to-code-traceability.md)
- [Evidence ledger](data/evidence_ledger.csv)

Passing tests establish internal consistency for this implementation. They are not external peer review, proof of Pardon's results or empirical confirmation of SSZ.

## Reproduce Everything

```bash
git clone https://github.com/error-wtf/pardon-symplectic-geometry-ssz-lab.git
cd pardon-symplectic-geometry-ssz-lab
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python python/run_all.py
```

`run_all.py` regenerates all 13 GIF/PNG pairs, the Hamiltonian CSV/Markdown report, the observable-routing export and the executable test reports. For individual commands, see [How To Run Everything](docs/how-to-run.md).

## Repository Map

| Path | Purpose |
|---|---|
| `python/pardon_math/` | Reusable mathematical functions and SSZ guardrails |
| `python/*.py` | Visualization and report generators |
| `tests/test_math_core.py` | 49 invariant, regression, guardrail and artifact checks |
| `outputs/` | 13 generated GIF/PNG pairs, all at stable dimensions |
| `data/` | Minimal machine-readable routing, evidence and numerical reports |
| `docs/` | Mathematical context, SSZ analysis, claim boundaries and readable reports |
| `VISUALIZATION_INDEX.md` | Complete visual catalog and interpretation guide |

## Related SSZ Repositories

- [ssz-complete-documentation](https://github.com/error-wtf/ssz-complete-documentation) - source documentation used for formula and guardrail comparison.
- [ssz-lagrange](https://github.com/error-wtf/ssz-lagrange) - Lagrange and Hamilton formulations.
- [ssz-trajectories](https://github.com/error-wtf/ssz-trajectories) - trajectory and geodesic context.
- [galactic-year](https://github.com/error-wtf/galactic-year) - orbit-scale numerical context.
- [chord-partition](https://github.com/error-wtf/chord-partition) - discrete phi and closure structures.
- [claudes-cycles](https://github.com/error-wtf/claudes-cycles) - finite cycle and closure-verification patterns.

## Credits

The mathematical achievements described in the Fields Medal context belong to **John Pardon** and his collaborators. The [International Mathematical Union citation](https://www.mathunion.org/imu-awards/fields-medal/fields-medals-2026) and Pardon's publications are the authoritative sources for those results.

The SSZ framework and documentation used for the methodological comparison are credited to **Carmen N. Wrede** and **Lino P. Casu**.

Repository design, educational integration, Python code, visualizations, tests and documentation: **Lino P. Casu**. Full attribution is in [CREDITS.md](CREDITS.md) and [SOURCES.md](SOURCES.md).

No affiliation with or endorsement by John Pardon, Carmen N. Wrede, Stony Brook University, the Simons Center for Geometry and Physics, Princeton University, Stanford University, the International Mathematical Union or any cited publisher is implied.

## License

Anti-Capitalist Software License v1.4, 2026 (c) Lino Casu. See [LICENSE](LICENSE).
