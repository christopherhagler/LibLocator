# Author: Christopher Hagler / cwh0020@auburn.edu
# Date: 2024-09-01
# Assignment Name: hw05

import numpy as np

def p1(data, powers):
    """
    Implement Richardson extrapolation.

    Assume the expansion of 
    f(h) = f(0) + c_1 h^{alpha_1} + c_2 h^{alpha_2} + ... + c_n h^{alpha_n} + ...

    @param data: a list of values [f(2^(-1)), f(2^(-2)), ..., f(2^(-n))]
    @param powers: a list of powers [alpha_1, alpha_2, ..., alpha_{n-1]]

    @return: the extrapolated value of f(0) using Richardson extrapolation
    """
    n = len(data)
    table = np.zeros((n, n))
    table[:, 0] = data

    for j in range(1, n):
        k = 2  # Since h is being halved each time
        for i in range(n - j):
            factor = k ** powers[j - 1]
            table[i, j] = (factor * table[i + 1, j - 1] - table[i, j - 1]) / (factor - 1)
    
    return table[0, n - 1]

def compute_A_beta(beta, m=10):
    """
    Computes A(beta) using Richardson extrapolation.

    Parameters:
    beta (float): The exponent in the series, where 0 < beta <= 1.
    m (int): Number of data points for extrapolation (should not exceed 15).

    Returns:
    A_beta (float): The extrapolated value of the series A(beta).
    """
    # Initialize arrays
    ak = np.zeros(m)
    hk = np.zeros(m)
    
    for k in range(1, m + 1):
        h_k = 2 ** (-k)
        N = int(1 / h_k)
        hk[k - 1] = h_k
        
        # Compute partial sum up to N
        i = np.arange(N + 1)
        terms = (-1) ** i / (2 * i + 1) ** beta
        ak[k - 1] = np.sum(terms)
    
    # Build the matrix H for least squares
    n_terms = m  # Number of terms in the model
    H = np.zeros((m, n_terms))
    H[:, 0] = 1  # First column is ones for A(beta)
    for j in range(1, n_terms):
        H[:, j] = hk ** (beta + j - 1)
    
    # Solve the least squares problem
    # Y = H * C, where Y = ak, C = [A_beta, c1, c2, ..., c_{n_terms-1}]
    C, residuals, rank, s = np.linalg.lstsq(H, ak, rcond=None)
    A_beta = C[0]
    return A_beta

def p3(shifts):
    """
    Compute the coefficients of the finite difference scheme for f'(x)
    using the formula

    f'(x) ≈ (1/h) * (c_0 f(x_0) + c_1 f(x_1) + ... + c_n f(x_n)) + O(h^n)

    @param shifts: a list of real values (a_0, a_1, ..., a_n), the nodes are x_i = x + a_i * h

    @return: coefs: a numpy array of coefficients (c_0, c_1, ..., c_n)
    """
    n = len(shifts)
    A = np.zeros((n, n))
    b = np.zeros(n)
    b[1] = 1  # Coefficient for the first derivative

    for i in range(n):
        A[i, :] = [shift ** i / np.math.factorial(i) for shift in shifts]
    
    coefs = np.linalg.solve(A, b)
    return coefs

def p4(shifts, l):
    """
    Compute the coefficients of the finite difference scheme for f^{(l)}(x)
    using the formula

    f^{(l)}(x) ≈ (1/h^l) * (c_0 f(x_0) + c_1 f(x_1) + ... + c_n f(x_n)) + O(h^{n + 1 - l})

    @param shifts: a list of real values (a_0, a_1, ..., a_n), the nodes are x_i = x + a_i * h
    @param l: an integer n > l >= 1, the order of the derivative

    @return: coefs: a numpy array of coefficients (c_0, c_1, ..., c_n)
    """
    n = len(shifts)
    if l >= n:
        raise ValueError("Order of derivative l must be less than the number of shifts n.")
    A = np.zeros((n, n))
    b = np.zeros(n)
    b[l] = np.math.factorial(l)

    for i in range(n):
        A[i, :] = [shift ** i / np.math.factorial(i) for shift in shifts]
    
    coefs = np.linalg.solve(A, b)
    return coefs
