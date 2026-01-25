
import torch
import pytest
from LLMs.torch_examples.batch_agg import standardize

def test_standardize_rows_mean_zero_std_one():
	torch.manual_seed(0)
	M = torch.randn((3, 4), dtype=torch.float32)
	S = standardize(M)
	# Check that each row has mean close to 0 and std close to 1
	row_means = S.mean(dim=1)
	row_stds = S.std(dim=1, unbiased=True)
	assert torch.allclose(row_means, torch.zeros_like(row_means), atol=1e-6)
	assert torch.allclose(row_stds, torch.ones_like(row_stds), atol=1e-6)


