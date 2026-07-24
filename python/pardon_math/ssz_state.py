from __future__ import annotations

import numpy as np

from .ssz_bridge import PHI, D_factor, scale_factor, xi_canonical


def phi_ladder(k_min: int = -3, k_max: int = 6) -> np.ndarray:
    k = np.arange(k_min, k_max + 1, dtype=float)
    return PHI**k


def state_vector(x: np.ndarray | float) -> dict[str, np.ndarray | float]:
    xi = xi_canonical(x)
    s = scale_factor(x)
    d = D_factor(x)
    n_eff = 4.0 * np.asarray(s)
    nu = np.log(np.asarray(s)) / np.log(PHI)
    if np.isscalar(x):
        return {"x": float(x), "Xi": float(xi), "s": float(s), "D": float(d), "N_eff": float(n_eff), "nu": float(nu)}
    return {"x": np.asarray(x), "Xi": xi, "s": s, "D": d, "N_eff": n_eff, "nu": nu}


def regime_label(x: float) -> str:
    if x < 1.8:
        return "g2/very_close"
    if x <= 2.2:
        return "blend"
    if x <= 3.0:
        return "photon_sphere"
    if x <= 10.0:
        return "strong_context/g1_formula"
    return "weak"
