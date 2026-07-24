# Physics Repository Expansion Audit for the Pardon/SSZ Bridge

Scope: local public/non-private physics repositories under `/home/error/physics`. Private/unpublished work is intentionally excluded from this Pardon-facing report.

## What Was Checked

The scan covered local Git repositories, README structure, test layout, Python code presence, visual output folders and canonical SSZ documentation guardrails. The highest-relevance source documents were:

- `ssz-complete-documentation/11_GUARDRAILS/prime_directive.md`
- `ssz-complete-documentation/11_GUARDRAILS/method_assignment.md`
- `ssz-complete-documentation/02_FOUNDATIONS/regime_and_formula_domain_clarification.md`
- `ssz-complete-documentation/13_FREQUENCY_FRAMEWORK/holonomy_invariants.md`
- `ssz-lagrange/README.md`
- `ssz-trajectories/README.md`
- `ssz-lensing/README.md`
- `frequency-curvature-validation/README.md`

## Main Result

The Pardon lab should expand through stricter mathematical validation, not through additional decorative plots. The useful pattern is:

```text
SSZ observable -> method assignment -> regime/formula-domain guardrail -> invariant test -> visualization
```

That matches the Pardon-side lesson: do not mistake a visual object for a proof; preserve the structure that makes a count, trajectory or invariant meaningful.

## Expansion Axes

### 1. Method Assignment as Fail-Closed Routing

SSZ documentation explicitly forbids using one method for all observables. The Pardon lab already has a method-assignment toy flow. The next improvement is a fuller routing matrix:

- timelike clock/redshift -> `Xi/D` route;
- null lensing/Shapiro/VLBI -> PPN completion route;
- orbit/precession/frame dragging -> PPN orbit route;
- Hamiltonian/geodesic simulations -> phase-space invariant route.

### 2. Regime vs Formula Domain Separation

The SSZ docs distinguish physical regimes from operative formula domains. This maps directly to the Pardon-side concern with domains, degeneracy and meaningful counts.

A useful guardrail test is:

```text
x = r/r_s
classify physical regime
select operative Xi branch
assert no forbidden/deprecated formula is used
assert visual labels show both regime and formula domain
```

### 3. Hamiltonian/Symplectic Validation

`ssz-lagrange` exposes Lagrange/Hamilton language. `ssz-trajectories` integrates radial and non-radial geodesics. The Pardon lab should act as a template for:

- energy drift checks;
- angular momentum drift checks;
- symplectic versus naive integrator comparisons;
- turning-point stability diagnostics;
- phase-space overlays next to coordinate-space trajectories.

### 4. Null Observables Need PPN Completion

`ssz-lensing` and the SSZ guardrails stress that null observables cannot be treated as `Xi`-only. Any future lensing visual in this lab should say:

```text
Xi-only visual = temporal contribution only
full null observable = PPN completion with spatial contribution
```

### 5. Holonomy: Static vs Dynamic

The SSZ holonomy docs state that static closed products telescope to 1. The Pardon lab's holonomy toy is useful only if it clearly distinguishes:

- static telescoping identity: algebraic sanity check;
- dynamic/non-spherical perturbation: physically interesting deviation.

## What Should Not Be Added

- No private/unpublished content in the public Pardon repo.
- No SSZ documentation-audit visualization; keep audit as data/text only.
- No claim that John Pardon's theorems validate SSZ.
- No conversion of test counts into proof language.
- No single-route observable calculator.

## Recommended Next Code Additions

1. `observable_routing_matrix.py`: fuller SSZ method assignment table with tests.
2. `regime_guardrail_tests.py`: explicit regime/formula-domain assertions.
3. `hamiltonian_drift_report.py`: table comparing Euler/RK/symplectic drift on a toy SSZ effective potential.
4. `holonomy_static_vs_dynamic.py`: separate static telescoping from dynamic perturbation.
5. `docs/claim-boundaries.md`: one-page boundary between toy model, theorem, implementation and physical claim.
