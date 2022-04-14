import numpy as np


def solve(func, y0, x, h=None):
    if not h:
        h = x[1] - x[0]
    y = np.zeros((len(x), len(y0)))
    y[0, :] = y0
    M = np.zeros(len(x))
    F = np.zeros(len(x))
    for i, t in enumerate(x):
        dydt, m, f = func(y[i, :], t)
        if t != x[-1]:
            y[i + 1, :] = y[i, :] + np.array(dydt) * h
        M[i] = m
        F[i] = f

    return y, M, F
