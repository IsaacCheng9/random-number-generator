"""
Unit tests for the random_num_gen.py module.
"""
import decimal
import random

import pytest

import random_num_gen


def test_input_validation():
    """
    Check that valid inputs pass validation tests and are parsed properly.
    """
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
    assert random_gen.random_nums == random_nums
    assert random_gen.probabilities == [
        decimal.Decimal("0.01"),
        decimal.Decimal("0.3"),
        decimal.Decimal("0.58"),
        decimal.Decimal("0.1"),
        decimal.Decimal("0.01"),
    ]
    assert random_gen.cum_probabilities == [
        decimal.Decimal("0.01"),
        decimal.Decimal("0.31"),
        decimal.Decimal("0.89"),
        decimal.Decimal("0.99"),
        decimal.Decimal("1.0"),
    ]


def test_input_validation_random_nums_not_int():
    """
    Check that random_nums must be a list of integers.
    """
    random_nums = [-1, 0, 1, 2, 3.1]
    probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
    with pytest.raises(TypeError):
        random_num_gen.RandomGen(random_nums, probabilities)


def test_input_validation_probabilities_not_float():
    """
    Check that probabilities must be a list of floats.
    """
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 0.3, 0.58, 0.1, "0.01"]
    with pytest.raises(TypeError):
        random_num_gen.RandomGen(random_nums, probabilities)


def test_input_validation_length_mismatch():
    """
    Check that the length of random_nums and probabilities must be equal.
    """
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 0.3, 0.58, 0.1]
    with pytest.raises(ValueError):
        random_num_gen.RandomGen(random_nums, probabilities)


def test_input_validation_negative_probability():
    """
    Check that probabilities must be non-negative.
    """
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 0.3, 0.58, 0.1, -0.01]
    with pytest.raises(ValueError):
        random_num_gen.RandomGen(random_nums, probabilities)


def test_input_validation_larger_than_one_probability():
    """
    Check that probabilities cannot be greater than 1.0.
    """
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 1.01, 0.58, 0.1, -0.01]
    with pytest.raises(ValueError):
        random_num_gen.RandomGen(random_nums, probabilities)


def test_input_validation_probability_sum_not_one():
    """
    Check that probabilities must sum to 1.
    """
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 0.3, 0.58, 0.1, 0.02]
    with pytest.raises(ValueError):
        random_num_gen.RandomGen(random_nums, probabilities)


def test_find_index_of_number_for_random_roll_boundaries():
    """
    Check the boundaries for the number indices when finding the index of a
    number that a random roll corresponds to.
    """
    random_nums = [1, 2, 3]
    probabilities = [0.1, 0.2, 0.7]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
    # Check that it returns the first index for the lowest possible roll.
    assert (
        random_num_gen.find_cumulative_probability_index_of_float(
            random_gen.cum_probabilities, 0.00
        )
        == 0
    )
    # Check that it returns the last index for the highest possible roll.
    assert (
        random_num_gen.find_cumulative_probability_index_of_float(
            random_gen.cum_probabilities, 0.9999999999999999
        )
        == 2
    )


def test_find_index_of_number_for_random_roll_ranges():
    """
    Check the ranges for the number indices when finding the index of a
    number that a random roll corresponds to.
    """
    random_nums = [1, 2, 3]
    probabilities = [0.1, 0.2, 0.7]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
    # Check that the first index is returned for a roll at the upper
    # boundary of the first range.
    assert (
        random_num_gen.find_cumulative_probability_index_of_float(
            random_gen.cum_probabilities, 0.09999999999999999
        )
        == 0
    )
    # Check that the second index is returned for a roll at the lower
    # boundary of the second range.
    assert (
        random_num_gen.find_cumulative_probability_index_of_float(
            random_gen.cum_probabilities, 0.1
        )
        == 1
    )


def test_returns_values_from_number_list():
    """
    Check that the number generator only returns integers from the list.
    """
    random_nums = [1, 2, 3, 4, 5, 6]
    probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
    iterations = 1000
    for _ in range(iterations):
        assert random_gen.next_num() in random_nums


def test_returns_same_results_for_same_seed():
    """
    Check that the number generator returns the same sequence of numbers
    when the seed is the same, as the random function is pseudorandom.
    """
    random_nums = [1, 2, 3, 4, 5, 6]
    probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
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


def test_returns_different_results_for_different_seeds():
    """
    Check that the number generator returns different sequences of numbers
    when the seed is different, as the random function is pseudorandom.
    """
    random_nums = [1, 2, 3, 4, 5, 6]
    probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
    iterations = 1000

    # Seed the random number generator and get the expected results to
    # compare outputs with.
    random.seed(10)
    expected_res = [random_gen.next_num() for _ in range(iterations)]

    # Check that the same sequence of numbers is returned when the seed is
    # different.
    samples = 100
    for increment in range(1, samples + 1):
        random.seed(10 + increment)
        assert [random_gen.next_num() for _ in range(iterations)] != expected_res


def test_monte_carlo_simulation():
    """
    Check that the number generator returns numbers with frequencies that
    are within an expected range given the probabilities.
    """
    random_nums = [1, 2, 3, 4, 5, 6]
    probabilities = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
    random_gen = random_num_gen.RandomGen(random_nums, probabilities)
    iterations = 100000
    samples = 100

    # Get the expected frequencies of the numbers given the probabilities.
    expected_frequencies = [prob * iterations for prob in probabilities]

    for _ in range(samples):
        random.seed()
        # Get the actual frequencies of the numbers returned by the number
        # generator.
        actual_frequencies = [0] * len(random_nums)
        for _ in range(iterations):
            actual_frequencies[random_gen.next_num() - 1] += 1

        # Check that the actual frequencies are within 5% of the expected
        # range given the probabilities.
        for index in range(len(random_nums)):
            assert (
                abs(actual_frequencies[index] - expected_frequencies[index])
                / expected_frequencies[index]
                <= 0.05
            )


if __name__ == "__main__":
    pytest.main()
