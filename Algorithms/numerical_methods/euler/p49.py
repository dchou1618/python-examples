from collections import defaultdict
import math


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
        for i in range(3, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True


def sieve_n_digit_primes(n: int):
    if n < 1:
        return []

    low = 10 ** (n - 1)
    high = 10**n - 1

    if n == 1:
        low = 2

    limit = math.isqrt(high)
    is_prime = [True] * (limit + 1)
    base_primes = []

    # sieve base primes
    for p in range(2, limit + 1):
        if is_prime[p]:
            base_primes.append(p)
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False

    # Segment the range [low, high] into cache-friendly block sizes
    # 32KB to 256KB block size prevents CPU cache thrashing
    block_size = 500000
    n_digit_primes = []

    for current_low in range(low, high + 1, block_size):
        current_high = min(current_low + block_size - 1, high)
        range_size = current_high - current_low + 1

        segment = [True] * range_size

        for p in base_primes:
            # Find the first multiple of p >= current_low and >= p^2
            start_multiple = max(p * p, ((current_low + p - 1) // p) * p)

            for j in range(start_multiple, current_high + 1, p):
                segment[j - current_low] = False

        for i in range(range_size):
            if segment[i]:
                n_digit_primes.append(current_low + i)

    return n_digit_primes


def prime_permutations(n: int, perms: int) -> str:
    """
    n: number of digits in the prime permutations
    end in odd
    perms: number of permutations to consider
    _ _ _ 1,3,5,7,9
    """
    all_primes = sieve_n_digit_primes(n)
    table = defaultdict(list)
    for prime in all_primes:
        key = "".join(sorted(str(prime)))
        table[key].append(prime)

    res = []
    for key, nums in table.items():
        if len(nums) < perms:
            continue
        nums_set = set(nums)
        for start in nums_set:
            for next_num in nums_set:
                if next_num <= start:
                    continue
                diff = next_num - start
                seq = [start]
                curr = start
                while curr in nums_set and len(seq) < perms:
                    curr += diff
                    if curr in nums_set:
                        seq.append(curr)
                    else:
                        break
                if len(seq) == perms:
                    res.append("".join([str(v) for v in seq]))
    return res
