import numpy as np

from numba import njit


# TriDiagonal Matrix Algorithm
@njit(fastmath=True)
def TDMAsolver(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    n = len(d)
    a_copy: np.ndarray = a.copy()
    b_copy: np.ndarray = b.copy()
    c_copy: np.ndarray = c.copy()
    d_copy: np.ndarray = d.copy()

    for it in range(1, n):
        xi = a_copy[it - 1] / b_copy[it - 1]
        b_copy[it] -= xi * c_copy[it - 1]
        d_copy[it] -= xi * d_copy[it - 1]

    w: np.ndarray = np.zeros(n, dtype=d.dtype)
    w[-1] = d_copy[-1] / b_copy[-1]

    for il in range(n - 2, -1, -1):
        w[il] = (d_copy[il] - c_copy[il] * w[il + 1]) / b_copy[il]

    return w
