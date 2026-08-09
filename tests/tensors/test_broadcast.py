from Algorithms.tensors.broadcast import layer_norm, batch_norm, normalize_l2, pairwise_cosine, pairwise_cosine_broadcast
import numpy as np
import pytest


def test_normalize_l2_keeps_shape_and_unit_norms():
    A = np.array([[3.0, 4.0], [6.0, 8.0]])
    out = normalize_l2(A, dim=1)
    assert out.shape == A.shape
    norms = np.sqrt((out**2).sum(axis=1))
    assert np.allclose(norms, np.ones_like(norms))


def test_layer_norm_statistics_and_errors():
    rng = np.random.RandomState(0)
    A = rng.randn(4, 3, 10) * 5 + 2
    out = layer_norm(A)
    means = out.mean(axis=2)
    vars = out.var(axis=2)
    assert np.allclose(means, 0, atol=1e-6)
    assert np.allclose(vars, 1, rtol=1e-3)
    with pytest.raises(ValueError):
        layer_norm(np.zeros((2, 3)))


def test_batch_norm_statistics_and_errors():
    rng = np.random.RandomState(1)
    A = rng.randn(5, 4, 8) * 3 + 1
    out = batch_norm(A)
    means = out.mean(axis=(0, 1))
    vars = out.var(axis=(0, 1))
    assert np.allclose(means, 0, atol=1e-6)
    assert np.allclose(vars, 1, rtol=1e-3)
    with pytest.raises(ValueError):
        batch_norm(np.zeros((3, 4)))


def test_pairwise_cosine_matches_broadcast_and_self_similarity():
    A = np.array([
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 1.0],
    ])

    out_direct = pairwise_cosine(A)
    out_broadcast = pairwise_cosine_broadcast(A)

    assert out_direct.shape == (3, 3)
    assert out_broadcast.shape == (3, 3)
    assert np.allclose(out_direct, out_broadcast)
    assert np.allclose(np.diag(out_direct), np.ones(3))


def test_pairwise_cosine_zero_vector_behaviour():
    A = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
    ])

    with np.errstate(divide='warn', invalid='warn'):
        with pytest.warns(RuntimeWarning):
            _ = pairwise_cosine(A)

    with np.errstate(divide='warn', invalid='warn'):
        with pytest.warns(RuntimeWarning):
            _ = pairwise_cosine_broadcast(A)
