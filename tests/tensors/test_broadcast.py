from Algorithms.tensors.broadcast import layer_norm, batch_norm, normalize_l2
import numpy as np
import pytest


def test_normalize_l2_keeps_shape_and_unit_norms():
	A = np.array([[3.0, 4.0], [6.0, 8.0]])
	out = normalize_l2(A, dim=1)
	assert out.shape == A.shape
	norms = np.sqrt((out ** 2).sum(axis=1))
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

