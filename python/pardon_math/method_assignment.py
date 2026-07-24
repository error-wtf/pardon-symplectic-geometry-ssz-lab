from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservableRoute:
    observable: str
    method: str
    domain: str
    guardrail: str
    claim_boundary: str


ROUTES = {
    "clock": ObservableRoute("clock", "Xi/D direct", "timelike local clock comparison", "do not reuse this route for null-ray lensing or Shapiro delay", "toy bridge to SSZ clock formulas, not a proof of the physical model"),
    "redshift": ObservableRoute("redshift", "Xi/D direct", "timelike frequency ratio", "source/observer convention must be stated", "derived identity inside the simplified bridge module"),
    "time_dilation": ObservableRoute("time_dilation", "Xi/D direct", "timelike proper-time comparison", "no photon proper-time interpretation", "derived identity inside the simplified bridge module"),
    "frequency_shift": ObservableRoute("frequency_shift", "Xi/D direct", "timelike frequency comparison", "closed static products telescope unless dynamics/non-sphericity is present", "methodological bridge only"),
    "gps": ObservableRoute("gps", "Xi/D direct plus operational frame corrections", "timelike clock network", "do not collapse real GPS modelling to a single scalar", "routing sanity check only"),
    "pound_rebka": ObservableRoute("pound_rebka", "Xi/D direct", "laboratory gravitational redshift", "keep height/weak-field approximation explicit", "routing sanity check only"),
    "lensing": ObservableRoute("lensing", "PPN (1+gamma)", "null ray observable", "Xi-only is temporal contribution only; spatial curvature completion is required", "methodological bridge only"),
    "shapiro": ObservableRoute("shapiro", "PPN (1+gamma)", "null delay observable", "Xi-only route is incomplete for full delay; spatial curvature contribution is required", "methodological bridge only"),
    "vlbi": ObservableRoute("vlbi", "PPN (1+gamma)", "null timing/angle observable", "requires spatial contribution and measurement geometry", "methodological bridge only"),
    "null": ObservableRoute("null", "PPN (1+gamma)", "generic null observable", "must not be evaluated with a timelike-only shortcut", "methodological bridge only"),
    "orbit": ObservableRoute("orbit", "PPN beta/gamma or Hamiltonian orbit machinery", "timelike trajectory", "check energy/angular-momentum drift and regime domain", "toy validation pattern only"),
    "precession": ObservableRoute("precession", "PPN beta/gamma", "timelike orbital correction", "do not infer from a static redshift formula alone", "methodological bridge only"),
    "frame_dragging": ObservableRoute("frame_dragging", "PPN beta/gamma", "rotating-source orbital observable", "requires spin/metric data beyond scalar Xi", "methodological bridge only"),
    "geodesic": ObservableRoute("geodesic", "Lagrange/Hamilton geodesic equations", "phase-space trajectory", "validate invariants before interpreting coordinate plots", "toy validation pattern only"),
    "holonomy_static": ObservableRoute("holonomy_static", "static telescoping identity", "closed static frequency product", "closed product should return 1 in the static toy model", "sanity check, not a physical anomaly"),
    "holonomy_dynamic": ObservableRoute("holonomy_dynamic", "dynamic loop diagnostic", "time-dependent or non-spherical loop", "only deviations with stated dynamics are physically interesting", "illustrative diagnostic only"),
}

METHODS = {key: value.method for key, value in ROUTES.items()}

ALIASES = {
    "shapiro_delay": "shapiro",
    "vlbi_delay": "vlbi",
    "perihelion_precession": "precession",
    "hamiltonian_orbit": "orbit",
}


def normalize_observable(observable: str) -> str:
    key = observable.lower().strip().replace("-", "_").replace(" ", "_")
    return ALIASES.get(key, key)


def route_observable(observable: str) -> ObservableRoute:
    key = normalize_observable(observable)
    if key not in ROUTES:
        raise KeyError(f"unknown observable class: {observable}")
    return ROUTES[key]


def assign_method(observable: str) -> str:
    return route_observable(observable).method
