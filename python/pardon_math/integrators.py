from __future__ import annotations

import numpy as np


def harmonic_energy(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    return 0.5 * (q * q + p * p)


def explicit_euler(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    traj = np.zeros((steps + 1, 2), dtype=float)
    traj[0] = [q0, p0]
    q, p = q0, p0
    for k in range(1, steps + 1):
        q_new = q + dt * p
        p_new = p - dt * q
        q, p = q_new, p_new
        traj[k] = [q, p]
    return traj


def symplectic_euler(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    traj = np.zeros((steps + 1, 2), dtype=float)
    traj[0] = [q0, p0]
    q, p = q0, p0
    for k in range(1, steps + 1):
        p = p - dt * q
        q = q + dt * p
        traj[k] = [q, p]
    return traj


def leapfrog(q0: float, p0: float, dt: float, steps: int) -> np.ndarray:
    traj = np.zeros((steps + 1, 2), dtype=float)
    traj[0] = [q0, p0]
    q, p = q0, p0
    for k in range(1, steps + 1):
        p_half = p - 0.5 * dt * q
        q = q + dt * p_half
        p = p_half - 0.5 * dt * q
        traj[k] = [q, p]
    return traj
