from Algorithms.numerical_methods.euler.p49 import prime_permutations


def test_sol():
    assert sorted(prime_permutations(n=4, perms=3)) == ["148748178147", "296962999629"]


def test_higher_n():
    assert sorted(prime_permutations(n=5, perms=4)) == ["83987889379388798837"]
