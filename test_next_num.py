import decimal
import random

import pytest

import next_num

# TODO: Set a fixed seed to ensure that random number generation is deterministic.
# TODO: Use multiple seeds and perform +-2 SD test. Use Monte Carlo method?
# TODO: Look into using Bayesian stats.
# TODO: Look into performing Binomial tests with confidence intervals.


class TestInputValidation:
    """
    Check that valid and invalid inputs are handled correctly.
    """

    def test_input_validation(self):
        """
        Check that valid inputs pass validation tests and are parsed properly.
        """
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

    def test_input_validation_random_nums_not_int(self):
        """
        Check that random_nums must be a list of integers.
        """
        random_nums = [-1, 0, 1, 2, 3.1]
        probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
        with pytest.raises(TypeError):
            next_num.RandomGen(random_nums, probabilities)

    def test_input_validation_probabilities_not_float(self):
        """
        Check that probabilities must be a list of floats.
        """
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, "0.01"]
        with pytest.raises(TypeError):
            next_num.RandomGen(random_nums, probabilities)

    def test_input_validation_length_mismatch(self):
        """
        Check that the length of random_nums and probabilities must be equal.
        """
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1]
        with pytest.raises(ValueError):
            next_num.RandomGen(random_nums, probabilities)

    def test_input_validation_negative_probability(self):
        """
        Check that probabilities must be non-negative.
        """
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, -0.01]
        with pytest.raises(ValueError):
            next_num.RandomGen(random_nums, probabilities)

    def test_input_validation_probability_sum_not_one(self):
        """
        Check that probabilities must sum to 1.
        """
        random_nums = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, 0.02]
        with pytest.raises(ValueError):
            next_num.RandomGen(random_nums, probabilities)


class TestNextNum:
    """
    Check that the random number generator provides valid outputs.
    """

    def test_find_index_of_number_for_random_roll_boundaries(self):
        """
        Check the boundaries for the number indices when finding the index of a
        number that a random roll corresponds to.
        """
        random_nums = [1, 2, 3]
        probabilities = [0.1, 0.2, 0.7]
        random_gen = next_num.RandomGen(random_nums, probabilities)
        # Check that it returns the first index for the lowest possible roll.
        assert (
            random_gen.find_index_of_number_for_random_roll(
                random_gen._cum_probabilities, 0.00
            )
            == 0
        )
        # TODO: Look into whether this is actually the upper bound.
        # Check that it returns the last index for the highest possible roll.
        assert (
            random_gen.find_index_of_number_for_random_roll(
                random_gen._cum_probabilities, 0.9999999999999999
            )
            == 2
        )

    def test_find_index_of_number_for_random_roll_ranges(self):
        """
        Check the ranges for the number indices when finding the index of a
        number that a random roll corresponds to.
        """
        random_nums = [1, 2, 3]
        probabilities = [0.1, 0.2, 0.7]
        random_gen = next_num.RandomGen(random_nums, probabilities)
        # TODO: Look into whether this is actually the upper bound.
        # Check that the first index is returned for a roll at the upper
        # boundary of the first range.
        assert (
            random_gen.find_index_of_number_for_random_roll(
                random_gen._cum_probabilities, 0.09999999999999999
            )
            == 0
        )
        # Check that the second index is returned for a roll at the lower
        # boundary of the second range.
        assert (
            random_gen.find_index_of_number_for_random_roll(
                random_gen._cum_probabilities, 0.1
            )
            == 1
        )

    def test_returns_values_from_number_list(self):
        """
        Check that the number generator only returns integers from the list.
        """
        random_nums = [1, 2, 3, 4, 5, 6]
        probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
        random_gen = next_num.RandomGen(random_nums, probabilities)
        iterations = 10000
        for _ in range(iterations):
            assert random_gen.next_num() in random_nums

    def test_returns_same_results_for_same_seed(self):
        """
        Check that the number generator returns the same sequence of numbers
        when the seed is the same, as the random function is pseudorandom.
        """
        random_nums = [1, 2, 3, 4, 5, 6]
        probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
        random_gen = next_num.RandomGen(random_nums, probabilities)
        iterations = 1000

        # Seed the random number generator and get the expected results to
        # compare outputs with.
        random.seed(10)
        expected_res = [random_gen.next_num() for _ in range(iterations)]

        # Check that the same sequence of numbers is returned when the seed is
        # the same.
        samples = 100
        for _ in range(samples):
            random.seed(10)
            assert [random_gen.next_num() for _ in range(iterations)] == expected_res


if __name__ == "__main__":
    pytest.main()
