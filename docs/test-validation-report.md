# Test Validation Report

Generated from the repository's `unittest` discovery run.

> Passing tests establish internal implementation consistency only. They do not prove
> Pardon's theorems or physically validate SSZ.

## Summary

| Validation layer | Passed | Total | Meaning |
|---|---:|---:|---|
| Mathematical invariants | 14 | 14 | area, radius, CR residuals, intersections, moduli, knots, holonomy |
| Numerical regression | 15 | 15 | energy drift, SSZ C1/C2 blend, state identities, Hamiltonian report |
| Fail-closed guardrails | 6 | 6 | observable routing, regime split, forbidden-formula rejection |
| Artifact and traceability | 14 | 14 | output dimensions and motion, README scope, claim boundaries, traceability |

Overall: **49/49 passed**, **0 failed**, **0 skipped**.

Machine-readable details: `data/test_validation_report.json`.
