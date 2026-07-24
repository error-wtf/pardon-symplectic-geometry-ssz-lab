from __future__ import annotations

import numpy as np


def curve_a(n: int = 500) -> np.ndarray:
    x = np.linspace(0, 1, n)
    y = 0.5 + 0.18 * np.sin(2 * np.pi * x)
    return np.column_stack([x, y % 1])


def curve_b(phase: float, n: int = 500) -> np.ndarray:
    x = np.linspace(0, 1, n)
    y = (x + phase) % 1
    return np.column_stack([x, y])


def nearest_intersections(a: np.ndarray, b: np.ndarray, threshold: float = 0.015) -> np.ndarray:
    hits: list[np.ndarray] = []
    for point in a[::3]:
        distances = np.linalg.norm(b - point, axis=1)
        if distances.min() < threshold:
            hits.append(point)
    if not hits:
        return np.empty((0, 2))
    return np.unique(np.round(np.array(hits), 2), axis=0)
