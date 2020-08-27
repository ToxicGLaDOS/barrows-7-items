import math
from decimal import Decimal


def choose(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n - r)


def p(N):
    return 1 / Decimal(450 - 58 * N)

def cdf(k, N=6, super_precise=False):
    value = sum([choose(N + 1, i) * p(N) ** i * (1 - p(N)) ** (N + 1 - i) for i in range(math.floor(k + 1))])
    if super_precise:
        return value
    else:
        return float(value)


def inverse_cdf(k, N=6, super_precise=False):
    return 1 - cdf(k, N, super_precise=super_precise)