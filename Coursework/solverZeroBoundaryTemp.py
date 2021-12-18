from numba.np.ufunc import parallel
import numpy as np
from typing import Tuple

from tdma import TDMAsolver
from numba import njit, prange


def get_solution_matrix(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    A = np.zeros((d.shape[0], b.shape[0]), dtype=np.float32)
    b_indexes = np.diag_indices_from(A)
    a_indexes = (b_indexes[0][:-1], b_indexes[0][1:])
    c_indexes = (b_indexes[0][1:], b_indexes[0][:-1])
    A[b_indexes] = b
    A[a_indexes] = c
    A[c_indexes] = a
    return A


@njit(fastmath=True, parallel=True)
def solve_heat1d(a: np.ndarray, b: np.ndarray, c: np.ndarray, grid: np.ndarray, R: float) -> np.ndarray:
    solutions = np.zeros((grid.shape[0], grid.shape[1]), dtype=np.float32)

    # for i, vals in enumerate(grid):
    for i in prange(grid.shape[0]):
        vals = grid[i]
        d: np.ndarray = R * np.roll(vals, 1) + R * np.roll(vals, -1) + (1.0 - 2.0 * R) * vals

        solution = TDMAsolver(a, b, c, d)

        # the boundary temperature is zero
        solution[0] = solution[-1] = 0.0
        solutions[i] = solution
    return solutions


@njit(fastmath=True, parallel=True)
def set_initial_temperature_distribution(x: np.ndarray, y: np.ndarray, u: np.ndarray):
    for i in prange(x.shape[0]):
        for j in prange(y.shape[0]):
            u0 = (1 - x[i] ** 2 / x[-1] ** 2) * (1 - y[j] ** 2 / y[-1] ** 2)
            u[0][i, j] = u0


@njit(fastmath=True)
def solve_heat2d(x: np.ndarray, y: np.ndarray, time: np.ndarray, sigma: float) -> Tuple[np.ndarray, np.ndarray]:
    dx = x[1] - x[0]
    dt = time[1] - time[0]

    u: np.ndarray = np.zeros((time.shape[0], x.shape[0], y.shape[0]), dtype=np.float32)

    # initial temperature distribution:
    set_initial_temperature_distribution(x, y, u)

    # temperature at centre of the square:
    center_temperature: np.ndarray = np.zeros(time.shape[0], dtype=np.float32)
    center_temperature[0] = u[0][x.size // 2, y.size // 2]

    R: float = sigma * dt / (2.0 * dx ** 2)  # for matrix diagonals
    a: np.ndarray = np.full((x.shape[0] - 1), -R, dtype=np.float32)
    b: np.ndarray = np.full(x.shape[0], 1.0 + 2.0 * R, dtype=np.float32)
    c: np.ndarray = a.copy()
    a[0] = c[-1] = 0.0

    for i in range(0, time.shape[0] - 1):
        x_derivative: np.ndarray = solve_heat1d(a, b, c, u[i], R)
        u[i + 1] = solve_heat1d(a, b, c, x_derivative, R)
        center_temperature[i + 1] = u[i + 1][x.size // 2, y.size // 2]

    return u, center_temperature
