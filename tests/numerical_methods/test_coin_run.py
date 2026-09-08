import logging

import pytest

from Algorithms.numerical_methods.coin_run import CoinRunSimulation


def test_run_combines_simulation_and_benchmark():
    simulation = CoinRunSimulation(seed=7)

    benchmark = simulation.run(steps=3, length=8)

    assert benchmark["elapsed_seconds"] >= 0
    assert [result["step"] for result in benchmark["result"]] == [0, 1, 2]
    assert all(1 <= result["num_runs"] <= 8 for result in benchmark["result"])
    assert all(1 <= result["max_length_runs"] <= 8 for result in benchmark["result"])


def test_simulation_logs_each_completed_step(caplog):
    simulation = CoinRunSimulation(seed=7)

    with caplog.at_level(logging.DEBUG, logger=simulation.logger.name):
        simulation.simulate(steps=2, length=4)

    assert [record.message for record in caplog.records] == [
        "Completed coin-run simulation step 0",
        "Completed coin-run simulation step 1",
    ]


@pytest.mark.parametrize(
    "steps, length, message",
    [
        (-1, 4, "steps must be non-negative"),
        (1, 0, "length must be positive"),
    ],
)
def test_simulation_rejects_invalid_parameters(steps, length, message):
    with pytest.raises(ValueError, match=message):
        CoinRunSimulation(seed=7).simulate(steps, length)