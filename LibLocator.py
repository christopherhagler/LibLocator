# Author: Christopher Hagler / cwh0020@auburn.edu
# Date: 2024-09-01
# Assignment Name: hw05

import numpy as np
import math

def p1(data, powers):
    """
    Implement Richardson extrapolation.

    Assume the expansion of 
    f(h) = f(0) + c_1 h^{alpha_1} + c_2 h^{alpha_2} + ... + c_n h^{alpha_n} + ...

    @param data: a list of values [f(2^(-1)), f(2^(-2)), ..., f(2^(-n))]
    @param powers: a list of powers [alpha_1, alpha_2, ..., alpha_{n-1}]

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
    @param use_extrapolation: optional boolean to indicate if Richardson extrapolation should be used

    @return: the value of the series.
    """
    max_iterations = 25  # Adjusted to ensure convergence
    tolerance = 1e-12
    data = []
    last_partial_sum = 0.0

    for n in range(1, max_iterations + 1):
        N = 2 ** n
        k = np.arange(N)
        terms = (-1) ** k / (2 * k + 1) ** beta
        partial_sum = np.sum(terms)
        if use_extrapolation:
            data.append(partial_sum)
        # Check for convergence
        if n > 1 and abs(partial_sum - last_partial_sum) < tolerance:
            break
        last_partial_sum = partial_sum

    if use_extrapolation and len(data) >= 2:
        # Use Richardson extrapolation on the series data
        powers = [1] * (len(data) - 1)
        return p1(data, powers)
    else:
        return last_partial_sum

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
        A[i, :] = [shift ** i / math.factorial(i) for shift in shifts]
    
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
        A[i, :] = [shift ** i / math.factorial(i) for shift in shifts]
    
    coefs = np.linalg.solve(A, b)
    return coefs


assert(abs(p1(  [2, 1],    [1]              )         ) < 1e-8)
assert(abs(p1(  [4, 2, 1], [1,2]            )         ) < 1e-8)
assert(abs(p1(  [1, 2, 4], [1,2]            ) - 7.0   ) < 1e-8)
assert(abs(p1(  [5, 4, 3], [1,3]            ) - 13/7  ) < 1e-8)
assert(abs(p1(  [5, 4, 3, 2, 1], [1,2,3,4]  ) + 19/35 ) < 1e-8)
assert(abs(p1(  [64, 8, 4, 1],   [1,2,3]    ) + 16/3  ) < 1e-8)

assert(abs ( p2(1)   - 0.7853981633974483) < 1e-6)
#assert(abs ( p2(0.8) - 0.7436078366584389) < 1e-6)
#assert(abs ( p2(0.5) - 0.6676914571896092) < 1e-6)
#assert(abs ( p2(0.2) - 0.5737108471859466) < 1e-6)

#assert(abs ( p3([-1, 0, 1]) - np.array([-0.5, 0, 0.5])) < 1e-8).all()
#assert(abs ( p3([-2, -1, 1]) - np.array([0, -0.5, 0.5])) < 1e-8).all()
#assert(abs ( p3([-2, -3, 6]) - np.array([3/8, -4/9, 5/72])) < 1e-8).all() 

print("Done!")
