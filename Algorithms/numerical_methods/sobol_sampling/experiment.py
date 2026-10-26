import numpy as np


# Primitive-polynomial parameters for dimensions 2 through 10.
_DIRECTION_PARAMETERS = (
    (1, 0, (1,)),
    (2, 1, (1, 3)),
    (3, 1, (1, 3, 1)),
    (3, 2, (1, 1, 1)),
    (4, 1, (1, 1, 3, 3)),
    (4, 4, (1, 3, 5, 13)),
    (5, 2, (1, 1, 5, 5, 17)),
    (5, 4, (1, 1, 5, 5, 5)),
    (5, 7, (1, 1, 7, 11, 19)),
)


class Sobol:
    def __init__(self, dimensions: int, num_directions: int):
        if not 1 <= dimensions <= len(_DIRECTION_PARAMETERS) + 1:
            raise ValueError("dimensions must be between 1 and 10")
        if not 1 <= num_directions <= 32:
            raise ValueError("num_directions must be between 1 and 32")

        self.index = 0
        self.point = np.zeros(dimensions, dtype=np.uint32)
        self.bits = 32
        self.num_directions = num_directions
        self.directions = np.zeros((dimensions, num_directions), dtype=np.uint32)

        for j in range(num_directions):
            self.directions[0, j] = 1 << (self.bits - j - 1)

        for dimension, (degree, polynomial, initial_values) in enumerate(
            _DIRECTION_PARAMETERS[: dimensions - 1], start=1
        ):
            for j, initial_value in enumerate(initial_values[:num_directions]):
                self.directions[dimension, j] = initial_value << (
                    self.bits - j - 1
                )

            for j in range(degree, num_directions):
                value = self.directions[dimension, j - degree] ^ (
                    self.directions[dimension, j - degree] >> degree
                )
                for k in range(1, degree):
                    if polynomial & (1 << (degree - k - 1)):
                        value ^= self.directions[dimension, j - k]
                self.directions[dimension, j] = value

    def __iter__(self):
        return self

    def __next__(self):
        first_zero_position = (~self.index & (self.index + 1)).bit_length() - 1
        if first_zero_position >= self.num_directions:
            raise StopIteration
        self.point = self.point ^ self.directions[:, first_zero_position]
        self.index += 1
        return self.point

