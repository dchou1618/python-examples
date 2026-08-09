import numpy as np


def normalize_l2(A: np.array, dim: int) -> np.array:
    """
    input:
    A: [D1,D2,...]
    operations:
    keepdims preserves the dimension. For instance:
    A       [B, N, D]
    norm    [B, N, 1]
    output:
    A/norm: [D1,D2,...] same shape but normalize along given axis/dim
    """
    norm = np.sqrt((A**2).sum(axis=dim, keepdims=True))
    return A / norm


def layer_norm(A: np.array) -> np.array:
    """
    input:
    A: [B, N, D] (batch, seq len, feature dimension)
    operations: keepdims used to retain original dimensions for broadcasting
    """
    if len(A.shape) != 3:
        raise ValueError("Input must be a 3D array with shape [B, N, D]")
    means = A.mean(axis=2, keepdims=True)
    vars = A.var(axis=2, keepdims=True)

    return (A - means) / np.sqrt(vars + 1e-5)


def batch_norm(A: np.array) -> np.array:
    """
    input:
    A: [B, N, D] (batch, seq len, feature dimension)
    operations:
    pool batch and sequence length so we normalize each feature independently
    using the pooled batch statistics. keepdims used to retain original dimensions for broadcasting
    """
    if len(A.shape) != 3:
        raise ValueError("Input must be a 3D array with shape [B, N, D]")
    means = A.mean(axis=(0, 1), keepdims=True)
    vars = A.var(axis=(0, 1), keepdims=True)

    return (A - means) / np.sqrt(vars + 1e-5)

def pairwise_cosine(A: np.array) -> np.array:
    """
    input:
    A: [N, D]

    output:
    [N, N]: each entry in matrix is cosine similarity
    """
    norm = np.sqrt((A**2).sum(axis=1, keepdims=True))
    normalized = A / norm
    return normalized @ normalized.T

def pairwise_cosine_broadcast(A: np.array) -> np.array:
    """
    input:
    A: [N, D]

    output:
    [N, N]: each entry in matrix is cosine similarity
    """
    norm = np.sqrt((A**2).sum(axis=1, keepdims=True))
    normalized = A / norm
    return (normalized[:, None, :] * normalized[None, :, :]).sum(axis=-1)

def feature_thresholds(A: np.array, thresholds: np.array) -> np.array:
    """
    input: 
    A: [B, N, D]
    thresholds: [D] for each dimension

    output:
    [B, N, D] with features below threshold masked out
    """
    mask = A > thresholds
    return A * mask