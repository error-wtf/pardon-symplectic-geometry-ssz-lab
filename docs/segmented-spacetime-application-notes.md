# Segmented Spacetime Application Notes

## Purpose

This document explains how the toy models in this repository can improve the numerical and conceptual discipline of Segmented Spacetime (SSZ) work under `/home/error/physics/`.

## Relevant Local Repositories

The local SSZ-style repositories inspected for structure and conventions include:

- `ssz-metric-pure`
- `ssz-lagrange`
- `ssz-lensing`
- `segmented-calculation-suite`
- `ssz-qubits`
- `Segmented-Spacetime-Mass-Projection-Unified-Results`

These repos commonly emphasize:

- quick-start commands;
- reproducible tests;
- visual plots;
- Anti-Capitalist license;
- explicit scientific status;
- cross-repository context.

## Where Pardon's Mathematical Environment Helps

### 1. Hamiltonian Structure

SSZ geodesic and ray models can be written in Hamiltonian form. Once this is done, symplectic geometry becomes the correct background language. The relevant invariant is not merely energy but the phase-space structure.

### 2. Integrator Choice

The script `symplectic_integrator_comparison.py` shows a practical failure mode: explicit Euler spirals away in phase space. A structure-preserving method such as leapfrog stays bounded for the harmonic oscillator.

For SSZ this suggests a validation rule:

```text
Never trust a long geodesic/ray simulation until a structure-preserving integrator has been compared against a naive one.
```

### 3. Lensing and Ray Tracing

For lensing, Hamiltonian optics treats rays as trajectories in phase space. Symplectic stepping helps distinguish real bending effects from numerical drift.

### 4. Degeneracies and Singular Limits

The toy moduli-space demo shows how solution spaces can collapse, disappear, or change dimension. SSZ models that remove or soften singularities should document parameter limits with the same discipline:

```text
parameter -> solution structure -> diagnostic plot -> test
```

### 5. Tests as Scientific Hygiene

This repo follows the SSZ pattern: core functions live separately from visualization scripts, and tests target the core functions. That keeps plots from becoming unverifiable illustrations.

## Correct Claims

Safe claim:

> Symplectic geometry and Hamiltonian numerical methods are useful for SSZ validation because SSZ geodesic/ray dynamics can be studied in phase space.

Unsafe claim:

> Pardon's Fields Medal work proves SSZ.

Do not make the unsafe claim.
