"""
An implementation of a random number generator that takes a list of numbers
and their corresponding probabilities of occurring. When random numbers are
generated multiple times, the distribution of numbers should converge towards
the probabilities given due to the law of large numbers.
"""
import bisect
import collections
import decimal
import random
from typing import List


def find_cumulative_probability_index_of_float(
    cumulative_probabilities: List[decimal.Decimal], probability_float: float
) -> int:
    """
    Find the index of the cumulative probability corresponding to the
    probability float.

    Args:
        cumulative_probabilities: List of cumulative probabilities.
        probability_float: Probability between 0 and 1 inclusive.

    Returns:
        The index corresponding to the cumulative probability float.
    """
    # Find the insertion point for random_float in cumulative_probabilities.
    index = bisect.bisect(cumulative_probabilities, probability_float)
    return index


class RandomNumberList:
    """
    A list of random numbers that can be generated by RandomGen.
    """

    def __set__(self, obj, value):
        if not all(isinstance(num, int) for num in value):
            raise TypeError("All random numbers must be integers.")
        self.value = value

    def __get__(self, obj, objtype=None):
        return self.value


class RandomGen:
    """
    A random number generator that returns a random number given a list of
    integers and their corresponding float probabilities of occurring.
    """

    random_nums = RandomNumberList()

    def __init__(self, random_nums: List[int], probabilities: List[float]):
        """
        Args:
            random_nums: Integer values that may be returned by the random
                number generator. Example: [-1, 0, 1, 2, 3]
            probabilities: Probability of each number being returned by the
                random number generator. Example: [0.01, 0.3, 0.58, 0.1, 0.01]
        """
        if len(random_nums) != len(probabilities):
            raise ValueError("Length of random_nums and probabilities must be equal.")

        self.random_nums = random_nums

        # Calculate the cumulative probabilities to find the range that each
        # number falls into when generating a random number.
        self.probabilities = []
        self.cum_probabilities = []
        cumulative = decimal.Decimal(0.00)
        for probability in probabilities:
            if probability < 0:
                raise ValueError("Probabilities must be non-negative.")
            if probability > 1.0:
                raise ValueError("Probabilities cannot be greater than 1.0.")
            if not isinstance(probability, float):
                raise TypeError("Probabilities must be a list of floats.")

            # Convert probabilities into decimal floating point arithmetic for
            # precision to prevent floating point arithmetic errors.
            probability = decimal.Decimal(str(probability))
            cumulative += probability
            self.probabilities.append(probability)
            self.cum_probabilities.append(cumulative)

        if self.cum_probabilities[-1] != 1.0:
            raise ValueError("Probabilities must sum to 1.")

    def next_num(self) -> int:
        """
        Generate a random number based on the probabilities provided.

        Returns:
            One of the random_nums - when called multiple times over a long
            period, it should return the numbers roughly with the initialised
            probabilities.
        """
        random_roll = random.random()
        # Find the index of the number whose probability range this random roll
        # fits into.
        number_index = find_cumulative_probability_index_of_float(
            self.cum_probabilities, random_roll
        )
        return self.random_nums[number_index]


if __name__ == "__main__":
    input_random_nums = [-1, 0, 1, 2, 3]
    input_probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
    random_gen = RandomGen(input_random_nums, input_probabilities)
    num_counts = collections.defaultdict(int)
    # Set how many numbers to generate - a larger number of iterations will
    # converge to the expected probabilities due to the law of large numbers.
    ITERATIONS = 10000
    for _ in range(ITERATIONS):
        num_counts[random_gen.next_num()] += 1

    # Print the parameters and results of the random number generation.
    print(f"Numbers: {input_random_nums}\nProbabilities: {input_probabilities}\n")
    print("Expected Results [Number: Frequency]:")
    for i, random_num in enumerate(input_random_nums):
        print(f"{random_num}: {int(input_probabilities[i] * ITERATIONS)} times")
    print("\nActual Results [Number: Frequency " "(Proportion)]:")
    for input_num in input_random_nums:
        print(
            f"{input_num}: {num_counts[input_num]} times "
            f"({num_counts[input_num] / ITERATIONS})"
        )
