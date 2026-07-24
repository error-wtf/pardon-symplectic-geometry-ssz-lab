# Test Validation Report

Generated from the repository's `unittest` discovery run.

> Passing tests establish internal implementation consistency only. They do not prove 
> Pardon's theorems or physically validate SSZ.

## Summary

| Validation layer | Passed | Total | Meaning |
|---|---:|---:|---|
| Mathematical invariants | 13 | 13 | area, radius, CR residuals, intersections, moduli, knots, holonomy |
| Numerical regression | 11 | 11 | energy drift, SSZ bridge, state identities, Hamiltonian report |
| Fail-closed guardrails | 6 | 6 | observable routing, regime split, forbidden-formula rejection |
| Artifact and traceability | 13 | 13 | repo graph, source index, outputs, README, scope boundaries |

Overall: **43/43 passed**, **0 failed**, **0 skipped**.

Machine-readable details: `data/test_validation_report.json`.
