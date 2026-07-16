from typing import Optional

def is_prime(n: int):
    if n < 1:
        raise ValueError("n must be at least 1")
    elif n == 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    else:
        for i in range(3, int(math.sqrt(n))+1):
            if n % i == 0:
                return False
        return True
    
def sieve(n: int):
    is_prime = [True]*(n+1)
    primes = []
    for p in range(2, n+1):
        if is_prime[p]:
            primes.append(p)
            for v in range(p*p, n+1, p):
                is_prime[v] = False
    return is_prime, primes

def consecutive_prime_sum(n: int) -> Optional[int]:
    is_prime, primes = sieve(n)
    longest_sum = 0
    longest_sum_prime = None
    pref_sums = [0]*(len(primes)+1)
    # go through every prefix sum (pairs of start and end primes), sum should be prime
    for i in range(1, len(pref_sums)):
        pref_sums[i] = pref_sums[i-1] + primes[i-1]

    for start in range(len(primes)):
        for end in range(start+longest_sum+1, len(primes)+1):
            s = pref_sums[end]-pref_sums[start]
            if s >= n:
                break
            if is_prime[s]:
                longest_sum = end-start
                longest_sum_prime = s
    return longest_sum_prime
