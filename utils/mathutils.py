import numpy as np
from scipy.differentiate import derivative

def vec2tilde(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

def tilde2vec(tilde):
    return np.array([tilde[2, 1], tilde[0, 2], tilde[1, 0]])

def matrix_derivative(f, x, shape, args=(), **kwargs):
    """Call SciPy's derivative() routine with a scalar-to-matrix function
    
    This function extend's SciPy's derivative() function to handle
    functions f: R -> R^mxn. The call signature is identical to that
    of derivative(), with the exception that following the evaluation point
    x, the shape of the output (m, n) must also be specified. This function
    returns only the df field of derivative().

    Parameters
    ----------
    shape :  tuple of int
        Shape of output structure of f, in format (rows, columns).

    Notes
    -----
    See https://docs.scipy.org/doc/scipy/reference/generated/scipy.differentiate.derivative.html
    for full documenation of derivative() routine.

    :Authors:
        Erick White <erick.white@colorado.edu>
    """
    f_args = lambda x: f(x, args)
    f_element = lambda x, i, j: f_args(x)[i, j]

    dfdx = np.empty((shape[0], shape[1]))

    for i in range(shape[0]):
        for j in range(shape[1]):
            dfdx[i, j] = derivative(np.vectorize(f_element, signature='(),(),()->()'), x, args=(i, j), **kwargs).df

    return dfdx

import numpy as np

def RK4_step(t, h, X, eval_f, **kwargs):
    tj = t + h
    k1 = h * eval_f(tj, X, **kwargs)
    k2 = h * eval_f(tj + h / 2, X + 0.5 * k1, **kwargs)
    k3 = h * eval_f(tj + h / 2, X + 1 / 2 * k2, **kwargs)
    k4 = h * eval_f(tj + h, X + k3, **kwargs)

    Xj = X + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    return tj, Xj