import numpy as np
import pytest

from Algorithms.numerical_methods.sobol_sampling.experiment import Sobol


def test_first_eight_three_dimensional_points_match_reference_sequence():
	sampler = Sobol(dimensions=3, num_directions=32)
	points = [tuple(int(value) for value in next(sampler)) for _ in range(8)]

	assert points == [
		(0x80000000, 0x80000000, 0x80000000),
		(0xC0000000, 0x40000000, 0x40000000),
		(0x40000000, 0xC0000000, 0xC0000000),
		(0x60000000, 0x60000000, 0xA0000000),
		(0xE0000000, 0xE0000000, 0x20000000),
		(0xA0000000, 0x20000000, 0xE0000000),
		(0x20000000, 0xA0000000, 0x60000000),
		(0x30000000, 0x50000000, 0xF0000000),
	]


def test_ten_dimensional_generator_initializes_every_coordinate():
	sampler = Sobol(dimensions=10, num_directions=8)

	assert tuple(int(value) for value in next(sampler)) == (0x80000000,) * 10


@pytest.mark.parametrize(
	("dimensions", "num_directions"),
	[(0, 32), (11, 32), (3, 0), (3, 33)],
)
def test_rejects_unsupported_dimensions_or_direction_counts(
	dimensions, num_directions
):
	with pytest.raises(ValueError):
		Sobol(dimensions=dimensions, num_directions=num_directions)


def test_stops_after_configured_direction_bits_are_exhausted():
	sampler = Sobol(dimensions=2, num_directions=2)

	assert len(list(sampler)) == 3


def test_sobol_points_cover_grid_more_evenly_than_pseudorandom_points():
	num_points = 255
	sampler = Sobol(dimensions=2, num_directions=8)
	sobol_points = np.array([next(sampler) for _ in range(num_points)]) / 2**32
	pseudo_random_points = np.random.default_rng(seed=42).random((num_points, 2))

	sobol_counts = np.histogramdd(
		sobol_points, bins=8, range=((0, 1), (0, 1))
	)[0]
	pseudo_random_counts = np.histogramdd(
		pseudo_random_points, bins=8, range=((0, 1), (0, 1))
	)[0]

	assert np.var(sobol_counts) < np.var(pseudo_random_counts)
