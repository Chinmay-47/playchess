from pprint import pprint
from typing import Optional

from playchess.config import DIMENSIONS


class Board:
    """Class to represent a chess board."""

    def __init__(self):
        self.board = \
            [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]] + \
            [["bp"] * DIMENSIONS] + \
            [[None] * DIMENSIONS] * (DIMENSIONS - 4) + \
            [["wp"] * DIMENSIONS] + \
            [["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.move_log = []

    def print(self) -> None:
        pprint(self.board)

    def moves_made(self, last_n: Optional[int] = None) -> list:
        """Shows moves made previously"""

        if last_n is not None:
            return self.move_log[-last_n:]

        return self.move_log

    @property
    def num_moves_made(self):
        """Shows number of moves made."""

        return len(self.move_log)


def main():
    b = Board()
    b.print()


if __name__ == '__main__':
    main()
