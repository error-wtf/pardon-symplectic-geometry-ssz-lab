from __future__ import annotations

import csv
import json
import re
import sys
import unittest
import urllib.parse
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from pardon_math.cr_residual import cauchy_riemann_residual
from pardon_math.integrators import explicit_euler, harmonic_energy, leapfrog, symplectic_euler
from pardon_math.holonomy import dynamic_loop_deviation, triple_clock_product
from pardon_math.knot import cumulative_lengths, distortion_sample, trefoil
from pardon_math.lagrangian import curve_a, curve_b, nearest_intersections
from pardon_math.method_assignment import ROUTES, assign_method, route_observable
from pardon_math.moduli import circle_moduli_points, solution_dimension_label
from pardon_math.regime_guardrails import assert_formula_allowed, formula_domain, physical_regime, route_regime
from pardon_math.symplectic import polygon_area, rotate
from pardon_math.ssz_bridge import (
    BLEND_END,
    BLEND_START,
    D_MIN_AT_RS,
    PHI,
    SSZ_PROFILE,
    XI_MAX,
    D_factor,
    effective_potential,
    scale_factor,
    xi_canonical,
    xi_decay,
    xi_strong,
    xi_weak,
)
from pardon_math.ssz_state import phi_ladder, regime_label, state_vector


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

    def test_intersection_candidates_are_clustered(self):
        counts = [
            len(nearest_intersections(curve_a(500), curve_b(phase, 500)))
            for phase in np.linspace(0.0, 0.9, 10)
        ]
        self.assertGreater(max(counts), 0)
        self.assertLessEqual(max(counts), 4)


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


class SSZBridgeTests(unittest.TestCase):
    def test_canonical_values_at_rs_are_finite(self):
        self.assertAlmostEqual(xi_strong(1.0), XI_MAX, places=12)
        self.assertAlmostEqual(D_factor(1.0), D_MIN_AT_RS, places=12)
        self.assertGreater(D_factor(1.0), 0.5)

    def test_weak_branch_matches_documentation(self):
        self.assertAlmostEqual(xi_weak(10.0), 0.05, places=12)
        self.assertAlmostEqual(scale_factor(10.0), 1.05, places=12)

    def test_d_factor_recovers_outward_after_blend(self):
        xs = np.array([2.2, 3.0, 5.0, 10.0])
        d = D_factor(xs)
        self.assertTrue(np.all(np.diff(d) > 0))
        self.assertAlmostEqual(D_factor(1.0), D_factor(1.5), places=12)

    def test_effective_potential_is_positive(self):
        xs = np.linspace(1.0, 10.0, 50)
        self.assertTrue(np.all(effective_potential(xs, ell=2.0) > 0))

    def test_declared_profile_and_alternative_are_explicit(self):
        self.assertEqual(SSZ_PROFILE, "local_saturation_c2_blend_v1")
        self.assertAlmostEqual(xi_decay(1.0), xi_strong(1.0), places=12)
        self.assertNotAlmostEqual(xi_decay(PHI), xi_strong(PHI), places=3)

    def test_blend_joins_the_declared_source_branches(self):
        self.assertAlmostEqual(xi_canonical(BLEND_START), xi_strong(BLEND_START), places=12)
        self.assertAlmostEqual(xi_canonical(BLEND_END), xi_weak(BLEND_END), places=12)

    def test_blend_is_c1_at_both_formula_boundaries(self):
        h = 1e-5
        for boundary in (BLEND_START, BLEND_END):
            left = (xi_canonical(boundary) - xi_canonical(boundary - h)) / h
            right = (xi_canonical(boundary + h) - xi_canonical(boundary)) / h
            self.assertAlmostEqual(left, right, delta=2e-5)

    def test_blend_is_c2_at_both_formula_boundaries(self):
        h = 1e-5
        for boundary in (BLEND_START, BLEND_END):
            left = (
                xi_canonical(boundary)
                - 2.0 * xi_canonical(boundary - h)
                + xi_canonical(boundary - 2.0 * h)
            ) / h**2
            right = (
                xi_canonical(boundary + 2.0 * h)
                - 2.0 * xi_canonical(boundary + h)
                + xi_canonical(boundary)
            ) / h**2
            self.assertAlmostEqual(left, right, delta=1e-2)


class SSZStateTests(unittest.TestCase):
    def test_phi_ladder_self_similarity(self):
        xs = phi_ladder(-2, 4)
        ratios = xs[1:] / xs[:-1]
        self.assertTrue(np.allclose(ratios, ratios[0]))

    def test_state_conversions_are_consistent(self):
        st = state_vector(1.0)
        self.assertAlmostEqual(st["s"], 1.0 + st["Xi"], places=12)
        self.assertAlmostEqual(st["D"], 1.0 / st["s"], places=12)
        self.assertAlmostEqual(st["N_eff"], 4.0 * st["s"], places=12)

    def test_regime_labels_cover_guardrails(self):
        self.assertEqual(regime_label(1.0), "g2/very_close")
        self.assertEqual(regime_label(2.0), "blend")
        self.assertEqual(regime_label(2.6), "photon_sphere")
        self.assertEqual(regime_label(5.0), "strong_context/g1_formula")
        self.assertEqual(regime_label(20.0), "weak")


