import numpy as np

from numba import njit

@njit(fastmath=True)
def TDMAsolver(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    nf = len(d)
    ac: np.ndarray = a.copy()
    bc: np.ndarray = b.copy()
    cc: np.ndarray = c.copy()
    dc: np.ndarray = d.copy()

    for it in range(1, nf):
        mc = ac[it - 1] / bc[it - 1]
        bc[it] -= mc * cc[it - 1]
        dc[it] -= mc * dc[it - 1]

    xc: np.ndarray = np.zeros(nf, dtype=d.dtype)
    xc[-1] = dc[-1] / bc[-1]

    for il in range(nf - 2, -1, -1):
        xc[il] = (dc[il] - cc[il] * xc[il + 1]) / bc[il]

    return xc