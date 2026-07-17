from Algorithms.numerical_methods.euler.p50 import consecutive_prime_sum, sieve


def test_sieve_marks_zero_and_one_as_non_prime():
    is_prime, primes = sieve(10)
    assert is_prime[0] is False
    assert is_prime[1] is False
    assert primes == [2, 3, 5, 7]


def test_sol():
    assert consecutive_prime_sum(n=1_000_000) == 997651