class MethodAssignmentTests(unittest.TestCase):
    def test_prime_directive_routing(self):
        self.assertEqual(assign_method("redshift"), "Xi/D direct")
        self.assertEqual(assign_method("lensing"), "PPN (1+gamma)")
        self.assertIn("Hamilton", assign_method("geodesic"))

    def test_full_route_contains_guardrails(self):
        self.assertGreaterEqual(len(ROUTES), 15)
        lensing = route_observable("shapiro delay")
        self.assertEqual(lensing.observable, "shapiro")
        self.assertIn("spatial", lensing.guardrail)
        self.assertIn("methodological", route_observable("vlbi-delay").claim_boundary)

    def test_unknown_observable_fails_closed(self):
        with self.assertRaises(KeyError):
            assign_method("everything")


class RegimeGuardrailTests(unittest.TestCase):
    def test_physical_regime_and_formula_domain_are_separate(self):
        self.assertEqual(physical_regime(2.6), "photon_sphere_context")
        self.assertEqual(formula_domain(2.6), "g1_weak_branch")
        self.assertIn("photon-sphere context", route_regime(2.6).guardrail)

    def test_regime_boundaries_match_ssz_state_labels(self):
        self.assertEqual(physical_regime(1.0), "very_close/g2_context")
        self.assertEqual(formula_domain(1.0), "g2_saturation")
        self.assertEqual(physical_regime(2.0), "transition_blend")
        self.assertEqual(formula_domain(2.0), "c2_smootherstep_blend")
        self.assertEqual(physical_regime(20.0), "weak_field")

    def test_forbidden_formula_routes_fail_closed(self):
        assert_formula_allowed("g2_saturation")
        with self.assertRaises(ValueError):
            assert_formula_allowed("single method for all observables")
        with self.assertRaises(ValueError):
            assert_formula_allowed("universal-xi-only-null")


class HolonomyTests(unittest.TestCase):
    def test_static_triple_clock_product_telescopes(self):
        self.assertAlmostEqual(triple_clock_product((1.2, 2.5, 8.0)), 1.0, places=12)

    def test_dynamic_loop_deviation_has_shape(self):
        t = np.linspace(0, 2*np.pi, 50)
        y = dynamic_loop_deviation(t)
        self.assertEqual(y.shape, t.shape)
        self.assertGreater(float(y.max() - y.min()), 0.01)


class EvidenceLedgerTests(unittest.TestCase):
    def test_evidence_ledger_has_claim_scopes(self):
        with (ROOT / "data" / "evidence_ledger.csv").open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 10)
        self.assertTrue(all(row["claim_scope"] for row in rows))

