from typing import Optional
from Algorithms.numerical_methods.euler import utils


def consecutive_prime_sum(n: int) -> Optional[int]:
    is_prime, primes = utils.sieve(n)
    longest_sum = 0
    longest_sum_prime = None
    pref_sums = [0] * (len(primes) + 1)
    # go through every prefix sum (pairs of start and end primes), sum should be prime
    for i in range(1, len(pref_sums)):
        pref_sums[i] = pref_sums[i - 1] + primes[i - 1]

    for start in range(len(primes)):
        for end in range(start + longest_sum + 1, len(primes) + 1):
            s = pref_sums[end] - pref_sums[start]
            if s >= n:
                break
            if is_prime[s]:
                longest_sum = end - start
                longest_sum_prime = s
    return longest_sum_prime
