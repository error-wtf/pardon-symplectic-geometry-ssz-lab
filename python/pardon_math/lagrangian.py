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
    """Return separated intersection candidates for two sampled torus graphs.

    The curves are compared with periodic distance in the y-coordinate. Local
    minima are retained so a dense cluster around one crossing counts once.
    """
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != 2 or b.shape[1] != 2:
        raise ValueError("curves must have shape (n, 2)")
    order_a = np.argsort(a[:, 0])
    order_b = np.argsort(b[:, 0])
    sampled = a[order_a]
    b_sorted = b[order_b]
    b_y = np.interp(sampled[:, 0], b_sorted[:, 0], b_sorted[:, 1])
    signed = (sampled[:, 1] - b_y + 0.5) % 1.0 - 0.5
    distance = np.abs(signed)
    local_minimum = np.ones(len(distance), dtype=bool)
    local_minimum[1:-1] = (distance[1:-1] <= distance[:-2]) & (distance[1:-1] <= distance[2:])
    candidates = sampled[(distance < threshold) & local_minimum]
    if len(candidates) == 0:
        return np.empty((0, 2))

    separated: list[np.ndarray] = []
    minimum_spacing = max(2.0 * threshold, 0.025)
    for point in candidates:
        if not separated:
            separated.append(point)
            continue
        deltas = np.abs(np.asarray(separated) - point)
        torus_deltas = np.minimum(deltas, 1.0 - deltas)
        if np.all(np.linalg.norm(torus_deltas, axis=1) > minimum_spacing):
            separated.append(point)
    return np.asarray(separated)
