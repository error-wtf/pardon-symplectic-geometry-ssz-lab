# Source-to-Code Traceability

This table links each public-facing output to its implementation, test anchor and claim boundary.

| Artifact | Script/Data | Core module | Test anchor | Claim boundary |
|---|---|---|---|---|
| `outputs/symplectic_area_preservation.gif` | `python/symplectic_lab.py` | `pardon_math/symplectic.py` | `SymplecticTests` | Educational Hamiltonian toy model |
| `outputs/phase_space_energy.gif` | `python/phase_space_energy.py` | `pardon_math/integrators.py` | `IntegratorTests` | Harmonic oscillator diagnostic, not an SSZ geodesic |
| `outputs/symplectic_vs_euler.gif` | `python/symplectic_integrator_comparison.py` | `pardon_math/integrators.py` | `IntegratorTests` | Integrator comparison only |
| `outputs/holomorphic_curve_residual.gif` | `python/holomorphic_curve_residual.py` | `pardon_math/cr_residual.py` | `CauchyRiemannTests` | Cauchy-Riemann residual toy, not pseudo-holomorphic curve theory |
| `outputs/lagrangian_intersections.gif` | `python/lagrangian_intersections.py` | `pardon_math/lagrangian.py` | `LagrangianTests` | Intersection intuition, not a Fukaya category |
| `outputs/moduli_space_toy.gif` | `python/moduli_space_toy.py` | `pardon_math/moduli.py` | `ModuliTests` | Singular family intuition only |
| `outputs/knot_distortion.gif` | `python/knot_distortion.py` | `pardon_math/knot.py` | `KnotTests` | Finite sampled knot approximation |
| `outputs/ssz_symplectic_bridge.gif` | `python/ssz_symplectic_bridge.py` | `pardon_math/ssz_bridge.py` | `SSZBridgeTests` | Exterior `x >= 1` toy Hamiltonian under the declared local-saturation profile |
| `outputs/regime_blend_map.gif` | `python/regime_blend_map.py` | `pardon_math/ssz_bridge.py`, `pardon_math/regime_guardrails.py` | `SSZBridgeTests`, `RegimeGuardrailTests` | Exterior `x >= 1` formula-domain and regime guardrail |
| `outputs/holonomy_loop.gif` | `python/holonomy_loop_visualization.py` | `pardon_math/holonomy.py` | `HolonomyTests` | Static identity plus illustrative dynamic deviation |
| `outputs/method_assignment_flow.gif` | `python/method_assignment_flow.py` | `pardon_math/method_assignment.py` | `MethodAssignmentTests` | Fail-closed observable routing |
| `outputs/phi_ladder_state.gif` | `python/phi_ladder_state_visualization.py` | `pardon_math/ssz_state.py` | `SSZStateTests` | Exterior phi ladder under the declared local-saturation profile; alternative inner profile differs |
| `outputs/hamiltonian_drift_report.gif` | `python/hamiltonian_drift_visualization.py` | `hamiltonian_drift_report.py`, `pardon_math/ssz_bridge.py` | `HamiltonianDriftTests` | Numeric QA diagnostic, not physical validation |
| `data/test_validation_report.json` | `python/test_validation_report.py` | discovered `unittest` suite | `TestValidationReportTests` | Internal implementation consistency, not mathematical proof or physical validation |

The rejected documentation-audit, repository-interplay and test-dashboard images are intentionally absent. These meta-dashboard images are intentionally absent because they do not explain a mathematical identity, numerical behavior, physical routing decision or claim boundary. Test results remain available as JSON and Markdown.
