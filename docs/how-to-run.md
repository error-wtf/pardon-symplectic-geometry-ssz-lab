# How To Run Everything

## 1. Environment

```bash
cd /home/error/physics/pardon-symplectic-geometry-ssz-lab
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run Tests

```bash
python -m unittest discover -s tests
```

Expected result: all tests pass.

## 3. Generate All Visualizations

```bash
python python/run_all.py
```

Outputs are written to:

```text
outputs/
```

## 4. Run Individual Visualizations

```bash
python python/symplectic_lab.py
python python/phase_space_energy.py
python python/symplectic_integrator_comparison.py
python python/holomorphic_curve_residual.py
python python/lagrangian_intersections.py
python python/moduli_space_toy.py
python python/knot_distortion.py
```

## 5. How This Helps SSZ Work

The immediate reusable pattern is:

```text
model equation -> core numerical function -> test invariant -> generate plot/GIF -> document limitation
```

For SSZ, replace the harmonic oscillator Hamiltonian with an SSZ geodesic or ray Hamiltonian and keep the same validation discipline:

- check energy drift;
- check phase-space structure;
- compare naive and structure-preserving integrators;
- keep outputs reproducible.
