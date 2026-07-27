# utils.py


def sieve(n: int):
    is_prime = [True] * (n + 1)
    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False
    primes = []
    for p in range(2, n + 1):
        if is_prime[p]:
            primes.append(p)
            for v in range(p * p, n + 1, p):
                is_prime[v] = False
    return is_prime, primes
