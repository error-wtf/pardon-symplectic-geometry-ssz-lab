from __future__ import annotations

import numpy as np

from .ssz_bridge import D_factor


def triple_clock_product(radii: tuple[float, float, float]) -> float:
    a, b, c = radii
    return float((D_factor(a) / D_factor(b)) * (D_factor(b) / D_factor(c)) * (D_factor(c) / D_factor(a)))


def dynamic_loop_deviation(t: np.ndarray, amplitude: float = 0.03) -> np.ndarray:
    """Toy non-static holonomy deviation; not a physical SSZ prediction."""
    return 1.0 + amplitude * np.sin(t) * np.cos(2 * t)
