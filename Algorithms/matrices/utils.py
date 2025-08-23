import numpy as np
from scipy.linalg.blas import dsymm
import time

def slow_update_matrix(C: np.ndarray, 
                       A: np.ndarray, 
                       B: np.ndarray):
    n = C.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[k, i] * B[k, j] * A[k, j]
    return C
def update_matrix(C: np.ndarray, 
                  A: np.ndarray, 
                  B: np.ndarray):
    """
    Update matrix C by adding A^T @ B @ A, for symmetric matrix B efficiently
    and ensure innermost loop uses unit-stride vector operations. Since B is symmetric,
    it's stored in compact upper triangular form.
    """
    assert C.shape == A.shape and C.shape == B.shape, "Matrices C, A, and B must have the same shape."
    assert (B.T == B).all(), "Matrix B must be symmetric."
    BA = B @ A
    C += A.T @ BA
    return C

def symm_update(C, A, B):
    BA = dsymm(1.0, B, A)  # B symmetric
    C += A.T @ BA
    return C


if __name__ == "__main__":
    n = 10000  # try larger like 400–1000 for clearer results
    A = np.random.randn(n, n)
    B = np.random.randn(n, n)
    B = (B + B.T) / 2   # symmetrize
    C1 = np.zeros((n, n))
    C2 = np.zeros((n, n))

    # Time slow
    # start = time.time()
    # slow_update_matrix(C1.copy(), A, B)
    # print("Slow update time:", time.time() - start)

    # Time fast
    start = time.time()
    update_matrix(C2.copy(), A, B)
    print("Fast update time:", time.time() - start)

    start = time.time()
    symm_update(C2.copy(), A, B)
    print("BLAS symm update time:", time.time() - start)

    # Check correctness
    print("Difference norm:", np.linalg.norm(C1 - C2))