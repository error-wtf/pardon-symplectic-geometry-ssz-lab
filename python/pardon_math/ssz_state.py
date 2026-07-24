from __future__ import annotations

import numpy as np

from .ssz_bridge import (
    BLEND_END,
    BLEND_START,
    PHI,
    PHOTON_SPHERE_END,
    STRONG_CONTEXT_END,
    D_factor,
    scale_factor,
    xi_canonical,
)


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
    if x < BLEND_START:
        return "g2/very_close"
    if x <= BLEND_END:
        return "blend"
    if x <= PHOTON_SPHERE_END:
        return "photon_sphere"
    if x <= STRONG_CONTEXT_END:
        return "strong_context/g1_formula"
    return "weak"
