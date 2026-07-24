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
| `outputs/repo_interplay_map.gif` | `python/repo_interplay_map.py` | `pardon_math/repo_graph.py` | `RepoGraphTests` | Conceptual cross-repo map |
| `outputs/ssz_symplectic_bridge.gif` | `python/ssz_symplectic_bridge.py` | `pardon_math/ssz_bridge.py` | `SSZBridgeTests` | Toy radial Hamiltonian bridge |
| `outputs/regime_blend_map.gif` | `python/regime_blend_map.py` | `pardon_math/ssz_bridge.py`, `pardon_math/regime_guardrails.py` | `SSZBridgeTests`, `RegimeGuardrailTests` | Formula-domain and regime guardrail |
| `outputs/holonomy_loop.gif` | `python/holonomy_loop_visualization.py` | `pardon_math/holonomy.py` | `HolonomyTests` | Static identity plus illustrative dynamic deviation |
| `outputs/method_assignment_flow.gif` | `python/method_assignment_flow.py` | `pardon_math/method_assignment.py` | `MethodAssignmentTests` | Fail-closed observable routing |
| `outputs/phi_ladder_state.gif` | `python/phi_ladder_state_visualization.py` | `pardon_math/ssz_state.py` | `SSZStateTests` | Simplified operative bridge state |
| `outputs/hamiltonian_drift_report.gif` | `python/hamiltonian_drift_visualization.py` | `hamiltonian_drift_report.py`, `pardon_math/ssz_bridge.py` | `HamiltonianDriftTests` | Numeric QA diagnostic, not physical validation |
| `outputs/test_validation_matrix.gif` | `python/test_validation_visualization.py` | discovered `unittest` suite | all test classes | Internal implementation consistency, not mathematical proof or physical validation |
| `data/ssz_doc_index.json` | local documentation scan | data only | `SSZDocIndexTests` | Keyword index, not semantic proof |
| `data/physics_repo_audit.json` | local public-repo scan | data only | `PhysicsRepoAuditTests` | Non-private local expansion map |

The rejected SSZ documentation-audit image is intentionally absent from the gallery. The documentation audit remains text/data only because a documentation inventory is not a useful mathematical visualization.
