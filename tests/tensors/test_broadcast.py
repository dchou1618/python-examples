from Algorithms.tensors.broadcast import layer_norm, batch_norm, normalize_l2, pairwise_cosine, pairwise_cosine_broadcast, feature_thresholds
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


def test_feature_thresholds_basic_and_counts():
    A = np.array([[[1, 2, 3], [4, 5, 6]]])  # shape (1,2,3)
    thresholds = np.array([2, 4, 5])  # shape (3,)

    out = feature_thresholds(A, thresholds)
    # Output should retain original shape and keep values where mask is True
    assert out.shape == A.shape
    # second row kept, first row zeroed
    assert np.array_equal(out[0, 1, :], np.array([4, 5, 6]))
    assert np.array_equal(out[0, 0, :], np.zeros(3))
    mask = A > thresholds
    assert np.count_nonzero(out) == np.sum(mask)


def test_feature_thresholds_broadcast_variants_same_result():
    A = np.array([[[1, 2, 3], [4, 5, 6]]])  # (1,2,3)
    thr1 = np.array([2, 4, 5])              # (3,)
    thr2 = thr1.reshape(1, 1, 3)            # (1,1,3)
    thr3 = np.tile(thr1, (1, 2, 1))         # (1,2,3)

    out1 = feature_thresholds(A, thr1)
    out2 = feature_thresholds(A, thr2)
    out3 = feature_thresholds(A, thr3)

    assert np.array_equal(out1, out2)
    assert np.array_equal(out1, out3)
    # number of non-zero entries should equal number of True mask entries
    mask = A > thr1
    assert np.count_nonzero(out1) == np.sum(mask)


def test_feature_thresholds_all_false_returns_empty():
    A = np.zeros((2, 2, 2))
    thresholds = np.ones(2)

    out = feature_thresholds(A, thresholds)
    # retains shape but contains no selected values
    assert out.shape == A.shape
    assert np.count_nonzero(out) == 0
    assert np.allclose(out, 0)
