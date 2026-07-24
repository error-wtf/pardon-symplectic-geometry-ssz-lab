from __future__ import annotations

METHODS = {
    "clock": "Xi/D direct",
    "redshift": "Xi/D direct",
    "time_dilation": "Xi/D direct",
    "lensing": "PPN (1+gamma)",
    "shapiro": "PPN (1+gamma)",
    "null": "PPN (1+gamma)",
    "orbit": "PPN beta/gamma or Hamiltonian orbit machinery",
    "precession": "PPN beta/gamma",
    "geodesic": "Lagrange/Hamilton geodesic equations",
}


def assign_method(observable: str) -> str:
    key = observable.lower().strip()
    if key not in METHODS:
        raise KeyError(f"unknown observable class: {observable}")
    return METHODS[key]
