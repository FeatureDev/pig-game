# src/dice.py
"""dice.py Provides the Dice class for random dice rolls."""

import random


class Dice:
    """A simple six-sided dice."""

    def roll(self) -> int:
        """Roll the dice and return an integer in [1, 6]."""
        return random.randint(1, 6)

