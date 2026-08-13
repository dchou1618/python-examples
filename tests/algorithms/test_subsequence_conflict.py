import pytest

from Algorithms.arrays.subsequence_conflict import subsequence


@pytest.mark.parametrize(
    "input_lsts, expected",
    [
        ([[1, 2, 15, 8], [2, 4, 7, 8]], True),
        ([[1, 6, 4], [4, 1]], False),
        ([[1, 2, 15, 8], [10]], True),
    ],
)
def test_subsequence(input_lsts, expected):
    assert subsequence(input_lsts) is expected
