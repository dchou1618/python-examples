import time
import pytest
import functools
from Algorithms.datastructs.hash_table.cache import LRUCache, factorial

# -------------------------
# Correctness tests: LRUCache
# -------------------------

def test_basic_put_get():
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)

    assert cache.get(1) == 10
    assert cache.get(2) == 20
    assert cache.get(3) == -1


def test_eviction_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)

    # Access key 1 -> makes key 2 LRU
    assert cache.get(1) == 1

    # This should evict key 2
    cache.put(3, 3)

    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3


def test_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)

    cache.put(1, 100)  # update value + recency

    assert cache.get(1) == 100

    # key 2 should now be LRU
    cache.put(3, 3)

    assert cache.get(2) == -1
    assert cache.get(1) == 100
    assert cache.get(3) == 3


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)

    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_capacity_zero():
    cache = LRUCache(0)
    cache.put(1, 1)

    assert cache.get(1) == -1


def test_repeated_get_does_not_break_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)

    # Repeated gets
    assert cache.get(1) == 1
    assert cache.get(1) == 1

    cache.put(3, 3)

    # key 2 should still be evicted
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3


# -------------------------
# Timing tests: functools.lru_cache
# -------------------------

def uncached_factorial(n: int) -> int:
    return n * uncached_factorial(n - 1) if n > 1 else 1


def test_lru_cache_speedup():
    """
    This test checks that functools.lru_cache provides
    a measurable speedup over uncached recursion.

    We avoid flaky microbenchmarks by:
    - warming the cache
    - using multiple calls
    - asserting relative (order-of-magnitude) improvement
    """

    n = 300

    # Warm-up cached version
    factorial.cache_clear()
    factorial(n)

    # Measure cached calls
    start = time.perf_counter()
    for _ in range(1000):
        factorial(n)
    cached_time = time.perf_counter() - start

    # Measure uncached calls (much fewer iterations)
    start = time.perf_counter()
    for _ in range(10):
        uncached_factorial(n)
    uncached_time = time.perf_counter() - start

    # Cached should be significantly faster per call
    cached_per_call = cached_time / 1000
    uncached_per_call = uncached_time / 10

    assert cached_per_call < uncached_per_call / 50
