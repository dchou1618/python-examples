import numpy as np
import pytest

from Algorithms.tensors.kmeans import generate_centers, k_means


def test_generate_centers_within_bounds_and_shape():
    rng = np.random.RandomState(0)
    np.random.set_state(rng.get_state())

    k = 4
    dim = 3
    mn = np.array([0.0, -2.0, 5.0])
    mx = np.array([1.0, 2.0, 10.0])

    centers = generate_centers(k=k, dim=dim, mn=mn, mx=mx)

    assert centers.shape == (k, dim)
    assert np.all(centers >= mn)
    assert np.all(centers <= mx)


def test_generate_centers_respects_min_max_for_each_dimension():
    k = 10
    dim = 2
    mn = np.array([-1.0, -1.0])
    mx = np.array([1.0, 1.0])

    centers = generate_centers(k=k, dim=dim, mn=mn, mx=mx)

    assert np.all(centers[:, 0] >= -1.0)
    assert np.all(centers[:, 0] <= 1.0)
    assert np.all(centers[:, 1] >= -1.0)
    assert np.all(centers[:, 1] <= 1.0)


def test_k_means_simple_clusters_converge():
    rng = np.random.RandomState(1)
    # two well-separated clusters in 2D
    cluster_a = rng.randn(10, 2) * 0.1 + np.array([0.0, 0.0])
    cluster_b = rng.randn(10, 2) * 0.1 + np.array([5.0, 5.0])
    data = np.vstack([cluster_a, cluster_b])

    centers, labels = k_means(k=2, data=data, iterations=10)

    assert centers.shape == (2, 2)
    assert labels.shape == (20,)
    assert set(labels) <= {0, 1}

    # each cluster should be assigned consistently once centers are grown
    cluster0_mean = data[labels == 0].mean(axis=0)
    cluster1_mean = data[labels == 1].mean(axis=0)
    assert np.allclose(np.sort(centers, axis=0), np.sort(np.vstack([cluster0_mean, cluster1_mean]), axis=0), atol=1e-1)


def test_k_means_returns_valid_assignments_for_small_dataset():
    data = np.array([
        [0.0, 0.0],
        [0.1, -0.05],
        [5.0, 5.0],
        [4.9, 5.1],
    ])

    centers, labels = k_means(k=2, data=data, iterations=5)

    assert centers.shape == (2, 2)
    assert labels.shape == (4,)
    assert np.array_equal(np.sort(np.unique(labels)), np.array([0, 1]))
    assert np.all(labels[:2] == labels[0])
    assert np.all(labels[2:] == labels[2])
    assert labels[0] != labels[2]
