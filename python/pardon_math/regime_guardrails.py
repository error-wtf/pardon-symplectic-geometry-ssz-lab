from __future__ import annotations

from dataclasses import dataclass

from .ssz_bridge import BLEND_END, BLEND_START, PHOTON_SPHERE_END, STRONG_CONTEXT_END


@dataclass(frozen=True)
class RegimeRoute:
    x: float
    physical_regime: str
    formula_domain: str
    guardrail: str


FORBIDDEN_FORMULAS = {
    "rs_over_r_minus_rs",
    "xi_rs_over_r_minus_rs",
    "quadratic_exponential",
    "universal_xi_only_null",
    "single_method_for_all_observables",
}


def physical_regime(x: float) -> str:
    value = float(x)
    if value <= 0.0:
        raise ValueError("x = r/r_s must be positive")
    if value < BLEND_START:
        return "very_close/g2_context"
    if value <= BLEND_END:
        return "transition_blend"
    if value <= PHOTON_SPHERE_END:
        return "photon_sphere_context"
    if value <= STRONG_CONTEXT_END:
        return "strong_context/g1_formula"
    return "weak_field"


def formula_domain(x: float) -> str:
    value = float(x)
    if value <= 0.0:
        raise ValueError("x = r/r_s must be positive")
    if value < BLEND_START:
        return "g2_saturation"
    if value <= BLEND_END:
        return "c2_smootherstep_blend"
    return "g1_weak_branch"


def guardrail_for(x: float) -> str:
    regime = physical_regime(x)
    domain = formula_domain(x)
    if "photon_sphere" in regime:
        return "physical regime is photon-sphere context, but operative Xi formula is still g1 branch"
    return f"physical regime {regime}; operative formula domain {domain}"


def route_regime(x: float) -> RegimeRoute:
    return RegimeRoute(
        x=float(x),
        physical_regime=physical_regime(x),
        formula_domain=formula_domain(x),
        guardrail=guardrail_for(x),
    )


def assert_formula_allowed(formula_id: str) -> None:
    key = formula_id.lower().strip().replace("-", "_").replace(" ", "_")
    if key in FORBIDDEN_FORMULAS:
        raise ValueError(f"forbidden or deprecated formula route: {formula_id}")
