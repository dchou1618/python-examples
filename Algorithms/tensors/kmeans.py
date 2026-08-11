import numpy as np

def generate_centers(k: int,
                     dim: int,
                     mn: np.array,
                     mx: np.array):
  return mn + np.random.rand(k, dim)*(mx-mn)

def k_means(k: int, data: np.array, iterations: int):
  """
  given a numpy dataset, apply vector quantization to model probability
  density functions by distribution of prototype functions.

  array of tuples to list "tolist()" for the standard matrix format.
  Or np.vstack

  ## Annotate tensor sizes ##
  data: [num_points, feature_dimension]
  output:
  centers: [k, feature_dimension]
  labels: [num_points, feature_dimension]
  """
  # data = np.array(data.tolist())
  data = np.vstack(data)
  # axis is column 0 rows 1.
  mn, mx = data.min(axis=0), data.max(axis=0)
  # randomly generate centers
  centers = generate_centers(k=k,
                             dim=data.shape[-1],
                             mn=mn,
                             mx=mx)
  for _ in range(iterations):
    # distances: [num_points, num_centers (k), feature_dimension]
    # squared norm, at least avoids extra square root (monotonic increasing
    # function)
    distances = np.sum((data[:, None, :] - centers[None, :, :]) ** 2,
                       axis=2)

    # Which center is closest to each point?
    labels = np.argmin(distances, axis=1)

    # Recompute centers
    for j in range(k):
        points = data[labels == j]

        if len(points) > 0:
            centers[j] = points.mean(axis=0)

  return centers, labels