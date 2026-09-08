import numpy as np

from mixins.benchmark import BenchmarkMixin
from mixins.logging import LoggingMixin


def count_max_length_runs(length: int, rng=None):
    lst = np.random.randint(0, 2, length) if rng is None else rng.integers(0, 2, length)
    i = 1
    num_runs = 0
    curr_max = 0
    run = 1

    while i < length:
        if lst[i] == lst[i - 1]:
            run += 1
        else:
            # only update number of runs if run ends
            if run > curr_max:
                curr_max = run
                num_runs = 1
            elif run == curr_max:
                num_runs += 1
            run = 1
        i += 1
    if run > curr_max:
        curr_max = run
        num_runs = 1
    elif run == curr_max:
        num_runs += 1
    return num_runs


def count_num_runs(length: int, rng=None):
    lst = np.random.randint(0, 2, length) if rng is None else rng.integers(0, 2, length)
    runs = 1
    for i in range(1, length):
        if lst[i] != lst[i - 1]:
            runs += 1
    return runs


class CoinRunSimulation(BenchmarkMixin, LoggingMixin):
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def simulate(self, steps: int, length: int = 100):
        if steps < 0:
            raise ValueError("steps must be non-negative")
        if length < 1:
            raise ValueError("length must be positive")

        results = []
        for step in range(steps):
            result = {
                "step": step,
                "max_length_runs": count_max_length_runs(length, self.rng),
                "num_runs": count_num_runs(length, self.rng),
            }
            results.append(result)
            self.logger.debug("Completed coin-run simulation step %s", step)
        return results

    def run(self, steps: int, length: int = 100):
        return self.benchmark(self.simulate, steps, length)


def main():
    simulation = CoinRunSimulation()
    benchmark = simulation.run(steps=10_000, length=100)
    results = benchmark["result"]
    print(sum(result["max_length_runs"] for result in results) / len(results))
    print(sum(result["num_runs"] for result in results) / len(results))


if __name__ == "__main__":
    main()
