import time
from typing import Callable


class BenchmarkMixin:
    def benchmark(self, fn: Callable, *args, **kwargs):
        start = time.perf_counter()

        result = fn(*args, **kwargs)

        elapsed = time.perf_counter() - start

        return {
            "result": result,
            "elapsed_seconds": elapsed,
        }