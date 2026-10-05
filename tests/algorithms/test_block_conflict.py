import pytest

from Algorithms.arrays.block_conflict import block_conflict


def test_empty_operations_return_empty_result():
    assert block_conflict([]) == ""


def test_queries_without_obstacles_succeed():
    operations = [[2, 4, 3], [2, 10, 1], [2, -2, 5]]

    assert block_conflict(operations) == "111"


@pytest.mark.parametrize("obstacle", [4, 6])
def test_obstacle_at_either_interval_boundary_conflicts(obstacle):
    operations = [[1, obstacle], [2, 5, 3]]

    assert block_conflict(operations) == "0"


@pytest.mark.parametrize("obstacle", [3, 7])
def test_obstacle_outside_interval_does_not_conflict(obstacle):
    operations = [[1, obstacle], [2, 5, 3]]

    assert block_conflict(operations) == "1"


def test_queries_observe_obstacles_added_by_prior_operations():
    operations = [[1, 10], [2, 0, 3], [1, 1], [2, 0, 3]]

    assert block_conflict(operations) == "10"


def test_duplicate_obstacle_is_still_a_conflict():
    operations = [[1, 2], [1, 2], [2, 2, 1]]

    assert block_conflict(operations) == "0"


def test_obstacle_operations_do_not_add_to_result():
    assert block_conflict([[1, 4], [1, 8]]) == ""


def test_invalid_operation_type_raises_value_error():
    with pytest.raises(ValueError, match="Invalid operation type"):
        block_conflict([[3, 5]])