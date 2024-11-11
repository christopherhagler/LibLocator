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

def p2(beta, use_extrapolation=False):
    """
    Compute the value of the series 
        sum_{k=0}^(infty) ((-1)^k /(2k + 1)^{beta})

    @param beta: a real value for the parameter beta on (0, 1]
    @param use_extrapolation: optional boolean to indicate if convergence acceleration should be used

    @return: the value of the series.
    """
    max_terms = 1000000  # Increased number of terms for better accuracy
    tolerance = 1e-12
    s = 0.0
    k = 0
    terms = []
    sums = []
    
    while k < max_terms:
        term = (-1) ** k / (2 * k + 1) ** beta
        s += term
        terms.append(term)
        sums.append(s)
        k += 1

        # Check for convergence
        if abs(term) < tolerance:
            break

    if use_extrapolation and len(sums) >= 3:
        # Apply Shanks transformation for convergence acceleration
        n = len(sums)
        s_n2, s_n1, s_n = sums[-3], sums[-2], sums[-1]
        d1 = s_n2 - s_n1
        d2 = s_n1 - s_n
        if d2 != 0:
            s_extrapolated = s_n2 - (d1 ** 2) / (d2)
            return s_extrapolated
        else:
            return s_n
    else:
        return s

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
