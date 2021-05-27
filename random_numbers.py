import random


class RandomNumbers:
    NUMBERS = {
        'small': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        'big': [25, 50, 75, 100],
    }

    @staticmethod
    def get_target_number(low, high):
        """Get the target numbers as a random number anywhere
        between {low} and {high}.
        """
        return random.randint(low, high)

    @staticmethod
    def get_random_selection(big, total=6):
        """This method gets a random selection of numbers from the
        available numbers. The number of "big numbers" must be
        provided as the argument {big}. The parameter {total} is
        optional and set 6 by default (the actual number for the
        official Countdown game).
        """
        assert total - big >= 0
        big_numbers = random.sample(RandomNumbers.NUMBERS['big'], big)
        small_numbers = random.sample(RandomNumbers.NUMBERS['small'], total - big)
        return big_numbers + small_numbers
