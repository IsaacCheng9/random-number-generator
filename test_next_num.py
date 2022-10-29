import decimal

import pytest

import next_num

# TODO: Set a fixed seed to ensure that random number generation is deterministic.
# TODO: Use multiple seeds and perform +-2 SD test. Use Monte Carlo method?
# TODO: Look into using Bayesian stats.


class TestInputValidation:
    """
    Check that valid and invalid inputs are handled correctly.
    """

    def test_input_validation(self):
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
        random_gen = next_num.RandomGen(random_nums, probabilities)
        assert random_gen._random_nums == random_nums
        assert random_gen._probabilities == [
            decimal.Decimal("0.01"),
            decimal.Decimal("0.3"),
            decimal.Decimal("0.58"),
            decimal.Decimal("0.1"),
            decimal.Decimal("0.01"),
        ]
        assert random_gen._cum_probabilities == [
            decimal.Decimal("0.01"),
            decimal.Decimal("0.31"),
            decimal.Decimal("0.89"),
            decimal.Decimal("0.99"),
            decimal.Decimal("1.0"),
        ]

    def test_input_validation_length_mismatch(self):
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1]
        with pytest.raises(ValueError):
            next_num.RandomGen(random_nums, probabilities)

    def test_input_validation_negative_probability(self):
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, -0.01]
        with pytest.raises(ValueError):
            next_num.RandomGen(random_nums, probabilities)

    def test_input_validation_probability_sum_not_one(self):
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, 0.02]
        with pytest.raises(ValueError):
            next_num.RandomGen(random_nums, probabilities)


class TestNextNum:
    """
    Check that the random number generator provides valid outputs.
    """

    def test_returns_values_from_number_list(self):
        random_nums = [1, 2, 3, 4, 5, 6]
        probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
        random_gen = next_num.RandomGen(random_nums, probabilities)
        iterations = 10000
        for _ in range(iterations):
            assert random_gen.next_num() in random_nums
