# Sobol Sampling

`experiment.py` provides an unscrambled Sobol sequence generator for 1 through
10 dimensions. The first dimension uses powers of two; dimensions 2 through 10
use dimension-specific primitive-polynomial parameters and the Sobol direction
number recurrence.

```python
from Algorithms.numerical_methods.sobol_sampling.experiment import Sobol

sampler = Sobol(dimensions=3, num_directions=32)
point = next(sampler)
unit_point = point.astype(float) / (1 << sampler.bits)
```

Points are returned as `numpy.uint32` integer vectors. Divide by `2 ** 32` to
map coordinates to the unit cube. As in the original implementation, the
iterator's first point is the first non-zero sequence point; it does not yield
the all-zero origin. `num_directions` controls the available bit depth and must
be between 1 and 32, so at most `2 ** num_directions - 1` points can be
generated.
Requests outside the supported dimension or bit-depth ranges raise
`ValueError`.
