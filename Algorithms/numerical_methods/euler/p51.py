from Algorithms.numerical_methods.euler import utils
from typing import Optional
from itertools import combinations

def prime_digit_replacements(n: int, prime_family: int, start_point: Optional[int] = None) -> Optional[int]:
    """
    n: int 
    prime_family: int
    return: Smallest prime that has a prime family of size `prime_family`
    """
    is_prime, primes = utils.sieve(n)
    nums = '0123456789'
    for p in primes:
        if start_point is not None and p < start_point:
            continue
        s = str(p)
        for digit in nums:
            positions = [i for i, c in enumerate(s) if c == digit]

            if not positions:
                continue
            for r in range(1, len(positions)+1):
                for subset in combinations(positions, r):
                    if subset[-1] == n-1:
                        continue
                    count = 0
                    smallest = None
                    for replacement in nums:
                        if subset[0] == 0 and replacement == "0":
                            continue
                        updated = list(s)
                        for i in subset:
                            updated[i] = replacement

                        candidate = int(''.join(updated))
                        if is_prime[candidate]:
                            count += 1
                            if smallest is None or candidate < smallest:
                                smallest = candidate
                    if count == prime_family:
                        return smallest
    return None