class VisualizationOutputTests(unittest.TestCase):
    EXPECTED_STEMS = (
        "symplectic_area_preservation",
        "phase_space_energy",
        "symplectic_vs_euler",
        "holomorphic_curve_residual",
        "lagrangian_intersections",
        "moduli_space_toy",
        "knot_distortion",
        "ssz_symplectic_bridge",
        "regime_blend_map",
        "holonomy_loop",
        "method_assignment_flow",
        "phi_ladder_state",
        "hamiltonian_drift_report",
    )

    def test_all_visualization_pairs_exist(self):
        expected = set(self.EXPECTED_STEMS)
        actual_gifs = {path.stem for path in (ROOT / "outputs").glob("*.gif")}
        actual_pngs = {path.stem for path in (ROOT / "outputs").glob("*.png")}
        self.assertEqual(actual_gifs, expected)
        self.assertEqual(actual_pngs, expected)
        for stem in self.EXPECTED_STEMS:
            with self.subTest(stem=stem):
                self.assertTrue((ROOT / "outputs" / f"{stem}.gif").is_file())
                self.assertTrue((ROOT / "outputs" / f"{stem}.png").is_file())

    KEY_README_STEMS = (
        "symplectic_vs_euler",
        "hamiltonian_drift_report",
        "ssz_symplectic_bridge",
        "regime_blend_map",
        "method_assignment_flow",
        "holonomy_loop",
    )

    def test_visualization_index_catalogs_every_animation(self):
        index = (ROOT / "VISUALIZATION_INDEX.md").read_text(encoding="utf-8")
        for stem in self.EXPECTED_STEMS:
            with self.subTest(stem=stem):
                self.assertIn(f"outputs/{stem}.gif", index)
                self.assertIn(f"outputs/{stem}.png", index)

    def test_readme_embeds_only_key_diagnostics(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for stem in self.KEY_README_STEMS:
            with self.subTest(stem=stem):
                self.assertIn(f"outputs/{stem}.gif", readme)
                self.assertIn(f"outputs/{stem}.png", readme)
        for stem in set(self.EXPECTED_STEMS) - set(self.KEY_README_STEMS):
            with self.subTest(stem=stem):
                self.assertNotIn(f"outputs/{stem}.gif", readme)



class VisualizationScopeTests(unittest.TestCase):
    def test_meta_dashboards_are_not_gallery_outputs(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for stem in ("ssz_doc_audit", "repo_interplay_map", "test_validation_matrix"):
            with self.subTest(stem=stem):
                self.assertNotIn(f"{stem}.gif", readme)
                self.assertNotIn(f"{stem}.png", readme)
                self.assertFalse((ROOT / "outputs" / f"{stem}.gif").exists())
                self.assertFalse((ROOT / "outputs" / f"{stem}.png").exists())


class VisualizationQualityTests(unittest.TestCase):
    def test_all_visualizations_share_stable_dimensions(self):
        for stem in VisualizationOutputTests.EXPECTED_STEMS:
            with self.subTest(stem=stem, kind="png"):
                with Image.open(ROOT / "outputs" / f"{stem}.png") as image:
                    self.assertEqual(image.size, (1920, 1080))
            with self.subTest(stem=stem, kind="gif"):
                with Image.open(ROOT / "outputs" / f"{stem}.gif") as image:
                    self.assertEqual(image.size, (1280, 720))

    def test_static_frames_are_not_blank(self):
        for stem in VisualizationOutputTests.EXPECTED_STEMS:
            with self.subTest(stem=stem):
                with Image.open(ROOT / "outputs" / f"{stem}.png") as image:
                    pixels = np.asarray(image.convert("L"), dtype=float)
                self.assertGreater(float(pixels.std()), 5.0)

    def test_animations_contain_visible_motion(self):
        for stem in VisualizationOutputTests.EXPECTED_STEMS:
            with self.subTest(stem=stem):
                with Image.open(ROOT / "outputs" / f"{stem}.gif") as image:
                    self.assertGreaterEqual(image.n_frames, 2)
                    self.assertLessEqual(image.n_frames, 180)
                    image.seek(0)
                    first = np.asarray(image.convert("RGB"), dtype=np.int16)
                    image.seek(image.n_frames // 2)
                    middle = np.asarray(image.convert("RGB"), dtype=np.int16)
                mean_change = float(np.abs(middle - first).mean())
                self.assertGreater(mean_change, 0.05)


class DocumentationHardeningTests(unittest.TestCase):
    def test_claim_boundaries_are_explicit(self):
        text = (ROOT / "docs" / "claim-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("Pardon mathematics", text)
        self.assertIn("SSZ bridge", text)
        self.assertIn("weakest category controls", text)

    def test_source_to_code_traceability_mentions_every_visual_stem(self):
        text = (ROOT / "docs" / "source-to-code-traceability.md").read_text(encoding="utf-8")
        for stem in VisualizationOutputTests.EXPECTED_STEMS:
            with self.subTest(stem=stem):
                self.assertIn(stem, text)
        self.assertIn("meta-dashboard images are intentionally absent", text)

    def test_readme_links_hardening_docs(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/claim-boundaries.md", readme)
        self.assertIn("docs/source-to-code-traceability.md", readme)

    def test_relative_markdown_links_resolve(self):
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        markdown_files = list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md"))
        missing = []
        for markdown in markdown_files:
            for target in pattern.findall(markdown.read_text(encoding="utf-8")):
                target = target.strip().strip("<>")
                if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                relative = urllib.parse.unquote(target.split("#", 1)[0])
                if relative and not (markdown.parent / relative).resolve().exists():
                    missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual(missing, [])


class HamiltonianDriftTests(unittest.TestCase):
    def test_drift_report_outputs_exist_and_are_nontrivial(self):
        csv_path = ROOT / "data" / "hamiltonian_drift_report.csv"
        md_path = ROOT / "docs" / "hamiltonian-drift-report.md"
        self.assertTrue(csv_path.is_file())
        self.assertTrue(md_path.is_file())
        with csv_path.open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual({row["method"] for row in rows}, {"explicit_euler", "rk4", "symplectic_euler", "leapfrog"})
        drift = {row["method"]: float(row["absolute_drift"]) for row in rows}
        self.assertGreater(drift["explicit_euler"], drift["leapfrog"] * 100.0)

    def test_observable_routing_export_matches_routes(self):
        data = json.loads((ROOT / "data" / "observable_routing_matrix.json").read_text(encoding="utf-8"))
        self.assertEqual(data["count"], len(ROUTES))
        methods = {row["observable"]: row["method"] for row in data["routes"]}
        self.assertEqual(methods["lensing"], "PPN (1+gamma)")
        self.assertEqual(methods["redshift"], "Xi/D direct")


class TestValidationReportTests(unittest.TestCase):
    def test_report_is_machine_readable_and_bounded(self):
        data = json.loads((ROOT / "data" / "test_validation_report.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(data["summary"]["total"], 49)
        self.assertIn("internal implementation consistency", data["claim_boundary"])
        self.assertIn("Mathematical invariants", data["layers"])

    def test_report_covers_every_discovered_test_class(self):
        data = json.loads((ROOT / "data" / "test_validation_report.json").read_text(encoding="utf-8"))
        classes = {row["class"] for row in data["tests"]}
        self.assertIn("SymplecticTests", classes)
        self.assertIn("RegimeGuardrailTests", classes)
        self.assertIn("VisualizationOutputTests", classes)


if __name__ == "__main__":
    unittest.main()
