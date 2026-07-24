# Hamiltonian Drift Report

Toy SSZ effective-potential drift check. This is a numerical QA artifact, not a physical validation.

| Method | Absolute drift | Energy band | q range |
|---|---:|---:|---|
| `explicit_euler` | 1.081799e-03 | 1.083494e-03 | 3.000 .. 16.365 |
| `rk4` | 3.507138e-09 | 3.507138e-09 | 3.000 .. 16.313 |
| `symplectic_euler` | 1.006422e-04 | 3.414580e-04 | 3.000 .. 16.324 |
| `leapfrog` | 4.816277e-07 | 8.678425e-07 | 3.000 .. 16.313 |
