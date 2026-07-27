from Algorithms.numerical_methods.euler.p48 import self_powers


def test_sol1():
    res = self_powers(n=1000)
    assert res == 9110846700
