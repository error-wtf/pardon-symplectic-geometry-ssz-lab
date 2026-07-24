# How To Run Everything

## 1. Environment

```bash
git clone https://github.com/error-wtf/pardon-symplectic-geometry-ssz-lab.git
cd pardon-symplectic-geometry-ssz-lab
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
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
python python/ssz_symplectic_bridge.py
python python/phi_ladder_state_visualization.py
python python/method_assignment_flow.py
python python/holonomy_loop_visualization.py
python python/regime_blend_map.py
python python/hamiltonian_drift_visualization.py
python python/test_validation_report.py
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

The SSZ visuals use the explicit repository profile
`local_saturation_c2_blend_v1`. This keeps the saturation and complementary
decay source contexts from being silently mixed.
