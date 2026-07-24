from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.cr_residual import cauchy_riemann_residual
from pardon_math.integrators import explicit_euler, harmonic_energy, leapfrog, symplectic_euler
from pardon_math.knot import cumulative_lengths, distortion_sample, trefoil
from pardon_math.lagrangian import curve_a, curve_b, nearest_intersections
from pardon_math.moduli import circle_moduli_points, solution_dimension_label
from pardon_math.symplectic import polygon_area, rotate
from pardon_math.ssz_bridge import D_MIN_AT_RS, D_factor, XI_MAX, effective_potential, scale_factor, xi_canonical, xi_strong, xi_weak
from pardon_math.repo_graph import adjacency, load_repo_graph, validate_edges


class SymplecticTests(unittest.TestCase):
    def test_rotation_preserves_area(self):
        points = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        self.assertAlmostEqual(polygon_area(points), polygon_area(rotate(points, 1.234)), places=12)

    def test_rotation_preserves_radius(self):
        points = np.array([[1.0, 2.0], [-0.5, 0.25], [0.3, -0.8]])
        moved = rotate(points, 0.7)
        np.testing.assert_allclose(np.linalg.norm(points, axis=1), np.linalg.norm(moved, axis=1), atol=1e-12)


class CauchyRiemannTests(unittest.TestCase):
    def test_holomorphic_residual_small(self):
        _, _, residual = cauchy_riemann_residual(0.0, grid_n=80)
        self.assertLess(float(residual.mean()), 0.01)

    def test_nonholomorphic_residual_positive(self):
        _, _, residual = cauchy_riemann_residual(0.5, grid_n=80)
        self.assertGreater(float(residual.mean()), 0.5)


class IntegratorTests(unittest.TestCase):
    def test_euler_energy_drift_worse_than_leapfrog(self):
        euler = explicit_euler(1.0, 0.0, 0.08, 300)
        leap = leapfrog(1.0, 0.0, 0.08, 300)
        h0 = 0.5
        euler_error = abs(float(harmonic_energy(euler[-1, 0], euler[-1, 1])) - h0)
        leap_error = abs(float(harmonic_energy(leap[-1, 0], leap[-1, 1])) - h0)
        self.assertGreater(euler_error, 10 * leap_error)

    def test_symplectic_euler_bounded_for_short_run(self):
        traj = symplectic_euler(1.0, 0.0, 0.04, 200)
        energies = harmonic_energy(traj[:, 0], traj[:, 1])
        self.assertLess(float(energies.max() - energies.min()), 0.05)


class LagrangianTests(unittest.TestCase):
    def test_curves_have_shape(self):
        self.assertEqual(curve_a(10).shape, (10, 2))
        self.assertEqual(curve_b(0.2, 10).shape, (10, 2))

    def test_intersections_return_two_columns(self):
        hits = nearest_intersections(curve_a(120), curve_b(0.0, 120), threshold=0.03)
        self.assertEqual(hits.shape[1], 2)


class ModuliTests(unittest.TestCase):
    def test_moduli_labels(self):
        self.assertEqual(solution_dimension_label(-1.0), "empty")
        self.assertEqual(solution_dimension_label(0.0), "singular point")
        self.assertEqual(solution_dimension_label(1.0), "smooth circle")

    def test_moduli_point_counts(self):
        self.assertEqual(circle_moduli_points(-0.1).shape, (0, 2))
        self.assertEqual(circle_moduli_points(0.0).shape, (1, 2))
        self.assertEqual(circle_moduli_points(1.0, 20).shape, (20, 2))


class KnotTests(unittest.TestCase):
    def test_trefoil_shape(self):
        pts = trefoil(120)
        self.assertEqual(pts.shape, (120, 3))

    def test_lengths_positive(self):
        pts = trefoil(120)
        _, total = cumulative_lengths(pts)
        self.assertGreater(total, 0)

    def test_distortion_ratio_positive(self):
        pts = trefoil(80)
        ratio, i, j = distortion_sample(pts)
        self.assertGreater(ratio, 1.0)
        self.assertNotEqual(i, j)


if __name__ == "__main__":
    unittest.main()


class RepoGraphTests(unittest.TestCase):
    def test_repo_graph_edges_are_valid(self):
        graph = load_repo_graph(ROOT / "data" / "repo_links.json")
        self.assertTrue(validate_edges(graph))

    def test_repo_graph_connects_pardon_to_ssz(self):
        graph = load_repo_graph(ROOT / "data" / "repo_links.json")
        adj = adjacency(graph)
        self.assertIn("symplectic", adj["pardon"])
        self.assertIn("ssz_lagrange", adj["symplectic"])
        self.assertIn("ssz_trajectories", adj["symplectic"])


class SSZBridgeTests(unittest.TestCase):
    def test_canonical_values_at_rs_are_finite(self):
        self.assertAlmostEqual(xi_strong(1.0), XI_MAX, places=12)
        self.assertAlmostEqual(D_factor(1.0), D_MIN_AT_RS, places=12)
        self.assertGreater(D_factor(1.0), 0.5)

    def test_weak_branch_matches_documentation(self):
        self.assertAlmostEqual(xi_weak(10.0), 0.05, places=12)
        self.assertAlmostEqual(scale_factor(10.0), 1.05, places=12)

    def test_d_factor_increases_outward(self):
        xs = np.array([1.0, 1.5, 2.0, 5.0, 10.0])
        d = D_factor(xs)
        self.assertTrue(np.all(np.diff(d) > 0))

    def test_effective_potential_is_positive(self):
        xs = np.linspace(1.0, 10.0, 50)
        self.assertTrue(np.all(effective_potential(xs, ell=2.0) > 0))
