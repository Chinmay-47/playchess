import random
from typing import List

from playchess.move import Move


def find_random_move(moves: List[Move]) -> Move:
    """Returns a random move from a given list of moves."""

    return random.choice(moves)
