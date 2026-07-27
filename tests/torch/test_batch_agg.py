import torch
import pytest
from LLMs.torch_examples.batch_agg import (
    standardize,
    normalize_per_batch,
    sample_gaussian_pairs,
)


def test_standardize_rows_mean_zero_std_one():
    torch.manual_seed(0)
    M = torch.randn((3, 4), dtype=torch.float32)
    S = standardize(M)
    # Check that each row has mean close to 0 and std close to 1
    row_means = S.mean(dim=1)
    row_stds = S.std(dim=1, unbiased=True)
    assert torch.allclose(row_means, torch.zeros_like(row_means), atol=1e-6)
    assert torch.allclose(row_stds, torch.ones_like(row_stds), atol=1e-6)


def test_normalize_per_batch_even_split():
    torch.manual_seed(0)
    p = 5
    num_samples = 20
    batch_size = 4
    result = normalize_per_batch(p, num_samples, batch_size)
    # result shape: (num_samples, p)
    assert result.shape == (num_samples, p)
    # Check each batch has mean 0 and std 1 per dimension
    num_batches = num_samples // batch_size
    for i in range(num_batches):
        batch = result[i * batch_size : (i + 1) * batch_size, :]
        means = batch.mean(dim=0)
        stds = batch.std(dim=0, unbiased=True)
        assert torch.allclose(means, torch.zeros_like(means), atol=1e-5)
        assert torch.allclose(stds, torch.ones_like(stds), atol=1e-5)


def test_normalize_per_batch_uneven_split():
    torch.manual_seed(0)
    p = 3
    num_samples = 11
    batch_size = 4
    result = normalize_per_batch(p, num_samples, batch_size)
    # result shape: (num_samples, p)
    assert result.shape == (num_samples, p)
    # Check that each batch (by batch id) has mean ~0 and std ~1 per dimension
    # Since batch ids are random, just check global mean/std are close to 0/1
    means = result.mean(dim=0)
    stds = result.std(dim=0, unbiased=True)
    assert torch.allclose(means, torch.zeros_like(means), atol=0.2)
    assert torch.allclose(stds, torch.ones_like(stds), atol=0.2)


def test_normalize_per_batch_invalid_batch_size():
    with pytest.raises(ValueError):
        normalize_per_batch(2, num_samples=5, batch_size=10)


def test_sample_gaussian_pairs_shape_and_range():
    torch.manual_seed(0)
    p = 100
    num_samples = 1000
    result = sample_gaussian_pairs(p, num_samples)
    assert result.shape == (num_samples,)
    # Most values should be between -0.3 and 0.3 for high-dim random vectors
    assert (result.abs() < 0.5).float().mean() > 0.95
