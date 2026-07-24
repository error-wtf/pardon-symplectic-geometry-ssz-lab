# Internal Quality Hardening Notes

## Scope

This document records generic quality improvements derived from internal local repository review. It deliberately does not identify or disclose private/internal repository details.

## Adopted Quality Patterns

### 1. Claim Scope Categories

Every result should be classified as one of:

- `educational_toy_model`
- `derived_identity`
- `model_regression`
- `methodological_bridge`
- `external_source_summary`
- `future_work`

This prevents a toy demo from being mistaken for a research proof.

### 2. Forward-Only Pipeline

The repo should preserve a forward-only workflow:

```text
source/math premise -> implemented function -> invariant/test -> visualization -> interpretation boundary
```

Visualizations must not be used as calibration data.

### 3. Evidence Ledger

The repo should maintain a small ledger that ties every major output to:

- source premise;
- script;
- generated artifact;
- claim scope;
- tests or checks;
- limitation.

See `data/evidence_ledger.csv`.

### 4. Test Explanations

Tests should not only check numbers. They should encode why a condition matters:

- area preservation matters because Hamiltonian flow is symplectic;
- energy drift matters because naive integration can create fake physics;
- method assignment matters because SSZ forbids single-method observable handling;
- holonomy product matters because closed-loop frequency ratios are a geometric invariant in the static toy model.

### 5. Release Readiness

A clean local release condition is:

```text
compileall OK + unittest OK + run_all OK + output index complete + README scope boundaries intact
```
