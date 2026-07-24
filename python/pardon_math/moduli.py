from __future__ import annotations

import numpy as np


def circle_moduli_points(a: float, n: int = 300) -> np.ndarray:
    if a < 0:
        return np.empty((0, 2))
    if abs(a) < 1e-12:
        return np.array([[0.0, 0.0]])
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = np.sqrt(a)
    return np.column_stack([r * np.cos(theta), r * np.sin(theta)])


def solution_dimension_label(a: float) -> str:
    if a < 0:
        return "empty"
    if abs(a) < 1e-12:
        return "singular point"
    return "smooth circle"
