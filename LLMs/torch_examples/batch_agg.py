import torch


def standardize(M: torch.Tensor) -> torch.Tensor:
    """
    standardize standardizes each row of the input matrix M to have mean 0 and std 1.
    Arguments:
        M: input tensor of shape (n, p)
    Returns:
        A tensor of shape (n, p) where each row has mean 0 and std 1.
    """
    return (M - M.mean(axis=1).unsqueeze(1)) / M.std(axis=1).unsqueeze(1)


def normalize_per_batch(p: int, num_samples: int = 100, batch_size: int = 10):
    """
    normalize_per_batch generates num_samples random p-dim vectors,
    splits them into batches of size batch_size (last batch may be smaller),
    and standardizes each batch to have mean 0 and std 1 per dimension.
      Arguments:
          p: dimension of the vectors
          num_samples: total number of samples to generate
          batch_size: size of each batch
      Returns:
          A tensor of shape (num_samples, p) containing the standardized vectors.
    """
    if batch_size > num_samples:
        raise ValueError("batch_size must be at most number of samples.")
    mat = torch.randn((num_samples, p), dtype=torch.float32)
    num_batches = num_samples // batch_size
    remainder = num_samples % batch_size
    num_batches += int(remainder != 0)
    if remainder == 0:
        # evenly split
        batch_mat = mat.view(num_batches, batch_size, p)
        means = batch_mat.mean(dim=1, keepdim=True)  # (num_batches, 1, p)
        stds = batch_mat.std(dim=1, keepdim=True)  # (num_batches, 1, p)
        standardized = (batch_mat - means) / (stds + 1e-8)
        return standardized.view(num_samples, p)
    else:
        # scattered
        batch_ids = torch.randint(0, num_batches, (num_samples,))
        # count per group
        counts = torch.bincount(batch_ids, minlength=num_batches).unsqueeze(1)
        batch_ids_processed = batch_ids.unsqueeze(1).expand(-1, p)
        sum_per_group = torch.zeros((num_batches, p)).scatter_add_(
            0, batch_ids_processed, mat
        )
        mean_per_group = sum_per_group / counts.clamp(min=1)

        sum_sq = (mat - mean_per_group[batch_ids]) ** 2
        sum_sq_per_group = torch.zeros((num_batches, p)).scatter_add_(
            0, batch_ids_processed, sum_sq
        )
        var_per_group = sum_sq_per_group / counts.clamp(min=1)
        std_per_group = torch.sqrt(var_per_group + 1e-8)
        return (mat - mean_per_group[batch_ids]) / (std_per_group[batch_ids])


def sample_gaussian_pairs(p: int, num_samples: int = 10000, eps: float = 1e-8):
    """
    sanple_gaussian_pairs generates num_samples pairs of p-dimensional vectors
    from standard normal distribution, and computes their normalized inner products.
    Highlights that high-dimensional random vectors are almost orthogonal.
    Arguments:
      p: dimension of the vectors
      num_samples: number of pairs to sample
      eps: small value to avoid division by zero
    Returns:
      A tensor of shape (num_samples,) containing the normalized inner products.
    """
    pair_mat = torch.randn((2 * num_samples, p), dtype=torch.float32)
    pair_mat = pair_mat.view(num_samples, 2, p)
    norm_first = torch.norm(pair_mat[:, 0, :], dim=1)
    norm_second = torch.norm(pair_mat[:, 1, :], dim=1)
    dot_prod = (pair_mat[:, 0, :] * pair_mat[:, 1, :]).sum(dim=1)
    norm_inner_prods = dot_prod / (norm_first * norm_second + eps)
    return norm_inner_prods
