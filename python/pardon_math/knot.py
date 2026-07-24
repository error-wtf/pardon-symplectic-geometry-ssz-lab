from __future__ import annotations

import numpy as np


def trefoil(n: int = 360) -> np.ndarray:
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    points = np.column_stack([x, y, z])
    points -= points.mean(axis=0)
    points /= np.max(np.linalg.norm(points, axis=1))
    return points


def cumulative_lengths(points: np.ndarray) -> tuple[np.ndarray, float]:
    closed = np.vstack([points, points[0]])
    edges = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    cumulative = np.concatenate([[0.0], np.cumsum(edges)])
    return cumulative[:-1], float(cumulative[-1])


def distortion_sample(points: np.ndarray) -> tuple[float, int, int]:
    cumulative, total = cumulative_lengths(points)
    best = (0.0, 0, 1)
    n = len(points)
    for i in range(n):
        for j in range(i + 2, n):
            chord = float(np.linalg.norm(points[i] - points[j]))
            if chord < 1e-9:
                continue
            along = abs(cumulative[j] - cumulative[i])
            intrinsic = min(along, total - along)
            ratio = intrinsic / chord
            if ratio > best[0]:
                best = (float(ratio), i, j)
    return best
