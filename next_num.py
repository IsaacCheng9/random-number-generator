import bisect
import collections
import decimal
import random


class RandomGen(object):
    def __init__(self, random_nums: list, probabilities: list):
        """
        Args:
            random_nums: Integer values that may be returned by the random
                number generator. Example: [-1, 0, 1, 2, 3]
            probabilities: Probability of each number being returned by the
                random number generator. Example: [0.01, 0.3, 0.58, 0.1, 0.01]
        """
        # TODO: Consider adding a flag to sacrifice floating point precision for speed (using numpy with ints instead of decimal).
        # !IMPORTANT: Order checks from fastest to slowest to execute.
        if len(random_nums) != len(probabilities):
            raise ValueError("Length of random_nums and probabilities must be equal.")

        if any(type(num) != int for num in random_nums):
            raise TypeError("random_nums must be a list of integers.")
        self._random_nums = random_nums

        # Calculate the cumulative probabilities to find the range that each
        # number falls into when generating a random number.
        self._probabilities = []
        self._cum_probabilities = []
        cumulative = decimal.Decimal(0.00)
        for probability in probabilities:
            if probability < 0:
                raise ValueError("probabilities must be non-negative.")
            if type(probability) != float:
                raise TypeError("probabilities must be a list of floats.")

            # Convert probabilities into decimal floating point arithmetic for
            # precision to prevent floating point arithmetic errors.
            probability = decimal.Decimal(str(probability))
            cumulative += probability
            self._probabilities.append(probability)
            self._cum_probabilities.append(cumulative)

        if self._cum_probabilities[-1] != 1.0:
            raise ValueError("probabilities must sum to 1.")

    def find_index_of_number_for_random_roll(
        self, cumulative_probabilities: list, random_roll: float
    ) -> int:
        """
        Find the index of the number corresponding to the random roll.

        Args:
            cumulative_probabilities: List of cumulative probabilities.
            random_roll: Random float between 0 and 1 inclusive.

        Returns:
            Index of the number corresponding to the random roll.
        """
        # Find the insertion point for random_roll in cumulative_probabilities.
        index = bisect.bisect(cumulative_probabilities, random_roll)
        return index

    def next_num(self) -> int:
        """
        Generate a random number based on the probabilities provided.

        Returns:
            One of the random_nums - when called multiple times over a long
            period, it should return the numbers roughly with the initialised
            probabilities.
        """
        # TODO: Look into how this function works.
        random_roll = random.random()
        # Find the index of the number whose probability range this random roll
        # fits into.
        number_index = self.find_index_of_number_for_random_roll(
            self._cum_probabilities, random_roll
        )
        return self._random_nums[number_index]


if __name__ == "__main__":
    random_nums = [-1, 0, 1, 2, 3]
    probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
    random_gen = RandomGen(random_nums, probabilities)
    num_counts = collections.defaultdict(int)
    # Set how many numbers to generate - a larger sample size will generally
    # converge to the expected probabilities due to the law of large numbers.
    iterations = 10000
    for _ in range(iterations):
        num_counts[random_gen.next_num()] += 1

    # Print the results of the random number generation.
    print(f"Numbers: {random_nums}")
    print(
        f"Probabilities: {probabilities}\n\nNumbers Generated [Number: Frequency "
        "(Proportion)]"
    )
    for num in random_nums:
        print(f"{num}: {num_counts[num]} times ({num_counts[num] / iterations})")
