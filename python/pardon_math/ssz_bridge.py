from __future__ import annotations

import numpy as np

PHI = (1.0 + np.sqrt(5.0)) / 2.0
XI_MAX = 1.0 - np.exp(-PHI)
D_MIN_AT_RS = 1.0 / (1.0 + XI_MAX)
BLEND_START = 1.8
BLEND_END = 2.2
PHOTON_SPHERE_END = 3.0
STRONG_CONTEXT_END = 10.0
SSZ_PROFILE = "local_saturation_c2_blend_v1"


def smootherstep(t: np.ndarray | float) -> np.ndarray | float:
    arr = np.asarray(t)
    return arr**3 * (arr * (arr * 6 - 15) + 10)


def xi_weak(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (2.0 * np.asarray(x))


def xi_strong(x: np.ndarray | float) -> np.ndarray | float:
    """Local saturation-profile g2 form: min(1-exp(-phi*x), Xi_max)."""
    arr = np.asarray(x, dtype=float)
    result = np.minimum(1.0 - np.exp(-PHI * arr), XI_MAX)
    if np.isscalar(x):
        return float(result)
    return result


def xi_decay(x: np.ndarray | float) -> np.ndarray | float:
    """Complementary decay profile documented by SSZ; not operative in this lab."""
    arr = np.asarray(x, dtype=float)
    if np.any(arr <= 0.0):
        raise ValueError("x = r/r_s must be positive")
    result = 1.0 - np.exp(-PHI / arr)
    if np.isscalar(x):
        return float(result)
    return result


def xi_canonical(x: np.ndarray | float) -> np.ndarray | float:
    """Evaluate the fixed ``local_saturation_c2_blend_v1`` lab profile."""
    arr = np.asarray(x, dtype=float)
    if np.any(arr <= 0.0):
        raise ValueError("x = r/r_s must be positive")
    strong = xi_strong(arr)
    weak = xi_weak(arr)
    t = np.clip((arr - BLEND_START) / (BLEND_END - BLEND_START), 0.0, 1.0)
    blend = (1.0 - smootherstep(t)) * xi_strong(arr) + smootherstep(t) * xi_weak(arr)
    result = np.where(arr < BLEND_START, strong, np.where(arr > BLEND_END, weak, blend))
    if np.isscalar(x):
        return float(result)
    return result


def D_factor(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / (1.0 + xi_canonical(x))


def scale_factor(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 + xi_canonical(x)


def effective_potential(x: np.ndarray | float, ell: float = 2.0, epsilon: float = 1.0) -> np.ndarray | float:
    x_arr = np.asarray(x, dtype=float)
    return D_factor(x_arr) ** 2 * (epsilon + ell**2 / x_arr**2)


def hamiltonian_radial(q: np.ndarray | float, p: np.ndarray | float, ell: float = 2.0) -> np.ndarray | float:
    return 0.5 * np.asarray(p) ** 2 + effective_potential(np.asarray(q), ell=ell)
