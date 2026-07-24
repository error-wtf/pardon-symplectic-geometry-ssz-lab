from __future__ import annotations

import numpy as np


def cauchy_riemann_residual(epsilon: float, grid_n: int = 120) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    s = np.linspace(-1.2, 1.2, grid_n)
    t = np.linspace(-1.2, 1.2, grid_n)
    S, T = np.meshgrid(s, t, indexing="xy")
    x = S**2 - T**2 + epsilon * S
    y = 2 * S * T - epsilon * T
    ds = s[1] - s[0]
    dt = t[1] - t[0]
    x_t, x_s = np.gradient(x, dt, ds)
    y_t, y_s = np.gradient(y, dt, ds)
    residual = np.sqrt((x_s - y_t) ** 2 + (x_t + y_s) ** 2)
    return S, T, residual
